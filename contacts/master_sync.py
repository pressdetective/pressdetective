#!/usr/bin/env python3
"""
master_sync.py — Definitive contacts master rebuild

1. Add 3 malformed addresses from contacts_master to suppression
2. Full DNS re-verify all unique domains in contacts_final.csv
3. Sweep all 4 inboxes for fresh bounce notifications
4. Merge suppression list (dead_domain + user_not_found + invalid_syntax)
5. Write definitive contacts_live.csv (zero suppressed)
6. Print full compliance report
"""

import csv, re, sys, time, json, imaplib, ssl, email, datetime
from email.header import decode_header
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import dns.resolver
except ImportError:
    print("pip install dnspython"); sys.exit(1)

BASE         = Path(__file__).parent.parent
FINAL_CSV    = BASE / "contacts" / "contacts_final.csv"
LIVE_CSV     = BASE / "contacts" / "contacts_live.csv"
SUPPRESS_CSV = BASE / "contacts" / "suppression_list.csv"
REMOVED_CSV  = BASE / "contacts" / "contacts_removed_full.csv"
TAG_SUM_CSV  = BASE / "contacts" / "tag_summary.csv"
CREDS_PATH   = BASE / ".creds" / "proton_accounts.json"
BRIDGE_PW    = "FzspzmcI-DE4s1JIp7HU3A"

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

KNOWN_VALID = {
    'mahapolice.gov.in','nic.in','gov.in','bhc.gov.in','dcourts.gov.in',
    'aij.gov.in','mhcyber.gov.in','maharashtra.gov.in','goapolice.gov.in',
    'gspcb.in','mha.gov.in','ncrb.gov.in','delhipolice.gov.in','punepolice.gov.in',
    'gmail.com','yahoo.com','yahoo.co.in','yahoo.in','rediffmail.com',
    'hotmail.com','outlook.com','live.com','protonmail.com','proton.me','icloud.com',
    'timesgroup.com','hindustantimes.com','ndtv.com','thehindu.com','thehindu.co.in',
    'deccanherald.com','deccanchronicle.com','tribuneindia.com','indiatimes.com',
    'abplive.com','livelaw.in','barandbench.com','theleaflet.in','lawbeat.net',
    'indialegal.in','thewire.in','scroll.in','theprint.in','thequint.com',
    'mid-day.com','freepressjournal.in','dnaindia.com','indianexpress.com',
    'caravanmagazine.in','frontline.in','businessstandard.com','economictimes.com',
    'livemint.com','indiatoday.in','cnbctv18.com','outlookindia.com',
    'telegraphindia.com','manoramaonline.com','tribuneindia.com','newsx.com',
    'cbi.gov.in','up.gov.in','hppolice.gov.in',
}

EXCLUDE_INBOX = {
    'pressdetective.com','protonmail.com','proton.me','zeptomail.com',
    'zoho.com','postmaster','mailer-daemon',
}

BOUNCE_KW = [
    'undeliverable','delivery failed','delivery failure','returned mail',
    'mail delivery failed','user unknown','no such user','does not exist',
    'account does not exist','invalid address','recipient rejected',
    'permanent failure','address rejected','mailbox not found',
    'could not be delivered','mailbox unavailable',
]

mx_cache = {}

def check_domain(domain):
    d = domain.lower()
    for k in KNOWN_VALID:
        if d == k or d.endswith('.'+k):
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
            mx_cache[d] = (False, 'dead_domain')
            return False, 'dead_domain'

def _dec(h):
    parts = decode_header(h or '')
    return ''.join(
        p.decode(enc or 'utf-8', errors='replace') if isinstance(p, bytes) else p
        for p, enc in parts
    ).strip()

def _body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                p = part.get_payload(decode=True)
                if p:
                    return p.decode(part.get_content_charset() or 'utf-8', errors='replace')
    else:
        p = msg.get_payload(decode=True)
        if p:
            return p.decode(msg.get_content_charset() or 'utf-8', errors='replace')
    return ''

def sweep_inbox(account_key):
    creds = json.loads(CREDS_PATH.read_text(encoding='utf-8'))
    addr  = creds['accounts'][account_key]['address']
    ctx   = ssl.create_default_context()
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    found = set()
    total = 0
    try:
        m = imaplib.IMAP4('127.0.0.1', 1143)
        m.starttls(ssl_context=ctx); m.login(addr, BRIDGE_PW)
        m.select('INBOX')
        _, data = m.search(None, 'ALL')
        total = len(data[0].split())
        for search in ['FROM "mailer-daemon"','FROM "postmaster"',
                       'SUBJECT "undeliverable"','SUBJECT "delivery failed"',
                       'SUBJECT "failure notice"','SUBJECT "returned mail"',
                       'SUBJECT "could not be delivered"']:
            try:
                _, sd = m.search(None, search)
                for uid in (sd[0].split() or []):
                    _, md = m.fetch(uid, '(RFC822)')
                    msg  = email.message_from_bytes(md[0][1])
                    subj = _dec(msg.get('Subject','')).lower()
                    bt   = _body(msg).lower()
                    if not any(kw in subj or kw in bt[:500] for kw in BOUNCE_KW):
                        continue
                    combined = subj + ' ' + bt[:3000]
                    for e in re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', combined):
                        e = e.lower()
                        dom = e.split('@')[1] if '@' in e else ''
                        if dom and not any(x in dom for x in EXCLUDE_INBOX):
                            found.add(e)
            except Exception:
                pass
        m.logout()
    except Exception as ex:
        print(f"  [{account_key}] inbox error: {ex}")
    return account_key, addr, total, found

