#!/usr/bin/env python3
"""
Two-phase bounce cleanup:
Phase 1: Try ZeptoMail API for suppression/bounce list
Phase 2: SMTP RCPT TO verification on non-gov press contacts
         (silent probe — no email sent)
Removes confirmed dead mailboxes from contacts_clean.csv → contacts_final.csv
"""

import csv, json, sys, time, socket, smtplib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter
import urllib.request, urllib.error

try:
    import dns.resolver, dns.exception
except ImportError:
    print("ERROR: pip install dnspython"); sys.exit(1)

BASE  = Path(__file__).parent
CREDS = BASE.parent / 'clients' / 'tarun-thadani' / '.creds'

# ── Load ZeptoMail token ───────────────────────────────────────────────────────
token_raw = CREDS.read_text(encoding='utf-8').strip()
ZEPTO_TOKEN = ''
for line in token_raw.splitlines():
    if 'ZEPTO_TOKEN' in line:
        ZEPTO_TOKEN = line.split('=', 1)[1].strip()
        break

API_BASE = 'https://api.zeptomail.in'
HEADERS  = {
    'Authorization': f'Zoho-enczapikey {ZEPTO_TOKEN}',
    'Accept': 'application/json',
}

# Government / institutional domains — skip SMTP probe (won't respond + valid)
SKIP_SMTP_DOMAINS = {
    'mahapolice.gov.in', 'maharashtra.gov.in', 'nic.in', 'gov.in',
    'bhc.gov.in', 'aij.gov.in', 'goapolice.gov.in', 'gspcb.in',
    'mhcyber.gov.in', 'dcourts.gov.in', 'acbmaharashtra.gov.in',
    'cbi.gov.in',
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 1: ZeptoMail API — try all known suppression/bounce endpoints
# ─────────────────────────────────────────────────────────────────────────────
def try_zepto_api():
    """Returns set of bounced email addresses if API accessible, else empty set."""
    bounced = set()
    endpoints = [
        '/v1.1/email/suppression-list',
        '/v1.1/suppression-list',
        '/v1.1/email/bounce-list',
        '/v1.1/bounce-list',
        '/v1.1/email/invalid',
        '/v1.1/email/hard-bounce',
        '/v1.1/mail-activity',
    ]
    for ep in endpoints:
        url = API_BASE + ep
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                print(f"  [200] {ep} → {str(data)[:200]}")
                # Parse emails from response
                if isinstance(data, list):
                    for item in data:
                        email = item.get('email') or item.get('address') or item.get('recipient')
                        if email:
                            bounced.add(email.lower())
                elif isinstance(data, dict):
                    items = data.get('data') or data.get('emails') or data.get('list') or []
                    if isinstance(items, list):
                        for item in items:
                            if isinstance(item, dict):
                                email = item.get('email') or item.get('address') or item.get('recipient')
                            else:
                                email = str(item)
                            if email and '@' in str(email):
                                bounced.add(str(email).lower())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:100]
            err_code = ''
            try:
                err_code = json.loads(body).get('error',{}).get('details',[{}])[0].get('code','')
            except Exception:
                pass
            print(f"  [{e.code}] {ep} -> {err_code}")
        except Exception as ex:
            print(f"  [ERR] {ep} → {ex}")
    return bounced


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: SMTP RCPT TO probe per email address
# ─────────────────────────────────────────────────────────────────────────────
mx_cache = {}

def get_mx(domain: str) -> str | None:
    if domain in mx_cache:
        return mx_cache[domain]
    try:
        answers = sorted(
            dns.resolver.resolve(domain, 'MX', lifetime=5),
            key=lambda r: r.preference
        )
        host = str(answers[0].exchange).rstrip('.')
        mx_cache[domain] = host
        return host
    except Exception:
        mx_cache[domain] = None
        return None


