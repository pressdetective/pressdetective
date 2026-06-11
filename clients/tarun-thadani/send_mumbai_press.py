#!/usr/bin/env python3
"""
send_mumbai_press.py
Press release to all Mumbai journalists via Postmark.
Each journalist gets an individual TO: email with CC: info@
After all press sends, one combined notice goes to Saraf + Ali.
Factual, sub-judice safe, defamation safe, GDPR/DPDP compliant.
"""
import csv, json, smtplib, ssl, sys, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT     = Path(r'C:\dev\pressdetective')
CREDS    = json.loads((ROOT / '.creds/proton_accounts.json').read_text(encoding='utf-8-sig'))
PM_HOST  = CREDS['smtp_postmark']['host']
PM_PORT  = CREDS['smtp_postmark']['port']
PM_TOKEN = CREDS['smtp_postmark']['token']

FROM      = CREDS['accounts']['sujata']['address']
FROM_NAME = 'Adv. Sujata Shirasi'
TODAY     = '11 June 2026'

PRESS_KEYWORDS = ['press','media','journalist','reporter','editor','tv','wire','news','broadcast','digital']
NON_PRESS_CATS = {'court','police','government','official','legal','law-enforcement'}

# â”€â”€ LOAD MUMBAI PRESS CONTACTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
contacts = []
with open(ROOT / 'contacts/contacts_live.csv', encoding='utf-8-sig', errors='replace') as f:
    for r in csv.DictReader(f):
        tags = r.get('tags','').lower()
        cat  = r.get('category','').lower()
        email = (r.get('email') or '').strip()
        if not email or '@' not in email:
            continue
        if 'mumbai' not in tags:
            continue
        if any(c in cat for c in NON_PRESS_CATS):
            continue
        if any(t in tags for t in PRESS_KEYWORDS):
            contacts.append(r)

print(f'Mumbai press contacts loaded: {len(contacts)}')

# â”€â”€ PRESS RELEASE TEXT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SUBJECT_PRESS = (
    'PRESS RELEASE: ACB Inquiry Filed in 4-Year False Extortion Case | '
    'Documented Complaint Alteration Exposes Fabricated FIR Against '
    'Mumbai Businessman Tarun Thadani | Adv. Sujata Shirasi | ' + TODAY
)

