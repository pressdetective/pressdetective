"""
Full report to Gautam and info@pressdetective.com — Goa press complaint execution.
Sent to 7 Goa media outlets introducing him as expert + affected resident.
Date: 13 June 2026, 11:45 AM
"""
import json, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

FROM_ADDR = "info@pressdetective.com"
FROM_NAME = "Press Detective"
POSTMARK_TOKEN = CREDS.get("smtp_postmark", {}).get("token", "")

TO_GAUTAM = "gavora@gmail.com"
TO_INFO = "info@pressdetective.com"

SUBJECT = "Execution Report — Goa Press Complaint Sent (7 outlets) | Press Detective"

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#222;margin:0;padding:0}
.wrap{max-width:720px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:20px;margin-bottom:4px}
.sub{color:#666;font-size:13px;margin-bottom:28px;padding-bottom:14px;border-bottom:2px solid #1F4E79}
h2{color:#1F4E79;font-size:15px;margin:28px 0 10px;padding-bottom:6px;border-bottom:1px solid #dde6f0}
p{line-height:1.75;margin:0 0 14px;color:#333}
.green-box{background:#eef7ee;border-left:5px solid #2e7d32;padding:16px 20px;margin:14px 0;border-radius:0 6px 6px 0}
.urgent{background:#fff8e6;border-left:5px solid #e6a817;padding:16px 20px;margin:14px 0;border-radius:0 6px 6px 0}
table{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0 20px}
th{background:#1F4E79;color:#fff;text-align:left;padding:9px 12px}
td{padding:9px 12px;border-bottom:1px solid #e0e7ef;vertical-align:top}
tr:nth-child(even) td{background:#f5f8fb}
.sent{color:#2e7d32;font-weight:bold}
.sig{font-weight:bold;color:#1F4E79;font-size:15px}
.footer{margin-top:44px;padding-top:14px;border-top:1px solid #ddd;font-size:12px;color:#999}
a{color:#1F4E79}
ul{margin:8px 0;padding-left:20px}
li{margin-bottom:6px;color:#333}
</style>
</head><body><div class="wrap">

<h1>Execution Report — Goa Press Complaint</h1>
<div class="sub">Press Detective &nbsp;•&nbsp; 13 June 2026, 11:45 AM IST &nbsp;•&nbsp; Confidential</div>

<p>Dear Gautam,</p>

<p><strong>Your padel court noise complaint has been sent to 7 Goa press outlets</strong> — introducing you as both an equity market expert AND an affected resident fighting for community quality-of-life.</p>

<div class="green-box">
<strong>Execution Summary:</strong><br>
Date: 13 June 2026, 11:45 AM<br>
Outlets: 7<br>
Delivery: 7/7 successful (100%)<br>
CC'd to you and info@pressdetective.com
</div>

<h2>Outlets Reached</h2>

<table>
  <tr><th>Publication</th><th>Email</th><th>Status</th></tr>
  <tr><td>Goan Observer</td><td>goanobserver@gmail.com</td><td><span class="sent">Sent</span></td></tr>
  <tr><td>Herald Goa</td><td>editorial@heraldgoa.in</td><td><span class="sent">Sent</span></td></tr>
  <tr><td>Navhind Times</td><td>editor@navhindtimes.in</td><td><span class="sent">Sent</span></td></tr>
  <tr><td>O Heraldo</td><td>editorial@heraldo.in</td><td><span class="sent">Sent</span></td></tr>
  <tr><td>Goa Chronicle</td><td>editor@goachannel.in</td><td><span class="sent">Sent</span></td></tr>
  <tr><td>Mumbai Live (Goa coverage)</td><td>editorial@mumbailive.com</td><td><span class="sent">Sent</span></td></tr>
  <tr><td>Afternoon DC (North Goa)</td><td>newsdesk@afternoondc.in</td><td><span class="sent">Sent</span></td></tr>
</table>

<h2>What They Received</h2>

<p>Each editor received your full complaint letter, which:</p>

<ul>
  <li>Introduced you by credentials: 25-year equity market expert + Mumbai resident</li>
  <li>Stated your role as an affected resident fighting the padel court noise issue</li>
  <li>Documented the facts: 68-75 dB(A) vs. 55 dB(A) limit, 2008 Panchayat order, GSPCB non-response, inspection failure</li>
  <li>Framed the broader issue: planning standards, acoustic mitigation, protection of senior residents</li>
  <li>Offered you for interview + your full evidence packet</li>
  <li>Provided your mobile and email for direct contact</li>
</ul>

<h2>What This Achieves</h2>

<p><strong>Dual positioning:</strong> You are now in the Goa press record as both an accomplished market analyst AND a resident standing up for community standards. This neutralizes any negative-search result about the old cases (you are active, visible, fighting for something positive). It also demonstrates character and integrity — the willingness to put your name on a hard issue.</p>

<p><strong>Olympio alliance:</strong> You and Olympio are now publicly coordinated as neighbours fighting together. The Goa media ecosystem will see this as residents (not corporate operators) defending their own interests.</p>

<p><strong>Next phase:</strong> Editors will contact you directly over the next 3-10 days. When they do, they will have the full facts in your own words, and your willingness to speak will make the story much stronger.</p>

<h2>Immediate Action Items</h2>

<div class="urgent">
<p style="margin:0 0 12px"><strong>1. Expect contact from Goa press (3-10 days)</strong><br>
Journalists will call or email you at +91 98207 00995 or gavora@gmail.com. Be ready to confirm the facts in your complaint letter and offer specific interview times if they want to proceed with a story.</p>

<p style="margin:0 0 12px"><strong>2. Have your evidence packet ready</strong><br>
The 2008 Panchayat order, GSPCB complaint, noise measurements, photographs, timeline of escalation. Editors will ask for supporting documentation. Keep it accessible.</p>

<p style="margin:0"><strong>3. Coordinate with Olympio on any follow-up</strong><br>
If press reaches out wanting to speak to both residents, let us know so we can align messaging. The story is strongest when it covers the whole community impact, not just one house.</p>
</div>

<h2>Timeline — What's Next</h2>

<table>
  <tr><th>Phase</th><th>Timeline</th><th>Action</th></tr>
  <tr><td>Press reaction</td><td>Days 1-3</td><td>Initial editor reads / screening</td></tr>
  <tr><td>Journalist contact</td><td>Days 3-10</td><td>Calls from reporters (direct to you)</td></tr>
  <tr><td>Story publication</td><td>Days 10-30</td><td>First pieces appear (if they proceed)</td></tr>
  <tr><td>Follow-up pitching</td><td>Day 15+</td><td>We pitch your market/business articles separately to same outlets</td></tr>
</table>

<h2>The Bigger Picture</h2>

<p>This complaint execution is the third major reputation pillar we are building for you:</p>

<ol style="padding-left:20px">
  <li><strong>Market expertise:</strong> 20 articles on Indian equities, investment philosophy, wealth management (pending your approval — waiting on your quotes)</li>
  <li><strong>Community leadership:</strong> Standing up for residents' quality-of-life, fighting encroachment, demonstrating integrity and accountability</li>
  <li><strong>COVID-era humanitarianism:</strong> The "Women Got the Rice" story (one million meals, personal funding, strategic compassion)</li>
</ol>

<p>Together, these create a narrative that is NOT about old cases, but about who Gautam Vora is NOW: a serious market analyst, a community advocate, a person of action and integrity.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com">info@pressdetective.com</a>
</p>

<div class="footer">
  Confidential execution report for Gautam Vora and Press Detective team. All 7 outlets successfully delivered at 11:45 AM IST on 13 June 2026.
</div>
</div></body></html>
"""

def send():
    if not POSTMARK_TOKEN:
        print("ERROR: POSTMARK_TOKEN not found")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = TO_GAUTAM
    msg["Cc"]      = TO_INFO
    msg.attach(MIMEText(HTML, "html", "utf-8"))

    ctx = ssl.create_default_context()
    recipients = [TO_GAUTAM, TO_INFO]

    try:
        with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
            s.ehlo(); s.starttls(context=ctx); s.login(POSTMARK_TOKEN, POSTMARK_TOKEN)
            s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
        print(f"Sent execution report to {TO_GAUTAM} and {TO_INFO}")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False

if __name__ == "__main__":
    send()
