#!/usr/bin/env python3
"""
send_balance_emails.py -- 12 June 2026
Sends all balance/followup emails via Mailtrap (fallback: Postmark -> Proton remote).

EMAIL 1: Police departments followup (ACB TO + 8 CC)
EMAIL 2: Saraf final deadline warning (deadline TOMORROW 13 June)
EMAIL 3: Full case report to Ali Asgar Merchant
"""
import smtplib, ssl, json, sys, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT  = Path(r'C:\dev\pressdetective')
CREDS = json.loads((ROOT / '.creds/proton_accounts.json').read_text(encoding='utf-8-sig'))

FROM      = CREDS['accounts']['sujata']['address']
TOKEN     = CREDS['accounts']['sujata']['token']
PROTON_H  = CREDS['smtp_remote']['host']
PROTON_P  = CREDS['smtp_remote']['port']
PM_H      = CREDS['smtp_postmark']['host']
PM_P      = CREDS['smtp_postmark']['port']
PM_TOKEN  = CREDS['smtp_postmark']['token']
MT_H      = CREDS['smtp_mailtrap']['host']
MT_P      = CREDS['smtp_mailtrap']['port']
MT_TOKEN  = CREDS['smtp_mailtrap']['token']
MT_USER   = CREDS['smtp_mailtrap']['user']

TODAY = '12 June 2026'

# ── provider chain: Mailtrap first, then Postmark, then Proton ──────────────
def send(recipients, msg_obj, label):
    ctx_strict = ssl.create_default_context()
    ctx_loose  = ssl.create_default_context()
    ctx_loose.check_hostname = False
    ctx_loose.verify_mode    = ssl.CERT_NONE

    # 1. Mailtrap (live sending)
    try:
        with smtplib.SMTP(MT_H, MT_P, timeout=20) as s:
            s.ehlo(); s.starttls(context=ctx_strict); s.ehlo()
            s.login(MT_USER, MT_TOKEN)
            s.sendmail(FROM, recipients, msg_obj.as_string())
        print(f'  [{label}] OK via Mailtrap')
        return True
    except Exception as e:
        print(f'  [{label}] Mailtrap failed: {str(e)[:80]}')

    # 2. Postmark
    try:
        with smtplib.SMTP(PM_H, PM_P, timeout=20) as s:
            s.ehlo(); s.starttls(context=ctx_strict); s.ehlo()
            s.login(PM_TOKEN, PM_TOKEN)
            s.sendmail(FROM, recipients, msg_obj.as_string())
        print(f'  [{label}] OK via Postmark')
        return True
    except Exception as e:
        print(f'  [{label}] Postmark failed: {str(e)[:80]}')

    # 3. Proton remote
    try:
        with smtplib.SMTP(PROTON_H, PROTON_P, timeout=20) as s:
            s.ehlo(); s.starttls(context=ctx_loose); s.ehlo()
            s.login(FROM, TOKEN)
            s.sendmail(FROM, recipients, msg_obj.as_string())
        print(f'  [{label}] OK via Proton remote')
        return True
    except Exception as e:
        print(f'  [{label}] Proton remote failed: {str(e)[:80]}')

    print(f'  [{label}] ERROR: all providers failed')
    return False


def build(to_list, cc_list, subject, body):
    msg = MIMEMultipart('alternative')
    msg['From']             = f'Adv. Sujata Shirasi <{FROM}>'
    msg['To']               = ', '.join(to_list)
    if cc_list:
        msg['Cc']           = ', '.join(cc_list)
    msg['Subject']          = subject
    msg['List-Unsubscribe'] = '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    msg['X-PM-Message-Stream'] = 'outbound'
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    return msg


# ============================================================
# EMAIL 1 -- POLICE DEPARTMENTS FOLLOWUP
# ============================================================
POLICE_TO  = ['acbwebmail@mahapolice.gov.in']
POLICE_CC  = [
    'addlcpacbmumbai@mahapolice.gov.in',
    'acpdadar.mum@mahapolice.gov.in',
    'cbcidmumaecell@mahapolice.gov.in',
    'adg.cidcrime.pune@mahapolice.gov.in',
    'dgp.mah@mahapolice.gov.in',
    'sec.home@maharashtra.gov.in',
    'hobeomum@cbi.gov.in',
    'ps.dadar.mum@mahapolice.gov.in',
    'info@pressdetective.com',
]

