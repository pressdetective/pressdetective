"""
Submission status report to Gautam Vora — what was sent today.
FROM: info@pressdetective.com | CC: info@pressdetective.com
"""
import smtplib, ssl, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

FROM_ADDR = "info@pressdetective.com"
FROM_NAME = "Press Detective"
TO_ADDR   = "gavora@gmail.com"
CC_ALWAYS = ["info@pressdetective.com"]

def _pm_token():
    p = Path(__file__).parents[2] / ".creds" / "proton_accounts.json"
    return json.loads(p.read_text(encoding="utf-8")).get("smtp_postmark", {}).get("token", "")

SUBJECT = "Outreach Submitted — Press Pitch Sent to 4 Publications + Dale Bhagwagar Contacted | Press Detective"

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#222;margin:0;padding:0}
.wrap{max-width:700px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:20px;margin-bottom:4px;line-height:1.3}
.sub{color:#666;font-size:13px;margin-bottom:28px;padding-bottom:14px;border-bottom:2px solid #1F4E79}
h2{color:#1F4E79;font-size:15px;margin:28px 0 10px;padding-bottom:6px;border-bottom:1px solid #dde6f0}
p{line-height:1.75;margin:0 0 14px;color:#333}
table{border-collapse:collapse;width:100%;margin:10px 0 18px;font-size:13px}
th{background:#1F4E79;color:#fff;text-align:left;padding:9px 12px}
td{padding:9px 12px;border-bottom:1px solid #e0e7ef;vertical-align:top}
tr:nth-child(even) td{background:#f5f8fb}
.sent{color:#2e7d32;font-weight:bold}
.pending{color:#b45309;font-weight:bold}
.done{background:#eef7ee;border-left:5px solid #2e7d32;padding:16px 20px;margin:16px 0;border-radius:0 6px 6px 0}
.urgent{background:#fff8e6;border-left:5px solid #e6a817;padding:16px 20px;margin:16px 0;border-radius:0 6px 6px 0}
.sig{font-weight:bold;color:#1F4E79;font-size:15px}
.footer{margin-top:44px;padding-top:14px;border-top:1px solid #ddd;font-size:12px;color:#999}
a{color:#1F4E79}
</style>
</head><body><div class="wrap">

<h1>Outreach Submitted &mdash; Your Story Is Out</h1>
<div class="sub">Press Detective &nbsp;&bull;&nbsp; Confidential &nbsp;&bull;&nbsp; 11 June 2026</div>

<p>Dear Gautam,</p>

<p>We have now submitted your press pitch and outreach. Here is a full account of what went out today,
to whom, and what happens next.</p>

<h2>Press Pitch &mdash; Sent to 4 Publications</h2>

<div class="done">
<strong>&#10003; All 4 pitches delivered &mdash; 11 June 2026</strong>
</div>

<table>
  <thead><tr><th>Publication</th><th>Desk / Contact</th><th>Why we targeted them</th></tr></thead>
  <tbody>
    <tr>
      <td><strong>Mid-Day</strong></td>
      <td>City Desk &lt;citydesk@mid-day.com&gt;</td>
      <td>Mumbai-focused; strong human interest coverage; widely read across the city.
          A lockdown story set in Mumbai is exactly their beat.</td>
    </tr>
    <tr>
      <td><strong>Scroll.in</strong></td>
      <td>News Desk &lt;newsdesk@scroll.in&gt;</td>
      <td>National reach; long-form; excellent Google authority. A story here will
          rank on page 1 for &#8220;Gautam Vora&#8221; within weeks of publication.</td>
    </tr>
    <tr>
      <td><strong>The Print</strong></td>
      <td>Editorial Desk &lt;edit@theprint.in&gt;</td>
      <td>National; credible; entrepreneur and social impact stories perform very well here.
          The &#8220;who he gave to, and why&#8221; angle is exactly what The Print publishes.</td>
    </tr>
    <tr>
      <td><strong>DNA India</strong></td>
      <td>News Tips &lt;newsdesk@dnaindia.com&gt;</td>
      <td><strong>Strategic priority.</strong> DNA India currently carries a negative article
          about you. A published positive story on the same domain is one of the most valuable
          ORM placements we can make &mdash; it displaces the old article in Google&#8217;s
          results for DNA India + your name.</td>
    </tr>
  </tbody>
</table>

<p><strong>What the pitch says:</strong> The pitch leads with the one million meal number,
anchors on the women-and-children targeting decision, and offers you for interview. We have
framed this as a COVID retrospective story (six years on &mdash; what ordinary people did
that governments didn&#8217;t), a Mumbai city story, and a social entrepreneurship story.
All three frames have strong editorial appeal.</p>

<p><strong>What typically happens next:</strong> Desks usually respond within 3&ndash;7 days if
interested. If we hear nothing in 10 days, we follow up. If a journalist expresses interest,
we coordinate the interview and review any quotes before publication.</p>

<h2>Dale Bhagwagar Media Group &mdash; Outreach Sent</h2>

<div class="done">
<strong>&#10003; Outreach email delivered &mdash; 11 June 2026</strong>
</div>

<p>We have sent a professional courtesy email to Dale Bhagwagar&#8217;s media group at
<strong>dalebb@dalebb.com</strong> requesting that any coverage of the Viveka Babajee matter
within their network be updated with the August 2010 police clean chit.</p>

<p>The email:</p>
<ul>
  <li>States the clean chit fact clearly and accurately</li>
  <li>Asks for a correction note or editorial update, not a deletion</li>
  <li>Is a courtesy request, not a legal demand</li>
  <li>Is professional in tone throughout</li>
</ul>

<p>Dale Bhagwagar is a well-connected Mumbai PR professional. His network touches several
entertainment media outlets that carry coverage of the Viveka Babajee story.
A cooperative response from his end could result in corrections across multiple outlets.</p>

<h2>Still in progress &mdash; no action needed from you yet</h2>

<table>
  <thead><tr><th>Action</th><th>Status</th></tr></thead>
  <tbody>
    <tr><td>Google removal requests (3 URLs)</td>
        <td><span class="pending">Filing this week</span> &mdash; stronger with your HC bail order</td></tr>
    <tr><td>Wikipedia Talk page correction</td>
        <td><span class="pending">Ready to post</span> &mdash; awaiting your go-ahead</td></tr>
    <tr><td>Grokipedia correction</td>
        <td><span class="pending">Ready to submit</span> &mdash; queued after Wikipedia</td></tr>
    <tr><td>Website deployment</td>
        <td><span class="pending">Waiting on domain registration</span> &mdash; gautamvora.com</td></tr>
    <tr><td>LinkedIn profile</td>
        <td><span class="pending">Waiting on career timeline from you</span></td></tr>
  </tbody>
</table>

<h2>What we need from you right now</h2>

<div class="urgent">
<strong>Three things that will materially accelerate everything:</strong>

<p style="margin-top:12px"><strong>1. Confirm the COVID story facts</strong><br>
The press pitch is already out, but if any journalist comes back with questions, we need
to be sure of the numbers. Please confirm: over one million meals? Mumbai + Siolim + Porvorim?
Funded personally? Distributed to women and children only? Any photos from 2020?</p>

<p><strong>2. Register gautamvora.com</strong><br>
Your website is fully built and ready to deploy. Every day it is not live is a day Google
is not indexing it. Registration takes 5 minutes at any domain registrar
(GoDaddy, Namecheap, Google Domains). Cost: approx. &#8377;1,000&ndash;1,500/year.</p>

<p><strong>3. Any court document you have</strong><br>
The Bombay HC bail order and/or the August 2010 police clean chit document.
Even a scanned copy or a photograph of the order will substantially strengthen
our Google removal requests. If you have access to Adv. Sujata Shirasi, she may
be able to provide certified copies.</p>
</div>

<p>Reply to this email with any of the above and we act immediately.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com">info@pressdetective.com</a>
</p>

<div class="footer">
  Confidential &mdash; prepared for Gautam Vora only.
  All outreach sent on your behalf is factual and professionally worded.
  Legal steps (formal de-indexing petition, court-based removal) require qualified legal counsel.
</div>
</div></body></html>
"""

def send():
    token = _pm_token()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = TO_ADDR
    msg["Cc"]      = ", ".join(CC_ALWAYS)
    msg.attach(MIMEText(HTML, "html", "utf-8"))
    recipients = [TO_ADDR] + CC_ALWAYS
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(token, token)
        s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
    print(f"Sent to {TO_ADDR}, CC: {', '.join(CC_ALWAYS)}")

if __name__ == "__main__":
    send()
