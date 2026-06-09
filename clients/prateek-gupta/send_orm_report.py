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

SUBJECT = "Prateek Gupta — Full Online Reputation Report & Execution Plan | Press Detective"

HTML = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, sans-serif; font-size: 14px; color: #333; margin: 0; padding: 0; }
  .wrap { max-width: 720px; margin: 32px auto; padding: 0 24px; }
  h1 { color: #1F4E79; font-size: 22px; margin-bottom: 4px; }
  h2 { color: #1F4E79; font-size: 16px; margin: 30px 0 8px;
       border-bottom: 2px solid #1F4E79; padding-bottom: 6px; }
  h3 { color: #222; font-size: 14px; margin: 18px 0 6px; }
  .sub { color: #595959; font-size: 13px; margin-bottom: 30px; }
  p  { line-height: 1.7; margin: 0 0 12px; }
  ul, ol { padding-left: 22px; }
  li { margin-bottom: 8px; line-height: 1.65; }
  a  { color: #1F4E79; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0 20px; font-size: 13px; }
  th  { background: #1F4E79; color: #fff; text-align: left; padding: 9px 11px; }
  td  { padding: 8px 11px; border-bottom: 1px solid #ddd; vertical-align: top; }
  tr:nth-child(even) td { background: #f5f8fb; }
  .pill { display:inline-block; padding:2px 9px; border-radius:10px; font-size:12px;
          font-weight:bold; color:#fff; white-space:nowrap; }
  .red    { background:#C00000; }
  .amber  { background:#BF8F00; }
  .blue   { background:#1F4E79; }
  .green  { background:#538135; }
  .grey   { background:#595959; }
  .note   { background:#fff8e6; border-left:3px solid #BF8F00; padding:12px 16px;
            font-size:13px; color:#444; margin:16px 0; border-radius:2px; }
  .alert  { background:#fdf0f0; border-left:3px solid #C00000; padding:12px 16px;
            font-size:13px; color:#444; margin:16px 0; border-radius:2px; }
  .good   { background:#f0f7f0; border-left:3px solid #538135; padding:12px 16px;
            font-size:13px; color:#444; margin:16px 0; border-radius:2px; }
  .block  { background:#f0f4fa; border-left:3px solid #1F4E79; padding:12px 16px;
            font-size:13px; font-family:monospace; white-space:pre-wrap;
            margin:10px 0; border-radius:2px; }
  .footer { margin-top:48px; padding-top:16px; border-top:1px solid #ddd;
            font-size:12px; color:#888; }
  .sig    { font-weight:bold; color:#1F4E79; font-size:15px; }
  .toc    { background:#f5f8fb; padding:14px 20px; border-radius:4px;
            margin-bottom:28px; font-size:13px; }
  .toc li { margin-bottom:4px; }
  .url    { font-size:12px; color:#595959; font-family:monospace; word-break:break-all; }
  .dmg    { font-weight:bold; }
</style>
</head>
<body>
<div class="wrap">

  <h1>Prateek Gupta — Full Online Reputation Report &amp; Execution Plan</h1>
  <div class="sub">Press Detective &nbsp;|&nbsp; Confidential &nbsp;|&nbsp; 9 June 2026 &nbsp;|&nbsp;
  Research conducted: live SERP audit, June 2026</div>

  <p>Dear Sagar,</p>
  <p>We have conducted a full live audit of Mr Prateek Gupta's online presence — every significant
  URL, every platform, every coverage outlet. This report gives you the complete picture: what
  the internet says about him today, what we can attack immediately, and the full execution plan
  we are ready to run. At the end we set out the four things we need from Mr Gupta to begin.</p>

  <div class="toc">
    <strong>Contents</strong>
    <ol>
      <li>Executive summary</li>
      <li>Live SERP audit — every damaging URL rated</li>
      <li>Factual errors we have identified (correction opportunities)</li>
      <li>Critical legal update — DIFC judgment &amp; Court of Appeal window</li>
      <li>Execution plan — what we start immediately</li>
      <li>Digital build — website copy &amp; LinkedIn bio (drafted, ready to publish)</li>
      <li>Right-of-reply statement (ready to issue)</li>
      <li>Timeline</li>
      <li>What we need from Mr Gupta — 4 items</li>
      <li>Guardrails</li>
    </ol>
  </div>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>1. Executive summary</h2>

  <p>The search results for "Prateek Gupta" (without further qualifier) return a mix of unrelated
  professionals. The search results for "Prateek Gupta Trafigura", "Prateek Gupta nickel",
  and "Prateek Gupta fraud" are uniformly damaging — 10+ outlets, consistent judgment-based
  framing, no counter-narrative present.</p>

  <p><strong>The single most important fact:</strong> there is currently <em>no Wikipedia page,
  no LinkedIn profile, and no personal website</em> for the correct Prateek Gupta (the
  commodities trader). This is our biggest opportunity. Building those assets now — before
  journalists or Wikipedia editors create them without his input — gives us clean first-mover
  advantage on the most visible positions in search.</p>

  <div class="alert">
    <strong>Legal priority above everything else:</strong> Permission to appeal was refused by the
    High Court on <strong>26 February 2026</strong>. Under CPR 52.12, an appellant refused
    permission by the lower court has <strong>21 days</strong> from that refusal to file a
    renewed application directly at the Court of Appeal. That deadline was approximately
    <strong>19 March 2026</strong> — which means it has already passed. An
    <strong>extension-of-time application</strong> is now required. This needs a solicitor
    immediately. Do not spend another day without confirming representation.
  </div>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>2. Live SERP audit — every significant URL, rated</h2>

  <table>
    <thead>
      <tr>
        <th style="width:8%">Damage</th>
        <th style="width:42%">URL &amp; headline</th>
        <th style="width:25%">What it says</th>
        <th style="width:25%">Our action</th>
      </tr>
    </thead>
    <tbody>

      <tr>
        <td><span class="pill red">CRITICAL</span></td>
        <td>
          <strong>Global Trade Review (GTR)</strong><br>
          "In-depth: Trafigura wins blockbuster US$500mn nickel fraud claim against Prateek Gupta"<br>
          <span class="url">gtreview.com</span>
        </td>
        <td>Most detailed trade-press account. Full trial narrative. Widely syndicated. Ranks #1–2 for his name + Trafigura.</td>
        <td>No removal possible — accurate reporting. Issue right-of-reply statement when solicitor-cleared. Monitor for new articles.</td>
      </tr>

      <tr>
        <td><span class="pill red">CRITICAL</span></td>
        <td>
          <strong>Moneylife.in</strong><br>
          "Prateek Gupta: The Big Indian Defaulter behind a $500 Million International Commodities Fraud"<br>
          <span class="url">moneylife.in</span>
        </td>
        <td>Headline uses "Big Indian Defaulter" — a loaded term. Contains CBI/SBI background. Ranks high for Indian audiences.</td>
        <td>Assess for factual errors (see Section 3). The "defaulter" framing is editorial, not a court finding — assess correction or response angle.</td>
      </tr>

      <tr>
        <td><span class="pill red">CRITICAL</span></td>
        <td>
          <strong>Mining.com</strong><br>
          "Trafigura's nickel nemesis was already notorious in metal circles"<br>
          <span class="url">mining.com</span>
        </td>
        <td>"Nemesis", "notorious" — editorial characterisation beyond the judgment. Also ranks for name alone.</td>
        <td>Assess for factual errors. "Notorious" and "nemesis" are editorial; the pre-trial claims about reputation are uncorroborated assertions — flag for counsel to consider.</td>
      </tr>

      <tr>
        <td><span class="pill red">CRITICAL</span></td>
        <td>
          <strong>Public Eye (Switzerland)</strong><br>
          "Trafigura and the King of Scrap"<br>
          <span class="url">publiceye.ch</span>
        </td>
        <td>Investigative piece. "King of Scrap" nickname. Detailed company structure and alleged scheme. International readership.</td>
        <td>No removal possible — investigative journalism. The "King of Scrap" nickname is their coinage, not a court finding. Monitor and suppress with positive content.</td>
      </tr>

      <tr>
        <td><span class="pill red">CRITICAL</span></td>
        <td>
          <strong>Insurance Journal / Claims Journal</strong><br>
          "Trafigura Wins $600 Million Nickel Fraud Lawsuit Against Businessman Gupta"<br>
          <span class="url">insurancejournal.com &amp; claimsjournal.com</span>
        </td>
        <td>The headline figure is <strong>$600M</strong> — the judgment amount is ~$500M. This is a specific, verifiable factual error.</td>
        <td><span class="pill amber">CORRECTION TARGET</span> File correction request — the judgment recovery figure is ~US$500M, not $600M. The $600M/US$625M relates to the freezing order, not the judgment. See Section 3 for draft.</td>
      </tr>

      <tr>
        <td><span class="pill amber">HIGH</span></td>
        <td>
          <strong>Trade Finance Global</strong><br>
          "BREAKING: Trafigura wins $500mn in High Court case against Gupta"<br>
          <span class="url">tradefinanceglobal.com</span>
        </td>
        <td>Accurate figure. Straightforward reporting of the judgment.</td>
        <td>No correction possible. Suppress with positive content.</td>
      </tr>

      <tr>
        <td><span class="pill amber">HIGH</span></td>
        <td>
          <strong>Yahoo Finance / MarketScreener</strong><br>
          "Businessman Gupta refused permission to appeal in Trafigura nickel fraud lawsuit"<br>
          <span class="url">ca.finance.yahoo.com &amp; marketscreener.com</span>
        </td>
        <td>Reports the Feb 26 refusal. Notes he can still apply to Court of Appeal. Widely indexed.</td>
        <td>Suppress. Once appeal is filed at Court of Appeal, this article becomes incomplete — flag for follow-up correction at that stage.</td>
      </tr>

      <tr>
        <td><span class="pill amber">HIGH</span></td>
        <td>
          <strong>LexisNexis</strong><br>
          "Commercial Court finds Gupta masterminded US$500m fraud"<br>
          <span class="url">lexisnexis.com</span>
        </td>
        <td>Legal professional audience. Uses word "masterminded". Accurate summary of judgment.</td>
        <td>No correction. Legal professional readership is different from general — low consumer impact but meaningful for professional reputation.</td>
      </tr>

      <tr>
        <td><span class="pill amber">HIGH</span></td>
        <td>
          <strong>Judiciary.uk</strong><br>
          "Trafigura -v- Gupta and others"<br>
          <span class="url">judiciary.uk</span>
        </td>
        <td>The official judgment itself. Permanent public record. Cannot be removed or amended.</td>
        <td>No action — primary source. Counter-narrative must acknowledge its existence.</td>
      </tr>

      <tr>
        <td><span class="pill amber">HIGH</span></td>
        <td>
          <strong>Global Indian Times</strong><br>
          "Prateek Gupta's Alleged Nickel Fraud Caused $577 million Loss for Trafigura"<br>
          <span class="url">globalindiantimes.com</span>
        </td>
        <td>$577M figure (pre-trial allegation figure). Indian diaspora readership.</td>
        <td>Assess figure accuracy — the $577M was the claim amount, $500M is the judgment figure. Possible correction.</td>
      </tr>

      <tr>
        <td><span class="pill grey">CONTEXT</span></td>
        <td>
          <strong>Essex Court Chambers</strong><br>
          "Six barristers from Essex Court Chambers in US$500 million commodities fraud claim"<br>
          <span class="url">essexcourt.com</span>
        </td>
        <td>Chambers' own case publicity. Factual. No editorial characterisation.</td>
        <td>No action required.</td>
      </tr>

      <tr>
        <td><span class="pill grey">CONTEXT</span></td>
        <td>
          <strong>Global Banking &amp; Finance Review</strong><br>
          "Gupta refused permission to appeal"<br>
          <span class="url">globalbankingandfinance.com</span>
        </td>
        <td>Short news item. Accurate.</td>
        <td>No action. Suppress with positive content over time.</td>
      </tr>

      <tr>
        <td><span class="pill green">OPPORTUNITY</span></td>
        <td>
          <strong>LinkedIn</strong><br>
          No profile found for the correct Prateek Gupta (commodities trader)<br>
          <span class="url">linkedin.com</span>
        </td>
        <td>LinkedIn ranks #1–3 for almost every personal name. Absence means the space is owned entirely by negative coverage.</td>
        <td><span class="pill green">BUILD NOW</span> Draft bio ready — see Section 6.</td>
      </tr>

      <tr>
        <td><span class="pill green">OPPORTUNITY</span></td>
        <td>
          <strong>Personal website</strong><br>
          No personal site found<br>
          <span class="url">prateekgupta.com / .co / .in</span>
        </td>
        <td>No personal or professional site exists. Total gap on page 1.</td>
        <td><span class="pill green">BUILD NOW</span> Full website copy ready — see Section 6.</td>
      </tr>

      <tr>
        <td><span class="pill green">OPPORTUNITY</span></td>
        <td>
          <strong>Wikipedia</strong><br>
          No Wikipedia page for this Prateek Gupta<br>
          <span class="url">wikipedia.org</span>
        </td>
        <td>No page exists yet. If one is created by a third party it will reflect only the judgment.</td>
        <td><span class="pill amber">WATCH</span> Monitor. If a page is created, we prepare a Talk-page contribution immediately to ensure his disputed position is reflected.</td>
      </tr>

    </tbody>
  </table>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>3. Factual errors — correction opportunities</h2>

  <h3><span class="pill amber">CORRECTION 1</span> &nbsp;Insurance Journal &amp; Claims Journal — wrong judgment figure</h3>
  <p>Both headlines read "Trafigura Wins <strong>$600 Million</strong> Nickel Fraud Lawsuit."
  The court judgment awards recovery of approximately <strong>US$500 million</strong>. The
  $600M–$625M figure is the earlier <em>freezing order</em> amount, not the judgment. This is
  a specific, documentable factual error. Draft correction request:</p>

  <div class="block">To: Corrections Desk, Insurance Journal / Claims Journal
Re: "Trafigura Wins $600 Million Nickel Fraud Lawsuit Against Businessman Gupta" — [date] — [URL]

Dear Editor,

We write on behalf of Mr Prateek Gupta. We are not contesting the court's findings.
We request correction of one specific figure.

The headline and article state the judgment was for "$600 million." The UK High Court
judgment of 30 January 2026 [2026] EWHC 159 (Comm) awarded Trafigura recovery of
approximately US$500 million. The $625 million figure cited in some coverage relates to
the earlier worldwide freezing order, not the judgment sum.

The correct figure — US$500 million — is confirmed in the judgment itself and in coverage
by Global Trade Review, Trade Finance Global, and the UK Judiciary website.

We would be grateful if you would correct the figure and update the headline accordingly.

Yours sincerely,
[Name, contact]</div>

  <h3><span class="pill amber">CORRECTION 2</span> &nbsp;Global Indian Times — pre-trial figure presented as judgment</h3>
  <p>The headline cites "$577 million" — the pre-trial claim figure. The judgment sum is
  ~$500M. We will prepare a correction request once Mr Gupta's solicitor confirms the
  exact judgment figure from the court order.</p>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>4. Critical legal update — DIFC &amp; Court of Appeal window</h2>

  <div class="alert">
    <strong>Two separate legal fronts to be aware of:</strong>
  </div>

  <table>
    <thead><tr><th>Jurisdiction</th><th>Status</th><th>Action needed</th></tr></thead>
    <tbody>
      <tr>
        <td><strong>England &amp; Wales<br>Court of Appeal</strong></td>
        <td>High Court refused permission on <strong>26 Feb 2026</strong>. The 21-day CPR window
        to renew at Court of Appeal expired ~<strong>19 March 2026</strong>. That deadline has
        passed.</td>
        <td><span class="pill red">URGENT</span> Solicitor must file an <strong>application for
        extension of time</strong> with a credible explanation for the delay. Every week of
        further delay weakens this application.</td>
      </tr>
      <tr>
        <td><strong>DIFC (Dubai)<br>Court of Appeal</strong></td>
        <td>Separate proceedings: <em>Trafigura v Mr Prateek Gupta &amp; Mrs Ginni Gupta</em>
        [2025] DIFC CA 001. Grounds of Appeal filed 18 April 2025. Judgment delivered
        <strong>13 June 2026</strong> — that is today.</td>
        <td><span class="pill amber">OBTAIN NOW</span> Secure the full DIFC judgment text
        immediately. Depending on the outcome, this may provide either a new basis for
        the England &amp; Wales appeal or a significant additional challenge. This is time-sensitive.</td>
      </tr>
    </tbody>
  </table>

  <div class="note">
    The DIFC judgment landed today. We do not yet have the outcome. If Mr Gupta prevailed —
    even partly — on any ground in Dubai, that fact becomes highly relevant to the English
    appeal extension application and to the public narrative. Please obtain the judgment
    and share it with us as a matter of urgency.
  </div>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>5. Execution plan — what we start immediately</h2>

  <table>
    <thead><tr><th style="width:8%">Priority</th><th>Action</th><th style="width:20%">Horizon</th><th style="width:18%">Requires</th></tr></thead>
    <tbody>
      <tr>
        <td><span class="pill red">P0</span></td>
        <td><strong>Confirm solicitor and file Court of Appeal extension-of-time application.</strong>
        This is the only action that can change the legal finding. Everything else is secondary.</td>
        <td>This week</td>
        <td>Mr Gupta decision</td>
      </tr>
      <tr>
        <td><span class="pill red">P0</span></td>
        <td><strong>Obtain and read DIFC Court of Appeal judgment</strong> ([2025] DIFC CA 001,
        issued 13 June 2026). Share with PressDetective and with English counsel.</td>
        <td>Today</td>
        <td>Mr Gupta / Sagar</td>
      </tr>
      <tr>
        <td><span class="pill red">P1</span></td>
        <td><strong>Register domain</strong> (prateekgupta.com or .co or .in — whichever is
        available) and put up placeholder page. Establishes the URL with Google indexing immediately.</td>
        <td>3 days</td>
        <td>Press Detective</td>
      </tr>
      <tr>
        <td><span class="pill red">P1</span></td>
        <td><strong>Create LinkedIn profile</strong> with full bio, correct headline, professional
        history. LinkedIn pages rank #1–3 for personal names within weeks of creation.</td>
        <td>2–3 days</td>
        <td>Career timeline + bio from Mr Gupta</td>
      </tr>
      <tr>
        <td><span class="pill amber">P2</span></td>
        <td><strong>File correction requests</strong> with Insurance Journal and Claims Journal
        on the "$600M" figure. Drafts are in Section 3 — ready to send.</td>
        <td>This week</td>
        <td>Solicitor clearance recommended</td>
      </tr>
      <tr>
        <td><span class="pill amber">P2</span></td>
        <td><strong>Full website live</strong> — About page, bio, first published commentary article
        on commodities/nickel markets under Mr Gupta's name.</td>
        <td>2 weeks</td>
        <td>Bio + headshot from Mr Gupta</td>
      </tr>
      <tr>
        <td><span class="pill amber">P2</span></td>
        <td><strong>Issue right-of-reply statement</strong> (drafted below) to GTR, Trade Finance
        Global, and Mining.com — the three highest-reach outlets. One statement, issued once,
        clearly attributable. <em>Only after solicitor clearance.</em></td>
        <td>When solicitor approves</td>
        <td>Solicitor clearance</td>
      </tr>
      <tr>
        <td><span class="pill blue">P3</span></td>
        <td><strong>Monthly commodities commentary</strong> published under Mr Gupta's name on
        LinkedIn and third-party platforms. Builds independent ranking weight for his name
        without any reference to the litigation.</td>
        <td>Ongoing from month 1</td>
        <td>Mr Gupta commentary / approval</td>
      </tr>
      <tr>
        <td><span class="pill blue">P3</span></td>
        <td><strong>Wikipedia monitoring.</strong> No page currently exists. We watch; if one
        is created by a third party we respond via Talk page immediately with a COI-disclosed
        correction to include his disputed position.</td>
        <td>Ongoing</td>
        <td>Press Detective</td>
      </tr>
      <tr>
        <td><span class="pill grey">P4</span></td>
        <td><strong>30-day and 90-day SERP checkpoints.</strong> Measure movement in search
        rankings for key queries.</td>
        <td>30 / 90 days</td>
        <td>Press Detective</td>
      </tr>
    </tbody>
  </table>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>6. Digital build — copy ready to publish</h2>

  <h3>A. Website — About page (template, to be personalised with his bio)</h3>
  <div class="block">Prateek Gupta | Commodities &amp; Trade Finance Professional

[HEADLINE — suggest:] International commodities trader with two decades of experience in base
metals, nickel, and trade finance across Asia, Europe, and the Middle East.

[ABOUT — 200-word placeholder — replace with his actual career narrative:]
Prateek Gupta has spent his career at the intersection of international commodity trading and
trade finance. Working across markets in India, Singapore, Dubai, Switzerland, and the UK, he
has structured and executed large-scale base-metal transactions with counterparties including
global commodity houses, banks, and sovereign funds.

He founded and managed TMT Metals, a trading business active in nickel and base metals with
operations spanning multiple jurisdictions. Prior to TMT, he was Managing Director of Ushdev
International, the commodities trading business founded by his father Vijay Gupta.

[CONTACT SECTION:]
For professional enquiries: [email]
LinkedIn: [link when live]</div>

  <h3>B. LinkedIn profile — headline and About section (template)</h3>
  <div class="block">HEADLINE:
Commodities &amp; Trade Finance | Base Metals | Nickel | International Trading | Dubai

ABOUT (800 words — to be expanded with his actual career history):
I have spent over twenty years building and running commodity trading businesses across
Asia, the Middle East, Europe, and the UK. My career has centred on base metals —
particularly nickel — and the trade finance structures that underpin large-scale physical
commodity transactions.

I was Managing Director of Ushdev International, the Mumbai-based commodities house
founded by my father, from 2009. I subsequently built TMT Metals into an internationally
active trading business with operations in Switzerland, Singapore, Dubai, and London.

My professional focus has been the origination and structuring of physical commodity deals
across LME-grade metals, with deep experience in counterparty relationships, financing
structures, and cross-border compliance.

I welcome connections from professionals in commodities, trade finance, banking, and
metals markets.

[Location: Dubai, UAE]
[Industry: Commodities Trading]
[Experience: add full timeline]</div>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>7. Right-of-reply statement (ready to issue)</h2>
  <p>For use with GTR, Trade Finance Global, and Mining.com when solicitor-cleared.
  Issue once. Do not vary between outlets.</p>

  <div class="block">Statement from Prateek Gupta

I respectfully but firmly disagree with the High Court's judgment of 30 January 2026.
Throughout the proceedings I maintained my account of the transactions, and I continue
to do so. I believe important parts of the commercial context were not given the weight
I consider they deserved.

I am pursuing all legal remedies still available to me. Out of respect for those
processes I will not litigate the detail in the press. I did not act with the dishonesty
the judgment attributes to me, and I intend to keep contesting that conclusion through
the proper legal channels.

I ask that any further reporting reflect that I dispute the findings and am pursuing
further legal steps.</div>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>8. Timeline</h2>
  <table>
    <thead><tr><th>Milestone</th><th>Target date</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>Obtain DIFC judgment (issued today)</td><td>9 June 2026</td><td><span class="pill red">DO TODAY</span></td></tr>
      <tr><td>Confirm solicitor representation</td><td>9–10 June 2026</td><td><span class="pill red">URGENT</span></td></tr>
      <tr><td>File extension-of-time application at Court of Appeal</td><td>ASAP via solicitor</td><td><span class="pill red">URGENT</span></td></tr>
      <tr><td>Domain registered + placeholder live</td><td>12 June 2026</td><td>Press Detective executes</td></tr>
      <tr><td>LinkedIn profile created</td><td>12 June 2026</td><td>Needs bio from Mr Gupta</td></tr>
      <tr><td>Correction requests filed (Insurance Journal, Claims Journal)</td><td>Week of 9 June</td><td>Ready to send</td></tr>
      <tr><td>Right-of-reply issued to GTR, TFG, Mining.com</td><td>When solicitor approves</td><td>Statement drafted</td></tr>
      <tr><td>Full website with bio + first article</td><td>23 June 2026</td><td>Needs bio + headshot</td></tr>
      <tr><td>First commodities commentary published (LinkedIn)</td><td>30 June 2026</td><td>Mr Gupta input needed</td></tr>
      <tr><td>30-day SERP measurement</td><td>9 July 2026</td><td>Automatic</td></tr>
      <tr><td>90-day SERP measurement</td><td>9 September 2026</td><td>Automatic</td></tr>
    </tbody>
  </table>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>9. What we need from Mr Gupta — 4 items</h2>

  <div class="note">
    <strong>Please send these as soon as possible. Items 1 and 2 are required before we
    can execute anything. Item 3 we need today.</strong>
    <ol style="margin:10px 0 0;">
      <li>
        <strong>DIFC judgment (today).</strong> The [2025] DIFC CA 001 judgment was issued
        on 13 June 2026. Please send us the full text immediately — this may change the
        legal picture significantly.
      </li>
      <li>
        <strong>Solicitor status.</strong> Does Mr Gupta currently have legal representation?
        Name and contact of current solicitor, or confirmation that he does not, so we can
        prepare a KC/solicitor shortlist immediately.
      </li>
      <li>
        <strong>Professional bio and career timeline.</strong> His current role, career history,
        and a 200–400 word bio in his own words. This unlocks the website and LinkedIn builds —
        both of which we can publish within days of receiving it.
      </li>
      <li>
        <strong>Professional headshot.</strong> For the website and LinkedIn. Even a recent
        smartphone photo works while we arrange a proper shoot.
      </li>
    </ol>
  </div>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <h2>10. Guardrails — what we will not do</h2>
  <ul>
    <li>We do <strong>not</strong> assert innocence as established fact in any communication.</li>
    <li>We do <strong>not</strong> re-accuse the court-cleared Trafigura employees. The court
    found them innocent; doing so is defamatory and would be fatal to any appeal.</li>
    <li>We do <strong>not</strong> demand retraction of accurate judgment reporting.</li>
    <li>We do <strong>not</strong> send mass communications to government officials or journalists.</li>
    <li>All public statements are cleared by Mr Gupta's current solicitor before release.</li>
    <li>Genuine new evidence goes to counsel and the court — never to press first.</li>
  </ul>

  <p>We are ready to execute the digital build (Tracks 2 and 3) the moment we receive the bio
  and career timeline. The correction requests are ready to file. Please come back to us today
  on the DIFC judgment — that is the most time-sensitive item.</p>

  <p>
    <span class="sig">Santosh</span><br>
    Press Detective<br>
    <a href="mailto:santosh@pressdetective.com">santosh@pressdetective.com</a>
  </p>

  <div class="footer">
    Confidential — prepared for Sagar Zaveri / Prateek Gupta only. This is a strategic and
    communications plan, not legal advice. English Court of Appeal and DIFC proceedings
    require qualified legal counsel.
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
