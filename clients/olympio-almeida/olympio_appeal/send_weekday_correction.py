"""
Weekday correction (17 June 2026 is a WEDNESDAY, earlier emails said Tuesday).
PressDetective Proton ONLY. Goes to Gautam + the contacts that actually
delivered (excludes NIC-blocked + dead, so no fresh bounces).

    python clients/olympio-almeida/olympio_appeal/send_weekday_correction.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import json, smtplib, ssl, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
HERE  = Path(__file__).parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))
FROM_ADDR="olympio.almeida@pressdetective.com"; FROM_NAME="Olympio Almeida"
TOKEN=CREDS["accounts"]["olympio"]["token"]; CC_INFO="info@pressdetective.com"
assert FROM_ADDR.endswith("@pressdetective.com"), "PressDetective only"

def send(subject, body, bcc=None, to=None):
    m=MIMEMultipart("alternative")
    m["Subject"]=subject; m["From"]=f"{FROM_NAME} <{FROM_ADDR}>"
    m["To"]=to or FROM_ADDR; m["Cc"]=CC_INFO
    if bcc: m["Bcc"]=", ".join(bcc)
    m.attach(MIMEText(body,"plain","utf-8"))
    rc=[FROM_ADDR,CC_INFO]+(list(bcc) if bcc else ([to] if to else []))
    ctx=ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
        s.sendmail(FROM_ADDR,rc,m.as_bytes())

SIG="""

Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  ·  Press: info@pressdetective.com
"""

# ── delivered audience = cleaned minus dead minus NIC-blocked ──────────────────
aud=json.loads((HERE/"audience_14june.json").read_text())
sup=set(json.loads((HERE/"suppress_14june.json").read_text()))
gov=set(json.loads((HERE/"govpolicy_blocked.json").read_text()))
mla_valid=["sec-legi.goa@nic.in","delilahlobo.goa@gmail.com","vijaisardesai@gmail.com",
           "drdeviyarane.mla.poriem@gmail.com","mlashetye03bicholim@gmail.com",
           "pravinarlekar4pernem@gmail.com","mla.mandrem.gvs@gov.in","mla.tivim.gvs@gov.in"]
def clean(l): return [e for e in dict.fromkeys(l) if e.lower() not in sup and e.lower() not in gov]
delivered = list(dict.fromkeys(clean(aud["depts"]) + clean(mla_valid) + clean(aud["press"]+aud["other"])))
print(f"Correction audience (delivered only): {len(delivered)}")

# ── contacts correction (brief, weekday only) ─────────────────────────────────
C_SUBJ="Correction — 17 June 2026 Siolim inspection falls on a WEDNESDAY (date & time unchanged)"
C_BODY=f"""\
Dear Editor / Colleague,

A brief correction to our recent emails regarding the joint site inspection at
Gaunsawaddo, Sodiem, Siolim.

The date and time are UNCHANGED:
   17 June 2026, 11:30 AM
   (Village Panchayat Siolim-Sodiem Notice Ref. VPSS/2026-27/site insp/648)

Please note that 17 June 2026 falls on a **WEDNESDAY**. An earlier email
referred to it as "Tuesday" in error. We apologise for any confusion — kindly
go by the date, 17 June 2026.

All other details remain the same.
{SIG}
---
If you do not wish to receive further updates, reply UNSUBSCRIBE and we will remove you.
"""

print("\n[contacts] sending weekday correction (BCC batches of 45)...")
B=45; batches=[delivered[i:i+B] for i in range(0,len(delivered),B)]; ok=0
for i,b in enumerate(batches,1):
    try:
        send(C_SUBJ, C_BODY, bcc=b); print(f"  batch {i}/{len(batches)} OK ({len(b)})"); ok+=1
    except Exception as e: print(f"  batch {i}/{len(batches)} FAIL {e}")
    time.sleep(3)
print(f"  contacts: {ok}/{len(batches)} batches")

# ── Gautam correction (weekday + Sunday/video clarification) ───────────────────
G_SUBJ="Correction — inspection is WEDNESDAY 17 June (not Tuesday) + a note on the Sunday videos"
G_BODY="""\
Dear Gautam,

A quick but important correction to my earlier updates.

THE INSPECTION IS ON WEDNESDAY, 17 JUNE 2026, at 11:30 AM.
I had mistakenly written "Tuesday" in earlier emails — the DATE (17 June) was
always correct, but the weekday was wrong. It is a Wednesday. Please arrive at
the Village Panchayat Siolim-Sodiem office by 11:15 AM that day.

ON THE SUNDAY VIDEOS:
The peak-noise day is Sunday, and the last Sunday before the inspection was
14 June. My earlier note calling it "Sunday the 15th" was also a day out
(the 15th is a Monday). So:
  - If you already recorded decibel-meter videos on Sunday 14 June, that is
    exactly what we needed — please send them across.
  - If not, there is no Sunday left before Wednesday's inspection. In that case
    please capture 2-3 timestamped clips on any day this week when the courts
    are in use (evenings/weekday play), with the decibel app visible on screen,
    so we still have measured readings to table on 17 June.

Everything else stands. Apologies for the mix-up on the days.

Regards,
PressDetective
On behalf of Olympio Almeida
olympio.almeida@pressdetective.com
"""
try:
    send(G_SUBJ, G_BODY, to="gavora@gmail.com"); print("\n[Gautam] correction OK -> gavora@gmail.com")
except Exception as e: print(f"\n[Gautam] FAIL {e}")
