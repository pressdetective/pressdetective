"""
Reply to Goan Observer journalist — introduce Gautam as neighbour-complainant.
FROM olympio.almeida@pressdetective.com via Proton remote SMTP.
CC: gavora@gmail.com (Gautam), info@pressdetective.com

    python clients/olympio-almeida/olympio_appeal/send_goanobserver_reply.py
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

TO_JOURNALIST = "goanobserver@gmail.com"
CC_GAUTAM     = "gavora@gmail.com"
CC_INFO       = "info@pressdetective.com"

SUBJ = ("Re: Siolim Noise Complaint — Please Connect with My Neighbour "
        "Gautam Vora Who Has Also Filed a Complaint | +91 98207 00995")

BODY = """\
Dear Editor / Reporter at Goa Observer,

Thank you so much for getting in touch. I am very grateful that you
are looking into this matter — it means a great deal to me.

I am afraid I am not keeping very well at the moment and am unable
to speak at length just now. I apologise for this.

However, I want to make sure you have everything you need for the
story, and so I am connecting you with my neighbour, Mr. Gautam Vora,
who lives nearby and has also been seriously affected by the noise
from the Sunday Racquet and Social Club padel courts.

Mr. Vora has independently filed his own written complaint about the
noise pollution from these courts. He has all the documents, has
been following the case closely, and is in a very good position to
speak to you about the full situation on the ground.

Please call him directly — he is expecting to hear from press:

    Gautam Vora
    Phone: +91 98207 00995
    Email: gavora@gmail.com

I have copied him on this email so he knows you may be in touch.

Mr. Vora can also give you access to:
  — The 26-page evidence packet (noise measurements, photographs,
    the 2008 Panchayat order, the GSPCB complaint, and the
    SP (SPCR) acknowledgement)
  — Details of the 17 June joint inspection and its outcome
  — The documented non-attendance of GSPCB
  — The complete timeline of this case

For anything further from my side, please write to
info@pressdetective.com and we will respond promptly.

We would very much welcome a story in Goa Observer. This is a matter
that affects many residents in Siolim and raises serious questions
about whether Goa's noise-pollution law is actually enforced.

The key facts for your story:

  My home:     La Masseria, Survey No. 197/A, Sodiem, Siolim
  The club:    Sunday Racquet and Social Club, House 47/3, Sodiem
  Noise:       68-75 dB(A) at my property (legal limit: 55 dB)
  2008:        Panchayat issued licence-revocation order — never
               enforced in 18 years
  March 2026:  Formal GSPCB complaint filed — no response in 104 days
  June 2026:   GSPCB failed to attend the formal joint inspection
               despite 9 days' advance notice from the Panchayat
  Police:      SP (SPCR) Panaji responded and forwarded for action
  MLA Siolim:  Delilah Lobo has not responded to repeated appeals

Please do call Gautam. He will give you everything you need.

Thank you again for your interest. I look forward to reading the
story in Goa Observer.

With warm regards,
Olympio Almeida
Siolim, Goa
olympio.almeida@pressdetective.com
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJ
msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
msg["To"]      = TO_JOURNALIST
msg["Cc"]      = f"{CC_GAUTAM}, {CC_INFO}"
msg.attach(MIMEText(BODY, "plain", "utf-8"))

rcpts = [TO_JOURNALIST, CC_GAUTAM, CC_INFO]

ctx = ssl.create_default_context()
print("Sending reply to Goan Observer ...")
print(f"  TO:  {TO_JOURNALIST}")
print(f"  CC:  {CC_GAUTAM}, {CC_INFO}")
try:
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())
    print("  OK — delivered to all three recipients")
except Exception as e:
    print(f"  FAIL: {e}")
