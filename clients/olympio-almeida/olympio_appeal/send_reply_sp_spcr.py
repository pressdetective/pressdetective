"""
Reply to SP (SPCR) Panaji — cstatepolice112@gmail.com
Polite, kind request to attend tomorrow's inspection.

    python clients/olympio-almeida/olympio_appeal/send_reply_sp_spcr.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import json, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"

TO_SP = "cstatepolice112@gmail.com"

SUBJ = ("Re: Complaint — Sunday Racquet and Social Club, Siolim | "
        "Humble Request — Please Attend Tomorrow's Inspection 11:30 AM")

BODY = """\
Dear Sir / Ma'am,

Namaste. I am Olympio Almeida, resident of La Masseria, Survey No. 197/A,
Sodiem, Siolim, Bardez, Goa — the complainant in the matter you have so
kindly acknowledged.

I am deeply grateful that your office has taken prompt cognizance of this
matter. It means a great deal to me and to the senior citizen residents of
our neighbourhood who have been suffering for years.

I am writing with one humble request: the Village Panchayat Siolim-Sodiem,
jointly with the Goa State Pollution Control Board, is conducting a formal
site inspection TOMORROW:

  Day:    Wednesday, 17 June 2026
  Time:   11:30 AM
  Venue:  Village Panchayat Siolim-Sodiem office,
          Sodiem, Siolim, Bardez, Goa

Could I request that your office kindly depute a police officer to attend
the inspection? Their presence would:

  1. Ensure the inspection proceeds smoothly without any obstruction.
  2. Allow the police to witness firsthand the noise levels (68-75 dB(A)
     measured against the 55 dB(A) residential limit).
  3. Register this complaint formally in the station records so there is
     an official police record of the matter.

I understand you are very busy, and I make this request with full respect
for the demands on your department. Even a junior officer's presence
would be enormously helpful and reassuring to the residents.

The matter involves the "Sunday Racquet and Social Club" operating outdoor
commercial padel courts in a residential zone. A 2008 Panchayat order
revoking the licence on this very plot has never been enforced in 18 years.
I filed a formal complaint with GSPCB on 9 March 2026, and have received
no response. Tomorrow's inspection is the first formal action in months.

A 26-page evidence packet (noise readings, photographs, the 2008 order,
the GSPCB complaint) is available on request — I would be happy to
send it to you immediately.

Once again, my sincere thanks to the Office of the Superintendent of
Police (SPCR), Panaji for your prompt attention. I have full faith in
the Goa Police.

Yours respectfully,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Sodiem, Siolim, Bardez, Goa
Email: olympio.almeida@pressdetective.com
Press contact: info@pressdetective.com
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJ
msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
msg["To"]      = TO_SP
msg["Cc"]      = CC_INFO

msg.attach(MIMEText(BODY, "plain", "utf-8"))

rcpts = [TO_SP, CC_INFO]
ctx = ssl.create_default_context()

print(f"Sending reply to SP (SPCR): {TO_SP} ...")
try:
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())
    print(f"  OK -> {TO_SP} (CC: {CC_INFO})")
    print()
    print("Reply to SP (SPCR) Panaji sent successfully.")
except Exception as e:
    print(f"  FAIL: {e}")
