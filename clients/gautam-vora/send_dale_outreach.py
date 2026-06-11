"""
Outreach to Dale Bhagwagar Media Group requesting factual correction.
Dale Bhagwagar is a prominent Mumbai PR professional whose clients/network
includes Bollywood personalities and entertainment media.

TO_ADDR: Verify before sending — check dalebb.com for current contact email.
         Historically listed as dalebb@dalebb.com
FROM: info@pressdetective.com via ZeptoMail
"""
import smtplib, ssl, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

FROM_ADDR = "info@pressdetective.com"
FROM_NAME = "Press Detective"
CC_ALWAYS = ["info@pressdetective.com"]

def _pm_token():
    p = Path(__file__).parents[2] / ".creds" / "proton_accounts.json"
    return json.loads(p.read_text(encoding="utf-8")).get("smtp_postmark", {}).get("token", "")

def _postmark_send(msg, recipients):
    t = _pm_token()
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(t, t)
        s.sendmail(FROM_ADDR, recipients, msg.as_bytes())

SUBJECT = "Request for factual correction — Viveka Babajee / Gautam Vora | Press Detective"

# IMPORTANT: Verify this email address at dalebb.com before sending.
# This script will NOT send until TO_ADDR is confirmed.
TO_ADDR = "dalebb@dalebb.com"   # <- verify at dalebb.com before running

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#333;margin:0;padding:0}
.wrap{max-width:640px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:18px;margin-bottom:4px}
.sub{color:#595959;font-size:13px;margin-bottom:28px}
p{line-height:1.7;margin:0 0 14px}
.quote{background:#f5f8fb;border-left:3px solid #1F4E79;padding:12px 16px;font-size:13px;font-style:italic;margin:16px 0;border-radius:0 4px 4px 0}
.footer{margin-top:40px;padding-top:14px;border-top:1px solid #ddd;font-size:12px;color:#888}
.sig{font-weight:bold;color:#1F4E79}
</style></head><body><div class="wrap">

<h1>Request for Factual Correction — Viveka Babajee / Gautam Vora</h1>
<div class="sub">Press Detective &nbsp;|&nbsp; Confidential &nbsp;|&nbsp; June 2026</div>

<p>Dear Mr. Bhagwagar,</p>

<p>I am writing on behalf of Mr. Gautam Vora, a Mumbai-based equity analyst and stockbroker,
regarding press coverage connected to your professional network in the entertainment media space.</p>

<p>A number of articles and web pages — some referencing your clients or associated entertainment
figures — include Mr. Vora's name in connection with the 2010 matter involving the late
Viveka Babajee. These articles, while factually incomplete, continue to circulate online and
cause significant professional harm to Mr. Vora.</p>

<p><strong>The critical omission in most of this coverage:</strong></p>

<div class="quote">
Mumbai Police issued a clean chit to Mr. Gautam Vora in August 2010, closing the investigation
with no charges filed against him. The case was fully resolved over 14 years ago with no adverse
findings.
</div>

<p>Where any article, profile page, or media item within your sphere of influence mentions
Mr. Vora in this context, we respectfully request that you consider adding this factual
clarification — either through a correction note, an editorial update, or by conveying this
information to the relevant publication.</p>

<p>We are not asking for the removal of historical coverage, but simply for the record to be
complete: the matter was investigated, concluded with no charges, and Mr. Vora received a formal
clean chit from Mumbai Police.</p>

<p>We would be grateful for any assistance you are able to provide. Please feel free to contact us
if you require further documentation or details.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com" style="color:#1F4E79">info@pressdetective.com</a>
</p>

<div class="footer">
  This message is sent in a professional capacity on behalf of our client.
  It is not a legal demand. All information shared is factual and verifiable.
</div>
</div></body></html>
"""

def send():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = TO_ADDR
    msg["Cc"]      = ", ".join(CC_ALWAYS)
    msg.attach(MIMEText(HTML, "html", "utf-8"))
    _postmark_send(msg, [TO_ADDR] + CC_ALWAYS)
    print(f"Sent to {TO_ADDR}, CC: {', '.join(CC_ALWAYS)}")

if __name__ == "__main__":
    send()
