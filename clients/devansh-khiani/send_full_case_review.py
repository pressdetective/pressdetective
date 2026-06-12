#!/usr/bin/env python3
"""
Send Devansh Khiani — Full Case Review + Solutions
From: santosh@pressdetective.com
To:   devansh@valsonprints.com, devansh.khiani@gmail.com, dev@varuntextiles.com
CC:   info@pressdetective.com
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.mailer import build_msg, send_mail

FROM_ADDR = "santosh@pressdetective.com"
FROM_NAME = "Santosh | Press Detective"
TO_ADDRS  = [
    "devansh@valsonprints.com",
    "devansh.khiani@gmail.com",
    "dev@varuntextiles.com",
]
CC        = "info@pressdetective.com"
SUBJECT   = "Devansh — we have reviewed all your cases. Here is where things stand. | Press Detective"

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
  .sub { color: #595959; font-size: 13px; margin-bottom: 28px; }
  p { line-height: 1.7; margin: 0 0 12px; }
  ul, ol { padding-left: 22px; }
  li { margin-bottom: 8px; line-height: 1.65; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0 20px; font-size: 13px; }
  th { background: #1F4E79; color: #fff; text-align: left; padding: 8px 10px; }
  td { padding: 8px 10px; border-bottom: 1px solid #ddd; vertical-align: top; }
  tr:nth-child(even) td { background: #f5f8fb; }
  .badge { display: inline-block; padding: 2px 10px; border-radius: 10px; font-size: 11px;
           font-weight: bold; color: #fff; white-space: nowrap; }
  .red    { background: #C00000; }
  .amber  { background: #BF8F00; }
  .green  { background: #538135; }
  .blue   { background: #1F4E79; }
  .note { background: #fff8e6; border-left: 3px solid #BF8F00; padding: 12px 16px;
          font-size: 13px; color: #444; margin: 16px 0; border-radius: 2px; }
  .win  { background: #f0f7f0; border-left: 3px solid #538135; padding: 12px 16px;
          font-size: 13px; color: #333; margin: 16px 0; border-radius: 2px; }
  .footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #ddd;
            font-size: 12px; color: #888; }
  .sig-name { font-weight: bold; color: #1F4E79; font-size: 15px; }
</style>
</head>
<body>
<div class="wrap">

  <h1>Full Case Review — Devansh Khiani</h1>
  <div class="sub">Press Detective &nbsp;|&nbsp; Confidential &nbsp;|&nbsp; 12 June 2026</div>

  <p>Dear Devansh,</p>

  <p>We have run a complete search across eCourts India — all states, all levels — and pulled
  every case file associated with your name. We want you to have the full picture in one place,
  with our read on each matter and what needs to happen next.</p>

  <p><strong>The short version: the most important case is at the Bombay High Court right now,
  and it is the one that can change everything. Everything else is either closed or manageable.
  We will sort this out — but we need you to give us a few answers so we can move fast.</strong></p>

  <!-- ─── CASE MAP ─────────────────────────────────────────────────── -->
  <h2>Your cases — at a glance</h2>

  <table>
    <thead>
      <tr>
        <th>Court</th><th>CNR</th><th>Matter</th><th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Bombay High Court</strong></td>
        <td style="font-size:11px;color:#555;">HCBM010099572025</td>
        <td>Quashing of FIR 12/2025 (Malabar Hill PS)</td>
        <td><span class="badge red">PENDING — primary case</span></td>
      </tr>
      <tr>
        <td>City Sessions Court, Mumbai</td>
        <td style="font-size:11px;color:#555;">MHCC020019602025</td>
        <td>Bail Application — same FIR</td>
        <td><span class="badge green">Disposed (bail granted)</span></td>
      </tr>
      <tr>
        <td>Bombay High Court</td>
        <td style="font-size:11px;color:#555;">HCBM010134162020</td>
        <td>Family civil matter (Jyoti Metharam Khiani)</td>
        <td><span class="badge amber">Pending — separate, family</span></td>
      </tr>
      <tr>
        <td>City Civil Court, Mumbai</td>
        <td style="font-size:11px;color:#555;">MHCC010105892025</td>
        <td>Valiram Sons partnership dispute</td>
        <td><span class="badge green">Disposed Feb 2026</span></td>
      </tr>
      <tr>
        <td>Taluka Court, Gandhidham</td>
        <td style="font-size:11px;color:#555;">GJKT110118582023</td>
        <td>Succession / probate (Gujarat)</td>
        <td><span class="badge green">Disposed Apr 2025</span></td>
      </tr>
    </tbody>
  </table>

  <!-- ─── HC QUASHING ───────────────────────────────────────────────── -->
  <h2>1. Bombay High Court — Quashing Petition &nbsp;<span class="badge red">PRIORITY</span></h2>

  <p>On 17 February 2025 — just two weeks after your bail was secured — your advocate
  Adv. Jugal Kanani filed a writ petition at the Bombay High Court asking the court to
  <strong>quash FIR 12/2025 in its entirety</strong>. This is the most powerful step that
  could have been taken, and it was taken quickly. The petition is before a division bench
  (Justices Kotwal and Modak) under the category
  <em>"Criminal Quashing — FIR, Crime Against Women and Children."</em></p>

  <p>Interim orders were passed on <strong>28 February 2025</strong> and again on
  <strong>9 April 2025</strong> — this typically means the High Court gave some form of
  interim protection (a stay on arrest or trial proceedings) while the petition is heard.
  The case was listed as <em>"Due Admission"</em> as of 23 July 2025 and remains
  <strong>pending as of 9 June 2026.</strong></p>

  <div class="win">
    <strong>What this means for you:</strong> If the Bombay High Court admits and
    ultimately allows this petition, the FIR is quashed — it ceases to exist in law.
    There is no trial, no charge sheet, no conviction. From a reputation standpoint, a
    quashing order is the strongest possible outcome — it is not a "not guilty" verdict,
    it is a ruling that the case should never have been registered. That is a very
    different thing and it matters enormously for how your name is protected.
  </div>

  <p><strong>Our action:</strong> We are monitoring every hearing date on this petition.
  The moment there is an order — admission, further interim relief, or final disposal —
  we will draft the appropriate response (press statement, digital update, correction
  requests) within 24 hours.</p>

  <p><strong>What we need from you on this case (urgent):</strong></p>
  <ol>
    <li>Has the petition been <strong>formally admitted</strong> by the HC, or is it still
        at the pre-admission stage?</li>
    <li>Is there currently a <strong>stay on the trial / further investigation</strong>
        from the HC? Or only a stay on arrest?</li>
    <li>When is the <strong>next hearing date</strong>?</li>
    <li>Has there been any approach — directly or through lawyers — from the complainant's
        side regarding a settlement or withdrawal?</li>
  </ol>

  <!-- ─── BAIL / SESSIONS ────────────────────────────────────────────── -->
  <h2>2. Sessions Court Bail — Sorted &nbsp;<span class="badge green">Done</span></h2>

  <p>The bail application (MHCC020019602025) was filed on 4 February 2025 and disposed
  on 6 February 2025 — bail granted within two days. This file is closed from a
  case-management perspective. The underlying protection now runs through the
  High Court petition above.</p>

  <!-- ─── VALIRAM SONS ──────────────────────────────────────────────── -->
  <h2>3. Valiram Sons Civil Suit — Closed &nbsp;<span class="badge green">Done</span></h2>

  <p>You were named as a respondent in a civil partnership dispute involving
  M/s. Valiram Sons at the City Civil Court, Mumbai (MHCC010105892025). This matter was
  disposed on 3 February 2026 — relatively quickly for a civil suit. No action needed
  from us unless there is a pending appeal you are aware of.</p>

  <p>One question: <strong>what was the outcome?</strong> A consent order, a dismissal,
  a settlement? We ask because if there is any digital coverage of the dispute (news,
  court-reporting sites) we want to know the full correct outcome before it surfaces.</p>

  <!-- ─── GUJARAT SUCCESSION ───────────────────────────────────────── -->
  <h2>4. Gujarat Succession / Probate — Closed &nbsp;<span class="badge green">Done</span></h2>

  <p>A civil miscellaneous appeal under the Indian Succession Act 1925 (Section 278) was
  filed at the Gandhidham Taluka Court in December 2023 and disposed in April 2025. This
  appears to be a probate or letters-of-administration matter related to an estate in
  Gandhidham, Kachchh. It is fully closed.</p>

  <p>No reputational risk from this matter. No action needed unless you want us to
  confirm the specific estate detail for completeness.</p>

  <!-- ─── FAMILY HC ─────────────────────────────────────────────────── -->
  <h2>5. Bombay HC Family Matter — Separate &nbsp;<span class="badge amber">Monitor</span></h2>

  <p>There is a 2020 interlocutory application at the Bombay High Court in the names of
  family members (HCBM010134162020). This is a civil family matter — separate from the
  criminal case — and your name does not appear as a direct party. It has been before
  Hon'ble Justice Deshmukh and last had an order in April 2025. We will track it but it
  does not require urgent action from you on our side.</p>

  <!-- ─── WHAT WE NEED ──────────────────────────────────────────────── -->
  <h2>What we need from you — reply to this email</h2>

  <div class="note">
    <strong>Just reply to this email with your answers. We will take it from there.</strong>
    <ol style="margin:10px 0 0;">
      <li><strong>HC petition status</strong> — admitted or still pre-admission? Any
          stay on trial? Next hearing date?</li>
      <li><strong>Valiram Sons outcome</strong> — what was the final order?</li>
      <li><strong>Media / online</strong> — have you seen anything about yourself on
          Google, social media, news sites, or WhatsApp forwards in connection with any
          of these matters?</li>
      <li><strong>Anything else</strong> — any other matter, demand, threat, or situation
          — business or personal — where you feel you need support. Tell us. We will
          sort it out.</li>
    </ol>
  </div>

  <p>You do not need to worry about the complexity of what we have found. We have seen
  situations like this before and we know exactly what to do at each stage. The High Court
  petition is the right move and it is already in motion. Our job now is to make sure
  nothing slips through — legally, digitally, or in the press — while that process plays
  out.</p>

  <p>Write back whenever you are ready. We are here.</p>

  <p>
    <span class="sig-name">Santosh</span><br>
    Press Detective<br>
    <a href="mailto:santosh@pressdetective.com" style="color:#1F4E79;">santosh@pressdetective.com</a>
  </p>

  <div class="footer">
    Confidential — prepared for Devansh Khiani only. This is a strategic and reputational
    plan, not legal advice. All legal decisions must be taken with Adv. Jugal Kanani or
    your counsel of choice.
  </div>

</div>
</body>
</html>
"""


def send():
    to_str = ", ".join(TO_ADDRS)
    msg = build_msg(
        from_addr=f"{FROM_NAME} <{FROM_ADDR}>",
        to=to_str,
        subject=SUBJECT,
        body="Please view this email in an HTML-capable email client.",
        cc=CC,
    )
    msg.clear_content()
    msg.add_alternative(HTML, subtype="html")
    ok = send_mail(msg, account="santosh")
    if ok:
        print(f"Sent to: {to_str}")
        print(f"CC: {CC}")
    else:
        print("ERROR: all providers failed")


if __name__ == "__main__":
    send()