def smtp_check(email: str) -> str:
    """
    Returns: 'valid' | 'invalid' | 'unknown'
    'invalid' = server explicitly said user doesn't exist (5xx RCPT TO)
    'unknown' = server graylisted / blocked probe / timeout
    """
    domain = email.split('@')[1].lower()
    # Skip government domains
    for skip in SKIP_SMTP_DOMAINS:
        if domain == skip or domain.endswith('.' + skip):
            return 'skip'

    mx = get_mx(domain)
    if not mx:
        return 'unknown'

    try:
        with smtplib.SMTP(timeout=8) as s:
            s.connect(mx, 25)
            s.ehlo('pressdetective.com')
            code, _ = s.mail('')
            if code not in (250, 251):
                return 'unknown'
            code, msg = s.rcpt(email)
            if code in (250, 251):
                return 'valid'
            elif code >= 500:   # 550, 551, 553 = user not found
                return 'invalid'
            else:               # 4xx = temporary / greylisted
                return 'unknown'
    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected,
            socket.timeout, ConnectionRefusedError, OSError):
        return 'unknown'
    except Exception:
        return 'unknown'


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    src = BASE / 'contacts_clean.csv'
    rows = list(csv.DictReader(src.open(encoding='utf-8-sig')))
    total = len(rows)
    print(f"Loaded {total} contacts from contacts_clean.csv\n")

    # ── Phase 1: ZeptoMail API ────────────────────────────────────────────
    print("Phase 1: ZeptoMail API bounce list...")
    api_bounced = try_zepto_api()
    print(f"  API returned {len(api_bounced)} bounced addresses\n")

    # ── Phase 2: SMTP probe — press + non-gov non-gmail contacts only ─────
    smtp_targets = [
        r for r in rows
        if 'press' in r.get('tags','')
        or 'govt-state' in r.get('tags','')
        or 'ngo-civic' in r.get('tags','')
        or 'individual' in r.get('tags','')
        or 'general' in r.get('tags','')
    ]
    # Exclude already-known-valid-domain addresses and large providers
    BIG_PROVIDERS = {'gmail.com','yahoo.com','yahoo.co.in','yahoo.in','rediffmail.com',
                     'hotmail.com','outlook.com','live.com','icloud.com'}
    smtp_targets = [
        r for r in smtp_targets
        if r['email'].split('@')[1].lower() not in BIG_PROVIDERS
    ]

    print(f"Phase 2: SMTP probe on {len(smtp_targets)} press/civic contacts (non-gmail/gov)...")
    print("  (probing MX servers — no emails sent)\n")

    smtp_invalid = set()
    smtp_valid   = set()
    smtp_unknown = set()
    done = 0

    with ThreadPoolExecutor(max_workers=15) as pool:
        futures = {pool.submit(smtp_check, r['email']): r['email'] for r in smtp_targets}
        for future in as_completed(futures):
            email = futures[future]
            result = future.result()
            done += 1
            if result == 'invalid':
                smtp_invalid.add(email)
            elif result == 'valid':
                smtp_valid.add(email)
            else:
                smtp_unknown.add(email)
            if done % 100 == 0:
                print(f"  SMTP: {done}/{len(smtp_targets)} checked | "
                      f"invalid={len(smtp_invalid)} valid={len(smtp_valid)} unknown={len(smtp_unknown)}")

    print(f"\nSMTP results:")
    print(f"  Confirmed invalid (user not found): {len(smtp_invalid)}")
    print(f"  Confirmed valid:                    {len(smtp_valid)}")
    print(f"  Unknown (greylisted/blocked):       {len(smtp_unknown)}")

    # ── Combine all known-bad addresses ───────────────────────────────────
    all_bad = api_bounced | smtp_invalid
    print(f"\nTotal addresses to remove: {len(all_bad)}")

    # ── Write contacts_final.csv ──────────────────────────────────────────
    final, removed = [], []
    for row in rows:
        if row['email'] in all_bad:
            row['reject_reason'] = 'smtp_user_not_found' if row['email'] in smtp_invalid else 'api_bounce'
            removed.append(row)
        else:
            final.append(row)

    fieldnames = list(rows[0].keys())
    fn_with_reason = fieldnames + (['reject_reason'] if 'reject_reason' not in fieldnames else [])

    out_final   = BASE / 'contacts_final.csv'
    out_removed = BASE / 'contacts_smtp_removed.csv'

    with out_final.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader()
        w.writerows(final)

    with out_removed.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fn_with_reason, extrasaction='ignore')
        w.writeheader()
        for r in removed:
            r.setdefault('reject_reason', 'removed')
        w.writerows(removed)

    # ── Report ────────────────────────────────────────────────────────────
    domain_removals = Counter(r['email'].split('@')[1] for r in removed)
    tag_counts = Counter()
    for r in final:
        for t in r.get('tags','').split('|'):
            if t: tag_counts[t] += 1

    report = f"""SMTP Bounce Cleanup Report
Generated: 2026-06-09
==========================
Input (contacts_clean.csv):  {total}
Final (contacts_final.csv):  {len(final)}
Removed:                      {len(removed)}

  From ZeptoMail API:         {len(api_bounced)}
  From SMTP probe (invalid):  {len(smtp_invalid)}

Top removed domains:
"""
    for dom, cnt in domain_removals.most_common(20):
        report += f"  {dom}: {cnt}\n"

    report += f"\nTag counts after cleanup:\n"
    priority = ['top-priority','police-hq','court-high','anti-corruption','police-special',
                'economic-fraud','police-zone','anti-extortion','crime-branch','cyber-crime',
                'court-lower','court-sessions','court-family','govt-admin','land-records',
                'police-station','press','govt-state','ngo-civic','goa','individual',
                'dgp-desk','general']
    for t in priority:
        if t in tag_counts:
            report += f"  {t:<25} {tag_counts[t]}\n"

    rpt_path = BASE / 'smtp_clean_report.txt'
    rpt_path.write_text(report, encoding='utf-8')
    print('\n' + report)

if __name__ == '__main__':
    t0 = time.time()
    main()
    print(f"Done in {time.time()-t0:.1f}s")
