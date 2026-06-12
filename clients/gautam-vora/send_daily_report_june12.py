"""
Daily report to Gautam Vora — 12 June 2026.
Press blitz summary + today's plan + action items.
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
    return json.loads(p.read_text(encoding="utf-8-sig")).get("smtp_postmark", {}).get("token", "")

SUBJECT = "Daily Update — 28 Publications Pitched, Google Removal Filing Today | Press Detective"

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#222;margin:0;padding:0}
.wrap{max-width:700px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:20px;margin-bottom:4px;line-height:1.3}
.sub{color:#666;font-size:13px;margin-bottom:28px;padding-bottom:14px;border-bottom:2px solid #1F4E79}
h2{color:#1F4E79;font-size:15px;margin:28px 0 10px;padding-bottom:6px;border-bottom:1px solid #dde6f0}
p{line-height:1.75;margin:0 0 14px;color:#333}
table{border-collapse:collapse;width:100%;margin:10px 0 20px;font-size:13px}
th{background:#1F4E79;color:#fff;text-align:left;padding:9px 12px}
td{padding:9px 12px;border-bottom:1px solid #e0e7ef;vertical-align:top}
tr:nth-child(even) td{background:#f5f8fb}
.sent{color:#2e7d32;font-weight:bold}
.pending{color:#b45309;font-weight:bold}
.green-box{background:#eef7ee;border-left:5px solid #2e7d32;padding:16px 20px;margin:14px 0;border-radius:0 6px 6px 0}
.urgent{background:#fff8e6;border-left:5px solid #e6a817;padding:16px 20px;margin:14px 0;border-radius:0 6px 6px 0}
.sig{font-weight:bold;color:#1F4E79;font-size:15px}
.footer{margin-top:44px;padding-top:14px;border-top:1px solid #ddd;font-size:12px;color:#999}
a{color:#1F4E79}
</style>
</head><body><div class="wrap">

<h1>Daily Update &mdash; 12 June 2026</h1>
<div class="sub">Press Detective &nbsp;&bull;&nbsp; Confidential &nbsp;&bull;&nbsp; Gautam Vora Reputation Clearance</div>

<p>Dear Gautam,</p>

<p>A large day of outreach. Here is everything that went out today and what is happening next.</p>

<h2>Press Blitz &mdash; 28 Publications Total</h2>

<div class="green-box">
<strong>Your COVID relief story has now been pitched to 28 publications and desks across
India &mdash; all sent in the last 24 hours.</strong>
</div>

<table>
  <thead><tr><th>Category</th><th>Publications</th><th>Status</th></tr></thead>
  <tbody>
    <tr>
      <td><strong>National digital</strong></td>
      <td>The Wire, The Quint, NDTV, News18, FirstPost, India Today,
          Outlook India, The Caravan, Scroll.in, The Print</td>
      <td><span class="sent">Sent</span></td>
    </tr>
    <tr>
      <td><strong>Business / finance</strong></td>
      <td>Livemint, DNA India</td>
      <td><span class="sent">Sent</span></td>
    </tr>
    <tr>
      <td><strong>Entrepreneur media</strong></td>
      <td>YourStory, Inc42, Entrepreneur India</td>
      <td><span class="sent">Sent</span></td>
    </tr>
    <tr>
      <td><strong>Print nationals</strong></td>
      <td>The Hindu (Mumbai), Times of India (2 desks),
          Hindustan Times (2 desks)</td>
      <td><span class="sent">Sent</span></td>
    </tr>
    <tr>
      <td><strong>Mumbai local</strong></td>
      <td>Mid-Day, Free Press Journal, Mumbai Live, Afternoon DC</td>
      <td><span class="sent">Sent</span></td>
    </tr>
    <tr>
      <td><strong>Goa media</strong></td>
      <td>Herald Goa, Navhind Times, O Heraldo, Goa Chronicle</td>
      <td><span class="sent">Sent</span></td>
    </tr>
    <tr>
      <td><strong>PR outreach</strong></td>
      <td>Dale Bhagwagar Media Group</td>
      <td><span class="sent">Sent</span></td>
    </tr>
  </tbody>
</table>

<p><strong>What each publication received:</strong> The full 1,400-word personal essay
&#8220;The Women Got the Rice&#8221; &mdash; complete and ready to publish as written,
with a pitch note explaining the story and offering you for interview. Editors can read
the entire piece in their inbox without clicking anywhere.</p>

<p><strong>Typical response time:</strong> 3&ndash;10 days. We follow up with any desk
that has not responded within 10 days. If a journalist wants to proceed, we coordinate
the interview and review any quotes before publication.</p>

<h2>Today&#8217;s Plan &mdash; What We Are Executing Now</h2>

<table>
  <thead><tr><th>Action</th><th>Status</th><th>Notes</th></tr></thead>
  <tbody>
    <tr>
      <td>Google removal request &mdash; Yahoo News</td>
      <td><span class="pending">Filing today</span></td>
      <td>Using the drafts already prepared. Stronger with HC bail order.</td>
    </tr>
    <tr>
      <td>Google removal request &mdash; Business Standard</td>
      <td><span class="pending">Filing today</span></td>
      <td>Incomplete record (only shows bail rejection, not HC grant).</td>
    </tr>
    <tr>
      <td>Google removal request &mdash; DNA India</td>
      <td><span class="pending">Filing today</span></td>
      <td>Factually inaccurate headline re: murder charge you were not facing.</td>
    </tr>
    <tr>
      <td>Wikipedia Talk page correction</td>
      <td><span class="pending">Posting this week</span></td>
      <td>COI-compliant request to add August 2010 clean chit to Viveka Babajee article.</td>
    </tr>
    <tr>
      <td>Grokipedia correction</td>
      <td><span class="pending">Submitting this week</span></td>
      <td>Email to editorial team requesting same addition.</td>
    </tr>
  </tbody>
</table>

<h2>The Big Picture &mdash; Where We Are</h2>

<p>The strategy has two tracks running simultaneously:</p>

<p><strong>Track 1 &mdash; Push down (suppression):</strong> Your personal website
(4 articles, ready to deploy), the COVID relief story in 28 publication inboxes,
and any content that gets published will collectively push the negative results down
on Google over the next 4&ndash;12 weeks.</p>

<p><strong>Track 2 &mdash; Remove (takedown):</strong> The three Google removal requests
being filed today, the Wikipedia correction, the Grokipedia correction, and the
Dale Bhagwagar outreach all target specific negative URLs for removal or correction.</p>

<p>Both tracks are in motion. The suppression track works automatically once the
website is live and the first article gets published. The removal track works
on a 4&ndash;12 week decision cycle per request.</p>

<h2>What We Need From You &mdash; Three Things</h2>

<div class="urgent">
<p style="margin:0 0 12px"><strong>1. Confirm the COVID story facts (most urgent)</strong><br>
28 publications now have the story in their inboxes. When they come back with questions &mdash;
and some will &mdash; we need to confirm the numbers with you before responding. Are these correct?
Over one million meals? Mumbai + Siolim + Porvorim? Funded personally? Women and children only?
Do you have any photos from the distribution?</p>

<p style="margin:0 0 12px"><strong>2. Register gautamvora.com</strong><br>
The website is complete with 4 articles including the full COVID essay. Every day it is not
live is a day Google is not indexing it. Registration takes 5 minutes at any registrar
(GoDaddy, Namecheap, Google Domains). Approx. Rs 1,000&ndash;1,500 per year.</p>

<p style="margin:0"><strong>3. Any court document you have</strong><br>
The Bombay HC bail order and/or the August 2010 police closure document &mdash; even a
scanned copy &mdash; makes our Google removal requests substantially stronger.
If you have access to Adv. Sujata Shirasi, she may be able to provide certified copies.</p>
</div>

<p>Reply to this email and we move on all three immediately.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com">info@pressdetective.com</a>
</p>

<div class="footer">
  Confidential &mdash; prepared for Gautam Vora only. This is a strategic communications plan,
  not legal advice. Formal de-indexing petitions via Indian courts require qualified legal counsel.
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
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(token, token)
        s.sendmail(FROM_ADDR, [TO_ADDR] + CC_ALWAYS, msg.as_bytes())
    print(f"Sent to {TO_ADDR}, CC: {', '.join(CC_ALWAYS)}")

if __name__ == "__main__":
    send()
