#!/usr/bin/env python3
"""
send_acb_complaint.py  --  ACB complaint + Saraf notice + report
Sender: sujata.shirasi@pressdetective.com
Try order: Proton remote SMTP (token) -> Postmark SMTP
"""
import json, smtplib, ssl, sys, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT  = Path(r'C:\dev\pressdetective')
CREDS = json.loads((ROOT / '.creds/proton_accounts.json').read_text(encoding='utf-8-sig'))

FROM_ADDR  = CREDS['accounts']['sujata']['address']
FROM_NAME  = 'Adv. Sujata Shirasi'
SUJATA_TOKEN = CREDS['accounts']['sujata']['token']

PROTON_HOST  = CREDS['smtp_remote']['host']   # smtp.protonmail.ch
PROTON_PORT  = CREDS['smtp_remote']['port']   # 587

POSTMARK_HOST  = CREDS['smtp_postmark']['host']
POSTMARK_PORT  = CREDS['smtp_postmark']['port']
POSTMARK_TOKEN = CREDS['smtp_postmark']['token']

TODAY = '11 June 2026'

# â”€â”€ RECIPIENTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ACB_MAIN   = 'acbwebmail@mahapolice.gov.in'
ACB_CC = [
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
SARAF_EMAIL = 'abhishek_saraf78@yahoo.com'
SARAF_CC    = ['acbwebmail@mahapolice.gov.in', 'info@pressdetective.com', 'aliasgarmerchant@gmail.com']
REPORT_TO   = ['aliasgarmerchant@gmail.com', 'info@pressdetective.com']

# â”€â”€ EMAIL 1: ACB FORMAL COMPLAINT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ACB_SUBJECT = (
    'FORMAL COMPLAINT â€” FIR No. 0654/2022, Dadar PS: '
    'Fabricated Extortion Case | Request for Inquiry & Summoning of Complainant '
    'for Cross-Examination | Adv. Sujata Shirasi'
)
ACB_BODY = f"""\
To,
Shri Vishwas Nangre-Patil, IPS
Additional Director General of Police
Anti-Corruption Bureau, Maharashtra State
Mumbai

CC:
- Addl. Commissioner of Police, ACB Mumbai
- ACP Dadar Division, Mumbai Police
- CB-CID Anti-Extortion Cell, Mumbai
- Addl. DG, CID Crime, Maharashtra
- Director General of Police, Maharashtra
- Secretary (Home), Government of Maharashtra
- CBI Mumbai (Head of Branch / EO)
- Station House Officer, Dadar Police Station

Date: {TODAY}
Subject: FORMAL COMPLAINT â€” Fabricated FIR No. 0654/2022 (Dadar PS) |
         Request for Inquiry into Alteration of Complaint & Lack of Due
         Diligence by Investigating Officer | Summoning of Complainant
         Abhishek Badriprasad Saraf for Cross-Examination

Sir,

I, Adv. Sujata Shirasi, Advocate, Bombay High Court, write to you in my
capacity as the legal representative currently investigating false FIR No.
0654/2022 registered at Dadar Police Station, Mumbai, acting for Mr. Tarun
Thadani and Mr. Ali Asgar Merchant, both named as accused in the said FIR.

I place before you a formal complaint requesting:

  (A) An inquiry by the Anti-Corruption Bureau into how the original
      complaint of 4 June 2022 was materially altered two months later
      to add a Rs. 1 crore extortion allegation that was wholly absent
      from the original complaint;

  (B) An inquiry into the lack of due diligence by Inspector Sanjay
      Taralgatti of the CB-CID Anti-Extortion Cell in registering
      FIR No. 0654/2022; and

  (C) The summoning of the complainant, Mr. Abhishek Badriprasad Saraf,
      for cross-examination / recording of statement under applicable
      provisions of law, in light of the material inconsistencies between
      his original complaint and the FIR.

======================================================================
PART I â€” THE FACTS ON RECORD
======================================================================

1. THE INCIDENT (2 June 2022)
   A private restaurant event took place in Worli, Mumbai on the evening
   of 2 June 2022. An altercation occurred between Mr. Ali Asgar Merchant
   and Mr. Abhishek Badriprasad Saraf. Mr. Tarun Thadani was NOT present
   at the venue. His only connection to the event was having sent out
   invitations. He was not there when any altercation took place.

2. THE ORIGINAL COMPLAINT â€” NO EXTORTION, NO THADANI (4 June 2022)
   Two days after the incident, Mr. Abhishek Badriprasad Saraf filed
   online complaint ID: 23244/2022. That complaint:
     (a) Alleged ONLY that he had been slapped â€” a matter at most under
         IPC Section 323 (bailable, minor offence).
     (b) Contained NO allegation of extortion.
     (c) Contained NO demand for Rs. 1 crore or any sum.
     (d) Did NOT name Mr. Tarun Thadani in any capacity.

   This is the original, unaltered complaint filed by the complainant
   himself.

3. THE MATERIALLY ALTERED COMPLAINT (~August 2022)
   Approximately two months later, a materially different version was
   presented to the police. This new version:
     (a) Added an entirely new allegation â€” that a demand of Rs. 1 crore
         as extortion had been made.
     (b) Inserted Mr. Tarun Thadani's name as an accused for the first
         time, despite his never having been at the venue.
   
   The complainant offers no explanation for the two-month delay or for
   why these serious allegations were absent from his original complaint.

4. FIR REGISTRATION WITHOUT DUE DILIGENCE (12-13 August 2022)
   FIR No. 0654/2022 was registered at Dadar Police Station under
   IPC Sections 384/385/387 and 506 r/w 34 (extortion and criminal
   intimidation). The matter was handled by Inspector Sanjay Taralgatti
   of the CB-CID Anti-Extortion Cell.

   Based on our investigation, the FIR was registered:
     (a) Without examining any of the named accused prior to registration.
     (b) Without verifying Call Detail Records (CDR) to check whether
         any extortion demand was ever communicated.
     (c) Without checking any bank records to verify whether any payment
         was made or demanded.
     (d) Without reviewing CCTV footage available from the venue.
     (e) Without conducting any inquiry into the two-month gap between
         the original complaint and the altered version.

   Sections 384-387 IPC carry sentences of up to 10 years imprisonment
   and are non-bailable. Registering such an FIR without examination of
   accused or verification of evidence constitutes a serious failure of
   due diligence.

5. THE CHARGE-SHEET AND DISCHARGE REFUSAL
   A charge-sheet was filed. In June 2023, the Times of India reported
   the chargesheet, causing severe damage to Mr. Thadani's reputation.
   On 31 March 2024, the Sessions Court refused discharge. Mr. Thadani
   has been attending court for four years for an incident at which he
   was not present and a charge that his own accusers did not make in
   their original complaint.

6. COMPLAINANT'S DOCUMENTED BACKGROUND
   It is respectfully submitted, for the purpose of this inquiry, that
   Mr. Abhishek Badriprasad Saraf has a documented history of involvement
   in contested proceedings. The High Court at Calcutta has been seized
   of civil proceedings (CS No. 313 of 2012 â€” Martin Burn Ltd. v. Saraf)
   for over a decade. The pleadings in those proceedings allege misuse of
   Powers of Attorney, document forgery, and unlawful occupation of the
   third floor of Esplanade House, 29 Hazarimal Somani Marg, Fort, Mumbai
   â€” the same address at which Mr. Saraf currently resides.
   
   These are matters of public court record and are submitted purely
   to provide context relevant to the credibility of the complainant
   and the assessment of his motives.

   Contact details of the complainant for the purpose of any inquiry:
     Name    : Abhishek Badriprasad Saraf
     Address : 3rd Floor, Esplanade House, 29, Hazarimal Somani Marg,
               Fort, Mumbai 400001
     Email   : abhishek_saraf78@yahoo.com
     Phone   : +91 98201 80065
     Landline: 22071113 / 22447435

======================================================================
PART II â€” SPECIFIC REQUESTS TO THE ACB
======================================================================

In light of the above, I most respectfully request this office to:

  1. CONDUCT AN INQUIRY into how complaint ID 23244/2022 (4 June 2022)
     was materially altered to insert an extortion allegation and
     Mr. Thadani's name, and by whom.

  2. INQUIRE INTO THE CONDUCT of Inspector Sanjay Taralgatti, CB-CID
     Anti-Extortion Cell, who registered FIR No. 0654/2022 without
     examining any accused, without CDR verification, without bank
     record checks, and without CCTV review.

  3. SUMMON MR. ABHISHEK BADRIPRASAD SARAF for a formal cross-
     examination / statement under applicable provisions, specifically
     to account for:
       (a) The two-month gap between his original complaint and the
           materially altered version;
       (b) The complete absence of any extortion allegation in the
           original complaint of 4 June 2022;
       (c) Why Mr. Tarun Thadani â€” who was not at the venue â€” was
           inserted as an accused.

  4. TAKE NOTE that a WITHOUT PREJUDICE notice was sent to Mr. Saraf
     on 9 June 2026 demanding withdrawal of the false FIR within 7
     days (deadline: 16 June 2026). No response has been received.

I am available to provide any additional documentation, affidavits
or records that may assist this inquiry. I may be reached at the
contact details below.

Yours faithfully,

Adv. Sujata Shirasi
Advocate â€” Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Phone    : +91 93216 13691
Email    : sujata.shirasi@pressdetective.com
Date     : {TODAY}

PressDetective | info@pressdetective.com
"""