POLICE_SUBJ = (
    'FOLLOW-UP: FIR No. 0654/2022 Dadar PS | Saraf 48-Hour Deadline Expires TOMORROW '
    '13 June 2026 | Quashing Petition Being Filed | Adv. Sujata Shirasi | ' + TODAY
)

POLICE_BODY = """\
To,
The Addl. Director General of Police
Anti-Corruption Bureau, Maharashtra
Email: acbwebmail@mahapolice.gov.in

CC: All authorities as listed below (9 offices total)

Date: 12 June 2026

Subject: Follow-Up to Formal Complaint dated 11 June 2026 |
         FIR No. 0654/2022, Dadar Police Station |
         48-Hour Notice to Complainant Expires Tomorrow |
         Section 528 BNSS Quashing Petition Being Prepared

Ref: Formal complaint filed by Adv. Sujata Shirasi, 11 June 2026,
     on behalf of Accused No. 1 Mr. Ali Asgar Merchant and
     Accused No. 2 Mr. Tarun Thadani in FIR No. 0654/2022.

======================================================================
RESPECTFUL FOLLOW-UP
======================================================================

I write to follow up on the formal complaint submitted to this office
on 11 June 2026 regarding FIR No. 0654/2022 registered at Dadar
Police Station, Mumbai, by Inspector Sanjay Taralgatti of the
CB-CID Anti-Extortion Cell.

I wish to update this office on the current status and anticipated
next steps.

======================================================================
STATUS UPDATE
======================================================================

1. 48-HOUR NOTICE TO MR. ABHISHEK BADRIPRASAD SARAF -- EXPIRES TOMORROW

   A formal 48-hour notice was served on the complainant,
   Mr. Abhishek Badriprasad Saraf, on 11 June 2026, demanding
   withdrawal of FIR No. 0654/2022 before 13 June 2026.

   That notice expires TOMORROW -- 13 June 2026.

   As of today (12 June 2026), no withdrawal has been received
   and no response has been forthcoming from Mr. Saraf.

2. QUASHING PETITION -- BOMBAY HIGH COURT

   A petition under Section 528 BNSS (equivalent of Section 482
   CrPC) for quashing of FIR No. 0654/2022 and the charge-sheet
   thereunder is being prepared for filing at the Bombay High Court.

   The petition will be filed immediately upon expiry of the
   notice tomorrow if Mr. Saraf does not withdraw.

   Grounds for quashing:
     (a) Material inconsistency between original complaint
         ID: 23244/2022 (filed 4 June 2022 -- no extortion,
         no Thadani, slap only) and the version that preceded
         FIR registration two months later
     (b) Absence of any evidence of extortion (no CDR, no bank
         records, no CCTV review, no witness statements)
     (c) Lack of pre-registration examination of any accused
     (d) Mr. Tarun Thadani was not present at the venue on
         2 June 2022 -- his name was absent from the original
         complaint

3. CRIMINAL COMPLAINTS AGAINST SARAF

   Upon expiry of the notice, criminal complaints will also be
   filed against Mr. Abhishek Badriprasad Saraf under:
     -- IPC Section 182 (false information to public servant)
     -- IPC Section 192 (fabricating evidence)
     -- IPC Section 211 (false charge with intent to injure)

======================================================================
REQUEST TO THIS OFFICE
======================================================================

I most respectfully request this office to:

  (a) Acknowledge receipt of the formal complaint of 11 June 2026
      (if not already done) and confirm that the matter is under
      review

  (b) Note that the quashing petition will be filed tomorrow
      and the complaint file before this office will form part
      of the supporting record placed before the Bombay High Court

  (c) If any preliminary inquiry into Inspector Sanjay Taralgatti's
      investigation has been initiated, kindly inform this office
      so that the same may be brought to the attention of the court

I remain at the complete disposal of this office and will provide
any further documentation or affidavit as required.

Yours faithfully,

Adv. Sujata Shirasi
Advocate -- FIR No. 0654/2022 Defence
Acting for Accused No. 1 Mr. Ali Asgar Merchant
         and Accused No. 2 Mr. Tarun Thadani
Phone    : +91 93216 13691
Email    : sujata.shirasi@pressdetective.com
Date     : 12 June 2026

CC:
  Addl. Commissioner of Police, ACB Mumbai
  ACP Dadar (Dadar Police Station)
  CB-CID Anti-Extortion Cell, Mumbai
  Addl. Director General CID Crime, Pune
  Director General of Police, Maharashtra
  Secretary (Home), Government of Maharashtra
  Central Bureau of Investigation, Mumbai
  Dadar Police Station (OC)
  PressDetective (info@pressdetective.com) -- for record

PressDetective | info@pressdetective.com
"""


