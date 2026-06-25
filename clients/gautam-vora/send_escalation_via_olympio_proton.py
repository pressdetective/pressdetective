"""
GSPCB No-Show Escalation via Olympio Almeida (Proton Bridge).
FROM: olympio.almeida@pressdetective.com
TO: Goa press + police
VIA: Proton Bridge (127.0.0.1:1025, STARTTLS)
CC: Gautam + info@pressdetective.com

Frames as: two neighbors (Olympio + Gautam) coming together against GSPCB inaction.
"""
import json, smtplib, ssl, getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida & Gautam Vora"
PROTON_PASSWORD = CREDS.get("accounts", {}).get("olympio", {}).get("bridge_password", "")

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

SUBJECT_PRESS = "URGENT: GSPCB Fails to Attend Padel Court Inspection — Siolim Community Demands Accountability"

SUBJECT_POLICE = "Urgent Escalation — GSPCB No-Show + Community Response (Olympio Almeida & Gautam Vora, Siolim)"

BODY_PRESS = """\
Dear Editor,

Two residents of La Masseria Villas, Siolim — Olympio Almeida and Gautam Vora — are writing to escalate a serious enforcement failure affecting our entire community.

On 13 June 2026, the Village Panchayat of Siolim-Sodiem scheduled a formal joint site inspection with the Goa State Pollution Control Board (GSPCB) to investigate noise pollution from "Sunday Racquet and Social Club" padel courts at House No. 47/3, Gaunsawaddo, Sodiem, Siolim.

The Panchayat provided 9 days' advance notice. The inspection was set for 11:30 AM.

**The GSPCB did not attend.**

THE COMMUNITY ISSUE:

Multiple residents — including senior citizens with documented health conditions — are experiencing continuous noise pollution (68-75 dB(A) vs. 55 dB(A) residential limit) from padel courts located 30-40 feet from our homes.

THE ENFORCEMENT FAILURE:

1. **March 2026:** Formal GSPCB complaint filed (Gautam Vora)
   Status: 96 days without response

2. **June 2026:** Village Panchayat schedules joint inspection
   Status: GSPCB fails to attend despite notice

3. **2008 Background:** Panchayat issued licence-revocation order against the same facility
   Status: Never enforced in 18 years

THE QUESTION:

Is the GSPCB unable or unwilling to enforce Goa's noise-pollution regulations?

OUR REQUEST:

We welcome coverage of this matter. It is not about opposition to sport — it is about:
- Planning standards and residential protection
- Government enforcement of environmental law
- Community quality-of-life and protection of vulnerable residents

COMMUNITY CONTACTS:

**Olympio Almeida** (La Masseria, Siolim)
Phone: +91 [to be provided by Olympio]
Email: olympio.almeida@pressdetective.com

**Gautam Vora** (La Masseria, Siolim)
Phone: +91 98207 00995
Email: gavora@gmail.com

Both are available for extensive interview and will provide:
- Noise measurement data and photographs
- 2008 Panchayat licence-revocation order
- GSPCB complaint (96-day unanswered record)
- 9 June inspection notice + proof of GSPCB no-show
- Complete timeline of escalation attempts
- Other resident statements

We look forward to coverage that holds government accountable.

With best regards,

Olympio Almeida
Gautam Vora
Siolim Residents
olympio.almeida@pressdetective.com
"""

BODY_POLICE = """\
Subject: Urgent Escalation — GSPCB No-Show + Community Response (Olympio Almeida & Gautam Vora, Siolim)

Dear SP (SPCR) / Police Leadership,

Two residents of La Masseria Villas, Siolim — Olympio Almeida and Gautam Vora — are formally escalating a noise pollution and enforcement failure matter.

BACKGROUND:

Formal GSPCB complaint filed: 9 March 2026 (Gautam Vora)
Status: 96 days without response

Village Panchayat joint inspection scheduled: 13 June 2026, 11:30 AM (9 days' notice given to GSPCB)
Status: GSPCB failed to attend

FACTS:

- Noise level: 68-75 dB(A) vs. 55 dB(A) residential limit
- Source: "Sunday Racquet and Social Club" (House No. 47/3, Sodiem, Siolim)
- Distance from residences: 30-40 feet
- Affected residents: Multiple, including senior citizens with health conditions
- Prior enforcement: 2008 Panchayat licence-revocation order (still unenforced after 18 years)

ESCALATION:

This matter has now been escalated to Goa press and media. Community residents are coming forward with public statements of the enforcement failure and GSPCB inaction.

REQUEST:

1. Verify GSPCB non-attendance on 13 June inspection
2. Investigate why GSPCB failed to attend despite notice
3. Direct enforcement action on the facility if violations confirmed
4. Coordinate with GSPCB on status of 96-day-old complaint

RESIDENT CONTACTS:

Olympio Almeida
Phone: +91 [provided by Olympio]
Email: olympio.almeida@pressdetective.com

Gautam Vora
Phone: +91 98207 00995
Email: gavora@gmail.com

Both available for follow-up communication.

Respectfully submitted,

Olympio Almeida
Gautam Vora
La Masseria Villas, Siolim, Goa
"""

def send():
    if not PROTON_PASSWORD:
        print("ERROR: Proton bridge_password not in .creds/proton_accounts.json")
        return

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Send to Goa press
    print("Sending escalation FROM Olympio to Goa press via Proton Bridge...\n")
    sent_press = 0
    for outlet in GOA_PRESS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT_PRESS
        msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
        msg["To"]      = outlet
        msg["Cc"]      = f"{CC_GAUTAM}, {CC_INFO}"
        msg.attach(MIMEText(BODY_PRESS, "plain", "utf-8"))

        recipients = [outlet, CC_GAUTAM, CC_INFO]
        try:
            with smtplib.SMTP("127.0.0.1", 1025, timeout=20) as s:
                s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, PROTON_PASSWORD)
                s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
            print(f"  OK  {outlet}")
            sent_press += 1
        except Exception as e:
            print(f"  FAIL  {outlet}  -- {str(e)[:60]}")

    print(f"\nPress: {sent_press}/{len(GOA_PRESS)} sent")

    # Send to police
    print("\nSending escalation FROM Olympio to Goa police via Proton Bridge...\n")
    sent_police = 0
    for police_addr in GOA_POLICE:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT_POLICE
        msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
        msg["To"]      = police_addr
        msg["Cc"]      = CC_INFO
        msg.attach(MIMEText(BODY_POLICE, "plain", "utf-8"))

        recipients = [police_addr, CC_INFO]
        try:
            with smtplib.SMTP("127.0.0.1", 1025, timeout=20) as s:
                s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, PROTON_PASSWORD)
                s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
            print(f"  OK  {police_addr}")
            sent_police += 1
        except Exception as e:
            print(f"  FAIL  {police_addr}  -- {str(e)[:60]}")

    print(f"\nPolice: {sent_police}/{len(GOA_POLICE)} sent")
    return sent_press, sent_police

if __name__ == "__main__":
    print("Sending escalation FROM Olympio Almeida via Proton Bridge...\n")
    send()
