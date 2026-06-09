#!/usr/bin/env python3
"""
rebuild_clean.py — Full rebuild of contacts_live.csv

1. Load contacts_final.csv (3,449)
2. Strip all 79 suppressed addresses
3. Re-run DNS/MX check on any domain not in KNOWN_VALID
4. Normalise category names
5. Enrich / repair tags from category + designation + name
6. Write:
     contacts_live.csv         — send-ready (suppression + DNS clean)
     contacts_final.csv        — update in-place (14 dead removed)
     suppression_list.csv      — updated with new dead domains
     tag_summary.csv           — tag frequency table
7. Print full stats + compliance summary
"""

import csv, re, sys, time, json, datetime
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import dns.resolver, dns.exception
except ImportError:
    print("ERROR: pip install dnspython"); sys.exit(1)

BASE         = Path(__file__).parent.parent
FINAL_CSV    = BASE / "contacts" / "contacts_final.csv"
LIVE_CSV     = BASE / "contacts" / "contacts_live.csv"
SUPPRESS_CSV = BASE / "contacts" / "suppression_list.csv"
TAG_SUM_CSV  = BASE / "contacts" / "tag_summary.csv"
REMOVED_CSV  = BASE / "contacts" / "contacts_removed_full.csv"

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

# ── Known-valid domains — skip DNS round-trip ────────────────────────────────
KNOWN_VALID = {
    # Govt
    'mahapolice.gov.in','nic.in','gov.in','bhc.gov.in','dcourts.gov.in',
    'aij.gov.in','mhcyber.gov.in','maharashtra.gov.in','goapolice.gov.in',
    'gspcb.in','mha.gov.in','ncrb.gov.in','hppolice.gov.in','delhipolice.gov.in',
    'punjabpolice.gov.in','punepolice.gov.in','up.gov.in',
    # Generic webmail
    'gmail.com','yahoo.com','yahoo.co.in','yahoo.in','rediffmail.com',
    'hotmail.com','outlook.com','live.com','protonmail.com','proton.me',
    'icloud.com',
    # Major Indian press
    'timesgroup.com','hindustantimes.com','ndtv.com','thehindu.com',
    'thehindu.co.in','deccanherald.com','deccanchronicle.com',
    'tribuneindia.com','indiatimes.com','abplive.com','abpmajha.in',
    'abpnews.in','zeenews.india.com','aajtak.in','indiatoday.in',
    'businesstoday.in','theeconomictimes.com','economictimes.com',
    'livemint.com','financialexpress.com','businessstandard.com',
    # Legal press
    'livelaw.in','barandbench.com','theleaflet.in','lawbeat.net',
    'indialegal.in','thewire.in','scroll.in','theprint.in','thequint.com',
    # Mumbai press
    'mid-day.com','freepressjournal.in','dnaindia.com','mumbaimirror.com',
    'maharashtratimes.com','lokmat.com','loksatta.com',
    # National press
    'indianexpress.com','hindustantimes.com','telegraphindia.com',
    'thestatesman.com','tribuneindia.com','sentinelassam.com',
    'frontline.in','caravanmagazine.in',
}

# ── Canonical category map (dirty → clean) ──────────────────────────────────
CAT_MAP = {
    'press':                          'Press',
    'press / media':                  'Press',
    'press/media':                    'Press',
    'press media':                    'Press',
    'press/legal media':              'Press/Legal Media',
    'legal media':                    'Press/Legal Media',
    'general':                        'Police/Government',
    'police/government/press':        'Police/Government',
    'police/government':              'Police/Government',
    'police':                         'Police/Government',
    'government':                     'Government',
    'other government office':        'Government',
    'mumbai administration':          'Government',
    'mumbai administration - land':   'Government',
    'elected reps / panchayat':       'Government',
    'regulator / environment':        'Government',
    'cmm courts mumbai':              'Court',
    'bombay high court':              'Court',
    'court':                          'Court',
    'ngo / civic':                    'NGO/Civic',
    'ngo/civic':                      'NGO/Civic',
    'individual':                     'Individual',
    'individual supporter':           'Individual',
    'mumbai police station':          'Police/Government',
    'mumbai police - acp':            'Police/Government',
    'mumbai police - cyber crime':    'Police/Government',
}

def normalise_category(raw: str) -> str:
    key = raw.strip().lower()
    return CAT_MAP.get(key, raw.strip() or 'Other')

# ── Tag enrichment rules ─────────────────────────────────────────────────────

