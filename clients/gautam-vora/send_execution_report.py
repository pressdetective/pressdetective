"""
Send the full execution-status + intake-request email to Gautam Vora.
FROM: info@pressdetective.com  |  TO: gavora@gmail.com  |  CC: info@pressdetective.com
Attach: Gautam_Vora_Reputation_Audit.docx
"""
import smtplib, ssl, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import cfg

SUBJECT = "Reputation Clearance — Execution Plan & What We Need From You | Press Detective"
DIR = os.path.dirname(os.path.abspath(__file__))

HTML = """\
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{font-family:Arial,sans-serif;font-size:14px;color:#333;margin:0;padding:0}
.wrap{max-width:700px;margin:32px auto;padding:0 24px}
h1{color:#1F4E79;font-size:20px;margin-bottom:4px}
h2{color:#1F4E79;font-size:16px;margin:28px 0 8px;padding-bottom:6px;border-bottom:2px solid #1F4E79}
.sub{color:#595959;font-size:13px;margin-bottom:28px}
p{line-height:1.7;margin:0 0 12px}
ul,ol{padding-left:22px} li{margin-bottom:8px;line-height:1.65}
table{border-collapse:collapse;width:100%;margin:12px 0 20px;font-size:13px}
th{background:#1F4E79;color:#fff;text-align:left;padding:8px 10px}
td{padding:8px 10px;border-bottom:1px solid #ddd;vertical-align:top}
tr:nth-child(even) td{background:#f5f8fb}
.check{color:#538135;font-weight:bold}
.pending{color:#BF8F00;font-weight:bold}
.urgent{background:#fff3cd;border-left:4px solid #BF8F00;padding:14px 18px;margin:16px 0;border-radius:0 4px 4px 0;font-size:13px}
.done{background:#eef7ee;border-left:4px solid #538135;padding:14px 18px;margin:16px 0;border-radius:0 4px 4px 0;font-size:13px}
.block{background:#f0f4fa;border-left:3px solid #1F4E79;padding:12px 16px;font-size:13px;font-family:monospace;white-space:pre-wrap;margin:10px 0;border-radius:0 4px 4px 0}
.footer{margin-top:48px;padding-top:16px;border-top:1px solid #ddd;font-size:12px;color:#888}
.sig{font-weight:bold;color:#1F4E79;font-size:15px}
</style></head><body><div class="wrap">

<h1>Reputation Clearance — Execution Plan &amp; What We Need From You</h1>
<div class="sub">Press Detective &nbsp;|&nbsp; Confidential &nbsp;|&nbsp; 9 June 2026</div>

<p>Dear Gautam,</p>
<p>We have completed the full audit of your online reputation and begun executing the clearance plan.
This email sets out exactly what we have done, what we are doing now, and the three critical pieces
of information we need from you before we can go further.</p>
<p>The full audit report is attached.</p>

<h2>Status — what has been done</h2>
<div class="done">
<strong>&#10003; Completed this week:</strong>
<ul style="margin:8px 0 0">
  <li>Full reputation audit — 12 sources mapped, severity rated, removability assessed</li>
  <li>Prioritized action plan built (P1 → P4 + monitoring)</li>
  <li>Three Google removal request drafts written — Yahoo News, Business Standard, DNA India</li>
  <li>Wikipedia Talk page correction drafted (ready to post with COI disclosure)</li>
  <li>Grokipedia correction submission drafted (ready to file)</li>
  <li>Personal website built and ready to deploy at gautamvora.com (pending domain registration)</li>
  <li>LinkedIn profile brief written</li>
  <li>Monitoring framework set up (Google Alerts queue)</li>
</ul>
</div>

<h2>What we are executing now (no input needed)</h2>
<table>
  <thead><tr><th>Action</th><th>Status</th><th>Horizon</th></tr></thead>
  <tbody>
    <tr><td>Personal website (gautamvora.com) — placeholder live</td>
        <td><span class="pending">Pending domain registration</span></td><td>Day 1–3</td></tr>
    <tr><td>Wikipedia Talk page — post correction request with COI disclosure</td>
        <td><span class="pending">Ready to post — awaiting your go-ahead</span></td><td>This week</td></tr>
    <tr><td>Grokipedia correction submission</td>
        <td><span class="pending">Ready to submit — awaiting your go-ahead</span></td><td>This week</td></tr>
    <tr><td>LinkedIn profile build</td>
        <td><span class="pending">Draft ready — need career details from you</span></td><td>Week 1</td></tr>
    <tr><td>Market commentary content (3 seed articles)</td>
        <td><span class="pending">Drafting in progress</span></td><td>Week 2</td></tr>
    <tr><td>Google removal requests filed</td>
        <td><span class="pending">Drafts ready — stronger with your court docs</span></td><td>Week 1–2</td></tr>
    <tr><td>Dale Bhagwagar Media Group outreach</td>
        <td><span class="check">Queued</span></td><td>Week 2</td></tr>
    <tr><td>30-day SERP measurement</td>
        <td><span class="check">Scheduled</span></td><td>Day 30</td></tr>
  </tbody>
</table>

<h2>What we need from you — 3 critical items</h2>

<div class="urgent">
<strong>Please reply with these as soon as possible:</strong>

<p style="margin-top:10px"><strong>1. Final outcome of the Tikku / Palande matter (most important)</strong><br>
Were you <em>discharged, acquitted, or is it still pending?</em> Please attach any court order,
discharge certificate, or bail order you have. This single fact makes our Google removal requests
and de-indexing petitions significantly stronger. Without it we file with less leverage; with a
discharge or acquittal order we can argue formal exoneration.</p>

<p><strong>2. Current professional role</strong><br>
Your title, employer / firm name, and a one-line description of what you do today
(e.g. "Independent equity analyst, Mumbai" or "Director, XYZ Capital Ltd").
This goes on your website, LinkedIn, and in all our published content.</p>

<p><strong>3. LinkedIn profile URL</strong><br>
If you have an existing LinkedIn, share the URL so we can build on it.
If not, share your full career timeline (firms, roles, dates) and we will create one.</p>
</div>

<p><strong>Also useful when you have time:</strong></p>
<ul>
  <li>The August 2010 police clean chit / closure report (even an informal document helps)</li>
  <li>A professional bio (100–200 words) and a headshot for the website</li>
  <li>Any existing professional website or social handles you control</li>
  <li>Any positive press, market commentary or media quotes you have given</li>
</ul>

<h2>The Google removal requests — drafts ready to file</h2>
<p>We have three submissions ready. Here are the key arguments for each:</p>
<table>
  <thead><tr><th>URL</th><th>Ground for removal</th></tr></thead>
  <tbody>
    <tr>
      <td><strong>Yahoo News</strong> — "boyfriend arrested in Tikku murder"</td>
      <td>Headline is factually misleading: fuses two unrelated cases. Clean chit (2010) + no conviction in either matter + 14+ years old.</td>
    </tr>
    <tr>
      <td><strong>Business Standard</strong> — "Court rejects bail"</td>
      <td>Reports only the sessions court rejection, not the subsequent HC bail grant. Incomplete and misleading final picture. No conviction.</td>
    </tr>
    <tr>
      <td><strong>DNA India</strong> — "HC grants bail to stock broker Gautam Vora (Tikku)"</td>
      <td>Headline associates your name directly with a murder case. You were not accused of murder. HC granted bail. No conviction.</td>
    </tr>
  </tbody>
</table>
<p>We will file these via Google's "Results about you" tool. <strong>If you can share a court document (any order), it makes these substantially stronger.</strong></p>

<h2>Your personal website — ready to deploy</h2>
<p>We have built a clean, SEO-optimised personal website for you. It is ready to go live the moment
you register <strong>gautamvora.com</strong> (or we can do that for you). The site includes:</p>
<ul>
  <li>SEO-optimised title: <em>Gautam Vora — Equity Analyst &amp; Stockbroker, Mumbai</em></li>
  <li>Schema.org Person markup so Google correctly identifies you as a finance professional</li>
  <li>About section (placeholder — will update with your bio and headshot)</li>
  <li>Commentary section ready for regular articles</li>
  <li>Mobile-responsive, fast-loading design</li>
</ul>
<p>The site will typically appear on page 1 within 4–8 weeks of launch. It is the single most
important suppression asset we can deploy.</p>

<h2>Timeline</h2>
<table>
  <thead><tr><th>Milestone</th><th>Horizon</th><th>Needs your input?</th></tr></thead>
  <tbody>
    <tr><td>Website placeholder live</td><td>Day 1–3</td><td>Domain registration confirmation</td></tr>
    <tr><td>Google removal requests filed</td><td>This week</td><td>Optional: court doc</td></tr>
    <tr><td>Wikipedia &amp; Grokipedia corrections submitted</td><td>This week</td><td>Your go-ahead</td></tr>
    <tr><td>LinkedIn profile live</td><td>Week 1</td><td>Career timeline</td></tr>
    <tr><td>Full website with bio + first article</td><td>Week 2</td><td>Bio + headshot</td></tr>
    <tr><td>Market commentary — 3 seed articles published</td><td>Week 2–4</td><td>Your review/approval</td></tr>
    <tr><td>De-indexing petition filed (if discharge confirmed)</td><td>2–8 weeks</td><td>Court document</td></tr>
    <tr><td>30-day SERP check</td><td>Day 30</td><td>—</td></tr>
    <tr><td>Full 90-day assessment</td><td>Day 90</td><td>—</td></tr>
  </tbody>
</table>

<p>Please reply with the three critical items and we will move immediately. The attached report
has the full background analysis, source inventory, and strategy rationale.</p>

<p>
  <span class="sig">Press Detective</span><br>
  <a href="mailto:info@pressdetective.com" style="color:#1F4E79">info@pressdetective.com</a>
</p>

<div class="footer">
  Confidential — prepared for Gautam Vora only. This is a strategic plan, not legal advice.
  Removal of court and news records in India may require qualified legal counsel.
</div>
</div></body></html>
"""

