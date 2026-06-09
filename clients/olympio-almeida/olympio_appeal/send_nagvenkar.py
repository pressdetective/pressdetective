#!/usr/bin/env python3
"""
send_nagvenkar.py
Sends a direct, warm letter to Geeta Nagvenkar (Member Secretary, GSPCB)
referencing Aires Rodrigues' personal intervention, requesting urgent site
inspection and a meeting at the property.
CC: Aires Rodrigues.
Report to gavora@gmail.com + info@pressdetective.com.
"""
import smtplib, ssl, os
from email.message import EmailMessage

HERE     = os.path.dirname(os.path.abspath(__file__))
TOKEN    = os.environ["ZEPTO_TOKEN"]
FROM     = "Olympio Almeida <olympio.almeida@pressdetective.com>"
EVIDENCE = os.path.join(HERE, "Evidence_Packet_FULL.pdf")

# ── Letter to Geeta Nagvenkar ─────────────────────────────────────

gspcb_body = (
    "To,\n"
    "Ms. Geeta Nagvenkar,\n"
    "Member Secretary,\n"
    "Goa State Pollution Control Board (GSPCB),\n"
    "Pilerne Industrial Estate, Saligao, Bardez, Goa 403 511.\n\n"
    "RE: Personal Call from Adv. Aires Rodrigues -- Formal Request for Site\n"
    "Inspection and Meeting at the Property -- Noise Pollution, Tree Felling\n"
    "& Encroachment -- Sunday Racquet and Social Club, Sodiem, Siolim.\n\n"
    "Dear Ms. Nagvenkar,\n\n"
    "I am Olympio Almeida, resident of Sodiem, Siolim, Bardez, Goa -- the\n"
    "complainant in the noise-pollution matter involving the Sunday Racquet and\n"
    "Social Club at House No. 47/3, Gaunsawaddo, Sodiem, Siolim (Survey No. 197/7).\n\n"
    "I have just received a deeply heartening message from Adv. Aires Rodrigues --\n"
    "one of Goa's most respected advocates and voices for civic justice -- who writes:\n\n"
    '    "I have just received your email and am very disturbed with the suffering\n'
    '     you\'ll are undergoing. I have spoken to the Member Secretary of the Goa\n'
    '     Pollution Control Board Geeta Nagvenkar and have requested her prompt\n'
    '     intervention. Have forwarded to her your complaint. I am currently in\n'
    '     London but will pursue the matter with her and other authorities."\n\n'
    "The fact that Adv. Rodrigues reached out to you personally, from London, within\n"
    "hours of receiving my complaint, tells me that you now understand the gravity\n"
    "and urgency of this situation. I am deeply grateful to him and to you.\n\n"
    "WHAT THIS MATTER IS ABOUT\n"
    "1. A commercial padel-court operation has encroached upon my land at Survey No.\n"
    "   197/7, Gaunsawaddo, Sodiem, Siolim, without right or title.\n"
    "2. Trees growing on the plot were felled without any Tree Authority permission\n"
    "   under the Goa Preservation of Trees Act, 1984.\n"
    "3. The courts run from 7:00 a.m. until midnight daily, generating 68-75 dB(A)\n"
    "   of continuous noise -- against the 55 dB(A) residential limit.\n"
    "4. My elderly neighbours at La Masseria -- several with multiple cardiac stents\n"
    "   -- have been unable to sleep for months.\n"
    "5. The original complaint was filed with GSPCB on 9 March 2026. Today is\n"
    "   9 June 2026. Three months. Not a single acknowledgement from GSPCB.\n"
    "6. The same plot had its Panchayat construction licence revoked in September\n"
    "   2008 (Order V.P.S.S./2008-09/977) -- on my own complaint -- for\n"
    "   unauthorised construction.\n\n"
    "WHAT I AM FORMALLY REQUESTING\n"
    "In light of Adv. Rodrigues' personal intervention and your commitment to look\n"
    "into this matter, I respectfully and warmly request:\n\n"
    "(a) AN URGENT SITE INSPECTION -- Please depute a GSPCB officer (ideally with\n"
    "    a calibrated sound level meter) to visit the site at Gaunsawaddo, Sodiem,\n"
    "    Siolim at any time between 7:00 p.m. and midnight when the disturbance is\n"
    "    at its worst. I will be at the site to personally receive your officer and\n"
    "    show them everything.\n\n"
    "(b) A MEETING AT THE PROPERTY -- I invite you, Ms. Nagvenkar, or any senior\n"
    "    GSPCB officer you nominate, to come to Sodiem, Siolim and stand at the\n"
    "    boundary of my land. See the tree stumps. Meet the elderly residents.\n"
    "    Look at the courts that have been built on my land. This matter will be\n"
    "    immediately clear to anyone who visits.\n\n"
    "(c) AN ACKNOWLEDGEMENT -- A written acknowledgement that the March 2026\n"
    "    complaint has been received and is being acted upon. This is all I have\n"
    "    been asking for since March.\n\n"
    "I am available every day, at any time. I will come to your office, meet your\n"
    "team at the site, and provide any additional documentation you need.\n\n"
    "Adv. Aires Rodrigues has assured me he will follow up with you from London.\n"
    "I am copying him on this message.\n\n"
    "The full 26-page evidence packet (complaint, photographs, noise measurements,\n"
    "2008 Panchayat revocation order, and medical records of the affected residents)\n"
    "is attached for your ready reference.\n\n"
    "With warmth, hope and respect,\n"
    "Olympio Almeida\n"
    "Resident, Sodiem, Siolim, Bardez, Goa\n"
    "olympio.almeida@pressdetective.com\n"
    "Mobile: +91 98221 68112 (please call any time -- I will answer)"
)