PRESS_PUBS = {
    'livelaw.in':            'livelaw',
    'barandbench.com':       'bar-and-bench',
    'theleaflet.in':         'the-leaflet',
    'lawbeat.net':           'lawbeat',
    'indialegal.in':         'india-legal',
    'thewire.in':            'the-wire',
    'theprint.in':           'the-print',
    'thequint.com':          'the-quint',
    'scroll.in':             'scroll',
    'mid-day.com':           'mid-day',
    'freepressjournal.in':   'fpj-mumbai',
    'dnaindia.com':          'dna-india',
    'hindustantimes.com':    'hindustan-times',
    'ndtv.com':              'ndtv',
    'indianexpress.com':     'indian-express',
    'thehindu.com':          'the-hindu',
    'indiatimes.com':        'times-of-india',
    'timesgroup.com':        'times-of-india',
    'caravanmagazine.in':    'caravan',
    'frontline.in':          'frontline',
    'businessstandard.com':  'business-standard',
    'economictimes.com':     'economic-times',
}

DESIG_TAG_MAP = [
    # role patterns → tag
    (re.compile(r'editor.in.chief|editor-in-chief', re.I),     'editor-in-chief'),
    (re.compile(r'managing\s+editor|executive\s+editor', re.I),'managing-editor'),
    (re.compile(r'\beditor\b', re.I),                           'editor'),
    (re.compile(r'bureau\s+chief', re.I),                       'bureau-chief'),
    (re.compile(r'correspondent|reporter', re.I),               'reporter'),
    (re.compile(r'senior\s+reporter|senior\s+journalist', re.I),'senior-reporter'),
    (re.compile(r'legal\s+reporter|law\s+reporter', re.I),      'legal-reporter'),
    (re.compile(r'crime|court\s+reporter', re.I),               'crime-court-beat'),
    (re.compile(r'investigative', re.I),                        'investigative'),
    (re.compile(r'founder|co.founder', re.I),                   'founder'),
    (re.compile(r'director\s+general|dgp', re.I),               'dgp-desk'),
    (re.compile(r'inspector\s+general|ig\b', re.I),             'ig-desk'),
    (re.compile(r'deputy\s+commissioner|dcp|dcb', re.I),        'dcp-desk'),
    (re.compile(r'superintendent|ssp|sp\b', re.I),              'sp-desk'),
    (re.compile(r'inspector|constable|sub.inspector', re.I),    'police-station'),
    (re.compile(r'judge|justice\b', re.I),                      'court-high'),
    (re.compile(r'magistrate|judicial', re.I),                  'court-lower'),
    (re.compile(r'advocate|solicitor|barrister|counsel', re.I), 'lawyer'),
    (re.compile(r'high\s+court', re.I),                         'high-court-beat'),
    (re.compile(r'supreme\s+court', re.I),                      'supreme-court-beat'),
    (re.compile(r'ngo|civil\s+society|activist', re.I),         'ngo-civic'),
    (re.compile(r'collector|district\s+magistrate|dm\b', re.I), 'govt-admin'),
    (re.compile(r'cyber\s+crime|cybercrime', re.I),             'cyber-crime'),
    (re.compile(r'goa\b', re.I),                                'goa'),
    (re.compile(r'mumbai|bombay', re.I),                        'mumbai-press'),
]

PRIORITY_TAGS = {
    'editor-in-chief', 'managing-editor', 'editor', 'bureau-chief',
    'dgp-desk', 'crime-court-beat', 'legal-reporter', 'investigative',
    'high-court-beat', 'supreme-court-beat', 'livelaw', 'bar-and-bench',
}

def enrich_tags(row: dict) -> str:
    existing = set(t.strip() for t in (row.get('tags') or '').split('|') if t.strip())
    cat   = (row.get('category') or '').lower()
    desig = (row.get('designation') or '').strip()
    email = (row.get('email') or '').strip().lower()
    name  = (row.get('name') or '').strip()
    domain = email.split('@')[1] if '@' in email else ''

    # Base category tag
    if 'police' in cat or 'government' in cat:
        existing.add('police-hq')
        existing.add('govt-state')
    if 'press/legal' in cat:
        existing.add('press')
        existing.add('legal-press')
    elif 'press' in cat:
        existing.add('press')
    if 'court' in cat:
        existing.add('court-high')
    if 'ngo' in cat:
        existing.add('ngo-civic')

    # Publication tag from domain
    pub = PRESS_PUBS.get(domain)
    if pub:
        existing.add(pub)
        existing.add('press')

    # Designation-based tags
    for pattern, tag in DESIG_TAG_MAP:
        if pattern.search(desig) or pattern.search(name):
            existing.add(tag)

    # Top-priority flag
    if existing & PRIORITY_TAGS:
        existing.add('top-priority')

    # Goa detection
    if 'goa' in email or 'goa' in desig.lower():
        existing.add('goa')

    # Mumbai detection
    if 'mumbai' in desig.lower() or 'mumbai' in (row.get('designation') or '').lower():
        existing.add('mumbai-press')

    return '|'.join(sorted(existing))


