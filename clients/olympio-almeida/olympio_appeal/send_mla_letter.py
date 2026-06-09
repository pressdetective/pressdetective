#!/usr/bin/env python3
"""send_mla_letter.py — Open letter to Delilah Lobo MLA Siolim."""
import smtplib, ssl, os
from email.message import EmailMessage

HERE  = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.environ["ZEPTO_TOKEN"]
FROM  = "Olympio Almeida <olympio.almeida@pressdetective.com>"
EVIDENCE = os.path.join(HERE, "Evidence_Packet_FULL.pdf")

CC_LIST = [
    "coln.goa@nic.in","ms-gspcb.goa@nic.in","ctp-tcp.goa@nic.in",
    "sdm-mapusa.goa@nic.in","vpsiolimsodiem@gmail.com",
    "picoastal.siolim@goapolice.gov.in","spn-pol.goa@nic.in",
    "dgpgoa@goapolice.gov.in","cmgoa.grievance@gov.in",
    "editor@heraldgoa.in","news@heraldgoa.in",
    "editor@thegoan.net","desk@thegoan.net",
    "editor@goachronicle.com","info@prudentmedia.in",
    "tips@scroll.in","editor@thewire.in",
    "dtedit@cse.org.in","airgoa@gmail.com",
    "airesrodrigues1@gmail.com","goafoundation@gmail.com",
    "bailanchomanch@gmail.com","goabachaoabhiyan@gmail.com",
    "heta.pandit@gmail.com","pravinsingh03@gmail.com",
    "swapneshs2001@gmail.com","ngtwz@nic.in",
    "dir-land.goa@nic.in","ac1-north.goa@nic.in","dipgoa@gmail.com",
]

