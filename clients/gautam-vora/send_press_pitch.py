"""
Press pitch for Gautam Vora's COVID relief story.
Targets Mumbai / national media with the 'one million meals' story.

TO: list of journalist/desk emails below — add confirmed contacts before sending.
FROM: info@pressdetective.com (Press Detective, on behalf of Gautam Vora)
STRATEGY: The COVID story is strong enough to stand alone. It will also
           generate positive indexed content that pushes negative results down.

DNS note: Add gautamvora.com URL in the pitch once the site is live.
"""
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cfg

SUBJECT = "Pitch: One Mumbai entrepreneur, one million meals, and the decision that made it work | Lockdown 2020"

# Add confirmed journalist / desk emails here before running.
# Format: ("Name / Desk", "email@publication.com")
JOURNALISTS = [
    ("City Desk", "citydesk@mid-day.com"),
    ("News Desk", "newsdesk@scroll.in"),
    ("Editorial Desk", "edit@theprint.in"),
    # DNA India — strategic: they have an old negative article about Gautam
    ("News Tips", "newsdesk@dnaindia.com"),
    # Add specific journalist contacts here as you source them:
    # ("Reporter Name", "reporter@hindustantimes.com"),
    # ("Reporter Name", "reporter@timesofindia.com"),
]

PITCH_HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#333;margin:0;padding:0}
.wrap{max-width:680px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:18px;line-height:1.3;margin-bottom:4px}
.sub{color:#595959;font-size:13px;margin-bottom:24px}
p{line-height:1.75;margin:0 0 14px}
.pullquote{font-size:18px;color:#1F4E79;font-style:italic;border-left:3px solid #1F4E79;
  padding:10px 16px;margin:20px 0;line-height:1.5}
.facts{background:#f5f8fb;border:1px solid #dde6f0;border-radius:6px;padding:18px 20px;margin:20px 0}
.facts h3{color:#1F4E79;font-size:13px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px}
.facts ul{padding-left:20px;margin:0}
.facts li{margin-bottom:6px;font-size:14px}
.footer{margin-top:40px;padding-top:14px;border-top:1px solid #ddd;font-size:12px;color:#888}
.sig{font-weight:bold;color:#1F4E79}
a{color:#1F4E79}
</style></head><body><div class="wrap">

<h1>One Mumbai entrepreneur. One million meals. The decision that made it work.</h1>
<div class="sub">Story pitch from Press Detective &nbsp;|&nbsp; On behalf of Gautam Vora &nbsp;|&nbsp; June 2026</div>

<p>Dear Editor,</p>

<p>I am writing to pitch a story that has not been told publicly: during India&#8217;s first COVID lockdown
in 2020, a Mumbai-based entrepreneur named Gautam Vora personally organised and distributed over
<strong>one million meals</strong> across Mumbai, Siolim (Goa), and Porvorim (North Goa) &#8212;
funded entirely from his own pocket, executed with a team of close friends, and coordinated on the
ground with local panchayat members.</p>

<div class="pullquote">
  &#8220;The most important decision he made was not how much to spend. It was who to hand it to.&#8221;
</div>

<p>The defining detail of this operation is a decision Gautam made early on: he distributed rations
<strong>exclusively to women, elderly women, and children &#8212; not to adult men.</strong>
The reason was not sentiment. He had seen how aid given to men in crisis zones often gets resold
or redirected. By placing food in the hands of mothers, he ensured it reached the children.
A relief operation built on understanding human behaviour, not on good intentions alone.</p>

<div class="facts">
  <h3>The facts</h3>
  <ul>
    <li><strong>Over one million meals</strong> distributed across Mumbai and Goa</li>
    <li>Funded <strong>entirely from Gautam&#8217;s own pocket</strong> &#8212; no NGO, no corporate backing</li>
    <li>Executed by <strong>a team of friends</strong> who showed up during a locked-down city</li>
    <li>Ground coordination via <strong>local panchayat members</strong> in Mumbai, Siolim, and Porvorim</li>
    <li>Distributed as <strong>dry ration kits</strong> (rice, dal, oil &#8212; two weeks of provisions)</li>
    <li>Deliberate targeting: <strong>women, elderly women, and children only</strong></li>
    <li>Spanned <strong>urban Mumbai slums</strong> and <strong>Goan village communities</strong></li>
    <li>Completed during lockdown &#8212; crossing state lines under movement restrictions</li>
  </ul>
</div>

<p>This is not a story about a generous man. Generosity is common enough, and it is rarely
this effective. This is a story about a man who was quietly furious at the gap between a city&#8217;s
need and its response, who decided the gap was his problem to solve, and who built a system that
worked &#8212; at scale, across two states, during a pandemic, in six weeks.</p>

<p>The story works as:</p>
<ul style="padding-left:20px;margin-bottom:14px">
  <li>A <strong>long-form feature</strong> on lockdown relief and who actually fed India&#8217;s cities</li>
  <li>A <strong>COVID retrospective</strong> (six years on &#8212; what ordinary people did that governments didn&#8217;t)</li>
  <li>A <strong>social entrepreneurship piece</strong> on the operational insight that made it work: give to women</li>
  <li>A <strong>Goa-angle</strong> story &#8212; Mumbai funding, Siolim/Porvorim ground operation, panchayat coordination</li>
</ul>

<p>Gautam Vora is available for interview. He is based in Mumbai. He is willing to speak about the
operational decisions, the logistics, the team, and the communities reached.</p>

<p>I am happy to provide further details, additional context, or to arrange a call at your convenience.</p>

<p>
  <span class="sig">Press Detective</span><br>
  On behalf of Gautam Vora<br>
  <a href="mailto:info@pressdetective.com">info@pressdetective.com</a>
</p>

<div class="footer">
  Press Detective provides media relations and reputation management services.
  All facts stated in this pitch are accurate and verifiable.
  Distribution via panchayat records, ground photographs, and Gautam Vora&#8217;s personal testimony.
</div>
</div></body></html>
"""

PITCH_TEXT = """
Story pitch: One Mumbai entrepreneur, one million meals, and the decision that made it work.

During India's first COVID lockdown, Mumbai entrepreneur Gautam Vora personally organised and distributed over one million meals across Mumbai, Siolim, and Porvorim — funded entirely from his own pocket, executed with friends, coordinated via local panchayat members.

The defining detail: he distributed rations exclusively to women, elderly women, and children — not adult men. The reason was operational: aid given to men in crisis zones often gets redirected. By placing food in mothers' hands, it reached the children.

Over one million meals. No NGO. No corporate backing. His own money. His friends. Six weeks. Two states. During a lockdown.

Gautam Vora is available for interview. Contact: info@pressdetective.com
"""

def send_all():
    for name, email in JOURNALISTS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT
        msg["From"]    = f"{cfg.FROM_NAME} <{cfg.FROM_ADDR}>"
        msg["To"]      = email
        if cfg.CC_ALWAYS:
            msg["Cc"] = ", ".join(cfg.CC_ALWAYS)
        msg.attach(MIMEText(PITCH_TEXT, "plain", "utf-8"))
        msg.attach(MIMEText(PITCH_HTML, "html",  "utf-8"))
        recipients = [email] + (cfg.CC_ALWAYS or [])
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(cfg.SMTP_HOST, cfg.SMTP_PORT, context=ctx) as s:
            s.login(cfg.USERNAME, cfg.PASSWORD)
            s.sendmail(cfg.FROM_ADDR, recipients, msg.as_bytes())
        print(f"Sent to {name} <{email}>")

if __name__ == "__main__":
    print(f"Sending pitch to {len(JOURNALISTS)} journalists / desks...")
    send_all()
    print("Done.")
