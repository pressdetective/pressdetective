#!/usr/bin/env python3
"""
Deep clean contacts_tagged.csv:
1. Syntax check — remove malformed emails
2. Remove placeholder/template/garbage emails
3. DNS verify every domain (MX then A record, cached per domain)
4. Parallel DNS lookups using ThreadPoolExecutor
5. Improve tags on cleaned data
6. Output: contacts_clean.csv + contacts_removed.csv + clean_report.txt
"""

import csv, re, sys, time
from pathlib import Path
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import dns.resolver, dns.exception
    HAS_DNS = True
except ImportError:
    print("ERROR: pip install dnspython"); sys.exit(1)

BASE = Path(__file__).parent

# ── KNOWN VALID DOMAINS (skip DNS, always pass) ───────────────────────────────
KNOWN_VALID = {
    # Indian government
    'mahapolice.gov.in', 'maharashtra.gov.in', 'nic.in', 'gov.in',
    'bhc.gov.in', 'aij.gov.in', 'goapolice.gov.in', 'gspcb.in',
    'mhcyber.gov.in', 'dcourts.gov.in', 'acbmaharashtra.gov.in',
    'mahacid.gov.in', 'cbi.gov.in',
    # Major global mail providers
    'gmail.com', 'googlemail.com',
    'yahoo.com', 'yahoo.co.in', 'yahoo.in', 'ymail.com',
    'outlook.com', 'hotmail.com', 'hotmail.co.in', 'live.com', 'msn.com',
    'rediffmail.com',
    'icloud.com', 'me.com',
    # Major Indian/international media
    'hindustantimes.com', 'ndtv.com', 'ndtvgroup.com', 'thehindu.com',
    'timesgroup.com', 'indiatimes.com', 'timesofindia.com',
    'indianexpress.com', 'financialexpress.com', 'loksatta.com',
    'mumbaimirror.com', 'mid-day.com', 'midday.com',
    'bbc.co.uk', 'bbc.com', 'reuters.com', 'ap.org', 'afp.com',
    'theprint.in', 'thewire.in', 'scroll.in', 'thequint.com',
    'abp.in', 'abp.com', 'abpnews.in', 'aajtak.com',
    'zee.com', 'zeenews.com', 'zeeentertainment.com',
    'tv9network.com', 'tv9telugu.com',
    'navhindtimes.com', 'herald-goa.com', 'gomantak.com', 'prudentmedia.in',
    'goanews.com',
    # Domains confirmed from case sources
    'santoshsakpal.com', 'madh.co.in', 'martinburnltd.com',
    'savegoa.com', 'videovolunteers.org', 'humantouch.org.in',
    'actforgoa.org', 'goaheritageactiongroup.org',
    'berkeley.edu',
    'amitassociates.co',
    'dalalee.co.uk',
}

# ── PLACEHOLDER / GARBAGE PATTERNS ───────────────────────────────────────────
BAD_PATTERNS = [
    r'^user@mail\.com$',
    r'^example@',
    r'^test@',
    r'^noreply@',
    r'^no-reply@',
    r'^admin@example',
    r'@domain\.com$',
    r'@mail\.com$',
    r'^postmaster@',
    r'^webmaster@',
    r'^info@mail\.',
    r'\s',                          # spaces in email
]

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

# ── DNS RESOLVER ──────────────────────────────────────────────────────────────
resolver = dns.resolver.Resolver()
resolver.timeout = 4
resolver.lifetime = 6
resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1']

def check_domain(domain: str) -> tuple[str, bool, str]:
    """Returns (domain, is_valid, reason)"""
    d = domain.lower()
    # Check known valid (including subdomain match)
    for kd in KNOWN_VALID:
        if d == kd or d.endswith('.' + kd):
            return (d, True, 'known-valid')
    # Try MX first
    try:
        ans = resolver.resolve(d, 'MX', lifetime=5)
        if ans:
            return (d, True, 'mx-ok')
    except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return (d, False, 'no-domain')
    except dns.resolver.NoAnswer:
        pass
    except Exception:
        pass
    # Fallback: A record
    try:
        ans = resolver.resolve(d, 'A', lifetime=5)
        if ans:
            return (d, True, 'a-record-ok')
    except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return (d, False, 'no-domain')
    except dns.resolver.NoAnswer:
        return (d, False, 'no-mx-no-a')
    except Exception as ex:
        return (d, None, f'dns-error:{ex}')
    return (d, False, 'no-mx-no-a')


def is_placeholder(email: str) -> bool:
    for pat in BAD_PATTERNS:
        if re.search(pat, email, re.IGNORECASE):
            return True
    return False


