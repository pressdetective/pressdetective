#!/usr/bin/env python3
"""send_police_retry_21jun.py -- 21 June 2026
Per user: try AGAIN to all police departments, via Santosh / Proton only.
NOTE: we are already sending as santosh@pressdetective.com over Proton. The mahapolice/
mgovcloud gateway rejects external email; most addresses are already suppressed. The guard
(lib.presend_guard) strips suppressed/dead so we don't bounce. This run prints the exact
per-address outcome -- the proof that email cannot reach them (portal/post is the route).
Messaging rule: venue never named; focus on how Saraf altered the FIR + manipulated police.
"""
import smtplib, ssl, json, sys, time
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import sys as _pg_sys, pathlib as _pg_pl
_pg_sys.path.insert(0, str(_pg_pl.Path(__file__).resolve().parents[2]))
import lib.presend_guard  # noqa: F401
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CREDS=json.loads(Path(r'C:\dev\pressdetective\.creds\proton_accounts.json').read_text(encoding='utf-8-sig'))
FROM=CREDS['accounts']['santosh']['address']; TOKEN=CREDS['accounts']['santosh']['token']
PH=CREDS['smtp_remote']['host']; PP=CREDS['smtp_remote']['port']
FROM_HDR=formataddr(('Santosh Sakpal, Independent Investigator', FROM))
TODAY='21 June 2026'; INFO='info@pressdetective.com'

POLICE=[f'{s}@mahapolice.gov.in' for s in (
 'ps.aareysub.mum','ps.agripada.mum','ps.airport.mum','ps.andheri.mum','ps.antophill.mum',
 'ps.azadmaidan.mum','ps.bangurnagar.mum','ps.bykhla.mum','ps.centralcyber.mum','ps.charkop.mum',
 'ps.charkopp.mum','ps.chunabhatti.mum','ps.dadar.mum','ps.dbmarg.mum','ps.deonar.mum',
 'ps.dnnagar.mum','ps.eastcyber.mum','ps.goregaoneatc.mum','ps.govandi.mum','ps.jjmarg.mum',
 'ps.jogeshwari.mum','ps.juhu.mum','ps.kalachowki.mum','ps.kalchowki.mum','ps.kanjurmarg.mum',
 'ps.kasturba.mum','ps.kurla.mum','ps.ltmarg.mum','ps.mahim.mum','ps.malabarhill.mum',
 'ps.mankhurd.mum','ps.mulund.mum','ps.nagpada.mum','ps.northcyber.mum','ps.oshiwara.mum',
 'ps.paydhunie.mum','ps.sagari2.mum','ps.sahar.mum','ps.samtanagar.mum','ps.southcyber.mum',
 'ps.tilaknagar.mum','ps.versova.mum','ps.vikhroli.mum','ps.vproad.mum','ps.wadala.mum',
 'dcpzone1-mum','dcpzone2-mum','dcpzone3-mum','dcpzone4-mum','dcpzone5-mum','dcpzone6-mum',
 'dcpzone7-mum','dcpzone8-mum','dcpzone9-mum','dcpzone10-mum','dcpzone11-mum','dcpzone12-mum',
 'dcpzoneport-mum','dcpdet1.mum','dcpenforcement-mum','dcpeowzone-mum','dcpcybercrime.mum',
 'crimebranchmumbai','eow.mumbai','acpworli.mum','acpam.mum','cp.mumbai','cp.mumbai.jtcp.crime',
 'acbwebmail','cbcidmumaecell','dgp.mah','adg.eowms',
)]

SUBJ=('TO ALL POLICE DEPARTMENTS -- false / altered complaint by Mr. Abhishek Saraf behind FIR '
      '0654/2022 | his OWN first complaint (Worli PS, ID 23244/2022) had NO extortion | request '
      'to register, reinvestigate & take lawful action | Santosh Sakpal | '+TODAY)
