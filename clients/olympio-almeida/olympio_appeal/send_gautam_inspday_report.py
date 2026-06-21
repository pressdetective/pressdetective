"""
Gautam — full inspection day report: all sends + press release text.

    python clients/olympio-almeida/olympio_appeal/send_gautam_inspday_report.py
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

SUBJ = "FULL INSPECTION DAY REPORT — All Sends + Press Release Text | 17 June 2026"

BODY = """\
Dear Gautam,

This is the complete record of everything sent today — every wave,
the press release, and the full contact breakdown.

=================================================================
PART 1 — TODAY'S SENDS (17 JUNE 2026, ALL WAVES)
=================================================================

WAVE A — INSPECTION DAY BLAST (morning, @pressdetective.com remote)

  New Goa press (94 incl. other):   94  First-ever contact, inspection TODAY
  New Goa government (87):          87  TODAY reminder, SP responded
  New Goa police/govt (12):         12  TODAY + police notice
  New NGO/civic (36):               36  Come as community witness
  New politicians/MPs/MLAs (11):    11  Your constituency, Lobo named
  Existing press + civic (137):    137  TODAY reminder
  Existing depts + police (37):     37  TODAY final call
  Existing MLAs (10):               10  TODAY + Lobo named
  Delilah Lobo direct x2:            2  Personal urgent appeal
  ──────────────────────────────────────
  WAVE A TOTAL:                    426  — 100% delivered

WAVE B — PRESS RELEASE (separate targeted send, both accounts)

  Batches 1-4 (180): @protonmail.com via Bridge          — ALL OK
  Batches 5-6 (49):  @pressdetective.com remote SMTP     — ALL OK
  ──────────────────────────────────────
  WAVE B TOTAL:                    229  — 100% delivered
  All major Goa outlets: Herald, Navhind, The Goan, Tarun Bharat,
  Prudent Media, HT Goa, News18, UNI, Loksatta, Sakal, Telegraph
  Goa, The Statesman + 200 more journalists and desks.

WAVE C — SP (SPCR) REPLY (16 June, last night)

  TO: cstatepolice112@gmail.com (Gmail — no NIC block)
  Warm, polite thank-you; requested police officer at inspection.
  DELIVERED.

WAVE D — SP UPDATE BROADCAST (16 June, last night)

  165 contacts — press(137) + depts(18) + MLAs(10)
  News: SP SPCR responded; still waiting for Lobo.
  ALL DELIVERED.

─────────────────────────────────────────────────────────────────
GRAND TOTAL TODAY:  820+ sends (Waves A + B + C + D)
NEW CONTACTS EVER REACHED FOR FIRST TIME TODAY:  243
─────────────────────────────────────────────────────────────────

=================================================================
PART 2 — FULL CAMPAIGN TOTALS (6–17 June 2026)
=================================================================

  Wave 1  Initial appeal (6 Jun):              156
  Wave 2  Press + dept escalation:             295
  Wave 3  Post-DMARC full push:                210
  Wave 4  Weekday correction:                  153
  Wave 5  Calendar invites bulk:               197
  Wave 6  Final push all segments:             184
  Wave 7  Press personal appeal:               137
  Wave 8  Police + govt via Bridge (x2):        37
  Wave 9  SP update broadcast:                 165
  Wave 10 Inspection day blast:                426
  Wave 11 Press release:                       229
  ─────────────────────────────────────────────────
  TOTAL SENDS (all waves):               ~2,200+
  Unique individuals ever reached:         ~450+
  Calendar invites distributed:           1,000+
  Dead addresses cleaned / suppressed:      ~150
  Government responses received:              1
    (SP SPCR Panaji — 16 June 2026)
  Press outlets covered:                     229
  MLA responses received:                      0
    (Delilah Lobo — documented silence)

=================================================================
PART 3 — DELILAH LOBO — DOCUMENTED NON-RESPONSE
=================================================================

Sent to DIRECTLY (TO field, not BCC):
  delilahlobo.goa@gmail.com          — multiple waves + today
  delilahlobosiolimoffice@gmail.com  — today's final appeal

Today's message opened with:
  "The inspection is THIS MORNING — in just a few hours. I have
  written to you many times. I know you are extremely busy. But
  I ask you one final time... please come, or please send someone."

Status as of sending: NO RESPONSE.
Her silence is documented across every wave of this campaign.
This is a reportable fact and an RTI/legal asset.

=================================================================
PART 4 — THE PRESS RELEASE
         (exact text sent to 229 Goa journalists)
=================================================================

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

FOR IMMEDIATE RELEASE
17 June 2026 | Siolim, Goa
Contact: olympio.almeida@protonmail.com | info@pressdetective.com
Evidence packet (26 pages) available on request.


POLICE RESPOND TO SIOLIM SENIOR CITIZEN'S NOISE COMPLAINT —
JOINT INSPECTION TAKES PLACE TODAY AT 11:30 AM

18-year-old Panchayat revocation order still unenforced; GSPCB
silent for 3 months; MLA Siolim has not responded.


