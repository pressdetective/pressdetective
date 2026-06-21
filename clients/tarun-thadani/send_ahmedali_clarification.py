#!/usr/bin/env python3
"""
send_ahmedali_clarification.py -- 20 June 2026
Narrative clarification + reiterated right-of-reply to S. Ahmed Ali + ToI desks.
Corrects our own earlier wording: NOT "absent from the venue" but "only invited the
guests and was not present at the time of the argument". From Santosh via Proton.
Lawful framing retained (no arrest threat, no bribery-as-fact).
"""
import smtplib, ssl, json, sys
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
FROM=CREDS['accounts']['santosh']['address']; TOKEN=CREDS['accounts']['santosh']['token']
PROTON_H=CREDS['smtp_remote']['host']; PROTON_P=CREDS['smtp_remote']['port']
FROM_HDR=formataddr(('Santosh Sakpal, Independent Investigator', FROM))
TODAY='20 June 2026'

INFO='info@pressdetective.com'; AHMED='ahmed.ali@timesgroup.com'
CC=['editor@timesgroup.com','mumbai.letters@timesgroup.com','mumbai.crime@timesgroup.com', INFO]
assert 'saraf' not in (AHMED+''.join(CC)).lower()

SUBJ=('CLARIFICATION & RIGHT OF REPLY -- FIR 0654/2022 | Mr. Tarun Thadani only '
      'INVITED the guests and was NOT present at the time of the argument | '
      'Correction requested within 7 days | '+TODAY)

BODY=f"""To,   Mr. S. Ahmed Ali, Senior Assistant Editor, The Times of India, Mumbai
CC:   The Editor, Times of India (Mumbai); ToI Mumbai City/Crime Desk; PressDetective
Date: {TODAY}

Dear Mr. Ahmed Ali,

Further to my notice of today's date, and to state the position precisely, let me set
out the actual story behind FIR No. 0654/2022 -- the story your report left out.

THE GATHERING
On 2 June 2022 a private get-together was held at a restaurant in Worli. The person who
organised it did one thing and one thing only: he sent out the invitations. That person
is Mr. Tarun Thadani, founder of the wellness marketplace Dharte (dharte.com). His
involvement began and ended with inviting people to a social evening.

THE ARGUMENT -- WHICH HE WAS NOT PART OF
What happened later had nothing to do with him. An argument broke out between two of the
guests -- Mr. Ali Asgar Merchant and the complainant, Mr. Abhishek Saraf -- and in the
course of it Mr. Saraf was slapped. Mr. Thadani was NOT present at the time of the
argument and played no part in it. A slap, at its very highest, is a bailable matter
(Section 323 IPC).

THE COMPLAINT THAT KEPT CHANGING
Two days later, on 4 June 2022, Mr. Saraf filed his own complaint (online ID 23244/2022).
In his own words then, it was about the slap and nothing more -- no extortion, no demand
for Rs 1 crore, and no mention of Mr. Thadani. It was only about two months later that a
very different version surfaced: a Rs 1 crore "extortion", and, for the first time, Mr.
Thadani's name. FIR No. 0654/2022 was registered on that later version -- with no accused
examined, and not a single call record, bank statement or CCTV clip checked.

THE POINT YOUR READERS DESERVE TO KNOW
A man who did nothing but invite guests to a gathering -- and who was not even present
when the argument happened -- has been swept into a non-bailable "extortion" case built
on a complaint that, when first written, accused him of nothing.

WHAT I ASK
I reiterate, within 7 days: (a) a correction carrying these facts with the same
prominence; (b) a right of reply for the accused and their counsel
; and (c) that the article be taken down or annotated pending
correction. I will gladly share the underlying documents.

Failing a fair correction, the affected parties reserve all lawful remedies, including a
complaint for criminal defamation (Section 356, Bharatiya Nyaya Sanhita) and a complaint
to the Press Council of India. Formal complaints concerning this matter are already
before the Anti-Corruption Bureau of Maharashtra and the Mumbai Police.

This communication is sub-judice compliant and prejudges nothing; it seeks only accurate,
balanced reporting and the accused's right of reply.

Yours faithfully,
Santosh Sakpal
Independent Investigator
Phone   : +91 82689 17276 | Email: santoshsakpal03@gmail.com
Address : B/6 Shimgyamanohar Apartments, Thane Belapur Road, Digha West, Navi Mumbai 400708
Date    : {TODAY}   (Submitted with the assistance of PressDetective | info@pressdetective.com)
"""

m=MIMEMultipart('alternative'); m['From']=FROM_HDR; m['To']=AHMED; m['Cc']=', '.join(CC)
m['Subject']=SUBJ; m['Reply-To']=FROM
m.attach(MIMEText(BODY,'plain','utf-8'))
rcpts=[AHMED]+CC
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
print('Sending clarification (story) to Ahmed Ali + ToI desks ...')
try:
    with smtplib.SMTP(PROTON_H,PROTON_P,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.ehlo(); s.login(FROM,TOKEN)
        s.sendmail(FROM,rcpts,m.as_string())
    print(f'  OK via Proton ({len(rcpts)} rcpt):', ', '.join(rcpts))
except Exception as e:
    print('  FAIL:', str(e)[:160])
print('Done. (will verify via Bridge)')
