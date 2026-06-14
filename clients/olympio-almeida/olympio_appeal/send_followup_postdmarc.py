"""
Pre-inspection FOLLOW-UP to all cleaned contacts — PressDetective Proton ONLY.
Sent after the DMARC duplicate was removed (govt mail now authenticates).

HARD SCOPE: PressDetective only. FROM olympio.almeida@pressdetective.com via
smtp.protonmail.ch (PressDetective's own Proton token). NEVER any Dharte
sender / address / token. CC info@pressdetective.com on everything.

No "your earlier mail failed" language — this is a clean final reminder.

Segments:
  1. Departments (official, cleaned)        -> attend/depute the 17 June inspection
  2. MLAs (valid + Secretariat sec-legi)    -> position + attend/depute
  3. Press + civic (cleaned)                -> coverage + Sunday "hear it yourself"
  4. Gautam                                 -> internal report

    python clients/olympio-almeida/olympio_appeal/send_followup_postdmarc.py
"""
import json, smtplib, ssl, sys, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
HERE  = Path(__file__).parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

# ── PressDetective Proton ONLY ────────────────────────────────────────────────
FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"
assert FROM_ADDR.endswith("@pressdetective.com"), "scope guard: PressDetective only"

# ── safety: refuse if DMARC not fixed (don't re-bounce govt) ───────────────────
try:
    import dns.resolver
    recs = [r.to_text() for r in dns.resolver.resolve("_dmarc.pressdetective.com", "TXT")]
    n = sum(1 for x in recs if x.replace('" "','').strip('"').lstrip().startswith("v=DMARC1"))
    if n != 1:
        print(f"ABORT — DMARC has {n} records (need 1). Fix DNS before sending to govt.")
        sys.exit(1)
except Exception as e:
    print(f"WARN — could not verify DMARC ({e}); continuing (press/civic deliver regardless).")

# ── audience (cleaned) ────────────────────────────────────────────────────────
aud  = json.loads((HERE / "audience_14june.json").read_text())
sup  = set(json.loads((HERE / "suppress_14june.json").read_text()))   # confirmed dead -> exclude

def clean(lst): return [e for e in dict.fromkeys(lst) if e.lower() not in sup]

depts = clean(aud["depts"])
mlas_valid = ["sec-legi.goa@nic.in",          # Goa Legislature Secretariat (official MLA route)
              "delilahlobo.goa@gmail.com",     # Siolim — the jurisdiction MLA
              "vijaisardesai@gmail.com","vijaisardesai.goa@gmail.com",
              "drdeviyarane.mla.poriem@gmail.com","mlashetye03bicholim@gmail.com",
              "pravinarlekar4pernem@gmail.com",
              "mla.mandrem.gvs@gov.in","mla.tivim.gvs@gov.in"]
mlas  = clean(mlas_valid)
press = clean(aud["press"] + aud["other"])

print(f"Audience (cleaned): depts={len(depts)} mlas={len(mlas)} press+civic={len(press)}")

# ── send helper (PressDetective Proton remote) ────────────────────────────────
def send(subject, body, bcc):
    m = MIMEMultipart("alternative")
    m["Subject"] = subject
    m["From"] = f"{FROM_NAME} <{FROM_ADDR}>"
    m["To"]   = FROM_ADDR
    m["Cc"]   = CC_INFO
    m["Bcc"]  = ", ".join(bcc)
    m.attach(MIMEText(body, "plain", "utf-8"))
    rcpts = [FROM_ADDR, CC_INFO] + list(bcc)
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, m.as_bytes())

SIG = """

Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  ·  Press: info@pressdetective.com
"""

DEPT_SUBJ = "Reminder — Joint Site Inspection Tuesday 17 June 2026, 11:30 AM, Siolim (please depute a representative)"
DEPT_BODY = f"""\
To the concerned Department,

This is a reminder ahead of the joint site inspection scheduled by Village
Panchayat Siolim-Sodiem (Notice Ref. VPSS/2026-27/site insp/648 dated
08 June 2026) for TUESDAY, 17 JUNE 2026 at 11:30 AM, at Survey No. 197/7,
Gaunsawaddo, Sodiem, Siolim.

The matter: the "Sunday Racquet and Social Club" runs outdoor padel courts in
a residential zone — measured noise of 68-75 dB(A) against the 55 dB(A) limit,
encroachment on adjoining private land, and a 2008 Panchayat order revoking a
licence on the same plot. A complaint filed with GSPCB on 9 March 2026 remains
unanswered.

We respectfully request your department to:
  1. Depute an officer to attend the inspection on 17 June 2026.
  2. Bring the relevant departmental record (consent-to-operate / land-use /
     survey position / prior complaints, as applicable).
  3. Place your department's response to the 9 March complaint on record.

GSPCB has separately been asked to use calibrated meters and to take an
unannounced Sunday reading (when the courts are at peak use).
{SIG}"""

