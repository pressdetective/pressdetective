#!/usr/bin/env python3
"""_daily_report_june11.py — Full daily report 11 June 2026, to aliasgar + info@"""
import smtplib, ssl, json, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT     = Path(r'C:\dev\pressdetective')
CREDS    = json.loads((ROOT / '.creds/proton_accounts.json').read_text(encoding='utf-8'))
FROM     = CREDS['accounts']['sujata']['address']
TOKEN    = CREDS['accounts']['sujata']['token']
HOST     = CREDS['smtp_remote']['host']
PORT     = CREDS['smtp_remote']['port']
PM_HOST  = CREDS['smtp_postmark']['host']
PM_PORT  = CREDS['smtp_postmark']['port']
PM_TOKEN = CREDS['smtp_postmark']['token']

TO = ['aliasgarmerchant@gmail.com', 'info@pressdetective.com']
SUBJECT = '[FIR 0654/2022] FULL DAILY REPORT — 11 June 2026 | ACB Filed + Saraf Notice + Press Broadcast | Adv. Sujata Shirasi'

BODY = """FULL DAILY REPORT — FIR No. 0654/2022 (Tarun Thadani / Ali Asgar Merchant)
PressDetective | Adv. Sujata Shirasi
Date: 11 June 2026

======================================================================
EXECUTIVE SUMMARY
======================================================================

Today was the single most active day in this case since the FIR was
registered in August 2022. Three major actions were completed:

  1. ACB Maharashtra formal complaint filed — 9 authorities copied
  2. Final 48-hour notice sent directly to Abhishek Saraf
  3. Press release broadcast reached 426 journalists

The case is now formally before the Anti-Corruption Bureau of
Maharashtra. Saraf has until 13 June 2026 (48 hours) to withdraw
the FIR before we file the Section 528 BNSS Quashing Petition.

======================================================================
ACTION 1 — FORMAL COMPLAINT TO ACB MAHARASHTRA
======================================================================

Filed: 11 June 2026
To:   Shri Vishwas Nangre-Patil, IPS, Addl. DGP, ACB Maharashtra
      acbwebmail@mahapolice.gov.in

Copied to 8 additional authorities:
  addlcpacbmumbai@mahapolice.gov.in   Addl. CP ACB Mumbai
  acpdadar.mum@mahapolice.gov.in      ACP Dadar
  cbcidmumaecell@mahapolice.gov.in    CB-CID Anti-Extortion Cell
  adg.cidcrime.pune@mahapolice.gov.in Addl. DG CID Crime
  dgp.mah@mahapolice.gov.in           DGP Maharashtra
  sec.home@maharashtra.gov.in         Secretary (Home) Maharashtra
  hobeomum@cbi.gov.in                 CBI Mumbai
  ps.dadar.mum@mahapolice.gov.in      Dadar Police Station

THREE REQUESTS IN THE COMPLAINT:

  (A) Inquiry into how Saraf's original complaint (4 June 2022,
      ID: 23244/2022 — slap only, NO extortion, NO Thadani) was
      materially altered two months later to insert Rs. 1 crore
      extortion and Thadani's name.

  (B) Inquiry into Inspector Sanjay Taralgatti (CB-CID Anti-Extortion
      Cell) for registering FIR 0654/2022 under IPC 384/385/387 & 506
      without examining any accused, without CDR verification, without
      bank record checks, without CCTV review.

  (C) Summoning Abhishek Saraf for cross-examination on the material
      inconsistencies between his original complaint and the FIR.

======================================================================
ACTION 2 — FINAL 48-HOUR NOTICE TO ABHISHEK SARAF
======================================================================

Sent: 11 June 2026
To:   abhishek_saraf78@yahoo.com
      3rd Floor, Esplanade House, 29 Hazarimal Somani Marg, Fort, Mumbai
CC:   ACB, info@pressdetective.com, aliasgarmerchant@gmail.com

DEADLINE: 13 June 2026 (48 hours to withdraw FIR)

Failure to withdraw will result in:
  -> Section 528 BNSS Quashing Petition at Bombay High Court
  -> Criminal complaints under IPC 182, 192, 211 against Saraf
  -> Full production of all documentation to the ACB

This is the second notice (first: 9 June 2026 — no response received).

======================================================================
ACTION 3 — PRESS RELEASE BROADCAST (426 JOURNALISTS REACHED)
======================================================================

   9 June 2026 (Batch 1):  40 contacts via BCC group email
  10 June 2026 (Batches):  386 individual emails, 12s between each

Outlets reached include:
  The Hindu, Indian Express, Hindustan Times, Tribune, Quint, Scroll,
  The Caravan, The Wire, Aaj Tak, India Today, Outlook, NDTV, Times Now,
  Republic World, ABP Live, CNBC-TV18, Free Press Journal, Mid-Day,
  DNA India, Esakal, LiveLaw, Bar & Bench + 400 more journalists.

Broadcast PAUSED — new marketing strategy being developed.
Remaining: 1,285 contacts (index 427+) ready to resume.

======================================================================
ACTION 4 — CRITICAL FACTUAL CORRECTION (PERMANENT)
======================================================================

Found and permanently corrected a false claim in case documents:

  WRONG: "He attended briefly and left before any altercation."
  TRUTH: "Mr. Tarun Thadani was NOT present at the venue. His only
         connection was having sent invitations. The altercation was
         between Mr. Ali Asgar Merchant and Abhishek Badriprasad Saraf.
         Mr. Ali Asgar Merchant slapped Saraf. Thadani was not there."

This correction is permanent across all case documents.

======================================================================
VERIFIED FACTS — THE BEDROCK OF THIS CASE
======================================================================

  - Tarun Thadani was NOT at the venue. Sent invitations only.
  - Ali Asgar Merchant slapped Abhishek Badriprasad Saraf.
  - Saraf's original complaint (23244/2022, 4 June 2022):
    slap only — no extortion, no Thadani, no Rs. 1 crore.
  - Two months later: extortion added, Thadani inserted.
  - Taralgatti registered FIR without examining any accused or
    verifying any evidence — lack of due diligence on record.
  - No CDR evidence. No bank records. No extortion. No payment.

======================================================================
KEY DEADLINES
======================================================================

  13 Jun 2026 : Saraf 48-hour withdrawal deadline (HARD)
  16 Jun 2026 : Original WITHOUT PREJUDICE notice deadline

  IF NO WITHDRAWAL:
    -> Section 528 BNSS Quashing Petition, Bombay High Court
    -> IPC 182 / 192 / 211 criminal complaints against Saraf
    -> Resume press broadcast to 1,285 remaining media contacts

======================================================================
WHAT WE NEED FROM MR. ALI ASGAR MERCHANT (by 14 June 2026)
======================================================================

  [ ] Call log / CDR records for June 2022 (from mobile provider)
  [ ] Bank statements June-September 2022
  [ ] WhatsApp / SMS messages with Abhishek Saraf (screenshots)
  [ ] Written account of events on 2 June 2022
  [ ] Names of any witnesses at the restaurant
  [ ] Any information about CCTV footage from the venue
  [ ] Confirmation that Thadani had no role in any demand

Please call: +91 93216 13691

======================================================================
TODAY'S FULL EMAIL LOG — 12 AUTHORITIES + 426 PRESS
======================================================================

   1.  acbwebmail@mahapolice.gov.in         ACB formal complaint (TO)
   2.  addlcpacbmumbai@mahapolice.gov.in    ACB formal complaint (CC)
   3.  acpdadar.mum@mahapolice.gov.in       ACB formal complaint (CC)
   4.  cbcidmumaecell@mahapolice.gov.in     ACB formal complaint (CC)
   5.  adg.cidcrime.pune@mahapolice.gov.in  ACB formal complaint (CC)
   6.  dgp.mah@mahapolice.gov.in            ACB formal complaint (CC)
   7.  sec.home@maharashtra.gov.in          ACB formal complaint (CC)
   8.  hobeomum@cbi.gov.in                  ACB formal complaint (CC)
   9.  ps.dadar.mum@mahapolice.gov.in       ACB formal complaint (CC)
  10.  abhishek_saraf78@yahoo.com           Final 48-hour notice (TO)
  11.  aliasgarmerchant@gmail.com           Saraf notice CC + this report
  12.  info@pressdetective.com              CC on all above
   +   426 press/media contacts             Press broadcast (earlier)

  TOTAL UNIQUE RECIPIENTS TODAY: 438

======================================================================

Adv. Sujata Shirasi
Advocate — Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Phone : +91 93216 13691
Email : sujata.shirasi@pressdetective.com

PressDetective | info@pressdetective.com
"""


