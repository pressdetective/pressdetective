#!/usr/bin/env python3
"""
send_santosh_press_story.py -- 20 June 2026
Wider press push + police/ACB full-investigation request.

User decisions (this round):
  - Saraf background  = POLICE DUE-DILIGENCE REQUEST ONLY (cite public Martin Burn
                        CS 313/2012; full identity+address to police; NO underworld
                        claim anywhere; NOT to press).
  - Scope             = WIDER Mumbai press (NEW contacts only) + police/ACB.
  - Sender            = single authenticated santosh@pressdetective.com (Postmark).

EXPLICITLY EXCLUDED (declined for legal/deliverability reasons):
  - Any "underworld / D.K. Rao" allegation about Saraf (unsubstantiated; defamation).
  - Multi-identity Proton sending (protonmail.com/proton.me/pm.me) -- no creds,
    Bridge not running, and rotating senders harms deliverability.

EMAIL 1 (press): documented-facts narrative + request for full investigation.
                 To 404 NEW Mumbai crime/legal press (BCC batches). Privacy-minimised:
                 names Saraf as complainant but no personal phone/home address.
EMAIL 2 (auth):  full-investigation + antecedent due-diligence request to core
                 police/ACB authorities, WITH Saraf's full identity + address +
                 public Martin Burn reference.

Saraf is NEVER a recipient (runtime assert). MP4 never attached. Sub-judice safe.
"""
import smtplib, ssl, json, sys, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

import sys as _pg_sys, pathlib as _pg_pl
_pg_sys.path.insert(0, str(_pg_pl.Path(__file__).resolve().parents[2]))
import lib.presend_guard  # enforce no-contact + suppression + live verification on every send

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT  = Path(r'C:\dev\pressdetective')
CREDS = json.loads((ROOT / '.creds/proton_accounts.json').read_text(encoding='utf-8-sig'))
FROM     = CREDS['accounts']['santosh']['address']
TOKEN    = CREDS['accounts']['santosh']['token']
PROTON_H = CREDS['smtp_remote']['host']; PROTON_P = CREDS['smtp_remote']['port']

TODAY = '20 June 2026'
FORBIDDEN = {'abhishek_saraf78@yahoo.com'}

INFO       = 'info@pressdetective.com'
ACB        = 'acbwebmail@mahapolice.gov.in'
AEC        = 'cbcidmumaecell@mahapolice.gov.in'
JTCP_CRIME = 'cp.mumbai.jtcp.crime@mahapolice.gov.in'
DGP        = 'dgp.mah@mahapolice.gov.in'
EOW_ADG    = 'adg.eowms@mahapolice.gov.in'

NEW_PRESS = json.loads((ROOT / 'clients/tarun-thadani/_new_press_list.json').read_text())

def assert_clean(addrs, where):
    bad = [a for a in addrs if a.lower() in FORBIDDEN or 'saraf' in a.lower()]
    if bad:
        print(f'FATAL: forbidden recipient {bad} in {where}'); sys.exit(2)
assert_clean(NEW_PRESS, 'NEW_PRESS')

SIG_NAME = 'Santosh Sakpal, Independent Investigator'

def smtp_send(rcpts, msg_obj, label):
    ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    try:
        with smtplib.SMTP(PROTON_H, PROTON_P, timeout=25) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo(); s.login(FROM, TOKEN)
            s.sendmail(FROM, rcpts, msg_obj.as_string())
        print(f'  [{label}] OK via Proton ({len(rcpts)} rcpt)'); return True
    except Exception as e:
        print(f'  [{label}] FAILED: {str(e)[:80]}'); return False

def build(to_list, cc_list, subject, body, bcc_list=None, unsub=False):
    msg = MIMEMultipart('alternative')
    msg['From'] = f'{SIG_NAME} <{FROM}>'
    msg['To'] = ', '.join(to_list)
    if cc_list: msg['Cc'] = ', '.join(cc_list)
    msg['Subject'] = subject
    msg['Reply-To'] = FROM
    msg['X-PM-Message-Stream'] = 'outbound'
    if unsub:
        msg['List-Unsubscribe'] = '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    rcpts = list(to_list) + list(cc_list or []) + list(bcc_list or [])
    assert_clean(rcpts, subject[:30])
    return msg, rcpts

