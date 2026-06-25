"""
ESCALATION: GSPCB No-Show on Joint Inspection — Full Community Response.
Send to Goa press + police after inspection failure on 13 June 2026.
Frames as: residents united, government inaction, enforcement failure.
FROM: info@pressdetective.com via Postmark
CC: gavora@gmail.com, info@pressdetective.com
"""
import json, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

FROM_ADDR = "info@pressdetective.com"
FROM_NAME = "Press Detective"
POSTMARK_TOKEN = CREDS.get("smtp_postmark", {}).get("token", "")

CC_GAUTAM = "gavora@gmail.com"
CC_INFO = "info@pressdetective.com"

# Goa press + police
GOA_PRESS = [
    "goanobserver@gmail.com",
    "editorial@heraldgoa.in",
    "editor@navhindtimes.in",
    "editorial@heraldo.in",
    "editor@goachannel.in",
    "editorial@mumbailive.com",
    "newsdesk@afternoondc.in",
]

GOA_POLICE = [
    "igpgoa@goapolice.gov.in",
    "complaint@goapolice.gov.in",
]

SUBJECT = "URGENT: GSPCB Fails to Attend Joint Inspection — Community Residents Demand Accountability | Gautam Vora, Siolim"

BODY_PRESS = """\
Dear Editor,

BREAKING: The Goa State Pollution Control Board (GSPCB) failed to attend a formally scheduled joint site inspection on padel court noise pollution in Siolim on 13 June 2026 — despite nine days' advance notice.

This is an escalation and public accountability issue affecting residents across the community.

THE FACTS:

On 13 June 2026, the Village Panchayat of Siolim-Sodiem scheduled a formal joint inspection with the GSPCB to investigate noise pollution complaints from the "Sunday Racquet and Social Club" padel courts at House No. 47/3, Gaunsawaddo, Sodiem, Siolim.

The Panchayat provided 9 days' advance notice. The inspection was scheduled for 11:30 AM.

**The GSPCB did not attend.**

CONTEXT — THE COMPLAINT:

Multiple residents, including senior citizens with documented health conditions, have filed formal complaints about continuous noise pollution (68-75 dB(A) vs. 55 dB(A) residential limit) from the padel courts, which are located 30-40 feet from residential properties.

**Lead complainant:** Gautam Vora, a Mumbai-based equity analyst and resident of La Masseria Villas, Siolim. Contact: +91 98207 00995 / gavora@gmail.com

Formal complaint filed with GSPCB: 9 March 2026
No response to date: 96 days

THE ESCALATION:

1. **2008 Panchayat licence-revocation order** against the same facility — never enforced in 18 years.
2. **GSPCB formal complaint** — ignored for 96 days.
3. **Village Panchayat joint inspection** — GSPCB fails to attend despite notice.
4. **Police escalation** — SP (SPCR) Panaji has forwarded the matter for action.
5. **Community response** — Multiple residents now united in demanding action.

THE QUESTION:

Is the GSPCB unable or unwilling to enforce Goa's noise-pollution regulations? Why was a formally scheduled inspection failed?

THE COMMUNITY:

Residents across La Masseria and surrounding properties have come together on this issue. This is not a single complaint — it is a community action against a facility that is operating in violation of:
- The 2008 Panchayat licence-revocation order
- Goa's noise-pollution standards (MoEFCC guidelines)
- Residential planning protocols

Senior citizens are affected. Quality-of-life is at stake. Government accountability is needed.

FOR INTERVIEW:

Gautam Vora is available for extensive interview and can provide:
- Noise measurement data and photographs
- 2008 Panchayat order (proof of prior revocation)
- GSPCB complaint and 96-day correspondence gap
- Documentation of 9 June inspection notice and 13 June GSPCB no-show
- Timeline of escalation attempts
- Community resident list (additional complainants available for interview)

Contact: +91 98207 00995 | gavora@gmail.com

This is a story about enforcement failure, community solidarity, and the question of whether Goa's pollution-control board actually enforces its own regulations.

We welcome coverage.

Press Detective
info@pressdetective.com
"""