def build_msg():
    msg = MIMEMultipart('alternative')
    msg['From']    = f'Adv. Sujata Shirasi <{FROM}>'
    msg['To']      = ', '.join(TO)
    msg['Subject'] = SUBJECT
    msg['List-Unsubscribe'] = '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    msg.attach(MIMEText(BODY, 'plain', 'utf-8'))
    return msg


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

msg = build_msg()
print(f'Sending daily summary to: {", ".join(TO)}')

sent = False
print('  Trying Proton remote SMTP ...')
try:
    with smtplib.SMTP(HOST, PORT, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.ehlo()
        s.login(FROM, TOKEN)
        s.sendmail(FROM, TO, msg.as_string())
    print('  OK via Proton remote')
    sent = True
except Exception as e:
    print(f'  Proton remote failed: {str(e)[:80]}')

if not sent:
    print('  Trying Postmark ...')
    try:
        with smtplib.SMTP(PM_HOST, PM_PORT, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(PM_TOKEN, PM_TOKEN)
            s.sendmail(FROM, TO, msg.as_string())
        print('  OK via Postmark')
        sent = True
    except Exception as e:
        print(f'  Postmark failed: {str(e)[:80]}')

if not sent:
    print('ERROR: All providers failed')
    sys.exit(1)
else:
    print('Done. Report sent.')