# ============================================================
# EMAIL 2 -- SARAF FINAL DEADLINE WARNING
# ============================================================
SARAF_TO = ['abhishek_saraf78@yahoo.com']
SARAF_CC = [
    'acbwebmail@mahapolice.gov.in',
    'cbcidmumaecell@mahapolice.gov.in',
    'aliasgarmerchant@gmail.com',
    'info@pressdetective.com',
]

SARAF_SUBJ = (
    'FINAL WARNING -- FIR No. 0654/2022 | Withdrawal Deadline TOMORROW '
    '13 June 2026 | Petition Filed on Non-Compliance | Adv. Sujata Shirasi | ' + TODAY
)

SARAF_BODY = """\
To,
Mr. Abhishek Badriprasad Saraf
3rd Floor, Esplanade House, 29 Hazarimal Somani Marg,
Fort, Mumbai 400001
Email: abhishek_saraf78@yahoo.com

CC:
  Anti-Corruption Bureau Maharashtra (acbwebmail@mahapolice.gov.in)
  CB-CID Anti-Extortion Cell (cbcidmumaecell@mahapolice.gov.in)
  Mr. Ali Asgar Merchant -- Accused No. 1 (aliasgarmerchant@gmail.com)
  PressDetective (info@pressdetective.com)

Date: 12 June 2026

Subject: FINAL NOTICE -- Withdrawal of FIR No. 0654/2022 |
         Deadline: 13 June 2026 (TOMORROW) |
         Non-Compliance Will Result in Immediate Court Filing

======================================================================
FINAL NOTICE BEFORE LEGAL ACTION
======================================================================

Dear Mr. Saraf,

I refer to the 48-hour notice served on you on 11 June 2026 requiring
the withdrawal of FIR No. 0654/2022 registered at Dadar Police
Station, Mumbai.

YOUR DEADLINE IS TOMORROW -- 13 JUNE 2026.

As of today, no response and no withdrawal have been received.

This is my FINAL NOTICE to you.

======================================================================
IF YOU DO NOT WITHDRAW BY TOMORROW -- WHAT WILL HAPPEN
======================================================================

Upon expiry of the notice on 13 June 2026, the following will be
initiated without further warning:

  1. SECTION 528 BNSS QUASHING PETITION -- BOMBAY HIGH COURT
     We will file a petition before the Bombay High Court seeking
     quashing of FIR No. 0654/2022 and the charge-sheet in its
     entirety. The petition will place on record:
       -- Your original complaint of 4 June 2022 (ID: 23244/2022)
          which alleged a slap only -- no extortion, no Thadani
       -- The materially altered version that preceded the FIR
       -- The complete absence of evidence for extortion
       -- Inspector Taralgatti's failure to examine any accused
          or verify any evidence before registration

  2. CRIMINAL COMPLAINTS AGAINST YOU
     Criminal complaints will be filed against you personally under:
       -- IPC Section 182 (false information to public servant)
       -- IPC Section 192 (fabricating evidence)
       -- IPC Section 211 (false charge with intent to injure)
     These are cognisable offences. You will be the accused.

  3. ACB FORMAL INQUIRY INTO YOUR CONDUCT
     The Anti-Corruption Bureau of Maharashtra has our full complaint
     on record (filed 11 June 2026). We will formally request an
     inquiry into the alteration of your original complaint.

  4. NATIONAL PRESS BROADCAST
     1,285 national media contacts (The Hindu, Indian Express,
     NDTV, India Today, The Wire, Scroll, The Caravan and more)
     will receive the full documented case including your original
     complaint, the altered version, and all filed proceedings.
     359 Mumbai journalists have already received this material.

======================================================================
THE FACTS DO NOT FAVOUR YOU, MR. SARAF
======================================================================

Your own complaint of 4 June 2022 -- filed two days after the
incident when your memory was freshest -- contained:
  (a) NO allegation of extortion
  (b) NO mention of Rs. 1 crore or any sum of money
  (c) NO mention of Mr. Tarun Thadani in any capacity

That complaint is on documented record. It cannot be explained away.
Every law enforcement authority we have written to has been provided
a copy of both versions of your complaint.

Mr. Thadani was NOT at the venue on 2 June 2022. He is in this FIR
entirely because his name was added to your complaint two months
after you first filed it.

Nine law enforcement authorities, three legal proceedings, 359
journalists, and a petition at the Bombay High Court. This is where
we are -- one day before your deadline.

======================================================================
WHAT YOU CAN STILL DO
======================================================================

Withdraw FIR No. 0654/2022 before the end of 13 June 2026.

A withdrawal at this stage, before court proceedings formally begin,
is still a path to resolution. Once the quashing petition is filed
and criminal complaints are registered against you, that path closes.

I write to you not with hostility but because the truth is on record
and every day you delay makes your own position more difficult.

This is your final opportunity.

Yours faithfully,

Adv. Sujata Shirasi
Advocate -- FIR No. 0654/2022 Defence
Acting for Accused No. 1 Mr. Ali Asgar Merchant
         and Accused No. 2 Mr. Tarun Thadani
Phone    : +91 93216 13691
Email    : sujata.shirasi@pressdetective.com
Date     : 12 June 2026

Note: This correspondence has been copied to the Anti-Corruption
Bureau of Maharashtra, CB-CID Anti-Extortion Cell, Mr. Ali Asgar
Merchant and PressDetective for record. All responses must be
addressed to this office in writing.
"""


