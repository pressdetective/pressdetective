#!/usr/bin/env python3
"""
send_saraf_notice.py
Without-Prejudice notice to Abhishek Saraf — final opportunity to withdraw FIR 0654/2022
Sender : sujata.shirasi@pressdetective.com (Adv. Sujata Shirasi)
To     : abhishek_saraf78@yahoo.com
CC     : ACB, CID, Dadar PS, Azad Maidan PS, Anti-Extortion Cell, Aliasgar Merchant, info@
Report : aliasgarmerchant@gmail.com + info@pressdetective.com
Via    : ZeptoMail SMTP_SSL
"""
import smtplib, ssl, sys, time
from email.message import EmailMessage

import json, pathlib
_creds    = json.loads((pathlib.Path(__file__).parents[2] / '.creds/proton_accounts.json').read_text())
HOST      = _creds['smtp_bridge']['host']       # 127.0.0.1
PORT      = _creds['smtp_bridge']['port']       # 1025
SMTP_USER = _creds['accounts']['sujata']['address']
SMTP_PASS = _creds['accounts']['sujata']['bridge_password']
FROM_ADDR = _creds['accounts']['sujata']['address']
FROM_NAME = 'Adv. Sujata Shirasi'

TO_ADDR   = 'abhishek_saraf78@yahoo.com'
TO_NAME   = 'Abhishek Badriprasad Saraf'

REPORT_TO = ['aliasgarmerchant@gmail.com', 'info@pressdetective.com']

# CC list: officials + Aliasgar Merchant + info@
CC_LIST = [
    # Aliasgar Merchant (co-accused, directly affected party)
    'aliasgarmerchant@gmail.com',
    # Anti-Corruption Bureau
    'acbwebmail@mahapolice.gov.in',
    'addlcpacbmumbai@mahapolice.gov.in',
    'nagraj.patil@nic.in',
    # Dadar Police Station (where FIR 0654/2022 was filed)
    'ps.dadar.mum@mahapolice.gov.in',
    'acpdadar.mum@mahapolice.gov.in',
    # Azad Maidan Police Station
    'ps.azadmaidan.mum@mahapolice.gov.in',
    # CB-CID Anti-Extortion Cell (registered FIR)
    'cbcidmumaecell@mahapolice.gov.in',
    'dcbcid.cawc-mum@mahapolice.gov.in',
    # CID Crime Maharashtra
    'adg.cidcrime.pune@mahapolice.gov.in',
    'cp.mum.addcp.sbcid@mahapolice.gov.in',
    # CBI Mumbai
    'hozmum@cbi.gov.in',
    'hobeomum@cbi.gov.in',
    # PressDetective
    'info@pressdetective.com',
]

SUBJECT = (
    'WITHOUT PREJUDICE — Final Opportunity to Withdraw False FIR No. 0654/2022 | '
    'Dadar Police Station | Tarun Thadani | Hearing Today 9 June 2026'
)

