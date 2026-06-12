"""
Send Gautam 20-article approval email + press correction letters summary.
Requires his sign-off before any articles go to press.
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

SUBJECT = "Your 20 Articles — Please Review & Approve Before We Send to Press | Press Detective"

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
.article-list{margin:0 0 20px;padding:0;list-style:none}
.article-list li{padding:10px 14px;border-bottom:1px solid #e0e7ef;font-size:13px;display:flex;gap:10px;align-items:baseline}
.article-list li:nth-child(even){background:#f7f9fc}
.num{color:#1F4E79;font-weight:bold;min-width:24px;font-size:12px}
.title{font-weight:bold;color:#1a1a2e;flex:1}
.cat{color:#888;font-size:11px;white-space:nowrap}
.quote-box{background:#f0f4fa;border:1px solid #d0dff0;border-radius:6px;padding:14px 18px;margin:14px 0}
.quote-box p{margin:0 0 8px;font-size:13px}
.quote-box .q{font-style:italic;color:#1F4E79;font-size:14px;margin:8px 0 0;padding-left:12px;border-left:3px solid #1F4E79}
.corrections-list{margin:0 0 14px;padding-left:20px}
.corrections-list li{margin-bottom:8px;font-size:13px;color:#333}
.sig{font-weight:bold;color:#1F4E79;font-size:15px}
.footer{margin-top:44px;padding-top:14px;border-top:1px solid #ddd;font-size:12px;color:#999}
table{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0 20px}
th{background:#1F4E79;color:#fff;text-align:left;padding:9px 12px}
td{padding:9px 12px;border-bottom:1px solid #e0e7ef;vertical-align:top}
</style>
</head><body><div class="wrap">

<h1>Your 20 Articles &mdash; Approval Request</h1>
<div class="sub">Press Detective &nbsp;&bull;&nbsp; Confidential &nbsp;&bull;&nbsp; 12 June 2026</div>

<p>Dear Gautam,</p>

<p>We have written <strong>20 articles</strong> in your name, covering your investment philosophy,
market views, private wealth management approach, and the COVID relief story. All are
ready to send to press &mdash; but <strong>nothing goes out until you read and approve</strong>.</p>

<p>Please read through the list below, reply to this email with any corrections, and confirm
you are happy for us to proceed.</p>

<div class="green-box">
<strong>How to respond:</strong> Reply to this email.<br>
If you approve all articles as written: <em>"Approved &mdash; send all."</em><br>
If you want changes: list the article title and what to change.<br>
If you want to add your actual quotes: paste them in &mdash; we will insert them into the relevant article.
</div>

<h2>The 20 Articles</h2>

<p>These are written in your voice as a first-person expert. Each one is 550&ndash;700 words.
Every one includes a strong opinion, a quotable line, and a clear argument.</p>

<ul class="article-list">
  <li><span class="num">1</span><span class="title">The Women Got the Rice</span><span class="cat">Personal Essay &mdash; COVID relief, Mumbai &amp; Goa, 2020</span></li>
  <li><span class="num">2</span><span class="title">I Don&#8217;t Invest in Stocks. I Invest in Businesses.</span><span class="cat">Opinion &mdash; investment philosophy</span></li>
  <li><span class="num">3</span><span class="title">What the Private Wealth Management Industry in India Won&#8217;t Tell You</span><span class="cat">Wealth Management</span></li>
  <li><span class="num">4</span><span class="title">Patient Capital: The Unfair Advantage Most Indian Investors Refuse to Use</span><span class="cat">Investing &mdash; compounding, SIPs, behaviour</span></li>
  <li><span class="num">5</span><span class="title">How to Read a Promoter Before the Quarterly Numbers Tell You Anything</span><span class="cat">Stock Analysis &mdash; promoter pledging, RPTs</span></li>
  <li><span class="num">6</span><span class="title">SEBI at 35: How Indian Markets Finally Grew Up</span><span class="cat">Regulation &mdash; T+1, insider trading, reforms</span></li>
  <li><span class="num">7</span><span class="title">Why Indian Retail Investors Keep Losing Money &mdash; And What Actually Fixes It</span><span class="cat">Opinion &mdash; behavioural finance</span></li>
  <li><span class="num">8</span><span class="title">India&#8217;s Infrastructure Decade: What the Numbers Actually Say</span><span class="cat">Market Analysis &mdash; NIP, Rs 111 trillion, sectors</span></li>
  <li><span class="num">9</span><span class="title">Twenty-Five Years of Indian Market Cycles: What I Know Now That I Didn&#8217;t Then</span><span class="cat">Market History &mdash; personal memoir style</span></li>
  <li><span class="num">10</span><span class="title">The Diversification Myth: Why Most Indian Portfolios Are Diversified in Name Only</span><span class="cat">Portfolio Strategy &mdash; correlation, risk factors</span></li>
  <li><span class="num">11</span><span class="title">Mumbai: What India&#8217;s Financial Capital Looks Like from the Inside</span><span class="cat">Opinion &mdash; Dalal Street, Nariman Point, BKC</span></li>
  <li><span class="num">12</span><span class="title">What I Have Learned from 25 Years of Managing Private Client Wealth</span><span class="cat">Wealth Management &mdash; trust, life planning</span></li>
  <li><span class="num">13</span><span class="title">The Case for Unlisted Indian Companies: Where Real Wealth Is Being Created</span><span class="cat">Alternative Investing &mdash; pre-IPO, unlisted equity</span></li>
  <li><span class="num">14</span><span class="title">What Warren Buffett Got Right &mdash; And What Does Not Apply to India</span><span class="cat">Investment Philosophy &mdash; promoter character</span></li>
  <li><span class="num">15</span><span class="title">FIIs, SIPs and What Actually Moves Indian Markets Now</span><span class="cat">Market Analysis &mdash; domestic flows, structural shift</span></li>
  <li><span class="num">16</span><span class="title">The Small-Cap Illusion: Why Most Small-Cap Funds Consistently Fail Their Investors</span><span class="cat">Fund Analysis &mdash; AUM, illiquidity, herding</span></li>
  <li><span class="num">17</span><span class="title">How I Value Indian Financial Companies: A Framework After 25 Years</span><span class="cat">Stock Analysis &mdash; banks, NBFCs, NPA culture</span></li>
  <li><span class="num">18</span><span class="title">Understanding India&#8217;s Stock Exchange Structure: NSE, BSE and SEBI</span><span class="cat">Market Structure &mdash; explainer</span></li>
  <li><span class="num">19</span><span class="title">Why Promoter Holdings Are the Most Important Signal in Indian Equities</span><span class="cat">Equity Research &mdash; pledge data, stake changes</span></li>
  <li><span class="num">20</span><span class="title">The Indian Mid-Cap Opportunity: A Fundamental Framework</span><span class="cat">Investment Framework &mdash; ROCE, moat, valuation</span></li>
</ul>

<h2>Your Expert Quotes &mdash; We Need These From You</h2>

<p>These articles become much more powerful for press if they include a few genuine quotes
in your voice on current market conditions. Once you approve the articles, editors will
ask for a brief statement for context. If you can send us 3&ndash;5 short quotes, we will
add them to the most relevant articles.</p>

<div class="quote-box">
<p><strong>Suggested topics for your quotes (just 1&ndash;3 sentences each):</strong></p>
<ul style="padding-left:20px;font-size:13px;margin:8px 0">
  <li>Current market view &mdash; where do you see the Sensex / Nifty heading in the next 6&ndash;12 months?</li>
  <li>The SIP / domestic money story &mdash; what has changed most about Indian markets in the last 5 years?</li>
  <li>Your take on mid-caps right now &mdash; opportunity or froth?</li>
  <li>What advice would you give a first-time investor in India today?</li>
  <li>What sector or theme are you most excited about in India for the next decade?</li>
</ul>
<p class="q">Example format: <em>"India&#8217;s domestic SIP machine has fundamentally changed how corrections play out. FII selling that would have driven a 20% bear market ten years ago now creates a 10% correction that domestic money absorbs in weeks. We are in a structurally different market."</em></p>
</div>

<h2>Press Correction Letters &mdash; Also Ready to Send</h2>

<p>We have drafted formal factual correction letters to <strong>four publications</strong>
that published inaccurate or misleading coverage about you. These are ready to send, but
we need two things from you first:</p>

<div class="urgent">
<p style="margin:0 0 12px"><strong>1. Your brother&#8217;s full name</strong><br>
His name appears in some of these articles alongside yours. He has no involvement in
either matter and his name should not appear. We have included a <em>[BROTHER&#8217;S FULL NAME]</em>
placeholder in the letters &mdash; please supply his full name so we can file them correctly.</p>

<p style="margin:0"><strong>2. Court documents</strong><br>
The Bombay HC bail order (Tikku matter, 2012) and/or the August 2010 Mumbai Police
closure document strengthen all four letters considerably. Even a scanned copy is fine.
Adv. Sujata Shirasi can obtain certified copies if needed.</p>
</div>

<table>
  <tr><th>Publication</th><th>What we are requesting</th></tr>
  <tr><td>DNA India</td><td>Correct headline &mdash; you were not a murder accused. Remove brother&#8217;s name.</td></tr>
  <tr><td>Business Standard</td><td>Add missing fact: Bombay HC granted bail. Remove brother&#8217;s name.</td></tr>
  <tr><td>Mid-Day</td><td>Note August 2010 clean chit. Offer of interview for balance. Remove brother&#8217;s name.</td></tr>
  <tr><td>Times of India</td><td>HC bail grant not reported alongside sessions court refusal. Remove brother&#8217;s name.</td></tr>
</table>

<h2>Summary &mdash; What We Need From You</h2>

<ol class="corrections-list">
  <li><strong>Reply approving the 20 articles</strong> (or with specific corrections)</li>
  <li><strong>Send 3&ndash;5 market quotes</strong> in your own words for insertion into key articles</li>
  <li><strong>Confirm your brother&#8217;s full name</strong> so we can file the correction letters</li>
  <li><strong>Send any court documents</strong> (HC bail order, August 2010 police closure)</li>
  <li><strong>Register gautamvora.com</strong> &mdash; the website with all 20 articles is built and waiting</li>
</ol>

<p>Once you approve, we send the articles to all 28 publications the same day.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com">info@pressdetective.com</a>
</p>

<div class="footer">
  Confidential &mdash; for Gautam Vora only. These are draft articles for your approval;
  nothing is published or distributed until you confirm in writing. This is a strategic
  communications plan, not legal advice.
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
