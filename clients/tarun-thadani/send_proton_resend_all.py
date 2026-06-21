#!/usr/bin/env python3
"""
send_proton_resend_all.py -- 20 June 2026
RE-SEND of today's campaign that silently failed.

ROOT CAUSE of the failure: the From header was built as
  'Santosh Sakpal, Independent Investigator <santosh@pressdetective.com>'
The COMMA made both Postmark AND Proton parse "Santosh Sakpal" as a second,
invalid address and reject every message ("Invalid 'From' address"). Fixed here
with email.utils.formataddr -> '"Santosh Sakpal, Independent Investigator" <...>'.

PER USER: send via ProtonMail only. santosh@pressdetective.com IS ProtonMail
(domain hosted on Proton; smtp.protonmail.ch). Verified working in diagnostic
(login 235, SEND OK). NO Postmark fallback in this run (Proton-only by request).

Proton has a daily recipient limit and is not a bulk sender. Order: authorities
first, then police circular, then full press. On a throttle/limit error the run
STOPS and reports exactly where, so nothing fails silently again.

Saraf is NEVER a recipient (runtime assert). MP4 never attached. Sub-judice safe.
NO underworld/D.K. Rao claim anywhere (declined: unsubstantiated/defamatory).
"""
import smtplib, ssl, json, sys, time
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT  = Path(r'C:\dev\pressdetective')
CREDS = json.loads((ROOT / '.creds/proton_accounts.json').read_text(encoding='utf-8-sig'))
FROM     = CREDS['accounts']['santosh']['address']
TOKEN    = CREDS['accounts']['santosh']['token']
PROTON_H = CREDS['smtp_remote']['host']; PROTON_P = CREDS['smtp_remote']['port']
FROM_HDR = formataddr(('Santosh Sakpal, Independent Investigator', FROM))   # <-- FIX

TODAY = '20 June 2026'
FORBIDDEN = {'abhishek_saraf78@yahoo.com'}

INFO='info@pressdetective.com'; ACB='acbwebmail@mahapolice.gov.in'
AEC='cbcidmumaecell@mahapolice.gov.in'; JTCP='cp.mumbai.jtcp.crime@mahapolice.gov.in'
DGP='dgp.mah@mahapolice.gov.in'; EOW='adg.eowms@mahapolice.gov.in'

POLICE = [f'{s}@mahapolice.gov.in' for s in (
 'ps.aareysub.mum','ps.agripada.mum','ps.airport.mum','ps.andheri.mum','ps.antophill.mum',
 'ps.bangurnagar.mum','ps.bykhla.mum','ps.centralcyber.mum','ps.charkop.mum','ps.charkopp.mum',
 'ps.chunabhatti.mum','ps.dadar.mum','ps.dbmarg.mum','ps.deonar.mum','ps.dnnagar.mum',
 'ps.eastcyber.mum','ps.goregaoneatc.mum','ps.govandi.mum','ps.jjmarg.mum','ps.jogeshwari.mum',
 'ps.juhu.mum','ps.kalachowki.mum','ps.kalchowki.mum','ps.kanjurmarg.mum','ps.kasturba.mum',
 'ps.kurla.mum','ps.ltmarg.mum','ps.mahim.mum','ps.malabarhill.mum','ps.mankhurd.mum',
 'ps.mulund.mum','ps.nagpada.mum','ps.northcyber.mum','ps.oshiwara.mum','ps.paydhunie.mum',
 'ps.sagari2.mum','ps.sahar.mum','ps.samtanagar.mum','ps.southcyber.mum','ps.tilaknagar.mum',
 'ps.versova.mum','ps.vikhroli.mum','ps.vproad.mum','ps.wadala.mum',
 'dcpzone1-mum','dcpzone2-mum','dcpzone3-mum','dcpzone4-mum','dcpzone5-mum','dcpzone6-mum',
 'dcpzone7-mum','dcpzone8-mum','dcpzone9-mum','dcpzone10-mum','dcpzone11-mum','dcpzone12-mum',
 'dcpzoneport-mum','dcpdet1.mum','dcpenforcement-mum','dcpeowzone-mum','dcpcybercrime.mum',
 'crimebranchmumbai','eow.mumbai','acpworli.mum','acpam.mum',
)]
PRESS = json.loads((ROOT / 'clients/tarun-thadani/_press_all.json').read_text())