# ============================================================
# EMAIL 3 -- FULL REPORT TO ALI (via Mailtrap this round)
# ============================================================
ALI_TO = ['aliasgarmerchant@gmail.com']
ALI_CC = ['info@pressdetective.com']

ALI_SUBJ = (
    '[FIR 0654/2022] FULL CASE REPORT + URGENT DOCUMENT REQUEST '
    '| Deadline Tomorrow (Saraf) + 14 June (Your Documents) '
    '| Adv. Sujata Shirasi | ' + TODAY
)

ALI_BODY = """\
Dear Mr. Ali Asgar Merchant (Accused No. 1 -- FIR No. 0654/2022),

I am writing to you with an urgent update and a final reminder
of your document deadline.

Adv. Sujata Shirasi | +91 93216 13691

======================================================================
WHERE WE STAND -- 12 JUNE 2026
======================================================================

SARAF'S DEADLINE: TOMORROW 13 JUNE 2026
  The 48-hour notice served on Mr. Abhishek Badriprasad Saraf
  expires TOMORROW. As of today he has not responded and has
  not withdrawn FIR No. 0654/2022.

  If he does not withdraw by end of 13 June 2026:
    -> Section 528 BNSS Quashing Petition filed at Bombay HC
    -> IPC 182 + 192 + 211 criminal complaints against Saraf
    -> ACB inquiry into Inspector Taralgatti
    -> 1,285 national press receive full case details

ALL 9 POLICE / GOVERNMENT AUTHORITIES ON RECORD:
  A formal followup has been sent TODAY (12 June 2026) to all
  9 Maharashtra law enforcement authorities reminding them that
  the quashing petition is being filed tomorrow.

  Authorities holding our complaint:
    ACB Maharashtra (Addl. DGP Shri Vishwas Nangre-Patil)
    Addl. CP ACB Mumbai
    ACP Dadar
    CB-CID Anti-Extortion Cell (the unit that registered the FIR)
    Addl. DG CID Crime, Pune
    DGP Maharashtra
    Secretary (Home), Government of Maharashtra
    CBI Mumbai
    Dadar Police Station

359 MUMBAI JOURNALISTS ALREADY BRIEFED (11 June 2026)
  Full press release delivered individually to 359 journalists.

======================================================================
WHAT THIS CASE RESTS ON -- THE CORE DEFENCE
======================================================================

The single most powerful fact:

  On 4 JUNE 2022 -- Mr. Saraf's ORIGINAL complaint (ID: 23244/2022)
  alleged only a SLAP. No extortion. No Rs. 1 crore demand.
  No mention of Mr. Tarun Thadani.

  TWO MONTHS LATER the complaint was altered to add:
    -> Rs. 1 crore extortion demand (fabricated)
    -> Mr. Thadani's name (he was not present at the venue)

  The FIR was registered on the basis of the altered complaint.
  No CDR checked. No bank records verified. No CCTV reviewed.
  No accused examined before registration.

Mr. Tarun Thadani was NOT at the restaurant on 2 June 2022.
He sent invitations for the gathering only. The altercation was
between you and Mr. Saraf. The maximum offence disclosed by the
original complaint is IPC 323 -- bailable, one year maximum.

This is our case. The documents prove it.

======================================================================
URGENT -- YOUR DOCUMENT DEADLINE: 14 JUNE 2026 (TOMORROW + 1)
======================================================================

Mr. Merchant, I cannot file the strongest possible quashing
petition without your documents. I need the following from you
BY 14 JUNE 2026:

  1. CALL DETAIL RECORDS (CDR) -- June 2022
     Get from your mobile provider (Airtel / Jio / Vi).
     Visit their store or call 121 / 198. Ask for "call records
     for June 2022." This proves no extortion calls were made.

  2. BANK STATEMENTS -- June to September 2022
     From any account you hold. Proves no payment was received
     from Saraf. Direct evidence against the extortion charge.

  3. WHATSAPP / SMS MESSAGES WITH SARAF
     Screenshot every conversation with Abhishek Saraf.
     Before, during and after 2 June 2022.

  4. YOUR WRITTEN ACCOUNT OF 2 JUNE 2022
     What happened. Who did what. What was said. Who was present.
     Whether any demand for money was made by anyone.
     Whether Mr. Tarun Thadani was at the venue.
     (Can be a simple email or WhatsApp voice note to me.)

  5. WITNESS NAMES
     Anyone who was at the restaurant that evening.

  6. CCTV INFORMATION
     Any knowledge of CCTV at the venue or whether footage exists.

  7. WRITTEN CONFIRMATION: THADANI WAS NOT PRESENT
     A simple line: "Mr. Tarun Thadani was not present at the
     restaurant on 2 June 2022."

Send to: sujata.shirasi@pressdetective.com
Or call: +91 93216 13691 (I will take a statement over the phone)

WITHOUT THESE DOCUMENTS, the quashing petition will be filed
on the facts alone. WITH your documents, we go into court with
full evidentiary support. Please do not delay.

======================================================================
ACTIONS TAKEN TO DATE (COMPLETE LOG)
======================================================================

  11 Jun 2026   ACB Maharashtra formal complaint filed (9 authorities)
  11 Jun 2026   Final 48-hour notice served on Saraf
  11 Jun 2026   CB-CID Anti-Extortion Cell review request sent
  11 Jun 2026   359 Mumbai journalists individually briefed
  12 Jun 2026   Accused order confirmed + corrected in all documents
  12 Jun 2026   Police departments followup sent (all 9)
  12 Jun 2026   Saraf FINAL WARNING sent (deadline tomorrow)
  12 Jun 2026   This full report to you

  TOTAL RECIPIENTS TO DATE: 370+ (9 authorities + Saraf + 359 press + you)

======================================================================
KEY DATES
======================================================================

  TOMORROW   13 Jun 2026   Saraf deadline (withdraw or face petition)
  14 Jun 2026               YOUR DOCUMENT DEADLINE
  16 Jun 2026               Original Without Prejudice notice deadline

======================================================================

Please call me today or first thing tomorrow morning.

Adv. Sujata Shirasi
Advocate -- FIR No. 0654/2022 Defence
Phone    : +91 93216 13691
Email    : sujata.shirasi@pressdetective.com
Date     : 12 June 2026

PressDetective | info@pressdetective.com
--
To unsubscribe: reply UNSUBSCRIBE or email info@pressdetective.com
"""


