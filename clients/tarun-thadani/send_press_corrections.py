#!/usr/bin/env python3
"""
send_press_corrections.py
Factual correction / right-of-reply letters to Times of India and Hindustan Times
re: coverage of FIR No. 0654/2022 and Tarun Thadani.

From : sujata.shirasi@pressdetective.com
CC   : info@pressdetective.com
Usage: python send_press_corrections.py [--dry-run]
"""
import sys, time, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from lib.mailer import send_mail, build_msg

FROM_ACC  = 'sujata'
FROM_ADDR = 'sujata.shirasi@pressdetective.com'

SUBJECT = ("Factual Correction Request — Tarun Thadani / FIR No. 0654/2022, "
           "Dadar Police Station, Mumbai")

BODY = """\
Dear Editors / Corrections Desk,

We write on behalf of Mr. Tarun Thadani, Founder and Group CEO of Dharte
(dharte.com), a wellness and sustainability marketplace headquartered in Mumbai.

We are aware that your publication may have reported on, or may in future report
on, FIR No. 0654 of 2022 registered at Dadar Police Station, Mumbai, in which
Mr. Thadani is named as an accused. We respectfully request that any such
reporting — past or future — reflect the following verified facts, which are
supported by documentary evidence and available for your inspection.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFIED FACTS — PLEASE CORRECT OR INCORPORATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MR. THADANI WAS NOT PRESENT AT THE INCIDENT
   The FIR concerns an alleged incident at a private event at a restaurant in
   Worli, Mumbai, on the night of 2–3 June 2022. Mr. Thadani's sole connection
   to the event was sending invitations. He was not present at the venue.
   No independent witness places him there. This is a matter of documentary
   record available to any journalist who requests it.

2. THE EXTORTION ALLEGATION WAS FABRICATED AFTER THE FACT
   The complainant, Mr. Abhishek Badriprasad Saraf, filed his original complaint
   on 4 June 2022. That complaint alleged assault only. It contained no mention
   of extortion and no mention of Mr. Thadani. The ₹1 crore extortion allegation
   and Mr. Thadani's name were introduced approximately two months later when the
   FIR was eventually registered in August 2022 — without any accused being
   examined, and without any corroborating evidence being produced.

3. THE COMPLAINANT HAS A DOCUMENTED HISTORY OF VEXATIOUS LITIGATION
   Mr. Abhishek Badriprasad Saraf is the subject of a Change.org petition
   (181 signatures) alleging he unlawfully occupies the third floor of Esplanade
   House, the historic home of Jamsetji Tata (UNESCO Heritage Site), using a
   forged power of attorney — a scheme valued at over ₹150 crore. Court records
   and investigative files document his alleged pattern of filing false FIRs and
   using criminal process as a tool of harassment.

4. DISCHARGE WAS REFUSED BUT IS BEING CHALLENGED
   The Sessions Court refused discharge on 31 March 2024. This is a procedural
   ruling on prima facie sufficiency — it does not constitute a finding of guilt.
   Mr. Thadani is challenging the refusal by way of Criminal Revision and a
   petition under Section 528 of the BNSS (formerly Section 482 CrPC) before
   the Bombay High Court. These proceedings are ongoing.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUR REQUESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A. If your publication has already published any article linking Mr. Thadani
   to this FIR without the above context, we request an immediate correction
   or addendum incorporating these facts.

B. If your publication is planning to report on this matter, we request an
   opportunity to provide a formal statement and supporting documents before
   publication — as required by responsible journalism practice and the
   guidelines of the Press Council of India.

C. We request written confirmation that this letter has been received and
   forwarded to the relevant editor and legal desk.

We are available to provide documentary evidence — including the original
4 June 2022 complaint (showing no extortion, no mention of Mr. Thadani),
the court order of 31 March 2024, the Change.org petition against Mr. Saraf,
and the Bombay High Court filing reference — to any journalist or editor
upon request.

Failure to correct inaccurate reporting may result in a formal complaint to
the Press Council of India and legal proceedings for defamation.

We trust your commitment to factual and fair reporting.

Yours faithfully,
Sujata Shirasi
PressDetective — Legal & Media Relations
On behalf of Mr. Tarun Thadani
sujata.shirasi@pressdetective.com
+91 93216 13691

Counsel of record: Adv. Sujata Shirasi, Bombay High Court
"""

OUTLETS = [
    {
        "label": "Times of India — Corrections / Reader Response",
        "to": "reader@timesgroup.com",
        "cc_extra": "mumbainews@timesgroup.com",
    },
    {
        "label": "Times of India — Mumbai Desk",
        "to": "mumbainews@timesgroup.com",
        "cc_extra": None,
    },
    {
        "label": "Hindustan Times — Feedback / Corrections",
        "to": "htfeedback@hindustantimes.com",
        "cc_extra": "mumbai.desk@hindustantimes.com",
    },
    {
        "label": "Hindustan Times — Mumbai Desk",
        "to": "mumbai.desk@hindustantimes.com",
        "cc_extra": None,
    },
]

def main(dry_run=False):
    seen = set()
    for outlet in OUTLETS:
        to = outlet["to"]
        if to in seen:
            continue
        seen.add(to)
        label = outlet["label"]
        cc_extra = outlet.get("cc_extra")
        cc = "info@pressdetective.com"
        if cc_extra:
            cc = f"info@pressdetective.com, {cc_extra}"
        msg = build_msg(
            from_addr=FROM_ADDR,
            to=to,
            subject=SUBJECT,
            body=BODY,
            cc=cc,
        )
        if dry_run:
            print(f"[dry-run] would send to {label} <{to}>")
            continue
        ok = send_mail(msg, account=FROM_ACC)
        status = "OK" if ok else "FAILED"
        print(f"[{status}] {label} -> {to}")
        time.sleep(4)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
