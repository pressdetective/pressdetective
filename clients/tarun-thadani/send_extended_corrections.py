#!/usr/bin/env python3
"""
Day 1: Send factual correction / pre-publication notices to:
  - Midday (Mumbai)
  - Free Press Journal (Mumbai)
  - Maharashtra Times (Mumbai)
  - NDTV India (crime desk)
  - Mumbai Mirror / Mirror Now (digital)

Run from repo root: python clients/tarun-thadani/send_extended_corrections.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.mailer import send_mail, build_msg

FROM     = "sujata.shirasi@pressdetective.com"
FROM_DISPLAY = "Adv. Sujata Shirasi <sujata.shirasi@pressdetective.com>"
CC_EXTRA = ["info@pressdetective.com"]

LETTER_PREPUB = """\
Dear Editor / Crime Desk,

I write on behalf of my client Tarun Thadani, Founder and CEO of Dharte (dharte.com),
to draw your attention to a factual matter before it reaches publication.

An article in the Times of India (Mumbai) — "Two bizmen chargesheeted for assault, \
Rs 1cr extortion bid in '22" (byline: S Ahmed Ali) — reported on FIR No. 0654/2022 \
registered at Dadar Police Station, Mumbai.

I write to ensure your editorial desk has full factual context:

1. My client was NOT present at the location of the alleged incident on the date
   in question. This is verifiable from contemporaneous records and will be
   demonstrated in proceedings before the Bombay High Court.

2. There was no extortion demand. The FIR complainant, Mr. Abhishek Badriprasad
   Saraf, owed money to my client. The FIR was filed after Mr. Saraf defaulted on
   his obligations and is part of a documented pattern of using criminal complaints
   to evade creditors.

3. Mr. Saraf has prior disputes on record — including a matter before the
   Anti-Corruption Bureau — that are directly relevant to his credibility as
   a complainant. These antecedents are a matter of public record.

4. A Section 528 BNSS (formerly S. 482 CrPC) quashing petition is filed by the
   co-accused. My client's petition is being finalised.

Under Press Council of India Norm 7, we request that before any publication
referencing FIR 0654/2022 or Tarun Thadani's name in connection with it, your
desk affords us the right of reply. Please contact me at the details below.

A factual correction letter has already been sent to Times of India Mumbai
(mumbainews@timesgroup.com) on 11 June 2026.

Yours faithfully,
Adv. Sujata Shirasi
On behalf of Tarun Thadani
+91 93216 13691
sujata.shirasi@pressdetective.com
info@pressdetective.com
"""

LETTER_MIDDAY = """\
Dear Midday Editorial Desk / Crime Reporter,

I write on behalf of Tarun Thadani (tarun@dharte.com), Founder of Dharte.com,
regarding FIR No. 0654/2022 (Dadar PS, Mumbai) and specifically the Times of
India article published under the headline "Two bizmen chargesheeted for assault,
Rs 1cr extortion bid in '22" (byline: S Ahmed Ali).

We are writing proactively to ensure Midday has the full picture should this
story come to your attention:

FACTS ON RECORD:
- Tarun Thadani was not present at the alleged incident location
- No extortion demand was made — the complainant owed Mr. Thadani money
- The complainant (Abhishek Badriprasad Saraf) has prior disputes including
  an Anti-Corruption Bureau matter
- A quashing petition under Section 528 BNSS is in progress before the
  Bombay High Court

In keeping with Press Council Norm 7, we request advance right-of-reply
before any coverage of this matter.

Adv. Sujata Shirasi | +91 93216 13691 | sujata.shirasi@pressdetective.com
"""


OUTLETS = [
    {
        "label":    "Midday Mumbai",
        "to":       "feedback@mid-day.com",
        "cc_extra": [],
        "subject":  "Pre-publication notice: Tarun Thadani / FIR 0654/2022 — right of reply request",
        "body":     LETTER_MIDDAY,
    },
    {
        "label":    "Midday Mumbai (letters)",
        "to":       "letters@mid-day.com",
        "cc_extra": [],
        "subject":  "Factual correction request: Tarun Thadani / FIR 0654/2022",
        "body":     LETTER_MIDDAY,
    },
    {
        "label":    "Free Press Journal Mumbai",
        "to":       "letters@freepressjournal.in",
        "cc_extra": [],
        "subject":  "Pre-publication right-of-reply request: Tarun Thadani / FIR 0654/2022",
        "body":     LETTER_PREPUB,
    },
    {
        "label":    "Maharashtra Times",
        "to":       "mtletters@timesgroup.com",
        "cc_extra": ["mumbaidesk@timesgroup.com"],
        "subject":  "Pre-publication right-of-reply: Tarun Thadani / FIR 0654/2022",
        "body":     LETTER_PREPUB,
    },
    {
        "label":    "NDTV India Mumbai",
        "to":       "mumbai@ndtv.com",
        "cc_extra": [],
        "subject":  "Right-of-reply request re FIR 0654/2022: Tarun Thadani, Dharte.com",
        "body":     LETTER_PREPUB,
    },
    {
        "label":    "Mirror Now / Mumbai Mirror digital",
        "to":       "feedback@mirrorindiatv.com",
        "cc_extra": [],
        "subject":  "Factual notice: Tarun Thadani / FIR 0654/2022 — right of reply",
        "body":     LETTER_PREPUB,
    },
]


def main():
    seen = set()
    for outlet in OUTLETS:
        to_addr = outlet["to"]
        if to_addr in seen:
            print(f"[skip] duplicate to={to_addr}")
            continue
        seen.add(to_addr)

        cc_list = list(CC_EXTRA) + outlet.get("cc_extra", [])
        cc_str  = ", ".join(cc_list) if cc_list else None

        msg = build_msg(
            from_addr=FROM_DISPLAY,
            to=to_addr,
            subject=outlet["subject"],
            body=outlet["body"],
            cc=cc_str,
        )
        ok = send_mail(msg, account="sujata")
        status = "OK" if ok else "FAILED"
        print(f"[{status}] {outlet['label']} -> {to_addr}")


if __name__ == "__main__":
    main()