# â”€â”€ EMAIL 2: NOTICE TO ABHISHEK SARAF â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SARAF_SUBJECT = (
    f'FINAL NOTICE â€” Withdraw False FIR No. 0654/2022 Within 48 Hours | '
    f'ACB Maharashtra Complaint Filed | Adv. Sujata Shirasi | {TODAY}'
)
SARAF_BODY = f"""\
WITHOUT PREJUDICE

To,
Mr. Abhishek Badriprasad Saraf
3rd Floor, Esplanade House
29, Hazarimal Somani Marg, Fort
Mumbai 400001

Email : abhishek_saraf78@yahoo.com
Phone : +91 98201 80065

Date  : {TODAY}

Dear Mr. Saraf,

I refer to my WITHOUT PREJUDICE notice of 9 June 2026, to which no
response has been received.

I write to inform you that, as of today, 11 June 2026, a FORMAL
COMPLAINT has been filed with the Anti-Corruption Bureau of Maharashtra,
addressed to Shri Vishwas Nangre-Patil, IPS, Additional Director General
of Police, ACB Maharashtra, requesting:

  (a) An inquiry into how your original online complaint of 4 June 2022
      (ID: 23244/2022) â€” which alleged only a slap and contained no
      mention of extortion and no mention of Mr. Tarun Thadani â€” was
      materially altered two months later to insert these allegations;

  (b) An inquiry into the conduct of Inspector Sanjay Taralgatti in
      registering FIR No. 0654/2022 without examining any accused or
      verifying any evidence;

  (c) That you be summoned for cross-examination on the material
      inconsistencies between your original complaint and the FIR.

The ACB complaint has been copied to the Commissioner's Office,
CB-CID Anti-Extortion Cell, CID Crime Maharashtra, DGP Maharashtra,
the Maharashtra Home Department, CBI Mumbai, and Dadar Police Station.

THE DOCUMENTED FACTS AGAINST YOUR COMPLAINT:

  1. Your own complaint of 4 June 2022 contained ZERO mention of
     extortion and ZERO mention of Mr. Thadani. This is a matter
     of record.

  2. Mr. Tarun Thadani was not at the venue on 2 June 2022. He had
     sent invitations but was not present. There is no evidence of
     him being there or making any demand of any kind.

  3. The altercation was between Mr. Ali Asgar Merchant and yourself.
     There is no evidence on record â€” no call records, no bank
     transfers, no messages, no witnesses â€” showing any extortion
     demand was ever made.

  4. The Rs. 1 crore extortion allegation and Mr. Thadani's name
     appeared for the first time two months after the incident,
     at a stage when the police had told you that a slap alone
     was a minor, bailable matter.

YOUR EXPOSURE IF YOU DO NOT WITHDRAW:

  Filing a false complaint, fabricating evidence, and making false
  charges with intent to injure a person are cognisable offences under
  the Indian Penal Code (Sections 182, 192, 211). You face potential
  criminal proceedings under these provisions in addition to the ACB
  inquiry now initiated.

  The matter is also before the Bombay High Court by way of a proposed
  quashing petition under Section 528 BNSS, where the documented
  inconsistencies in your complaint will be placed before the Hon'ble
  Court.

  A press release detailing the facts of this case has already been
  distributed to over 426 journalists and media outlets across India.
  A further 1,285 press contacts are being reached. The documented
  record â€” including your original complaint showing no extortion and
  no Thadani â€” is in the public domain.

YOU ARE CALLED UPON to withdraw FIR No. 0654/2022 in its entirety
within 48 hours of receipt of this notice (i.e., by 13 June 2026).

Failure to do so will result in:
  - Filing of the Section 528 BNSS Quashing Petition before the
    Bombay High Court;
  - Criminal complaints under IPC Sections 182, 192 and 211 against
    you;
  - Full cooperation with the ACB inquiry, including production of
    all documentation.

This notice is issued WITHOUT PREJUDICE to all legal rights and
remedies available to Mr. Tarun Thadani and Mr. Ali Asgar Merchant.

Yours faithfully,

Adv. Sujata Shirasi
Advocate â€” Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Phone    : +91 93216 13691
Email    : sujata.shirasi@pressdetective.com
Date     : {TODAY}

NOTE: This notice has been sent by email and is copied to the
Anti-Corruption Bureau of Maharashtra and PressDetective for record.
"""