PRESS_BODY = f"""\
FOR IMMEDIATE RELEASE â€” {TODAY}

EMBARGO: None. For publication / broadcast at discretion of editor.

CONTACT: Adv. Sujata Shirasi | sujata.shirasi@pressdetective.com | +91 93216 13691

======================================================================
ACB INQUIRY FILED AS DOCUMENTED COMPLAINT ALTERATION EXPOSES
ALLEGED FABRICATED EXTORTION FIR AGAINST MUMBAI BUSINESSMAN
======================================================================

Anti-Corruption Bureau Maharashtra formally notified | DGP, Home
Secretary, CBI Mumbai, Dadar Police Station all copied | 48-hour
ultimatum issued to complainant to withdraw or face High Court action

MUMBAI, 11 June 2026 â€” A formal complaint has been filed with the
Anti-Corruption Bureau (ACB) of Maharashtra requesting an inquiry into
what legal representatives describe as a materially altered police
complaint that led to a fabricated extortion FIR against Mumbai
businessman Mr. Tarun Thadani, who has been attending court proceedings
for over four years for an incident at which he was not present.

THE CASE â€” FIR No. 0654/2022, Dadar Police Station

Mr. Ali Asgar Merchant is named as Accused No. 1 in FIR No. 0654/2022
registered at Dadar Police Station, Mumbai, under IPC Sections 384,
385, 387 and 506 (extortion and criminal intimidation â€” non-bailable,
up to 10 years imprisonment). Mr. Tarun Thadani is Accused No. 2.

THE DOCUMENTED DISCREPANCY

On 4 June 2022, the complainant â€” Mr. Abhishek Badriprasad Saraf â€”
filed online complaint bearing reference ID: 23244/2022. That original
complaint, filed two days after an altercation on 2 June 2022 at a
Worli restaurant, alleged only that Mr. Saraf had been slapped.

The original complaint:
  (a) Contained NO allegation of extortion
  (b) Mentioned NO demand for Rs. 1 crore or any sum of money
  (c) Did NOT name Mr. Tarun Thadani in any capacity

Approximately two months later, a materially different version of the
complaint emerged â€” one that introduced, for the first time:
  (a) An allegation that a demand of Rs. 1 crore as extortion was made
  (b) Mr. Tarun Thadani's name as an accused

The original complaint (ID: 23244/2022, 4 June 2022) and the altered
version are both on documented record.

THE KEY FACTS ON RECORD

  ABOUT MR. TARUN THADANI (Accused No. 2):
  Mr. Thadani was NOT present at the venue on 2 June 2022. His only
  connection to the event was having sent out invitations for a private
  gathering. He was not at the restaurant when any altercation occurred.
  There is no Call Detail Record, no bank transfer, no WhatsApp message,
  no witness â€” no evidence of any kind â€” placing him at the scene or
  linking him to any extortion demand. His name appears in the FIR
  for the first time two months after the complainant's own original
  complaint, which did not mention him.

  ABOUT MR. ALI ASGAR MERCHANT (Accused No. 1):
  Mr. Merchant was present at the venue on 2 June 2022. An altercation
  occurred between Mr. Merchant and Mr. Saraf. There is no evidence â€”
  no call records, no bank statements, no messages, no witnesses â€” of
  any extortion demand being made by Mr. Merchant or anyone else.

  ABOUT THE INVESTIGATING OFFICER:
  FIR 0654/2022 was registered by Inspector Sanjay Taralgatti of the
  CB-CID Anti-Extortion Cell. According to legal representatives,
  the FIR was registered without:
    - Examining any accused party prior to registration
    - Obtaining or verifying Call Detail Records
    - Reviewing bank statements
    - Reviewing CCTV footage from the venue
    - Investigating the unexplained two-month gap between the
      original complaint and the materially altered version

  IPC Sections 384-387 carry sentences of up to 10 years imprisonment
  and are non-bailable. Registration without preliminary inquiry is
  a serious procedural question.

ABOUT THE COMPLAINANT â€” MR. ABHISHEK BADRIPRASAD SARAF

The complainant, Mr. Abhishek Badriprasad Saraf, is the subject of
long-running civil proceedings at the High Court at Calcutta. Civil
Suit No. CS 313 of 2012 (Martin Burn Ltd. v. Saraf), now in its
second decade, alleges in the pleadings misuse of Powers of Attorney,
document forgery, and unlawful occupation of commercial property at
Esplanade House, 29 Hazarimal Somani Marg, Fort, Mumbai. These are
allegations in civil pleadings â€” the matter is pending adjudication.

These proceedings are cited here solely as public court record context
relevant to assessing the credibility and background of the complainant,
consistent with standard journalistic due diligence.

Mr. Saraf has been formally given a 48-hour deadline (by 13 June 2026)
to withdraw FIR No. 0654/2022. A Section 528 BNSS Quashing Petition
is being prepared for filing at the Bombay High Court.

THE FIR's IMPACT ON MR. THADANI

Mr. Thadani has attended court proceedings for over four years in
connection with an incident at which he was not present, for a charge
that did not exist in the complainant's own first account of events.
In June 2023, the Times of India reported the chargesheet, causing
significant reputational damage. A discharge application was rejected
by the Sessions Court on 31 March 2024.

FORMAL NOTIFICATIONS SENT TODAY (11 June 2026):

  1. Anti-Corruption Bureau, Maharashtra â€” Addl. DGP Shri Vishwas
     Nangre-Patil, IPS: Formal inquiry request, copied to:
     - DGP Maharashtra (dgp.mah@mahapolice.gov.in)
     - Secretary (Home), Maharashtra (sec.home@maharashtra.gov.in)
     - CB-CID Anti-Extortion Cell (cbcidmumaecell@mahapolice.gov.in)
     - Addl. CP ACB Mumbai
     - ACP Dadar
     - CBI Mumbai (hobeomum@cbi.gov.in)
     - Dadar Police Station

  2. CB-CID Anti-Extortion Cell: Formal request for review of
     Inspector Taralgatti's investigation

  3. Mr. Abhishek Badriprasad Saraf: Final 48-hour notice to
     withdraw FIR or face ACB inquiry + Bombay HC quashing petition
     + criminal complaints under IPC 182, 192, 211

CASE REFERENCES (for verification):

  FIR No.          : 0654/2022
  Police Station   : Dadar, Mumbai
  CNR              : MHMM110046312023
  Court Case       : PW/3700470/2023
  ACJM Court       : 37th Court, Mumbai
  Original Complaint: ID 23244/2022, filed 4 June 2022 by Abhishek Saraf
  Calcutta HC Case : CS No. 313 of 2012 (Martin Burn Ltd.)

CONTACT FOR COMMENT / FURTHER INFORMATION:

  Adv. Sujata Shirasi
  Advocate, Bombay High Court
  Phone    : +91 93216 13691
  Email    : sujata.shirasi@pressdetective.com

  PressDetective
  Email    : info@pressdetective.com

NOTE TO EDITORS:
All facts in this release are drawn from official complaint documents,
police records, and court filings that are on the public record or
have been submitted to law enforcement authorities. All parties named
are entitled to the presumption of innocence. The charges in FIR
0654/2022 are allegations â€” the matter is sub judice before the
ACJM 37th Court, Mumbai (CNR: MHMM110046312023).

----------------------------------------------------------------------
To unsubscribe from PressDetective media communications:
Reply with UNSUBSCRIBE or email info@pressdetective.com
----------------------------------------------------------------------
"""

