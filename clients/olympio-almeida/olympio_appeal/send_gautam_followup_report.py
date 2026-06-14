"""Gautam follow-up delivery report (14 June) — PressDetective Proton ONLY."""
import json, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))
FROM_ADDR="olympio.almeida@pressdetective.com"; FROM_NAME="Olympio Almeida"
TOKEN=CREDS["accounts"]["olympio"]["token"]; CC_INFO="info@pressdetective.com"
assert FROM_ADDR.endswith("@pressdetective.com")

def send(msg):
    rc=[]
    for h in ("To","Cc","Bcc"):
        if msg.get(h): rc+=[a.strip() for a in msg[h].split(",")]
    ctx=ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
        s.sendmail(FROM_ADDR,rc,msg.as_bytes())

lines=[
"Dear Gautam,",
"",
"Follow-up report (Saturday 14 June). Short version: the campaign is on track",
"for Tuesday, and the bodies that actually run the inspection have received",
"everything. Full detail below.",
"",
"=================================================================",
"TODAY'S FOLLOW-UP — WHAT WAS SENT AND WHAT LANDED",
"=================================================================",
"",
"We sent a pre-inspection reminder to all 210 cleaned contacts (departments,",
"MLAs, press and civic groups). 142 were delivered. The ones that matter most",
"all received it:",
"",
"  DELIVERED — the inspection bodies:",
"   - Village Panchayat Siolim-Sodiem (the office ORGANISING the 17 June",
"     inspection) — received.",
"   - Goa State Pollution Control Board, working address — received.",
"   - The neighbouring Panchayat that already replied — received.",
"   - All verified Goa press and civic groups, and the area MLAs' offices.",
"",
"=================================================================",
"ONE HONEST LIMITATION — THE NIC GOVERNMENT ADDRESSES",
"=================================================================",
"",
"39 of the central government email addresses (the Collector, the IGP and the",
"police @goapolice.gov.in, GSPCB's @nic.in address, Town & Country Planning,",
"the directorates) sit behind the National Informatics Centre's mail gateway",
"(mx.mgovcloud.in). That gateway rejects mail from outside private email",
"systems as a matter of policy — it is not something we can change from our",
"side, and it affects everyone who emails them from a non-government address.",
"",
"Why this is NOT a problem for Tuesday:",
"  - The Panchayat that called the inspection, and GSPCB (the co-inspector),",
"    were both reached on their working addresses.",
"  - The inspection itself is IN PERSON on Tuesday, so the Collector / Police /",
"    TCP are reached there in the manner that actually counts.",
"",
"For the formal paper record with those NIC offices, the right channels are a",
"hand-delivered or posted letter and the GSPCB online grievance portal — we can",
"prepare those next week so there is a dated, signed record on file.",
"",
"=================================================================",
"LIST HYGIENE",
"=================================================================",
"",
"We also found and removed 18 more invalid press addresses that had been padding",
"the list. The contact database is steadily getting cleaner and more honest.",
"",
"=================================================================",
"TOMORROW (SUNDAY 15 JUNE) — STILL THE KEY DAY, AND IT'S ON YOU",
"=================================================================",
"",
"Tuesday's inspection is at 11:30 AM, when the courts are usually quiet. The",
"noise peaks on SUNDAYS. So tomorrow's recordings are the single most important",
"piece of evidence, and only you can capture them:",
"",
"  1. Record 3-4 short clips (1-2 min) between 10 AM and 2 PM tomorrow.",
"  2. Keep a decibel-meter app visible ON SCREEN (NIOSH SLM or Decibel X, free).",
"  3. Make sure each clip shows the phone's date/time.",
"  4. Film from a few spots: terrace/garden, boundary wall, and indoors with a",
"     window open.",
"",
"Send them to me by Sunday evening and we will table them at the inspection.",
"As always, your name and contact never appear anywhere — you are only ever",
"'a neighbouring resident'.",
"",
"=================================================================",
"TUESDAY 17 JUNE — LOGISTICS",
"=================================================================",
"",
"  Time:  11:30 AM (arrive by 11:15 AM)",
"  Venue: Village Panchayat Siolim-Sodiem office",
"  Bring: your March complaint copy, your Sunday videos, any GSPCB/Panchayat",
"         letters you hold, and notes of dates/times you have observed the noise.",
"",
"We are in good shape. The organisers have it, the press has it, and the one",
"thing still outstanding is tomorrow's recordings.",
"",
"Regards,",
"PressDetective",
"On behalf of Olympio Almeida",
"olympio.almeida@pressdetective.com",
]

msg=MIMEMultipart("alternative")
msg["Subject"]="Olympio Siolim Case — Follow-up Delivered (14 June): organisers reached, Tuesday on track, your Sunday task"
msg["From"]=f"{FROM_NAME} <{FROM_ADDR}>"; msg["To"]="gavora@gmail.com"; msg["Cc"]=CC_INFO
msg.attach(MIMEText("\n".join(lines),"plain","utf-8"))
try:
    send(msg); print("Gautam follow-up report — OK -> gavora@gmail.com")
except Exception as e:
    print(f"FAILED: {e}")
