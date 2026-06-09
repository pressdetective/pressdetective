#!/usr/bin/env python3
"""
send_plan.py — Send the Tarun Thadani name-cleanup plan to tarun@dharte.com

Send chain: Proton Bridge → Proton remote → ZeptoMail (first available wins).

Usage:
    python send_plan.py
    ZEPTO_TOKEN=<token> python send_plan.py          # force zepto
    PROTON_TOKEN_SANTOSH=<token> python send_plan.py # force proton remote
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from lib.mailer import send_mail, build_msg

FROM_ADDR = "santosh@pressdetective.com"
TO_ADDR   = "tarun@dharte.com"

SUBJECT = "PressDetective — Name Cleanup Plan: Tarun Thadani / FIR 0654/2022"

BODY = """\
Dear Tarun,

Please find below our Name Cleanup Plan for clearing your name in connection with
FIR No. 0654/2022 (Dadar PS, Mumbai) filed by Abhishek Badriprasad Saraf.

The plan runs across four parallel tracks:

  1. Legal — Criminal Revision + s.528 BNSS Quashing Petition at Bombay High Court,
     plus a counter-complaint against Saraf for filing a false FIR.

  2. Investigative — Saraf antecedents dossier (Martin Burn / ACB / video evidence),
     alibi reconstruction for 2 June 2022, and a pattern-of-abuse brief for counsel.

  3. Media — Press release on Saraf timed to court admission; right-of-reply to the
     Times of India (re: defamation notice of 29 Jul 2025); positive founder profile
     in a national business publication; Change.org petition.

  4. Digital — Google search audit, content suppression (IT Rules 2021 / Press Council),
     owned-content build (LinkedIn, Dharte About page, Wikipedia), and monitoring alerts.

────────────────────────────────────────────────────────────

FULL PLAN TEXT

────────────────────────────────────────────────────────────

EXECUTIVE SUMMARY

Tarun Thadani is the victim of a deliberately constructed false case. The FIR filed by
Abhishek Badriprasad Saraf contains two material fabrications:

  (1) Tarun was not present at the 2 June 2022 Worli event — his role was limited to
      sending invitations.
  (2) The ₹1 crore extortion allegation did not appear in Saraf's original complaint
      (4 June 2022) — it was inserted approximately two months later when the FIR was
      registered in August 2022, with no accused examined first.

Saraf has a documented history of vexatious litigation, ACB complaints, and alleged
forgery (Martin Burn Ltd). This plan weaponises that evidentiary record.

────────────────────────────────────────────────────────────

TRACK 1 — LEGAL (Immediate Priority)

1A. Criminal Revision Petition
  Court : Sessions Court / Bombay High Court
  Goal  : Challenge the discharge refusal of 31 March 2024
  Arguments:
    • No prima facie evidence Tarun was present on 2 June 2022
    • Extortion charge absent from original complaint; added two months later without
      examining any accused
    • No independent corroborating witness
  Counsel: Adv. Sujata Shirasi  |  +91 93216 13691
  Deadline: File within 90 days

1B. Section 528 BNSS (formerly s.482 CrPC) Quashing Petition
  Court : Bombay High Court
  Goal  : Quash FIR 0654/2022 entirely
  Arguments:
    • FIR registered on a materially amended complaint without lawful basis
    • Complainant's prior complaint negates the extortion charge
    • Abuse of process — pattern of Saraf using criminal machinery to harass
    • Video of Saraf physically assaulting Ali Asgar Merchant contradicts "victim" narrative
  Deadline: File within 60 days

1C. Counter-complaint against Abhishek Saraf
  Charges: s.182 IPC (false information), s.211 IPC (false charge), s.420 IPC (cheating)
  Supporting material: Martin Burn forgery file, ACB complaint pattern
  Counsel sign-off required before filing

────────────────────────────────────────────────────────────

TRACK 2 — INVESTIGATIVE

