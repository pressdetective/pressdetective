"""
Final pre-inspection report to Gautam — best wishes + safe journey.
PressDetective Proton ONLY.

    python clients/olympio-almeida/olympio_appeal/send_gautam_final.py
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
assert FROM_ADDR.endswith("@pressdetective.com")

SUBJ = "Olympio Siolim Case -- Final Report + Safe Journey to Goa (Inspection TOMORROW 11:30 AM)"

BODY = """\
Dear Gautam,

This is the final report before tomorrow's inspection. Everything is in order.
Safe journey to Goa -- we are ready.

=================================================================
TOMORROW -- YOUR ARRIVAL DETAILS
=================================================================

  Day:    Wednesday, 17 June 2026
  Time:   11:30 AM  (please arrive at the office by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office
          Sodiem, Siolim, Goa

A calendar invite with reminders was sent to you separately.

WHAT TO BRING
  - Copy of your original complaint (March 2026)
  - Any noise/decibel videos you have recorded
  - Any letters from GSPCB or the Panchayat
  - A note of dates and times you personally observed the noise
  - Your phone (decibel app on standby)

=================================================================
FULL CAMPAIGN REPORT -- EVERYTHING DONE
=================================================================

Here is the complete picture of what has been done on your behalf
since the inspection notice arrived on 8 June 2026:

WAVE 1 -- DEPARTMENTS (pre-inspection notice)
  Sent to 40 official addresses: GSPCB (Chairman + Member Secretary),
  Collector North Goa, Town & Country Planning, Directorate of Panchayats,
  Land Revenue, BDO Bardez, SP North Goa, Siolim Coastal PI, Mapusa PI,
  and all relevant police stations. Each was asked to depute a rep,
  bring their departmental record, and put their response on record.

WAVE 2 -- GOA PRESS + CIVIC GROUPS
  164 press contacts and civic organisations received a request-for-
  comments letter and an invitation to attend or observe.

WAVE 3 -- MLAs
  All area MLAs contacted by email and today by calendar invite --
  Delilah Lobo (Siolim MLA, key jurisdiction), Vijai Sardesai,
  and area legislators. Requested to attend or depute, and to raise
  the matter with GSPCB and the Collector.

WAVE 4 -- CALENDAR INVITES (today, 16 June)
  .ics calendar invites sent to:
    - Gautam (you) -- delivered with 2-hour and 30-minute reminders
    - info@pressdetective.com
    - 89 departments + civic/NGO contacts
    - 96 press contacts
    - 13 MLAs
  Every recipient can click "Add to Calendar" in their email to
  save the event immediately.

WAVE 5 -- WEEKDAY CORRECTION
  An earlier email referred to 17 June as "Tuesday" -- corrected
  immediately. A correction was sent to all 153 delivered contacts.
  The date (17 June) and time (11:30 AM) were always correct.

=================================================================
DELIVERY REALITY -- HONEST PICTURE
=================================================================

  Inspection organisers (VP Siolim-Sodiem gmail):    DELIVERED
  GSPCB working address (goapcb@gmail.com):           DELIVERED
  Siolim MLA Delilah Lobo (gmail):                   DELIVERED
  All gmail-hosted press, civic, NGOs:                DELIVERED
  NIC/gov.in/goapolice.gov.in addresses (39):         BLOCKED
    (NIC GovCloud rejects all external senders --
     this is a known national policy, not our error)

The people who matter MOST for tomorrow -- the Panchayat that called
the inspection and the GSPCB that is co-conducting it -- have received
every communication. You are not walking in cold.

=================================================================
WHAT TO EXPECT AT THE INSPECTION
=================================================================

  - The Panchayat sarpanch or their representative will lead.
  - GSPCB should bring calibrated noise meters.
  - The club owners or their representative may be present.
  - State your observations clearly and calmly. You are a resident
    with a legitimate complaint -- you are on the right side of the law.
  - Ask for the inspection REPORT IN WRITING and a reference number.
    If not given on the day, request it formally within 48 hours.
  - Note the names and designations of all officials present.
  - If noise is audible during the inspection itself, point it out.
  - Do not engage with the club owners directly -- speak through the
    Panchayat / GSPCB officer.

=================================================================
AFTER THE INSPECTION -- NEXT STEPS (for reference)
=================================================================

  Within 7 days:  Follow up with the Panchayat for the written report.
  By 24 June:     File RTI if the written report has not been issued.
  GSPCB:          Request the noise-meter reading result in writing.
  Police/TCP:     If needed, we can prepare posted letters + GSPCB
                  online grievance portal submissions for a formal
                  paper trail with the NIC-blocked offices.

=================================================================
AS ALWAYS -- YOUR ANONYMITY IS ABSOLUTE
=================================================================

Your name, your contact details, and your identity do not appear
anywhere -- not in any letter, any press release, any filing, or
any document. In every piece of campaign material you are referred
to only as "a neighbouring senior resident."

This will not change at or after the inspection. If any official
or press person asks who filed the complaint, the answer is:
Olympio Almeida, La Masseria, Survey No. 197/A, Siolim -- and
that is the only name on the record.

=================================================================
BEST WISHES FOR TOMORROW
=================================================================

You have done the hard part -- you filed the complaint, you kept
the faith, and you let us build the case around it. Tomorrow is
the moment the system actually shows up.

Safe journey to Goa. Arrive by 11:15 AM. Stay calm, stay on
record, and get that written report.

We will be with you every step of the way.

With warm regards and every good wish,
PressDetective
On behalf of Olympio Almeida
olympio.almeida@pressdetective.com
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJ
msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
msg["To"]      = "gavora@gmail.com"
msg["Cc"]      = CC_INFO
msg.attach(MIMEText(BODY, "plain", "utf-8"))

rcpts = ["gavora@gmail.com", CC_INFO]
ctx = ssl.create_default_context()
try:
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())
    print("Gautam final report + best wishes -- OK -> gavora@gmail.com (CC info@)")
except Exception as e:
    print(f"FAILED: {e}")