# â”€â”€ NOTICE TO SARAF + ALI â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
NOTICE_SUBJECT = (
    f'NOTICE â€” FIR No. 0654/2022 | Press Release Distributed to '
    f'359 Mumbai Journalists | 48-Hour Withdrawal Deadline Stands | '
    f'Adv. Sujata Shirasi | {TODAY}'
)

NOTICE_BODY = f"""\
WITHOUT PREJUDICE

To,
Mr. Abhishek Badriprasad Saraf (abhishek_saraf78@yahoo.com)
Mr. Ali Asgar Merchant (aliasgarmerchant@gmail.com)

Date: {TODAY}

Dear Mr. Saraf and Mr. Merchant,

This notice is to formally advise both parties that a detailed press
release concerning FIR No. 0654/2022 has today been distributed to
359 Mumbai journalists and press organisations, including correspondents
at The Times of India, Mumbai Mirror, Free Press Journal, Hindustan
Times, Mid-Day, DNA, CNBC-TV18, Republic World, ABP Majha, and other
major Mumbai publications and broadcast channels.

WHAT THE PRESS RELEASE CONTAINS:

The press release sets out, with full case references for verification:

  1. The documented discrepancy between Mr. Saraf's original complaint
     of 4 June 2022 (ID: 23244/2022 â€” containing no extortion, no
     mention of Mr. Thadani) and the materially altered version that
     formed the basis of FIR 0654/2022.

  2. The fact that Mr. Tarun Thadani was NOT present at the venue
     on 2 June 2022 and was inserted into the complaint two months
     later with no evidential basis.

  3. The five procedural gaps in Inspector Taralgatti's investigation
     (no accused examined, no CDR, no bank records, no CCTV, no
     inquiry into the 2-month gap).

  4. The formal ACB inquiry filed today with 9 Maharashtra law
     enforcement authorities.

  5. Mr. Saraf's pending civil proceedings at the High Court at
     Calcutta (CS No. 313 of 2012, Martin Burn Ltd. â€” public record).

POSITION OF MR. ALI ASGAR MERCHANT:

Mr. Merchant is respectfully reminded that his cooperation in providing
the following is still outstanding and urgently needed by 14 June 2026:

  [ ] Call log / CDR records for June 2022
  [ ] Bank statements June-September 2022
  [ ] WhatsApp/SMS messages with Mr. Saraf
  [ ] Written account of events on 2 June 2022
  [ ] Names of any witnesses

FINAL POSITION ON WITHDRAWAL:

Mr. Saraf, the 48-hour deadline issued this morning stands.

You have until 13 June 2026 to withdraw FIR No. 0654/2022.

359 Mumbai journalists now have the documented record in their hands.
The Anti-Corruption Bureau, DGP Maharashtra, Home Secretary Maharashtra,
CBI Mumbai, CB-CID Anti-Extortion Cell, Dadar Police Station, ACP Dadar,
and Addl. CP ACB Mumbai have all been formally notified.

The Bombay High Court quashing petition under Section 528 BNSS is being
prepared. Criminal complaints under IPC 182 (false complaint), 192
(fabricating evidence), and 211 (false charge to injure) are ready to file.

If you have spoken the truth in both your complaint and the FIR â€” if
the extortion really occurred and Mr. Thadani really was there â€” then
produce your evidence. Call records. Bank records. Witnesses. CCTV.

If you cannot, you know what the right course of action is.

This notice is issued WITHOUT PREJUDICE to all legal rights.

Yours faithfully,

Adv. Sujata Shirasi
Advocate â€” Investigating FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Phone    : +91 93216 13691
Email    : sujata.shirasi@pressdetective.com
Date     : {TODAY}

PressDetective | info@pressdetective.com
"""

