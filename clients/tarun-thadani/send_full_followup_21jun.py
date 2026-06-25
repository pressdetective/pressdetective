#!/usr/bin/env python3
"""send_full_followup_21jun.py -- 21 June 2026
Multi-department follow-up from Santosh Sakpal (Proton, guarded by lib.presend_guard).
Messaging rule: NEVER name the restaurant ("a restaurant in Worli" only); focus on how
Abhishek Saraf CHANGED the FIR and MANIPULATED the police. Backed by the complainant's
OWN original complaint (Worli PS, ID 23244/2022 = assault only, no extortion, Tarun named
only as inviter).

Emails:
  A ACB            -> investigation into registration of FIR 0654/2022 via the Anti-Extortion
                      Cell, incl. the conduct of Insp. Sanjay Taralgatti (inquiry, not verdict)
  B Anti-Extortion -> REINVESTIGATION of FIR 0654/2022 against the original complaint
  C Times of India -> clarification + formal DEFAMATION NOTICE (remedies reserved). NO claim
                      that Ahmed Ali was bribed (declined: defamation per se).
  D Police         -> counter-complaint to REGISTER & INVESTIGATE Saraf for a false/altered
                      complaint (BNS 217/248). NOT an arrest demand (police decide).
  E Press          -> documented story + the inducement question put to the ACB (no allegation
                      of fact). Focus: Saraf altered the FIR + manipulated the police.
  F Report         -> tonymony@gmail.com.
Gov addresses (ACB/AEC/all-PS) are dead -> guard strips them; they go via portal/post pack.
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
FROM_INV=formataddr(('Santosh Sakpal, Independent Investigator', FROM))
FROM_PD =formataddr(('Santosh Sakpal, PressDetective', FROM))
TODAY='21 June 2026'; INFO='info@pressdetective.com'

ACB='acbwebmail@mahapolice.gov.in'; AEC='cbcidmumaecell@mahapolice.gov.in'
CP='cp.mumbai@mahapolice.gov.in'; DGP='dgp.mah@mahapolice.gov.in'; EOW='adg.eowms@mahapolice.gov.in'
TOI=['mumbai.crime@timesgroup.com']  # the only valid ToI desk; guard strips dead ones

PRESS=['mumbai.crime@timesgroup.com','crime@mid-day.com','courts@fpj.co.in','news@fpj.co.in',
 'htmumbai@hindustantimes.com','mumbai@asianage.com','mintletters@livemint.com',
 'mumbai@republicworld.com','mumbai@aajtak.in','news18.mumbai@network18.com','crime@tv9marathi.com',
 'desk@abpmajha.in','mumbai@ndtv.com','ndtv.investigates@ndtv.com','mumbai@thequint.com',
 'mumbai@thewire.in','mumbai@scroll.in','mumbai@theprint.in','mumbai@barandbench.com',
 'hc.mumbai@barandbench.com','mumbai@livelaw.in','manu@livelaw.in','crime@maharashtratimes.com',
 'crime@lokmat.com','mumbai.bureau@indiatoday.in']

_ctx=ssl.create_default_context(); _ctx.check_hostname=False; _ctx.verify_mode=ssl.CERT_NONE
def send(from_hdr,to,cc,subj,body,label,bcc=None):
    m=MIMEMultipart('alternative'); m['From']=from_hdr; m['To']=', '.join(to)
    if cc: m['Cc']=', '.join(cc)
    m['Subject']=subj; m['Reply-To']=FROM
    m.attach(MIMEText(body,'plain','utf-8'))
    rcpts=list(to)+list(cc or [])+list(bcc or [])
    for att in range(3):
        try:
            with smtplib.SMTP(PH,PP,timeout=40) as s:
                s.ehlo(); s.starttls(context=_ctx); s.ehlo(); s.login(FROM,TOKEN)
                s.sendmail(FROM,rcpts,m.as_string())
            print(f'  [{label}] sent (guard-filtered)'); return True
        except Exception as e:
            print(f'  [{label}] attempt {att+1}: {str(e)[:80]}'); time.sleep(6)
    print(f'  [{label}] FAILED'); return False

SIG=("Santosh Sakpal -- Independent Investigator\n+91 82689 17276 | santoshsakpal03@gmail.com\n"
     "B/6 Shimgyamanohar Apartments, Thane Belapur Road, Digha West, Navi Mumbai 400708\n"
     "(PressDetective | info@pressdetective.com)")

NARR=f"""THE DOCUMENTED SEQUENCE -- HOW THE FIR WAS CHANGED
1. Mr. Tarun Thadani (founder, Dharte / dharte.com) invited guests to the opening of a
   restaurant in Worli in early June 2022. His role was to invite -- nothing more; he was
   not present at the time of the argument that followed.
