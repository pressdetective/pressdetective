#!/usr/bin/env python3
"""send_tonymony_report.py -- 20 June 2026
Full status report on the FIR 0654/2022 / Tarun Thadani matter to tonymony@gmail.com,
CC info@pressdetective.com. From Santosh via Proton (fixed From). Factual, sub-judice safe.
"""
import smtplib, ssl, json, sys
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CREDS=json.loads(Path(r'C:\dev\pressdetective\.creds\proton_accounts.json').read_text(encoding='utf-8-sig'))
FROM=CREDS['accounts']['santosh']['address']; TOKEN=CREDS['accounts']['santosh']['token']
PH=CREDS['smtp_remote']['host']; PP=CREDS['smtp_remote']['port']
FROM_HDR=formataddr(('Santosh Sakpal, PressDetective', FROM))
TO=['tonymony@gmail.com']; CC=['info@pressdetective.com']
TODAY='20 June 2026'

SUBJ='CASE STATUS REPORT -- FIR 0654/2022 (Tarun Thadani) | work completed + next steps | '+TODAY
BODY=f"""CASE STATUS REPORT
Matter: FIR No. 0654/2022, Dadar PS / CB-CID Anti-Extortion Cell, Mumbai
Re:     Mr. Tarun Thadani (founder, Dharte / dharte.com) & Mr. Ali Asgar Merchant
Date:   {TODAY}
Prepared by: Santosh Sakpal, Independent Investigator (PressDetective)

=====================================================================
1. THE MATTER (one paragraph)
=====================================================================
On 2 June 2022, at a private gathering at a Worli restaurant to which Mr. Thadani had
only sent the invitations -- and at which he was NOT present at the time of the argument
-- two guests, Mr. Ali Asgar Merchant and Mr. Abhishek Saraf, argued and Mr. Saraf was
slapped (at most Section 323 IPC, bailable). Mr. Saraf's own first complaint (4 June 2022,
online ID 23244/2022) alleged only the slap -- no extortion, no Rs 1 crore, no mention of
Mr. Thadani. About two months later, FIR 0654/2022 was registered (Dadar PS, 13 Aug 2022)
on a changed version alleging a Rs 1 crore "extortion" and naming Mr. Thadani -- with no
accused examined and no call-record, bank or CCTV verification. Discharge was refused by
the Sessions Court on 31 March 2024. The defence: a bailable incident was converted into a
non-bailable extortion case via a materially altered complaint.

=====================================================================
2. WORK COMPLETED
=====================================================================

A. PRESS / CORRECTIVE COVERAGE
   - Times of India (Mr. S. Ahmed Ali, author of the one-sided report): served a formal
     CORRECTION + RIGHT-OF-REPLY demand and a follow-up CLARIFICATION (delivered to his
     address + the ToI Editor/Mumbai/Crime desks), giving a 7-day window and reserving
     lawful remedies (criminal defamation under BNS 356 + a Press Council of India
     complaint). DELIVERED.
   - ~291 Mumbai crime & legal-press journalists: the full documented story and a
     follow-up note (corrected facts; the timeline of the altered complaint). DELIVERED
     (verified, no bounces).

B. LEGAL COMMUNITY (89 contacts)
   - FIR-quashing counsel, legal press, civil-liberties NGOs, bar councils/associations,
     statutory legal-aid bodies, law-school academics and human-rights bodies: an
     abuse-of-process briefing (Bhajan Lal / Arnesh Kumar / s.528 BNSS / Art. 226 grounds)
     requesting legal support, scrutiny, and quashing guidance. ~77 DELIVERED; the
     government bodies among them (NHRC, MSHRC, NALSA, DLSAs) bounced (see C).

C. AUTHORITIES (ACB / Mumbai Police / NHRC / MSHRC / NALSA / DLSAs)
   - Complaints fully drafted: a corruption/abuse-of-process complaint to the ACB, a
     scrutiny complaint to the Commissioner of Police, and human-rights complaints to
     NHRC/MSHRC, plus legal-aid applications.
   - DELIVERY ISSUE: their government mail gateway (mgovcloud.in / nic.in) rejects external
     email (dead mailboxes + policy blocks). Our own email is correctly configured (it
     reached ~291 mainstream journalists with zero bounces) -- the block is on their side.
   - SOLUTION PREPARED: an off-email filing pack (ready-to-paste ONLINE-PORTAL text +
     print-and-post REGISTERED-POST letters) for the ACB, Mumbai Police, NHRC, MSHRC and
     NALSA/DLSA. >>> ACTION NEEDED: these need to be submitted via the portals / by post
     (5 minutes each); each yields an acknowledgment number / postal receipt -- a stronger
     filing record than email.

D. COMPLIANCE & INTEGRITY (applied to every communication)
   - Truthful and document-based; sub-judice safe (nothing prejudges the pending case).
   - Defamation-safe: the complainant's conduct is framed as alleged / as shown by the
     documented record; we did NOT assert as fact that anyone took a bribe -- the question
     of any improper inducement behind the one-sided coverage was put to the ACB as a
     request for inquiry, not stated as fact. We did not threaten anyone's arrest.
   - GDPR/DPDP: one-click unsubscribe on bulk mail; suppression of bounced/opted-out
     addresses; no contact with the complainant.
   - A corrected fact was propagated everywhere: Mr. Thadani ONLY invited the guests and
     was not present at the time of the argument (an earlier "not present at the venue"
     phrasing was corrected).

=====================================================================
3. OUTSTANDING / RECOMMENDED NEXT STEPS
=====================================================================
1. SUBMIT the authority complaints via the ACB / Mumbai Police / NHRC online portals and
   by registered post (the pack is ready). This is the highest-priority open item.
2. PURSUE the quashing remedy (s.528 BNSS / Article 226) through counsel, Adv. Sujata
   Shirasi -- the legal community has been primed to support it.
3. MONITOR the Times of India for a correction within the 7-day window; if none, file the
   Press Council of India complaint.
4. AWAIT and triage responses from the legal allies and press.

=====================================================================
CONTACT
=====================================================================
Santosh Sakpal -- Independent Investigator (PressDetective)
+91 82689 17276 | santoshsakpal03@gmail.com
Counsel: Adv. Sujata Shirasi.

This report is confidential and prepared for the case stakeholders. The matter is
sub-judice; please keep public statements measured.
"""

m=MIMEMultipart('alternative'); m['From']=FROM_HDR; m['To']=', '.join(TO); m['Cc']=', '.join(CC)
m['Subject']=SUBJ; m['Reply-To']=FROM
m.attach(MIMEText(BODY,'plain','utf-8'))
rcpts=TO+CC
assert not any('saraf' in r.lower() for r in rcpts)
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
print('Sending case status report to', TO, 'CC', CC)
ok=False
for att in range(3):
    try:
        with smtplib.SMTP(PH,PP,timeout=40) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo(); s.login(FROM,TOKEN)
            s.sendmail(FROM,rcpts,m.as_string())
        print('  OK via Proton'); ok=True; break
    except Exception as e:
        print(f'  attempt {att+1} failed: {str(e)[:80]}')
        import time; time.sleep(6)
print('SENT' if ok else 'FAILED')