MLA_SUBJ = "Reminder — 17 June Siolim Inspection: your position & presence requested"
MLA_BODY = f"""\
To the Honourable Member of the Goa Legislative Assembly
(and the Goa Legislature Secretariat, for circulation to Members),

A joint inspection with the Goa State Pollution Control Board is scheduled for
TUESDAY, 17 JUNE 2026 at 11:30 AM at Gaunsawaddo, Sodiem, Siolim, concerning
the "Sunday Racquet and Social Club" — outdoor padel courts in a residential
zone (68-75 dB(A) vs the 55 dB(A) limit), encroachment, and a 2008 Panchayat
licence-revocation on the same plot.

As our elected representatives, we respectfully request you to (1) state your
position on enforcement of the Noise Pollution Rules 2000 and land-use law,
(2) attend or depute a representative to the 17 June inspection, and (3) raise
the long-pending complaint (9 March 2026) with GSPCB and the Collector, North Goa.
{SIG}"""

PRESS_SUBJ = "Tomorrow (Sun 15 June) hear it yourself · Inspection Tue 17 June — Sunday Racquet Club noise, Siolim"
PRESS_BODY = f"""\
Dear Editor / Colleague,

A brief reminder on the Siolim noise/encroachment story ahead of this week's
official inspection.

TOMORROW — SUNDAY 15 JUNE, 9 AM - 7 PM — HEAR IT YOURSELF
The "Sunday Racquet and Social Club" runs outdoor padel courts at Gaunsawaddo,
Sodiem, Siolim, in a residential zone ~30-40 ft from senior citizens' homes.
Sunday is peak day; residents measure 68-75 dB(A) against the 55 dB(A) limit.
Come to Gaunsawaddo tomorrow and hear it firsthand — a free phone decibel app
(NIOSH SLM, Decibel X) gives an instant reading. Residents will speak on record.

TUESDAY 17 JUNE, 11:30 AM — OFFICIAL JOINT INSPECTION
Village Panchayat Siolim-Sodiem + the Goa State Pollution Control Board, at
Survey No. 197/7. GSPCB, the Collector (North Goa), TCP, Police and area MLAs
have been asked to attend. Media are welcome to observe.

A 26-page evidence packet (noise readings, photographs, the 2008 order, the
March 2026 complaint) is available on request by return email.
{SIG}
---
If you do not wish to receive further updates on this matter, reply UNSUBSCRIBE
and we will remove you immediately.
"""

# ── execute ───────────────────────────────────────────────────────────────────
log = {}
print("\n[1] Departments...")
try:
    send(DEPT_SUBJ, DEPT_BODY, depts); print(f"  OK ({len(depts)})"); log["depts"]=f"OK {len(depts)}"
except Exception as e: print(f"  FAIL {e}"); log["depts"]=f"FAIL {e}"
time.sleep(3)

print("[2] MLAs...")
try:
    send(MLA_SUBJ, MLA_BODY, mlas); print(f"  OK ({len(mlas)})"); log["mlas"]=f"OK {len(mlas)}"
except Exception as e: print(f"  FAIL {e}"); log["mlas"]=f"FAIL {e}"
time.sleep(3)

print("[3] Press + civic (BCC batches of 45)...")
B=45; batches=[press[i:i+B] for i in range(0,len(press),B)]; ok=0
for i,b in enumerate(batches,1):
    try:
        send(PRESS_SUBJ, PRESS_BODY, b); print(f"  batch {i}/{len(batches)} OK ({len(b)})"); ok+=1
    except Exception as e: print(f"  batch {i}/{len(batches)} FAIL {e}")
    time.sleep(3)
log["press"]=f"{ok}/{len(batches)} batches, {len(press)} recipients"

(HERE/"followup_postdmarc_log.json").write_text(json.dumps(log,indent=2))
print("\nSummary:", json.dumps(log, indent=2))
print("Saved followup_postdmarc_log.json")
