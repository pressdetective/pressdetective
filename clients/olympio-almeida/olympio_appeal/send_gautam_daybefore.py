"""
Day-before report to Gautam + info@ — Wednesday 17 June inspection.
PressDetective Proton ONLY.

    python clients/olympio-almeida/olympio_appeal/send_gautam_daybefore.py
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

def send(subject, body, to):
    m = MIMEMultipart("alternative")
    m["Subject"] = subject
    m["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    m["To"]      = to
    m["Cc"]      = CC_INFO
    m.attach(MIMEText(body, "plain", "utf-8"))
    rcpts = [to, CC_INFO]
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, m.as_bytes())

SUBJ = "Olympio Siolim Case -- TOMORROW Wednesday 17 June, 11:30 AM: Full Pre-Inspection Report"

BODY = """\
Dear Gautam,

The inspection is TOMORROW. Here is the complete picture.

=================================================================
TOMORROW -- WEDNESDAY 17 JUNE 2026
=================================================================

  Time:     11:30 AM (please arrive by 11:15 AM)
  Venue:    Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa
  Matter:   Joint site inspection -- "Sunday Racquet and Social Club"
            padel courts, House No. 47/3, Gaunsawaddo, Sodiem, Siolim
            (Survey No. 197/7), re noise + encroachment + 2008 order.

WHAT TO BRING
  - Your copy of the original complaint (March 2026)
  - Any noise videos / decibel readings you have captured
  - Any GSPCB or Panchayat letters you have received
  - Notes of dates and times you personally observed the noise

=================================================================
FULL CAMPAIGN SUMMARY -- WHAT WAS SENT AND WHAT LANDED
=================================================================

Over the past week, Olympio's appeal went to the entire official,
press and civic ecosystem in Goa. Here is the honest picture:

1. OFFICIAL DEPARTMENTS (40 addresses)
   - Sent: Pre-inspection notice to GSPCB (Chairman + Member Secretary),
     Collector North Goa, Town & Country Planning, Directorate of
     Panchayats, Land Revenue, BDO Bardez, SP North Goa, area police PIs.
   - Status: Gmail-hosted addresses DELIVERED. NIC/gov.in addresses
     (39 total across all segments) are POLICY-BLOCKED by the national
     NIC GovCloud gateway -- this affects every external sender, not
     just us. It is not fixable by email.
   - KEY: The two bodies actually running tomorrow's inspection --
     Village Panchayat Siolim-Sodiem (vpsiolimsodiem@gmail.com) and
     GSPCB (goapcb@gmail.com) -- BOTH received our mail. That is what
     matters for tomorrow.

2. AREA MLAs (9 valid addresses)
   - Sent: Request for public position + attend/depute on 17 June.
   - Siolim MLA Delilah Lobo (delilahlobo.goa@gmail.com) -- DELIVERED.
   - Goa Legislature Secretariat (sec-legi.goa@nic.in) -- NIC-blocked
     (policy, not our DMARC). Official channel also contacted.

3. GOA PRESS + CIVIC (162 contacts, cleaned)
   - Sent: Request for comments + "hear it yourself" Sunday invitation +
     inspection notice. Four batches, BCC, GDPR unsubscribe line.
   - Delivered to all non-dead, non-NIC press addresses.
   - 18 additional dead addresses found and suppressed post-send
     (fabricated addresses from the original list).

4. WEEKDAY CORRECTION
   - Earlier emails mistakenly said "Tuesday" -- corrected to WEDNESDAY.
   - Correction sent to all 153 successfully delivered contacts.
   - You received the correction on 15 June.

=================================================================
DELIVERABILITY SUMMARY
=================================================================

  Total sent across all waves:      ~300 recipients
  Confirmed delivered (est.):       ~145-155
  NIC GovCloud policy-blocked:      39  (real mailboxes, unreachable
                                        by any external email sender)
  Dead/invalid (suppressed):        128 total (list now clean)
  Inspection organisers reached:    YES -- VP + GSPCB both on gmail

=================================================================
THE NIC BLOCK -- WHY IT DOES NOT HURT TOMORROW
=================================================================

The Collector, IGP, SP, police PIs, GSPCB @nic.in, TCP directorate
all use NIC GovCloud email which blocks every non-government sender.
This is a known national policy issue -- it is not something wrong
with our email or domain.

For the FORMAL paper record with those offices, the right channels are:
  a) Hand-delivered or posted letter (we can prepare these post-inspection)
  b) GSPCB online grievance portal (creates a dated official reference)
  c) The in-person inspection tomorrow -- which is more powerful than any email

=================================================================
AFTER TOMORROW -- NEXT STEPS
=================================================================

  1. Press the Panchayat for the WRITTEN inspection report within 7 days.
  2. File RTI if the report is not issued by 24 June 2026.
  3. Request GSPCB's calibrated noise reading result in writing.
  4. If police or TCP need formal notice, prepare posted letters + online
     portal submissions so there is a dated paper trail.
  5. If any journalist covers the inspection, offer them the 26-page
     evidence packet.

=================================================================
AS ALWAYS -- YOUR ANONYMITY IS ABSOLUTE
=================================================================

Your name and contact do not appear anywhere -- not in any letter,
press communication, legal filing, or public document. In all material
you are referred to only as "a neighbouring senior resident."

Everything is in order for tomorrow. The organisers have our
submission, the press has been briefed, and the officials who can
actually act are on notice. See you on the right side of this.

Regards,
PressDetective
On behalf of Olympio Almeida
olympio.almeida@pressdetective.com
"""

try:
    send(SUBJ, BODY, "gavora@gmail.com")
    print("Gautam day-before report -- OK -> gavora@gmail.com (CC info@)")
except Exception as e:
    print(f"FAILED: {e}")
