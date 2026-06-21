#!/usr/bin/env python3
"""
send_falsecase_allies.py -- 20 June 2026
Outreach to the 89 'falsecase_allies_research_21jun2026' legal contacts (FIR-quashing
lawyers, legal press, civil-liberties NGOs, bar bodies, legal-aid, academics, HRCs).
From Santosh via Proton (fixed From). Asks for legal support / scrutiny / quashing help
and a fair investigation into the complainant's conduct. Corrected facts (Thadani only
invited guests, not present at the argument). Sub-judice safe; abuse-of-process framing;
no "arrest him" demand (reframed as lawful accountability/investigation); no bribery-as-
fact. Saraf never a recipient. List-Unsubscribe.
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
ALLIES=json.loads((ROOT/'clients/tarun-thadani/_allies.json').read_text())
assert not any('saraf' in a.lower() or 'yahoo' in a.lower() for a in ALLIES)

_ctx=ssl.create_default_context(); _ctx.check_hostname=False; _ctx.verify_mode=ssl.CERT_NONE
def proton_send(rcpts,msg,label,retries=1):
    for att in range(retries+1):
        try:
            with smtplib.SMTP(PROTON_H,PROTON_P,timeout=40) as s:
                s.ehlo(); s.starttls(context=_ctx); s.ehlo(); s.login(FROM,TOKEN)
                s.sendmail(FROM,rcpts,msg.as_string())
            print(f'  [{label}] OK via Proton ({len(rcpts)} rcpt)'); return True
        except Exception as e:
            print(f'  [{label}] attempt {att+1}: {str(e)[:70]}')
            if att<retries: time.sleep(8)
    return False

SUBJ=('Request for legal support -- apparent ABUSE OF PROCESS / fabricated non-bailable '
      'FIR 0654/2022 | a no-extortion complaint converted into a Rs 1 crore "extortion" '
      'two months later | Santosh Sakpal | '+TODAY)
BODY=f"""To:   Members of the Bar (incl. FIR-quashing counsel), the legal press, civil-liberties
      organisations, statutory legal-aid authorities, law academics and human-rights bodies
From: Santosh Sakpal, Independent Investigator | +91 82689 17276 | santoshsakpal03@gmail.com
Date: {TODAY}

Respected Sir/Madam,

I write to seek your attention, and where you are able, your assistance, in what appears
to be a textbook abuse of the criminal process: a bailable incident converted, two months
later, into a non-bailable "extortion" FIR through a materially altered complaint --
sweeping in a man who had merely hosted a gathering.

THE DOCUMENTED SEQUENCE
1. On 2 June 2022 a private gathering was held at a restaurant in Worli. Mr. Tarun Thadani
   (founder, Dharte / dharte.com) only sent out the invitations; he was NOT present at the
   time of the argument that followed.
2. Two guests argued, and the complainant, Mr. Abhishek Saraf, was slapped by Mr. Ali Asgar
   Merchant -- at its very highest an offence under Section 323 IPC (bailable).
3. The complainant's OWN first complaint (4 June 2022, online ID 23244/2022) alleged ONLY
   the slap -- no extortion, no demand of Rs 1 crore, and no mention of Mr. Thadani.
4. About two months later, FIR No. 0654/2022 was registered (Dadar PS, 13 August 2022)
   under Sections 384/385/387/506 r/w 34 IPC -- non-bailable extortion -- now alleging a
   Rs 1 crore demand and naming Mr. Thadani for the first time.
5. To the best of our knowledge no accused was examined before registration, and no call
   detail records, bank statements or CCTV -- none of which support any extortion -- were
   verified.

WHY THIS SHOULD CONCERN THE LEGAL COMMUNITY
- A bailable slap has been inflated into a non-bailable charge carrying up to ten years.
- The defining ingredient of extortion -- the demand -- is absent from the complainant's
  own first account and surfaced only two months later.
- There was no preliminary verification -- precisely the vice that State of Haryana v.
  Bhajan Lal, Arnesh Kumar, and the inherent-powers jurisdiction (now Section 528 BNSS /
  Article 226) exist to remedy.
- An innocent host, not even present at the argument, faces a fabricated non-bailable case.

HOW YOU CAN HELP
- Examine the matter and, where you are able, lend legal guidance or support toward
  quashing this FIR (Section 528 BNSS / Article 226), or point us to counsel who can;
- Bring scrutiny to this apparent abuse of process through the legal press and
  civil-liberties / human-rights fora;
- Support a fair, lawful inquiry: complaints are already before the Anti-Corruption Bureau
  and the Mumbai Police seeking investigation into how this FIR came to be registered and
  into the conduct of the complainant. We seek lawful accountability -- not trial by
  assertion -- and your expertise would help ensure the documented irregularities are
  examined.

I make no assertion of guilt, and nothing here prejudges the pending proceedings; I ask
only that these documented irregularities receive the scrutiny they warrant, so that the
process is not abused and an innocent person is not made to suffer a fabricated
non-bailable case. The full documents are available on request.

Counsel for the accused is on record in the trial court.

Yours faithfully,
Santosh Sakpal -- Independent Investigator
+91 82689 17276 | santoshsakpal03@gmail.com
B/6 Shimgyamanohar Apartments, Thane Belapur Road, Digha West, Navi Mumbai 400708
(Issued with the assistance of PressDetective | info@pressdetective.com)
To unsubscribe: email info@pressdetective.com, subject UNSUBSCRIBE."""

def chunk(l,n):
    for i in range(0,len(l),n): yield l[i:i+n]
print('='*70); print('FALSECASE ALLIES OUTREACH |',FROM_HDR); print(f'Recipients: {len(ALLIES)}'); print('='*70)
ok=n=0; failed=[]
for i,b in enumerate(chunk(ALLIES,20),1):
    n+=1
    m=MIMEMultipart('alternative'); m['From']=FROM_HDR; m['To']=FROM; m['Cc']=INFO
    m['Subject']=SUBJ; m['Reply-To']=FROM
    m['List-Unsubscribe']='<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    m.attach(MIMEText(BODY,'plain','utf-8'))
    rcpts=[FROM,INFO]+b
    if proton_send(rcpts,m,f'ALLIES {i} ({len(b)})'): ok+=1
    else: failed.append(i)
    time.sleep(6)
print('\n'+'='*70); print(f'RESULT: {ok}/{n} batches OK'+(f'  FAILED {failed}' if failed else ''))
print('Done. (verify via Bridge next)')
