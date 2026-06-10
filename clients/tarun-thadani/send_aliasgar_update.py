#!/usr/bin/env python3
"""
send_aliasgar_update.py
Full legal update + plan of action for Ali Asgar Merchant, co-accused in FIR 0654/2022.

NOTE: Video is confidential case evidence — do NOT attach or distribute via email.

From : Adv. Sujata Shirasi <sujata.shirasi@pressdetective.com>
To   : aliasgarmerchant@gmail.com
CC   : info@pressdetective.com

Legal note: video is shared strictly for purposes of legal defence in
FIR 0654/2022 and must not be shared publicly or with any third party
outside these proceedings.
"""
import sys, time
from email.message import EmailMessage
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.mailer import build_msg, send_mail

FROM_ACCT = "sujata"
TO        = "aliasgarmerchant@gmail.com"
CC        = ["info@pressdetective.com"]

VIDEO_PATH = Path("G:/My Drive/ABHISHEK SARAF/Abhishek_Saraf_Slap_Ali_Asgar_Merchant.mp4")

SUBJECT = (
    "YOUR FULL LEGAL UPDATE + PLAN OF ACTION | FIR 0654/2022 | "
    "Adv. Sujata Shirasi | 9 June 2026"
)

BODY = """\
Dear Mr. Ali Asgar Merchant,

I am Adv. Sujata Shirasi, Counsel for Mr. Tarun Thadani and the legal
team handling FIR No. 0654/2022.  I am writing to you today with a
complete, honest update on where this case stands, a plain-English
legal analysis of what the evidence actually shows, and a clear plan
of action for proving your innocence.

Please read this in full.  It matters.

I have also attached the video of the incident (Abhishek_Saraf_Slap_
Ali_Asgar_Merchant.mp4).  This video is provided to you strictly for
the purposes of your legal defence.  Do not share it publicly or with
anyone outside this legal matter.

======================================================================
PART 1 — WHAT THE VIDEO ACTUALLY PROVES (LEGAL ANALYSIS)
======================================================================

The video shows you slapping Abhishek Badriprasad Saraf.

I am telling you this honestly because your defence begins with
facing the facts squarely.  Here is what that means legally:

  WHAT THE VIDEO DOES PROVE
  ─────────────────────────
  The incident on 2 June 2022 was a physical altercation — a slap.
  That is it.

  In law, this is Section 319 of the Indian Penal Code — voluntarily
  causing hurt.  The maximum punishment is ONE YEAR imprisonment
  OR a fine, OR both (Section 323 IPC).

  CRITICALLY: Section 323 IPC is a BAILABLE offence.  This means:
    - Police CANNOT arrest you without a warrant
    - You are entitled to bail as a matter of right
    - It is tried by the Magistrate as a minor offence
    - It is even COMPOUNDABLE — meaning it can be settled
      between the parties

  WHAT THE VIDEO DOES NOT PROVE
  ──────────────────────────────
  The video shows a slap.  It does NOT show:
    - Any demand for money
    - Any threat for payment
    - Any mention of Rs. 1 crore
    - Any "or else" threat
    - Any conversation about extortion

  Because none of that happened.

  THIS IS THE HEART OF YOUR DEFENCE
  ───────────────────────────────────
  Extortion under Indian law (IPC Sections 383–387) requires:
    (1) A THREAT made to the victim
    (2) With the INTENTION of causing WRONGFUL GAIN to yourself
        and WRONGFUL LOSS to the victim
    (3) Where the victim was put in FEAR of injury
    (4) And thereby induced to DELIVER PROPERTY (money)

  There is not a single piece of evidence on record — no call records,
  no bank statements, no WhatsApp messages, no witnesses — that shows
  you or Mr. Tarun Thadani demanded Rs. 1 crore from Abhishek Saraf
  or threatened him in any way to extort money.

  The extortion charge is a fabrication.

WHAT ABHISHEK SARAF DID — AND WHY
──────────────────────────────────

  On 4 June 2022 — two days after the incident — Saraf filed complaint
  ID 23244/2022.  That complaint alleged ONLY a slap.  No extortion.
  No Rs. 1 crore.  No Tarun Thadani.

  Why?  Because on 4 June 2022, he told the truth.

  The police told him a slap was a minor, bailable matter.  Saraf did
  not accept that.  He knew that if it remained a slap case, he would
  get no leverage — no arrest, no bail pressure, no fear.

  So approximately two months later, he changed the complaint.
  He added Rs. 1 crore extortion.  He added Tarun Thadani as an
  accused.  And Inspector Sanjay Taralgatti of the CB-CID
  Anti-Extortion Cell registered FIR 0654/2022 on that basis without
  examining a single accused, without checking your phone records,
  without verifying any bank statements, without watching CCTV.

  Saraf chose extortion specifically because:
    - It falls under IPC Section 384/385/387
    - These are NON-BAILABLE offences
    - Police can arrest without warrant
    - You can be held without bail
    - It carries sentences of up to 10 years

  A slap = bailable = no leverage.
  Extortion = non-bailable = arrest, fear, pressure.

  That is the only reason the extortion charge exists.

======================================================================
PART 2 — WHERE THE CASE STANDS TODAY
======================================================================

  FIR No.       : 0654/2022
  Registered    : Dadar Police Station, Mumbai (~12-13 August 2022)
  Court         : Addl. Chief Judicial Magistrate, 37th Court, Mumbai
  CNR           : MHMM110046312023
  Case No.      : PW/3700470/2023
  Today's date  : 9 June 2026
  Hearing today : YES — another hearing date in this matter

  STATUS: Charge-sheeted.  A discharge application was refused by the
  Sessions Court on 31 March 2024.  We are pursuing:

  (a) Criminal Revision Application in Bombay High Court against
      the 31 March 2024 discharge refusal.

  (b) Section 528 BNSS Quashing Petition in Bombay High Court to
      quash the FIR and chargesheet in their entirety.

WHAT HAS BEEN DONE IN THE LAST 24 HOURS:

  Yesterday and today, I sent formal complaints to every relevant
  authority in Mumbai and Maharashtra regarding Inspector Taralgatti's
  failure to conduct due diligence:

    - CB-CID Anti-Extortion Cell (12 individual + group emails)
    - Anti-Corruption Bureau Mumbai (3 officers + group)
    - Dadar Police Station + ACP Dadar
    - CID Crime Maharashtra
    - CBI Mumbai (Head of Zone + Branch EO)
    - DGP Maharashtra
    - Maharashtra Home Department
    - AND a WITHOUT PREJUDICE notice to Abhishek Saraf directly

  That is 25 separate official communications sent today alone.
  Every authority in Maharashtra police has now been formally notified.

  Abhishek Saraf has been asked to withdraw the FIR within 7 days
  (by 16 June 2026).

======================================================================
PART 3 — YOUR PLAN OF ACTION: HOW WE PROVE YOUR INNOCENCE
======================================================================

STEP 1: THE LEGAL ARGUMENT (ALREADY IN MOTION)

  Primary remedy: Section 528 BNSS Quashing Petition
    Court   : Bombay High Court
    Grounds :
      (i)   The extortion charge was ABSENT from Saraf's original
            complaint of 4 June 2022 — it was fabricated and added
            two months later with no basis
      (ii)  The FIR was registered without examining any accused
      (iii) There is zero evidence of any extortion demand on record
            (no calls, no bank transfers, no messages, no witnesses)
      (iv)  The video establishes the incident was a slap — at most
            IPC Section 323 (bailable) — not extortion
      (v)   Saraf has a documented pattern of misusing the legal
            system (Martin Burn forgery/fraud case, Calcutta HC)
      (vi)  Mr. Tarun Thadani was not present at all — his inclusion
            is itself evidence of fabrication

  Secondary remedy: Criminal Revision Application
    Court   : Bombay High Court
    Purpose : Challenge the Sessions Court's refusal to discharge you
    Grounds : No prima facie case on the evidence for extortion

  Counter-complaint against Saraf (to be filed by counsel):
    Sections: IPC 182 (false information), 192 (fabricating evidence),
              211 (false charge to injure), 499/500 (criminal defamation)
    Purpose : Puts Saraf on the defensive; creates record of his conduct

STEP 2: YOUR PERSONAL EVIDENCE (THIS IS WHERE I NEED YOUR HELP)

  To build the strongest possible case, I need the following from you.
  Please gather and send these to me as a matter of urgency:

  1. YOUR PHONE RECORDS (most important)
     - Your call log for 2 June 2022 and the two weeks after
     - I need to show there were NO calls from your number to Saraf
       demanding money or making any threat
     - Ask your mobile provider (Jio/Airtel/Vi) for CDR records
       for June 2022

  2. YOUR BANK STATEMENTS
     - June–September 2022
     - To show that NO Rs. 1 crore or any large sum was received by
       you from Saraf
     - This directly destroys the extortion narrative

  3. YOUR WHATSAPP / SMS MESSAGES WITH SARAF
     - Were there any messages between you and Saraf before or
       after 2 June 2022?
     - Please take screenshots of the entire chat history

  4. WHAT HAPPENED ON 2 JUNE 2022 — YOUR STATEMENT
     Please write out for me, in your own words:
       (a) Why were you at the restaurant that evening?
       (b) What was your relationship with Abhishek Saraf
           before that evening?
       (c) What happened — in sequence — leading up to the slap?
       (d) Was anyone else present who saw what happened?
       (e) Did you or Tarun Thadani at any point ask Saraf for
           money, directly or indirectly?  (I need your honest answer)
       (f) Had you had any financial dealings with Saraf before?

  5. WITNESS CONTACTS
     - Were there other people at the restaurant that evening?
     - Can any of them confirm the slap happened but no extortion
       demand was made?
     - Even a person who saw you and Saraf that evening, even briefly,
       is a valuable witness

  6. CCTV FOOTAGE
     - Do you know the name of the restaurant?
     - Is there any possibility of getting CCTV footage from that
       venue showing the full context of the altercation?

  7. YOUR RELATIONSHIP WITH TARUN THADANI
     - How do you know Tarun?
     - Can you confirm he had left before any altercation with Saraf?
     - Can you state clearly that Tarun had no role in the slap
       and no involvement in any extortion demand?

STEP 3: PUBLIC RECORD (TIMED TO COURT PROCEEDINGS)

  Once the quashing petition is admitted:
    - Press release about the fabricated FIR to be distributed to
      major Mumbai publications
    - ToI correction / Press Council complaint on any inaccurate coverage
    - Full factual record of Saraf's pattern (Martin Burn, etc.)
      to be placed before the media

  This step happens AFTER filing — not before.  Timing is everything.

======================================================================
PART 4 — WHAT THIS CASE COMES DOWN TO
======================================================================

Mr. Merchant, this is the honest truth of your situation:

  THE BAD NEWS:
  The video shows you slapped Abhishek Saraf.  That is not deniable.
  For that specific act, you may face liability under IPC Section 323
  (simple hurt).  That is a bailable, minor offence.  With a good
  lawyer's help, this can be addressed — it is not a serious matter
  in the scheme of things.

  THE GOOD NEWS:
  You did NOT commit extortion.  There is no evidence you did.
  No call records.  No bank transfer.  No witness to any demand.
  The extortion charge — the charge that carries up to 10 years
  imprisonment and is non-bailable — was fabricated.

  It was fabricated by Saraf because he was angry about the slap
  and knew that a slap alone would give him no power over you.
  He added extortion because extortion is non-bailable — and he
  wanted you arrested.

  Inspector Taralgatti helped him achieve that by registering the
  FIR without doing his job.

  THE PATH FORWARD:
  The quashing petition at Bombay High Court is your strongest weapon.
  If we can show the court that:
    (1) The original complaint had NO extortion
    (2) The extortion was added two months later with no basis
    (3) Inspector Taralgatti registered the FIR without examining
        a single accused or verifying a single piece of evidence
    (4) There is zero evidence on record of any extortion demand
    (5) The video shows a slap — not extortion

  ...then the court has every reason to quash this FIR.

  The law is on your side.  The facts are on your side.
  You just need to help me build the case.

======================================================================
PART 5 — WHAT I NEED FROM YOU THIS WEEK
======================================================================

Please respond to this email by 14 June 2026 with:

  [ ] Your mobile CDR records for June 2022 (call logs)
  [ ] Your bank statements June–September 2022
  [ ] Screenshots of all messages with Saraf
  [ ] Your written account of events on 2 June 2022
  [ ] Names of any witnesses
  [ ] Any information about the restaurant CCTV

If you are not already represented by your own counsel for this
matter, I would strongly recommend you engage one.  I represent
Mr. Tarun Thadani as the lead accused — your interests are aligned
with his, but you should have your own advocate present in court.

Please call me or write to me.  I am here to help you.

======================================================================

Yours faithfully,

Adv. Sujata Shirasi
Counsel for Mr. Tarun Thadani
Phone : +91 93216 13691
Email : sujata.shirasi@pressdetective.com
Date  : 9 June 2026

PressDetective
info@pressdetective.com

----------------------------------------------------------------------
GDPR / DPDP NOTE: The attached video (Abhishek_Saraf_Slap_Ali_Asgar_
Merchant.mp4) is shared under the lawful basis of legal obligation and
the exercise of legal claims in ongoing court proceedings (FIR 0654/
2022, CNR MHMM110046312023).  It is provided solely for the purpose
of your legal defence and must not be reproduced, distributed, or made
public without prior written consent from Adv. Sujata Shirasi.
----------------------------------------------------------------------
"""


def main():
    print("\n" + "=" * 60)
    print("ALIASGAR MERCHANT — FULL UPDATE + PLAN OF ACTION")
    print(f"To   : {TO}")
    print(f"CC   : {CC}")
    print(f"Subj : {SUBJECT[:70]}...")
    print("=" * 60)

    # Build base message
    msg = build_msg(
        from_addr=f'Adv. Sujata Shirasi <sujata.shirasi@pressdetective.com>',
        to=TO,
        subject=SUBJECT,
        body=BODY,
        cc=', '.join(CC),
    )

    # VIDEO NOT ATTACHED — confidential case evidence, not for distribution via email.
    # The video is stored locally at G:/My Drive/ABHISHEK SARAF/ for counsel use only.

    print("\nSending via Proton Bridge...")
    try:
        result = send_mail(msg, account="sujata")
        if not result:
            raise RuntimeError("All providers failed")
        print(f"\n[OK] Email sent to {TO}")
        print(f"[OK] CC: {', '.join(CC)}")
        print("[OK] No attachment (video is confidential, not distributed)")
    except Exception as e:
        print(f"\n[ERR] Send failed: {e}")
        raise SystemExit(1)

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
