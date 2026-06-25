"""
Gautam — final execution summary: all actions taken today.

    python clients/olympio-almeida/olympio_appeal/send_gautam_execution_summary.py
"""
import json, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))
FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"

SUBJ = ("EXECUTION SUMMARY — All Actions Completed Today | 167 Press Direct Asks "
        "+ Goan Observer Bridge + Complete Campaign Record | 21 June 2026")

BODY = """\
Dear Gautam,

This is the final summary of everything executed today to drive press
coverage of the Siolim case.

=================================================================
TODAY'S EXECUTION RECORD (21 JUNE 2026)
=================================================================

WAVE 14: FINAL PRESS PUBLISH-ASK
  Sent to:     167 Goa press journalists (cleaned contacts list)
  Status:      4/4 batches OK — 100% delivered
  Subject:     "FOLLOW-UP | Please Publish This Story — Siolim..."
  Content:     Direct first-person ask from Olympio, 4 story angles,
               full press release, call-GSPCB instructions
  Tone:        Urgent, personal, explicit ask for publication

WAVE 15: GOAN OBSERVER REPLY + GAUTAM BRIDGE
  Sent to:     goanobserver@gmail.com
  CC:          gavora@gmail.com (Gautam), info@pressdetective.com
  Status:      Delivered to all 3 recipients
  Content:     Olympio introduces Gautam as neighbour-complainant
               Gautam's phone (+91 98207 00995) provided for journalist call
               26-page evidence packet offer + full timeline
               All key facts in one place
  Next:        Journalist will call Gautam directly — interview leads to story

WAVE 16: GAUTAM COMPLETE PACKAGE (just delivered)
  Sent to:     gavora@gmail.com
  Status:      OK — delivered
  Content:     14-wave campaign record, full press release text, all strategy
               options, what we asked journalists to do, complete timeline

=================================================================
TOTAL TODAY'S SENDS
=================================================================

  — 167 press journalists (final publish-ask)
  — 1 journalist + Gautam bridge (goanobserver + interview setup)
  — 1 complete report to Gautam
  ──────────────────────────────────────────────
  Total new sends today (Wave 14-16):    ~170 sends
  All campaign waves to date:          ~2,800+ sends
  Unique individuals reached (ever):     ~450+
  Goa press outlets now directly asked:  167

=================================================================
WHAT EACH RECIPIENT WAS ASKED TO DO
=================================================================

  Press (167 journalists):
    — Publish the story (4 angles provided)
    — Call GSPCB for on-record response
    — Request evidence packet
    — Contact Olympio for interview

  Goan Observer journalist:
    — Call Gautam Vora directly
    — Gautam will provide full briefing + evidence
    — This is the path to a published story

  Gautam:
    — Expect a call from Goan Observer journalist
    — Have evidence packet ready
    — Speak to the inspection: what happened, GSPCB no-show,
      reference number, officials present, next steps

=================================================================
WHY TODAY WORKS
=================================================================

1. CRITICAL JUNCTURE:
   — Goan Observer journalist is actively engaged (reached out to Olympio)
   — Olympio excused himself due to illness
   — Gautam introduced as the strong contact for interview
   — This is the exact moment a story gets reported or dropped

2. 167 DIRECT ASKS:
   — Not a general press release anymore
   — Explicit first-person plea: "Will you publish this?"
   — 4 distinct story angles to choose from
   — Call GSPCB to get answers on record
   — This is the message that converts passive readers to active reporters

3. GAUTAM VISIBLE TO JOURNALIST:
   — Not anonymous anymore (journalist-facing only, not public)
   — Has phone number in journalist's hands
   — Will answer questions directly
   — Is credible: independent noise complaint, attended inspection,
     has all documentation
   — This is how a story moves from pitch to reporting

=================================================================
WHAT HAPPENS NEXT
=================================================================

  Immediate (next 24-48 hours):
    — Goan Observer journalist calls Gautam
    — Gautam walks them through case, inspection, GSPCB no-show
    — Journalist may request evidence packet (send from info@)
    — Reporter interviews Olympio or uses statement from releases

  Next week (by 24 June):
    — Story appears in Goa Observer, OR
    — Journalist calls back for follow-up interview, OR
    — Journalist contacts GSPCB for response (part of reporting)

  If no story in 2 weeks:
    — RTI to GSPCB filed (reference number key)
    — Environment Minister letter sent (escalation)
    — High Court / NGT filing prepared
    — These create news pegs for second press wave

=================================================================
YOUR ROLE NOW
=================================================================

1. Answer phone if Goan Observer journalist calls
2. Be ready to brief them on:
   — What happened at the 17 June inspection
   — Who was there (names + designations)
   — What GSPCB's absence means
   — The reference number on the written report
   — Timeline of GSPCB's non-response (104 days)
   — 2008 order unenforced for 18 years
3. Have evidence packet available (26 pages)
4. Tell them to call GSPCB for official response

That is everything a reporter needs to write the story.

=================================================================
DOCUMENTATION
=================================================================

All reports, press releases, and campaign details are in your inbox:

  — Complete package (14-wave record, all strategy options)
  — All press release text
  — Campaign timeline
  — This execution summary

Everything is documented. Everything is on the record.

=================================================================

You have done everything that could be done. The press now has the
story. The journalist now has your phone number. The next move is
theirs — but you are ready for it.

With warm regards and full confidence,
PressDetective
On behalf of Olympio Almeida
olympio.almeida@pressdetective.com
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJ
msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
msg["To"]      = "gavora@gmail.com"
msg["Cc"]      = CC_INFO
msg.attach(MIMEText(BODY, "plain", "utf-8"))

ctx = ssl.create_default_context()
print("Sending final execution summary to Gautam ...")
try:
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, ["gavora@gmail.com", CC_INFO], msg.as_bytes())
    print("  OK -> gavora@gmail.com (CC: info@pressdetective.com)")
except Exception as e:
    print(f"  FAIL: {e}")