print("Sending to Geeta Nagvenkar / GSPCB ...", end=" ", flush=True)
m = EmailMessage()
m["From"]    = FROM
m["To"]      = "ms-gspcb.goa@nic.in"
m["Cc"]      = (
    "airesrodrigues1@gmail.com, "
    "mail.gspcb@gov.in, "
    "goapcb@gspcb.in, "
    "chairman-gspcb.goa@nic.in"
)
m["Subject"] = (
    "Personal Call from Adv. Aires Rodrigues -- Urgent Site Inspection & Meeting "
    "Request -- Siolim Padel Court Noise, Tree Felling & Encroachment"
)
m.set_content(gspcb_body)
with open(EVIDENCE, "rb") as f:
    m.add_attachment(f.read(), maintype="application", subtype="pdf",
                     filename="Evidence_Packet_Siolim_Encroachment.pdf")

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.zeptomail.in", 465, context=ctx, timeout=300) as s:
    s.ehlo()
    s.login("emailapikey", TOKEN)
    s.send_message(m)
print("OK")

# ── Report to Gautam + info ───────────────────────────────────────

report_body = (
    "Gautam,\n\n"
    "A major breakthrough: Aires Rodrigues replied within hours of receiving his\n"
    "personalised outreach email. His message to Olympio:\n\n"
    '    "I have just received your email and am very disturbed with the suffering\n'
    '     you\'ll are undergoing. I have spoken to the Member Secretary of the Goa\n'
    '     Pollution Control Board Geeta Nagvenkar and have requested her prompt\n'
    '     intervention. Have forwarded to her your complaint. I am currently in\n'
    '     London but will pursue the matter with her and other authorities."\n\n'
    "This is significant. Aires Rodrigues is one of the most respected public-interest\n"
    "advocates in Goa. He has personally called Geeta Nagvenkar (Member Secretary,\n"
    "GSPCB) and forwarded the complaint -- from London -- within hours.\n\n"
    "ACTION TAKEN IMMEDIATELY\n"
    "A targeted letter was sent to Geeta Nagvenkar:\n"
    "  To:  ms-gspcb.goa@nic.in (Member Secretary GSPCB)\n"
    "  CC:  airesrodrigues1@gmail.com | mail.gspcb@gov.in | goapcb@gspcb.in | chairman-gspcb.goa@nic.in\n"
    "  Attached: Full 26-page Evidence Packet\n\n"
    "The letter:\n"
    "- Quotes Aires' message verbatim (so Nagvenkar knows we know about their call)\n"
    "- Formally requests an urgent SITE INSPECTION with a sound level meter,\n"
    "  between 7 p.m. and midnight when the noise is at its worst\n"
    "- Personally invites Ms. Nagvenkar to come to the property and meet Olympio\n"
    "- Requests a written acknowledgement of the 9 March 2026 complaint\n"
    "- Warm, grateful and respectful in tone -- not adversarial\n\n"
    "WHY THIS CHANGES THE SITUATION\n"
    "The GSPCB Member Secretary has now received the complaint from THREE directions:\n"
    "1. Aires Rodrigues personally (phone call from London)\n"
    "2. The formal re-filing from Olympio (Track 1, sent this morning)\n"
    "3. This new letter, quoting Aires' call verbatim, with Evidence Packet attached\n\n"
    "She cannot now claim she does not know about this matter. Every step is\n"
    "documented in writing.\n\n"
    "WHAT YOU SHOULD DO NOW (IMPORTANT)\n"
    "1. WhatsApp or email Aires Rodrigues immediately. Thank him warmly. Tell him\n"
    "   the letter to Nagvenkar has been sent and copied him. Ask if he can help\n"
    "   set up a call between Olympio and Nagvenkar, or accompany Olympio to the\n"
    "   site when he returns from London.\n\n"
    "2. If Nagvenkar or any GSPCB officer contacts Olympio to arrange the site\n"
    "   inspection, confirm a date IMMEDIATELY and forward the details to\n"
    "   info@pressdetective.com.\n\n"
    "3. If no GSPCB response by 14 June (5 days), follow up with Nagvenkar and\n"
    "   copy Adv. Rodrigues on the follow-up.\n\n"
    "4. This would be an excellent moment to call the GSPCB office directly:\n"
    "   GSPCB phone: 0832-2412754 / 2412755. Ask to speak to Ms. Nagvenkar's\n"
    "   office and confirm receipt of Adv. Rodrigues' forwarded complaint.\n\n"
    "FULL CAMPAIGN STATUS (9 June 2026)\n"
    "- 156 institutional emails delivered\n"
    "- 13 supporter personalised emails sent (12/12)\n"
    "- Track 1 Phase 1: 5 formal complaints to DM, TCP, Police, Panchayat, GSPCB\n"
    "- Track 1 Phase 2: 4 RTI applications (30-day clock running)\n"
    "- Encroachment resources: 23 tailored emails to NGOs, media, government\n"
    "- Aires Rodrigues breakthrough: direct letter to GSPCB Member Secretary sent\n\n"
    "The three-way combination is fully in motion:\n"
    "COMPLAINTS + MEDIA PITCHES + NGO/ADVOCATE BACKING (Aires actively pushing)\n\n"
    "PressDetective | 9 June 2026\n"
    "olympio.almeida@pressdetective.com"
)

print("Sending report to gavora + info ...", end=" ", flush=True)
r = EmailMessage()
r["From"]    = FROM
r["To"]      = "gavora@gmail.com"
r["Cc"]      = "info@pressdetective.com"
r["Subject"] = (
    "[PressDetective] BREAKTHROUGH -- Aires Rodrigues Calls GSPCB Member Secretary; "
    "Site Inspection & Meeting Requested"
)
r.set_content(report_body)
ctx2 = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.zeptomail.in", 465, context=ctx2, timeout=300) as s:
    s.ehlo()
    s.login("emailapikey", TOKEN)
    s.send_message(r)
print("OK")
print("\nAll done.")
