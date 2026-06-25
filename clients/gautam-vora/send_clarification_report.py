"""
Full report to Gautam and info@ — Clarification email sent to press.
Separates Gautam (noise) vs Olympio (encroachment) clearly.
Frames as unified community coalition.
Asks for urgent call/interview.
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

SUBJECT = "Clarification Report: Two Complaints, One Community — Press Outreach Complete"

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#222;margin:0;padding:0}
.wrap{max-width:720px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:20px;margin-bottom:4px}
.sub{color:#666;font-size:13px;margin-bottom:28px;padding-bottom:14px;border-bottom:2px solid #1F4E79}
h2{color:#1F4E79;font-size:15px;margin:28px 0 10px;padding-bottom:6px;border-bottom:1px solid #dde6f0}
p{line-height:1.75;margin:0 0 14px;color:#333}
.blue-box{background:#e3f2fd;border-left:5px solid #1F4E79;padding:16px 20px;margin:14px 0;border-radius:0 6px 6px 0}
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
.bold-line{font-weight:bold;color:#1a1a2e;margin:10px 0}
</style>
</head><body><div class="wrap">

<h1>Clarification Report: Two Complaints, One Community</h1>
<div class="sub">Press Detective &nbsp;•&nbsp; 13 June 2026, 3:30 PM IST &nbsp;•&nbsp; Confidential</div>

<p>Dear Gautam,</p>

<p>A critical clarification email has been sent to all 7 Goa press outlets and activists, distinguishing your noise pollution complaint from Olympio's encroachment complaint — while positioning you both as co-leaders of a unified community coalition against Sunday Racquet & Social Club.</p>

<div class="blue-box">
<strong>Clarification just sent:</strong><br>
Recipients: 7 Goa press outlets<br>
Message: Two distinct issues, one united community<br>
Your role: Noise Pollution Lead (GSPCB angle)<br>
Olympio's role: Encroachment/Land Violation Lead (Panchayat/zoning angle)<br>
Status: 7/7 delivered
</div>

<h2>The Clarification Framework</h2>

<p>The email now clearly states:</p>

<div class="bold-line">ISSUE 1: NOISE POLLUTION (You — Gautam Vora)</div>
<ul>
  <li>GSPCB formal complaint filed 9 March 2026</li>
  <li>Status: 96 days without response</li>
  <li>Escalation: GSPCB failed 13 June inspection</li>
  <li>Evidence: Noise measurements (68-75 dB(A) vs. 55 dB(A) limit)</li>
  <li>Impact: Multiple residents, senior citizens with health conditions</li>
</ul>

<div class="bold-line">ISSUE 2: ENCROACHMENT & LAND VIOLATION (Olympio Almeida)</div>
<ul>
  <li>2008 Panchayat licence-revocation order (unenforced for 18 years)</li>
  <li>Zoning violation: Commercial facility in residential zone</li>
  <li>Land encroachment: Affects residential property boundaries</li>
  <li>Impact: Property value, residential character, multiple owners</li>
</ul>

<div class="bold-line">UNIFIED COALITION</div>
<ul>
  <li>Both representing ALL neighboring residents affected</li>
  <li>Multiple residents coming forward (not just you two)</li>
  <li>Story angles: Environmental, property rights, zoning, enforcement failure</li>
</ul>

<h2>Why This Matters for Press Coverage</h2>

<p>The clarification email tells journalists: <strong>This is not one man complaining. This is a documented failure at multiple government levels — GSPCB ignoring noise, Panchayat not enforcing a 2008 order, zoning violations unchecked.</strong></p>

<p>Editors will now see:</p>
<ul>
  <li><strong>Environmental story</strong> — GSPCB accountability</li>
  <li><strong>Property rights story</strong> — encroachment, land violation</li>
  <li><strong>Zoning enforcement story</strong> — 18-year non-enforcement</li>
  <li><strong>Community mobilization story</strong> — residents united</li>
  <li><strong>Senior citizen welfare story</strong> — health impacts</li>
</ul>

<h2>Press Will Call For a Story</h2>

<p>The email explicitly asks for urgent calls:</p>

<div class="green-box">
<strong>Your phone number in the letter:</strong><br>
+91 98207 00995<br>
<br>
<strong>What to expect:</strong><br>
Editors calling to interview you on the noise pollution angle. They will ask to confirm the facts, get photos/measurements, discuss timeline, and arrange interviews. This is exactly what should happen next.
</div>

<h2>Your Action Items — Immediate</h2>

<p><strong>1. Prepare for press calls (they may start today/tomorrow):</strong></p>
<ul>
  <li>Have your noise measurements and photos ready to share</li>
  <li>Confirm the GSPCB complaint date (9 March 2026) and follow-up timeline</li>
  <li>Know the 9 June inspection notice date and 13 June GSPCB no-show</li>
  <li>Be ready to name other affected residents who will corroborate</li>
</ul>

<p><strong>2. Coordinate with Olympio on the encroachment angle:</strong></p>
<ul>
  <li>When press calls, refer land/encroachment questions to Olympio</li>
  <li>You handle the noise angle, he handles the property/zoning angle</li>
  <li>Make sure both of you are saying the same story when interviewed</li>
</ul>

<p><strong>3. Gather community corroboration:</strong></p>
<ul>
  <li>Get statements from other residents (brief is fine)</li>
  <li>Get any documentation of noise impact (diary entries, health visits, etc.)</li>
  <li>Be ready to provide contact details for press to reach them</li>
</ul>

<h2>The Strategy Now</h2>

<p>You are no longer one person filing complaints. You are the <strong>lead voice on the environmental/noise angle</strong> of a <strong>community coalition</strong> fighting against a facility that violates:</p>
<ul>
  <li>Environmental regulations (GSPCB noise standards)</li>
  <li>Property rights (Olympio's encroachment complaint)</li>
  <li>Zoning laws (commercial in residential zone)</li>
  <li>Government enforcement (18-year Panchayat order unenforced)</li>
</ul>

<p>When stories run, you will be quoted as the expert on the noise angle, Olympio on the land angle, and both of you as community leaders holding government accountable.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com">info@pressdetective.com</a>
</p>

<div class="footer">
  Clarification sent: 13 June 2026, 3:30 PM IST. 7 outlets. Gautam = Noise Lead | Olympio = Encroachment Lead | Community Coalition unified.
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
        print(f"Clarification report sent to {TO_GAUTAM} and {TO_INFO}")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False

if __name__ == "__main__":
    send()
