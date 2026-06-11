"""
Press pitch to Times of India and Hindustan Times — COVID relief story.
Includes the full article inline so editors can read it immediately.
FROM: info@pressdetective.com | CC: info@pressdetective.com
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
    return json.loads(p.read_text(encoding="utf-8-sig")).get("smtp_postmark", {}).get("token", "")

SUBJECT = "Pitch: One Mumbai entrepreneur, one million meals, and the decision that made it work | Ready to publish"

JOURNALISTS = [
    ("Mumbai Desk", "mumbai.mirror@timesgroup.com"),
    ("Features Desk", "features@timesgroup.com"),
    ("Mumbai City Desk", "htmumbai@hindustantimes.com"),
    ("HT Features", "htfeatures@hindustantimes.com"),
]

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#222;margin:0;padding:0}
.wrap{max-width:700px;margin:24px auto;padding:0 24px}
.pitch{background:#f0f4fa;border-left:5px solid #1F4E79;padding:18px 22px;margin-bottom:28px;border-radius:0 6px 6px 0}
.pitch h2{color:#1F4E79;font-size:16px;margin:0 0 10px}
.pitch p{margin:0 0 10px;line-height:1.7;color:#333;font-size:14px}
.pitch ul{padding-left:20px;margin:8px 0}
.pitch li{margin-bottom:6px;color:#333;font-size:14px}
.divider{border:none;border-top:2px solid #1F4E79;margin:28px 0 24px}
.article-label{font-family:Arial,sans-serif;font-size:11px;text-transform:uppercase;
  letter-spacing:1.5px;color:#888;margin-bottom:12px}
.article{font-family:Georgia,'Times New Roman',serif}
.article h1{font-size:28px;color:#111;line-height:1.25;margin:0 0 10px;font-weight:700}
.article .deck{font-size:17px;color:#444;font-style:italic;line-height:1.5;margin-bottom:18px}
.article .byline{font-family:Arial,sans-serif;font-size:12px;color:#888;border-top:1px solid #ddd;
  border-bottom:1px solid #ddd;padding:8px 0;margin-bottom:24px}
.article p{font-size:16px;line-height:1.85;margin-bottom:20px;color:#1a1a1a}
.article p.drop::first-letter{float:left;font-size:60px;line-height:.85;padding-right:7px;
  padding-top:4px;color:#1F4E79;font-weight:700}
.article h2{font-family:Arial,sans-serif;font-size:11px;text-transform:uppercase;
  letter-spacing:2px;color:#1F4E79;margin:32px 0 14px;padding-bottom:6px;border-bottom:1px solid #dde6f0}
.article .pullquote{margin:28px 0;padding:0 0 0 20px;border-left:4px solid #1F4E79;
  font-size:20px;color:#1F4E79;font-style:italic;line-height:1.45}
.sig{font-family:Arial,sans-serif;margin-top:32px;font-size:13px;color:#555}
.sig strong{color:#1F4E79}
</style>
</head><body><div class="wrap">

<!-- PITCH NOTE -->
<div class="pitch">
  <h2>Story pitch &mdash; ready to publish</h2>
  <p>Dear Editor,</p>
  <p>We are pitching a story that has not been told publicly: during India&#8217;s first COVID
  lockdown in 2020, Mumbai entrepreneur <strong>Gautam Vora</strong> personally organised and
  distributed over <strong>one million meals</strong> across Mumbai, Siolim and Porvorim &mdash;
  funded entirely from his own pocket, executed with a team of friends, and coordinated with
  local panchayat members.</p>
  <p>The defining detail: he distributed rations <strong>exclusively to women, elderly women,
  and children</strong>. Not sentiment &mdash; strategy. He had seen how aid given to men in
  crisis zones gets redirected. By placing food in mothers&#8217; hands, it reached the children.</p>
  <ul>
    <li>Over <strong>one million meals</strong> across Mumbai and Goa</li>
    <li>Funded <strong>entirely from his own pocket</strong> &mdash; no NGO, no corporate backing</li>
    <li>Executed by <strong>a team of personal friends</strong> during full lockdown</li>
    <li>Ground coordination via <strong>local panchayat members</strong> in Mumbai, Siolim, Porvorim</li>
    <li>Deliberate targeting: <strong>women, elderly women, and children only</strong></li>
  </ul>
  <p>The full article is below &mdash; ready to publish as written, or we can arrange an
  interview with Gautam Vora at your convenience.</p>
  <p style="margin:0"><strong>Press Detective</strong> &mdash; on behalf of Gautam Vora &mdash;
  <a href="mailto:info@pressdetective.com" style="color:#1F4E79">info@pressdetective.com</a></p>
</div>

<hr class="divider">
<div class="article-label">Full article &mdash; ready to publish</div>

<!-- FULL ARTICLE -->
<div class="article">

<h1>The Women Got the Rice</h1>
<div class="deck">During India&#8217;s first lockdown, one Mumbai entrepreneur personally organised
over one million meals across Mumbai and Goa. The money was his own. The team was his friends.
And the most important decision he made had nothing to do with how much to spend.</div>
<div class="byline">By <strong>Gautam Vora</strong> &nbsp;&bull;&nbsp; Mumbai &nbsp;&bull;&nbsp;
2020 (personal account)</div>

<p class="drop">In the early weeks of India&#8217;s first lockdown, I made a decision that most
people running relief operations never make. I was watching &mdash; somewhere between a warehouse
loading bay and a narrow lane in a Mumbai neighbourhood &mdash; and I saw what happens when you
put food in the hands of adult men in a crisis.</p>

<p>It disappears. Not always. Not every man. But often enough, in the particular logic of crisis
zones, that the maths stops working. The food goes to market. It gets resold for cash that is
needed for something else. Or it moves sideways, through some informal economy of obligation that
has nothing to do with hunger, to someone who needed it less.</p>

<p>I made a rule. Dry ration kits &mdash; rice, dal, oil, the essentials for two weeks &mdash;
would be handed only to women, elderly women, and children. Not as a moral statement.
As a system design decision. The food needed to reach the kitchen. In the households I was
looking at, across the slum clusters of Mumbai and the village lanes of Siolim and Porvorim,
the women are the kitchen. If the kit is in her hands, it stays in the home.
If it is in his, that is less certain.</p>

<div class="pullquote">This is not a statement about gender. It is an observation about where
food goes, and why, in the precise conditions of a pandemic shutdown.</div>

<p>The decision sounds simple. It was not simple. It meant knocking on different doors,
having different conversations, navigating the particular awkwardness of handing aid to a mother
while her husband stood three feet away. It meant explaining ourselves. It meant the occasional
refusal &mdash; pride is real, and dignity does not suspend itself during a crisis.
But it worked. The food stayed in the homes. The children ate.</p>

<h2>How it began</h2>

<p>I am an entrepreneur. I think in logistics and systems. When the lockdown came down in late
March 2020, I watched the government machinery move at the speed government machinery moves,
and I watched the gap between need and response widen in real time. The city had stopped.
The daily-wage earners, the domestic workers, the street vendors, the fishing families &mdash;
they had no buffer. A week without income in those households is an emergency. Two weeks is a
crisis. Three weeks is the kind of hunger that doesn&#8217;t announce itself loudly but sits
in the bodies of children.</p>

<p>I decided the gap was my problem to solve. Not because anyone asked me to. Because it was in
front of me, and I had the resources to do something about it, and waiting for a better-organised
institution to arrive was a choice I was not willing to make.</p>

<p>I called my friends.</p>

<h2>The team</h2>

<p>That is the detail I keep coming back to, because it says something I cannot quite articulate
any other way. Not volunteers who answered a public call. Not paid staff. My friends. People who
looked at their phones in April 2020 &mdash; when the city had stopped, when everyone was supposed
to stay inside, when going outside felt like breaking a law that was also, genuinely, for your own
protection &mdash; and said yes.</p>

<p>They spent weeks doing physical, exhausting work. Loading vans. Counting kits. Navigating
checkpoints. Knocking on doors. In the heat. In masks that were uncomfortable before discomfort
became ordinary. At personal risk, in the way that everything was personal risk that spring.</p>

<p>You cannot manufacture that kind of response. It is built over years of being the kind of
person whose friends show up. I am grateful for it in a way I find difficult to express.</p>

<h2>The logistics</h2>

<p>Sourcing dry rations in a locked-down city meant working with a supply chain that had
half-collapsed. Wholesale markets with reduced hours and spooked suppliers. Transport permissions
that were being invented in real time by administrators who were also, like everyone else,
making it up as they went. Moving goods from Mumbai to Siolim, to Porvorim, across a state
border that was officially closed, required a level of improvisation that no relief operations
manual had ever anticipated, because the conditions had never existed before.</p>

<p>The ground coordinators made it possible. Local panchayat members. Government contacts who had
been contacts for years and who knew, precisely, which door to knock on. Which cluster of buildings
was being passed over because it didn&#8217;t appear on any official list. Which old woman
hadn&#8217;t left her house in three weeks and would not have been found by anyone operating
from a spreadsheet.</p>

<div class="pullquote">Local knowledge cannot be bought with a wire transfer.
It has to be earned, over time, through the slow accumulation of trust.</div>

<h2>Siolim. Porvorim. Mumbai.</h2>

<p>Siolim is a village on the north Goa coast. Porvorim is a township outside Panaji &mdash;
neither fully urban nor village, with apartment buildings next to old Goan houses next to
communities of migrant workers who had been stranded when the lockdown came down, far from
their home states, belonging temporarily to nowhere.</p>

<p>In each of these places, the panchayat members knew which door to knock on. My team carried
the kits. The women took them. In Siolim, there was an old woman who stood in her doorway
holding a bag she had not expected, looking at us with an expression I will not try to describe
because to describe it would be to reduce it. I will say only that she was not surprised we
had come. She was surprised it had taken this long.</p>

<h2>The number</h2>

<p>At some point the count crossed a million meals. I am not sure exactly when. That is the
thing about this kind of work when you are inside it: the number is not the point. The point
is the next van, the next list, the next door. The number is something you find when you step
back and add it up, weeks later, and try to understand what the last two months were.</p>

<p>Over one million meals. Funded entirely from my own pocket. Distributed entirely through
personal relationships. Targeted, deliberately and on the basis of a clear operational
judgement, at the people most likely to ensure the food reached the children.</p>

<h2>What I learned</h2>

<p>The most important thing I know about relief work now is that the last mile is not a logistics
problem. It is a relationships problem. You cannot solve it with money alone, or with a
well-designed NGO structure, or with the best intentions in the world. You solve it with people
who already know the ground &mdash; who have been walking those lanes for years and who will
pick up the phone when you call.</p>

<p>The second thing I know is that who you give to matters more than how much you give.
Aid that reaches the wrong hands is not aid. It is a cost. The decision to target women and
children was not charitable instinct. It was the result of watching what happens when you get
it wrong, and choosing to get it right instead.</p>

<p>One million meals is a number. The number is made of individual moments: a mother opening
her door, a child who ate that night, an old woman in Siolim who had not been forgotten.
Each of those moments was the product of a network of relationships built over years, and a
team of friends who showed up, and a decision made early about who would hold the rice.</p>

<p>The decision was the whole thing.</p>

</div>

<div class="sig">
  &mdash;<br>
  <strong>Press Detective</strong><br>
  On behalf of Gautam Vora, Mumbai<br>
  <a href="mailto:info@pressdetective.com" style="color:#1F4E79">info@pressdetective.com</a><br>
  <span style="color:#999;font-size:12px">Gautam Vora is available for interview.
  All facts are accurate and verifiable.</span>
</div>

</div></body></html>
"""

def send():
    token = _pm_token()
    ctx = ssl.create_default_context()
    for name, addr in JOURNALISTS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT
        msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
        msg["To"]      = addr
        msg["Cc"]      = ", ".join(CC_ALWAYS)
        msg.attach(MIMEText(HTML, "html", "utf-8"))
        with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
            s.ehlo(); s.starttls(context=ctx); s.login(token, token)
            s.sendmail(FROM_ADDR, [addr] + CC_ALWAYS, msg.as_bytes())
        print(f"Sent to {name} <{addr}>")

if __name__ == "__main__":
    print(f"Sending to {len(JOURNALISTS)} TOI / HT desks...")
    send()
    print("Done.")