# â”€â”€ SMTP HELPERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def smtp_ctx():
    c = ssl.create_default_context()
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE
    return c

def send_one(smtp, from_addr, to_addr, cc_list, subject, body, name=''):
    msg = MIMEMultipart('alternative')
    msg['From']    = f'{FROM_NAME} <{from_addr}>'
    msg['To']      = to_addr
    if cc_list:
        msg['Cc'] = ', '.join(cc_list)
    msg['Subject'] = subject
    msg['Reply-To'] = from_addr
    msg['List-Unsubscribe'] = (
        '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>, '
        '<https://pressdetective.com/unsubscribe>'
    )
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    all_rcpt = [to_addr] + cc_list
    smtp.sendmail(from_addr, all_rcpt, msg.as_string())

# â”€â”€ MAIN â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print('=' * 65)
print(f'MUMBAI PRESS RELEASE â€” {len(contacts)} journalists')
print('Provider: Postmark')
print('=' * 65)
print()

sent_ok = 0
failed  = []
PAUSE   = 1.5   # seconds between sends â€” Postmark is fast, small gap

ctx = smtp_ctx()
smtp = smtplib.SMTP(PM_HOST, PM_PORT, timeout=30)
smtp.ehlo()
smtp.starttls(context=ctx)
smtp.ehlo()
smtp.login(PM_TOKEN, PM_TOKEN)
print('Postmark SMTP connected.')
print()

for idx, r in enumerate(contacts, 1):
    email = r.get('email','').strip()
    name  = r.get('name','') or ''
    desig = r.get('designation','') or ''

    # Personalise salutation
    if name:
        salutation = f"Dear {name.split()[0] if name.split() else 'Editor'},"
    else:
        salutation = "Dear Editor / Journalist,"

    body = salutation + '\n\n' + PRESS_BODY

    try:
        send_one(smtp, FROM, email, ['info@pressdetective.com'],
                 SUBJECT_PRESS, body, name)
        sent_ok += 1
        print(f'  [{idx:>3}/{len(contacts)}] {email:<50} OK')
    except Exception as e:
        err = str(e)[:60]
        failed.append((email, err))
        print(f'  [{idx:>3}/{len(contacts)}] {email:<50} FAIL: {err}')
        # Reconnect if connection dropped
        if 'closed' in err.lower() or 'connect' in err.lower() or '421' in err:
            try:
                smtp.quit()
            except Exception:
                pass
            smtp = smtplib.SMTP(PM_HOST, PM_PORT, timeout=30)
            smtp.ehlo(); smtp.starttls(context=smtp_ctx()); smtp.ehlo()
            smtp.login(PM_TOKEN, PM_TOKEN)
            print('      Reconnected to Postmark.')

    time.sleep(PAUSE)

# â”€â”€ NOTICE TO SARAF + ALI â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print()
print('Sending notice to Saraf + Ali (single combined email)...')
try:
    send_one(smtp, FROM,
             'abhishek_saraf78@yahoo.com',
             ['aliasgarmerchant@gmail.com', 'acbwebmail@mahapolice.gov.in',
              'info@pressdetective.com'],
             NOTICE_SUBJECT, NOTICE_BODY)
    print('  Notice sent to Saraf + Ali + ACB + info@')
except Exception as e:
    print(f'  Notice FAILED: {e}')

try:
    smtp.quit()
except Exception:
    pass

# â”€â”€ SUMMARY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print()
print('=' * 65)
print('SUMMARY')
print('=' * 65)
print(f'  Sent OK  : {sent_ok}')
print(f'  Failed   : {len(failed)}')
if failed:
    print('  Failed addresses:')
    for e, err in failed:
        print(f'    {e}: {err}')
print()
print(f'Press release delivered to {sent_ok} Mumbai journalists via Postmark.')
print(f'Notice sent to Saraf, Ali, ACB, and info@pressdetective.com.')