BODY = """\
Dear Mr. Abhishek Badriprasad Saraf,

I write to you as an Advocate currently investigating false FIR No. 0654/2022 \
— a case I am convinced was deliberately fabricated and used to target two innocent \
men: Mr. Tarun Thadani and Mr. Ali Asgar Merchant. I write on a WITHOUT PREJUDICE \
basis, to afford you one final opportunity — in good faith — to do the right thing.

This letter is copied to the Anti-Corruption Bureau, the Crime Investigation \
Department, Dadar Police Station, Azad Maidan Police Station, the CB-CID \
Anti-Extortion Cell, CBI Mumbai, and Mr. Ali Asgar Merchant, so that every \
relevant authority is aware of what is being asked of you, and why.

──────────────────────────────────────────────────
TODAY'S COURT HEARING
──────────────────────────────────────────────────

As you are well aware, today — 9 June 2026 — is yet another hearing date in \
the matter arising from the same incident. Mr. Thadani has now attended court \
for the fourth consecutive year. This is a man who was not even present at the \
restaurant when the altercation between you and Mr. Ali Asgar Merchant took place.

CNR: MHMM110046312023 | Case No.: PW/3700470/2023
Court: Addl. Chief Judicial Magistrate, 37th Court, Mumbai

──────────────────────────────────────────────────
THE TRUTH — WHICH THE RECORDS SHOW
──────────────────────────────────────────────────

On 4 June 2022, you filed an online complaint (ID 23244/2022) alleging a slap \
from Mr. Ali Asgar Merchant. That complaint contained NO allegation of extortion. \
No demand of money. No mention of Mr. Tarun Thadani at all — Mr. Thadani was \
not at the venue. His only connection to the event was having sent out invitations.

You were told by the police that a slap was a minor offence. You did not accept that answer.

Approximately two months later, the complaint was fundamentally changed. A new \
allegation appeared: that Rs. 1 crore had been demanded as extortion. For the \
very first time, Mr. Tarun Thadani — who was not at the venue at all, whose \
only connection to the event was having sent invitations — was inserted as an accused.

FIR No. 0654/2022 was then registered at Dadar Police Station on 12-13 August \
2022, without a single accused being examined beforehand, without any call records, \
bank statements or CCTV evidence being verified.

These are not our allegations. These are the facts — they are written in the \
sequence of your own complaint, in the police records, and in the CCTV footage.

──────────────────────────────────────────────────
YOUR HISTORY — WHICH IS NOW A MATTER OF PUBLIC RECORD
──────────────────────────────────────────────────

Mr. Saraf, we are aware of who you are and of your conduct in other matters:

  • You illegally occupy the entire third floor of Esplanade House, 29 Hazarimal \
Somani Marg, Fort, Mumbai — a UNESCO-listed heritage building — under a tenancy \
held by Martin Burn Limited. You obtained three Powers of Attorney from the \
Fatehpuria family in March 2009 and used them to forge documents, divert rental \
income, extract Rs. 40 lakhs, and take over the property.

  • Martin Burn Limited has been pursuing you in the High Court at Calcutta \
(CS No. 313 of 2012) for over a decade on grounds of fraud, misuse of Power of \
Attorney, and illegal occupation. Despite judgments, orders and interventions by \
multiple courts and authorities, you continue to occupy that property and continue \
to evade accountability.

  • You came from Calcutta to Mumbai, ingratiated yourself into circles of trust, \
and have used manipulation of the legal system as a weapon — against the \
Fatehpuria family, against Martin Burn Limited, and now against Mr. Tarun Thadani \
and Mr. Ali Asgar Merchant.

You are now well known to every authority copied on this letter.

──────────────────────────────────────────────────
WHAT WE HAVE DONE — AND WHAT WE WILL DO
──────────────────────────────────────────────────

In the public interest and in pursuit of the truth, we have:

  1. Written formally to the Anti-Corruption Bureau of Maharashtra, requesting \
an inquiry into how the original complaint of 4 June 2022 was materially altered \
to add an extortion charge that did not exist.

  2. Written to the Commissioner's Office and senior officers of the CB-CID \
Anti-Extortion Cell, requesting an inquiry into the lack of due diligence by \
Inspector Sanjay Taralgatti in registering FIR 0654/2022 without examining any \
accused, without verifying any evidence, and without establishing that Mr. Thadani \
was ever at the venue.

  3. Informed CBI Mumbai of the pattern of conduct across Mumbai and Calcutta.

  4. Notified 3,031 journalists, senior government officers, police officers and \
public representatives across Mumbai and Maharashtra, with full particulars of \
this case and your background.

  5. Filed a defamation notice against the Times of India for publishing a story \
based on the chargesheet without verifying the facts.

  6. Prepared and are ready to file criminal complaints against you under:
       - Section 182 IPC — for giving false information to a public servant
       - Section 192 IPC — for fabricating evidence
       - Section 211 IPC — for false charge of offence made with intent to injure
       - Section 499/500 IPC — for criminal defamation of Mr. Thadani

  7. We are ready to approach the High Court, the National Human Rights Commission \
and any other authority to ensure this case becomes a documented example of how \
the criminal justice system must NOT be misused.

──────────────────────────────────────────────────
OUR REQUEST TO YOU — IN GOOD FAITH
──────────────────────────────────────────────────

Mr. Saraf, this letter is not sent in anger. It is sent in good faith.

You have an opportunity, even at this late stage, to do something honest: \
to withdraw the false case against Mr. Tarun Thadani and Mr. Ali Asgar Merchant. \
To admit — at least to yourself — that a slap in a personal dispute, however \
regrettable, does not justify a fabricated extortion charge and four years of \
damage to innocent people's lives.

We request you, with full sincerity, to withdraw FIR No. 0654/2022 within \
7 days of the date of this letter.

If you choose not to, we will exercise every legal right available. The criminal \
complaints listed above will be filed. Every forum — the courts, the ACB, the CBI, \
the media — will be engaged. This case will become a documented public example \
of how one individual misused the Mumbai Police to punish men who had done him \
no wrong.

The choice — and the responsibility — is yours.

──────────────────────────────────────────────────

Yours faithfully,

Adv. Sujata Shirasi
Advocate — Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Phone: +91 93216 13691
E-mail: sujata.shirasi@pressdetective.com

Date: 9 June 2026

──────────────────────────────────────────────────
NOTE TO COPIED AUTHORITIES
──────────────────────────────────────────────────

The institutions and officers copied on this letter are requested to take note \
of the facts stated above and to keep this communication on record. We remain \
available to provide any further information, documents or assistance required.
"""


REPORT_SUBJECT = (
    '[TT-FIR][NOTICE-SENT][9Jun2026] Without-Prejudice notice to Abhishek Saraf '
    '— FIR 0654/2022 | ACB + CID + Police copied | sujata.shirasi@pressdetective.com'
)