def clean(addrs, where):
    bad=[a for a in addrs if a.lower() in FORBIDDEN or 'saraf' in a.lower()]
    if bad: print(f'FATAL forbidden {bad} in {where}'); sys.exit(2)
clean(PRESS,'PRESS'); clean(POLICE,'POLICE')

# ---------------- Proton-only sender with limit detection ----------------
_ctx = ssl.create_default_context(); _ctx.check_hostname=False; _ctx.verify_mode=ssl.CERT_NONE
LIMIT_HIT = {'stop': False}
def proton_send(rcpts, msg_obj, label):
    if LIMIT_HIT['stop']:
        print(f'  [{label}] SKIPPED (Proton limit already hit)'); return 'skip'
    try:
        with smtplib.SMTP(PROTON_H, PROTON_P, timeout=30) as s:
            s.ehlo(); s.starttls(context=_ctx); s.ehlo(); s.login(FROM, TOKEN)
            s.sendmail(FROM, rcpts, msg_obj.as_string())
        print(f'  [{label}] OK via Proton ({len(rcpts)} rcpt)'); return 'ok'
    except Exception as e:
        es=str(e).lower()
        if any(k in es for k in ['limit','quota','too many','rate','exceed','4.2.1','2024','spam']):
            LIMIT_HIT['stop']=True
            print(f'  [{label}] !! PROTON LIMIT/BLOCK: {str(e)[:160]}'); return 'limit'
        print(f'  [{label}] ERROR: {str(e)[:160]}'); return 'err'

def build(to_list, cc_list, subject, body, bcc=None, unsub=False):
    m=MIMEMultipart('alternative'); m['From']=FROM_HDR; m['To']=', '.join(to_list)
    if cc_list: m['Cc']=', '.join(cc_list)
    m['Subject']=subject; m['Reply-To']=FROM
    if unsub: m['List-Unsubscribe']='<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    m.attach(MIMEText(body,'plain','utf-8'))
    r=list(to_list)+list(cc_list or [])+list(bcc or []); clean(r,subject[:30]); return m,r

def chunk(l,n):
    for i in range(0,len(l),n): yield l[i:i+n]

SIG=f"""Yours faithfully,
Santosh Sakpal -- Independent Investigator
Phone   : +91 82689 17276 | Email: santoshsakpal03@gmail.com
Address : B/6 Shimgyamanohar Apartments, Thane Belapur Road, Digha West, Navi Mumbai 400708
Date    : {TODAY}   (Submitted with the assistance of PressDetective | info@pressdetective.com)"""

# ===================== BODIES =====================
AUTH_SUBJ=('COMPLAINT + REQUEST FOR FULL INVESTIGATION & DUE DILIGENCE -- False FIR '
 'No. 0654/2022 (Dadar PS / CB-CID Anti-Extortion Cell) | Fabricated Rs 1 Crore '
 '"Extortion" | Dharte.com Founder Falsely Implicated | Santosh Sakpal | '+TODAY)
AUTH_BODY=f"""To,  The Director General, Anti-Corruption Bureau of Maharashtra
CC:  CB-CID Anti-Extortion Cell; Jt. CP (Crime), Mumbai; DGP Maharashtra;
     ADG Economic Offences Wing; PressDetective (for record)
Date: {TODAY}

Respected Sir/Madam,

I, Santosh Sakpal, an independent investigator, request a full investigation into
how FIR No. 0654/2022 came to be registered, and into the conduct of the complainant.

THE DOCUMENTED FACTS
1. On or about 2 June 2022, at a Worli restaurant, Mr. Abhishek Badriprasad Saraf
   was slapped by Mr. Ali Asgar Merchant -- at its highest IPC s.323 (bailable).
2. On 4 June 2022 Mr. Saraf's OWN online complaint (ID 23244/2022) alleged ONLY the
   slap -- NO extortion, NO Rs 1 crore, NO mention of Mr. Tarun Thadani.
3. The regular police did not register a serious case on so minor a matter.
4. Roughly two months later FIR No. 0654/2022 was registered (Dadar PS, 13 Aug 2022)
   and routed through the CB-CID Anti-Extortion Cell, now alleging -- for the first
   time -- a Rs 1 crore "extortion" and naming Mr. Thadani, founder of Dharte
   (dharte.com), who was NOT present at the venue.
5. No accused was examined before registration; no CDR, bank records or CCTV (none of
   which support any extortion) were verified.

WHAT I ALLEGE AND REQUEST BE INVESTIGATED (in good faith, for lawful inquiry)
 (i)  Whether, the regular police having declined, Mr. Saraf fabricated and inflated
      the incident into a false Rs 1 crore "extortion" to bring it within the Anti-
      Extortion Cell's remit;
 (ii) Whether the registration of the FIR was procured by corrupt or improper means;
 (iii)Whether the Anti-Extortion Cell and its investigating officer were MISLED /
      MANIPULATED by that false narrative into registering a non-bailable case
      unsupported by evidence;
 (iv) Why a non-bailable FIR (up to 10 years) issued without examining any accused.

DUE DILIGENCE ON THE COMPLAINANT (full particulars provided so authorities may verify)
   Name    : Mr. Abhishek Badriprasad Saraf
   Phone   : +91 98201 80065
   Address : 3rd Floor, Esplanade House, 29, Hazarimal Somani Marg, Fort, Mumbai 400001
   Public-record reference: party to Calcutta High Court proceedings CS 313/2012
   (Martin Burn Limited). I make no assertion beyond this public record and leave
   verification of his antecedents and associations to the authorities.

PRAYER: (1) a full investigation into the manufacture/registration of FIR 0654/2022;
(2) due-diligence verification of the complainant's antecedents; (3) such action as
the law permits against any person -- complainant or public servant -- who abused the
process. This matter is sub-judice; nothing herein prejudges any pending proceeding.

{SIG}"""

