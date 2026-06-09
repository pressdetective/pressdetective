#!/usr/bin/env python3
"""
Verify contacts_master.csv by:
1. Syntax check
2. MX record lookup per domain (cached — only one lookup per unique domain)
3. Filter out entries where domain has no MX records
Outputs: contacts_verified.csv + contacts_rejected.csv + verification_report.txt
"""

import csv, re, sys, time
from collections import defaultdict
from pathlib import Path

try:
    import dns.resolver
    import dns.exception
    HAS_DNS = True
except ImportError:
    HAS_DNS = False
    print("WARNING: dnspython not available — skipping MX check")

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

# Domains we know are valid even if DNS is slow/blocked (well-known govt domains)
KNOWN_VALID_DOMAINS = {
    'mahapolice.gov.in', 'nic.in', 'gov.in', 'bhc.gov.in', 'dcourts.gov.in',
    'aij.gov.in', 'mhcyber.gov.in', 'maharashtra.gov.in', 'goapolice.gov.in',
    'gspcb.in', 'gmail.com', 'yahoo.com', 'yahoo.co.in', 'yahoo.in',
    'rediffmail.com', 'hotmail.com', 'outlook.com', 'live.com',
    'timesgroup.com', 'hindustantimes.com', 'ndtv.com', 'thehindu.com',
    'thehindu.co.in', 'deccanherald.com', 'deccanchronicle.com',
    'tribuneindia.com', 'indiatimes.com', 'abplive.com',
    'navhindtimes.com', 'herald-goa.com', 'gomantak.com', 'prudentmedia.in',
    'goanews.com', 'santoshsakpal.com', 'madh.co.in', 'martinburnltd.com',
}

mx_cache = {}  # domain -> True/False/None (None = could not check)

def check_syntax(email):
    return bool(EMAIL_RE.match(email))

def get_domain(email):
    return email.split('@')[1].lower() if '@' in email else ''

def has_mx(domain):
    if domain in mx_cache:
        return mx_cache[domain]
    # Check known valid first
    for known in KNOWN_VALID_DOMAINS:
        if domain == known or domain.endswith('.' + known):
            mx_cache[domain] = True
            return True
    if not HAS_DNS:
        mx_cache[domain] = None
        return None
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=5)
        result = len(answers) > 0
        mx_cache[domain] = result
        return result
    except (dns.exception.DNSException, Exception):
        # Try A record fallback
        try:
            dns.resolver.resolve(domain, 'A', lifetime=5)
            mx_cache[domain] = True
            return True
        except Exception:
            mx_cache[domain] = False
            return False

def main():
    base = Path(__file__).parent
    src = base / 'contacts_master.csv'
    dst_ok = base / 'contacts_verified.csv'
    dst_bad = base / 'contacts_rejected.csv'
    report = base / 'verification_report.txt'

    rows = list(csv.DictReader(src.open(encoding='utf-8-sig')))
    total = len(rows)
    print(f"Loaded {total} contacts")

    verified, rejected = [], []
    domains_checked = 0
    domain_results = {}

    for i, row in enumerate(rows):
        email = row['email'].strip().lower()
        row['email'] = email

        # 1. Syntax
        if not check_syntax(email):
            row['reject_reason'] = 'invalid_syntax'
            rejected.append(row)
            continue

        # 2. MX check (one per domain)
        domain = get_domain(email)
        if domain not in domain_results:
            result = has_mx(domain)
            domain_results[domain] = result
            domains_checked += 1
            if domains_checked % 50 == 0:
                print(f"  Checked {domains_checked} domains, {i+1}/{total} emails processed...")

        mx_ok = domain_results[domain]
        if mx_ok is False:
            row['reject_reason'] = 'no_mx_record'
            rejected.append(row)
        else:
            row['reject_reason'] = ''
            verified.append(row)

    # Write outputs
    fieldnames = list(rows[0].keys()) + (['reject_reason'] if 'reject_reason' not in rows[0] else [])

    with dst_ok.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=[k for k in fieldnames if k != 'reject_reason'])
        w.writeheader()
        w.writerows({k: v for k, v in r.items() if k != 'reject_reason'} for r in verified)

    with dst_bad.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rejected)

    # Stats by reject reason
    reasons = defaultdict(int)
    for r in rejected:
        reasons[r['reject_reason']] += 1

    # Stats by domain for no_mx
    bad_domains = defaultdict(int)
    for r in rejected:
        if r['reject_reason'] == 'no_mx_record':
            bad_domains[get_domain(r['email'])] += 1

    report_text = f"""Email Verification Report
Generated: 2026-06-09
=============================
Total input:      {total}
Verified (pass):  {len(verified)}
Rejected (fail):  {len(rejected)}

Rejection reasons:
  invalid_syntax:  {reasons['invalid_syntax']}
  no_mx_record:    {reasons['no_mx_record']}

Top rejected domains (no MX):
"""
    for dom, cnt in sorted(bad_domains.items(), key=lambda x: -x[1])[:30]:
        report_text += f"  {dom}: {cnt} addresses\n"

    report.write_text(report_text, encoding='utf-8')
    print(report_text)
    print(f"Verified CSV → {dst_ok}")
    print(f"Rejected CSV → {dst_bad}")

if __name__ == '__main__':
    main()
