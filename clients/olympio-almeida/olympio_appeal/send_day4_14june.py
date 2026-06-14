"""
Day 4 (Saturday 14 June 2026) — Olympio Almeida / Sunday Racquet Club campaign.
T-minus 3 days to the 17 June inspection; TOMORROW (Sun 15 June) is peak-noise day.

Sends, all signed by Olympio, all CC info@pressdetective.com:
  A. Departments (43 official .gov.in/.nic.in/gspcb.in) — depute a rep for 17 June + official response
  B. All Goa press + civic allies (~234) — request for comments + Sunday "hear it yourself"
  C. MLAs (19) — request their public position / to attend or depute + comment
  D. Gautam — full Day 4 update (anonymous; only as direct recipient, never named)

Provider: Proton remote SMTP (smtp.protonmail.ch) with Mailtrap fallback per send.
Run from repo root: python clients/olympio-almeida/olympio_appeal/send_day4_14june.py
"""

import json, smtplib, ssl, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))
HERE  = Path(__file__).parent

FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"
MT        = CREDS["smtp_mailtrap"]

# ── audience ──────────────────────────────────────────────────────────────────
aud   = json.loads((HERE / "audience_14june.json").read_text(encoding="utf-8"))
mlas  = list(dict.fromkeys(aud["mlas"]))
depts = [e for e in dict.fromkeys(aud["depts"]) if e != "mlasil.gvs@gov.in"]
if "mlasil.gvs@gov.in" not in mlas:
    mlas.append("mlasil.gvs@gov.in")
press = list(dict.fromkeys(aud["press"]))
other = list(dict.fromkeys(aud["other"]))
# comment-request audience = all press + civic allies (NOT departments, NOT MLAs)
press_blast = list(dict.fromkeys(press + other))

print(f"Audience: depts={len(depts)}  MLAs={len(mlas)}  press+civic={len(press_blast)}")

# ── send (Proton remote, Mailtrap fallback) ───────────────────────────────────
def _rcpts(msg):
    out = []
    for hdr in ("To", "Cc", "Bcc"):
        v = msg.get(hdr, "")
        if v:
            out += [a.strip() for a in v.split(",") if a.strip()]
    return out

def send(msg):
    rcpts = _rcpts(msg)
    raw = msg.as_bytes()
    ctx = ssl.create_default_context()
    # primary: Proton remote
    try:
        with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
            s.sendmail(FROM_ADDR, rcpts, raw)
        return "proton"
    except Exception as e1:
        # fallback: Mailtrap
        try:
            with smtplib.SMTP(MT["host"], MT["port"], timeout=30) as s:
                s.ehlo(); s.starttls(context=ctx); s.login(MT["user"], MT["token"])
                s.sendmail(FROM_ADDR, rcpts, raw)
            return "mailtrap"
        except Exception as e2:
            raise RuntimeError(f"proton:{e1} | mailtrap:{e2}")

