import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "smtp.zeptomail.in"
SMTP_PORT = 465
USERNAME  = "emailapikey"
PASSWORD  = "PHtE6r0EEem43WcqoxAF4f7qH8L1PIov9LhuKQESuY0WCv8AF01SqtArlj61ox55UqURE6Kaz9k74rPOsOyHJD7vMz0fVGqyqK3sx/VYSPOZsbq6x00VtlsecUXZUYbvcdJo1yDWvtvaNA=="
FROM_ADDR = "santosh@pressdetective.com"
FROM_NAME = "Santosh | Press Detective"
TO_ADDR   = "sagarzaveri.tbz@gmail.com"
CC_ALWAYS = ["tonymony@gmail.com"]

SUBJECT = "Prateek Gupta — Name Clarity Plan | Press Detective"

HTML = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, sans-serif; font-size: 14px; color: #333; margin: 0; padding: 0; }
  .wrap { max-width: 700px; margin: 32px auto; padding: 0 24px; }
  h1 { color: #1F4E79; font-size: 20px; margin-bottom: 4px; }
  h2 { color: #1F4E79; font-size: 16px; margin: 28px 0 8px;
       border-bottom: 2px solid #1F4E79; padding-bottom: 6px; }
  h3 { color: #333; font-size: 14px; margin: 16px 0 6px; }
  .sub { color: #595959; font-size: 13px; margin-bottom: 28px; }
  p { line-height: 1.7; margin: 0 0 12px; }
  ul, ol { padding-left: 22px; }
  li { margin-bottom: 8px; line-height: 1.65; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0 20px; font-size: 13px; }
  th { background: #1F4E79; color: #fff; text-align: left; padding: 8px 10px; }
  td { padding: 8px 10px; border-bottom: 1px solid #ddd; vertical-align: top; }
  tr:nth-child(even) td { background: #f5f8fb; }
  .pill { display: inline-block; padding: 2px 9px; border-radius: 10px; font-size: 12px;
          font-weight: bold; color: #fff; }
  .pill-red    { background: #C00000; }
  .pill-amber  { background: #BF8F00; }
  .pill-blue   { background: #1F4E79; }
  .pill-green  { background: #538135; }
  .note { background: #fff8e6; border-left: 3px solid #BF8F00; padding: 12px 16px;
          font-size: 13px; color: #444; margin: 16px 0; border-radius: 2px; }
  .alert { background: #fdf0f0; border-left: 3px solid #C00000; padding: 12px 16px;
           font-size: 13px; color: #444; margin: 16px 0; border-radius: 2px; }
  .block { background: #f0f4fa; border-left: 3px solid #1F4E79; padding: 12px 16px;
           font-size: 13px; font-family: monospace; white-space: pre-wrap;
           margin: 10px 0; border-radius: 2px; }
  .footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #ddd;
            font-size: 12px; color: #888; }
  .sig-name { font-weight: bold; color: #1F4E79; font-size: 15px; }
  .toc { background: #f5f8fb; padding: 14px 20px; border-radius: 4px;
         margin-bottom: 28px; font-size: 13px; }
  .toc li { margin-bottom: 4px; }
</style>
</head>
<body>
<div class="wrap">

  <h1>Prateek Gupta — Name Clarity Plan</h1>
  <div class="sub">Press Detective &nbsp;|&nbsp; Confidential &nbsp;|&nbsp; 9 June 2026</div>

  <p>Dear Sagar,</p>
  <p>Thank you for reaching out regarding Mr Prateek Gupta. We have reviewed the situation fully
  and set out below our complete Name Clarity Plan — what we can do, in what order, and within
  what guardrails. We ask that you share this with Mr Gupta and confirm how you would like to
  proceed.</p>

  <div class="toc">
    <strong>Contents</strong>
    <ol>
      <li>Situation assessment</li>
      <li>Track 1 — Legal (the only route to change the finding)</li>
      <li>Track 2 — Digital presence build (suppression strategy)</li>
      <li>Track 3 — Media response (narrow and accurate)</li>
      <li>Track 4 — Wikipedia &amp; AI knowledge panels</li>
      <li>Timeline &amp; milestones</li>
      <li>What we need from you</li>
      <li>Guardrails</li>
    </ol>
  </div>

  <!-- ─── 1. SITUATION ─────────────────────────────────────────── -->
  <h2>1. Situation assessment</h2>

  <p>The UK High Court (Mr Justice Saini) handed down a final judgment on 30 January 2026 in
  <em>Trafigura Pte Ltd &amp; Anor v Gupta &amp; Ors</em> [2026] EWHC 159 (Comm), finding Mr Gupta
  liable for fraud involving ~US$500 million in nickel transactions. The court also found that
  the former Trafigura employees he identified as perpetrators were innocent. The High Court
  refused permission to appeal in February 2026.</p>

  <p>Mr Gupta disputes the judgment. The appeal window to the <strong>Court of Appeal</strong>
  may still be open — or may require an extension-of-time application. That question must be
  confirmed by solicitors <em>before anything else</em>.</p>

  <div class="alert">
    <strong>Critical constraint:</strong> A final, publicly indexed court judgment exists. Unlike
    cases where charges were dropped or acquittals obtained, there is no clean chit to cite.
    The only honest and legally safe narrative is: <em>"Mr Gupta disputes the judgment and is
    pursuing legal remedies."</em> Any communication that goes further — asserting innocence as
    established fact or re-accusing the court-cleared Trafigura employees — is both defamatory
    and harmful to any appeal. Everything in this plan operates within that boundary.
  </div>

  <!-- ─── 2. LEGAL ──────────────────────────────────────────────── -->
  <h2>2. Track 1 — Legal <span style="font-weight:normal;font-size:13px;color:#595959;">(the only route that can actually change the finding)</span></h2>

  <div class="note">
    <strong>This track takes absolute priority.</strong> If the appeal succeeds, the finding is
    overturned and every other track becomes dramatically easier. If it fails, the plan below
    manages the reputational position within what the record allows.
  </div>

  <table>
    <thead><tr><th>Step</th><th>Action</th><th>Urgency</th></tr></thead>
    <tbody>
      <tr>
        <td><span class="pill pill-red">1</span></td>
        <td><strong>Confirm representation.</strong> Mr Gupta's former solicitors came off the record on 27 Jan 2026. Is he currently represented? If not, this is the single most urgent task.</td>
        <td>Immediate</td>
      </tr>
      <tr>
        <td><span class="pill pill-red">2</span></td>
        <td><strong>Verify the Court of Appeal deadline.</strong> Permission to renew at the Court of Appeal typically requires filing within 21 days of the High Court refusal. If that window has passed, an extension-of-time application is needed — requiring a credible explanation for the delay.</td>
        <td>Immediate</td>
      </tr>
      <tr>
        <td><span class="pill pill-amber">3</span></td>
        <td><strong>Engage commercial-appeals counsel.</strong> KCs and firms experienced in High Court commercial fraud appeals. Press Detective can help build a shortlist and draft a neutral outreach note.</td>
        <td>This week</td>
      </tr>
      <tr>
        <td><span class="pill pill-amber">4</span></td>
        <td><strong>Evidence brief for counsel.</strong> We prepare a factual dossier: transaction chronology, document index, Mr Gupta's point-by-point account cross-referenced to available documents, and a candidate "new evidence" log. Counsel reviews and decides what is arguable on appeal.</td>
        <td>2–4 weeks</td>
      </tr>
    </tbody>
  </table>

  <!-- ─── 3. DIGITAL PRESENCE ───────────────────────────────────── -->
  <h2>3. Track 2 — Digital presence build <span style="font-weight:normal;font-size:13px;color:#595959;">(suppression strategy)</span></h2>

  <p>Search results for "Prateek Gupta" are currently dominated by judgment coverage from GTR,
  Global Investigations Review, Mining.com, and others. We cannot remove accurate reporting of
  a public court judgment. What we <em>can</em> do is build strong, current, professional pages
  that rank above the case coverage over time. This is the core of the name clarity work.</p>

  <h3><span class="pill pill-blue">A</span> &nbsp;Personal website</h3>
  <p>A personal website (e.g. <em>prateekgupta.co</em> or similar) is the highest-impact suppression
  asset. Personal sites consistently rank on page 1 for personal names within 30–60 days of
  indexing. Three pages are needed:</p>
  <table>
    <thead><tr><th>Page</th><th>Purpose</th><th>SEO role</th></tr></thead>
    <tbody>
      <tr>
        <td><strong>Home / About</strong></td>
        <td>Professional bio, career highlights, headshot</td>
        <td>Primary ranking target for "Prateek Gupta"</td>
      </tr>
      <tr>
        <td><strong>Commentary</strong></td>
        <td>Articles on commodities, nickel markets, trade finance</td>
        <td>Long-tail keywords; builds domain authority</td>
      </tr>
      <tr>
        <td><strong>Contact</strong></td>
        <td>Professional contact form / LinkedIn link</td>
        <td>Signals active, real person to Google</td>
      </tr>
    </tbody>
  </table>
  <p><strong>Timeline:</strong> placeholder page live in 3 days of domain registration;
  full site with bio and first article in 2 weeks.</p>

  <h3><span class="pill pill-blue">B</span> &nbsp;LinkedIn profile</h3>
  <p>LinkedIn ranks on page 1 for virtually every personal name. A complete, active profile is
  the fastest suppression asset we can deploy.</p>
  <table>
    <thead><tr><th>Element</th><th>Our recommendation</th></tr></thead>
    <tbody>
      <tr><td>Headline</td><td>Commodities &amp; Trade Finance Professional | Nickel &amp; Base Metals | [Location]</td></tr>
      <tr><td>Custom URL</td><td>linkedin.com/in/prateekgupta (or closest available)</td></tr>
      <tr><td>About</td><td>800–1,000 words: career summary, sector expertise, forward-looking</td></tr>
      <tr><td>Featured</td><td>Pin website; any published market commentary</td></tr>
      <tr><td>Activity</td><td>1–2 posts/week: commodities markets, nickel, trade finance commentary</td></tr>
    </tbody>
  </table>
  <p>We draft the full About section once Mr Gupta supplies his career timeline.</p>

  <h3><span class="pill pill-blue">C</span> &nbsp;Published commentary</h3>
  <p>Articles published under Mr Gupta's name on third-party platforms (LinkedIn articles,
  commodity/trade media, Medium, Substack) build independent ranking weight. We recommend
  one substantive piece per month on nickel markets, base metals, or trade finance — his
  genuine area of expertise. These articles need make no reference to the litigation.</p>

  <!-- ─── 4. MEDIA ──────────────────────────────────────────────── -->
  <h2>4. Track 3 — Media response <span style="font-weight:normal;font-size:13px;color:#595959;">(narrow and accurate only)</span></h2>

  <p>Coverage of the judgment is accurate reporting of a public court decision. Demanding
  its removal or retraction is not a viable or productive strategy. What we can do:</p>

  <h3><span class="pill pill-amber">A</span> &nbsp;Right-of-reply statement (once, selectively)</h3>
  <p>We have drafted a statement for Mr Gupta. It states that he disputes the judgment and
  is pursuing legal remedies. It makes no claim of innocence as established fact and does not
  re-accuse the court-cleared individuals. It should be issued <strong>only after clearance
  from current solicitors</strong> and only to outlets that have directly sought comment or
  that carry significant errors alongside their judgment coverage.</p>

  <div class="block">Statement from Prateek Gupta

I respectfully but firmly disagree with the High Court's judgment of 30 January 2026.
Throughout these proceedings I have maintained my account of the transactions at the centre
of this dispute, and I continue to do so. I believe important parts of the commercial context
were not given the weight I consider they deserved.

I am taking advice on all avenues still open to me, including renewing my application for
permission to appeal to the Court of Appeal. Out of respect for that process I will not
litigate the detail in the press, but I did not act with the dishonesty the judgment
attributes to me, and I intend to keep contesting that conclusion through the proper
legal channels.</div>

  <h3><span class="pill pill-amber">B</span> &nbsp;Correction requests (specific factual errors only)</h3>
  <p>Where a named article contains a concrete, provable factual mistake — a wrong figure,
  a misidentified entity, a wrong date — we prepare a targeted correction request. This is
  NOT a vehicle for disputing the court's conclusions. We assess each article individually
  before recommending a request.</p>

  <!-- ─── 5. WIKIPEDIA ─────────────────────────────────────────── -->
  <h2>5. Track 4 — Wikipedia &amp; AI knowledge panels</h2>

  <p>If Wikipedia or AI-generated knowledge panels (Grok, Google Knowledge Graph, etc.) contain
  entries for Mr Gupta, we review them for accuracy. Accurate reporting of the judgment cannot
  be removed. What we can request — via the Wikipedia Talk page process with COI disclosure —
  is that entries reflect that he <em>disputes</em> the judgment and is pursuing further legal
  steps, rather than presenting the finding as the definitive and final account. Once any appeal
  is filed, that fact should appear in any such entry.</p>

  <!-- ─── 6. TIMELINE ──────────────────────────────────────────── -->
  <h2>6. Timeline &amp; milestones</h2>
  <table>
    <thead><tr><th>Milestone</th><th>Horizon</th><th>Dependency</th></tr></thead>
    <tbody>
      <tr><td>Confirm solicitor status and appeal deadline</td><td><strong>This week</strong></td><td>Mr Gupta</td></tr>
      <tr><td>Website domain registered + placeholder live</td><td>3 days</td><td>Press Detective</td></tr>
      <tr><td>Right-of-reply statement ready to issue</td><td>Ready now</td><td>Solicitor clearance first</td></tr>
      <tr><td>LinkedIn profile fully built</td><td>1 week</td><td>Career timeline from Mr Gupta</td></tr>
      <tr><td>Full website with bio + first article</td><td>2 weeks</td><td>Bio + headshot from Mr Gupta</td></tr>
      <tr><td>Evidence brief for counsel (chronology + doc index)</td><td>2–4 weeks</td><td>Case materials from Mr Gupta</td></tr>
      <tr><td>Counsel shortlist + outreach note</td><td>3–5 days</td><td>Confirmation needed has no solicitors</td></tr>
      <tr><td>Wikipedia / AI panel review &amp; correction</td><td>2–6 weeks</td><td>Press Detective</td></tr>
      <tr><td>First SERP measurement checkpoint</td><td>30 days</td><td>—</td></tr>
      <tr><td>Full assessment checkpoint</td><td>90 days</td><td>—</td></tr>
      <tr>
        <td><strong>If appeal filed and succeeds →</strong> Narrative anchor changes completely;<br>
        issue updated statement, correct Wikipedia, pursue targeted corrections</td>
        <td>TBD</td><td>Legal outcome</td>
      </tr>
    </tbody>
  </table>

  <!-- ─── 7. WHAT WE NEED ──────────────────────────────────────── -->
  <h2>7. What we need from you — 4 items</h2>
  <div class="note">
    <strong>Please reply with these as soon as possible:</strong>
    <ol style="margin:8px 0 0;">
      <li><strong>Does Mr Gupta currently have solicitors?</strong> Yes or No. If yes, their name and
      contact so we can coordinate. If no, we prepare a counsel shortlist immediately.</li>
      <li><strong>Career timeline.</strong> Current role/title, firm, and a 200-word professional bio.
      This unlocks the website and LinkedIn builds.</li>
      <li><strong>Case materials.</strong> Whatever Mr Gupta has — WhatsApp records, contracts,
      correspondence, the HC judgment itself. We use these to build the evidence brief for counsel.</li>
      <li><strong>Headshot.</strong> A professional photograph for the website and LinkedIn profile.</li>
    </ol>
  </div>

  <!-- ─── 8. GUARDRAILS ─────────────────────────────────────────── -->
  <h2>8. Guardrails (non-negotiable)</h2>
  <ul>
    <li>We do <strong>not</strong> assert innocence as established fact — his position is framed
    as his contested account.</li>
    <li>We do <strong>not</strong> re-accuse the court-cleared Trafigura employees in any
    communication. The court found them innocent; doing so is defamatory and would harm any appeal.</li>
    <li>We do <strong>not</strong> demand retraction of accurate judgment reporting.</li>
    <li>We do <strong>not</strong> send mass communications to government officials, journalists,
    or publications.</li>
    <li>All public statements are cleared by Mr Gupta's current solicitors before release.</li>
    <li>Genuine new evidence goes to counsel and the court — never to the press first.</li>
  </ul>

  <p>We are ready to begin immediately on the digital build (Tracks 2) in parallel while Track 1
  (legal) is being organised. Please reply with confirmation to proceed and the four items
  listed above.</p>

  <p>
    <span class="sig-name">Santosh</span><br>
    Press Detective<br>
    <a href="mailto:santosh@pressdetective.com" style="color:#1F4E79;">santosh@pressdetective.com</a>
  </p>

  <div class="footer">
    Confidential — prepared for Sagar Zaveri / Prateek Gupta only. This is a strategic plan,
    not legal advice. Matters before the UK courts require qualified legal counsel.
  </div>

</div>
</body>
</html>
"""


def send():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = TO_ADDR
    msg["Cc"]      = ", ".join(CC_ALWAYS)

    msg.attach(MIMEText(HTML, "html", "utf-8"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx) as s:
        s.login(USERNAME, PASSWORD)
        s.sendmail(FROM_ADDR, [TO_ADDR] + CC_ALWAYS, msg.as_bytes())
    print(f"Sent to {TO_ADDR}, CC: {', '.join(CC_ALWAYS)}")


if __name__ == "__main__":
    send()