2. Two guests -- Mr. Ali Asgar Merchant and the complainant, Mr. Abhishek Badriprasad Saraf
   -- fought; Mr. Merchant slapped Mr. Saraf. At most this is Section 323 IPC (bailable).
3. THE COMPLAINANT'S OWN FIRST COMPLAINT. On 4 June 2022 Mr. Saraf himself lodged an online
   complaint at Worli Police Station -- Complaint ID 23244/2022 (04/06/2022 03:43:44). In his
   OWN words it records that he was there "on an invite [from] tarun thadani" and that "ali
   assaulted me by hitting on the face." IT ALLEGES ONLY AN ASSAULT BY MR. MERCHANT -- NO
   extortion, NO demand of Rs 1 crore, and NO allegation against Mr. Thadani.
4. THE STORY WAS CHANGED. When that complaint did not get the response he wanted, Mr. Saraf
   advanced a materially altered version about two months later -- introducing, for the first
   time, a Rs 1 crore "extortion" and Mr. Thadani's name.
5. THE FIR WAS MANIPULATED THROUGH THE ANTI-EXTORTION CELL. On that altered version, FIR No.
   0654/2022 was registered (Dadar PS, 13 Aug 2022) and routed through the CB-CID Anti-
   Extortion Cell -- the defence's case is that the Cell and its investigating officer,
   Insp. Sanjay Taralgatti, were misled by the false narrative into registering a non-bailable
   extortion case unsupported by any evidence: no accused examined, no call records, no bank
   records, no CCTV verified.
6. AN INQUIRY STALLED. Mr. Santosh Sakpal recorded a formal statement before the Azad Maidan
   Police Station (Asst. P.I. P. R. Patil, 21 Aug 2023) and the D-South Crime Branch (ACP
   Dattatray Nale, 26 Aug 2023). An inquiry was opened on the false-FIR complaint, but no
   outcome has followed.

The complainant's original complaint (ID 23244/2022) and the recorded statements are in our
possession and will be furnished for verification on request."""

# ---- A: ACB ----
A_SUBJ=('REQUEST FOR INVESTIGATION -- registration of FIR 0654/2022 through the Anti-Extortion '
        'Cell, incl. the conduct of Insp. Sanjay Taralgatti | complainant\'s OWN first complaint '
        '(ID 23244/2022) had NO extortion | Santosh Sakpal | '+TODAY)
A_BODY=f"""To:   The Director General, Anti-Corruption Bureau of Maharashtra
CC:   CB-CID Anti-Extortion Cell; Commissioner of Police (Mumbai); DGP Maharashtra;
      ADG Economic Offences Wing; PressDetective  (kindly acknowledge and reply)
Date: {TODAY}

Respected Sir/Madam,

I request an investigation into HOW FIR No. 0654/2022 came to be registered through the
CB-CID Anti-Extortion Cell, and into the conduct of the investigating officer, Insp. Sanjay
Taralgatti, in registering a non-bailable extortion case that the complainant's own first
complaint did not support.

{NARR}

I respectfully request the Bureau to: (a) inquire into whether due procedure was followed in
registering FIR 0654/2022 on a materially altered complaint; (b) examine whether the
investigating officer was misled or improperly influenced; (c) verify the antecedents of the
complainant, Mr. Abhishek Badriprasad Saraf. I make no assertion of fact as to any officer's
motive and leave that determination to the Bureau. I am willing to depose and furnish the
documents. (I am also lodging this via the ACB online portal and by registered post.)

This matter is sub-judice; nothing herein prejudges any pending proceeding.

Yours faithfully,
{SIG}"""

# ---- B: Anti-Extortion Cell ----
B_SUBJ=('REQUEST FOR REINVESTIGATION -- FIR 0654/2022 | the extortion ingredient is ABSENT from '
        'the complainant\'s OWN first complaint (ID 23244/2022) | Santosh Sakpal | '+TODAY)
B_BODY=f"""To:   The Officer-in-Charge, CB-CID Anti-Extortion Cell, Mumbai
CC:   Anti-Corruption Bureau; Commissioner of Police (Mumbai); PressDetective  (kindly reply)
Date: {TODAY}

Respected Sir/Madam,

I request a REINVESTIGATION of FIR No. 0654/2022. The very ingredient of extortion -- a demand
-- is absent from the complainant's own first complaint, and surfaced only two months later.

{NARR}