# ============================================================
# SEND ALL THREE
# ============================================================
EMAILS = [
    {
        'label':  'Police Followup (9 depts)',
        'to':     POLICE_TO,
        'cc':     POLICE_CC,
        'subj':   POLICE_SUBJ,
        'body':   POLICE_BODY,
    },
    {
        'label':  'Saraf Final Warning',
        'to':     SARAF_TO,
        'cc':     SARAF_CC,
        'subj':   SARAF_SUBJ,
        'body':   SARAF_BODY,
    },
    {
        'label':  'Ali Full Report',
        'to':     ALI_TO,
        'cc':     ALI_CC,
        'subj':   ALI_SUBJ,
        'body':   ALI_BODY,
    },
]

results = {}
for em in EMAILS:
    all_rcpt = em['to'] + em['cc']
    print(f"\n{'='*60}")
    print(f"Sending: {em['label']}")
    print(f"  TO : {', '.join(em['to'])}")
    print(f"  CC : {', '.join(em['cc'])}")
    msg = build(em['to'], em['cc'], em['subj'], em['body'])
    ok = send(all_rcpt, msg, em['label'])
    results[em['label']] = 'SENT' if ok else 'FAILED'
    if ok:
        time.sleep(3)

print(f"\n{'='*60}")
print('RESULTS:')
for label, status in results.items():
    print(f'  {status}  {label}')
print('Done.')