# â”€â”€ EMAIL 3: REPORT TO ALIASGAR + INFO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
REPORT_SUBJECT = (
    f'[FIR 0654/2022] ACB COMPLAINT FILED + SARAF FINAL NOTICE SENT â€” '
    f'Report | {TODAY} | Adv. Sujata Shirasi'
)
REPORT_BODY = f"""\
Dear Mr. Ali Asgar Merchant,

This is a report on actions taken today, {TODAY}, in FIR No. 0654/2022.

======================================================================
ACTIONS TAKEN TODAY â€” {TODAY}
======================================================================

1. FORMAL COMPLAINT TO ACB MAHARASHTRA â€” FILED
   â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
   A formal complaint has been filed with:
   
   Shri Vishwas Nangre-Patil, IPS
   Additional Director General of Police
   Anti-Corruption Bureau, Maharashtra State, Mumbai

   Email : acbwebmail@mahapolice.gov.in
   
   The complaint was also copied to:
   - Addl. Commissioner of Police, ACB Mumbai
   - ACP Dadar
   - CB-CID Anti-Extortion Cell
   - Addl. DG CID Crime Maharashtra
   - DGP Maharashtra
   - Secretary (Home), Maharashtra
   - CBI Mumbai
   - Dadar Police Station

   Total authorities copied: 9

   THE COMPLAINT REQUESTS:
     (a) An inquiry into how Saraf's original complaint (no extortion,
         no Thadani) was materially altered two months later;
     (b) An inquiry into Inspector Taralgatti's lack of due diligence
         in registering FIR 0654/2022;
     (c) Summoning of Abhishek Saraf for cross-examination on the
         inconsistencies in his complaint.

2. FINAL NOTICE TO ABHISHEK SARAF â€” SENT
   â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
   A FINAL NOTICE has been sent directly to Abhishek Badriprasad Saraf
   at abhishek_saraf78@yahoo.com.

   The notice:
     - Informed him of the ACB complaint filed today;
     - Gave him 48 hours to withdraw the FIR (deadline: 13 June 2026);
     - Set out the documented facts against his complaint;
     - Warned of Section 528 BNSS quashing petition and criminal
       complaints under IPC 182/192/211 if he refuses.
   
   The notice was copied to ACB (acbwebmail@mahapolice.gov.in),
   info@pressdetective.com and aliasgarmerchant@gmail.com.

======================================================================
CURRENT TIMELINE & DEADLINES
======================================================================

  11 June 2026 : ACB complaint filed. Saraf final notice sent.
  13 June 2026 : 48-hour deadline for Saraf to respond to final notice.
  16 June 2026 : Original WITHOUT PREJUDICE notice deadline.
  
  If no response by 13-16 June:
    -> File Section 528 BNSS Quashing Petition, Bombay High Court
    -> File criminal complaints under IPC 182, 192, 211 against Saraf
    -> Full cooperation with ACB inquiry

======================================================================
PRESS RELEASE STATUS
======================================================================

  Delivered so far : 426 press/media contacts (national + legal media)
  Remaining        : 1,285 contacts (paused â€” being rescheduled)
  Key outlets      : The Hindu, Indian Express, The Wire, NDTV,
                     LiveLaw, Bar & Bench, Caravan, Frontline,
                     Times Now, CNBC-TV18, India Today, Outlook...

======================================================================

Please confirm if you have received all prior communications including
the legal update of 9 June 2026 and the action items requested of you.

Please call me if you have any questions: +91 93216 13691

Yours faithfully,

Adv. Sujata Shirasi
Advocate â€” Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Phone    : +91 93216 13691
Email    : sujata.shirasi@pressdetective.com
Date     : {TODAY}
"""