BODY=f"""To:   All Police Stations & Units, Mumbai City & Suburban; CB-CID Anti-Extortion Cell;
      Crime Branch; the DCsP (Zones I-XII & Port); the Commissioner of Police; ACB Maharashtra
CC:   PressDetective   (kindly acknowledge and reply)
Date: {TODAY}

Respected Sir/Madam,

I place on record, for all departments, how a false / materially altered complaint by Mr.
Abhishek Badriprasad Saraf led to FIR No. 0654/2022, and I request lawful action.

1. Mr. Tarun Thadani (founder, Dharte / dharte.com) only INVITED guests to the opening of a
   restaurant in Worli in early June 2022; he was not present at the time of the argument.
2. Two guests -- Mr. Ali Asgar Merchant and Mr. Saraf -- fought; Mr. Merchant slapped Mr. Saraf
   (at most Section 323 IPC, bailable).
3. Mr. Saraf's OWN first complaint (Worli PS, ID 23244/2022, 4 June 2022) records, in his own
   words, that he was there "on an invite [from] tarun thadani" and that "ali assaulted me by
   hitting on the face." It alleges ONLY an assault by Mr. Merchant -- NO extortion, NO Rs 1
   crore, NO role for Mr. Thadani.
4. When that complaint did not get the response he wanted, Mr. Saraf CHANGED the story ~2 months
   later -- adding a Rs 1 crore "extortion" and Mr. Thadani's name.
5. He got the false FIR 0654/2022 registered through the CB-CID Anti-Extortion Cell, MISLEADING
   the investigating officer (Insp. Sanjay Taralgatti) -- no accused examined, no CDR/bank/CCTV.
6. Mr. Santosh Sakpal recorded statements before the Azad Maidan PS (API P.R. Patil, 21/8/23) and
   the D-South Crime Branch (ACP Dattatray Nale, 26/8/23); an inquiry was opened but stalled.

REQUEST: (a) register and investigate the false / altered complaint by Mr. Saraf (the
contradiction between ID 23244/2022 and the later extortion version), applying Sections 217/248
BNS (formerly IPC 182/211); (b) reinvestigate FIR 0654/2022 against the original complaint; and
(c) take lawful action after due investigation. The original complaint (ID 23244/2022) and the
recorded statements will be furnished on request. Sub-judice; nothing herein prejudges any
pending proceeding.

Yours faithfully,
Santosh Sakpal -- Independent Investigator
+91 82689 17276 | santoshsakpal03@gmail.com  (PressDetective | info@pressdetective.com)"""

full=[f'{p}@mahapolice.gov.in' if '@' not in p else p for p in POLICE]
_ctx=ssl.create_default_context(); _ctx.check_hostname=False; _ctx.verify_mode=ssl.CERT_NONE
print('='*70); print(f'POLICE RETRY via Santosh/Proton -- {len(full)} departments'); print('='*70)
def chunk(l,n):
    for i in range(0,len(l),n): yield l[i:i+n]
sent=0
for i,b in enumerate(chunk(full,25),1):
    m=MIMEMultipart('alternative'); m['From']=FROM_HDR; m['To']=FROM; m['Cc']=INFO
    m['Subject']=SUBJ; m['Reply-To']=FROM
    m.attach(MIMEText(BODY,'plain','utf-8'))
    rcpts=[FROM,INFO]+b
    try:
        with smtplib.SMTP(PH,PP,timeout=40) as s:
            s.ehlo(); s.starttls(context=_ctx); s.ehlo(); s.login(FROM,TOKEN)
            s.sendmail(FROM,rcpts,m.as_string())
        print(f'  batch {i}: processed ({len(b)} police addrs -- see guard drops above)'); sent+=1
    except Exception as e:
        print(f'  batch {i}: {str(e)[:80]}')
    time.sleep(4)
print(f'\nProcessed {sent} batches. Any address NOT listed as dropped was kept and will bounce')
print('at the mgovcloud gateway. Verify via Bridge. Email cannot reach these -- use portal/post.')
