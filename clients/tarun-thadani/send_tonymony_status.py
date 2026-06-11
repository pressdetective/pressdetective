#!/usr/bin/env python3
"""
send_tonymony_status.py — Status report to tonymony@gmail.com on Tarun Thadani cleanup.
From : sujata.shirasi@pressdetective.com
Usage: python send_tonymony_status.py [--dry-run]
"""
import sys, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from lib.mailer import send_mail, build_msg

FROM_ACC  = 'sujata'
FROM_ADDR = 'sujata.shirasi@pressdetective.com'
TO_ADDR   = 'tonymony@gmail.com'
SUBJECT   = "Status Report — Tarun Thadani Reputation Cleanup (9 June 2026)"

BODY = """\
Hi Tony,

Full status update on the Tarun Thadani reputation cleanup and name-clearing campaign.
Everything executed today (9 June 2026) unless stated otherwise.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CASE BACKGROUND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Client        : Tarun Thadani, Founder & CEO, Dharte (dharte.com)
Matter        : FIR No. 0654/2022, Dadar PS, Mumbai
Complainant   : Abhishek Badriprasad Saraf (Esplanade House, Mumbai)
Allegation    : Assault + Rs. 1 crore extortion (IPC s.384/385/387, 506 r/w 34)
Tarun's role  : Sent invitations only — NOT present at the Worli event
Key defence   : Extortion allegation absent from original complaint (4 Jun 2022);
                added ~2 months later without examining any accused
Status        : Discharge refused 31 Mar 2024; Quashing + Criminal Revision pending
Counsel       : Adv. Sujata Shirasi, +91 93216 13691

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOOD NEWS — DIGITAL FOOTPRINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Full Google audit run across 8 search queries. Key finding:

  The FIR does NOT appear on page 1 of Google for any search of Tarun's name.
  No Times of India, Midday or Mumbai Mirror article linking him to the case
  was found. Professional identity (Dharte, LinkedIn, Crunchbase) dominates
  all results.

  The window to build permanent narrative armour is open RIGHT NOW — before
  the High Court petition attracts press coverage.

Saraf's fraud record IS indexed on Google:
  - Change.org petition: 181 signatures, Esplanade House / Rs. 150 cr property fraud
  - 3 x openpr.com articles exposing the fake FIR and Nitin Chamaria (CFO, Blue
    Energy Motors) as a coerced witness — all ranking on "Abhishek Saraf Mumbai"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTIONS COMPLETED TODAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRACK A — NARRATIVE ARMOUR
  [SENT]   Name Cleanup Plan -> tarun@dharte.com (from santosh@pressdetective.com)
  [SENT]   Online Reputation Audit -> tarun@dharte.com (from sujata@pressdetective.com)
  [DONE]   Wikipedia article draft for Dharte.com ready for Tarun's review + submission
  [DONE]   Crunchbase expanded bio copy ready for Tarun to paste in
  [SENT]   Founder profile pitch -> YourStory (editorial@yourstory.com)
  [SENT]   Founder profile pitch -> Inc42 (editorial@inc42.com)
  [SENT]   Founder profile pitch -> Mint Lounge (mints.desk@livemint.com)
  [SENT]   Founder profile pitch -> The Ken (editorial@the-ken.com)

TRACK B — DIGITAL CLEANUP
  [SENT]   Radaris India data correction -> privacy@radaris.com + support@radaris.com
           (removes false associations with Wipro/IBM/Canon/Deepak Insurance profiles)
  [DONE]   Google Alerts setup instructions prepared for Tarun

TRACK B / PRESS
  [SENT]   Factual correction letter -> Times of India (reader@timesgroup.com +
           mumbainews@timesgroup.com)
  [SENT]   Factual correction letter -> Hindustan Times (htfeedback@hindustantimes.com +
           mumbai.desk@hindustantimes.com)
           Letters assert: (1) Tarun not present at event; (2) extortion allegation
           fabricated post-facto; (3) Saraf's documented fraud history; (4) discharge
           refusal is being challenged at Bombay HC. Requests correction of any prior
           coverage and right-of-reply before future coverage.

TRACK D — MONITORING
  [DONE]   Google Alerts setup instructions ready for Tarun to activate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PENDING — NEEDS TARUN'S INPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Google Search Console access for dharte.com
     -> sujata.shirasi@pressdetective.com to be added as verified user
     -> Enables Google Knowledge Panel claim (locks Tarun's profile in search)

  2. Wikipedia article review
     -> File: wikipedia_draft.md — Tarun to review and approve
     -> Then submitted by neutral editor (1-2 weeks to go live)

  3. Crunchbase update
     -> File: crunchbase_bio.md — Tarun to log in and paste copy

  4. Google Alerts activation
     -> File: google_alerts_setup.md — 6 alerts, 5 minutes to set up
     -> Any new negative press must reach us same day

  5. UK Companies House — company list
     -> Director appointments indexed on GOV.UK — need company names to
        assess any association risk

  6. Social media handle confirmation
     -> Two Facebook profiles — need to deactivate duplicate (tarun.thadani1)

  7. Next court date (Quashing Petition / Criminal Revision)
     -> PressDetective needs advance notice to time press release

  8. Confirmation that Adv. Sujata Shirasi has been briefed on the
     60-day (s.528 quashing) and 90-day (criminal revision) filing deadlines

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT PRIORITY ACTIONS (queued)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  - Amplify Change.org petition (181 -> 1,000+ signatures via Dharte network)
  - Off-record briefing to The Wire / Scroll / The Quint (post court filing)
  - Consolidated Saraf press release (requires Adv. Shirasi sign-off)
  - IT Rules 2021 de-listing requests (once quashing order granted)

All files committed to: github.com/pressdetective/pressdetective (branch: tarunthadani)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sujata Shirasi
PressDetective
sujata.shirasi@pressdetective.com
"""

def main(dry_run=False):
    msg = build_msg(
        from_addr=FROM_ADDR,
        to=TO_ADDR,
        subject=SUBJECT,
        body=BODY,
        cc=None,
    )
    if dry_run:
        print(f"[dry-run] would send status report to {TO_ADDR}")
        return
    ok = send_mail(msg, account=FROM_ACC)
    print(f"[{'OK' if ok else 'FAILED'}] Status report -> {TO_ADDR}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