LETTER = """To,
Ms. Delilah Lobo,
Member of Legislative Assembly, Siolim Constituency,
Goa Legislative Assembly.

Respected Ms. Lobo,

I write to you with the deepest respect for your position as the elected
representative of the people of Siolim. I am Olympio Almeida, a lifelong
resident of Sodiem, Siolim -- your own constituency -- and I am writing because
I have a matter of great importance and of great personal pain that only you,
as our MLA, are in a position to help resolve.

I am writing openly. I am copying this letter to government officials, the press,
and civil society, because the matter involves a public inauguration that you
conducted, and because I believe you deserve the opportunity to respond publicly
and transparently to the questions I am raising.

I ask these questions not to embarrass you, but because I genuinely seek the truth
and because I believe you, as our elected representative, would want to know the
truth too.

==================================================================
THE INAUGURATION
==================================================================

On your official Facebook page (facebook.com/DelilahLoboofficial), you attended
and inaugurated the newly opened Sunday Racquet Club at Sodiem, Siolim. You
described it as "a fantastic initiative promoting sports, fitness and community
spirit" and expressed that you wished "the club great success."

I have no doubt that you attended this event in good faith, wishing to support a
sports initiative in your constituency. But I need you to know what I know about
this place -- because I believe you were not told.

==================================================================
WHAT I KNOW ABOUT THIS PLACE
==================================================================

The Sunday Racquet Club operates at House No. 47/3, Gaunsawaddo, Sodiem, Siolim,
on a plot identified as Survey No. 197/7.

1. THE SAME PLOT HAD ITS LICENCE REVOKED IN 2008 -- ON MY COMPLAINT
   In 2008, I myself filed a complaint with the Village Panchayat Siolim-Sodiem
   regarding unauthorised construction on Survey No. 197/7. The Panchayat confirmed
   construction "not as per the approved plan." The Panchayat issued Revocation Order
   Ref. V.P.S.S./2008-09/977 on 24 September 2008, revoking the construction licence
   under the Goa Panchayat Raj Act, 1994. TCP Mapusa Inspection Report
   Ref. DB/18694/08/1755 (11 July 2008) is on official record.

2. THE CLUB HAS ENCROACHED ON MY LAND
   A portion of my personal land at Survey No. 197/7, Gaunsawaddo, Sodiem,
   is being occupied by this club without any right, title, or consent from me.

3. TREES WERE FELLED WITHOUT PERMISSION
   Trees that grew on this land were cut down to build the padel courts,
   without any Tree Authority permission under the Goa Preservation of Trees Act, 1984.

4. ELDERLY RESIDENTS CANNOT SLEEP
   The club operates from 7:00 a.m. until midnight, generating noise of 68-75 dB(A).
   The residential limit is 55 dB(A). My neighbours include elderly senior citizens
   with coronary artery disease and multiple cardiac stents. They cannot sleep.

5. THREE MONTHS OF GSPCB SILENCE
   A detailed 26-page complaint was filed with the GSPCB on 9 March 2026.
   Three months passed with not a single acknowledgement.

==================================================================
MY QUESTIONS TO YOU
==================================================================

Respected Ms. Lobo, as my elected MLA and as a public official, I respectfully ask:

1. Before inaugurating the Sunday Racquet Club, were you informed -- or did you
   inquire -- whether the operation had valid licences from the Panchayat, TCP,
   and GSPCB? Were you aware the same plot had its construction licence revoked
   by your own constituency's Panchayat in 2008?

2. Were you aware that the club is built on land that includes a portion belonging
   to a resident of your constituency -- without his consent?

3. Were you aware that elderly residents of Siolim -- your own constituents --
   have been unable to sleep because of the noise, and that some have serious
   cardiac conditions?

4. As MLA for Siolim, will you now:
   (a) Inquire into the licences held (or not held) by the Sunday Racquet Club?
   (b) Intervene with the GSPCB to ensure a response to the March 2026 complaint?
   (c) Visit the site in person and meet the affected residents?

5. I ask with humility and with no intent to cause offence: is there any connection
   between you or your office and the operators of this club that the public should
   know about? I raise this because the inauguration by an MLA of what appears to be
   an unlicensed operation -- in the MLA's own constituency -- is something the
   residents of Siolim and the press will naturally ask about. I give you the
   opportunity to answer it first, and on your own terms.

==================================================================
WHERE THIS MATTER STANDS TODAY
==================================================================

On 9 June 2026, formal complaints were filed simultaneously with:
- The District Magistrate, North Goa
- TCP Department, Mapusa
- Village Panchayat Siolim-Sodiem
- Coastal Police Station, Siolim
- GSPCB (re-filing with warning of NGT proceedings)
- RTI applications filed with all four authorities

Adv. Aires Rodrigues -- one of Goa's most respected civic voices -- has personally
spoken to GSPCB Member Secretary Ms. Geeta Nagvenkar and forwarded the complaint.
A formal letter was sent to Ms. Nagvenkar today, copied to Adv. Rodrigues.

==================================================================
MY INVITATION TO YOU
==================================================================

I invite you, Ms. Lobo, to come to Sodiem -- your own constituency -- and visit
the site. Come and see the tree stumps where trees once stood. Meet the elderly
residents at La Masseria who cannot sleep. Stand on my land and see what has
been taken.

I am available every day. I pick up the phone: +91 98221 68112

The 26-page evidence file is attached to this letter.

Yours respectfully and with hope,
Olympio Almeida
Resident, Sodiem, Siolim, Bardez, Goa
olympio.almeida@pressdetective.com
Mobile: +91 98221 68112"""


def smtp_send(msg):
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.zeptomail.in", 465, context=ctx, timeout=300) as s:
        s.ehlo()
        s.login("emailapikey", TOKEN)
        s.send_message(msg)


def send_mla_letter():
    print("Sending open letter to Delilah Lobo MLA ...", end=" ", flush=True)
    m = EmailMessage()
    m["From"]    = FROM
    m["To"]      = "mlasil.gvs@gov.in"
    m["Cc"]      = ", ".join(CC_LIST)
    m["Subject"] = (
        "Open Letter to MLA Siolim — Regarding Your Inauguration of the Sunday Racquet "
        "Club at Sodiem: Questions About Licences, Encroachment and Affected Residents"
    )
    m.set_content(LETTER)
    with open(EVIDENCE, "rb") as f:
        m.add_attachment(f.read(), maintype="application", subtype="pdf",
                         filename="Evidence_Packet_Siolim_Encroachment.pdf")
    smtp_send(m)
    print("OK")


