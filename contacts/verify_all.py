#!/usr/bin/env python3
"""
Full email verification pass on contacts_final.csv.
1. Syntax check
2. DNS / MX check (cached per domain)
3. Inbox sweep — check all 4 ProtonMail accounts for bounce notifications
4. Add all bad addresses to suppression_list.csv (blacklist)
5. Write contacts_live.csv (clean, send-ready)

Usage:
    python -m contacts.verify_all
"""

import csv, re, sys, time, json, imaplib, ssl, email
from email.header import decode_header
from pathlib import Path
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime

try:
    import dns.resolver, dns.exception
except ImportError:
    print("ERROR: pip install dnspython"); sys.exit(1)

BASE          = Path(__file__).parent.parent
CONTACTS_CSV  = BASE / "contacts" / "contacts_final.csv"
LIVE_CSV      = BASE / "contacts" / "contacts_live.csv"
REMOVED_CSV   = BASE / "contacts" / "contacts_removed_full.csv"
SUPPRESS_CSV  = BASE / "contacts" / "suppression_list.csv"
CREDS_PATH    = BASE / ".creds" / "proton_accounts.json"
BRIDGE_PW     = "FzspzmcI-DE4s1JIp7HU3A"

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

# Domains we know are valid — skip DNS query
KNOWN_VALID = {
    'mahapolice.gov.in','nic.in','gov.in','bhc.gov.in','dcourts.gov.in',
    'aij.gov.in','mhcyber.gov.in','maharashtra.gov.in','goapolice.gov.in',
    'gspcb.in','gmail.com','yahoo.com','yahoo.co.in','yahoo.in',
    'rediffmail.com','hotmail.com','outlook.com','live.com',
    'timesgroup.com','hindustantimes.com','ndtv.com','thehindu.com',
    'deccanherald.com','deccanchronicle.com','tribuneindia.com',
    'indiatimes.com','abplive.com','livelaw.in','barandbench.com',
    'theleaflet.in','lawbeat.net','indialegal.in','thehindu.co.in',
    'thewire.in','scroll.in','theprint.in','thequint.com',
    'mid-day.com','freepressjournal.in','dnaindia.com',
    'indianexpress.com','protonmail.com','proton.me',
}

mx_cache = {}

def check_domain(domain: str) -> tuple[bool, str]:
    """Returns (is_valid, reason)"""
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


# ── Inbox sweep for bounce notifications ─────────────────────────────────────

BOUNCE_KEYWORDS = [
    'undeliverable', 'delivery failed', 'delivery failure',
    'returned mail', 'mail delivery failed', 'bounce',
    'user unknown', 'no such user', 'does not exist',
    'account does not exist', 'invalid address', 'recipient rejected',
    'permanent failure', 'address rejected',
]

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
                if p: return p.decode(part.get_content_charset() or 'utf-8', errors='replace')
    else:
        p = msg.get_payload(decode=True)
        if p: return p.decode(msg.get_content_charset() or 'utf-8', errors='replace')
    return ''

def sweep_inbox_for_bounces(account_key: str) -> list[str]:
    """Returns list of bounced email addresses found in inbox notifications."""
    creds = json.loads(CREDS_PATH.read_text(encoding='utf-8'))
    addr  = creds['accounts'][account_key]['address']
    ctx   = ssl.create_default_context()
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

    bounced = []
    try:
        m = imaplib.IMAP4('127.0.0.1', 1143)
        m.starttls(ssl_context=ctx)
        m.login(addr, BRIDGE_PW)
        m.select('INBOX')

        # Search for common mailer-daemon / postmaster bounce subjects
        for search in ['FROM "mailer-daemon"', 'FROM "postmaster"', 'SUBJECT "undeliverable"',
                       'SUBJECT "delivery"', 'SUBJECT "failed"', 'SUBJECT "bounced"']:
            _, data = m.search(None, search)
            for uid in (data[0].split() or []):
                _, msg_data = m.fetch(uid, '(RFC822)')
                msg  = email.message_from_bytes(msg_data[0][1])
                subj = _dec(msg.get('Subject', '')).lower()
                body_text = _body(msg).lower()

                # Check if it's a bounce notification
                is_bounce = any(kw in subj or kw in body_text[:500] for kw in BOUNCE_KEYWORDS)
                if not is_bounce:
                    continue

                # Extract the bounced-to email from body
                combined = subj + ' ' + body_text[:2000]
                found = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', combined)
                for e in found:
                    e = e.lower()
                    # Exclude our own sending addresses and common mailer addresses
                    if not any(x in e for x in ['pressdetective', 'mailer-daemon', 'postmaster',
                                                 'protonmail', 'zeptomail', 'zoho']):
                        bounced.append(e)

        m.logout()
    except Exception as ex:
        print(f"  [inbox {account_key}] {ex}")
    return list(set(bounced))


