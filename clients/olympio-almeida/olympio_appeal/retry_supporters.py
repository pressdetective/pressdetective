#!/usr/bin/env python3
"""Retry send for 4 supporters whose emails failed (file not found on wrong branch)."""
import smtplib, ssl, os, time
from email.message import EmailMessage

HERE    = os.path.dirname(os.path.abspath(__file__))
TOKEN   = os.environ["ZEPTO_TOKEN"]
FROM    = "olympio.almeida@pressdetective.com"
APPEAL  = os.path.join(HERE, "5_Simple_Appeal_from_Olympio_Almeida_FILLED.pdf")

SUBJECT = "Request for your support - illegal padel club & land encroachment in Siolim, Goa"

BODY = """\
Dear {first},

I hope this finds you well. I'm Olympio Almeida, a resident of Sodiem, Siolim. I'm writing to you personally because of your work in defending Goa's land and communities.

A commercial padel-court business - the "Sunday Racquet and Social Club" at Gaunsawaddo, Sodiem, Siolim - is operating in the middle of our residential area. It has encroached onto my land, it runs loud play and music from morning until midnight, and it sits on a plot whose construction licence the Village Panchayat had already revoked once (back in 2008) for being built against the approved plan - originally on my own complaint.

We have complained to the Goa State Pollution Control Board, but nothing has moved in three months. Today I have formally refiled with GSPCB, filed an application before the District Magistrate under Section 152 BNSS for a stop order, and lodged RTI applications with the TCP Department, Panchayat, GSPCB and Collectorate demanding all licence records for the plot.

I'm attaching a short appeal setting out the key facts. I would be very grateful if you could look into it, lend your voice, or point me toward the right forum or person. I'm happy to share the full 26-page evidence file and the measured noise readings if useful.

Thank you for your time and for the work you do.

With respect,
Olympio Almeida
Sodiem, Siolim, Bardez - Goa
olympio.almeida@pressdetective.com | +91 98221 68112"""

RETRIES = [
    ("Mayur Shetgaonkar / I.P. Save Goa", "ipsavegoa@gmail.com"),
    ("Swapnesh Sherlekar",                 "swapneshs2001@gmail.com"),
    ("Desmond Alvares",                    "desmond.alvares1@gmail.com"),
    ("Viresh Borkar",                      "viresh.borkar@gmail.com"),
]

def send_one(name, email):
    first = name.split()[0]
    m = EmailMessage()
    m["From"]    = FROM
    m["To"]      = email
    m["Subject"] = SUBJECT
    m.set_content(BODY.format(first=first))
    with open(APPEAL, "rb") as f:
        m.add_attachment(f.read(), maintype="application", subtype="pdf",
                         filename=os.path.basename(APPEAL))
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.zeptomail.in", 465, context=ctx, timeout=300) as s:
        s.ehlo()
        s.login("emailapikey", TOKEN)
        s.send_message(m)

ok = 0; err = 0
for name, email in RETRIES:
    print(f"  [{name}] -> {email} ...", end=" ", flush=True)
    try:
        send_one(name, email)
        print("OK"); ok += 1
    except Exception as e:
        print(f"ERROR: {e}"); err += 1
    time.sleep(10)

print(f"\nDone. {ok}/{len(RETRIES)} sent, {err} errors.")