BODY_POLICE = """\
Subject: Urgent Escalation — GSPCB Joint Inspection No-Show on Padel Court Noise Complaint (13 June 2026)

Dear SP (SPCR) / Police Leadership,

Formal escalation and status report on the noise pollution complaint referenced to your office by the Village Panchayat of Siolim-Sodiem.

BACKGROUND:

On 9 March 2026, resident Gautam Vora filed a formal noise pollution complaint with the GSPCB regarding continuous noise from "Sunday Racquet and Social Club" padel courts at House No. 47/3, Sodiem, Siolim.

Facts:
- Noise level: 68-75 dB(A) vs. 55 dB(A) residential limit
- Affected residents: Multiple, including senior citizens with documented health conditions
- Distance from residences: 30-40 feet
- 2008 background: Panchayat issued licence-revocation order against the same facility (never enforced)

ESCALATION:

Status as of 13 June 2026:
- GSPCB complaint: 96 days without response
- GSPCB joint inspection: Scheduled by Panchayat for 13 June, 11:30 AM, with 9 days' notice
- **GSPCB attendance: FAILED to attend**
- Police escalation: Forwarded to your office for action

CURRENT STATUS:

The Village Panchayat has conducted the joint inspection without GSPCB participation, leaving the matter unresolved. The community is now escalating through media and public channels.

RESIDENT CONTACT:

Gautam Vora
Phone: +91 98207 00995
Email: gavora@gmail.com
Address: La Masseria Villas, Survey No. 197/A, Sodiem, Siolim, Goa

REQUEST FOR ACTION:

1. Verify GSPCB non-attendance on 13 June inspection
2. Investigate why GSPCB failed to attend despite notice
3. Direct enforcement action against the facility if violations are confirmed
4. Coordinate with GSPCB to determine status of the 96-day-old complaint

This matter is now in public domain and may receive media coverage.

Respectfully submitted,
Press Detective
On behalf of Gautam Vora and affected residents
info@pressdetective.com
"""

def send():
    if not POSTMARK_TOKEN:
        print("ERROR: POSTMARK_TOKEN not found")
        return

    ctx = ssl.create_default_context()

    # Send to Goa press
    print("Sending escalation to Goa press...\n")
    sent_press = 0
    for outlet in GOA_PRESS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT
        msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
        msg["To"]      = outlet
        msg["Cc"]      = f"{CC_GAUTAM}, {CC_INFO}"
        msg.attach(MIMEText(BODY_PRESS, "plain", "utf-8"))

        recipients = [outlet, CC_GAUTAM, CC_INFO]
        try:
            with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
                s.ehlo(); s.starttls(context=ctx); s.login(POSTMARK_TOKEN, POSTMARK_TOKEN)
                s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
            print(f"  OK  {outlet}")
            sent_press += 1
        except Exception as e:
            print(f"  FAIL  {outlet}  -- {str(e)[:50]}")

    print(f"\nPress: {sent_press}/{len(GOA_PRESS)} sent")

    # Send to police
    print("\nSending escalation to Goa police...\n")
    sent_police = 0
    for police_addr in GOA_POLICE:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Urgent Escalation — GSPCB No-Show on Padel Court Inspection (Gautam Vora, Siolim)"
        msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
        msg["To"]      = police_addr
        msg["Cc"]      = CC_INFO
        msg.attach(MIMEText(BODY_POLICE, "plain", "utf-8"))

        recipients = [police_addr, CC_INFO]
        try:
            with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
                s.ehlo(); s.starttls(context=ctx); s.login(POSTMARK_TOKEN, POSTMARK_TOKEN)
                s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
            print(f"  OK  {police_addr}")
            sent_police += 1
        except Exception as e:
            print(f"  FAIL  {police_addr}  -- {str(e)[:50]}")

    print(f"\nPolice: {sent_police}/{len(GOA_POLICE)} sent")
    return sent_press, sent_police

if __name__ == "__main__":
    send()
