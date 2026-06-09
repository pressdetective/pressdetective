#!/usr/bin/env python3
"""
Send the Olympio Almeida appeal through your LOCAL Proton Bridge.

RUN THIS ON YOUR OWN COMPUTER (the one running Proton Mail Bridge) — not in any
sandbox. The script connects to Bridge at 127.0.0.1:1025.

Usage:
    1. Put this file in the same folder as:
         - 5_Simple_Appeal_from_Olympio_Almeida.pdf
         - Evidence_Packet_FULL.pdf
         - BCC_institutional_list.txt
    2. Open a terminal in that folder.
    3. Preview first (sends nothing):   python3 send_appeal.py --dry-run
    4. Send for real:                   python3 send_appeal.py
       It will prompt for your Bridge password (paste it; it is NOT stored).

Notes:
    - Recipients are split into BCC batches (default 40) with a pause between,
      to stay within Proton sending limits. Adjust BATCH_SIZE / PAUSE if needed.
    - Free Proton accounts are limited (~100 recipients/day). If you have 156
      recipients, either upgrade or run across two days (see --start/--limit).
"""
import smtplib, ssl, sys, time, os, getpass, argparse
from email.message import EmailMessage

# ---- connection / identity (from Proton Bridge) ----
HOST = "127.0.0.1"
PORT = 1025
USERNAME = "olympio.almeida@pressdetective.com"   # Bridge SMTP username
FROM_ADDR = "olympio.almeida@pressdetective.com"   # shown as the sender

BATCH_SIZE = 40       # recipients per email (in BCC)
PAUSE = 20            # seconds between batches

SUBJECT = ("Appeal to look into encroachment, illegal construction and noise "
           "nuisance — “Sunday Racquet and Social Club”, Sodiem, Siolim")

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

The attached appeal and evidence compilation set out the facts, the measured noise levels and the relevant records, including the prior Panchayat revocation order for this plot. I shall be happy to provide any further information, photographs, documents or survey records required, and to assist any inspection.

I earnestly request your kind and prompt intervention.

Yours faithfully,
Olympio Almeida
Resident of Sodiem, Siolim, Bardez - Goa
olympio.almeida@pressdetective.com
"""

ATTACHMENTS = [
    "5_Simple_Appeal_from_Olympio_Almeida.pdf",
    "Evidence_Packet_FULL.pdf",
]
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


def build_message(bcc_batch):
    here = os.path.dirname(os.path.abspath(__file__))
    msg = EmailMessage()
    msg["From"] = FROM_ADDR
    msg["To"] = FROM_ADDR          # the visible recipient is you
    msg["Bcc"] = ", ".join(bcc_batch)
    msg["Subject"] = SUBJECT
    msg.set_content(BODY)
    for path in ATTACHMENTS:
        full = os.path.join(here, path)
        with open(full, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf",
                               filename=os.path.basename(path))
    return msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="build & list batches, send nothing")
    ap.add_argument("--start", type=int, default=0, help="recipient index to start from")
    ap.add_argument("--limit", type=int, default=0, help="max recipients this run (0 = all)")
    args = ap.parse_args()

    recipients = load_recipients()
    if args.limit:
        recipients = recipients[args.start:args.start + args.limit]
    else:
        recipients = recipients[args.start:]
    batches = [recipients[i:i+BATCH_SIZE] for i in range(0, len(recipients), BATCH_SIZE)]

    print(f"Recipients this run: {len(recipients)}  |  batches: {len(batches)} "
          f"(size {BATCH_SIZE})  |  attachments: {', '.join(ATTACHMENTS)}")

    if args.dry_run:
        for i, b in enumerate(batches, 1):
            print(f"  Batch {i}: {len(b)} recipients -> {b[0]} ... {b[-1]}")
        print("DRY RUN — nothing sent.")
        return

    password = getpass.getpass("Proton Bridge password (paste, not stored): ")
    ctx = ssl.create_default_context()
    # Bridge uses a self-signed cert on localhost:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    sent = 0
    for i, b in enumerate(batches, 1):
        with smtplib.SMTP(HOST, PORT, timeout=60) as s:
            s.starttls(context=ctx)
            s.login(USERNAME, password)
            s.send_message(build_message(b))
        sent += len(b)
        print(f"  Batch {i}/{len(batches)} sent ({len(b)} recipients, {sent} total).")
        if i < len(batches):
            time.sleep(PAUSE)
    print(f"Done. Sent to {sent} recipients across {len(batches)} message(s).")


if __name__ == "__main__":
    main()
