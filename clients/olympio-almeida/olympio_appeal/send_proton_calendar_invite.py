"""
Send a Proton Calendar invite for the 17 June inspection.
Attaches a .ics iCalendar file via Proton SMTP — recipients get
an "Add to Calendar" button directly in Proton Mail.

    python clients/olympio-almeida/olympio_appeal/send_proton_calendar_invite.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import json, smtplib, ssl, uuid, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))
FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"
assert FROM_ADDR.endswith("@pressdetective.com")

# 17 June 2026, 11:30 AM IST = 06:00 UTC
DTSTART  = "20260617T060000Z"
DTEND    = "20260617T080000Z"   # 1:30 PM IST
DTSTAMP  = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
UID      = str(uuid.uuid4())

# iCalendar — METHOD:REQUEST makes Proton show "Add to Calendar"
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
    "SUMMARY:Joint Site Inspection - Siolim Padel Courts (Olympio Almeida)",
    "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
    "DESCRIPTION:Joint inspection called by VP Siolim-Sodiem (Notice VPSS/2026-27"
    "/site insp/648\\, 08 June 2026). Matter: Sunday Racquet and Social Club --"
    " padel courts at House No. 47/3\\, Gaunsawaddo\\, Sodiem\\, Siolim."
    " Noise 68-75 dB(A) vs 55 dB(A) limit. GSPCB complaint 9 March 2026."
    " Arrive by 11:15 AM. Bring complaint copy and evidence.",
    f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
    f"ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;"
    f"RSVP=TRUE;CN=Gautam:mailto:gavora@gmail.com",
    f"ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;"
    f"RSVP=TRUE;CN=PressDetective:mailto:{CC_INFO}",
    "STATUS:CONFIRMED",
    "SEQUENCE:0",
    "BEGIN:VALARM",
    "TRIGGER:-PT120M",
    "ACTION:DISPLAY",
    "DESCRIPTION:Inspection in 2 hours - depart soon",
    "END:VALARM",
    "BEGIN:VALARM",
    "TRIGGER:-PT30M",
    "ACTION:DISPLAY",
    "DESCRIPTION:Inspection in 30 minutes",
    "END:VALARM",
    "END:VEVENT",
    "END:VCALENDAR",
])

BODY_TEXT = """\
Dear Gautam,

Please find attached a calendar invite for tomorrow's joint site inspection.

  Date:  Wednesday, 17 June 2026
  Time:  11:30 AM (please arrive by 11:15 AM)
  Venue: Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

Click "Add to Calendar" in your Proton Mail to save the event with reminders.

The full pre-inspection brief was sent separately. Please bring your March 2026
complaint copy, any noise recordings, and any letters you hold from the
Panchayat or GSPCB.

Regards,
PressDetective
On behalf of Olympio Almeida
olympio.almeida@pressdetective.com
"""

# Build multipart/mixed: text body + .ics attachment
msg = MIMEMultipart("mixed")
msg["Subject"] = "Calendar Invite: Joint Site Inspection - Wed 17 June 2026, 11:30 AM - Siolim"
msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
msg["To"]      = "gavora@gmail.com"
msg["Cc"]      = CC_INFO

msg.attach(MIMEText(BODY_TEXT, "plain", "utf-8"))

ics_part = MIMEBase("text", "calendar", method="REQUEST", charset="utf-8")
ics_part.set_payload(ICS.encode("utf-8"))
encoders.encode_base64(ics_part)
ics_part.add_header("Content-Disposition", "attachment",
                    filename="inspection_17june2026.ics")
msg.attach(ics_part)

rcpts = ["gavora@gmail.com", CC_INFO]
ctx = ssl.create_default_context()
try:
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())
    print(f"Calendar invite sent OK -> {', '.join(rcpts)}")
    print("Recipients will see 'Add to Calendar' in Proton Mail.")
except Exception as e:
    print(f"FAILED: {e}")
