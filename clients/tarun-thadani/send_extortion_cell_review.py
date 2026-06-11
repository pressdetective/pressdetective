#!/usr/bin/env python3
"""
send_extortion_cell_review.py
Formal request to CB-CID Anti-Extortion Cell for case review + Taralgatti inquiry.
CC all parties: ACB, Saraf (asking to withdraw), Ali (asking for comments).
Sender: sujata.shirasi@pressdetective.com via Proton remote SMTP / Postmark fallback.
"""
import smtplib, ssl, json, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT     = Path(r'C:\dev\pressdetective')
CREDS    = json.loads((ROOT / '.creds/proton_accounts.json').read_text(encoding='utf-8'))
FROM     = CREDS['accounts']['sujata']['address']
FROM_NAME = 'Adv. Sujata Shirasi'
TOKEN    = CREDS['accounts']['sujata']['token']
HOST     = CREDS['smtp_remote']['host']
PORT     = CREDS['smtp_remote']['port']
PM_HOST  = CREDS['smtp_postmark']['host']
PM_PORT  = CREDS['smtp_postmark']['port']
PM_TOKEN = CREDS['smtp_postmark']['token']

TODAY = '11 June 2026'

TO_PRIMARY = 'cbcidmumaecell@mahapolice.gov.in'
CC_LIST = [
    'acbwebmail@mahapolice.gov.in',
    'abhishek_saraf78@yahoo.com',
    'aliasgarmerchant@gmail.com',
    'info@pressdetective.com',
]
ALL_RCPT = [TO_PRIMARY] + CC_LIST

SUBJECT = (
    'URGENT REQUEST FOR CASE REVIEW — FIR No. 0654/2022, Dadar PS | '
    'Inquiry into Investigation Conduct | Request to All Parties for '
    'Comments | Adv. Sujata Shirasi | ' + TODAY
)

