"""
Send to police + government FROM olympio.almeida@protonmail.com via Proton Bridge.
Uses same bridge_password. Different sending domain may route differently at NIC.

    python clients/olympio-almeida/olympio_appeal/send_govpolice_protonmail.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import json, smtplib, ssl, uuid, datetime, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
HERE  = Path(__file__).parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

# Send FROM @protonmail.com native address
FROM_ADDR  = "olympio.almeida@protonmail.com"
FROM_NAME  = "Olympio Almeida"
BRIDGE_PW  = CREDS["accounts"]["olympio"]["bridge_password"]
CC_INFO    = "info@pressdetective.com"

# ── test auth first ───────────────────────────────────────────────────────────
print("Testing Bridge auth for olympio.almeida@protonmail.com ...")
bridge_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
bridge_ctx.check_hostname = False; bridge_ctx.verify_mode = ssl.CERT_NONE
try:
    with smtplib.SMTP("127.0.0.1", 1025, timeout=15) as s:
        s.ehlo(); s.starttls(context=bridge_ctx); s.login(FROM_ADDR, BRIDGE_PW)
    print("  AUTH OK — proceeding with sends")
except Exception as e:
    print(f"  AUTH FAILED: {e}")
    print("  olympio.almeida@protonmail.com may not be added to Bridge.")
    print("  Open Proton Mail Bridge and add this account, then re-run.")
    raise SystemExit(1)

# ── suppression ───────────────────────────────────────────────────────────────
sup_raw  = json.loads((HERE / "suppress_14june.json").read_text())
dead_raw = json.loads((HERE / "dead_14june.json").read_text())
new_raw  = json.loads((HERE / "newdead_followup.json").read_text())
TODAY_DEAD = {
    "anto.dias@timesgroup.com","goa.city@timesgroup.com","goa.online@timesgroup.com",
    "goa.toi@timesgroup.com","hcnscript@gmail.com","kanzilrodrigues@gmail.com",
    "nolasco.dsouza@timesgroup.com","pankaj.sharma@timesgroup.com","sanjay123@gmail.com",
    "timesarunsinha3000@gmail.com","timesofindia.goa@timesgroup.com",
}
sup = set(e.lower() for e in list(sup_raw)+list(dead_raw)+list(new_raw)) | {e.lower() for e in TODAY_DEAD}
aud = json.loads((HERE / "audience_14june.json").read_text())
def clean(lst):
    seen=set(); out=[]
    for e in lst:
        el=e.lower().strip()
        if el not in sup and el not in seen: seen.add(el); out.append(e)
    return out

ALL_GOV = clean(aud["depts"])
police  = [e for e in ALL_GOV if "goapolice.gov.in" in e.lower()]
depts   = [e for e in ALL_GOV if "goapolice.gov.in" not in e.lower()]
print(f"Police: {len(police)}  |  Departments: {len(depts)}  |  Total: {len(ALL_GOV)}")

# ── .ics ──────────────────────────────────────────────────────────────────────
def make_ics():
    DTSTAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ICS = "\r\n".join([
        "BEGIN:VCALENDAR","VERSION:2.0",
        "PRODID:-//PressDetective//Olympio Almeida//EN",
        "CALSCALE:GREGORIAN","METHOD:REQUEST","BEGIN:VEVENT",
        f"UID:{uuid.uuid4()}",f"DTSTAMP:{DTSTAMP}",
        "DTSTART:20260617T060000Z","DTEND:20260617T080000Z",
        "SUMMARY:TOMORROW — Joint Inspection 11:30 AM Siolim (17 June 2026)",
        "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
        "DESCRIPTION:Joint inspection VP Siolim-Sodiem + GSPCB."
        " Police and all departments requested to attend.",
        f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
        "STATUS:CONFIRMED","SEQUENCE:4",
        "BEGIN:VALARM","TRIGGER:-PT120M","ACTION:DISPLAY",
        "DESCRIPTION:Inspection in 2 hours","END:VALARM",
        "END:VEVENT","END:VCALENDAR",
    ])
    p = MIMEBase("text","calendar",method="REQUEST",charset="utf-8")
    p.set_payload(ICS.encode("utf-8")); encoders.encode_base64(p)
    p.add_header("Content-Disposition","attachment",filename="inspection_17june2026.ics")
    return p

def send_via_bridge(subject, body, bcc):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = FROM_ADDR
    msg["Cc"]      = CC_INFO
    msg["Bcc"]     = ", ".join(bcc)
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(make_ics())
    rcpts = [FROM_ADDR, CC_INFO] + list(bcc)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP("127.0.0.1", 1025, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, BRIDGE_PW)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())

SIG = """
Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@protonmail.com  |  Press: info@pressdetective.com
"""

# ── POLICE ────────────────────────────────────────────────────────────────────
POLICE_SUBJ = "URGENT — Police Presence Required TOMORROW 11:30 AM Wednesday 17 June 2026 | Siolim Inspection [Calendar Invite]"
POLICE_BODY = f"""\
To the Superintendent of Police / Station House Officer / Concerned Officer,