def build(subject, body, to=None, cc=None, bcc=None):
    m = MIMEMultipart("alternative")
    m["Subject"] = subject
    m["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    m["To"]      = to or FROM_ADDR
    m["Cc"]      = cc or CC_INFO
    if bcc:
        m["Bcc"] = ", ".join(bcc)
    m.attach(MIMEText(body, "plain", "utf-8"))
    return m

SIG = """\

Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com
Press coordination: info@pressdetective.com
"""

# ══════════════════════════════════════════════════════════════════════════════
# SEND A — DEPARTMENTS
# ══════════════════════════════════════════════════════════════════════════════
A_SUBJ = ("Pre-Inspection Notice — Please Depute Your Representative for "
          "17 June 2026 Joint Site Inspection, Siolim (3 days away)")

A_BODY = f"""\
To the Heads of the concerned Departments,
(Goa State Pollution Control Board · Collector, North Goa · Town & Country
Planning · Directorate of Panchayats · Land Revenue / Land Records ·
BDO Bardez · Superintendent of Police, North Goa · Siolim Police)

Subject: Joint site inspection on Tuesday, 17 June 2026 at 11:30 AM —
Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim — request to depute a
representative and to place your department's response on record.

Respected Sir / Madam,

This is a formal follow-up ahead of the joint site inspection scheduled by
Village Panchayat Siolim-Sodiem (Notice Ref. VPSS/2026-27/site insp/648
dated 08 June 2026) for Tuesday, 17 June 2026 at 11:30 AM at the disputed
site.

The matter concerns the "Sunday Racquet and Social Club" operating outdoor
padel courts at House No. 47/3, Gaunsawaddo, Sodiem, Siolim, in a residential
zone — with measured noise of 68-75 dB(A) against the 55 dB(A) residential
limit, encroachment on adjoining private land, and a 2008 Panchayat order
that revoked a licence on the same plot (Sy. No. 197/7).

I respectfully request each concerned department to:

  1. DEPUTE an officer to attend the joint inspection on 17 June 2026, so
     that land-use, noise, encroachment and licensing questions can be
     examined together rather than in isolation.

  2. CARRY the relevant departmental record to the inspection —
     • GSPCB: consent-to-operate status and any prior noise readings;
     • TCP / Panchayat: land-use classification and building/occupancy permissions;
     • Land Revenue / Records: survey position of Sy. No. 197/7 and 197/A;
     • Police: any prior complaints registered at Siolim PS.

  3. PLACE ON RECORD your department's response to the original complaint
     filed with GSPCB on 9 March 2026, which has not yet been answered.

A separate technical letter has already been sent to GSPCB requesting the use
of Class 1 / Class 2 calibrated sound-level meters and an unannounced
follow-up reading on a Sunday (when the courts are at peak use). I would be
grateful if the inspecting team would keep that request in view.

The residents — several of them senior citizens — have waited three months
for action. Your department's presence on 17 June will help bring this to a
fair and documented conclusion.
{SIG}"""

# ══════════════════════════════════════════════════════════════════════════════
# SEND B — ALL PRESS + CIVIC ALLIES (request for comments)
# ══════════════════════════════════════════════════════════════════════════════
B_SUBJ = ("Request for Your Comments — Sunday Racquet Club Noise, Siolim · "
          "Hear It Yourself TOMORROW (Sun 15 June) · Inspection Tue 17 June")

B_BODY = f"""\
Dear Editor / Colleague,

Ahead of the official joint inspection this Tuesday, I am writing to invite
your comments, coverage, or an on-record statement on a public-interest
environmental matter in Siolim, North Goa.

THE STORY IN ONE LINE
The "Sunday Racquet and Social Club" runs outdoor padel courts at House
No. 47/3, Gaunsawaddo, Sodiem, Siolim — in a residential zone, ~30-40 ft
from senior citizens' homes — generating 68-75 dB(A) against the 55 dB(A)
residential limit, with encroachment on private land and a 2008 Panchayat
licence-revocation on the very same plot (Sy. No. 197/7).

TOMORROW — SUNDAY 15 JUNE, 9 AM - 7 PM — HEAR IT YOURSELF
Sunday is peak operating day. We invite any journalist or photographer to
come to Gaunsawaddo tomorrow between 9 AM and 7 PM and hear the noise
firsthand. Bring a smartphone — a free decibel-meter app (NIOSH SLM,
Decibel X) gives an instant reading. Residents will be available to speak
on record.

TUESDAY 17 JUNE, 11:30 AM — OFFICIAL JOINT INSPECTION
Village Panchayat Siolim-Sodiem has scheduled a joint site inspection with
the Goa State Pollution Control Board (Notice Ref. VPSS/2026-27/site insp/648).
GSPCB, the Collector (North Goa), TCP, Police and area MLAs have all been
formally asked to attend. Media are welcome to observe.

WHAT WE ARE ASKING OF YOU
  • Your comment or editorial view on commercial noise in residential Goa;
  • Coverage of tomorrow's site visit and/or Tuesday's inspection;
  • If you wish, put questions to us or to the authorities on record.

A 26-page evidence packet (noise readings, photographs, the 2008 order and
the March 2026 complaint) is available on request by return email.

This is a story about ordinary residents, many of them elderly, asking only
that the law on noise and land-use be applied. We would value your voice.
{SIG}
---
If you do not wish to receive further updates on this matter, reply with the
word UNSUBSCRIBE and we will remove you from the list immediately.
"""

# ══════════════════════════════════════════════════════════════════════════════
# SEND C — MLAs (request public position + comment)
# ══════════════════════════════════════════════════════════════════════════════
C_SUBJ = ("Request to Honourable MLAs — Your Position & Presence at the "
          "17 June Siolim Noise/Encroachment Inspection")

C_BODY = f"""\
To the Honourable Members of the Goa Legislative Assembly,

Subject: Request for your public position and your presence (or a deputed
representative) at the joint site inspection on 17 June 2026, Siolim.

Respected Sir / Madam,

I write as a senior-citizen resident of La Masseria, Siolim, on behalf of
neighbours affected by the "Sunday Racquet and Social Club" — outdoor padel
courts at Gaunsawaddo, Sodiem, Siolim, operating in a residential zone with
measured noise of 68-75 dB(A) against the 55 dB(A) limit, encroachment on
private land, and a 2008 Panchayat licence-revocation on the same plot
(Sy. No. 197/7).

Village Panchayat Siolim-Sodiem has scheduled a joint inspection with the
Goa State Pollution Control Board for Tuesday, 17 June 2026 at 11:30 AM.

As our elected representatives, I respectfully request you to:

  1. STATE YOUR POSITION on the enforcement of the Noise Pollution Rules 2000
     and land-use law in residential Goa — we would be glad to share your
     comment with residents and the press.

  2. ATTEND, or depute a representative to, the 17 June inspection so that the
     residents' concerns are heard at the political as well as the
     administrative level.

  3. RAISE the matter, if you see fit, with the GSPCB and the Collector,
     North Goa, so that the long-pending complaint (filed 9 March 2026) is
     finally answered.

Tomorrow, Sunday 15 June, the courts will be at peak use between 9 AM and
7 PM — you or your office are most welcome to visit Gaunsawaddo and hear the
situation directly.

Your voice on this would mean a great deal to families who have waited three
months for a response.
{SIG}"""

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTE
# ══════════════════════════════════════════════════════════════════════════════
results = {}

# A — Departments (single BCC send)
print("\n[A] Departments...")
try:
    via = send(build(A_SUBJ, A_BODY, bcc=depts))
    print(f"  Departments ({len(depts)}) — OK via {via}")
    results["A_departments"] = f"OK ({len(depts)}) via {via}"
except Exception as e:
    print(f"  Departments — FAILED: {e}")
    results["A_departments"] = f"FAILED: {e}"
time.sleep(3)

# B — Press + civic (BCC batches of 45)
print("\n[B] Press + civic comment request...")
BATCH = 45
batches = [press_blast[i:i+BATCH] for i in range(0, len(press_blast), BATCH)]
bok = 0
for i, b in enumerate(batches, 1):
    try:
        via = send(build(B_SUBJ, B_BODY, bcc=b))
        print(f"  Batch {i}/{len(batches)} ({len(b)}) — OK via {via}")
        bok += 1
    except Exception as e:
        print(f"  Batch {i}/{len(batches)} — FAILED: {e}")
    time.sleep(3)
results["B_press"] = f"{bok}/{len(batches)} batches OK, {len(press_blast)} recipients"

# C — MLAs (single send, BCC)
print("\n[C] MLAs...")
try:
    via = send(build(C_SUBJ, C_BODY, bcc=mlas))
    print(f"  MLAs ({len(mlas)}) — OK via {via}")
    results["C_mlas"] = f"OK ({len(mlas)}) via {via}"
except Exception as e:
    print(f"  MLAs — FAILED: {e}")
    results["C_mlas"] = f"FAILED: {e}"
time.sleep(3)

print("\n=== SUMMARY ===")
for k, v in results.items():
    print(f"  {k}: {v}")

# save run log
(HERE / "day4_run_log.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print("\nSaved day4_run_log.json")
