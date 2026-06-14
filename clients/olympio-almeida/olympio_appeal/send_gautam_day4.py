"""Gautam full Day 4 update (Saturday 14 June 2026) via Proton remote SMTP."""
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

def send(msg):
    rcpts = []
    for hdr in ("To","Cc","Bcc"):
        v = msg.get(hdr,"")
        if v: rcpts += [a.strip() for a in v.split(",")]
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())

lines = [
"Dear Gautam,",
"",
"Day 4 update (Saturday, 14 June). We are now 3 days from the inspection, and",
"TOMORROW (Sunday 15 June) is the single most important day for evidence.",
"",
"=================================================================",
"WHAT WENT OUT TODAY (14 JUNE) -- all signed by Olympio",
"=================================================================",
"",
"1. DEPARTMENTS -- PRE-INSPECTION NOTICE (42 official addresses)",
"   Sent a formal 'please depute a representative' letter to every concerned",
"   department: GSPCB (chairman + member secretary), Collector North Goa, Town",
"   & Country Planning, Directorate of Panchayats, Land Revenue / Land Records,",
"   BDO Bardez, Superintendent of Police North Goa, and all area police PIs.",
"   Each was asked to (a) send an officer on 17 June, (b) bring their",
"   department's record (consent-to-operate, land-use, survey position, prior",
"   complaints), and (c) put their response to the 9 March complaint on record.",
"",
"2. ALL GOA PRESS + CIVIC ALLIES -- REQUEST FOR COMMENTS (234 contacts)",
"   Sent a request-for-comments letter to the full Goa press list and civic",
"   organisations, inviting their on-record comment, coverage, or editorial",
"   view -- and inviting them to come hear it themselves TOMORROW (Sun 15 June,",
"   9 AM - 7 PM) and to observe Tuesday's inspection. Evidence packet offered.",
"   (Sent in 6 batches via Proton remote; an unsubscribe line was included for",
"    GDPR/DPDP compliance.)",
"",
"3. MLAs -- REQUEST FOR PUBLIC POSITION (19 addresses)",
"   Wrote to the area MLAs (Siolim, Mapusa, Calangute, Porvorim, Tivim, Mandrem,",
"   Sanquelim, Margao, plus Delilah Lobo, Michael Lobo, Vijai Sardesai and",
"   others) asking them to (a) state their position on noise/land-use",
"   enforcement, (b) attend or depute a representative on 17 June, and (c) raise",
"   the long-pending complaint with GSPCB and the Collector.",
"",
"Total reached today: ~295 recipients across departments, press and MLAs.",
"",
"=================================================================",
"YOUR TASK TOMORROW (SUNDAY 15 JUNE) -- THE KEY EVIDENCE",
"=================================================================",
"",
"Tuesday's inspection is at 11:30 AM -- a time when the courts are usually",
"quiet. The noise peaks on SUNDAYS. So tomorrow's recordings are what prove the",
"problem. Please:",
"",
"  1. Record 3-4 short videos (1-2 min each) between 10 AM and 2 PM tomorrow.",
"  2. Have a decibel-meter app running ON SCREEN (NIOSH SLM or Decibel X --",
"     both free) so the reading is visible in the video.",
"  3. Make sure each clip shows the phone's date/time stamp.",
"  4. Record from a few positions: your terrace/garden, the boundary wall, and",
"     indoors with a window open (to show it carries inside).",
"  5. If safe and lawful from your own property, a wide shot showing the courts",
"     in use alongside the meter reading is the strongest single clip.",
"",
"Send the videos to me by Sunday evening. We will prepare a short signed note",
"to accompany them and table them at Tuesday's inspection -- and offer them to",
"any journalist who covers the story.",
"",
"As always, your name and contact stay entirely off every document. In all",
"campaign material you are referred to only as 'a neighbouring resident'.",
"",
"=================================================================",
"3-DAY COUNTDOWN",
"=================================================================",
"",
"  Sun 15 June  ->  Peak-noise day. Your videos. Press 'hear it yourself'.",
"  Mon 16 June  ->  Day-before reminder to all officials; confirm attendees.",
"  Tue 17 June  ->  INSPECTION, 11:30 AM, Siolim-Sodiem Panchayat office.",
"                   Please arrive by 11:15 AM.",
"  Wed 18 June+ ->  Press the Panchayat/GSPCB for the written report; file RTI",
"                   if it is not provided within 7 days.",
"",
"WHAT TO BRING ON TUESDAY",
"  - Copy of your original complaint (March 2026)",
"  - Your Sunday videos (phone + a USB copy)",
"  - Any GSPCB / Panchayat correspondence you hold",
"  - Notes of dates/times you have personally observed the noise",
"",
"=================================================================",
"RUNNING TOTALS (as of 14 June 2026)",
"=================================================================",
"",
"  Officials / departments notified:  ~69 (now re-notified pre-inspection)",
"  Press contacts engaged:            ~234 (4 waves; today = comment request)",
"  MLAs written to:                   19",
"  Civic organisations:               included in today's press wave",
"  Official replies received:         1 (VP Siolim-Marna -- jurisdiction)",
"  Verified hard bounces:             3 (generic Hindustan Times addresses)",
"  Inspection:                        17 June 2026, 11:30 AM",
"  RTI responses due:                 9 July 2026",
"",
"The momentum is strong and the whole official + press ecosystem is now on",
"notice three days out. Tomorrow's recordings are the one piece only you can",
"supply -- everything else is in motion.",
"",
"Regards,",
"PressDetective",
"On behalf of Olympio Almeida",
"olympio.almeida@pressdetective.com",
]

msg = MIMEMultipart("alternative")
msg["Subject"] = "Olympio Siolim Case -- Day 4 Update (14 June) + Your Sunday Video Task (3 days to inspection)"
msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
msg["To"]      = "gavora@gmail.com"
msg["Cc"]      = CC_INFO
msg.attach(MIMEText("\n".join(lines), "plain", "utf-8"))

try:
    send(msg)
    print("Gautam Day 4 update -- OK -> gavora@gmail.com")
except Exception as e:
    print(f"Gautam Day 4 update -- FAILED: {e}")
