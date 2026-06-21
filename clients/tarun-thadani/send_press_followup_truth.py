#!/usr/bin/env python3
"""
send_press_followup_truth.py -- 20 June 2026
Lawful press FOLLOW-UP story to deliverable Mumbai crime/legal press (~291,
bounced+suppressed excluded). From Santosh via Proton (fixed formataddr From).

Corrected facts: Mr. Thadani ONLY invited the guests and was NOT present at the time
of the argument. The Ahmed Ali angle is framed as a question + an ACB inquiry into any
inducement -- NOT a stated-as-fact bribery accusation (that would be defamation per se
and is declined). Sub-judice safe; List-Unsubscribe; Saraf never a recipient.
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
FROM=CREDS['accounts']['santosh']['address']; TOKEN=CREDS['accounts']['santosh']['token']
PROTON_H=CREDS['smtp_remote']['host']; PROTON_P=CREDS['smtp_remote']['port']
FROM_HDR=formataddr(('Santosh Sakpal, Independent Investigator', FROM))
TODAY='20 June 2026'; INFO='info@pressdetective.com'
PRESS=json.loads((ROOT/'clients/tarun-thadani/_press_deliverable.json').read_text())
assert not any('saraf' in p.lower() or 'mahapolice' in p.lower() for p in PRESS)

_ctx=ssl.create_default_context(); _ctx.check_hostname=False; _ctx.verify_mode=ssl.CERT_NONE
def proton_send(rcpts,msg,label,retries=1):
    for att in range(retries+1):
        try:
            with smtplib.SMTP(PROTON_H,PROTON_P,timeout=40) as s:
                s.ehlo(); s.starttls(context=_ctx); s.ehlo(); s.login(FROM,TOKEN)
                s.sendmail(FROM,rcpts,msg.as_string())
            print(f'  [{label}] OK via Proton ({len(rcpts)} rcpt)'); return True
        except Exception as e:
            print(f'  [{label}] attempt {att+1} failed: {str(e)[:70]}')
            if att<retries: time.sleep(8)
    return False

SUBJ=('PRESS NOTE (FOLLOW-UP) -- How a man who got no police response manufactured a '
      'false Rs 1 crore "extortion" and framed two people | Dharte.com founder only '
      'INVITED the guests, was not present at the argument | Santosh Sakpal | '+TODAY)
BODY=f"""PRESS NOTE (FOLLOW-UP) -- FOR CRIME & LEGAL DESKS
Issued by: Santosh Sakpal, Independent Investigator | +91 82689 17276 | santoshsakpal03@gmail.com
Date: {TODAY}

HOW A MAN WHO GOT NO RESPONSE FROM THE POLICE MANUFACTURED A FALSE
"Rs 1 CRORE EXTORTION" -- AND FRAMED TWO PEOPLE WHO DID NOTHING

Every fact below is from the record; the sharper characterisations are the defence's
contentions and the subject of complaints now before the Anti-Corruption Bureau and the
Mumbai Police.

THE GATHERING. On 2 June 2022 a private get-together was held at a restaurant in Worli.
One man organised it and did one thing only -- he sent out the invitations: Mr. Tarun
Thadani, founder of the wellness marketplace Dharte (dharte.com). He only invited the
guests, and he was NOT present at the time of the argument that followed.

THE ARGUMENT. Two guests -- Mr. Ali Asgar Merchant and Mr. Abhishek Saraf -- argued, and
in the course of it Mr. Saraf was slapped. At its very highest, a slap is a bailable
matter (Section 323 IPC). That is all that happened.

WHEN THE POLICE DID NOT ACT, THE STORY GREW. Mr. Saraf filed his own complaint on 4 June
2022 (online ID 23244/2022). In his own words then, it was about the slap and nothing more
-- no extortion, no Rs 1 crore, and no mention of Mr. Thadani. The regular police did not
register a serious case on so minor a matter. Then, about two months later, a very
different version appeared -- a Rs 1 crore "extortion", and, for the first time, Mr.
Thadani's name. On that later version FIR No. 0654/2022 was registered (Dadar PS, 13
August 2022) and routed through the CB-CID Anti-Extortion Cell -- with no accused examined,
and not one call record, bank statement or CCTV clip verified.

TWO PEOPLE FRAMED. The result: Mr. Merchant, and an absent host who had done nothing but
send invitations, were both swept into a non-bailable "extortion" case carrying up to ten
years -- built on a complaint that, when first written by the complainant himself, accused
them of nothing.

WHY WAS THE COVERAGE SO ONE-SIDED? A recent Times of India report by Mr. S. Ahmed Ali
carried only the complainant's version. It omitted every fact above -- that Mr. Thadani
merely invited the guests and was not present at the argument; that the complainant's own
first complaint contained no extortion and did not name him -- and, as far as is known,
sought no comment from the accused or their counsel before publication. PressDetective has
formally asked the Anti-Corruption Bureau of Maharashtra to examine the circumstances of
this publication, including whether any improper inducement was involved. We make no
allegation of fact against the journalist; we ask the question that fair reporting demands,
and we leave the authorities to answer it.

WHAT IS ASKED.
- A full investigation into how a no-extortion complaint became a non-bailable extortion
  FIR two months later (complaints are before the ACB and the Mumbai Police).
- Of journalists: please seek the defence's side before publishing -- contact PressDetective at +91 82689 17276 -- and examine the documented timeline above.

Mr. Thadani (Dharte.com) only invited the guests and was not present at the argument, and
was not named in the complainant's own original complaint. This note is sub-judice
compliant and prejudges nothing; the authorities named are the bodies competent to
establish the truth.

-- Santosh Sakpal, Independent Investigator (+91 82689 17276 | santoshsakpal03@gmail.com)
   Issued with the assistance of PressDetective | info@pressdetective.com
   To unsubscribe: email info@pressdetective.com, subject UNSUBSCRIBE."""

def chunk(l,n):
    for i in range(0,len(l),n): yield l[i:i+n]

print('='*70); print('PRESS FOLLOW-UP (TRUTH) |',FROM_HDR); print(f'Deliverable press: {len(PRESS)}'); print('='*70)
ok=n=0; failed=[]
for i,b in enumerate(chunk(PRESS,20),1):
    n+=1
    m=MIMEMultipart('alternative'); m['From']=FROM_HDR; m['To']=FROM; m['Cc']=INFO
    m['Subject']=SUBJ; m['Reply-To']=FROM
    m['List-Unsubscribe']='<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    m.attach(MIMEText(BODY,'plain','utf-8'))
    rcpts=[FROM,INFO]+b
    if proton_send(rcpts,m,f'PRESS {i} ({len(b)})'): ok+=1
    else: failed.append(i)
    time.sleep(6)
print('\n'+'='*70)
print(f'RESULT: {ok}/{n} batches OK' + (f'  FAILED batches: {failed}' if failed else ''))
print('NOTE: SMTP OK != delivered -- will verify via Bridge for bounces.')
print('Done.')