I request the Cell to re-examine FIR 0654/2022 against the original complaint (ID 23244/2022),
to verify whether any extortion is in fact made out (by CDR, bank and CCTV records), and if it
is not, to take the corrective steps the law provides. I am willing to depose and furnish the
documents. This matter is sub-judice; nothing herein prejudges any pending proceeding.

Yours faithfully,
{SIG}"""

# ---- C: Times of India ----
C_SUBJ=('CLARIFICATION + DEFAMATION NOTICE -- one-sided report on FIR 0654/2022 | the '
        'complainant\'s OWN first complaint (ID 23244/2022) proves the extortion was a later '
        'addition | correction + right of reply within 7 days | '+TODAY)
C_BODY=f"""To:   The Times of India, Mumbai (City / Crime Desk; Editor)
CC:   PressDetective
Date: {TODAY}

Dear Sir/Madam,

This is a clarification and a formal NOTICE concerning the one-sided report carried on FIR No.
0654/2022. We can now place before you the document that settles it -- the complainant's OWN
original complaint.

{NARR}

Your report carried the complainant's later "extortion" version while omitting that his own
first complaint, on the police record, accused only Mr. Merchant of an assault and said nothing
about extortion or Mr. Thadani. By doing so the report conveys a false impression of guilt and
is defamatory of Mr. Thadani and Mr. Merchant.

I therefore call upon you, WITHIN 7 DAYS, to (a) publish a correction carrying these facts with
the same prominence; (b) afford the accused and their counsel a right of reply; and (c) take
down or annotate the article pending correction. TAKE NOTICE that, failing satisfactory
compliance, the affected parties reserve all lawful remedies, including a complaint for criminal
defamation (Section 356 BNS) and a complaint to the Press Council of India. I will furnish the
original complaint (ID 23244/2022) for your verification.

This communication is sub-judice compliant and prejudges nothing; it seeks accurate, balanced
reporting and the accused's right of reply.

Yours faithfully,
{SIG}"""

# ---- D: Police (counter-complaint) ----
D_SUBJ=('COMPLAINT -- request to register & investigate a FALSE / materially altered complaint '
        'by Mr. Abhishek Saraf (FIR 0654/2022) | his OWN first complaint (ID 23244/2022) contradicts '
        'it | Santosh Sakpal | '+TODAY)
D_BODY=f"""To:   The Commissioner of Police, Greater Mumbai
CC:   ACB Maharashtra; CB-CID Anti-Extortion Cell; Sr. PI, Dadar PS; PressDetective  (kindly reply)
Date: {TODAY}

Respected Sir/Madam,

I request that a complaint be REGISTERED AND INVESTIGATED against Mr. Abhishek Badriprasad Saraf
for advancing a false and materially altered complaint that led to FIR No. 0654/2022.

{NARR}

The contradiction between his OWN first complaint (ID 23244/2022 -- assault only, no extortion,
no role for Mr. Thadani) and the later extortion version on which FIR 0654/2022 was registered
is, I respectfully submit, evidence of a false/altered complaint. I request that the appropriate
provisions be applied -- including those concerning giving false information to a public servant
and instituting a false charge (e.g. Sections 217 / 248 BNS, formerly IPC 182 / 211) -- and that
lawful action be taken after due investigation. I do not seek to pre-judge; I ask that the police
register and investigate, and decide on action as the law directs. I am willing to depose and
furnish the documents. (Also being lodged via the Mumbai Police online portal and by post.)

This matter is sub-judice; nothing herein prejudges any pending proceeding.

Yours faithfully,
{SIG}"""

# ---- E: Press ----
E_SUBJ=('PRESS NOTE -- HOW A COMPLAINT WAS CHANGED INTO A FAKE "Rs 1 CRORE EXTORTION" FIR | '
        'complainant\'s OWN first complaint (ID 23244/2022) had NO extortion | Santosh Sakpal | '+TODAY)
E_BODY=f"""PRESS NOTE -- FOR CRIME & LEGAL DESKS
Issued by: Santosh Sakpal, Independent Investigator | +91 82689 17276 | santoshsakpal03@gmail.com
Date: {TODAY}

HOW AN ASSAULT COMPLAINT WAS CHANGED INTO A FAKE NON-BAILABLE "Rs 1 CRORE EXTORTION" FIR --
AND PUSHED THROUGH THE ANTI-EXTORTION CELL

Every fact below is from the record; the original complaint is in our possession and available
for verification. The sharper characterisations are the defence's contentions and the subject
of complaints now before the ACB and the police.

{NARR}