BODY = f"""\
To,
The Officer-in-Charge / Competent Authority
CB-CID Anti-Extortion Cell
Mumbai Police
Email: cbcidmumaecell@mahapolice.gov.in

CC:
  (i)  Anti-Corruption Bureau, Maharashtra (acbwebmail@mahapolice.gov.in)
  (ii) Mr. Abhishek Badriprasad Saraf — Complainant (abhishek_saraf78@yahoo.com)
  (iii) Mr. Ali Asgar Merchant — Accused No. 2 (aliasgarmerchant@gmail.com)
  (iv)  PressDetective, for record (info@pressdetective.com)

Date: {TODAY}

Subject: Formal Request for Review of FIR No. 0654/2022 (Dadar Police
         Station) | Request for Inquiry into Investigation by Inspector
         Sanjay Taralgatti | Request to the Complainant to Come Forward
         | Request to Accused Parties for Their Comments

======================================================================
RESPECTFUL PRELIMINARY NOTE
======================================================================

With the utmost respect to this office and to the hard work of the
CB-CID Anti-Extortion Cell in protecting citizens of Maharashtra from
genuine extortion, I write this letter in the spirit of ensuring that
the very purpose of this Cell — the pursuit of truth and the protection
of the innocent — is upheld in the matter of FIR No. 0654/2022.

I am Adv. Sujata Shirasi, Advocate, Bombay High Court. I represent
Mr. Tarun Thadani and act in the interests of Mr. Ali Asgar Merchant,
both accused in FIR No. 0654/2022 registered at Dadar Police Station.

I approach this office not to be adversarial, but because I believe
that a careful review of the material in this matter will reveal that
the FIR as registered does not accurately reflect the original complaint
filed by the complainant, and that the investigation that preceded
registration was materially insufficient for charges of such gravity.

I most respectfully request this office to look into this matter
afresh — not because I disrespect the institution, but precisely
because I believe in it.

======================================================================
PART I — BACKGROUND: THE CASE AND THE COMPLAINT
======================================================================

1. FIR No. 0654/2022 was registered at Dadar Police Station,
   Mumbai, on approximately 12-13 August 2022 by Inspector Sanjay
   Taralgatti of the CB-CID Anti-Extortion Cell, under IPC Sections
   384, 385, 387 and 506 read with Section 34 (non-bailable extortion
   and criminal intimidation).

2. The FIR names as accused:
     (a) Mr. Tarun Thadani — who, with respect, was NOT present at the
         venue on 2 June 2022. He had arranged invitations for the
         gathering but was not physically present when the alleged
         incident occurred.
     (b) Mr. Ali Asgar Merchant — who was present at the venue.

3. The incident itself, on 2 June 2022 at a restaurant in Worli,
   Mumbai, involved a physical altercation between Mr. Ali Asgar
   Merchant and Mr. Abhishek Badriprasad Saraf.

======================================================================
PART II — THE MATERIAL INCONSISTENCY IN THE COMPLAINT
======================================================================

4. On 4 June 2022 — two days after the incident — the complainant,
   Mr. Abhishek Badriprasad Saraf, filed an online complaint bearing
   reference ID: 23244/2022.

   With great respect, I invite this office to examine that original
   complaint carefully. That complaint:

     (a) Alleged ONLY that Mr. Saraf had been slapped — an incident
         that at most constitutes an offence under IPC Section 323
         (bailable, maximum one year, compoundable).
     (b) Contained NO allegation of any extortion demand.
     (c) Mentioned NO demand for Rs. 1 crore or any other sum.
     (d) Did NOT name Mr. Tarun Thadani in any capacity whatsoever.

5. Approximately two months after complaint ID 23244/2022 was filed,
   a materially different version of the complaint came to light — one
   that for the first time alleged:
     (a) A demand of Rs. 1 crore as extortion; and
     (b) The involvement of Mr. Tarun Thadani.

   I respectfully submit that the original complaint of 4 June 2022
   and the later version that preceded FIR registration are materially
   inconsistent in ways that go to the very heart of the FIR.

   This is not a minor discrepancy. The entire basis for the
   non-bailable extortion charge — and the inclusion of Mr. Thadani
   as an accused — was absent from the complainant's own first account
   of events.

======================================================================
PART III — THE INVESTIGATION THAT PRECEDED THE FIR
======================================================================

6. With the greatest respect to Inspector Sanjay Taralgatti and to
   this Cell, I am constrained to bring to this office's attention
   the following matters regarding the investigation conducted before
   FIR registration:

   (a) NO PRE-REGISTRATION EXAMINATION OF ACCUSED
       To the best of our knowledge and on the basis of available
       records, none of the accused — including Mr. Tarun Thadani or
       Mr. Ali Asgar Merchant — was examined by the investigating
       officer prior to the registration of the FIR.

       In a case involving a non-bailable charge carrying up to ten
       years of imprisonment, the examination of the accused party
       before registration — or at minimum a preliminary inquiry —
       would ordinarily be expected.

   (b) NO CALL DETAIL RECORD VERIFICATION
       Extortion is a communicative crime. It requires a demand.
       That demand must have been transmitted — by phone, message,
       or in person. To our knowledge, no Call Detail Records were
       obtained or verified before the FIR was registered.

       If no CDR was checked, on what evidentiary basis was the
       extortion demand established?

   (c) NO BANK RECORD VERIFICATION
       If Rs. 1 crore was extorted, there must be evidence of either
       a demand for payment or a payment received. To our knowledge,
       no bank statements or payment records were examined.

   (d) NO CCTV REVIEW
       The incident occurred in a restaurant. Surveillance footage
       would have established the sequence of events, who was present,
       and what was said. To our knowledge, no CCTV footage was
       reviewed before registration.

   (e) THE TWO-MONTH GAP WAS NOT INVESTIGATED
       The most fundamental question — why the Rs. 1 crore demand
       and Mr. Thadani's name were absent from the complaint for
       two months and then suddenly appeared — does not appear to
       have been the subject of any preliminary inquiry.

7. I wish to be clear: I raise these matters not to impugn the
   integrity of Inspector Taralgatti personally, but because the
   legal consequences for the accused of a non-bailable FIR are
   severe, and those consequences demand that the investigation
   preceding registration be thorough. In this case, with the
   deepest respect, I submit that it was not.

======================================================================
PART IV — REQUEST TO THE CB-CID ANTI-EXTORTION CELL
======================================================================

In light of the above, I most respectfully request this office to:

  1. REVIEW the file of FIR No. 0654/2022 and the investigation
     that preceded its registration, having regard to the material
     inconsistency between complaint ID 23244/2022 (4 June 2022)
     and the version that preceded the FIR.

  2. INQUIRE into whether the prescribed procedure for registration
     of a non-bailable extortion FIR was followed in this matter,
     and in particular whether any preliminary inquiry was conducted
     under the provisions of the Criminal Procedure Code / BNSS
     before registration.

  3. CALL UPON the complainant, Mr. Abhishek Badriprasad Saraf,
     to provide a full and satisfactory explanation for the material
     differences between his original complaint of 4 June 2022 and
     the complaint version that preceded FIR registration.

  4. OBTAIN and review the Call Detail Records and bank statements
     of all relevant parties for the period June–August 2022, if
     this has not already been done.

  5. TAKE NOTE that a formal complaint has been filed with the Anti-
     Corruption Bureau of Maharashtra (addressed to Addl. DGP Shri
     Vishwas Nangre-Patil, IPS) regarding this same matter on this
     date, requesting a parallel inquiry.

======================================================================
PART V — REQUEST TO MR. ABHISHEK BADRIPRASAD SARAF (CC'd)
======================================================================

[This section is addressed directly to Mr. Abhishek Badriprasad Saraf,
who is CC'd on this correspondence.]

Dear Mr. Saraf,

I write to you with sincerity and without hostility.

You know the truth of what happened on 2 June 2022. Your own
original complaint of 4 June 2022 — filed two days after the event,
when your memory of it was freshest — contained no mention of
extortion, no demand for Rs. 1 crore, and no mention of Mr. Tarun
Thadani.

Three law enforcement authorities now have this case before them:
the CB-CID Anti-Extortion Cell, the Anti-Corruption Bureau, and
there is an application before the Bombay High Court. A press release
has been delivered to 426 journalists. The documented record of
your original complaint, and what it did and did not contain, is
now in the public domain.

I write to you with this appeal: come forward honestly. If you
believe this case should proceed, I respectfully ask you to respond
to the CB-CID Anti-Extortion Cell in reply to this letter, explaining
on the record:

  (a) Why your original complaint of 4 June 2022 contained no
      mention of extortion or of Mr. Thadani.
  (b) What prompted the material changes to your complaint two
      months after it was first filed.
  (c) What evidence you have of any extortion demand — phone
      records, messages, witnesses.

If you cannot provide satisfactory answers to these questions, I
urge you in the strongest possible terms — and with genuine concern
for your own situation — to withdraw FIR No. 0654/2022 before
further departments, courts and public institutions become involved.

It is not too late. The truth is a path to resolution. Every day
that passes closes that path further.

======================================================================
PART VI — REQUEST TO MR. ALI ASGAR MERCHANT (CC'd)
======================================================================

[This section is addressed to Mr. Ali Asgar Merchant, who is CC'd.]

Dear Mr. Merchant,

I write to you to request, formally and for the record, that you
provide your account of events of 2 June 2022 to the CB-CID
Anti-Extortion Cell in response to this correspondence.

Specifically, please confirm:

  (a) Your presence at the restaurant on 2 June 2022 and the
      circumstances of the altercation with Mr. Saraf.
  (b) Whether you or Mr. Tarun Thadani made any demand for money
      from Mr. Saraf at any time — before, during or after the event.
  (c) Whether Mr. Tarun Thadani was present at the venue on the
      evening of 2 June 2022.
  (d) Any witnesses who were present and observed the events.

Your statement will form part of the record before the CB-CID,
the ACB, and ultimately the Bombay High Court. Please respond at
the earliest opportunity.

Please also contact me directly: +91 93216 13691.

======================================================================
CLOSING
======================================================================

I thank this office most sincerely for its time and attention.

The only purpose of this letter is to ensure that the truth prevails.
If the evidence supports the charges in FIR 0654/2022, let that be
established through proper inquiry. If it does not, then the interests
of justice — which this Cell exists to serve — demand that the matter
be reviewed.

I remain at the complete disposal of this office and will provide any
documentation, affidavits or records requested.

Yours faithfully and respectfully,

Adv. Sujata Shirasi
Advocate — Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Phone    : +91 93216 13691
Email    : sujata.shirasi@pressdetective.com
Date     : {TODAY}

PressDetective | info@pressdetective.com

----------------------------------------------------------------------
Note: This correspondence has been sent to the CB-CID Anti-Extortion
Cell, the Anti-Corruption Bureau of Maharashtra, Mr. Abhishek
Badriprasad Saraf, Mr. Ali Asgar Merchant, and PressDetective for
record. All parties are requested to respond on the record.
----------------------------------------------------------------------
"""


