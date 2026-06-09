#!/usr/bin/env python3
"""
Personalised ONE-TO-ONE outreach to named supporters / press, via your LOCAL
Proton Bridge. Each person gets their own separate email addressed to them by
name — NOT a mass BCC. This lands far better with journalists and campaigners.

RUN THIS ON YOUR OWN COMPUTER (where Proton Mail Bridge is running).

Place in the same folder as:
    - Supporters_Outreach.csv   (columns: Name, Verified public email(s))
    - 5_Simple_Appeal_from_Olympio_Almeida.pdf

Usage:
    python3 send_outreach.py --dry-run     # preview every personalised email, send nothing
    python3 send_outreach.py               # send for real (prompts for Bridge password)

Options:
    --only-first-email   send to just the first address per person (skip secondary/work addresses)
    --pause 30           seconds between each send (default 30; be gentle, these are individuals)
"""
import smtplib, ssl, csv, os, sys, time, getpass, argparse, re
from email.message import EmailMessage

HOST = "127.0.0.1"
PORT = 1025
USERNAME = "olympio.almeida@pressdetective.com"
FROM_ADDR = "olympio.almeida@pressdetective.com"

CSV_FILE = "Supporters_Outreach.csv"
ATTACHMENT = "5_Simple_Appeal_from_Olympio_Almeida.pdf"

SUBJECT = "Request for your support — illegal padel club & land encroachment in Siolim"

# {name} is replaced with the recipient's first name (or "there" if unknown).
BODY_TEMPLATE = """\
Dear {name},

I hope this finds you well. I'm Olympio Almeida, a resident of Sodiem, Siolim. I'm writing to you personally because of your work in defending Goa's land and communities.

A commercial padel-court business - the "Sunday Racquet and Social Club" at Gaunsawaddo, Sodiem, Siolim - is operating in the middle of our residential area. It has encroached onto my land, it runs loud play and music from morning until midnight, and it sits on a plot whose construction licence the Village Panchayat had already revoked once for being built against the approved plan.

We have complained to the Goa State Pollution Control Board, but nothing has moved. I'm attaching a short appeal setting out the facts.

I would be very grateful if you could look into it, lend your voice, or point me to the right forum or person. I'm also happy to share the full evidence file and the measured noise readings if useful.

Thank you for your time and for the work you do.

With respect,
Olympio Almeida
Sodiem, Siolim, Bardez - Goa
olympio.almeida@pressdetective.com
"""

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")


def load_people(only_first):
    here = os.path.dirname(os.path.abspath(__file__))
    people = []
    with open(os.path.join(here, CSV_FILE), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = (row.get("Name") or "").strip()
            ems = EMAIL_RE.findall(row.get("Verified public email(s)", ""))
            ems = list(dict.fromkeys(ems))
            if only_first:
                ems = ems[:1]
            if name and ems:
                people.append((name, ems))
    return people


def build(name, to_addrs):
    here = os.path.dirname(os.path.abspath(__file__))
    first = name.split()[0] if name else "there"
    msg = EmailMessage()
    msg["From"] = FROM_ADDR
    msg["To"] = ", ".join(to_addrs)
    msg["Cc"] = "info@pressdetective.com"
    msg["Subject"] = SUBJECT
    msg.set_content(BODY_TEMPLATE.format(name=first))
    with open(os.path.join(here, ATTACHMENT), "rb") as a:
        msg.add_attachment(a.read(), maintype="application", subtype="pdf",
                           filename=os.path.basename(ATTACHMENT))
    return msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only-first-email", action="store_true")
    ap.add_argument("--pause", type=int, default=30)
    args = ap.parse_args()

    people = load_people(args.only_first_email)
    print(f"Personalised emails to send: {len(people)}  |  attachment: {ATTACHMENT}")
    if args.dry_run:
        for name, ems in people:
            print(f"  -> {name}: {', '.join(ems)}")
        print("DRY RUN — nothing sent.")
        return

    password = getpass.getpass("Proton Bridge password (paste, not stored): ")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for i, (name, ems) in enumerate(people, 1):
        with smtplib.SMTP(HOST, PORT, timeout=60) as s:
            s.starttls(context=ctx)
            s.login(USERNAME, password)
            s.send_message(build(name, ems))
        print(f"  {i}/{len(people)} sent to {name} ({', '.join(ems)})")
        if i < len(people):
            time.sleep(args.pause)
    print(f"Done. {len(people)} personalised emails sent.")


if __name__ == "__main__":
    main()
