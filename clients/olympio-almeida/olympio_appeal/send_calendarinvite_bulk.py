"""
Bulk calendar invite (.ics) to all Goa press + relevant departments.
TOMORROW: Wednesday 17 June 2026, 11:30 AM
Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

Segments:
  1. Departments (depts + civic "other" with official gmail contacts)  -- one batch
  2. Press (press list, cleaned, BCC batches of 45)

PressDetective Proton ONLY.

    python clients/olympio-almeida/olympio_appeal/send_calendarinvite_bulk.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import json, smtplib, ssl, uuid, time, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
HERE  = Path(__file__).parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))
FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"
assert FROM_ADDR.endswith("@pressdetective.com")

# ── audience ──────────────────────────────────────────────────────────────────
aud = json.loads((HERE / "audience_14june.json").read_text())
sup = set(e.lower() for e in json.loads((HERE / "suppress_14june.json").read_text()))

def clean(lst):
    return [e for e in dict.fromkeys(lst) if e.lower() not in sup]

depts_list = clean(aud["depts"])
other_list = clean(aud["other"])
press_list = clean(aud["press"])

# Departments + civic/official other combined (VP, GSPCB gmail, NGOs etc.)
dept_audience = list(dict.fromkeys(depts_list + other_list))
print(f"Audience: depts+civic={len(dept_audience)}  press={len(press_list)}")

# ── iCalendar (.ics) ───────────────────────────────────────────────────────────
DTSTART = "20260617T060000Z"   # 11:30 AM IST
DTEND   = "20260617T080000Z"   # 1:30 PM IST
DTSTAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
UID     = str(uuid.uuid4())

ICS = "\r\n".join([
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//PressDetective//Olympio Almeida//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:REQUEST",
    "BEGIN:VEVENT",
    f"UID:{UID}",
    f"DTSTAMP:{DTSTAMP}",
    f"DTSTART:{DTSTART}",
    f"DTEND:{DTEND}",
    "SUMMARY:Joint Site Inspection - Siolim Padel Courts (Wednesday 17 June 2026)",
    "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
    "DESCRIPTION:Joint site inspection called by Village Panchayat Siolim-Sodiem"
    " (Notice Ref. VPSS/2026-27/site insp/648\\, 08 June 2026).\\n\\n"
    "Matter: Sunday Racquet and Social Club -- outdoor padel courts at"
    " House No. 47/3\\, Gaunsawaddo\\, Sodiem\\, Siolim (Survey No. 197/7)."
    " Noise: 68-75 dB(A) vs 55 dB(A) limit. GSPCB complaint filed 9 March 2026.\\n\\n"
    "Departments: GSPCB\\, Collector North Goa\\, TCP\\, BDO Bardez\\, Police notified.\\n"
    "Arrive by 11:15 AM. Media welcome to observe.",
    f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
    "STATUS:CONFIRMED",
    "SEQUENCE:0",
    "BEGIN:VALARM",
    "TRIGGER:-PT120M",
    "ACTION:DISPLAY",
    "DESCRIPTION:Inspection in 2 hours",
    "END:VALARM",
    "BEGIN:VALARM",
    "TRIGGER:-PT30M",
    "ACTION:DISPLAY",
    "DESCRIPTION:Inspection in 30 minutes",
    "END:VALARM",
    "END:VEVENT",
    "END:VCALENDAR",
])

def make_ics_part():
    part = MIMEBase("text", "calendar", method="REQUEST", charset="utf-8")
    part.set_payload(ICS.encode("utf-8"))
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment",
                    filename="inspection_17june2026.ics")
    return part

# ── send helper ───────────────────────────────────────────────────────────────
def send_batch(subject, body, bcc=None, to=None):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = to or FROM_ADDR
    msg["Cc"]      = CC_INFO
    if bcc:
        msg["Bcc"] = ", ".join(bcc)
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(make_ics_part())
    rcpts = [msg["To"], CC_INFO] + (list(bcc) if bcc else [])
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())

# ── body templates ────────────────────────────────────────────────────────────
SIG = """
Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  ·  Press: info@pressdetective.com
"""

DEPT_SUBJ = "TOMORROW — Joint Site Inspection 11:30 AM Wednesday 17 June 2026 | Siolim Padel Courts [Calendar Invite Attached]"
DEPT_BODY = f"""\
To the concerned Department / Office,

A calendar invite is attached for the joint site inspection TOMORROW.

  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM (please arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

This inspection was called by the Village Panchayat Siolim-Sodiem
(Notice Ref. VPSS/2026-27/site insp/648, dated 08 June 2026) regarding
the "Sunday Racquet and Social Club" — outdoor padel courts at
House No. 47/3, Gaunsawaddo, Sodiem, Siolim — operating in a residential
zone with measured noise of 68-75 dB(A) against the 55 dB(A) limit.

Your department has been formally requested to:
  1. Depute a representative to attend tomorrow's inspection.
  2. Bring the relevant departmental record.
  3. Place your response to the 9 March 2026 GSPCB complaint on record.

Please click "Add to Calendar" on the attached .ics file to save the event.
{SIG}"""

PRESS_SUBJ = "TOMORROW 11:30 AM — Siolim Padel Court Inspection | Wednesday 17 June [Calendar Invite]"
PRESS_BODY = f"""\
Dear Editor / Colleague,

A calendar invite is attached for tomorrow's official joint inspection.

  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat Siolim-Sodiem + Goa State Pollution Control Board
will conduct a joint inspection of the "Sunday Racquet and Social Club"
padel courts at Gaunsawaddo, Sodiem — operating in a residential zone
with noise readings of 68-75 dB(A) against the 55 dB(A) limit.
A 2008 Panchayat licence-revocation on the same plot has not been enforced.

Media are welcome to observe. A 26-page evidence packet (noise readings,
photographs, the 2008 order, March 2026 GSPCB complaint) is available
on request by return email.

Click "Add to Calendar" on the attached .ics to save the event with reminders.
{SIG}
---
If you do not wish to receive further updates, reply UNSUBSCRIBE.
"""

# ── 1. Departments + civic (one BCC batch) ───────────────────────────────────
print(f"\n[1] Departments + civic ({len(dept_audience)} addresses)...")
B = 45
dept_batches = [dept_audience[i:i+B] for i in range(0, len(dept_audience), B)]
dept_ok = 0
for i, b in enumerate(dept_batches, 1):
    try:
        send_batch(DEPT_SUBJ, DEPT_BODY, bcc=b)
        print(f"  batch {i}/{len(dept_batches)} OK ({len(b)})")
        dept_ok += 1
    except Exception as e:
        print(f"  batch {i}/{len(dept_batches)} FAIL: {e}")
    time.sleep(3)

# ── 2. Press (BCC batches of 45) ─────────────────────────────────────────────
print(f"\n[2] Press ({len(press_list)} addresses, BCC batches of 45)...")
press_batches = [press_list[i:i+B] for i in range(0, len(press_list), B)]
press_ok = 0
for i, b in enumerate(press_batches, 1):
    try:
        send_batch(PRESS_SUBJ, PRESS_BODY, bcc=b)
        print(f"  batch {i}/{len(press_batches)} OK ({len(b)})")
        press_ok += 1
    except Exception as e:
        print(f"  batch {i}/{len(press_batches)} FAIL: {e}")
    time.sleep(3)

print(f"\nDone. Depts+civic: {dept_ok}/{len(dept_batches)} batches | Press: {press_ok}/{len(press_batches)} batches")
print(f"Total attempted: {len(dept_audience)} depts/civic + {len(press_list)} press")
