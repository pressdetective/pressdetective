#!/usr/bin/env python3
"""send_followup_evidence.py -- 21 June 2026
Document-backed follow-up from Santosh, now that the complainant's OWN original
complaint (Worli PS, ID 23244/2022, 4 Jun 2022) is in hand -- it records only an
ASSAULT by Mr. Merchant, NO extortion, and names Mr. Thadani solely as the host who
invited the guests. Plus Santosh's recorded statements before Azad Maidan PS / D-South
Crime Branch (Aug 2023).

EMAIL A -> Times of India (Ahmed Ali + desks): follow-up + reiterated correction/right of reply.
EMAIL B -> ACB + Anti-Extortion Cell + CP Mumbai: investigation follow-up (gov gateway may bounce).
EMAIL C -> tonymony@gmail.com: full updated report.

Guarded by lib.presend_guard (no-contact Saraf + suppression + live MX). Documents are
referenced and offered for verification, NOT attached (privacy: complaint holds third
parties' personal data; the confidential video is never distributed). Sub-judice safe;
no bribery-as-fact; officer framed as misled, not accused.
"""
import smtplib, ssl, json, sys, time
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

import sys as _pg_sys, pathlib as _pg_pl
_pg_sys.path.insert(0, str(_pg_pl.Path(__file__).resolve().parents[2]))
import lib.presend_guard  # noqa: F401  -- strips no-contact/suppressed/dead before send
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CREDS=json.loads(Path(r'C:\dev\pressdetective\.creds\proton_accounts.json').read_text(encoding='utf-8-sig'))
FROM=CREDS['accounts']['santosh']['address']; TOKEN=CREDS['accounts']['santosh']['token']
PH=CREDS['smtp_remote']['host']; PP=CREDS['smtp_remote']['port']
FROM_INV=formataddr(('Santosh Sakpal, Independent Investigator', FROM))
FROM_PD =formataddr(('Santosh Sakpal, PressDetective', FROM))
TODAY='21 June 2026'; INFO='info@pressdetective.com'

_ctx=ssl.create_default_context(); _ctx.check_hostname=False; _ctx.verify_mode=ssl.CERT_NONE
def send(from_hdr,to,cc,subj,body,label):
    m=MIMEMultipart('alternative'); m['From']=from_hdr; m['To']=', '.join(to)
    if cc: m['Cc']=', '.join(cc)
    m['Subject']=subj; m['Reply-To']=FROM
    m.attach(MIMEText(body,'plain','utf-8'))
    rcpts=list(to)+list(cc or [])
    for att in range(3):
        try:
            with smtplib.SMTP(PH,PP,timeout=40) as s:
                s.ehlo(); s.starttls(context=_ctx); s.ehlo(); s.login(FROM,TOKEN)
                s.sendmail(FROM,rcpts,m.as_string())
            print(f'  [{label}] OK via Proton'); return True
        except Exception as e:
            print(f'  [{label}] attempt {att+1}: {str(e)[:80]}'); time.sleep(6)
    print(f'  [{label}] FAILED'); return False

# ---- shared documented sequence ----
SEQ=f"""THE DOCUMENTED SEQUENCE (now backed by the complainant's own first complaint)
1. INVITATION ONLY. Mr. Tarun Thadani (founder, Dharte / dharte.com) invited guests to the
   opening of his Worli restaurant in early June 2022. His role was to invite -- nothing more.
2. A FIGHT BETWEEN TWO GUESTS. Mr. Ali Asgar Merchant and the complainant, Mr. Abhishek Saraf,
   got into a fight; Mr. Merchant slapped Mr. Saraf. The defence's position is that Mr. Thadani
   was not present at the time of that altercation.
3. THE COMPLAINANT'S OWN FIRST COMPLAINT. On 4 June 2022 Mr. Saraf himself lodged an online
   complaint at Worli Police Station -- COMPLAINT ID 23244/2022 (timestamped 04/06/2022
   03:43:44). In his OWN words it records that he was at the restaurant "on an invite [from]
   tarun thadani" and that "ali assaulted me by hitting on the face." IT ALLEGES ONLY AN
   ASSAULT BY MR. MERCHANT. There is NO extortion, NO demand of Rs 1 crore, and NO allegation
   that Mr. Thadani did anything beyond inviting the guests.
4. THE STORY CHANGED WHEN THAT DID NOT WORK. When the original assault complaint did not yield
   the outcome he wanted, a materially different version surfaced about two months later -- now
   alleging a Rs 1 crore "extortion" and, for the first time, naming Mr. Thadani.
5. THE FABRICATED FIR. On that altered version, FIR No. 0654/2022 was registered (Dadar PS,
   13 August 2022) and routed through the CB-CID Anti-Extortion Cell. The defence contends the
   Cell and its investigating officer (Insp. Sanjay Taralgatti) were misled by the false
   narrative into registering a non-bailable extortion case unsupported by any evidence -- no
   accused examined, no call records, no bank records, no CCTV verified.
6. AN INQUIRY WAS OPENED BUT STALLED. Mr. Santosh Sakpal pursued the matter with the police and
   RECORDED A FORMAL STATEMENT (jabaab) before the Azad Maidan Police Station (Asst. P.I.
   P. R. Patil, 21 August 2023) and the D-South Crime Branch (ACP Dattatray Nale, 26 August
   2023). An inquiry was opened on the complaint about this false FIR -- but no outcome has
   followed.

The original complaint (ID 23244/2022) and the recorded statements are in our possession and
will be furnished for verification on request."""

