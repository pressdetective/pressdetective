#!/usr/bin/env python3
"""resend_all_with_fixed_dns.py -- 25 June 2026
Resend all pending investigation/campaign emails now that SPF is fixed.
Includes: investigation notice, legal allies, press, government bodies.
"""
import smtplib, ssl, json, sys, time
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import lib.presend_guard  # noqa: F401
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CREDS = json.loads(Path(r'C:\dev\pressdetective\.creds\proton_accounts.json').read_text(encoding='utf-8-sig'))
FROM = CREDS['accounts']['santosh']['address']
TOKEN = CREDS['accounts']['santosh']['token']
PROTON_H = CREDS['smtp_remote']['host']
PROTON_P = CREDS['smtp_remote']['port']
FROM_HDR = formataddr(('Santosh Sakpal, Independent Investigator', FROM))

TODAY = '25 June 2026'
INFO = 'info@pressdetective.com'
ROOT = Path(r'C:\dev\pressdetective')

# INVESTIGATION NOTICE BODY (same as investigation_notice.py)
INVESTIGATION_SUBJ = f'FORMAL INVESTIGATION NOTICE -- False/Altered Complaint FIR 0654/2022 | {TODAY}'
INVESTIGATION_BODY = f"""To:   Anti-Corruption Bureau of Maharashtra; CB-CID Anti-Extortion Cell;
      Commissioner of Police, Mumbai; National Human Rights Commission

From: Santosh Sakpal, Independent Investigator
Date: {TODAY}

Subject: FORMAL INVESTIGATION NOTICE -- Independent investigation into FIR 0654/2022

Respected Officers/Commissioners,

I, Santosh Sakpal, Independent Investigator, formally notify you of an independent
investigation into FIR No. 0654/2022 documenting material complaint alteration.

FINDINGS:
- Original complaint (4 June 2022, ID 23244/2022): Assault only, IPC 323, bailable
- Altered FIR (13 Aug 2022, 0654/2022): Rs 1 crore extortion, non-bailable
- Gap: 2 months, no new evidence, no accused examined
- Proof: Same subject, materially different allegations = false complaint

REQUEST:
(a) Register counter-investigation (BNS 217/248 - false complaint)
(b) Reinvestigate FIR 0654/2022 against original complaint
(c) Take lawful action after investigation

Formal complaints filed via portals and registered post. This email provides
additional notice and documents investigation status.

Yours faithfully,
Santosh Sakpal
Independent Investigator
+91 82689 17276
santoshsakpal03@gmail.com"""

# RECIPIENTS: Broader distribution including alternative addresses
RECIPIENTS = {
    'Government & Authorities': [
        ('ACB Maharashtra', 'acbmaharashtra@gmail.com'),
        ('ACB Webmail', 'acbwebmail@mahapolice.gov.in'),
        ('Anti-Extortion Cell', 'aec@cbcidmumbai.in'),
        ('Mumbai Police CP', 'cp.mumbai@mahapolice.gov.in'),
        ('NHRC', 'cr.nhrc@nic.in'),
    ],
    'Press Contacts': [
        ('TOI Crime Desk', 'mumbai.crime@timesgroup.com'),
        ('TOI Mumbai Desk', 'mumbai.letters@timesgroup.com'),
        ('TOI Editor', 'editor@timesgroup.com'),
    ],
    'Legal Allies (Sample)': [
        ('IAMAI', 'legal@iamai.in'),
        ('CCPI', 'info@ccpindia.org'),
        ('IPLEADERS', 'contact@ipleaders.in'),
    ]
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('=' * 70)
print('RESEND ALL EMAILS -- DNS FIXED')
print('=' * 70)
print(f'From: {FROM}')
print(f'Date: {TODAY}')
print(f'SPF: v=spf1 include:_spf.protonmail.ch -all (OPTIMIZED)')
print()

overall_results = {}
total_sent = 0
total_failed = 0

for category, recipients_list in RECIPIENTS.items():
    print(f'\n[{category}]')
    category_sent = 0
    category_failed = 0

    for name, addr in recipients_list:
        m = MIMEMultipart('alternative')
        m['From'] = FROM_HDR
        m['To'] = addr
        m['Cc'] = INFO
        m['Subject'] = INVESTIGATION_SUBJ
        m['Reply-To'] = FROM
        m.attach(MIMEText(INVESTIGATION_BODY, 'plain', 'utf-8'))

        rcpts = [addr, INFO]

        try:
            with smtplib.SMTP(PROTON_H, PROTON_P, timeout=30) as s:
                s.ehlo()
                s.starttls(context=ctx)
                s.ehlo()
                s.login(FROM, TOKEN)
                s.sendmail(FROM, rcpts, m.as_string())
            print(f'  [OK] {name:<40} {addr}')
            category_sent += 1
            total_sent += 1
        except Exception as e:
            err = str(e)[:50]
            print(f'  [FAIL] {name:<40} {err}')
            category_failed += 1
            total_failed += 1

        time.sleep(2)

    overall_results[category] = f'{category_sent} sent, {category_failed} failed'

print('\n' + '=' * 70)
print('SUMMARY:')
for cat, result in overall_results.items():
    print(f'  {cat:<30} {result}')

print(f'\nTOTAL: {total_sent} sent, {total_failed} failed')
print('=' * 70)
print('\nNow check Bridge IMAP in 30-60 seconds for bounce DSNs.')
print('With fixed SPF (strict -all), deliverability should improve.')
print('Monitor info@pressdetective.com for delivery confirmations.')
