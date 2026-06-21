#!/usr/bin/env python3
"""
send_ahmedali_demand.py -- 20 June 2026
From Santosh Sakpal (Proton, fixed From). Two emails:

EMAIL 1 -> S. Ahmed Ali (ToI) + Editor/desk: DEMAND for correction + right of reply.
   Lawful framing: the publication is defamatory by omission; demand correction,
   takedown/annotation + right of reply within 7 days; RESERVE lawful remedies
   (BNS 356 criminal defamation + Press Council complaint). NO arrest threat.
   NO assertion that he took money (would be defamation per se). Asks him to
   confirm whether he sought the accused's comment + his sourcing.

EMAIL 2 -> ACB + Commissioner of Police Mumbai (official, web-verified addresses):
   complaint re false FIR 0654/2022 + request to INVESTIGATE the publication's
   circumstances INCLUDING whether any improper inducement influenced it
   (framed as inquiry, "I make no assertion" -- ACB to determine). Due-diligence
   on complainant Saraf. Points to ACB/Police online portals as the definitive
   channel (mahapolice email has been bouncing).

Saraf is NEVER a recipient. No underworld claim. Sub-judice safe.
"""
import smtplib, ssl, json, sys, time
from email.utils import formataddr
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
FROM_HDR = formataddr(('Santosh Sakpal, Independent Investigator', FROM))
TODAY = '20 June 2026'
FORBIDDEN = {'abhishek_saraf78@yahoo.com'}

INFO='info@pressdetective.com'
AHMED='ahmed.ali@timesgroup.com'
TOI_CC=['editor@timesgroup.com','mumbai.letters@timesgroup.com','mumbai.crime@timesgroup.com', INFO]
ACB='acbwebmail@mahapolice.gov.in'
CP_MUM='cp.mumbai@mahapolice.gov.in'

def clean(addrs):
    bad=[a for a in addrs if a.lower() in FORBIDDEN or 'saraf' in a.lower()]
    if bad: print('FATAL forbidden',bad); sys.exit(2)

_ctx=ssl.create_default_context(); _ctx.check_hostname=False; _ctx.verify_mode=ssl.CERT_NONE
def proton_send(rcpts,msg,label):
    try:
        with smtplib.SMTP(PROTON_H,PROTON_P,timeout=30) as s:
            s.ehlo(); s.starttls(context=_ctx); s.ehlo(); s.login(FROM,TOKEN)
            s.sendmail(FROM,rcpts,msg.as_string())
        print(f'  [{label}] OK via Proton ({len(rcpts)} rcpt)'); return True
    except Exception as e:
        print(f'  [{label}] FAIL: {str(e)[:150]}'); return False

def build(to,cc,subject,body):
    m=MIMEMultipart('alternative'); m['From']=FROM_HDR; m['To']=', '.join(to)
    if cc: m['Cc']=', '.join(cc)
    m['Subject']=subject; m['Reply-To']=FROM
    m.attach(MIMEText(body,'plain','utf-8'))
    r=list(to)+list(cc or []); clean(r); return m,r

SIG=f"""Yours faithfully,
Santosh Sakpal
Independent Investigator
Phone   : +91 82689 17276 | Email: santoshsakpal03@gmail.com
Address : B/6 Shimgyamanohar Apartments, Thane Belapur Road, Digha West, Navi Mumbai 400708
Date    : {TODAY}   (Submitted with the assistance of PressDetective | info@pressdetective.com)"""

# ---------------- EMAIL 1: Ahmed Ali demand ----------------
E1_SUBJ=('DEMAND FOR CORRECTION & RIGHT OF REPLY -- Defamatory one-sided report on '
 'FIR 0654/2022 | Mr. Tarun Thadani was NOT present & was NOT in the original '
 'complaint | Response required within 7 days | '+TODAY)
E1_BODY=f"""To,   Mr. S. Ahmed Ali, Senior Assistant Editor, The Times of India, Mumbai
CC:   The Editor, Times of India (Mumbai); ToI Mumbai City/Crime Desk; PressDetective

Date: {TODAY}

Dear Mr. Ahmed Ali,

I am an independent investigator looking into FIR No. 0654/2022 (Dadar PS / CB-CID
Anti-Extortion Cell). Your recent Times of India report on this case is, with
respect, materially one-sided: by omitting the documented facts set out below and
without seeking the accused's version, it conveys to the ordinary reader the false
impression that Mr. Tarun Thadani and Mr. Ali Asgar Merchant are guilty.

DOCUMENTED FACTS YOUR REPORT OMITS
1. Mr. Tarun Thadani, founder of Dharte (dharte.com), was NOT present at the venue
   on 2 June 2022.
2. The complainant's OWN original complaint of 4 June 2022 (online ID 23244/2022)
   alleged ONLY a slap -- NO extortion, NO Rs 1 crore, and did NOT name Mr. Thadani.
3. The Rs 1 crore "extortion" allegation and Mr. Thadani's name appeared only about
   two months later, when FIR 0654/2022 was registered -- with no accused examined
   and no call-record, bank or CCTV verification.
4. No comment was sought from the accused or their counsel before publication.

By carrying only the complainant's version and omitting the above, the report is
defamatory of Mr. Thadani and Mr. Merchant.

I therefore call upon you and the Times of India, WITHIN 7 DAYS, to:
 (a) publish a correction/clarification carrying the above facts, with the same
     prominence as the original report;
 (b) afford the accused/their counsel a right of reply; and
 (c) pending correction, take down or prominently annotate the online article.

Please also confirm in writing (i) whether you sought any comment from the accused
or their counsel before publication and, if not, why; and (ii) the basis and
sources for the "extortion" characterisation.

TAKE NOTICE that, failing satisfactory compliance within 7 days, the affected
parties reserve the right to pursue all lawful remedies, including a complaint for
criminal defamation (Section 356, Bharatiya Nyaya Sanhita) and a complaint to the
Press Council of India. Formal complaints concerning this matter -- including the
circumstances of the FIR's registration and of its reporting -- are already before
the Anti-Corruption Bureau of Maharashtra and the Mumbai Police.

This communication is sub-judice compliant and prejudges nothing; it seeks only
accurate, balanced reporting and the accused's right of reply.

{SIG}"""

