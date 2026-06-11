#!/usr/bin/env python3
"""
send_radaris_removal.py — Request data correction / removal from Radaris India.
From    : sujata.shirasi@pressdetective.com  (via Proton Bridge)
To      : privacy@radaris.com, support@radaris.com
CC      : info@pressdetective.com
Usage   : python send_radaris_removal.py [--dry-run]
"""
import sys, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from lib.mailer import send_mail, build_msg

FROM_ACC  = 'sujata'
FROM_ADDR = 'sujata.shirasi@pressdetective.com'
TO_ADDRS  = ["privacy@radaris.com", "support@radaris.com"]
SUBJECT   = "Data Correction Request — Tarun Thadani (radaris.in)"

BODY = """\
To Whom It May Concern,

I am writing on behalf of Mr. Tarun Thadani, an entrepreneur based in Mumbai, Maharashtra,
India (Founder and Group CEO, Dharte — dharte.com).

We have identified that the Radaris India profile for "Tarun Thadani" at radaris.in
incorrectly aggregates his identity with multiple unrelated individuals who share the same
name. Specifically, the profile mixes Mr. Thadani's records with:

  (a) An IT/data security analyst who worked at Wipro Technologies, Bengaluru
  (b) A marketing manager who worked at IBM and Canon India in New Delhi
  (c) A General Manager (Insurance) at Deepak Fertilisers and Petrochemicals Corp. Ltd.

None of these individuals is Mr. Tarun Thadani (Dharte). The aggregation creates false
professional associations and constitutes inaccurate personal data under applicable privacy law.

Request:

  1. REMOVE all profiles for individuals not matching: Tarun Thadani, Mumbai, Founder/CEO,
     Dharte / KPT Hospitality / Cool Chef.

  2. UPDATE the remaining (correct) profile to reflect:
       - Name: Tarun Thadani
       - Location: Mumbai, Maharashtra, India
       - Current role: Founder & Group CEO, Dharte (dharte.com)
       - Previous roles: KPT Hospitality (Founder, 2010), Cool Chef (Owner, 2010)
       - Remove: any association with Wipro, IBM, Canon India, Deepak Fertilisers,
         Bengaluru, New Delhi, or insurance sector

  3. CONFIRM removal/correction by reply to this email.

This request is made under the right to accuracy of personal data. Mr. Thadani has not
consented to Radaris India aggregating or publishing his personal information and requests
immediate correction of the inaccuracies described above.

If Radaris India is unable to correct these records within 14 days of this email, we will
escalate to the relevant data protection authority.

Please acknowledge receipt of this request.

Yours faithfully,
Sujata Shirasi
PressDetective
sujata.shirasi@pressdetective.com
+91 93216 13691
"""

def main(dry_run=False):
    for to in TO_ADDRS:
        msg = build_msg(
            from_addr=FROM_ADDR,
            to=to,
            subject=SUBJECT,
            body=BODY,
        )
        if dry_run:
            print(f"[dry-run] would send to {to}")
            continue
        ok = send_mail(msg, account=FROM_ACC)
        status = "OK" if ok else "FAILED"
        print(f"[{status}] Radaris removal -> {to}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