def send_report():
    cc_display = "\n".join(f"  {i+1:2d}. {e}" for i, e in enumerate(CC_LIST))
    report = f"""Gautam,

A pivotal development in the Olympio Almeida Siolim case.

DELILAH LOBO MLA -- THE SIOLIM CONSTITUENCY MLA -- publicly attended and
inaugurated the Sunday Racquet Club at Sodiem, Siolim. On her official Facebook
page, she described it as "a fantastic initiative promoting sports, fitness and
community spirit" and wished it "great success."

She is the elected MLA for the very constituency where the club operates illegally,
on land with a revoked Panchayat licence, encroaching on Olympio's land, with trees
felled without permission.

ACTION TAKEN
An open letter was sent to Delilah Lobo at her official MLA email (mlasil.gvs@gov.in)
with 30 people on CC: government officials, press, NGOs and civic advocates.

The letter asks, respectfully and specifically:
1. Did she check the club's licences before inaugurating it?
2. Was she aware the same plot's licence was revoked in 2008 -- on Olympio's complaint?
3. Was she aware the club occupies Olympio's land without consent?
4. Was she aware elderly constituents with cardiac conditions cannot sleep?
5. Will she now intervene with GSPCB, Panchayat and TCP?
6. Is there any connection between her and the club's operators? (Phrased
   respectfully, giving her the chance to answer first on her own terms)

She is invited to visit the property in person and meet the affected residents.
The 26-page Evidence Packet was attached to the letter.

30-PERSON CC LIST
{cc_display}

WHY THIS IS SIGNIFICANT
An MLA publicly endorsing an operation that has no valid licence, is on land
with a 2008 revocation order, has encroached on a resident's land, has had trees
felled illegally, and has left elderly cardiac patients unable to sleep -- is now
a matter of public record.

With 10 press outlets, the NGT, the GSPCB Member Secretary (now personally
engaged via Aires Rodrigues), and 7 NGOs all copied, she will need to respond.

If she does not respond within 7 days, the letter itself -- and her silence --
becomes a news story. If she responds, whatever she says will clarify her
connection to the club.

WHAT YOU SHOULD DO NOW
1. WhatsApp or email Aires Rodrigues (airesrodrigues1@gmail.com) and tell him
   the MLA letter has been sent. He may have intelligence on Delilah Lobo and
   the club operators.

2. If any press outlet contacts you, be brief and factual:
   "We have asked the MLA to clarify whether she was aware of the licence issues
   before the inauguration. We are awaiting her response."

3. Forward the inauguration Facebook video/post to:
   - info@prudentmedia.in (Prudent Media TV -- most impactful in Goa)
   - editor@heraldgoa.in
   Say: "This is the MLA at the inauguration. Our letter to her was sent today.
   Happy to share the full evidence file if you want to investigate."

4. Document any response from Delilah Lobo's office and forward immediately
   to info@pressdetective.com.

FULL CAMPAIGN STATUS (9 June 2026)
- 156 institutional emails: delivered
- 13 supporter personalised emails: all sent
- Track 1: 5 formal complaints + 4 RTI applications filed on 9 June 2026
- 23 NGO/media/government outreach emails
- GSPCB Member Secretary (Geeta Nagvenkar): personal letter sent, CC Aires
- MLA Siolim (Delilah Lobo): open letter sent, 30 on CC

PressDetective | 9 June 2026"""

    print("Sending report to gavora + info ...", end=" ", flush=True)
    r = EmailMessage()
    r["From"]    = FROM
    r["To"]      = "gavora@gmail.com"
    r["Cc"]      = "info@pressdetective.com"
    r["Subject"] = (
        "[PressDetective] OPEN LETTER SENT TO MLA SIOLIM — Delilah Lobo Inaugurated "
        "the Club — 30 on CC Including All Press"
    )
    r.set_content(report)
    smtp_send(r)
    print("OK")


if __name__ == "__main__":
    send_mla_letter()
    send_report()
    print("\nDone.")
