#!/usr/bin/env python3
"""
Send the Olympio Almeida appeal through ZeptoMail SMTP.

Run on any computer with normal internet access. Place in the same folder as:
    - 5_Simple_Appeal_from_Olympio_Almeida.pdf
    - Evidence_Packet_FULL.pdf
    - BCC_institutional_list.txt

The ZeptoMail "Send Mail token" is read from the ZEPTO_TOKEN environment
variable (so it isn't written into this file). Set it first, e.g.:

    Windows (PowerShell):  $env:ZEPTO_TOKEN = "PHtE6r0E...=="
    macOS / Linux:         export ZEPTO_TOKEN="PHtE6r0E...=="

Then:
    python3 send_via_zeptomail.py --dry-run     # preview, sends nothing
    python3 send_via_zeptomail.py               # send for real
"""
import smtplib, ssl, os, sys, time, argparse
from email.message import EmailMessage

HOST = "smtp.zeptomail.in"
PORT = 587                 # STARTTLS. Use 465 with SMTP_SSL for SSL.
SMTP_USER = "emailapikey"  # literal ZeptoMail username
FROM_ADDR = "olympio.almeida@pressdetective.com"   # must be verified in ZeptoMail

BATCH_SIZE = 40
PAUSE = 20

SUBJECT = ("Appeal to look into encroachment, illegal construction and noise "
           "nuisance - \"Sunday Racquet and Social Club\", Sodiem, Siolim")

BODY = """\
Respected Sir / Madam,

I, Olympio Almeida, a resident of Sodiem, Siolim, Bardez - Goa, am writing to appeal to all the authorities concerned to kindly look into a serious and continuing matter at Survey No. 197 / House No. 47/3, Gaunsawaddo, Sodiem, Siolim.

A commercial sporting business - outdoor padel courts operating as the "Sunday Racquet and Social Club" - is being run in the middle of a residential area, immediately next to family homes. It has also ENCROACHED UPON MY LAND. It is causing daily distress to residents, several of whom are senior citizens, and it appears to be operating in violation of the law. In particular:

1. Encroachment on my property - the operators have encroached upon and occupied a portion of my land without any right, title or consent;
2. Loud and continuous noise - the sharp impact of paddle-ball play, amplified music and rowdy, late-night activity - from early morning until around midnight, well above the noise limits permitted for a residential area;
3. Commercial use of land in a residential zone, with no proper buffer from neighbouring homes; and
4. A documented history of unauthorised construction at this very plot - the Village Panchayat Siolim-Sodiem had earlier revoked the construction licence here for building "not as per the approved plan."

Despite complaints already made, the disturbance continues and no effective action appears to have been taken on the ground.

I therefore appeal to the authorities to kindly:

1. Carry out an inspection and a survey/demarcation of the premises, including during evening and night hours when the disturbance is at its worst;
2. Examine the legality of the construction and the commercial operation on this residential plot, and have the encroachment on my land surveyed, removed and my property restored to me;
3. Take appropriate action under the noise-pollution, public-nuisance, planning and panchayat laws; and
4. Direct that the disturbance be stopped, so that residents - especially the elderly and unwell - can live in peace.

The attached appeal and evidence compilation set out the facts, the measured noise levels and the relevant records. I shall be happy to provide any further information required, and to assist any inspection.

I earnestly request your kind and prompt intervention.

Yours faithfully,
Olympio Almeida
Sodiem, Siolim, Bardez - Goa
olympio.almeida@pressdetective.com
"""

ATTACHMENTS = ["5_Simple_Appeal_from_Olympio_Almeida.pdf", "Evidence_Packet_FULL.pdf"]
RECIPIENTS_FILE = "BCC_institutional_list.txt"


def load_recipients():
    here = os.path.dirname(os.path.abspath(__file__))
    raw = open(os.path.join(here, RECIPIENTS_FILE), encoding="utf-8").read()
    seen, out = set(), []
    for e in raw.replace("\n", ",").split(","):
        e = e.strip()
        if e and e.lower() not in seen:
            seen.add(e.lower()); out.append(e)
    return out


def build(bcc):
    here = os.path.dirname(os.path.abspath(__file__))
    m = EmailMessage()
    m["From"] = FROM_ADDR
    m["To"] = FROM_ADDR
    m["Cc"] = "info@pressdetective.com"
    m["Bcc"] = ", ".join(bcc)
    m["Subject"] = SUBJECT
    m.set_content(BODY)
    for p in ATTACHMENTS:
        with open(os.path.join(here, p), "rb") as f:
            m.add_attachment(f.read(), maintype="application", subtype="pdf",
                             filename=os.path.basename(p))
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    recips = load_recipients()
    recips = recips[args.start: args.start + args.limit] if args.limit else recips[args.start:]
    batches = [recips[i:i+BATCH_SIZE] for i in range(0, len(recips), BATCH_SIZE)]
    print(f"Recipients: {len(recips)} | batches: {len(batches)} (size {BATCH_SIZE})")

    if args.dry_run:
        for i, b in enumerate(batches, 1):
            print(f"  Batch {i}: {len(b)} -> {b[0]} ... {b[-1]}")
        print("DRY RUN - nothing sent.")
        return

    token = os.environ.get("ZEPTO_TOKEN")
    if not token:
        print("ERROR: set ZEPTO_TOKEN env var to your ZeptoMail Send Mail token.")
        sys.exit(1)

    ctx = ssl.create_default_context()
    sent = 0
    for i, b in enumerate(batches, 1):
        with smtplib.SMTP(HOST, PORT, timeout=60) as s:
            s.starttls(context=ctx)
            s.login(SMTP_USER, token)
            s.send_message(build(b))
        sent += len(b)
        print(f"  Batch {i}/{len(batches)} sent ({sent} total).")
        if i < len(batches):
            time.sleep(PAUSE)
    print(f"Done. Sent to {sent} recipients.")


if __name__ == "__main__":
    main()