def main():
    src = BASE / 'contacts_tagged.csv'
    rows = list(csv.DictReader(src.open(encoding='utf-8-sig')))
    print(f"Loaded {len(rows)} contacts")

    # ── PASS 1: syntax + placeholder filter ───────────────────────────────
    valid_syntax, rejected = [], []
    for row in rows:
        email = row['email'].strip().lower()
        row['email'] = email
        if not EMAIL_RE.match(email):
            row['reject_reason'] = 'invalid_syntax'
            rejected.append(row)
        elif is_placeholder(email):
            row['reject_reason'] = 'placeholder'
            rejected.append(row)
        else:
            valid_syntax.append(row)

    print(f"After syntax/placeholder filter: {len(valid_syntax)} valid, {len(rejected)} rejected")

    # ── PASS 2: DNS verification per unique domain ─────────────────────────
    domains = set(r['email'].split('@')[1] for r in valid_syntax)
    print(f"Verifying {len(domains)} unique domains via DNS...")

    domain_results = {}
    domain_reasons = {}

    # Split into known (skip) and unknown (check)
    unknown_domains = []
    for d in domains:
        for kd in KNOWN_VALID:
            if d == kd or d.endswith('.' + kd):
                domain_results[d] = True
                domain_reasons[d] = 'known-valid'
                break
        else:
            unknown_domains.append(d)

    print(f"  Known-valid: {len(domain_results)} domains (skipped DNS)")
    print(f"  Need DNS check: {len(unknown_domains)} domains")

    checked = 0
    dead_domains = []

    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(check_domain, d): d for d in unknown_domains}
        for future in as_completed(futures):
            d, ok, reason = future.result()
            domain_results[d] = ok
            domain_reasons[d] = reason
            checked += 1
            if ok is False:
                dead_domains.append((d, reason))
            if checked % 50 == 0:
                print(f"  DNS: {checked}/{len(unknown_domains)} done...")

    print(f"DNS complete. Dead domains: {len(dead_domains)}")
    if dead_domains:
        print("  Removed domains (sample):")
        for d, r in sorted(dead_domains)[:20]:
            print(f"    {d}  [{r}]")

    # ── PASS 3: apply DNS results ──────────────────────────────────────────
    dns_valid, dns_rejected = [], []
    for row in valid_syntax:
        domain = row['email'].split('@')[1]
        ok = domain_results.get(domain)
        if ok is False:
            row['reject_reason'] = f'dead_domain:{domain}'
            dns_rejected.append(row)
        elif ok is None:
            row['reject_reason'] = f'dns_error:{domain}'
            # Keep DNS-error contacts (network issue, not dead domain)
            row['tags'] = row.get('tags','') + '|dns-unconfirmed'
            dns_valid.append(row)
        else:
            row['reject_reason'] = ''
            dns_valid.append(row)

    rejected.extend(dns_rejected)
    print(f"\nFinal count:")
    print(f"  Verified (keep): {len(dns_valid)}")
    print(f"  Rejected (remove): {len(rejected)}")

    # ── Improve tags on clean data ────────────────────────────────────────
    # Re-tag contacts that were auto-tagged as 'unverified' but passed DNS
    for row in dns_valid:
        tags = set(row.get('tags','').split('|'))
        tags.discard('unverified')   # passed DNS, no longer unverified
        tags.discard('')
        if not tags:
            tags.add('general')
        row['tags'] = '|'.join(sorted(tags))

    # ── Write outputs ─────────────────────────────────────────────────────
    fieldnames = list(rows[0].keys())
    if 'reject_reason' not in fieldnames:
        fieldnames.append('reject_reason')

    out_clean = BASE / 'contacts_clean.csv'
    clean_fields = [f for f in fieldnames if f != 'reject_reason']
    with out_clean.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=clean_fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(dns_valid)

    out_removed = BASE / 'contacts_removed.csv'
    with out_removed.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader()
        w.writerows(rejected)

    # ── Report ────────────────────────────────────────────────────────────
    reject_reasons = Counter(r.get('reject_reason','').split(':')[0] for r in rejected)
    dead_domain_counts = Counter()
    for r in rejected:
        reason = r.get('reject_reason','')
        if reason.startswith('dead_domain:'):
            dead_domain_counts[reason.split(':', 1)[1]] += 1

    tag_counts = Counter()
    for r in dns_valid:
        for t in r.get('tags','').split('|'):
            if t:
                tag_counts[t] += 1

    report = f"""Deep Clean Report — PressDetective Contacts
Generated: 2026-06-09
=============================================
Input contacts:    {len(rows)}
Verified (clean):  {len(dns_valid)}
Removed (total):   {len(rejected)}

Rejection breakdown:
  Invalid syntax:  {reject_reasons.get('invalid_syntax', 0)}
  Placeholder:     {reject_reasons.get('placeholder', 0)}
  Dead domain:     {reject_reasons.get('dead_domain', 0)}
  DNS error:       {reject_reasons.get('dns_error', 0)}

Top dead domains removed:
"""
    for dom, cnt in dead_domain_counts.most_common(30):
        report += f"  {dom}: {cnt} addresses\n"

    report += f"\nTag breakdown (clean contacts):\n"
    priority = ['top-priority','police-hq','court-high','anti-corruption','police-special',
                'economic-fraud','police-zone','anti-extortion','crime-branch','cyber-crime',
                'court-lower','court-sessions','court-family','govt-admin','land-records',
                'police-station','press','govt-state','ngo-civic','goa','individual',
                'corporate','dgp-desk','dns-unconfirmed','general']
    for t in priority:
        if t in tag_counts:
            report += f"  {t:<25} {tag_counts[t]}\n"
    for t in sorted(tag_counts):
        if t not in priority and tag_counts[t]:
            report += f"  {t:<25} {tag_counts[t]}\n"

    (BASE / 'clean_report.txt').write_text(report, encoding='utf-8')
    print(report)
    print(f"Clean CSV:   {out_clean}")
    print(f"Removed CSV: {out_removed}")

if __name__ == '__main__':
    t0 = time.time()
    main()
    print(f"\nDone in {time.time()-t0:.1f}s")