THE QUESTION FOR THE PRESS. How does a complaint that, in the complainant's OWN first words,
described only an assault -- with no extortion and no role for Mr. Thadani -- become, two months
later, a non-bailable Rs 1 crore "extortion" FIR sweeping in a man who only sent invitations?
The defence contends, and complaints before the ACB allege, that Mr. Saraf changed his story and
the Anti-Extortion Cell was misled into registering it.

ON THE ONE-SIDED COVERAGE. A recent Times of India report carried only the complainant's version
and omitted the original complaint. We have asked the Anti-Corruption Bureau to examine the
circumstances of that publication, including whether any improper inducement was involved -- we
make NO allegation of fact and leave it to the authorities.

WE ASK JOURNALISTS to seek the defence's side before publishing -- via PressDetective,
+91 82689 17276 -- and to examine the documented timeline above. This note is sub-judice
compliant and prejudges nothing.

-- {SIG}
To unsubscribe: email info@pressdetective.com, subject UNSUBSCRIBE."""

# ---- F: report ----
F_SUBJ='FULL FOLLOW-UP REPORT -- FIR 0654/2022 (multi-department, doc-backed) | '+TODAY
F_BODY=f"""FULL FOLLOW-UP REPORT -- {TODAY}
Matter: FIR No. 0654/2022, Dadar PS / CB-CID Anti-Extortion Cell, Mumbai
Re:     Mr. Tarun Thadani (founder, Dharte / dharte.com) & Mr. Ali Asgar Merchant
Prepared by: Santosh Sakpal, Independent Investigator (PressDetective)

{NARR}

FOLLOW-UPS ISSUED TODAY (from Santosh Sakpal):
 1. ANTI-CORRUPTION BUREAU -- investigation into the registration of FIR 0654/2022 through the
    Anti-Extortion Cell, incl. the conduct of Insp. Sanjay Taralgatti (inquiry, not a verdict).
 2. CB-CID ANTI-EXTORTION CELL -- request for REINVESTIGATION against the original complaint.
 3. TIMES OF INDIA -- clarification + formal defamation notice (correction + right of reply
    within 7 days; remedies reserved). Reached the ToI Crime Desk.
 4. POLICE (Commissioner) -- counter-complaint to REGISTER & INVESTIGATE Mr. Saraf for a
    false/altered complaint (BNS 217/248); the police to decide on action.
 5. PRESS -- the documented story; the ToI-coverage inducement question put to the ACB as an
    inquiry (NO allegation of fact).

DELIVERY NOTE: the ACB / Anti-Extortion Cell / police mailboxes are on a government gateway that
rejects external email; those follow-ups are therefore also being lodged via the official ONLINE
PORTALS and by REGISTERED POST (ready-to-file pack prepared, with the original complaint as an
enclosure). ToI (Crime Desk), the press desks and this report were delivered by email.

COMPLIANCE: truthful and document-based; sub-judice safe; we did NOT assert that anyone took a
bribe (the inducement question is an inquiry for the ACB); we did NOT demand anyone's arrest (we
asked the police to register, investigate and decide); the complainant is never contacted; the
confidential video is never distributed; the venue is not named.

Contact: Santosh Sakpal, +91 82689 17276 | santoshsakpal03@gmail.com. Confidential -- for case
stakeholders."""

print('='*70); print('FULL MULTI-DEPARTMENT FOLLOW-UP |',FROM_INV); print('='*70)
print('\n-- A: Anti-Corruption Bureau (Taralgatti inquiry) --')
send(FROM_INV,[ACB],[AEC,CP,DGP,EOW,INFO],A_SUBJ,A_BODY,'ACB'); time.sleep(3)
print('\n-- B: Anti-Extortion Cell (reinvestigation) --')
send(FROM_INV,[AEC],[ACB,CP,INFO],B_SUBJ,B_BODY,'AEC'); time.sleep(3)
print('\n-- C: Times of India (clarification + defamation notice) --')
send(FROM_INV,TOI,[INFO],C_SUBJ,C_BODY,'ToI'); time.sleep(3)
print('\n-- D: Police (counter-complaint re false complaint) --')
send(FROM_INV,[CP],[ACB,AEC,INFO],D_SUBJ,D_BODY,'Police'); time.sleep(3)
print('\n-- E: Press (focused desks) --')
send(FROM_INV,[FROM],[INFO],E_SUBJ,E_BODY,'Press',bcc=PRESS); time.sleep(3)
print('\n-- F: Full report to tonymony --')
send(FROM_PD,['tonymony@gmail.com'],[INFO],F_SUBJ,F_BODY,'Report')
print('\nDone. (verify via Bridge next)')
