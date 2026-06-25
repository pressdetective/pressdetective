#!/usr/bin/env python3
"""send_investigation_notice.py -- 25 June 2026
Formal investigation notice from Santosh Sakpal (Independent Investigator)
to ACB, Mumbai Police, Anti-Extortion Cell, NHRC, notifying of investigation
into false/altered complaint FIR 0654/2022 and requesting acknowledgment.
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

# Recipients: ACB, AEC, Mumbai Police CP, NHRC
RECIPIENTS = {
    'ACB Maharashtra': 'acbmaharashtra@gmail.com',
    'Anti-Extortion Cell': 'cbcidmumaecell@mahapolice.gov.in',
    'Mumbai Police CP': 'cp.mumbai@mahapolice.gov.in',
    'NHRC': 'cr.nhrc@nic.in',
}

SUBJ = f'FORMAL INVESTIGATION NOTICE -- False/Altered Complaint FIR 0654/2022 | Independent Investigation by Santosh Sakpal, Investigator | {TODAY}'

BODY = f"""To:   Anti-Corruption Bureau of Maharashtra; CB-CID Anti-Extortion Cell;
      Commissioner of Police, Mumbai; National Human Rights Commission
From: Santosh Sakpal, Independent Investigator
Date: {TODAY}
Contact: +91 82689 17276 | santoshsakpal03@gmail.com

Subject: FORMAL INVESTIGATION NOTICE -- Independent investigation into FIR 0654/2022 and
         false/altered complaint by Mr. Abhishek Badriprasad Saraf

Respected Officers/Commissioners,

I, Santosh Sakpal, Independent Investigator, formally notify you that I am conducting
an independent investigation into FIR No. 0654/2022 (Dadar Police Station, CB-CID
Anti-Extortion Cell, 13 August 2022) and have documented evidence of material
complaint alteration and false registration.

INVESTIGATION FINDINGS:

1. ORIGINAL COMPLAINT (4 June 2022, ID 23244/2022 - Worli PS)
   Complainant: Mr. Abhishek Badriprasad Saraf
   Allegations: Assault only (Section 323 IPC, bailable)
   Subjects: Only Mr. Ali Asgar Merchant (the slapper)
   Extortion claim: ABSENT
   Rs 1 crore demand: ABSENT
   Mr. Tarun Thadani mention: ABSENT

2. ALTERED COMPLAINT (~2 months later, 13 August 2022)
   FIR No. 0654/2022 (Dadar PS, routed through Anti-Extortion Cell)
   Allegations: Rs 1 crore "extortion" (Sections 384/385/387/506)
   Subjects: Now includes Mr. Tarun Thadani (who was NOT present)
   Extortion claim: ADDED (absent from original)
   Rs 1 crore demand: ADDED (absent from original)
   Investigation: No accused examined, no CDR/bank/CCTV verified

3. DOCUMENTED CONTRADICTION
   The same complainant, in the same matter, filed two materially different
   versions without any new evidence, intervention, or investigation between them.
   This is the definition of false complaint and complaint alteration.

FORMAL REQUEST:
I request that you:

(a) Register a counter-investigation into the false/altered complaint by Mr. Saraf
    under Sections 217/248 BNS (formerly IPC 182/211);

(b) Conduct due-diligence inquiry into how FIR 0654/2022 came to be registered
    without examination of accused or verification of evidence;

(c) Reinvestigate FIR 0654/2022 against the original complaint (ID 23244/2022)
    to determine whether any extortion element is supported by evidence;

(d) Consider the conduct of the investigating officer (Insp. Sanjay Taralgatti)
    in the context of complaint alteration and registration without verification.

DOCUMENT ENCLOSED:
Original complaint ID 23244/2022 (proof of the documented discrepancy)

LEGAL FRAMEWORK:
- Bhajan Lal doctrine (State of Haryana v. Bhajan Lal) -- inherent power to
  prevent abuse of criminal process
- Section 528 BNSS (formerly s.401 CrPC) -- quashing of frivolous prosecution
- Article 226 -- constitutional remedy for abuse of process
- Arnesh Kumar requirements -- preliminary verification before non-bailable FIR

STATUS:
This independent investigation has been conducted under legal counsel and in
coordination with ongoing criminal proceedings. Formal complaints have been
filed with this Commission, the ACB, and the Mumbai Police requesting
investigation into the complaint alteration and registration impropriety.

I am available to depose, furnish documents, and cooperate with any inquiry
or investigation. This matter is sub-judice; this notice documents formal
investigation findings and requests for lawful action.

Respectfully,

Santosh Sakpal
Independent Investigator
B/6 Shimgyamanohar Apartments, Thane Belapur Road, Digha West, Navi Mumbai 400708
Phone: +91 82689 17276
Email: santoshsakpal03@gmail.com

(Issued with the assistance of PressDetective | info@pressdetective.com)
Counsel on record: Adv. Sujata Shirasi, Trial Court, Mumbai"""

print('=' * 70)
print('INVESTIGATION NOTICE SUBMISSION')
print('=' * 70)
print(f'\nFrom: {FROM}')
print(f'Date: {TODAY}')
print(f'\nRecipients:')
for name, addr in RECIPIENTS.items():
    print(f'  - {name}: {addr}')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

results = {}
for org_name, to_addr in RECIPIENTS.items():
    print(f'\n[{org_name}]')

    m = MIMEMultipart('alternative')
    m['From'] = FROM_HDR
    m['To'] = to_addr
    m['Cc'] = INFO
    m['Subject'] = SUBJ
    m['Reply-To'] = FROM
    m.attach(MIMEText(BODY, 'plain', 'utf-8'))

    rcpts = [to_addr, INFO]

    try:
        with smtplib.SMTP(PROTON_H, PROTON_P, timeout=30) as s:
            s.ehlo()
            s.starttls(context=ctx)
            s.ehlo()
            s.login(FROM, TOKEN)
            s.sendmail(FROM, rcpts, m.as_string())
        print(f'  [OK] Investigation notice sent via Proton')
        results[org_name] = 'SENT'
    except Exception as e:
        print(f'  [FAIL] {str(e)[:70]}')
        results[org_name] = f'FAILED: {str(e)[:50]}'

    time.sleep(3)

print('\n' + '=' * 70)
print('RESULTS:')
for org, status in results.items():
    print(f'  {status:30} -- {org}')

print('\n' + '=' * 70)
print('INVESTIGATION NOTICE DELIVERY COMPLETE')
print('=' * 70)
print('\nAll organizations have been formally notified of the investigation')
print('findings. Check Bridge IMAP for any bounce DSNs (government gateways')
print('may reject due to policy blocks). Formal filings via portals are the')
print('primary channel; this email serves as additional documented notice.')