# ===========================================================================
# EMAIL 1 -- PRESS STORY (documented facts; request full investigation)
# ===========================================================================
P_TO = [FROM]; P_CC = [INFO]
P_SUBJ = ('PRESS NOTE / REQUEST FOR INVESTIGATION -- How a Bailable Slap Became a '
          'Non-Bailable "Rs 1 Crore Extortion": The FIR 0654/2022 Story | '
          'Dharte.com Founder Tarun Thadani Trapped Though Not Present | '
          'Santosh Sakpal, Investigator | ' + TODAY)
P_BODY = f"""\
PRESS NOTE -- FOR CRIME & LEGAL DESKS
Issued by : Santosh Sakpal, Independent Investigator
Contact   : +91 82689 17276 | santoshsakpal03@gmail.com
Date      : {TODAY}

HOW A MINOR SLAP WAS TURNED INTO A NON-BAILABLE "Rs 1 CRORE EXTORTION" --
AND HOW TWO MEN, ONE OF THEM NOT EVEN PRESENT, WERE TRAPPED IN IT

This note sets out a documented timeline and asks the press, the police and the
Anti-Corruption Bureau to examine how FIR No. 0654/2022 (Dadar PS / CB-CID Anti-
Extortion Cell) came to exist. Every factual assertion below is drawn from the
record; the sharper characterisations are the contentions of the defence and the
subject of complaints now before the ACB and the Mumbai police.

THE STORY THE RECORD TELLS
--------------------------
> On or about 2 June 2022, at a Worli restaurant, Mr. Abhishek Badriprasad Saraf
  was slapped by Mr. Ali Asgar Merchant. At its very highest, a slap is IPC s.323
  -- bailable and compoundable.

> On 4 June 2022, Mr. Saraf himself lodged an online complaint (ID 23244/2022).
  In his own words at the time, it alleged ONLY the slap. There was NO mention of
  extortion, NO demand for Rs 1 crore, and NO mention of Mr. Tarun Thadani --
  founder of the wellness marketplace Dharte (dharte.com).

> The regular police did not register a serious case on so minor a matter.

> Then, roughly two months later, the story changed completely. FIR No. 0654/2022
  was registered (Dadar PS, 13 August 2022) and routed through the CB-CID Anti-
  Extortion Cell -- now alleging, for the first time, a Rs 1 crore "extortion"
  and naming Mr. Thadani, who was NOT present at the venue at all.

> No accused was summoned or examined before the FIR was registered. No call
  records, bank records or CCTV -- none of which support any extortion demand --
  were verified.

THE QUESTION THIS RAISES
------------------------
How does a complaint that, in the complainant's own first telling, described only
a slap become -- two months later, with no new verified evidence -- a non-bailable
extortion case carrying up to ten years, sweeping in a man who was never there?

The defence contends, and complaints now before the Anti-Corruption Bureau allege,
that after failing to obtain action on a minor matter, the complainant advanced a
false and exaggerated "extortion" narrative that misled the Anti-Extortion Cell
into registering a grave non-bailable case -- trapping both Mr. Merchant and an
absent Mr. Thadani. A recent Times of India report has carried the case one-
sidedly, omitting every one of the exculpatory facts above and without seeking
the accused's version.

WHAT IS BEING ASKED
-------------------
A FULL INVESTIGATION: into how a no-extortion complaint became a non-bailable
extortion FIR two months later, and into the circumstances of its registration.
Formal complaints to this effect are before the ACB and the Mumbai police.

OF JOURNALISTS: please seek the defence's version before publishing -- contact PressDetective at +91 82689 17276 -- and examine the documented timeline above. Mr. Thadani
(Dharte.com) was not present and was not named in the complainant's own original
complaint.

This note is sub-judice compliant and prejudges nothing; the authorities named are
the bodies competent to establish the truth.

-- {SIG_NAME} (+91 82689 17276 | santoshsakpal03@gmail.com)
   Issued with the assistance of PressDetective | info@pressdetective.com
   To unsubscribe: email info@pressdetective.com, subject UNSUBSCRIBE.
"""

# ===========================================================================
# EMAIL 2 -- POLICE/ACB: FULL INVESTIGATION + ANTECEDENT DUE DILIGENCE
# ===========================================================================
A_TO = [ACB]; A_CC = [AEC, JTCP_CRIME, DGP, EOW_ADG, INFO]
A_SUBJ = ('REQUEST FOR FULL INVESTIGATION + DUE DILIGENCE ON COMPLAINANT -- '
          'FIR No. 0654/2022 | Fabricated Extortion via Anti-Extortion Cell | '
          'Complainant Antecedents to be Verified | Santosh Sakpal, Investigator | '
          + TODAY)