def send():
    msg = MIMEMultipart("mixed")
    msg["Subject"] = SUBJECT
    msg["From"]    = f"{cfg.FROM_NAME} <{cfg.FROM_ADDR}>"
    msg["To"]      = cfg.TO_ADDR
    if cfg.CC_ALWAYS:
        msg["Cc"] = ", ".join(cfg.CC_ALWAYS)

    msg.attach(MIMEText(HTML, "html", "utf-8"))

    docx_path = os.path.join(DIR, "Gautam_Vora_Reputation_Audit.docx")
    if os.path.exists(docx_path):
        with open(docx_path, "rb") as f:
            part = MIMEBase("application",
                            "vnd.openxmlformats-officedocument.wordprocessingml.document")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                            'attachment; filename="Gautam_Vora_Reputation_Audit.docx"')
            msg.attach(part)
        print("  DOCX attached")
    else:
        print("  WARNING: DOCX not found, sending without attachment")

    recipients = [cfg.TO_ADDR] + (cfg.CC_ALWAYS or [])
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(cfg.SMTP_HOST, cfg.SMTP_PORT, context=ctx) as s:
        s.login(cfg.USERNAME, cfg.PASSWORD)
        s.sendmail(cfg.FROM_ADDR, recipients, msg.as_bytes())
    print(f"Sent to {cfg.TO_ADDR}" + (f", CC: {', '.join(cfg.CC_ALWAYS)}" if cfg.CC_ALWAYS else ""))

if __name__ == "__main__":
    send()