POL_SUBJ=('FORMAL COMPLAINT -- False FIR No. 0654/2022 | Fabricated "Extortion" After '
 'Police Declined to Act | Dharte.com Founder Tarun Thadani Falsely Implicated (Not '
 'Present) | Request for Scrutiny | Santosh Sakpal | '+TODAY)
POL_BODY=f"""To,  The Sr. PI / Officer-in-Charge, ALL Police Stations, Mumbai City & Suburban;
     CB-CID Anti-Extortion Cell; Crime Branch; DCsP (Zones I-XII & Port).
CC:  Jt. CP (Crime); ACB Maharashtra; DGP Maharashtra; PressDetective (record)
Date: {TODAY}

Respected Sir/Madam,

I place the following documented facts on record and request scrutiny.
1. On or about 2 June 2022 a minor altercation occurred at a Worli restaurant in which
   Mr. Abhishek Badriprasad Saraf was slapped by Mr. Ali Asgar Merchant (at most IPC
   s.323, bailable).
2. Mr. Saraf's OWN original complaint of 4 June 2022 (ID 23244/2022) alleged only the
   slap -- NO extortion, NO Rs 1 crore, and did NOT name Mr. Tarun Thadani.
3. The regular police rightly did not register a serious case.
4. ~Two months later, FIR No. 0654/2022 was registered (Dadar PS, 13 Aug 2022) on a
   materially altered narrative alleging a Rs 1 crore "extortion" and naming Mr.
   Thadani, founder of Dharte (dharte.com) -- who was NOT present -- routed through the
   CB-CID Anti-Extortion Cell.
5. Neither accused was examined before registration; no CDR/bank/CCTV verified.

It is my respectful submission that, the regular police having declined, the complainant
manufactured a false extortion narrative and caused a non-bailable FIR to be registered
through the Anti-Extortion Cell, falsely implicating an innocent man who was not present.
A detailed complaint on the corrupt manner of registration is before the ACB.

REQUEST: take this on record and scrutinise the FIR, the original complaint (ID
23244/2022), and the investigation that preceded registration. Sub-judice; prejudges
nothing.

{SIG}"""

PR_SUBJ=('PRESS NOTE / REQUEST FOR INVESTIGATION -- How a Bailable Slap Became a Non-'
 'Bailable "Rs 1 Crore Extortion": FIR 0654/2022 | Dharte.com Founder Tarun Thadani '
 'Trapped Though Not Present | Santosh Sakpal | '+TODAY)