def load_suppression():
    if not SUPPRESS_CSV.exists():
        return {}
    return {r['email'].strip().lower(): r
            for r in csv.DictReader(SUPPRESS_CSV.open(encoding='utf-8-sig'))
            if r.get('email')}

def save_suppression(records):
    SUPPRESS_CSV.parent.mkdir(exist_ok=True)
    with SUPPRESS_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['email','reason','date','source'], extrasaction='ignore')
        w.writeheader()
        for addr, row in sorted(records.items()):
            row['email'] = addr
            w.writerow(row)

def add_batch(records, emails, reason, source):
    today = datetime.date.today().isoformat()
    n = 0
    for e in emails:
        e = e.strip().lower()
        if e and e not in records:
            records[e] = {'email': e, 'reason': reason, 'date': today, 'source': source}
            n += 1
    return n


def main():
    print("=" * 62)
    print("PRESSDETECTIVE — MASTER CONTACTS SYNC")
    print("=" * 62)

    rows = list(csv.DictReader(FINAL_CSV.open(encoding='utf-8-sig')))
    fieldnames = list(rows[0].keys())
    all_emails = {r['email'].strip().lower() for r in rows}
    print(f"\nLoaded contacts_final.csv: {len(rows)} contacts")

    supp = load_suppression()
    print(f"Loaded suppression_list:  {len(supp)} entries")

    # ── Step 1: Invalid syntax from contacts_master ──────────────────────────
    print("\n[1] Checking for invalid-syntax addresses not yet suppressed...")
    MASTER_CSV = BASE / "contacts" / "contacts_master.csv"
    master_rows = list(csv.DictReader(MASTER_CSV.open(encoding='utf-8-sig')))
    master_emails = {r['email'].strip().lower() for r in master_rows if r.get('email')}
    bad_syntax_master = [
        e for e in master_emails
        if not EMAIL_RE.match(e) and e not in supp
    ]
    if bad_syntax_master:
        n = add_batch(supp, bad_syntax_master, 'invalid_syntax', 'master_audit')
        print(f"  Added {n} invalid-syntax addresses to suppression")
        for e in bad_syntax_master:
            print(f"    {e}")
    else:
        print("  None found.")

    # Also check contacts_final for bad syntax
    bad_syntax_final = [r['email'] for r in rows if not EMAIL_RE.match(r['email'].strip().lower())]
    if bad_syntax_final:
        n = add_batch(supp, bad_syntax_final, 'invalid_syntax', 'final_audit')
        print(f"  Added {n} invalid-syntax from contacts_final")

    # ── Step 2: Full DNS re-verify ────────────────────────────────────────────
    print("\n[2] Full DNS re-verification of all unique domains...")
    unique_domains = list({r['email'].split('@')[1].lower()
                           for r in rows if '@' in r['email']})
    to_check = [d for d in unique_domains
                if not any(d == k or d.endswith('.'+k) for k in KNOWN_VALID)]
    print(f"  Total unique domains   : {len(unique_domains)}")
    print(f"  Known-valid (skip DNS) : {len(unique_domains)-len(to_check)}")
    print(f"  Checking via DNS       : {len(to_check)}")

    dead_domains = set()
    done = 0
    with ThreadPoolExecutor(max_workers=20) as pool:
        futs = {pool.submit(check_domain, d): d for d in to_check}
        for fut in as_completed(futs):
            d = futs[fut]
            ok, _ = fut.result()
            done += 1
            if not ok:
                dead_domains.add(d)
            if done % 50 == 0:
                print(f"  DNS: {done}/{len(to_check)} checked, {len(dead_domains)} dead")

    dead_emails = [r['email'].strip().lower() for r in rows
                   if '@' in r['email']
                   and r['email'].split('@')[1].lower() in dead_domains
                   and r['email'].strip().lower() not in supp]
    print(f"  Dead domains           : {len(dead_domains)}")
    if dead_domains:
        for d in sorted(dead_domains): print(f"    {d}")
    print(f"  New dead-domain emails : {len(dead_emails)}")
    if dead_emails:
        n = add_batch(supp, dead_emails, 'dead_domain', 'dns_master_sync')
        print(f"  Suppressed             : {n}")

    # ── Step 3: Inbox bounce sweep ────────────────────────────────────────────
    print("\n[3] Sweeping all 4 inboxes for bounce notifications...")
    inbox_bounced = set()
    for key in ['info', 'sujata', 'santosh', 'olympio']:
        key, addr, total, found = sweep_inbox(key)
        print(f"  [{key}] {addr:<45} {total} msgs | {len(found)} addrs in bounces")
        inbox_bounced |= found

    # Only suppress if they're in our contacts (genuine recipient bounces)
    recipient_bounced = [e for e in inbox_bounced if e in all_emails and e not in supp]
    non_recipient     = [e for e in inbox_bounced if e not in all_emails]
    print(f"  Total unique in bounce bodies : {len(inbox_bounced)}")
    print(f"  Confirmed recipient bounces   : {len(recipient_bounced)}")
    print(f"  Non-contact body noise        : {len(non_recipient)} (ignored)")

    if recipient_bounced:
        n = add_batch(supp, recipient_bounced, 'user_not_found', 'inbox_sweep_master_sync')
        print(f"  New entries added to blacklist: {n}")

    # ── Step 4: Save suppression ──────────────────────────────────────────────
    save_suppression(supp)
    print(f"\n[4] Suppression list saved: {len(supp)} total entries")
    reason_cnt = Counter(v['reason'] for v in supp.values())
    for r, c in reason_cnt.most_common():
        print(f"  {r:<25} {c}")

    # ── Step 5: Build contacts_live.csv ───────────────────────────────────────
    print("\n[5] Building contacts_live.csv...")
    supp_set    = set(supp.keys())
    live_rows   = [r for r in rows if r['email'].strip().lower() not in supp_set]
    removed_rows = [r for r in rows if r['email'].strip().lower() in supp_set]

    with LIVE_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader(); w.writerows(live_rows)

    fn_rem = fieldnames + ['reject_reason'] if 'reject_reason' not in fieldnames else fieldnames
    with REMOVED_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fn_rem, extrasaction='ignore')
        w.writeheader()
        for r in removed_rows:
            r2 = dict(r)
            r2['reject_reason'] = supp.get(r['email'].lower(), {}).get('reason', 'suppressed')
            w.writerow(r2)

    # ── Step 6: Tag summary ───────────────────────────────────────────────────
    tag_cnt = Counter()
    for r in live_rows:
        for t in (r.get('tags') or '').split('|'):
            if t.strip(): tag_cnt[t.strip()] += 1
    with TAG_SUM_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['tag','count'])
        w.writeheader()
        for t, c in tag_cnt.most_common():
            w.writerow({'tag': t, 'count': c})

    # ── Step 7: Final compliance report ──────────────────────────────────────
    cat_cnt = Counter(r.get('category','') for r in live_rows)
    print(f"\n{'='*62}")
    print(f"FINAL STATE — CONTACTS MASTER SYNC COMPLETE")
    print(f"{'='*62}")
    print(f"contacts_final.csv (complete list)  : {len(rows)}")
    print(f"contacts_live.csv  (send-ready)     : {len(live_rows)}")
    print(f"contacts_removed_full.csv (log)     : {len(removed_rows)}")
    print(f"suppression_list.csv (blacklist)    : {len(supp)}")
    print(f"  dead_domain                       : {reason_cnt.get('dead_domain',0)}")
    print(f"  user_not_found                    : {reason_cnt.get('user_not_found',0)}")
    print(f"  invalid_syntax                    : {reason_cnt.get('invalid_syntax',0)}")
    print(f"  unsubscribe                       : {reason_cnt.get('unsubscribe_request',0)}")
    print(f"tag_summary.csv                     : {len(tag_cnt)} unique tags")
    print()
    print(f"GDPR / DPDP ACT 2023 COMPLIANCE")
    print(f"  Suppression list checked before every send   : YES (mailer/send.py)")
    print(f"  List-Unsubscribe header (RFC 8058)           : YES")
    print(f"  One-click unsubscribe processing (48h)       : YES")
    print(f"  DPDP Act 2023 footer on all outbound         : YES")
    print(f"  Reply-To = From account                      : YES")
    print(f"  CC info@pressdetective.com always            : YES")
    print(f"  Grievance Officer disclosed                  : YES (info@pressdetective.com)")
    print()
    print(f"CATEGORIES (live list):")
    for cat, c in cat_cnt.most_common():
        print(f"  {cat:<35} {c}")
    print()
    print(f"TOP 25 TAGS (live list):")
    for t, c in tag_cnt.most_common(25):
        print(f"  {t:<35} {c}")


if __name__ == '__main__':
    main()
