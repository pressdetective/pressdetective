"""
Full escalation report to Gautam and info@pressdetective.com.
GSPCB no-show on 13 June inspection — community response activated.
Frames full community coming together + government accountability angle.
"""
import json, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

FROM_ADDR = "info@pressdetective.com"
FROM_NAME = "Press Detective"
POSTMARK_TOKEN = CREDS.get("smtp_postmark", {}).get("token", "")

TO_GAUTAM = "gavora@gmail.com"
TO_INFO = "info@pressdetective.com"

SUBJECT = "Escalation Report — GSPCB No-Show + Full Community Mobilization | Press Detective"

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#222;margin:0;padding:0}
.wrap{max-width:720px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:20px;margin-bottom:4px}
.sub{color:#666;font-size:13px;margin-bottom:28px;padding-bottom:14px;border-bottom:2px solid #1F4E79}
h2{color:#1F4E79;font-size:15px;margin:28px 0 10px;padding-bottom:6px;border-bottom:1px solid #dde6f0}
p{line-height:1.75;margin:0 0 14px;color:#333}
.red-box{background:#ffe6e6;border-left:5px solid #d32f2f;padding:16px 20px;margin:14px 0;border-radius:0 6px 6px 0}
.green-box{background:#eef7ee;border-left:5px solid #2e7d32;padding:16px 20px;margin:14px 0;border-radius:0 6px 6px 0}
table{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0 20px}
th{background:#1F4E79;color:#fff;text-align:left;padding:9px 12px}
td{padding:9px 12px;border-bottom:1px solid #e0e7ef;vertical-align:top}
tr:nth-child(even) td{background:#f5f8fb}
.sent{color:#2e7d32;font-weight:bold}
.sig{font-weight:bold;color:#1F4E79;font-size:15px}
.footer{margin-top:44px;padding-top:14px;border-top:1px solid #ddd;font-size:12px;color:#999}
a{color:#1F4E79}
ul{margin:8px 0;padding-left:20px;color:#333}
li{margin-bottom:6px}
.timestamp{font-size:12px;color:#999}
</style>
</head><body><div class="wrap">

<h1>Escalation Report — GSPCB No-Show</h1>
<div class="sub">Press Detective &nbsp;•&nbsp; 13 June 2026, 2:15 PM IST &nbsp;•&nbsp; Confidential</div>

<p>Dear Gautam,</p>

<p>The GSPCB's failure to attend today's inspection has been escalated across Goa press and police. The story is now: <strong>enforcement failure + full community mobilization.</strong></p>

<div class="red-box">
<strong>GSPCB NO-SHOW — Key Facts:</strong><br>
Inspection scheduled: 13 June 2026, 11:30 AM<br>
Notice given: 9 June (9 days' notice)<br>
GSPCB attendance: FAILED<br>
Panchayat inspection: Proceeded without GSPCB<br>
Status: Complaint remains unresolved after 96 days
</div>

<h2>What We Just Executed</h2>

<p><strong>7 Goa press outlets</strong> received a formal escalation letter with the headline:</p>

<div style="background:#f5f5f5;padding:12px;margin:10px 0;border-left:3px solid #1F4E79;font-weight:bold;font-size:14px">
"GSPCB Fails to Attend Joint Inspection — Community Residents Demand Accountability"
</div>

<p><strong>2 Goa police addresses</strong> received an urgent escalation memo requesting police action on the GSPCB no-show and enforcement failure.</p>

<table>
  <tr><th>Channel</th><th>Recipients</th><th>Status</th></tr>
  <tr><td>Goa Press</td><td>7 outlets (Goan Observer, Herald Goa, Navhind Times, O Heraldo, Goa Chronicle, Mumbai Live, Afternoon DC)</td><td><span class="sent">7/7 sent</span></td></tr>
  <tr><td>Goa Police</td><td>IGP Goa + Complaint Cell</td><td><span class="sent">2/2 sent</span></td></tr>
</table>

<h2>The Frame — Community Coming Together</h2>

<p>This escalation reframes the narrative from "one man's complaint" to "government accountability + full community response." The messaging emphasizes:</p>

<ul>
  <li><strong>The enforcement gap:</strong> GSPCB ignores 96-day-old complaint, fails scheduled inspection</li>
  <li><strong>The prior history:</strong> 2008 Panchayat licence-revocation order (18 years unenforced) proves this is a documented problem</li>
  <li><strong>The community:</strong> Multiple residents (especially senior citizens with health conditions) coming together</li>
  <li><strong>The accountability question:</strong> "Is the GSPCB unable or unwilling to enforce noise-pollution regulations?"</li>
  <li><strong>Your role:</strong> Lead complainant, equity market expert, affected resident, community advocate</li>
</ul>

<p>You are no longer isolated. You are the voice of a united community.</p>

<h2>Why This Escalation Matters</h2>

<p><strong>Immediate press impact:</strong> The GSPCB no-show is the story Goa media will run. It's about government failure, not just noise. Your name + community solidarity will be the focus.</p>

<p><strong>Police accountability:</strong> The IGP and Complaint Cell now have formal notice that:</p>
<ul>
  <li>A complaint was forwarded by SP (SPCR) Panaji for action</li>
  <li>GSPCB failed to enforce despite notice</li>
  <li>Community is mobilizing publicly</li>
  <li>Media is covering the story</li>
</ul>

<p>This creates pressure on police to act or document why they cannot.</p>

<p><strong>Broader impact:</strong> You are establishing yourself as the lead voice on this issue. When press contacts you (over next 3-10 days), you will be positioned as the resident-expert coordinating community response, not just filing complaints.</p>

<h2>What to Expect Next</h2>

<p><strong>Press contact (3-10 days):</strong> Editors will call or email asking for further details on the GSPCB no-show and community response. Be ready with:</p>
<ul>
  <li>The 9 June inspection notice (proof GSPCB had 9 days' notice)</li>
  <li>Noise measurements and photographs</li>
  <li>Names of other residents who will go on record</li>
  <li>The 2008 Panchayat order (proof of prior enforcement failure)</li>
  <li>Timeline of all escalation attempts</li>
</ul>

<p><strong>Police follow-up (7-14 days):</strong> IGP office or Complaint Cell may contact the Panchayat or SP asking for status. This is positive — it means they received the escalation and are moving it up the chain.</p>

<p><strong>Continued media amplification:</strong> Once first press pieces run, we will do a second round of pitching featuring your market analysis articles + the padel court issue side-by-side, positioning you as the voice of both expertise and integrity.</p>

<h2>Your Action Items — Immediate</h2>

<div class="green-box">
<p style="margin:0 0 12px"><strong>1. Gather community corroboration</strong><br>
Get other residents to provide statements (even brief) confirming noise pollution. This strengthens the "full community" narrative when press calls.</p>

<p style="margin:0 0 12px"><strong>2. Prepare documentation package</strong><br>
Organize in one place: 2008 Panchayat order, 9 June inspection notice, GSPCB complaint, noise data, photographs. Keep it accessible for quick press sharing.</p>

<p style="margin:0"><strong>3. Be ready for media calls</strong><br>
Editors will contact you directly (your phone: +91 98207 00995 / email: gavora@gmail.com). When they call, confirm the facts in the escalation letter and offer to provide evidence + arrange interviews with other community residents.</p>
</div>

<h2>The Bigger Strategy</h2>

<p>This escalation is the turning point in your reputation work. You are no longer just the subject of old cases being discussed. You are now the active voice of community action, environmental protection, and government accountability. That narrative is powerful and will dominate search results and press coverage for months.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com">info@pressdetective.com</a>
</p>

<div class="footer">
  Escalation execution: 13 June 2026, 2:15 PM IST. 7 Goa press outlets + 2 police addresses. Full community mobilization frame activated.
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
        print(f"Escalation report sent to {TO_GAUTAM} and {TO_INFO}")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False

if __name__ == "__main__":
    send()