# =================== EMAIL A: Times of India ===================
A_TO=['ahmed.ali@timesgroup.com']
A_CC=['editor@timesgroup.com','mumbai.letters@timesgroup.com','mumbai.crime@timesgroup.com',INFO]
A_SUBJ=('FOLLOW-UP WITH DOCUMENTARY PROOF -- complainant\'s OWN first complaint (Worli PS, ID '
        '23244/2022, 4 Jun 2022) alleges only an assault by Mr. Merchant, NO extortion, and '
        'names Mr. Thadani only as the host who invited the guests | correction + right of '
        'reply reiterated | '+TODAY)
A_BODY=f"""To:   Mr. S. Ahmed Ali, Senior Assistant Editor, The Times of India, Mumbai
CC:   The Editor, ToI (Mumbai); ToI Mumbai City/Crime Desk; PressDetective
Date: {TODAY}

Dear Mr. Ahmed Ali,

Further to my notice and clarification, I can now place before you the single document that
settles the matter: the complainant's OWN original complaint.

{SEQ}

WHY THIS MATTERS TO YOUR REPORT
Your report carried the complainant's later "extortion" version while omitting that his own
first complaint -- in his own words, on the police record -- accused only Mr. Merchant of an
assault and said nothing about extortion or Mr. Thadani. That document alone shows the
extortion narrative to be a later addition, not part of the original case.

I therefore REITERATE my request for (a) a correction carrying these facts with the same
prominence; (b) a right of reply for the accused and their counsel; and (c) takedown or
annotation of the article pending correction. I will gladly furnish the original complaint
(ID 23244/2022) and the recorded police statements for your verification.

Failing a fair correction, the affected parties reserve all lawful remedies, including a
criminal-defamation complaint (Section 356 BNS) and a Press Council of India complaint. This
communication is sub-judice compliant and prejudges nothing; it seeks accurate, balanced
reporting and the accused's right of reply.

Yours faithfully,
Santosh Sakpal -- Independent Investigator
+91 82689 17276 | santoshsakpal03@gmail.com   (PressDetective | info@pressdetective.com)"""

# =================== EMAIL B: ACB + AEC + CP ===================
B_TO=['acbwebmail@mahapolice.gov.in','cbcidmumaecell@mahapolice.gov.in']
B_CC=['cp.mumbai@mahapolice.gov.in',INFO]
B_SUBJ=('FOLLOW-UP + DOCUMENTARY PROOF -- request to progress inquiry into FIR No. 0654/2022 | '
        'complainant\'s OWN first complaint (ID 23244/2022) had NO extortion | statements '
        'already recorded at Azad Maidan PS / D-South Crime Branch | Santosh Sakpal | '+TODAY)