2A. Saraf Antecedents Dossier
  Compile into a single brief:
    • Martin Burn Ltd forgery allegations / Esplanade House file
    • ACB/fake FIR press-release narrative
    • Video: Saraf slapping Ali Asgar Merchant
    • Midday press coverage
    • All known FIRs/complaints filed by Saraf across Mumbai police stations

2B. Alibi Reconstruction (2 June 2022)
  Gather: phone location data, email/calendar records, CCTV if available,
  witness statements proving Tarun was not at the Worli venue

2C. Invitation Records
  Document that Tarun's only role was sending event invitations — no organisational
  or financial involvement in the event itself

────────────────────────────────────────────────────────────

TRACK 3 — MEDIA AND PUBLIC NARRATIVE

3A. Press Release on Saraf
  Existing draft: FOR_IMMEDIATE_RELEASE_Abhishek_Saraf.docx
  Distribution: ToI, Midday, Free Press Journal, HT Mumbai, NDTV India, The Wire
  Timing: Day the quashing petition is admitted at High Court
  Requires counsel approval

3B. Times of India Right-of-Reply
  Factual correction letter citing inaccuracies in any published article
  If no correction: Press Council of India complaint
  Brief ToI legal desk on the false-FIR angle

3C. Positive Founder Profile
  Target outlets: The Ken, Mint, YourStory, Inc42
  Angle: Dharte.com — wellness marketplace founder story
  Goal: Index above FIR coverage on Google for "Tarun Thadani"
  Timing: Coordinate with quashing petition admission

3D. Change.org Petition
  Demand accountability for Saraf's pattern of false FIRs
  Launch AFTER legal filing — do not pre-empt court proceedings

────────────────────────────────────────────────────────────

TRACK 4 — DIGITAL REPUTATION

4A. Search Audit — queries to check:
  "Tarun Thadani", "Tarun Thadani Dharte", "Tarun Thadani FIR", "Tarun Thadani Mumbai"

4B. Content Suppression
  • Press Council correction requests
  • De-listing under IT Rules 2021 once quashing order is granted

4C. Owned Content Build
  • Dharte.com About page — strong founder bio
  • LinkedIn — thought-leadership posts (wellness / sustainability)
  • Wikipedia — factual Dharte.com article (avoids FIR entirely)
  • Medium/Substack — Tarun's own writing

4D. Monitoring
  • Google Alerts: "Tarun Thadani" (daily digest)
  • Social: Twitter/X, Reddit, LinkedIn
  • New press mentions reported to PressDetective within 24 hours

────────────────────────────────────────────────────────────

TIMELINE

  Weeks 1–2  : Saraf evidence brief; alibi reconstruction; brief Adv. Shirasi
  Weeks 3–4  : File s.528 BNSS quashing petition — Bombay High Court
  Weeks 5–6  : File Criminal Revision on discharge refusal
  Weeks 6–8  : ToI right-of-reply; founder profile commissioned
  Weeks 8–12 : Press release on Saraf (timed to court admission); Change.org
  Week 12+   : Digital suppression; owned-content build; ongoing monitoring

────────────────────────────────────────────────────────────

NEXT STEPS FOR YOU

  1. Reply to confirm this plan.
  2. Share any additional evidence (location data, messages, witness contacts).
  3. Confirm Adv. Shirasi is briefed on the Tracks 1A / 1B timelines.
  4. Approve the ToI right-of-reply draft — PressDetective will prepare within 5 days.

────────────────────────────────────────────────────────────

All court filings and press releases require sign-off by Adv. Sujata Shirasi before
release. PressDetective does not provide legal advice — this plan is an investigative
and communications strategy only.

Warm regards,
Santosh
PressDetective
santosh@pressdetective.com
"""

if __name__ == "__main__":
    msg = build_msg(
        from_addr=FROM_ADDR,
        to=TO_ADDR,
        subject=SUBJECT,
        body=BODY,
        cc="info@pressdetective.com",
    )
    ok = send_mail(msg, account="santosh")
    raise SystemExit(0 if ok else 1)