SIOLIM, GOA — In a significant development overnight, the Office of
the Superintendent of Police (SPCR), Panaji has formally acknowledged
a noise-pollution complaint from a 70-year-old Siolim resident and
forwarded the matter for necessary police action.

The inspection — called by Village Panchayat Siolim-Sodiem,
co-conducted by GSPCB — takes place TODAY at 11:30 AM.
Press are welcome to attend and cover.

  WHEN:  TODAY, Wednesday 17 June 2026 — 11:30 AM
  WHERE: Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa


THE COMPLAINANT

Olympio Almeida, 70, resident of La Masseria, Survey No. 197/A, Siolim.
Next door: "Sunday Racquet and Social Club" — outdoor commercial padel
courts in a residential zone. Noise: 68-75 dB(A). Legal limit: 55 dB(A).

"I am 70 years old. I bought my home in Siolim for peace and quiet.
For years we could not sit in our own garden. When I measured the noise
it read 72 decibels. All I want is for the law to be enforced."
— Olympio Almeida


AN 18-YEAR-OLD ORDER NEVER ENFORCED

The Siolim-Sodiem Panchayat issued a formal licence-revocation order
against this plot in 2008 — on Almeida's own complaint about unauthorised
construction. It has never been enforced. 18 years on, the commercial
operations continue at full volume. Almeida also documents encroachment
on his own land at Survey No. 197/A.


GSPCB COMPLAINT — 3 MONTHS, NO RESPONSE

On 9 March 2026, Almeida filed a formal GSPCB complaint with noise
measurements, photographs, and legal citations. More than three months
later, GSPCB has not acknowledged receipt, sent an inspector, or
communicated any response.


OVERNIGHT: POLICE RESPOND

On 16 June 2026, the SP (SPCR) Panaji formally acknowledged the complaint
and forwarded it for police action — the first meaningful government
response since the March filing.

MLA Siolim, Ms. Delilah Lobo, has been contacted repeatedly this week.
As of this morning, no response has been received from her office.


THE STORY FOR GOA'S PRESS

Can a Panchayat revocation order be ignored for 18 years? What recourse
does a senior citizen have when GSPCB doesn't respond for 3 months? Does
Goa's noise law protect residents — or only on paper? Will the MLA
respond when a constituent asks for help?

TODAY'S INSPECTION is the moment to find out. Come. Observe. Report.
Bring a free decibel app (NIOSH SLM or Decibel X) and measure yourself.


EVIDENCE AVAILABLE — reply for immediate access (26 pages):
  1. Decibel measurements with timestamps and location data
  2. Photographs of courts and proximity to homes
  3. 2008 Panchayat licence-revocation order (full document)
  4. March 2026 GSPCB complaint (full text)
  5. Panchayat inspection notice VPSS/2026-27/site insp/648
  6. SP (SPCR) formal acknowledgement — 16 June 2026


CHRONOLOGY:
  Pre-2008:      Club begins operations in residential zone
  2008:          Panchayat licence-revocation order — never enforced
  9 March 2026:  Formal GSPCB complaint filed
  March-June:    GSPCB silent — no acknowledgement, no inspection
  8 June 2026:   VP Siolim-Sodiem issues joint inspection notice
  16 June 2026:  SP (SPCR) Panaji formally responds; forwards for action
  16 June 2026:  MLA Siolim (Delilah Lobo) — still no response
  17 June 2026:  INSPECTION TODAY at 11:30 AM


CONTACT: olympio.almeida@pressdetective.com | info@pressdetective.com
Complainant available for interview.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

=================================================================
PART 5 — WHAT WE NEED FROM YOU AFTER THE INSPECTION
=================================================================

Please send to info@pressdetective.com as soon as possible after
the inspection ends:

  1. Names and designations of all officials present
  2. Whether GSPCB did a noise measurement (calibrated or otherwise)
  3. Whether a police officer attended
  4. Whether Delilah Lobo or her office sent anyone
  5. The reference number on the written inspection report
  6. Names of any press who came
  7. Any incidents, obstructions, or unusual events
  8. Any verbal commitments made by officials

This information determines:
  - RTI deadline (Day 7 = 24 June if no written report)
  - Follow-up media angles
  - Next police steps (follow up with SP SPCR)
  - Whether to escalate to High Court / NGT

=================================================================
YOUR ANONYMITY — UNCHANGED
=================================================================

Your name, email, and all identifying details remain private
throughout. You are "the complainant" in all public material.
Nothing in this campaign or its press release identifies you.

=================================================================

This campaign has reached 450+ individuals across 11 waves over
12 days. The police responded. The Panchayat called the inspection.
229 journalists have the full story. The evidence is documented.

Whatever happened at 11:30 AM today — you did everything that could
be done. Now we hear from you and act on what the inspection found.

With all confidence and respect,
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

ctx = ssl.create_default_context()
print("Sending full inspection day report to Gautam ...")
try:
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, ["gavora@gmail.com", CC_INFO], msg.as_bytes())
    print("  OK -> gavora@gmail.com (CC: info@pressdetective.com)")
except Exception as e:
    print(f"  FAIL: {e}")