def smtp_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def build_msg():
    msg = MIMEMultipart('alternative')
    msg['From']    = f'{FROM_NAME} <{FROM}>'
    msg['To']      = TO_PRIMARY
    msg['Cc']      = ', '.join(CC_LIST)
    msg['Subject'] = SUBJECT
    msg['Reply-To'] = FROM
    msg['List-Unsubscribe'] = '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    msg.attach(MIMEText(BODY, 'plain', 'utf-8'))
    return msg


print('=' * 65)
print('ANTI-EXTORTION CELL REVIEW REQUEST')
print(f'TO : {TO_PRIMARY}')
print(f'CC : {chr(10).join("     " + c for c in CC_LIST)}')
print('=' * 65)

msg = build_msg()
sent = False

print(f'Trying Proton remote SMTP ({HOST}:{PORT}) ...')
try:
    ctx = smtp_ctx()
    with smtplib.SMTP(HOST, PORT, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.ehlo()
        s.login(FROM, TOKEN)
        s.sendmail(FROM, ALL_RCPT, msg.as_string())
    print('OK via Proton remote')
    sent = True
except Exception as e:
    print(f'Proton remote failed: {str(e)[:100]}')

if not sent:
    print(f'Trying Postmark ({PM_HOST}:{PM_PORT}) ...')
    try:
        ctx = smtp_ctx()
        with smtplib.SMTP(PM_HOST, PM_PORT, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(PM_TOKEN, PM_TOKEN)
            s.sendmail(FROM, ALL_RCPT, msg.as_string())
        print('OK via Postmark')
        sent = True
    except Exception as e:
        print(f'Postmark failed: {str(e)[:100]}')

if not sent:
    print('ERROR: All providers failed')
    sys.exit(1)

print()
print('RECIPIENTS:')
for r in ALL_RCPT:
    print(f'  {r}')
print()
print('DONE.')