# ── Suppression helpers ───────────────────────────────────────────────────────

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
        for email_addr, row in sorted(records.items()):
            row['email'] = email_addr
            w.writerow(row)

def bulk_suppress(emails, reason, source='verify_all'):
    records = load_suppression()
    added = 0; today = datetime.date.today().isoformat()
    for e in emails:
        e = e.strip().lower()
        if e and EMAIL_RE.match(e) and e not in records:
            records[e] = {'email': e, 'reason': reason, 'date': today, 'source': source}
            added += 1
    save_suppression(records)
    return added


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rows = list(csv.DictReader(CONTACTS_CSV.open(encoding='utf-8-sig')))
    total = len(rows)
    print(f"Loaded {total} contacts from contacts_final.csv")

    # ── Phase 1: Sweep inboxes for bounce notifications ───────────────────
    print("\nPhase 1: Sweeping all 4 inboxes for bounce notifications...")
    inbox_bounced = []
    for key in ['info', 'sujata', 'santosh', 'olympio']:
        found = sweep_inbox_for_bounces(key)
        print(f"  [{key}]  {len(found)} potential bounced addresses")
        inbox_bounced.extend(found)
    inbox_bounced = list(set(inbox_bounced))
    print(f"  Total inbox bounces: {len(inbox_bounced)}")

    n = bulk_suppress(inbox_bounced, reason='inbox_bounce_notification', source='inbox_sweep')
    print(f"  Added to blacklist: {n}")

    # ── Phase 2: Syntax check ─────────────────────────────────────────────
    print("\nPhase 2: Syntax check...")
    bad_syntax = []
    for row in rows:
        if not EMAIL_RE.match(row['email'].strip().lower()):
            bad_syntax.append(row['email'])
    print(f"  Bad syntax: {len(bad_syntax)}")
    if bad_syntax:
        n = bulk_suppress(bad_syntax, reason='invalid_syntax', source='verify_all')
        print(f"  Added to blacklist: {n}")

    # ── Phase 3: DNS / MX check (parallel) ───────────────────────────────
    print(f"\nPhase 3: DNS/MX check on {total} contacts (parallel, 20 threads)...")
    unique_domains = list({row['email'].split('@')[1].lower()
                           for row in rows if '@' in row['email']})
    print(f"  Unique domains: {len(unique_domains)}")

    dead_domains = set()
    checked = 0
    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(check_domain, d): d for d in unique_domains}
        for future in as_completed(futures):
            d = futures[future]
            is_valid, reason = future.result()
            checked += 1
            if not is_valid:
                dead_domains.add(d)
            if checked % 100 == 0:
                print(f"  Checked {checked}/{len(unique_domains)} domains, {len(dead_domains)} dead so far")

    print(f"  Dead domains: {len(dead_domains)}")
    dead_emails = [row['email'] for row in rows
                   if row['email'].split('@')[1].lower() in dead_domains]
    print(f"  Emails on dead domains: {len(dead_emails)}")
    if dead_emails:
        n = bulk_suppress(dead_emails, reason='dead_domain', source='dns_verify_all')
        print(f"  Added to blacklist: {n}")

    # ── Phase 4: Write contacts_live.csv ──────────────────────────────────
    print("\nPhase 4: Writing clean contacts_live.csv...")
    suppressed = set(load_suppression().keys())
    live, removed = [], []
    for row in rows:
        if row['email'].strip().lower() in suppressed:
            removed.append(row)
        else:
            live.append(row)

    fieldnames = list(rows[0].keys()) if rows else []
    with LIVE_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader(); w.writerows(live)

    fn_removed = fieldnames + ['reject_reason'] if 'reject_reason' not in fieldnames else fieldnames
    with REMOVED_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fn_removed, extrasaction='ignore')
        w.writeheader()
        for r in removed:
            supp = load_suppression()
            r['reject_reason'] = supp.get(r['email'].lower(), {}).get('reason', 'suppressed')
            w.writerow(r)

    # ── Summary ───────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"VERIFICATION COMPLETE")
    print(f"{'='*55}")
    print(f"Input total      : {total}")
    print(f"Inbox bounces    : {len(inbox_bounced)}")
    print(f"Bad syntax       : {len(bad_syntax)}")
    print(f"Dead domains     : {len(dead_emails)}")
    print(f"Total suppressed : {len(suppressed)}")
    print(f"Live (send-ready): {len(live)}")
    print(f"Removed          : {len(removed)}")
    print(f"\nBlacklist        : {SUPPRESS_CSV}")
    print(f"Live contacts    : {LIVE_CSV}")
    print(f"Removed log      : {REMOVED_CSV}")

    # Tag summary of live contacts
    tag_cnt = Counter()
    for r in live:
        for t in (r.get('tags') or '').split('|'):
            if t.strip(): tag_cnt[t.strip()] += 1
    print(f"\nTop tags in live list:")
    for t, c in tag_cnt.most_common(15):
        print(f"  {t:<30} {c}")


if __name__ == '__main__':
    main()