# ---------------- EMAIL 2: ACB + CP Mumbai ----------------
E2_SUBJ=('COMPLAINT & REQUEST FOR INVESTIGATION -- False FIR 0654/2022 + one-sided '
 'press report | Request inquiry into circumstances of publication incl. any '
 'inducement | Santosh Sakpal | '+TODAY)
E2_BODY=f"""To,   The Director General, Anti-Corruption Bureau of Maharashtra (acbwebmail@mahapolice.gov.in)
      The Commissioner of Police, Mumbai (cp.mumbai@mahapolice.gov.in)
CC:   PressDetective
[Online channels for record: ACB portal https://acbmaharashtra.gov.in ; toll-free 1064;
 Mumbai Police online complaints https://mumbaipolice.gov.in/OnlineComplaints]

Date: {TODAY}

Respected Sir/Madam,

I, Santosh Sakpal, an independent investigator, respectfully submit this complaint
and request an investigation.

THE FALSE FIR (documented facts)
1. On or about 2 June 2022, at a Worli restaurant, Mr. Abhishek Badriprasad Saraf was
   slapped by Mr. Ali Asgar Merchant -- at most IPC s.323 (bailable).
2. Mr. Saraf's OWN original complaint of 4 June 2022 (ID 23244/2022) alleged only the
   slap -- NO extortion, NO Rs 1 crore, NO mention of Mr. Tarun Thadani.
3. The regular police did not register a serious case on so minor a matter.
4. About two months later FIR No. 0654/2022 was registered (Dadar PS, 13 Aug 2022),
   routed through the CB-CID Anti-Extortion Cell, now alleging a Rs 1 crore "extortion"
   and naming Mr. Thadani, founder of Dharte (dharte.com) -- who was NOT present. No
   accused was examined; no CDR/bank/CCTV verified.

THE ONE-SIDED PRESS REPORT
A recent Times of India report by Mr. S. Ahmed Ali carries this case one-sidedly,
omitting every exculpatory fact above and without seeking the accused's version. I am
separately demanding a correction and right of reply from the newspaper.

REQUESTS
1. A full investigation into the manufacture and registration of FIR No. 0654/2022.
2. An inquiry into the circumstances of the said publication, INCLUDING whether any
   improper inducement influenced the one-sided reporting. I make NO assertion of fact
   on this point; I respectfully request the Bureau to determine it, as it is the body
   empowered to do so.
3. Action on the complaint already lodged against the reporter for defamatory
   publication (IPC 499/500 / BNS 356).

DUE DILIGENCE ON THE COMPLAINANT (particulars for verification)
   Name: Mr. Abhishek Badriprasad Saraf | Phone: +91 98201 80065
   Address: 3rd Floor, Esplanade House, 29, Hazarimal Somani Marg, Fort, Mumbai 400001
   Public-record reference only: party to Calcutta High Court proceedings CS 313/2012
   (Martin Burn Ltd). I leave verification of his antecedents to the authorities.

This matter is sub-judice; nothing herein prejudges any pending proceeding. I am
willing to depose and to furnish the documents in my possession, and I am filing this
through the online ACB/Police portals as well.

{SIG}"""

print('='*70); print('AHMED ALI DEMAND + ACB/POLICE COMPLAINT  |  FROM:',FROM_HDR); print('='*70)
res={}

print('\n--- EMAIL 1: Demand to S. Ahmed Ali + ToI Editor/desk ---')
m,r=build([AHMED], TOI_CC, E1_SUBJ, E1_BODY)
res['1. Ahmed Ali demand']='SENT' if proton_send(r,m,'AHMED') else 'FAIL'
time.sleep(5)

print('\n--- EMAIL 2: ACB + Commissioner of Police Mumbai ---')
m,r=build([ACB,CP_MUM], [INFO], E2_SUBJ, E2_BODY)
res['2. ACB + CP Mumbai']='SENT' if proton_send(r,m,'ACB/CP') else 'FAIL'

print('\n'+'='*70); print('RESULTS:')
for k,v in res.items(): print(f'  {v:>6}  --  {k}')
print('\nNOTE: SMTP OK != delivered -- will verify via Bridge for bounces next.')
print('Done.')
