"""
Gautam — feedback request after inspection + GSPCB no-show development.

    python clients/olympio-almeida/olympio_appeal/send_gautam_feedback.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
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

SUBJ = "URGENT — GSPCB No-Show at Inspection | Need Your Full Report + Feedback | What Next?"

BODY = """\
Dear Gautam,

Thank you for attending the inspection on Wednesday 17 June. We\
 understand you were there and that the Goa State Pollution Control\
 Board (GSPCB) did not attend.

This is an important development — and it changes the story. Please\
 read this in full and reply with your account of what happened.

=================================================================
WHY THE GSPCB NO-SHOW IS THE STORY NOW
=================================================================

This case began as a noise-pollution complaint. It is now a case of
regulatory failure on two separate counts:

  1. GSPCB ignored the formal March 2026 complaint for 4 months.
     No acknowledgement. No inspector. No reply.

  2. GSPCB was formally notified of Wednesday's joint inspection
     by the Village Panchayat Siolim-Sodiem (inspection notice
     VPSS/2026-27/site insp/648, dated 08 June 2026). They did
     not attend.

A statutory regulatory body was summoned to a formal government
inspection by the Panchayat, given 9 days' advance notice, and
simply did not show up.

This is a serious dereliction of duty under the Environment
Protection Act 1986 and the Noise Pollution Rules 2000 -- and it
is now a documented, verifiable fact that any journalist can
report and any RTI can confirm.

=================================================================
WE NEED YOUR FULL REPORT -- PLEASE REPLY WITH:
=================================================================

  1. Who DID attend the inspection on Wednesday?
     (Names and designations of every official present)

  2. Did the VP (Village Panchayat) representatives attend?
     Did they issue any verbal direction?

  3. Was a written inspection report / panchanama issued?
     If yes -- what is the reference number?

  4. Was a police officer present? (We had asked SP SPCR)

  5. Did any journalists come? Which outlets?

  6. Was anything said about GSPCB's absence by any official?

  7. Any other developments -- verbal commitments, obstructions,
     anything unusual?

  8. Were representatives of the club / opposite party present?

=================================================================
YOUR FEEDBACK -- WHAT SHOULD WE FOCUS ON?
=================================================================

We want your input on the next steps. Our current thinking:

  OPTION A: Press push (immediate)
  --------------------------------
  Send all 229 Goa journalists a press alert about the GSPCB
  no-show. Ask them to call GSPCB and get a response on record.
  This is investigative journalism territory -- "Why did the
  pollution board not attend its own inspection?"

  OPTION B: RTI filing (this week)
  --------------------------------
  File RTI with GSPCB demanding:
  - Confirmation they received the inspection notice
  - Name of officer assigned to the March complaint
  - Reason for non-attendance
  - Current status of the complaint
  Deadline: 30 days for response (gives us a new press peg)

  OPTION C: Escalate to High Court / NGT
  ---------------------------------------
  With GSPCB now having ignored the complaint AND the inspection,
  a Writ Petition to Bombay High Court (Goa bench) or the
  National Green Tribunal becomes much stronger. GSPCB's silence
  + no-show are documented grounds for court intervention.

  OPTION D: SP SPCR follow-up
  ----------------------------
  Follow up with cstatepolice112@gmail.com to ask: was a police
  officer sent? What action has the police taken since 16 June?

  OPTION E: MLA and Minister pressure
  ------------------------------------
  GSPCB reports to the Environment Minister of Goa. Write directly
  to the Minister with documented evidence of GSPCB's failure.
  Lobo's silence is now 12+ days -- worth naming in this letter.

We are likely doing ALL of these, but what is your instinct on
what moves first and hits hardest?

=================================================================
WHAT WENT OUT TO 229 JOURNALISTS YESTERDAY (19 June)
=================================================================

We sent a full ready-to-publish feature article ("I Can't Sit in
My Own Garden") to all 229 Goa press contacts. 6/6 batches, 100%
delivered. Subject line offered the article as "ready to publish"
with the evidence packet available on request.

We are NOW sending a second press alert about the GSPCB no-show --
with a direct ask to journalists to investigate. This goes out
immediately after this email to you.

You will receive a copy of that press alert in a separate email.

=================================================================
CAMPAIGN SUMMARY (all waves, your reference)
=================================================================

  Waves 1-11 (6-17 June):  ~2,200+ sends across all segments
  Wave 12 (19 June):        229 journalists -- feature article
  Wave 13 (today):          229 journalists -- GSPCB no-show alert
  Grand total:              ~2,600+ sends
  Unique individuals:        ~450+
  Government responses:         1  (SP SPCR, 16 June)
  MLA responses:                0  (Lobo -- 12+ days silence)
  GSPCB responses:              0  (4 months, including no-show)

=================================================================

Please reply to info@pressdetective.com with your account of the
inspection and any feedback on strategy. Everything you send us
helps us act faster and more precisely.

Your anonymity is unchanged -- you are "the complainant" in all
public material and will not be named in any press communication.

With warm regards,
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
print("Sending feedback request to Gautam ...")
try:
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, ["gavora@gmail.com", CC_INFO], msg.as_bytes())
    print("  OK -> gavora@gmail.com (CC: info@pressdetective.com)")
except Exception as e:
    print(f"  FAIL: {e}")
