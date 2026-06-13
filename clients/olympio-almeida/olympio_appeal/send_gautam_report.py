"""Send Gautam Day 3 full report via Proton remote SMTP."""
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

def proton_send(msg):
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        all_addrs = []
        for hdr in ("To", "Cc", "Bcc"):
            val = msg.get(hdr, "")
            if val:
                all_addrs += [a.strip() for a in val.split(",")]
        s.sendmail(FROM_ADDR, all_addrs, msg.as_bytes())

GAUTAM_TO   = "gavora@gmail.com"
GAUTAM_SUBJ = "Olympio Siolim Case -- Day 3 Full Report (13 June) + 4-Day Countdown"

lines = [
    "Dear Gautam,",
    "",
    "Here is your complete Day 3 update for the Sunday Racquet Club noise/encroachment campaign. The inspection is now 4 days away.",
    "",
    "=================================================================",
    "DAY 3 -- 13 JUNE 2026 -- ACTIVITIES SUMMARY",
    "=================================================================",
    "",
    "1. FIRST OFFICIAL REPLY RECEIVED",
    "Village Panchayat Siolim-Marna replied on 12 June confirming that the affected",
    "plot (Gaunsawaddo, Sodiem) falls within the jurisdiction of VP Siolim-Sodiem,",
    "not theirs. We thanked them and removed them from the active list.",
    "",
    "This is the first official reply in the entire campaign -- a positive signal",
    "that the pressure is being felt.",
    "",
    "2. GSPCB TECHNICAL LETTER",
    "Sent a formal technical letter to GSPCB today with three specific requests:",
    "  a) Use Class 1 or Class 2 calibrated sound-level meters (IEC 61672-1) for",
    "     the 17 June inspection -- not smartphone apps.",
    "  b) Conduct an UNANNOUNCED follow-up measurement on a SUNDAY (21 or 28 June)",
    "     between 10 AM and 2 PM -- this is peak noise time. Tuesday 11:30 AM is",
    "     when the courts are quiet; that measurement alone will not capture the problem.",
    "  c) Verify whether the operator holds a valid Consent to Operate under the",
    "     Air (Prevention & Control of Pollution) Act 1981.",
    "",
    "This creates a paper trail if GSPCB only shows up Tuesday and claims no noise.",
    "",
    "3. VP SIOLIM-SODIEM SCOPE LETTER",
    "Sent a formal scope letter to VP Siolim-Sodiem with four requests:",
    "  a) Record encroachment on Olympio's land (Sy. 197/A), tree damage,",
    "     unauthorised constructions, and current status of any Panchayat permissions.",
    "  b) Require the operator/owner to present at the inspection with all permission",
    "     documents -- building licence, occupancy cert, noise permits, 2008 file.",
    "  c) Provide a certified copy of the inspection report to the complainant.",
    "  d) Produce the original 2008 file in which the Panchayat revoked the licence",
    "     on Sy. 197/7.",
    "",
    "4. PRESS 'HEAR IT YOURSELF' OUTREACH",
    "Sent a targeted letter to 40 established Goa press outlets inviting them to",
    "visit Gaunsawaddo this Sunday (15 June) between 9 AM and 7 PM.",
    "",
    "5. CALENDAR INVITE WAVE -- ~240 PARTIES",
    "Sent updated calendar invitations (SEQUENCE:2) with a formal covering letter",
    "to all ~240 parties notified so far:",
    "  - 55 government officials (Collector, GSPCB, SP, TCP, Police, MLAs, MPs)",
    "  - 14 newly-added officials (IGP Goa, Dir Panchayats, Land Records Mapusa,",
    "    MLA Lobo personal, 8 Panchayat sub-offices)",
    "  - 9 civic organisations",
    "  - 172 Goa press contacts",
    "",
    "6. DAY 3 PRESS FOLLOW-UP (216 CONTACTS)",
    "Sent a second press follow-up to all 216 Goa press/civic contacts (excluding",
    "3 verified hard bounces) reminding them of the Sunday visit opportunity and",
    "the 17 June inspection. Sent via Mailtrap (batches 1-3, 135 contacts) and",
    "Proton remote SMTP (batches 4-5, 81 contacts).",
    "",
    "=================================================================",
    "4-DAY COUNTDOWN -- WHAT HAPPENS NEXT",
    "=================================================================",
    "",
    "  Sun 15 June  -> Press + residents visit Gaunsawaddo (if they come)",
    "                  YOUR TASK (see below)",
    "  Mon 16 June  -> Day-before reminder to all officials",
    "  Tue 17 June  -> INSPECTION at 11:30 AM, Siolim-Sodiem Panchayat office",
    "  Wed 18 June+ -> Follow up on inspection report; file RTI if report",
    "                  not provided within 7 days",
    "",
    "=================================================================",
    "YOUR TASK THIS SUNDAY (15 JUNE) -- CRITICAL",
    "=================================================================",
    "",
    "Please record 3-4 short videos (1-2 minutes each) this Sunday between",
    "10 AM and 2 PM with the following:",
    "",
    "  1. Hold your phone with a decibel-meter app running ON SCREEN",
    "     (NIOSH SLM, Decibel X, or similar -- free on Play Store/App Store)",
    "  2. Capture the meter reading clearly -- aim for readings when courts are active",
    "  3. Each video should show the phone's timestamp",
    "  4. Record from different positions if possible (your garden/terrace,",
    "     the boundary wall, inside with windows open)",
    "",
    "These videos will be presented at the inspection on Tuesday to demonstrate",
    "that peak noise occurs on Sundays, not Tuesdays at 11:30 AM.",
    "",
    "Send me the videos by Sunday evening -- we will prepare a summary note.",
    "",
    "=================================================================",
    "INSPECTION LOGISTICS -- 17 JUNE",
    "=================================================================",
    "",
    "  Time:  11:30 AM (please arrive by 11:15 AM)",
    "  Venue: Village Panchayat Siolim-Sodiem office",
    "  What to bring:",
    "    - Copy of your original complaint (March 2026)",
    "    - Any noise-measurement readings or notes you have",
    "    - Your Sunday videos (on phone or USB)",
    "    - Any previous correspondence from GSPCB or Panchayat",
    "",
    "Olympio will be present. Legal support is being coordinated.",
    "",
    "=================================================================",
    "CAMPAIGN STATUS (as of 13 June 2026)",
    "=================================================================",
    "",
    "  Officials formally notified:   ~69 (55 original + 14 new)",
    "  Press contacts reached:        ~216 Goa press (3 waves)",
    "  Civic organisations:           9",
    "  Calendar invitations sent:     ~247 parties (2 waves)",
    "  Official replies received:     1 (VP Siolim-Marna -- jurisdiction clarified)",
    "  Verified email bounces:        3 (generic Hindustan Times addresses only)",
    "  All critical government addresses: delivered clean",
    "  RTI responses due:             9 July 2026",
    "",
    "The campaign has strong momentum. The key remaining task is ensuring the",
    "inspection on 17 June produces a written report and that GSPCB commits to",
    "a Sunday measurement.",
    "",
    "Regards,",
    "PressDetective",
    "On behalf of Olympio Almeida",
    "olympio.almeida@pressdetective.com",
]

GAUTAM_BODY = "\n".join(lines)

gau_msg = MIMEMultipart("alternative")
gau_msg["Subject"] = GAUTAM_SUBJ
gau_msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
gau_msg["To"]      = GAUTAM_TO
gau_msg["Cc"]      = CC_INFO
gau_msg.attach(MIMEText(GAUTAM_BODY, "plain", "utf-8"))

try:
    proton_send(gau_msg)
    print(f"Gautam report -- OK -> {GAUTAM_TO}")
except Exception as e:
    print(f"Gautam report -- FAILED: {e}")