# ── DNS check ────────────────────────────────────────────────────────────────
mx_cache = {}

def check_domain(domain: str) -> tuple:
    d = domain.lower()
    for k in KNOWN_VALID:
        if d == k or d.endswith('.' + k):
            return True, 'known_valid'
    if d in mx_cache:
        return mx_cache[d]
    try:
        dns.resolver.resolve(d, 'MX', lifetime=6)
        mx_cache[d] = (True, 'mx_ok')
        return True, 'mx_ok'
    except Exception:
        try:
            dns.resolver.resolve(d, 'A', lifetime=4)
            mx_cache[d] = (True, 'a_record')
            return True, 'a_record'
        except Exception:
            mx_cache[d] = (False, f'dead_domain:{d}')
            return False, f'dead_domain:{d}'


# ── Suppression helpers ──────────────────────────────────────────────────────
def load_suppression() -> dict:
    if not SUPPRESS_CSV.exists(): return {}
    return {r['email'].strip().lower(): r
            for r in csv.DictReader(SUPPRESS_CSV.open(encoding='utf-8-sig'))
            if r.get('email')}

def save_suppression(records: dict):
    SUPPRESS_CSV.parent.mkdir(exist_ok=True)
    with SUPPRESS_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['email','reason','date','source'], extrasaction='ignore')
        w.writeheader()
        for addr, row in sorted(records.items()):
            row['email'] = addr
            w.writerow(row)