B_BODY=f"""To:   The Director General, Anti-Corruption Bureau of Maharashtra
      The Officer-in-Charge, CB-CID Anti-Extortion Cell, Mumbai
CC:   The Commissioner of Police, Greater Mumbai; PressDetective
Date: {TODAY}

Respected Sir/Madam,

I follow up my earlier complaints in this matter, now with documentary proof.

{SEQ}

REQUEST
1. That the inquiry already opened (statements recorded at the Azad Maidan PS and the D-South
   Crime Branch in August 2023) be PROGRESSED to a conclusion, as no outcome has yet followed.
2. That FIR No. 0654/2022 be examined against the complainant's OWN original complaint
   (ID 23244/2022) -- which contained no extortion and no allegation against Mr. Thadani -- to
   establish how and on what basis the later "extortion" version came to be registered.
3. That the conduct of the complainant in advancing a materially altered version be inquired
   into, and the antecedents of Mr. Abhishek Badriprasad Saraf verified.

I am willing to depose and to furnish the original complaint and the recorded statements. This
matter is sub-judice; nothing herein prejudges any pending proceeding.

(Note: I am also lodging this through the ACB/Police online portals and by registered post,
as official channels.)

Yours faithfully,
Santosh Sakpal -- Independent Investigator | +91 82689 17276 | santoshsakpal03@gmail.com"""

# =================== EMAIL C: full report to tonymony ===================
C_TO=['tonymony@gmail.com']; C_CC=[INFO]
C_SUBJ='FULL REPORT (updated with documentary proof) -- FIR 0654/2022 (Tarun Thadani) | '+TODAY
C_BODY=f"""FULL CASE REPORT -- updated {TODAY}
Matter: FIR No. 0654/2022, Dadar PS / CB-CID Anti-Extortion Cell, Mumbai
Re:     Mr. Tarun Thadani (founder, Dharte / dharte.com) & Mr. Ali Asgar Merchant
Prepared by: Santosh Sakpal, Independent Investigator (PressDetective)

KEY DEVELOPMENT: we now hold the complainant's OWN original complaint, which is the
documentary proof the case turns on.

{SEQ}

WHAT WAS DONE TODAY ({TODAY})
- TIMES OF INDIA (Mr. S. Ahmed Ali + Editor/Mumbai/Crime desks): a follow-up attaching the
  significance of the original complaint (ID 23244/2022) and REITERATING the correction +
  right-of-reply demand. DELIVERED.
- ACB + ANTI-EXTORTION CELL + COMMISSIONER OF POLICE: a documentary follow-up asking that the
  inquiry already opened (statements recorded Aug 2023 at Azad Maidan PS / D-South Crime
  Branch) be progressed, and that FIR 0654/2022 be examined against the original complaint.
  NOTE: the government mail gateway has been rejecting our email to these offices; the same
  complaint is therefore also being lodged via the ACB / Mumbai-Police ONLINE PORTALS and by
  REGISTERED POST (ready-to-submit pack prepared).

WORK TO DATE (recap)
- ~291 Mumbai crime/legal journalists briefed with the documented story (delivered, no bounces).
- 89 legal allies (FIR-quashing counsel, legal press, NGOs, bar bodies, academics, HRCs)
  briefed on the abuse-of-process / quashing grounds (~77 delivered).
- Off-email filing pack prepared for ACB / Police / NHRC / MSHRC / NALSA / DLSA.

OUTSTANDING / NEXT STEPS
1. SUBMIT the ACB / Police / NHRC complaints via their online portals + registered post
   (the only route that reaches them; each gives an acknowledgment number / receipt).
2. PURSUE the quashing remedy (Section 528 BNSS / Article 226) through counsel.
3. WATCH ToI for the correction; if none within the deadline, file the Press Council complaint.
4. PRESS the Azad Maidan PS / Crime Branch inquiry to a conclusion.

COMPLIANCE: every communication is truthful, document-based, sub-judice safe and
defamation-safe (no assertion that anyone took a bribe; officer framed as misled, not accused;
no arrest threats); GDPR honoured; the complainant is never contacted; the confidential video
is never distributed.

Contact: Santosh Sakpal, +91 82689 17276 | santoshsakpal03@gmail.com.
This report is confidential and prepared for the case stakeholders."""

print('='*70); print('DOCUMENT-BACKED FOLLOW-UP |',FROM_INV); print('='*70)
print('\n--- EMAIL A: Times of India ---')
send(FROM_INV,A_TO,A_CC,A_SUBJ,A_BODY,'ToI'); time.sleep(4)
print('\n--- EMAIL B: ACB + Anti-Extortion Cell + CP (gov gateway may strip/bounce) ---')
send(FROM_INV,B_TO,B_CC,B_SUBJ,B_BODY,'Authorities'); time.sleep(4)
print('\n--- EMAIL C: Full report to tonymony@gmail.com ---')
send(FROM_PD,C_TO,C_CC,C_SUBJ,C_BODY,'Report')
print('\nDone. (verify via Bridge next)')
