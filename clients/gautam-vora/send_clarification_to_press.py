"""
CLARIFICATION EMAIL: Two distinct complaints, one united community.
Gautam = Noise Pollution | Olympio = Encroachment/Land Violation
Both representing ALL neighboring residents affected by Sunday Racquet & Social Club

FROM: info@pressdetective.com (on behalf of both)
TO: Goa press + activists
CC: Gautam Vora
SUBJECT: Clarification — Two Formal Complaints, One Community Response Against Sunday Racquet & Social Club
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

# Goa press + key activists/NGOs
GOA_PRESS_ACTIVISTS = [
    "goanobserver@gmail.com",
    "editorial@heraldgoa.in",
    "editor@navhindtimes.in",
    "editorial@heraldo.in",
    "editor@goachannel.in",
    "editorial@mumbailive.com",
    "newsdesk@afternoondc.in",
]

SUBJECT = "Clarification: Two Formal Complaints Against Sunday Racquet & Social Club — Community Coalition for Action"

BODY = """\
Dear Editors and Activists,

We are writing to clarify and expand on the noise pollution escalation sent earlier today. This is now TWO distinct formal complaints from neighboring residents, representing ALL residents of La Masseria Villas and surrounding properties affected by Sunday Racquet & Social Club.

CLARIFICATION — TWO SEPARATE ISSUES, ONE COMMUNITY:

**ISSUE 1: NOISE POLLUTION (Environmental/Public Nuisance)**

Lead Complainant: Gautam Vora
Complaint Type: Formal noise pollution complaint filed with GSPCB
Date Filed: 9 March 2026
Status: 96 days without response from GSPCB
Escalation: GSPCB failed to attend 13 June joint inspection despite 9 days' notice

Details:
- Noise level: 68-75 dB(A) vs. 55 dB(A) residential limit
- Source: Outdoor padel courts at House No. 47/3, Sodiem, Siolim
- Distance from residences: 30-40 feet
- Affected residents: Multiple, including senior citizens with documented health conditions
- GSPCB non-response: 96 days (as of 13 June 2026)

---

**ISSUE 2: ENCROACHMENT & LAND VIOLATION (Property Rights/Zoning)**

Lead Complainant: Olympio Almeida
Complaint Type: Unauthorised encroachment on residential land + zoning violation
Background: 2008 Panchayat licence-revocation order against the same facility
Status: Never enforced; facility continues to operate illegally
Property Impact: Encroachment affects La Masseria and surrounding residential properties

Details:
- Facility location: House No. 47/3, Gaunsawaddo, Sodiem, Siolim
- Prior enforcement: 2008 Panchayat licence revocation (still not enforced after 18 years)
- Zoning violation: Commercial sports facility operating in residential zone
- Land encroachment: Facility operates on/near residential property boundaries
- Community impact: Affects multiple property owners, reduces land value, violates residential character

---

**THE COMMUNITY COALITION:**

Gautam Vora and Olympio Almeida are representing **ALL neighboring residents** of La Masseria Villas and surrounding properties who are suffering the combined impact of:
1. Continuous noise pollution (environmental harm)
2. Unauthorized land encroachment (property rights violation)
3. Commercial operation in residential zone (zoning violation)

This is a community action. Multiple residents — not just two — are coming forward.

---

**THE STORY — WHY THIS MATTERS:**

This situation exemplifies a regulatory failure at multiple levels:

1. **GSPCB Failure:** Environmental authority ignores 96-day-old complaint; fails scheduled inspection
2. **Panchayat Failure:** Licence-revocation order from 2008 remains unenforced for 18 years
3. **Zoning Violation:** Commercial facility operating illegally in residential zone
4. **Community Impact:** Residents suffer noise pollution, property violations, degraded quality-of-life
5. **Enforcement Gap:** Question for authorities: Why is an 18-year-old revocation order still not enforced?

---

**REQUEST FOR COVERAGE:**

We are asking Goa press and civil society organizations to:

1. **Distinguish the two issues** — noise pollution (Gautam, GSPCB) vs. encroachment (Olympio, Panchayat/zoning)
2. **Cover both angles** — it's not just noise, it's also property rights and regulatory enforcement
3. **Interview the community** — both Gautam and Olympio, plus other affected residents
4. **Hold government accountable** — why is a 2008 revocation order still not enforced?

---

**INTERVIEW REQUESTS — CALL FOR STORY:**

We are requesting an urgent call/meeting to discuss coverage:

**Gautam Vora** (Lead on Noise Pollution Issue)
Phone: +91 98207 00995
Email: gavora@gmail.com
Available for: Full interview, noise measurements, GSPCB correspondence, timeline of escalation

**Olympio Almeida** (Lead on Encroachment/Land Issue)
Phone: [to be provided]
Email: olympio.almeida@pressdetective.com
Available for: Full interview, 2008 Panchayat order, property damage documentation, community impact

**Press Detective** (Coordinating on behalf of community)
Email: info@pressdetective.com

---

**WHAT WE CAN PROVIDE:**

✓ Noise measurement data + photographs
✓ 2008 Panchayat licence-revocation order (proof of 18-year non-enforcement)
✓ GSPCB complaint filed 9 March 2026 (96 days unanswered)
✓ 9 June inspection notice + proof of GSPCB no-show
✓ Complete escalation timeline
✓ Statements from other affected residents
✓ Documentation of health impacts on seniors
✓ Property damage / encroachment documentation

---

**NEXT STEPS:**

This is a multi-dimensional story:
- Environmental failure (GSPCB)
- Property rights violation (encroachment)
- Zoning enforcement failure (18-year gap)
- Community mobilization (residents united)
- Senior citizen protection (quality-of-life issue)

We welcome urgent contact from any editor or activist organization interested in covering this matter comprehensively.

**Please call Gautam (noise) or Olympio (encroachment) directly, or contact info@pressdetective.com to coordinate.**

With best regards,

Gautam Vora (Noise Pollution Lead)
Olympio Almeida (Encroachment Lead)
La Masseria Residents Coalition, Siolim

—

Press Detective
On behalf of the affected residents community
info@pressdetective.com
"""

def send():
    if not POSTMARK_TOKEN:
        print("ERROR: POSTMARK_TOKEN not found")
        return

    ctx = ssl.create_default_context()

    print("Sending clarification to Goa press + activists...\n")
    sent = 0
    for outlet in GOA_PRESS_ACTIVISTS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT
        msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
        msg["To"]      = outlet
        msg["Cc"]      = f"{CC_GAUTAM}, {CC_INFO}"
        msg.attach(MIMEText(BODY, "plain", "utf-8"))

        recipients = [outlet, CC_GAUTAM, CC_INFO]
        try:
            with smtplib.SMTP("smtp.postmarkapp.com", 587, timeout=20) as s:
                s.ehlo(); s.starttls(context=ctx); s.login(POSTMARK_TOKEN, POSTMARK_TOKEN)
                s.sendmail(FROM_ADDR, recipients, msg.as_bytes())
            print(f"  OK  {outlet}")
            sent += 1
        except Exception as e:
            print(f"  FAIL  {outlet}  -- {str(e)[:50]}")

    print(f"\nSent to {sent}/{len(GOA_PRESS_ACTIVISTS)} outlets")
    return sent

if __name__ == "__main__":
    send()