A_BODY = f"""\
To,   The Director General, Anti-Corruption Bureau of Maharashtra
CC:   CB-CID Anti-Extortion Cell; Jt. CP (Crime), Mumbai; DGP Maharashtra;
      ADG Economic Offences Wing; PressDetective (for record)

Date: {TODAY}

Subject: Request for a full investigation into FIR No. 0654/2022 and for
         due-diligence verification of the antecedents of the complainant.

Respected Sir/Madam,

Further to my complaint of even date regarding the manner of registration of FIR
No. 0654/2022, I respectfully request a FULL INVESTIGATION into how a complaint
that originally alleged only a slap (complainant's own online complaint ID
23244/2022, 4 June 2022 -- no extortion, no Rs 1 crore, no mention of Mr. Tarun
Thadani) was converted, some two months later, into a non-bailable Rs 1 crore
"extortion" FIR (Dadar PS, 13 August 2022) routed through the Anti-Extortion Cell,
without any accused being examined and without CDR/bank/CCTV verification.

DUE DILIGENCE ON THE COMPLAINANT
--------------------------------
So that the authorities may independently assess the complainant's credibility, I
provide his full identifying particulars and request that his antecedents be
verified by the appropriate agencies:

   Name    : Mr. Abhishek Badriprasad Saraf
   Phone   : +91 98201 80065
   Address : 3rd Floor, Esplanade House, 29, Hazarimal Somani Marg,
             Fort, Mumbai 400001

   Public-record matter for reference: Mr. Saraf is a party to civil proceedings
   before the Hon'ble Calcutta High Court (CS 313/2012, Martin Burn Limited).

I make no assertion beyond this public-record reference; I respectfully leave the
verification of his antecedents and any associations to the authorities, which are
the bodies empowered to conduct such due diligence lawfully.

PRAYER
------
(1) A full investigation into the registration and manufacture of FIR 0654/2022;
(2) due-diligence verification of the complainant's antecedents and credibility;
(3) such action as the law permits against any person -- complainant or public
    servant -- found to have abused the process.

This matter is sub-judice; nothing herein prejudges any pending proceeding, and it
is submitted solely to invite lawful inquiry. I am willing to depose and to furnish
the documents in my possession.

Yours faithfully,
{SIG_NAME}
Phone   : +91 82689 17276
Email   : santoshsakpal03@gmail.com
Address : B/6 Shimgyamanohar Apartments, Thane Belapur Road, Digha West,
          Navi Mumbai 400708
Date    : {TODAY}
(Submitted with the assistance of PressDetective | info@pressdetective.com)
"""

# ===========================================================================
# SEND
# ===========================================================================
def chunk(lst, n):
    for i in range(0, len(lst), n): yield lst[i:i+n]

print('=' * 70)
print('SANTOSH -- WIDER PRESS STORY + FULL-INVESTIGATION REQUEST')
print(f'FROM: {FROM}  |  NEW press: {len(NEW_PRESS)}  |  DATE: {TODAY}')
print('=' * 70)
results = {}

print('\n--- EMAIL 2: Police/ACB full-investigation + due diligence ---')
msg, rcpts = build(A_TO, A_CC, A_SUBJ, A_BODY)
results['Police/ACB investigation'] = 'SENT' if smtp_send(rcpts, msg, 'ACB') else 'FAILED'
time.sleep(3)

print(f'\n--- EMAIL 1: Press story to {len(NEW_PRESS)} NEW Mumbai press ---')
okP=0; nP=0
for i, batch in enumerate(chunk(NEW_PRESS, 40), 1):
    nP+=1
    msg, rcpts = build(P_TO, P_CC, P_SUBJ, P_BODY, bcc_list=batch, unsub=True)
    if smtp_send(rcpts, msg, f'PRESS batch {i} ({len(batch)})'): okP+=1
    time.sleep(3)
results[f'Press ({len(NEW_PRESS)} new, {okP}/{nP} batches)'] = 'SENT' if okP==nP else f'PARTIAL {okP}/{nP}'

print('\n' + '=' * 70)
print('RESULTS:')
for k,v in results.items(): print(f'  {v:>12}  --  {k}')
print('\nNOTE: SMTP OK != delivered. Watch info@ for bounce DSNs.')
print('Done.')
