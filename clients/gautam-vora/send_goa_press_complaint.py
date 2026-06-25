"""
Send Gautam Vora's padel court complaint to all Goa press.
Introduces him as expert + affected resident fighting for quality-of-life.
FROM: info@pressdetective.com via Postmark
CC: gavora@gmail.com, info@pressdetective.com
Date: 13 June 2026
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

# Goa press contacts
GOA_PRESS = [
    "goanobserver@gmail.com",
    "editorial@heraldgoa.in",
    "editor@navhindtimes.in",
    "editorial@heraldo.in",
    "editor@goachannel.in",
    "editorial@mumbailive.com",  # Mumbai but covers Goa
    "newsdesk@afternoondc.in",   # North Goa
]

SUBJECT = "A Mumbai Expert Speaks: Padel Court Noise Pollution in Goa — Quality-of-Life Crisis | Gautam Vora"

BODY = """\
Dear Editor,

I am writing to bring an important quality-of-life issue to your attention — one that I believe merits coverage in the interest of your readers and the broader residents of Goa.

I am Gautam Vora, a Mumbai-based equity analyst and stockbroker with 25 years' experience in Indian capital markets. I am also a resident and villa owner at La Masseria Villas, Siolim, Goa.

In this role as a resident, I am writing to call attention to a significant noise pollution and public nuisance issue affecting our community, which I believe raises broader questions about quality-of-life, environmental protection, and the enforcement of Goa's noise-pollution regulations.

BACKGROUND: THE ISSUE

An outdoor padel sports facility known as "Sunday Racquet and Social Club" is located at House No. 47/3, Gaunsawaddo, Sodiem, Siolim — approximately 30-40 feet from residential properties including my own villa.

Since the courts became operational, residents have experienced:
- Continuous paddle-ball impact noise (measured at 68-75 dB(A) vs. 55 dB(A) residential limit)
- Shouting, loud conversations, and music throughout operating hours
- Disturbance extending into late evening and weekend hours

Critically, several of the affected residents are senior citizens aged 60+, many with documented health conditions (cardiac issues, diabetes, etc.) who purchased these homes expecting a quiet residential setting.

THE RECORD:

1. **2008 Panchayat Order:** The Village Panchayat of Siolim-Sodiem issued a licence-revocation order against the same facility — for unauthorised construction on the same plot — an order that has never been enforced in 18 years.

2. **March 2026 GSPCB Complaint:** I filed a formal complaint with the Goa State Pollution Control Board. As of today (13 June), this remains unaddressed after 96 days.

3. **June 2026 Site Inspection:** The Panchayat scheduled a formal joint inspection with the GSPCB to verify the facts. The GSPCB failed to attend despite 9 days' advance notice.

4. **Police Response:** The Superintendent of Police, Panaji (SPCR), responded and forwarded the matter for action.

5. **MLA Non-Response:** Repeated appeals to the Siolim MLA remain unanswered.

WHY THIS MATTERS

This is not about opposition to sport. It concerns the placement of outdoor sports facilities generating repetitive noise in extremely close proximity to residential properties — a matter that requires planning oversight, noise-mitigation standards, and protection of residential amenity.

Internationally, similar issues involving padel and pickleball courts have prompted planning reviews, noise investigations, and in some cases, relocation of facilities.

As these sports continue to grow in popularity, Goa will likely face these questions more often:
- What setback distances should be required from residences?
- What acoustic mitigation standards apply?
- How do we protect senior citizens and vulnerable residents?
- What is the balance between recreational development and residential rights?

THE ASK

I believe this issue deserves public attention and policy discussion. It affects the residents of Siolim today and may affect many communities across Goa in the years ahead.

I am available for interview and can provide:
- Noise measurement data and photographs
- The complete 2008 Panchayat order
- The GSPCB complaint and correspondence
- Details of the June inspection and GSPCB non-attendance
- Full timeline of escalation attempts

I welcome coverage of this matter and would be pleased to speak to your publication.

Contact:
Gautam Vora
+91 98207 00995
gavora@gmail.com

Respectfully,
Gautam Vora
Mumbai, India
"""

def send():
    if not POSTMARK_TOKEN:
        print("ERROR: POSTMARK_TOKEN not found in .creds/proton_accounts.json")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["Cc"]      = f"{CC_GAUTAM}, {CC_INFO}"
    msg.attach(MIMEText(BODY, "plain", "utf-8"))

    ctx = ssl.create_default_context()
    sent_count = 0
    failed = []

    for outlet in GOA_PRESS:
        msg["To"] = outlet
        recipients = [outlet, CC_GAUTAM, CC_INFO]
        try:
            with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
                s.ehlo(); s.starttls(context=ctx); s.login(POSTMARK_TOKEN, POSTMARK_TOKEN)
                s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
            print(f"  OK  {outlet}")
            sent_count += 1
        except Exception as e:
            print(f"  FAIL  {outlet}  -- {str(e)[:50]}")
            failed.append(outlet)

    print(f"\nSent to {sent_count}/{len(GOA_PRESS)} outlets")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    return sent_count, failed

if __name__ == "__main__":
    print("Sending Gautam Vora padel court complaint to Goa press...\n")
    send()
