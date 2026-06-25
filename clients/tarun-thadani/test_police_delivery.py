#!/usr/bin/env python3
"""test_police_delivery.py -- Test single email to police department (Dadar PS)
Verify that optimized SPF + Proton-only works with government gateway.
"""
import smtplib, ssl, json, sys
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

# Test recipient: Dadar Police Station (FIR station)
TEST_ADDR = 'ps.dadar.mum@mahapolice.gov.in'
INFO = 'info@pressdetective.com'

SUBJ = 'TEST DELIVERY -- FIR 0654/2022 follow-up | Dadar PS | Proton via optimized SPF'
BODY = f"""To: Dadar Police Station
From: Santosh Sakpal, Independent Investigator
Date: 25 June 2026

Respected Sir/Madam,

This is a test email to verify delivery to your mailbox following SPF/DKIM optimization.

FIR 0654/2022 (Dadar PS) - False extortion complaint by Abhishek Saraf.

The complainant's own original complaint (4 June 2022, ID 23244/2022) alleged only
a slap (Section 323 IPC, bailable) -- NO extortion, NO Rs 1 crore, NO mention of
Mr. Tarun Thadani. Yet FIR 0654/2022 (13 Aug 2022) was registered alleging a Rs 1
crore extortion with no accused examined and no evidence verified.

We request:
(a) register and investigate the false/altered complaint by Mr. Saraf (BNS 217/248)
(b) reinvestigate FIR 0654/2022 against the original complaint
(c) take lawful action after investigation

This matter is sub-judice. All documentation available on request.

Yours faithfully,
Santosh Sakpal
+91 82689 17276
santoshsakpal03@gmail.com"""

print('=' * 70)
print('TEST EMAIL TO POLICE DEPARTMENT')
print('=' * 70)
print(f'\nSender: {FROM}')
print(f'To: {TEST_ADDR}')
print(f'CC: {INFO}')
print(f'Subject: {SUBJ[:60]}...')

m = MIMEMultipart('alternative')
m['From'] = FROM_HDR
m['To'] = TEST_ADDR
m['Cc'] = INFO
m['Subject'] = SUBJ
m['Reply-To'] = FROM
m.attach(MIMEText(BODY, 'plain', 'utf-8'))

rcpts = [TEST_ADDR, INFO]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print(f'\nConnecting to {PROTON_H}:{PROTON_P}...')
try:
    with smtplib.SMTP(PROTON_H, PROTON_P, timeout=30) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.ehlo()
        s.login(FROM, TOKEN)
        s.sendmail(FROM, rcpts, m.as_string())
    print('[OK] Email sent via Proton')
except Exception as e:
    print(f'[FAIL] {e}')
    sys.exit(1)

print('\n' + '=' * 70)
print('TEST COMPLETE')
print('=' * 70)
print('\nNow check Bridge IMAP (Inbox > look for DSN) in 30-60 seconds.')
print('Expected outcomes:')
print('  SUCCESS: No bounce = SPF/policy block fixed, mail reached police')
print('  BOUNCE 5.7.7: Policy still blocks (need auth fix or different approach)')
print('  BOUNCE 5.1.1: Dead mailbox (address not found)')
print('  Other bounce: New error, investigate')
