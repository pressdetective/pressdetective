"""
Calendar invite to MLAs for 17 June inspection.
PressDetective Proton ONLY.

    python clients/olympio-almeida/olympio_appeal/send_mla_calendarinvite.py
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
FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"
assert FROM_ADDR.endswith("@pressdetective.com")

sup = set(e.lower() for e in json.loads((HERE / "suppress_14june.json").read_text()))

# Valid MLA addresses (gmail ones deliver; .gov.in/.nic.in NIC-blocked but include for record)
MLA_LIST = [
    "delilahlobo.goa@gmail.com",        # Siolim MLA — KEY jurisdiction
    "delilahlobosiolimoffice@gmail.com", # Siolim MLA office
    "vijaisardesai@gmail.com",           # Fatorda MLA / GFP leader
    "vijaisardesai.goa@gmail.com",
    "drdeviyarane.mla.poriem@gmail.com", # Poriem MLA
    "mlashetye03bicholim@gmail.com",     # Bicholim MLA
    "pravinarlekar4pernem@gmail.com",    # Pernem MLA
    "sec-legi.goa@nic.in",              # Goa Legislature Secretariat (NIC — blocked but official)
    "mla.mandrem.gvs@gov.in",           # Mandrem MLA (NIC — blocked)
    "mla.tivim.gvs@gov.in",             # Tivim MLA (NIC — blocked)
    "mla.calangute.gvs@gov.in",
    "mla.mapusa.gvs@gov.in",
    "mla.porvorim.gvs@gov.in",
]
mlas = [e for e in dict.fromkeys(MLA_LIST) if e.lower() not in sup]
print(f"MLAs to contact: {len(mlas)}")
for m in mlas: print(f"  {m}")

# .ics
DTSTART = "20260617T060000Z"
DTEND   = "20260617T080000Z"
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
    "DESCRIPTION:Joint site inspection called by VP Siolim-Sodiem"
    " (Notice VPSS/2026-27/site insp/648). Sunday Racquet and Social Club --"
    " padel courts at House No. 47/3\\, Gaunsawaddo\\, Sodiem\\, Siolim."
    " Noise 68-75 dB(A) vs 55 dB(A) limit. GSPCB complaint 9 March 2026."
    " MLAs requested to attend or depute a representative.",
    f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
    "STATUS:CONFIRMED",
    "SEQUENCE:0",
    "BEGIN:VALARM",
    "TRIGGER:-PT120M",
    "ACTION:DISPLAY",
    "DESCRIPTION:Inspection in 2 hours",
    "END:VALARM",
    "END:VEVENT",
    "END:VCALENDAR",
])

def make_ics():
    p = MIMEBase("text", "calendar", method="REQUEST", charset="utf-8")
    p.set_payload(ICS.encode("utf-8"))
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment", filename="inspection_17june2026.ics")
    return p

SUBJ = "Your Attendance Requested — Joint Site Inspection TOMORROW Wednesday 17 June, 11:30 AM, Siolim [Calendar Invite]"
BODY = f"""\
To the Honourable Member of the Goa Legislative Assembly,

A calendar invite is attached for tomorrow's joint site inspection.
Please click "Add to Calendar" to save the event.

  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat Siolim-Sodiem has called a joint inspection with the
Goa State Pollution Control Board regarding the "Sunday Racquet and Social Club"
— outdoor padel courts at House No. 47/3, Gaunsawaddo, Sodiem, Siolim — operating
in a residential zone with measured noise of 68-75 dB(A) against the 55 dB(A)
residential limit. A 2008 Panchayat licence-revocation order on the same plot
(Survey No. 197/7) remains unenforced. A complaint was filed with GSPCB on
9 March 2026 and has received no response to date.

As our elected representative, we respectfully request you to:
  1. Attend or depute a representative to the inspection tomorrow.
  2. State your position on noise-pollution enforcement and land-use compliance
     in residential areas.
  3. Raise the long-pending GSPCB complaint with the relevant authorities.

A 26-page evidence packet is available on request.

Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  ·  Press: info@pressdetective.com
"""

def send(bcc):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = SUBJ
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = FROM_ADDR
    msg["Cc"]      = CC_INFO
    msg["Bcc"]     = ", ".join(bcc)
    msg.attach(MIMEText(BODY, "plain", "utf-8"))
    msg.attach(make_ics())
    rcpts = [FROM_ADDR, CC_INFO] + list(bcc)
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())

B = 45
batches = [mlas[i:i+B] for i in range(0, len(mlas), B)]
ok = 0
for i, b in enumerate(batches, 1):
    try:
        send(b); print(f"  batch {i}/{len(batches)} OK ({len(b)})"); ok += 1
    except Exception as e:
        print(f"  batch {i}/{len(batches)} FAIL: {e}")
    time.sleep(3)
print(f"MLAs: {ok}/{len(batches)} batches sent ({len(mlas)} recipients)")