PR_BODY=f"""PRESS NOTE -- FOR CRIME & LEGAL DESKS
Issued by : Santosh Sakpal, Independent Investigator | +91 82689 17276 | santoshsakpal03@gmail.com
Date      : {TODAY}

HOW A MINOR SLAP WAS TURNED INTO A NON-BAILABLE "Rs 1 CRORE EXTORTION" --
AND HOW TWO MEN, ONE NOT EVEN PRESENT, WERE TRAPPED IN IT

Every fact below is from the record; the sharper characterisations are the defence's
contentions and the subject of complaints now before the ACB and the Mumbai police.

> On or about 2 June 2022, at a Worli restaurant, Mr. Abhishek Badriprasad Saraf was
  slapped by Mr. Ali Asgar Merchant. A slap is, at most, IPC s.323 -- bailable.
> On 4 June 2022 Mr. Saraf's OWN online complaint (ID 23244/2022) alleged ONLY the slap
  -- NO extortion, NO Rs 1 crore, NO mention of Mr. Tarun Thadani, founder of Dharte
  (dharte.com).
> The regular police did not register a serious case on so minor a matter.
> Then, ~two months later, the story changed entirely: FIR No. 0654/2022 (Dadar PS,
  13 Aug 2022), routed through the CB-CID Anti-Extortion Cell, alleged for the first
  time a Rs 1 crore "extortion" and named Mr. Thadani -- who was NOT present.
> No accused was examined before registration; no call records, bank records or CCTV
  were verified.

THE QUESTION: how does a complaint that, in the complainant's own first telling, was a
slap become -- two months later, with no new verified evidence -- a non-bailable
extortion case carrying up to ten years, sweeping in a man who was never there?

The defence contends, and complaints now before the ACB allege, that after failing to
obtain action on a minor matter the complainant advanced a false, exaggerated
"extortion" that misled the Anti-Extortion Cell into registering a grave non-bailable
case, trapping Mr. Merchant and an absent Mr. Thadani. A recent Times of India report
has carried the case one-sidedly, omitting every exculpatory fact above.

ASKED: a FULL INVESTIGATION into how a no-extortion complaint became a non-bailable
extortion FIR two months later (complaints are before the ACB and Mumbai police). Of
journalists: please seek the defence's version before publishing -- contact PressDetective at +91 82689 17276 -- and examine the documented timeline. Mr. Thadani
(Dharte.com) was not present and was not named in the complainant's own original
complaint. Sub-judice compliant; prejudges nothing.

-- Santosh Sakpal, Independent Investigator (+91 82689 17276 | santoshsakpal03@gmail.com)
   Issued with the assistance of PressDetective | info@pressdetective.com
   To unsubscribe: email info@pressdetective.com, subject UNSUBSCRIBE."""

# ===================== SEND =====================
print('='*70); print('PROTON-ONLY RE-SEND  |  FROM:', FROM_HDR)
print(f'Police depts: {len(POLICE)}  |  Press: {len(PRESS)}'); print('='*70)
res={}; sent_recip=0

print('\n--- 1/3 AUTHORITIES: ACB complaint + full investigation + due diligence ---')
m,r=build([ACB],[AEC,JTCP,DGP,EOW,INFO],AUTH_SUBJ,AUTH_BODY)
st=proton_send(r,m,'AUTH'); res['1. Authorities']=st
if st=='ok': sent_recip+=len(r)
time.sleep(6)

print('\n--- 2/3 POLICE circular (BCC batches of 20) ---')
okb=nb=0
for i,b in enumerate(chunk(POLICE,20),1):
    nb+=1; m,r=build([AEC],[JTCP,ACB,INFO],POL_SUBJ,POL_BODY,bcc=b)
    st=proton_send(r,m,f'POLICE {i} ({len(b)})')
    if st=='ok': okb+=1; sent_recip+=len(r)
    if st=='limit': break
    time.sleep(6)
res['2. Police']=f'{okb}/{nb} batches'

print('\n--- 3/3 PRESS story (BCC batches of 20) ---')
okp=np_=0
for i,b in enumerate(chunk(PRESS,20),1):
    np_+=1; m,r=build([FROM],[INFO],PR_SUBJ,PR_BODY,bcc=b,unsub=True)
    st=proton_send(r,m,f'PRESS {i} ({len(b)})')
    if st=='ok': okp+=1; sent_recip+=len(r)
    if st=='limit': break
    time.sleep(6)
res['3. Press']=f'{okp}/{np_} batches'

print('\n'+'='*70); print('RESULTS:')
for k,v in res.items(): print(f'  {v:>16}  --  {k}')
print(f'\nApprox recipients accepted by Proton: {sent_recip}')
if LIMIT_HIT['stop']:
    print('\n*** PROTON THROTTLED/BLOCKED mid-run -- remaining batches NOT sent.')
    print('*** Wait ~24h and re-run, or switch remainder to Postmark (now verified).')
print('NOTE: SMTP OK != delivered. Watch info@ inbox for bounce DSNs.')
print('Done.')