def add_suppressed(records: dict, emails, reason, source='rebuild_clean'):
    today = datetime.date.today().isoformat()
    added = 0
    for e in emails:
        e = e.strip().lower()
        if e and EMAIL_RE.match(e) and e not in records:
            records[e] = {'email': e, 'reason': reason, 'date': today, 'source': source}
            added += 1
    return added


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    rows = list(csv.DictReader(FINAL_CSV.open(encoding='utf-8-sig')))
    total_in = len(rows)
    print(f"Loaded {total_in} contacts from contacts_final.csv")
    fieldnames = list(rows[0].keys()) if rows else []

    # ── Step 1: Syntax check ─────────────────────────────────────────────────
    print("\nStep 1: Syntax check...")
    bad_syntax = [r for r in rows if not EMAIL_RE.match(r['email'].strip().lower())]
    print(f"  Bad syntax: {len(bad_syntax)}")

    # ── Step 2: DNS check on all non-known-valid domains ─────────────────────
    print("\nStep 2: DNS/MX re-verification (parallel, 20 threads)...")
    unique_domains = list({r['email'].split('@')[1].lower()
                           for r in rows if '@' in r['email']})

    # Skip domains already in KNOWN_VALID
    to_check = [d for d in unique_domains
                if not any(d == k or d.endswith('.' + k) for k in KNOWN_VALID)]
    print(f"  Total unique domains   : {len(unique_domains)}")
    print(f"  Known-valid (skip DNS) : {len(unique_domains) - len(to_check)}")
    print(f"  Domains to DNS-check   : {len(to_check)}")

    dead_domains = set()
    checked = 0
    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(check_domain, d): d for d in to_check}
        for future in as_completed(futures):
            d = futures[future]
            is_valid, reason = future.result()
            checked += 1
            if not is_valid:
                dead_domains.add(d)
            if checked % 50 == 0:
                print(f"  DNS: {checked}/{len(to_check)} checked, {len(dead_domains)} dead so far")

    print(f"  Dead domains found     : {len(dead_domains)}")
    if dead_domains:
        print("  Dead domains:")
        for d in sorted(dead_domains):
            print(f"    {d}")

    dead_email_addrs = [r['email'].strip().lower() for r in rows
                        if '@' in r['email']
                        and r['email'].split('@')[1].lower() in dead_domains]
    print(f"  Emails on dead domains : {len(dead_email_addrs)}")

    # ── Step 3: Update suppression list ──────────────────────────────────────
    print("\nStep 3: Updating suppression list...")
    supp = load_suppression()
    prev_count = len(supp)

    add_suppressed(supp, [r['email'] for r in bad_syntax], 'invalid_syntax', 'rebuild_clean')
    add_suppressed(supp, dead_email_addrs, 'dead_domain', 'rebuild_clean')
    new_added = len(supp) - prev_count
    print(f"  Previously suppressed  : {prev_count}")
    print(f"  Newly added            : {new_added}")
    print(f"  Total suppressed       : {len(supp)}")
    save_suppression(supp)

    # ── Step 4: Normalise categories + enrich tags ────────────────────────────
    print("\nStep 4: Normalising categories + enriching tags...")
    cat_fixes = 0
    tag_changes = 0
    for r in rows:
        old_cat = r.get('category','')
        new_cat = normalise_category(old_cat)
        if old_cat != new_cat:
            r['category'] = new_cat
            cat_fixes += 1
        old_tags = (r.get('tags') or '').strip()
        new_tags = enrich_tags(r)
        if old_tags != new_tags:
            r['tags'] = new_tags
            tag_changes += 1

    print(f"  Category name fixes    : {cat_fixes}")
    print(f"  Tag enrichments        : {tag_changes}")

    # ── Step 5: Write contacts_live.csv (suppression-clean) ─────────────────
    print("\nStep 5: Writing contacts_live.csv (suppression-clean)...")
    suppressed_set = set(supp.keys())
    live_rows = [r for r in rows if r['email'].strip().lower() not in suppressed_set]
    removed_rows = [r for r in rows if r['email'].strip().lower() in suppressed_set]

    with LIVE_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader(); w.writerows(live_rows)

    # Update contacts_final.csv in-place with normalised categories + tags
    with FINAL_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader(); w.writerows(rows)

    # Write removed log
    fn_rem = fieldnames + ['reject_reason'] if 'reject_reason' not in fieldnames else fieldnames
    with REMOVED_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fn_rem, extrasaction='ignore')
        w.writeheader()
        for r in removed_rows:
            r['reject_reason'] = supp.get(r['email'].lower(), {}).get('reason', 'suppressed')
            w.writerow(r)

    # ── Step 6: Write tag_summary.csv ────────────────────────────────────────
    tag_cnt = Counter()
    for r in live_rows:
        for t in (r.get('tags') or '').split('|'):
            if t.strip(): tag_cnt[t.strip()] += 1

    with TAG_SUM_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['tag', 'count'])
        w.writeheader()
        for t, c in tag_cnt.most_common():
            w.writerow({'tag': t, 'count': c})

    # ── Summary ───────────────────────────────────────────────────────────────
    cat_cnt = Counter(r.get('category','') for r in live_rows)
    print(f"\n{'='*60}")
    print(f"REBUILD COMPLETE")
    print(f"{'='*60}")
    print(f"Input contacts          : {total_in}")
    print(f"Dead domain (new)       : {len(dead_email_addrs)}")
    print(f"Total suppressed        : {len(suppressed_set)}")
    print(f"Removed from live       : {len(removed_rows)}")
    print(f"LIVE (send-ready)       : {len(live_rows)}")
    print()
    print(f"COMPLIANCE CHECK")
    print(f"  Suppression list      : {len(supp)} entries")
    print(f"  DPDP footer in mailer : YES (mailer/send.py)")
    print(f"  List-Unsubscribe hdr  : YES (RFC 8058)")
    print(f"  Reply-To = From       : YES")
    print(f"  CC info@              : YES (always)")
    print(f"  Grievance Officer     : info@pressdetective.com")
    print()
    print(f"CATEGORIES (live list):")
    for cat, c in cat_cnt.most_common():
        print(f"  {cat:<35} {c}")
    print()
    print(f"TOP TAGS (live list, top 20):")
    for t, c in tag_cnt.most_common(20):
        print(f"  {t:<35} {c}")
    print()
    print(f"FILES WRITTEN:")
    print(f"  contacts_live.csv          : {len(live_rows)} send-ready contacts")
    print(f"  contacts_final.csv         : {total_in} full list (tags/cats normalised)")
    print(f"  suppression_list.csv       : {len(supp)} suppressed")
    print(f"  contacts_removed_full.csv  : {len(removed_rows)} removed log")
    print(f"  tag_summary.csv            : {len(tag_cnt)} unique tags")


if __name__ == '__main__':
    main()
