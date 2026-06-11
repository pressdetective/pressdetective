"""
Full execution report to Gautam Vora — gavora@gmail.com
Covers: COVID story, website, press pitch, Google removals, Wikipedia, timeline.
FROM: info@pressdetective.com | CC: info@pressdetective.com
Uses Postmark SMTP (token from .creds/proton_accounts.json).
"""
import smtplib, ssl, os, json, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# Credentials
CREDS = Path(__file__).parents[2] / ".creds" / "proton_accounts.json"
def _postmark_token():
    if CREDS.exists():
        return json.loads(CREDS.read_text(encoding="utf-8")).get("smtp_postmark", {}).get("token", "")
    return os.environ.get("POSTMARK_TOKEN", "")

FROM_ADDR = "info@pressdetective.com"
FROM_NAME = "Press Detective"
TO_ADDR   = "gavora@gmail.com"
CC_ALWAYS = ["info@pressdetective.com"]

SUBJECT = "Your Reputation Clearance — Full Report & What We Have Built | Press Detective"

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#222;margin:0;padding:0}
.wrap{max-width:720px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:22px;margin-bottom:4px;line-height:1.3}
.sub{color:#666;font-size:13px;margin-bottom:32px;padding-bottom:16px;border-bottom:2px solid #1F4E79}
h2{color:#1F4E79;font-size:16px;margin:32px 0 10px;padding-bottom:7px;border-bottom:2px solid #1F4E79}
p{line-height:1.75;margin:0 0 14px;color:#333}
ul,ol{padding-left:22px}
li{margin-bottom:9px;line-height:1.65;color:#333}
table{border-collapse:collapse;width:100%;margin:12px 0 20px;font-size:13px}
th{background:#1F4E79;color:#fff;text-align:left;padding:9px 12px}
td{padding:9px 12px;border-bottom:1px solid #e0e7ef;vertical-align:top}
tr:nth-child(even) td{background:#f5f8fb}
.done{color:#2e7d32;font-weight:bold}
.ready{color:#1565c0;font-weight:bold}
.pending{color:#b45309;font-weight:bold}
.feature{background:#f0f4fa;border-left:5px solid #1F4E79;padding:18px 22px;margin:16px 0;border-radius:0 6px 6px 0}
.feature h3{color:#1F4E79;font-size:15px;margin:0 0 8px}
.feature p{margin:0;font-size:14px;color:#444}
.urgent{background:#fff8e6;border-left:5px solid #e6a817;padding:16px 20px;margin:16px 0;border-radius:0 6px 6px 0}
.urgent strong{color:#b45309}
.green-box{background:#eef7ee;border-left:5px solid #2e7d32;padding:16px 20px;margin:16px 0;border-radius:0 6px 6px 0}
.sig{font-weight:bold;color:#1F4E79;font-size:15px}
.footer{margin-top:48px;padding-top:14px;border-top:1px solid #ddd;font-size:12px;color:#999}
a{color:#1F4E79}
</style>
</head><body><div class="wrap">

<h1>Your Reputation Clearance &mdash; Full Report</h1>
<div class="sub">Press Detective &nbsp;&bull;&nbsp; Confidential &nbsp;&bull;&nbsp; 11 June 2026</div>

<p>Dear Gautam,</p>

<p>We have now completed the first full phase of your reputation clearance. This report covers
everything we have built, everything that is ready to deploy, and exactly what we need from you
to move to the next stage. We wanted you to have the complete picture in one place.</p>

<p>The short version: your counter-narrative is built, your website is ready, three
Google removal requests are drafted, and we have written the story of your COVID relief work
as a press-ready long-form piece. The most important work now is getting the website live
and the press pitch out.</p>

<h2>1. The COVID Relief Story &mdash; Your Most Powerful Asset</h2>

<div class="feature">
<h3>&#8220;The Women Got the Rice&#8221;</h3>
<p>We have written a 1,400-word long-form personal essay about your 2020 lockdown relief
operation &mdash; the million meals across Mumbai, Siolim and Porvorim; the decision to distribute
exclusively to women and children; the team of friends who showed up. The piece is ready to go on
your website and to pitch to press.</p>
</div>

<p>This story is the centrepiece of your entire reputation strategy. Here is why it matters so much:</p>
<ul>
  <li>A published piece on Scroll.in, The Print, or Hindustan Times will rank on page 1 for
      &#8220;Gautam Vora&#8221; within weeks of publication.</li>
  <li>It completely reframes the narrative &mdash; from old court coverage to a documented story of
      personal action at scale during a national crisis.</li>
  <li>The detail that anchors it &mdash; giving only to women and children, and why &mdash; is the
      kind of specific, counter-intuitive decision that journalists and readers remember.</li>
  <li>We have drafted a press pitch and will send it to <strong>Mid-Day, Scroll.in, The Print,
      and DNA India</strong> the moment you confirm the facts below.</li>
</ul>

<div class="urgent">
<strong>To confirm before we send the press pitch:</strong>
<ol style="margin-top:10px">
  <li>Are the facts in the story accurate? (Over one million meals; Mumbai + Siolim + Porvorim;
      funded personally; team of friends; panchayat coordination; women and children only)</li>
  <li>Do you have any photographs from the distribution? Even phone photos from 2020 significantly
      strengthen a press pitch.</li>
  <li>Are you willing to be interviewed by journalists? A short email interview or a call is
      usually all they need.</li>
  <li>Are there any panchayat members or friends involved who would be willing to be quoted?</li>
</ol>
</div>

<p>If the facts are correct and you are comfortable, we send the pitch within 24 hours of
your reply.</p>

<h2>2. Your Personal Website &mdash; Built and Ready to Deploy</h2>

<p>We have built a complete personal website for you. It is ready to go live the moment
you register <strong>gautamvora.com</strong>. The site includes:</p>

<table>
  <thead><tr><th>Page</th><th>Content</th></tr></thead>
  <tbody>
    <tr><td><strong>Homepage</strong></td>
        <td>SEO title: &#8220;Gautam Vora &mdash; Equity Analyst &amp; Stockbroker, Mumbai&#8221;;
            Schema.org Person markup; featured COVID essay card; 3 market commentary article links</td></tr>
    <tr><td><strong>&#8220;The Women Got the Rice&#8221;</strong></td>
        <td>1,400w personal essay on the COVID relief operation; full schema.org Article markup;
            typography-first design built for reading and sharing</td></tr>
    <tr><td><strong>India Stock Market Structure</strong></td>
        <td>600w piece on NSE/BSE/SEBI regulation — establishes equity expertise</td></tr>
    <tr><td><strong>Promoter Holdings in Indian Equities</strong></td>
        <td>600w analytical piece on shareholding patterns — demonstrates research depth</td></tr>
    <tr><td><strong>The Indian Mid-Cap Framework</strong></td>
        <td>650w investment framework piece — ROCE, cash conversion, moat, valuation</td></tr>
  </tbody>
</table>

<p>Once live, Google typically indexes a new personal site within <strong>2&ndash;4 weeks</strong>.
A site with your name as the domain, your name as the title, and four substantial articles about
your professional work will rank on page 1 for &#8220;Gautam Vora&#8221; within 4&ndash;8 weeks.</p>

<div class="green-box">
<strong>Action required from you:</strong> Register <strong>gautamvora.com</strong> through
any domain registrar (GoDaddy, Namecheap, Google Domains). Once you have it, we handle the
deployment and DNS setup.
</div>

<h2>3. Google Removal Requests &mdash; Ready to File</h2>

<p>We have prepared three formal removal requests, ready to paste into Google&#8217;s
&#8220;Results About You&#8221; tool. Each is built around the strongest available legal argument:</p>

<table>
  <thead><tr><th>Publication</th><th>Article</th><th>Ground for removal</th></tr></thead>
  <tbody>
    <tr><td><strong>Yahoo News</strong></td>
        <td>Headline linking your name to the murder case</td>
        <td>Factually misleading &mdash; fuses two unrelated matters; police clean chit 2010;
            no conviction in 14+ years; K.S. Puttaswamy privacy right</td></tr>
    <tr><td><strong>Business Standard</strong></td>
        <td>&#8220;Court rejects bail of Gautam Vora&#8221;</td>
        <td>Incomplete record &mdash; reports only sessions court rejection, not Bombay HC bail grant;
            creates false impression of ongoing detention</td></tr>
    <tr><td><strong>DNA India</strong></td>
        <td>Headline linking your name to murder case</td>
        <td>Factually inaccurate &mdash; you were not charged with murder; HC granted bail;
            no conviction; disproportionate reputational harm</td></tr>
  </tbody>
</table>

<p>These are <strong>significantly stronger</strong> with a copy of the Bombay HC bail order and/or
the August 2010 police closure document. If you can locate either of these &mdash; even a scanned
copy &mdash; please send it to us.</p>

<p>We can file these on your behalf via Google&#8217;s online form, or provide you the exact
text to paste. Filing takes approximately 15 minutes per request.</p>

<h2>4. Wikipedia &amp; Grokipedia Corrections &mdash; Ready to Post</h2>

<p>The Wikipedia article on Viveka Babajee names you but omits the August 2010 police clean chit.
We have written the full Talk page correction, with COI disclosure, ready to post. The text requests
a single additional sentence:</p>

<blockquote style="margin:12px 0 16px 24px;padding:10px 16px;border-left:3px solid #1F4E79;
  font-style:italic;color:#444;font-size:14px">
&#8220;Mumbai Police issued a clean chit to Vora in August 2010, concluding their investigation
with no charges filed against him.&#8221;
</blockquote>

<p>This is a factual addition, not a deletion. It has a strong basis under Wikipedia&#8217;s
Biographies of Living Persons policy. We will post this as soon as you confirm the wording
is accurate and give us the go-ahead.</p>

<p>The same correction text is ready for Grokipedia and other Wikipedia mirrors.</p>

<h2>5. Dale Bhagwagar Media Group &mdash; Outreach Drafted</h2>

<p>We have drafted a professional outreach email to Dale Bhagwagar&#8217;s media group requesting
that any coverage of the Viveka Babajee matter within their network be updated with the August 2010
clean chit. This is a courtesy request, not a legal demand. Ready to send once you confirm
you are comfortable with this approach.</p>

<h2>6. The Press Pitch &mdash; Ready to Send</h2>

<p>We have written a press pitch for the COVID relief story and will send it to the following
desks immediately upon your confirmation:</p>

<table>
  <thead><tr><th>Publication</th><th>Why we are targeting it</th></tr></thead>
  <tbody>
    <tr><td><strong>Mid-Day</strong></td><td>Mumbai-focused; strong human interest coverage;
        widely read in the city</td></tr>
    <tr><td><strong>Scroll.in</strong></td><td>National; long-form; high Google authority;
        indexed stories rank quickly</td></tr>
    <tr><td><strong>The Print</strong></td><td>National; credible; entrepreneur and social impact
        stories perform well</td></tr>
    <tr><td><strong>DNA India</strong></td><td><strong>Strategic priority</strong> &mdash; DNA India
        currently carries a negative article about you. A positive published story on the same domain
        is one of the highest-value ORM placements we can make.</td></tr>
  </tbody>
</table>

<h2>Summary: What happens next</h2>

<table>
  <thead><tr><th>Action</th><th>Who</th><th>When</th></tr></thead>
  <tbody>
    <tr><td>Confirm COVID story facts + photos availability</td>
        <td><span class="pending">You</span></td><td>As soon as possible</td></tr>
    <tr><td>Press pitch sent to 4 desks</td>
        <td><span class="ready">Press Detective</span></td><td>Within 24h of your confirmation</td></tr>
    <tr><td>Register gautamvora.com domain</td>
        <td><span class="pending">You</span></td><td>This week</td></tr>
    <tr><td>Website deployed and live</td>
        <td><span class="ready">Press Detective</span></td><td>Within 24h of domain confirmed</td></tr>
    <tr><td>Google removal requests filed (3)</td>
        <td><span class="ready">Press Detective</span></td><td>This week &mdash; stronger with court docs</td></tr>
    <tr><td>Wikipedia Talk page correction posted</td>
        <td><span class="ready">Press Detective</span></td><td>This week &mdash; awaiting your go-ahead</td></tr>
    <tr><td>Dale Bhagwagar outreach sent</td>
        <td><span class="ready">Press Detective</span></td><td>This week &mdash; awaiting your go-ahead</td></tr>
    <tr><td>LinkedIn profile built</td>
        <td><span class="pending">Needs career details from you</span></td><td>Week 1&ndash;2</td></tr>
    <tr><td>Page-1 shift visible</td>
        <td><span class="done">Automatic</span></td><td>Month 1&ndash;3</td></tr>
  </tbody>
</table>

<div class="urgent">
<strong>The three things we need from you to accelerate everything:</strong>
<ol style="margin-top:10px">
  <li><strong>COVID story confirmation</strong> &mdash; are the facts correct? Any photos?
      Are you willing to speak to journalists?</li>
  <li><strong>Tikku / Palande final outcome</strong> &mdash; discharge, acquittal, or still pending?
      Any court document you have access to (HC bail order, discharge certificate) would materially
      strengthen the Google removal requests.</li>
  <li><strong>Register gautamvora.com</strong> &mdash; this is the single highest-impact action
      you can take this week. The entire website is built and waiting.</li>
</ol>
</div>

<p>Reply to this email with any of the above and we move immediately.
Everything else we are handling on our side without waiting for your input.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com">info@pressdetective.com</a>
</p>

<div class="footer">
  Confidential &mdash; prepared for Gautam Vora only. This is a strategic communications plan,
  not legal advice. Actions relating to court records or de-indexing petitions may require
  qualified legal counsel.
</div>
</div></body></html>
"""

def send():
    token = _postmark_token()
    if not token:
        print("ERROR: Postmark token not found in .creds/proton_accounts.json")
        sys.exit(1)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = TO_ADDR
    msg["Cc"]      = ", ".join(CC_ALWAYS)
    msg.attach(MIMEText(HTML, "html", "utf-8"))
    recipients = [TO_ADDR] + CC_ALWAYS
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.login(token, token)
        s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
    print(f"Sent to {TO_ADDR}, CC: {', '.join(CC_ALWAYS)}")

if __name__ == "__main__":
    send()