REPORT_BODY = """\
PressDetective — Action Report
Date: 9 June 2026
Matter: Tarun Thadani & Ali Asgar Merchant / FIR No. 0654/2022 / Abhishek Badriprasad Saraf
Investigating Advocate: Adv. Sujata Shirasi

──────────────────────────────────────────────
TODAY'S ACTION
──────────────────────────────────────────────

A WITHOUT PREJUDICE letter was sent directly to Abhishek Badriprasad Saraf
at: abhishek_saraf78@yahoo.com

The letter:
  - Confirms today's court hearing (CNR MHMM110046312023, Case PW/3700470/2023)
  - States the facts of the falsified FIR 0654/2022
  - Lists all departments and authorities that have been notified
  - Formally requests withdrawal of the false case within 7 days
  - Puts him on notice of criminal complaints under s.182/192/211/499 IPC
  - Is copied to every relevant authority (see below)

──────────────────────────────────────────────
COPIED AUTHORITIES — FULL LIST
──────────────────────────────────────────────

  1.  aliasgarmerchant@gmail.com       — Mr. Ali Asgar Merchant (co-accused)
  2.  acbwebmail@mahapolice.gov.in     — Anti-Corruption Bureau Maharashtra
  3.  addlcpacbmumbai@mahapolice.gov.in — Addl. CP ACB Mumbai
  4.  nagraj.patil@nic.in              — Inspector Nagraj Patil
  5.  ps.dadar.mum@mahapolice.gov.in  — Dadar Police Station (FIR filed here)
  6.  acpdadar.mum@mahapolice.gov.in  — ACP Dadar
  7.  ps.azadmaidan.mum@mahapolice.gov.in — Azad Maidan Police Station
  8.  cbcidmumaecell@mahapolice.gov.in — CB-CID Mumbai Anti-Extortion Cell
  9.  dcbcid.cawc-mum@mahapolice.gov.in — DCB-CID Mumbai
  10. adg.cidcrime.pune@mahapolice.gov.in — ADG CID Crime Maharashtra
  11. cp.mum.addcp.sbcid@mahapolice.gov.in — Addl. CP SB-CID Mumbai
  12. hozmum@cbi.gov.in                — CBI Mumbai (Head of Zone)
  13. hobeomum@cbi.gov.in              — CBI Mumbai (Branch EO)
  14. info@pressdetective.com          — PressDetective

──────────────────────────────────────────────
PRIOR ACTIONS TAKEN IN THIS CASE
──────────────────────────────────────────────

  - 3,031 emails sent to Mumbai/Maharashtra journalists, press & government contacts
    on 9 June 2026 via sujata.shirasi@pressdetective.com (ZeptoMail, 0 errors)
  - Online reputation audit completed: Google first-page exposure documented
  - 4 legal deliverables prepared: Criminal Revision, s.482 Quashing Petition,
    Plan of Action, Change.org Campaign (all filed in clients/tarun-thadani/)
  - Defamation notice issued to Times of India (29 Jul 2025)
  - ACB complaint prepared and filed re alteration of original complaint

──────────────────────────────────────────────
NEXT STEPS
──────────────────────────────────────────────

  - Monitor for response from Saraf within 7 days (by 16 June 2026)
  - If no response: proceed with criminal complaints (s.182/192/211 IPC)
  - Follow up with ACB and CB-CID Anti-Extortion Cell
  - Continue press and media outreach
  - Prepare High Court petition if required

──────────────────────────────────────────────

Adv. Sujata Shirasi | Investigating False FIR 0654/2022 | Acting for Tarun Thadani & Ali Asgar Merchant
sujata.shirasi@pressdetective.com | +91 93216 13691
PressDetective | info@pressdetective.com
"""


def send(to_list, cc_list, subject, body, label=''):
    m = EmailMessage()
    m['From']    = f'{FROM_NAME} <{FROM_ADDR}>'
    m['To']      = ', '.join(to_list)
    m['Cc']      = ', '.join(cc_list)
    m['Subject'] = subject
    m.set_content(body)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP(HOST, PORT, timeout=60) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.ehlo()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(m)
    print(f'  [{label}] SENT')


def main():
    # Step 1 — send notice to Saraf + all officials on CC
    print(f'Step 1: Sending notice to {TO_ADDR} with {len(CC_LIST)} officials on CC ...')
    try:
        send(to_list=[f'{TO_NAME} <{TO_ADDR}>'],
             cc_list=CC_LIST,
             subject=SUBJECT,
             body=BODY,
             label='notice')
    except Exception as e:
        print(f'  ERROR: {e}'); sys.exit(1)

    time.sleep(3)

    # Step 2 — send action report to Aliasgar + info@
    print(f'\nStep 2: Sending action report to {", ".join(REPORT_TO)} ...')
    for addr in REPORT_TO:
        try:
            send(to_list=[addr],
                 cc_list=['info@pressdetective.com'] if addr != 'info@pressdetective.com' else [],
                 subject=REPORT_SUBJECT,
                 body=REPORT_BODY,
                 label=f'report->{addr}')
            time.sleep(2)
        except Exception as e:
            print(f'  ERROR sending to {addr}: {e}')

    print('\nAll done.')
    print(f'  Notice to Abhishek Saraf: {TO_ADDR}')
    print(f'  CC ({len(CC_LIST)} addresses): ACB, CID, Dadar PS, Azad Maidan PS, Anti-Extortion Cell, CBI, Aliasgar, info@')
    print(f'  Report sent to: {", ".join(REPORT_TO)}')


if __name__ == '__main__':
    main()