# â”€â”€ SMTP HELPERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def smtp_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def try_providers(from_addr, to_list, subject, body, label):
    """Try Proton remote SMTP, then Postmark. Returns (provider, error)."""
    msg = MIMEMultipart('alternative')
    msg['From']     = f'{FROM_NAME} <{from_addr}>'
    msg['To']       = to_list[0] if len(to_list) == 1 else to_list[0]
    if len(to_list) > 1:
        msg['Cc'] = ', '.join(to_list[1:])
    msg['Subject']  = subject
    msg['Reply-To'] = from_addr
    msg['List-Unsubscribe'] = '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    all_rcpt = to_list

    # Postmark stream header (required; set before any provider attempt)
    msg['X-PM-Message-Stream'] = 'outbound'

    # 1. Proton remote SMTP
    print(f'  [{label}] Trying Proton remote SMTP ({PROTON_HOST}:{PROTON_PORT}) ...')
    try:
        ctx = smtp_ctx()
        with smtplib.SMTP(PROTON_HOST, PROTON_PORT, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(from_addr, SUJATA_TOKEN)
            s.sendmail(from_addr, all_rcpt, msg.as_string())
        print(f'  [{label}] OK via Proton remote')
        return 'proton-remote', None
    except Exception as e:
        print(f'  [{label}] Proton remote failed: {str(e)[:100]}')

    # 2. Postmark SMTP
    print(f'  [{label}] Trying Postmark ({POSTMARK_HOST}:{POSTMARK_PORT}) ...')
    try:
        ctx = smtp_ctx()
        with smtplib.SMTP(POSTMARK_HOST, POSTMARK_PORT, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(POSTMARK_TOKEN, POSTMARK_TOKEN)
            s.sendmail(from_addr, all_rcpt, msg.as_string())
        print(f'  [{label}] OK via Postmark')
        return 'postmark', None
    except Exception as e:
        err = str(e)
        print(f'  [{label}] Postmark failed: {err[:100]}')
        return None, err


# â”€â”€ MAIN â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
results = {}

print('=' * 65)
print('ACB COMPLAINT + SARAF NOTICE + REPORT â€” 3 emails, 12 recipients')
print('=' * 65)
print()

# Email 1: ACB complaint
print('Email 1/3 â€” ACB Formal Complaint')
print(f'  TO : {ACB_MAIN}')
print(f'  CC : {", ".join(ACB_CC)}')
acb_all = [ACB_MAIN] + ACB_CC
provider, err = try_providers(FROM_ADDR, acb_all, ACB_SUBJECT, ACB_BODY, 'ACB')
results['ACB complaint'] = provider or f'FAILED: {err}'
print()

# Email 2: Saraf final notice
print('Email 2/3 â€” Final Notice to Abhishek Saraf')
print(f'  TO : {SARAF_EMAIL}')
print(f'  CC : {", ".join(SARAF_CC)}')
saraf_all = [SARAF_EMAIL] + SARAF_CC
provider, err = try_providers(FROM_ADDR, saraf_all, SARAF_SUBJECT, SARAF_BODY, 'SARAF')
results['Saraf notice'] = provider or f'FAILED: {err}'
print()

# Email 3: Report to Aliasgar + info
print('Email 3/3 â€” Report to Aliasgar + info@')
print(f'  TO : {", ".join(REPORT_TO)}')
provider, err = try_providers(FROM_ADDR, REPORT_TO, REPORT_SUBJECT, REPORT_BODY, 'REPORT')
results['Report'] = provider or f'FAILED: {err}'
print()

print('=' * 65)
print('SUMMARY')
print('=' * 65)
for k, v in results.items():
    print(f'  {k:<20} {v}')
print()
recipients_reached = (
    [ACB_MAIN] + ACB_CC +
    [SARAF_EMAIL] + SARAF_CC +
    REPORT_TO
)
unique = list(dict.fromkeys(recipients_reached))
print(f'Unique recipients: {len(unique)}')
for r in unique:
    print(f'  {r}')