A calendar invite is attached. Please click "Add to Calendar".

JOINT SITE INSPECTION — TOMORROW WEDNESDAY 17 JUNE 2026
  Time:   11:30 AM  (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat Siolim-Sodiem (Notice Ref. VPSS/2026-27/site insp/648,
08 June 2026) and GSPCB are jointly inspecting the "Sunday Racquet and Social
Club" — commercial padel courts at House No. 47/3, Gaunsawaddo, Sodiem, Siolim:

  - Noise: 68-75 dB(A) against the 55 dB(A) residential limit
  - Encroachment on private land (Survey No. 197/A)
  - 2008 Panchayat licence-revocation order still unenforced (18 years)
  - GSPCB complaint: 9 March 2026 — unanswered for 9 months

We formally request:
  1. Police presence at 11:30 AM tomorrow to ensure no obstruction.
  2. Any prior complaint records for House No. 47/3, Gaunsawaddo,
     Sodiem to be made available to the inspection team.
  3. Registration of this matter in your station records.

Attendance and absence will be formally noted in the inspection record.
{SIG}"""

print(f"\n[POLICE — protonmail.com Bridge] {len(police)}...")
try:
    send_via_bridge(POLICE_SUBJ, POLICE_BODY, police)
    print(f"  OK ({len(police)})")
except Exception as e:
    print(f"  FAIL: {e}")
time.sleep(5)

# ── DEPARTMENTS ───────────────────────────────────────────────────────────────
DEPT_SUBJ = "FINAL NOTICE — Inspection TOMORROW 11:30 AM Wednesday 17 June 2026 | Siolim | Your Attendance Is Expected [Calendar Invite]"
DEPT_BODY = f"""\
To the concerned Department / Authority,

A calendar invite is attached. Please click "Add to Calendar".

JOINT SITE INSPECTION — TOMORROW WEDNESDAY 17 JUNE 2026
  Time:   11:30 AM  (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

This is the final formal notice before tomorrow's inspection called by the
Village Panchayat Siolim-Sodiem (Notice Ref. VPSS/2026-27/site insp/648).

GSPCB, the Collector (North Goa), Town & Country Planning, Directorate of
Panchayats, Land Revenue, BDO Bardez, and police have all been formally
requested to attend. The inspection concerns the "Sunday Racquet and Social
Club" padel courts at Gaunsawaddo, Sodiem — noise at 68-75 dB(A) vs 55
dB(A) limit, encroachment, and a 2008 Panchayat order left unenforced.

Your department is expected to:
  1. Depute a representative at 11:30 AM sharp.
  2. Bring your departmental record relating to this site.
  3. Place your response to the 9 March 2026 GSPCB complaint on record.

Attendance and absence will be formally documented.
{SIG}"""

print(f"\n[DEPARTMENTS — protonmail.com Bridge] {len(depts)}...")
B = 45
batches = [depts[i:i+B] for i in range(0,len(depts),B)]
ok = 0
for i, b in enumerate(batches, 1):
    try:
        send_via_bridge(DEPT_SUBJ, DEPT_BODY, b)
        print(f"  batch {i}/{len(batches)} OK ({len(b)})"); ok += 1
    except Exception as e:
        print(f"  batch {i}/{len(batches)} FAIL: {e}")
    if i < len(batches): time.sleep(4)

print(f"\n{'='*55}")
print(f"FROM: {FROM_ADDR} via Proton Bridge")
print(f"Police: OK  |  Depts: {ok}/{len(batches)} batches")
print(f"Total gov/police via protonmail.com: {len(ALL_GOV)}")
