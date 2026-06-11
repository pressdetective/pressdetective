#!/usr/bin/env python3
"""
send_media_pitches.py — Pitch Tarun Thadani founder profile to national media outlets.
From    : sujata.shirasi@pressdetective.com  (via Proton Bridge)
Targets : YourStory, Inc42, Mint Lounge, The Ken
CC      : info@pressdetective.com
Usage   : python send_media_pitches.py [--dry-run]
"""
import sys, time, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from lib.mailer import send_mail, build_msg

FROM_ACC = 'sujata'
FROM_ADDR = 'sujata.shirasi@pressdetective.com'

SUBJECT = "Story Pitch: Mumbai Founder Who Turned a 35-Year Family Business Into India's Wellness Marketplace"

BODY = """\
Dear Editors,

I am writing on behalf of Tarun Thadani, the Mumbai-based entrepreneur who transformed
Silkworks — a 35-year-old home furnishings institution founded by his late father Prakash
A. Thadani in 1989 — into Dharte (dharte.com), India's first integrated wellness and
sustainability marketplace.

The story:

In 2021, with the home furnishings market disrupted post-pandemic and a personal loss to
navigate, Tarun made a counterintuitive bet: instead of shutting down or pivoting to
e-commerce, he rebuilt the company's identity around India's exploding wellness sector.
Dharte now connects thousands of seekers with yoga teachers, Ayurvedic practitioners,
sustainable brands, healers, nutritionists, and retreat venues across India — on a single
platform. It operates physical wellness spaces in Worli and on Madh Island in Mumbai,
and a retreat property in Dharamkot, Dharamshala.

Why this story now:

India's wellness market is projected to exceed $140 billion by 2030 (FICCI). Yet the
sector remains deeply fragmented — no single platform brings together the full spectrum
of practitioners, spaces, and brands. Dharte is one of the first serious attempts to do
for Indian wellness what Myntra did for fashion: aggregate, standardise, and scale.

The annual Dharte Fest (most recently September 27, 2025, at The Bombay Presidency Radio
Club, Colaba) brings together practitioners, brands, and seekers in one of Mumbai's most
storied venues — a signal that the platform has moved beyond digital to build a physical
community.

Story angles available:

  A) The pivot: how Tarun convinced his family, vendors, and customers that a 35-year
     furnishings brand could become a wellness destination — and the three years it took.

  B) The market gap: why India's $140B wellness industry still has no trusted aggregator,
     and what Dharte is building to fill it.

  C) The founder: grief, inheritance, reinvention — Tarun's personal story of losing his
     father and deciding to honour the family business by transforming it.

Happy to arrange an interview or provide further background. Tarun is available for
conversation at your convenience.

Warm regards,
Sujata Shirasi
PressDetective
sujata.shirasi@pressdetective.com

—
PressDetective represents clients in media relations, reputation management, and
investigative communications.
"""

OUTLETS = [
    {
        "label": "YourStory",
        "to": "editorial@yourstory.com",
    },
    {
        "label": "Inc42",
        "to": "editorial@inc42.com",
    },
    {
        "label": "Mint Lounge",
        "to": "mints.desk@livemint.com",
    },
    {
        "label": "The Ken",
        "to": "editorial@the-ken.com",
    },
]

def main(dry_run=False):
    for outlet in OUTLETS:
        label = outlet["label"]
        to    = outlet["to"]
        msg = build_msg(
            from_addr=FROM_ADDR,
            to=to,
            subject=SUBJECT,
            body=BODY,
        )
        if dry_run:
            print(f"[dry-run] would send to {label} <{to}>")
            continue
        ok = send_mail(msg, account=FROM_ACC)
        status = "OK" if ok else "FAILED"
        print(f"[{status}] {label} -> {to}")
        time.sleep(5)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
