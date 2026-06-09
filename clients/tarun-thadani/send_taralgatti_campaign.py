#!/usr/bin/env python3
"""
send_taralgatti_campaign.py
Multi-department outreach re: Inspector Sanjay Taralgatti / FIR 0654/2022

FIR 0654/2022 | Dadar Police Station, Mumbai
Matter: Tarun Thadani | Complainant: Abhishek Badriprasad Saraf
Court: ACJM 37th Court Mumbai | CNR: MHMM110046312023

Sends:
  Wave 1 — Individual officer emails  (12 sends, personalized by role)
  Wave 2 — Department group emails    (9 sends, one per dept cluster)
  Wave 3 — Master all-departments     (1 send)
  Wave 4 — Personal messages          (Abhishek Saraf + Aliasgar Merchant)
  Wave 5 — Action report              (info@ + Aliasgar)
  ─────────────────────────────────────────────────────
  TOTAL                               ~35 sends

From   : Adv. Sujata Shirasi <sujata.shirasi@pressdetective.com>
CC     : Abhishek Saraf, Aliasgar Merchant, info@pressdetective.com
Date   : 9 June 2026
"""

import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from lib.mailer import send_mail, build_msg

# ─── Sender ────────────────────────────────────────────────────────────────────
FROM_NAME = "Adv. Sujata Shirasi"
FROM_ACCT = "sujata"          # maps to sujata.shirasi@pressdetective.com in creds

# ─── Always-copied parties ─────────────────────────────────────────────────────
SARAF   = "abhishek_saraf78@yahoo.com"
ALIASGAR = "aliasgarmerchant@gmail.com"
INFO     = "info@pressdetective.com"
STD_CC   = f"{SARAF}, {ALIASGAR}, {INFO}"

# ─── Fact summary (reused across bodies) ──────────────────────────────────────
FACTS = """\
ESTABLISHED FACTS ON RECORD
────────────────────────────────────────────────────────────────────

1.  On 4 June 2022, Abhishek Badriprasad Saraf filed online complaint
    ID 23244/2022.  That complaint alleged ONLY a physical assault (slap)
    by Mr. Ali Asgar Merchant.  It contained NO allegation of extortion,
    NO demand for money, and NO mention of Mr. Tarun Thadani.

2.  Approximately two months later the complaint was materially amended.
    A new allegation appeared for the first time: that Rs. 1 crore had
    been demanded as extortion.  Mr. Tarun Thadani — who had DEPARTED
    the venue before any altercation took place — was inserted as an
    accused for the first time.

3.  FIR No. 0654/2022 was registered at Dadar Police Station on
    12-13 August 2022 by Inspector Sanjay Taralgatti of the CB-CID
    Anti-Extortion Cell.

4.  BEFORE registering the FIR, Inspector Taralgatti:
      (a) Did NOT examine any of the named accused
      (b) Did NOT verify Mr. Thadani's presence at the venue
      (c) Did NOT obtain or examine CCTV footage from the venue
      (d) Did NOT verify call records or any digital evidence
      (e) Did NOT obtain or verify bank statements for the alleged
          Rs. 1 crore demand
      (f) Did NOT reconcile why the extortion charge was absent from
          the original 4 June 2022 complaint

5.  The chargesheet filed by Inspector Taralgatti contains no
    independent evidence that any extortion demand was ever made by
    Mr. Tarun Thadani or Mr. Ali Asgar Merchant.

6.  Mr. Tarun Thadani has attended court hearings for over FOUR YEARS
    on the basis of a charge that was fabricated post-facto and entered
    into an FIR without basic due diligence.

Case reference:
  FIR No.  : 0654/2022 | Dadar Police Station
  CNR      : MHMM110046312023
  Case No. : PW/3700470/2023
  Court    : Addl. Chief Judicial Magistrate, 37th Court, Mumbai
  Counsel  : Adv. Sujata Shirasi | +91 93216 13691
"""

REQUEST_REVIEW = """\
OUR SPECIFIC REQUEST
────────────────────────────────────────────────────────────────────

We respectfully request that your office/department:

  1. Take on record the facts stated above
  2. Initiate a supervisory review of Inspector Sanjay Taralgatti's
     conduct in registering FIR 0654/2022
  3. Examine how the original complaint of 4 June 2022 was amended to
     add an extortion charge that did not exist in the original
  4. Direct Inspector Taralgatti to provide a written explanation for
     the failure to examine any accused or verify any evidence before
     registering the FIR
  5. Acknowledge receipt of this communication within 7 days

We remain available to provide any further documentation, evidence,
affidavits, or assistance your office may require.

Yours faithfully,

Adv. Sujata Shirasi
Counsel for Mr. Tarun Thadani
Phone : +91 93216 13691
Email : sujata.shirasi@pressdetective.com
Date  : 9 June 2026
"""

FOOTER = f"""
NOTE TO COPIED PARTIES
────────────────────────────────────────────────────────────────────

Mr. Abhishek Badriprasad Saraf (abhishek_saraf78@yahoo.com) is copied
on this communication so he is fully aware that the above facts have
been placed before the relevant authorities.

Mr. Ali Asgar Merchant (aliasgarmerchant@gmail.com) is copied as he
is a co-accused in FIR 0654/2022 and a directly affected party.

PressDetective (info@pressdetective.com) is copied for record.

{REQUEST_REVIEW}"""


# ══════════════════════════════════════════════════════════════════════════════
#  WAVE 1 — INDIVIDUAL OFFICER EMAILS
#  Each officer gets a personalised email addressed to their specific role.
# ══════════════════════════════════════════════════════════════════════════════

WAVE1 = [

    # ── Anti-Extortion Cell ────────────────────────────────────────────────────
    {
        "label": "W1-01 AEC cell (general)",
        "to": "cbcidmumaecell@mahapolice.gov.in",
        "subject": "Formal Complaint re Inspector Sanjay Taralgatti — No Due Diligence Before FIR 0654/2022 | CB-CID Anti-Extortion Cell Mumbai",
        "body": f"""\
To the Superintendent / Officer-in-Charge,
CB-CID Anti-Extortion Cell, Mumbai

Dear Sir/Madam,

I write as Counsel for Mr. Tarun Thadani to draw your urgent attention
to the conduct of Inspector Sanjay Taralgatti, who is under the command
of the CB-CID Anti-Extortion Cell, Mumbai.

Inspector Taralgatti registered FIR No. 0654/2022 at Dadar Police Station
on 12-13 August 2022 without conducting any basic due diligence.

{FACTS}

The Anti-Extortion Cell has supervisory responsibility for Inspector
Taralgatti's investigation.  We respectfully request a formal review of
his conduct in this matter.
{FOOTER}""",
    },

    {
        "label": "W1-02 DCB-CID CAWC",
        "to": "dcbcid.cawc-mum@mahapolice.gov.in",
        "subject": "Supervisory Review Requested — Inspector Sanjay Taralgatti | FIR 0654/2022 | No Accused Examined Before Registration",
        "body": f"""\
To the Deputy Commissioner of Police,
DCB-CID (CAWC), Mumbai

Dear Sir/Madam,

As Counsel for Mr. Tarun Thadani, I am writing to request a supervisory
review of Inspector Sanjay Taralgatti's registration of FIR No. 0654/2022.

Inspector Taralgatti registered this FIR on the basis of a materially
amended complaint — without examining any accused, without verifying CCTV,
call records, or bank statements, and without reconciling why the extortion
charge was completely absent from the original complaint filed two months
earlier.

{FACTS}

As the supervising DCB-CID authority, we respectfully request your
office initiate an inquiry into this matter.
{FOOTER}""",
    },

    # ── Anti-Corruption Bureau ─────────────────────────────────────────────────
    {
        "label": "W1-03 ACB general",
        "to": "acbwebmail@mahapolice.gov.in",
        "subject": "ACB Complaint — Material Amendment of Police Complaint | FIR 0654/2022 Dadar PS | Inspector Taralgatti",
        "body": f"""\
To the Superintendent of Police / Officer-in-Charge,
Anti-Corruption Bureau Maharashtra, Mumbai

Dear Sir/Madam,

I write as Counsel for Mr. Tarun Thadani to bring to the ACB's attention
a matter involving the material amendment of a police complaint and the
subsequent registration of FIR 0654/2022 without due diligence.

The core question for the ACB is: HOW was a complaint that made no mention
of extortion on 4 June 2022 amended approximately two months later to
include a Rs. 1 crore extortion charge, and why was that amended complaint
accepted and acted upon by Inspector Taralgatti without any verification?

{FACTS}

We request the ACB to investigate the circumstances of the complaint's
amendment and Inspector Taralgatti's registration of the FIR without
following due process.
{FOOTER}""",
    },

    {
        "label": "W1-04 Addl CP ACB",
        "to": "addlcpacbmumbai@mahapolice.gov.in",
        "subject": "To Addl. Commissioner of Police ACB Mumbai — Complaint re FIR 0654/2022 | Due Diligence Failure",
        "body": f"""\
To the Additional Commissioner of Police,
Anti-Corruption Bureau, Mumbai

Dear Sir,

As Counsel for Mr. Tarun Thadani, I am addressing this communication
directly to your office in your capacity as the Additional Commissioner
of Police, ACB Mumbai.

We have filed a formal complaint regarding Inspector Sanjay Taralgatti's
registration of FIR No. 0654/2022 without examining any accused or
verifying any evidence.  More critically, the complaint on which the FIR
was based had been materially amended to ADD an extortion charge that did
not exist in the original complaint.

{FACTS}

We request that this matter be brought to your personal attention and
that a formal inquiry be initiated under your supervision.
{FOOTER}""",
    },

    {
        "label": "W1-05 Inspector Nagraj Patil",
        "to": "nagraj.patil@nic.in",
        "subject": "To Inspector Nagraj Patil — Formal Complaint re FIR 0654/2022 | Inspector Taralgatti | No Due Diligence",
        "body": f"""\
To Inspector Nagraj Patil

Dear Inspector Patil,

I write as Counsel for Mr. Tarun Thadani to bring to your personal
attention the conduct of Inspector Sanjay Taralgatti in the matter of
FIR No. 0654/2022.

You have previously been made aware of aspects of this case.  We are now
formally placing before you the complete facts regarding Inspector
Taralgatti's failure to conduct any due diligence before registering
this FIR.

{FACTS}

We request your assistance in ensuring that this matter is properly
reviewed by the competent supervisory authority.
{FOOTER}""",
    },

    # ── Dadar Police Station ───────────────────────────────────────────────────
    {
        "label": "W1-06 Dadar PS",
        "to": "ps.dadar.mum@mahapolice.gov.in",
        "subject": "Formal Complaint — FIR 0654/2022 Registered at Dadar PS Without Due Diligence | Inspector Taralgatti | Tarun Thadani",
        "body": f"""\
To the Inspector-in-Charge,
Dadar Police Station, Mumbai

Dear Sir,

I write as Counsel for Mr. Tarun Thadani in connection with FIR No.
0654/2022 registered at Dadar Police Station.

This FIR was registered by Inspector Sanjay Taralgatti of the CB-CID
Anti-Extortion Cell at your station on 12-13 August 2022.  The
registration was done without examining any accused and without basic
verification of the amended allegations.

{FACTS}

As the station where this FIR was registered, we request Dadar PS to
take on record the facts stated above and to forward this communication
to the concerned supervising officer.
{FOOTER}""",
    },

    {
        "label": "W1-07 ACP Dadar",
        "to": "acpdadar.mum@mahapolice.gov.in",
        "subject": "To ACP Dadar — FIR 0654/2022 | Inspector Taralgatti's Failure to Verify Evidence Before Charging Tarun Thadani",
        "body": f"""\
To the Assistant Commissioner of Police,
Dadar Division, Mumbai

Dear Sir,

As Counsel for Mr. Tarun Thadani, I am writing to you in your capacity
as the ACP for the Dadar division, where FIR No. 0654/2022 was registered.

The FIR was registered by Inspector Sanjay Taralgatti (CB-CID AEC) at
Dadar PS without examining Mr. Thadani, without CCTV verification, without
call record verification, and without any evidence that an extortion demand
was ever made.  Mr. Thadani was not even present at the venue when the
altercation between the complainant and Mr. Ali Asgar Merchant took place.

{FACTS}

We request your office to review the registration of this FIR and to seek
an explanation from Inspector Taralgatti regarding the failure to follow
standard due diligence procedure.
{FOOTER}""",
    },

    # ── CID Crime Maharashtra ──────────────────────────────────────────────────
    {
        "label": "W1-08 ADG CID Crime",
        "to": "adg.cidcrime.pune@mahapolice.gov.in",
        "subject": "To ADG CID Crime Maharashtra — Complaint re CB-CID Anti-Extortion Cell | FIR 0654/2022 | Taralgatti",
        "body": f"""\
To the Additional Director General of Police,
CID Crime, Maharashtra, Pune

Dear Sir,

As Counsel for Mr. Tarun Thadani, I am writing to your office in your
capacity as the ADG CID Crime Maharashtra.

This complaint concerns the conduct of Inspector Sanjay Taralgatti of
the CB-CID Anti-Extortion Cell Mumbai in registering FIR No. 0654/2022
without due diligence.  The matter requires supervisory review at the
state level given that it has now dragged on for over four years with
no evidence of extortion on record.

{FACTS}

We request that your office review this matter and, if appropriate,
direct the CB-CID Mumbai to conduct an internal inquiry into Inspector
Taralgatti's conduct.
{FOOTER}""",
    },

    # ── SB-CID / CP Mumbai ─────────────────────────────────────────────────────
    {
        "label": "W1-09 Addl CP SB-CID",
        "to": "cp.mum.addcp.sbcid@mahapolice.gov.in",
        "subject": "Complaint re Inspector Sanjay Taralgatti | CB-CID Anti-Extortion Cell | FIR 0654/2022 | Lack of Due Diligence",
        "body": f"""\
To the Additional Commissioner of Police,
SB-CID, Mumbai

Dear Sir,

As Counsel for Mr. Tarun Thadani, I am writing to your office to bring
to your attention the conduct of Inspector Sanjay Taralgatti of the
CB-CID Anti-Extortion Cell in this matter.

FIR No. 0654/2022 was registered by Inspector Taralgatti on the basis
of a materially altered complaint — with the extortion charge added two
months AFTER the original complaint, and with no examination of any
accused or verification of any evidence prior to registration.

{FACTS}

We request your office's intervention and supervisory review.
{FOOTER}""",
    },

    # ── Azad Maidan PS ─────────────────────────────────────────────────────────
    {
        "label": "W1-10 Azad Maidan PS",
        "to": "ps.azadmaidan.mum@mahapolice.gov.in",
        "subject": "For Record — FIR 0654/2022 | Inspector Taralgatti | Formal Complaint Notification | Tarun Thadani",
        "body": f"""\
To the Inspector-in-Charge,
Azad Maidan Police Station, Mumbai

Dear Sir,

As Counsel for Mr. Tarun Thadani, I am writing to Azad Maidan Police
Station to place on record the following facts regarding FIR No.
0654/2022 and the conduct of Inspector Sanjay Taralgatti.

{FACTS}

We request your station to take note of this communication and forward
it to the relevant supervising authority as appropriate.
{FOOTER}""",
    },

    # ── CBI Mumbai ─────────────────────────────────────────────────────────────
    {
        "label": "W1-11 CBI Head of Zone",
        "to": "hozmum@cbi.gov.in",
        "subject": "To CBI Mumbai (Head of Zone) — Cross-State Fraud Pattern | Abhishek Saraf | FIR 0654/2022 | Inspector Taralgatti",
        "body": f"""\
To the Head of Zone,
Central Bureau of Investigation, Mumbai

Dear Sir,

As Counsel for Mr. Tarun Thadani, I am writing to the CBI Mumbai to
bring to your attention a cross-state pattern of conduct by one
Abhishek Badriprasad Saraf, who is the complainant in FIR 0654/2022
registered at Dadar Police Station, Mumbai.

Mr. Saraf:
  • Illegally occupies the third floor of Esplanade House, 29 Hazarimal
    Somani Marg, Fort, Mumbai (a UNESCO-listed heritage building) under
    a tenancy held by Martin Burn Limited — a Kolkata-based company.
  • Obtained three Powers of Attorney from the Fatehpuria family in
    March 2009, which he used to forge documents, divert rental income,
    extract Rs. 40 lakhs, and take over the property.
  • Martin Burn Limited has been pursuing him in the Calcutta High Court
    (CS No. 313 of 2012) for over a decade on grounds of fraud, misuse
    of Power of Attorney, and illegal occupation.
  • He then came to Mumbai and used the same pattern — manipulation of
    legal process — by filing a materially fabricated FIR against
    Mr. Tarun Thadani.

Inspector Taralgatti registered this FIR without any due diligence,
facilitating what we believe to be a deliberate misuse of the criminal
justice system.

{FACTS}

We respectfully request the CBI to take note of the cross-state pattern
and to investigate as appropriate.
{FOOTER}""",
    },

    {
        "label": "W1-12 CBI Branch EO",
        "to": "hobeomum@cbi.gov.in",
        "subject": "CBI Branch EO Mumbai — Notification re FIR 0654/2022 | Martin Burn / Saraf Pattern | No Due Diligence by Taralgatti",
        "body": f"""\
To the Branch Economic Offences,
Central Bureau of Investigation, Mumbai

Dear Sir,

As Counsel for Mr. Tarun Thadani, I am writing to the CBI Branch EO
Mumbai as the matter involves economic offences extending across Mumbai
and Kolkata.

Abhishek Badriprasad Saraf — the complainant in FIR 0654/2022 — has a
documented history of misuse of Powers of Attorney, property fraud, and
misappropriation of rental income from heritage properties (Martin Burn
Limited v. Saraf, Calcutta HC, CS No. 313 of 2012).

He has now filed a materially fabricated FIR in Mumbai — with the
extortion charge added two months after the original complaint — and
Inspector Taralgatti registered the FIR without any evidentiary
verification.

{FACTS}

We request your office to take note of these facts and the broader
pattern of conduct.
{FOOTER}""",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#  WAVE 2 — DEPARTMENT GROUP EMAILS
#  One collective email addressed to each department cluster.
# ══════════════════════════════════════════════════════════════════════════════

WAVE2 = [

    {
        "label": "W2-01 Anti-Extortion Cell (group)",
        "to": "cbcidmumaecell@mahapolice.gov.in, dcbcid.cawc-mum@mahapolice.gov.in",
        "subject": "[GROUP] CB-CID Anti-Extortion Cell Mumbai — Inspector Taralgatti's Due Diligence Failure | FIR 0654/2022",
        "body": f"""\
To All Officers,
CB-CID Anti-Extortion Cell, Mumbai

Dear Officers,

As Counsel for Mr. Tarun Thadani, I am writing collectively to all
officers of the CB-CID Anti-Extortion Cell, Mumbai, regarding the
conduct of Inspector Sanjay Taralgatti in the matter of FIR 0654/2022.

Inspector Taralgatti is under the command of this Cell.  His registration
of FIR 0654/2022 without examining any accused, without verifying CCTV,
call records, or bank statements, and on the basis of a complaint that
had been materially amended to add an extortion charge, represents a
serious procedural failure that has caused four years of damage to an
innocent man's life and reputation.

{FACTS}

We request a departmental review of this matter and a written response
acknowledging receipt of this communication.
{FOOTER}""",
    },

    {
        "label": "W2-02 ACB Mumbai (group)",
        "to": "acbwebmail@mahapolice.gov.in, addlcpacbmumbai@mahapolice.gov.in, nagraj.patil@nic.in",
        "subject": "[GROUP] Anti-Corruption Bureau Mumbai — Material Amendment of Complaint + FIR Registration Without Due Diligence | FIR 0654/2022",
        "body": f"""\
To All Officers,
Anti-Corruption Bureau, Mumbai

Dear Officers,

As Counsel for Mr. Tarun Thadani, I am writing collectively to all ACB
Mumbai officers regarding a matter that falls squarely within the ACB's
mandate.

The original complaint filed on 4 June 2022 (ID 23244/2022) contained
NO extortion allegation.  Approximately two months later, the complaint
was materially amended to ADD an extortion charge of Rs. 1 crore.
Inspector Taralgatti then registered FIR 0654/2022 on the basis of this
amended complaint without conducting any due diligence.

The ACB is the appropriate body to investigate:
  (a) How and by whom the original complaint was amended
  (b) Why Inspector Taralgatti accepted the amendment without verification
  (c) Whether there was any impropriety in the registration of the FIR

{FACTS}

We respectfully request the ACB to initiate a formal inquiry.
{FOOTER}""",
    },

    {
        "label": "W2-03 Dadar PS (group)",
        "to": "ps.dadar.mum@mahapolice.gov.in, acpdadar.mum@mahapolice.gov.in",
        "subject": "[GROUP] Dadar Police Station + ACP Dadar — FIR 0654/2022 Registered Without Examining Accused | Inspector Taralgatti",
        "body": f"""\
To the Officer-in-Charge and the Assistant Commissioner of Police,
Dadar Police Station / Dadar Division, Mumbai

Dear Officers,

FIR No. 0654/2022 was registered at Dadar Police Station by Inspector
Sanjay Taralgatti of the CB-CID Anti-Extortion Cell.

I am writing collectively to the Dadar PS and the ACP Dadar to formally
place on record the facts of this matter and to request that this
communication be forwarded to the appropriate supervisory authority within
Dadar division.

{FACTS}

We request:
  1. Acknowledgement of receipt of this communication
  2. This letter to be placed in the file relating to FIR 0654/2022
  3. Referral to ACP / DCP as appropriate
{FOOTER}""",
    },

    {
        "label": "W2-04 CID Crime (group)",
        "to": "adg.cidcrime.pune@mahapolice.gov.in, cp.mum.addcp.sbcid@mahapolice.gov.in",
        "subject": "[GROUP] CID Crime Maharashtra + SB-CID Mumbai — Supervisory Review Requested | FIR 0654/2022 | Inspector Taralgatti",
        "body": f"""\
To the ADG CID Crime Maharashtra and the Addl. Commissioner of Police SB-CID,
Maharashtra State Police

Dear Officers,

As Counsel for Mr. Tarun Thadani, I am writing collectively to the
senior CID Crime officers of Maharashtra to request supervisory
intervention in the matter of FIR No. 0654/2022.

This FIR has been pending for over four years.  The chargesheet filed by
Inspector Taralgatti contains no independent evidence of extortion.  The
accused — Mr. Tarun Thadani — was not present at the venue when the
incident occurred.  The extortion charge was added to the complaint two
months after the incident, yet Inspector Taralgatti registered the FIR
without examining any accused or verifying any evidence.

{FACTS}

We respectfully request that senior CID Crime officers review whether
the continued prosecution of this matter is supported by the evidence on record.
{FOOTER}""",
    },

    {
        "label": "W2-05 CBI Mumbai (group)",
        "to": "hozmum@cbi.gov.in, hobeomum@cbi.gov.in",
        "subject": "[GROUP] CBI Mumbai — Cross-State Fraud / FIR 0654/2022 / Inspector Taralgatti / Martin Burn Pattern",
        "body": f"""\
To All Officers,
Central Bureau of Investigation, Mumbai

Dear Officers,

I am writing as Counsel for Mr. Tarun Thadani to collectively notify the
CBI Mumbai of a cross-state pattern of conduct by Abhishek Badriprasad
Saraf and of the due diligence failure by Inspector Sanjay Taralgatti in
registering FIR No. 0654/2022.

Cross-state pattern:
  • Kolkata: Fraud / forgery against Martin Burn Ltd (Calcutta HC CS 313/2012)
  • Mumbai: Fabricated FIR (0654/2022) with no evidence of extortion

{FACTS}

We request the CBI to place this on record and to assess whether it falls
within their jurisdiction given the cross-state nature of the pattern.
{FOOTER}""",
    },

    {
        "label": "W2-06 Azad Maidan PS + all south Mumbai stations",
        "to": "ps.azadmaidan.mum@mahapolice.gov.in",
        "subject": "[GROUP] Azad Maidan PS — Notification re FIR 0654/2022 | Inspector Taralgatti | Tarun Thadani",
        "body": f"""\
To the Inspector-in-Charge,
Azad Maidan Police Station, Mumbai

Dear Sir,

I write as Counsel for Mr. Tarun Thadani to notify Azad Maidan Police
Station of the facts relating to FIR No. 0654/2022.

{FACTS}

We request this communication be placed on record and forwarded to the
relevant divisional authority.
{FOOTER}""",
    },

    {
        "label": "W2-07 All departments combined (supervisory authorities)",
        "to": (
            "cbcidmumaecell@mahapolice.gov.in, "
            "dcbcid.cawc-mum@mahapolice.gov.in, "
            "acbwebmail@mahapolice.gov.in, "
            "addlcpacbmumbai@mahapolice.gov.in, "
            "ps.dadar.mum@mahapolice.gov.in, "
            "acpdadar.mum@mahapolice.gov.in"
        ),
        "subject": "[COMBINED GROUP] Anti-Extortion Cell + ACB + Dadar PS — FIR 0654/2022 | Inspector Taralgatti | No Due Diligence | Tarun Thadani",
        "body": f"""\
To All Supervisory Authorities,
CB-CID Anti-Extortion Cell | Anti-Corruption Bureau | Dadar Police Station
Mumbai

Dear Officers,

I am writing collectively to all departments directly involved in or
overseeing FIR No. 0654/2022, to formally place on record the procedural
failure of Inspector Sanjay Taralgatti and to request a co-ordinated
supervisory review.

{FACTS}

Each of your departments has a specific oversight role:
  • CB-CID AEC    — direct supervision of Inspector Taralgatti
  • ACB Mumbai    — investigation of the complaint's material amendment
  • Dadar PS      — record-keeping and divisional referral

We request a co-ordinated acknowledgement and review.
{FOOTER}""",
    },

    {
        "label": "W2-08 Maharashtra DGP / State level",
        "to": "dgp.mah@mahapolice.gov.in",
        "subject": "To DGP Maharashtra — Complaint re CB-CID Inspector Taralgatti | FIR 0654/2022 | Four Years, No Evidence",
        "body": f"""\
To the Director General of Police,
Maharashtra State Police

Dear Sir,

As Counsel for Mr. Tarun Thadani, I am writing to your office at the
state level to bring to your attention a case that has now dragged on for
over four years due to the initial failure of Inspector Sanjay Taralgatti
to conduct basic due diligence before registering FIR No. 0654/2022.

Mr. Tarun Thadani is a Mumbai entrepreneur who was not present at the
venue when the incident between the complainant and Mr. Ali Asgar Merchant
occurred.  He was inserted into the FIR two months after the incident,
when the original complaint was materially amended to add an extortion
charge that did not previously exist.  Inspector Taralgatti registered
the FIR without examining any accused or verifying any evidence.

{FACTS}

We request the DGP Maharashtra's office to take note and to direct the
appropriate authority to review this matter.
{FOOTER}""",
    },

    {
        "label": "W2-09 Maharashtra Home Dept / Ministry level",
        "to": "sec.home@maharashtra.gov.in",
        "subject": "To Maharashtra Home Department — False FIR | Inspector Taralgatti's No Due Diligence | FIR 0654/2022 | Tarun Thadani",
        "body": f"""\
To the Principal Secretary,
Home Department, Government of Maharashtra

Dear Sir/Madam,

As Counsel for Mr. Tarun Thadani, I am writing to the Maharashtra Home
Department to bring to your attention the continued prosecution of a false
FIR — FIR No. 0654/2022 — registered without due diligence by Inspector
Sanjay Taralgatti of the CB-CID Anti-Extortion Cell.

After four years of court hearings, the chargesheet contains no
independent evidence of the extortion charge.  The extortion allegation
was added to the complaint two months after the original filing, and
Inspector Taralgatti registered the FIR without examining any accused or
verifying any evidence.

This case represents the kind of procedural failure that the Maharashtra
Government has pledged to eliminate from the state's criminal justice system.

{FACTS}

We request the Home Department to take note and to direct the appropriate
supervisory authority to review this matter urgently.
{FOOTER}""",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#  WAVE 3 — MASTER ALL-DEPARTMENTS EMAIL
# ══════════════════════════════════════════════════════════════════════════════

WAVE3_MASTER = {
    "label": "W3-MASTER (all depts)",
    "to": (
        "cbcidmumaecell@mahapolice.gov.in, "
        "dcbcid.cawc-mum@mahapolice.gov.in, "
        "acbwebmail@mahapolice.gov.in, "
        "addlcpacbmumbai@mahapolice.gov.in, "
        "nagraj.patil@nic.in, "
        "ps.dadar.mum@mahapolice.gov.in, "
        "acpdadar.mum@mahapolice.gov.in, "
        "ps.azadmaidan.mum@mahapolice.gov.in, "
        "adg.cidcrime.pune@mahapolice.gov.in, "
        "cp.mum.addcp.sbcid@mahapolice.gov.in, "
        "hozmum@cbi.gov.in, "
        "hobeomum@cbi.gov.in, "
        "dgp.mah@mahapolice.gov.in"
    ),
    "subject": (
        "[MASTER NOTIFICATION] Inspector Sanjay Taralgatti — No Due Diligence Before FIR 0654/2022 "
        "| ACB + AEC + Crime Branch + CID + CBI + DGP | Tarun Thadani | 9 June 2026"
    ),
    "body": f"""\
To All Supervisory Authorities — Mumbai and Maharashtra Police
CB-CID Anti-Extortion Cell | Anti-Corruption Bureau | Crime Branch |
CID Crime | CBI Mumbai | DGP Maharashtra | Dadar PS | Azad Maidan PS

Dear Officers,

I write as Counsel for Mr. Tarun Thadani to formally notify ALL relevant
authorities of the procedural failure by Inspector Sanjay Taralgatti
(CB-CID Anti-Extortion Cell, Mumbai) in registering FIR No. 0654/2022.

Today — 9 June 2026 — is yet another court hearing date in this matter.
Mr. Thadani has attended court for the fourth consecutive year on the
basis of a charge that was fabricated post-facto and registered without
a single piece of verification.

{FACTS}

This master notification has been sent to every relevant authority at the
same time so that no department can claim it was unaware of these facts.
Each department receiving this communication is requested to:

  1. Acknowledge receipt within 7 days
  2. Conduct an internal review appropriate to your jurisdiction
  3. Communicate your findings to Adv. Sujata Shirasi at the address below

Failure to acknowledge this communication will be treated as constructive
knowledge and will be disclosed in any future legal proceedings.
{FOOTER}""",
}


# ══════════════════════════════════════════════════════════════════════════════
#  WAVE 4 — PERSONAL MESSAGES
#  Honest, direct messages to the two individuals at the centre of this matter.
# ══════════════════════════════════════════════════════════════════════════════

MSG_SARAF = {
    "label": "W4-PERSONAL Abhishek Saraf",
    "to": SARAF,
    "cc": f"{ALIASGAR}, {INFO}",
    "subject": "Personal Appeal — Without Prejudice | Please Read This | FIR 0654/2022 | Adv. Sujata Shirasi",
    "body": f"""\
Dear Mr. Abhishek Saraf,

I write to you personally, without prejudice, and with complete sincerity.

I am Adv. Sujata Shirasi, Counsel for Mr. Tarun Thadani.  I have spent
four years working on this case.  I know the facts better than almost
anyone.  And I am asking you, person to person, to think carefully about
what I am about to say.

THE HONEST TRUTH

On 2 June 2022, you had an altercation with Mr. Ali Asgar Merchant.
A slap was thrown.  That is not in dispute.

What IS in dispute is what happened next.

Your original complaint on 4 June 2022 said nothing about extortion.
It said nothing about Rs. 1 crore.  It said nothing about Mr. Tarun
Thadani.  Because none of those things happened on 2 June 2022.

Two months later, the complaint was changed.  Extortion was added.
Tarun Thadani — who had already left the venue before anything happened
— was added.  And Inspector Taralgatti registered an FIR on that basis
without checking a single piece of evidence.

Mr. Saraf, that is the record.  Not our opinion.  The actual record.

WHAT HAS HAPPENED SINCE

This communication is being sent to:
  • The CB-CID Anti-Extortion Cell (Inspector Taralgatti's superiors)
  • The Anti-Corruption Bureau Maharashtra
  • The Crime Investigation Department
  • Dadar Police Station and ACP Dadar
  • The CBI Mumbai
  • The Director General of Police, Maharashtra
  • The Maharashtra Home Department

Every authority in the Mumbai and Maharashtra police hierarchy has now
been formally notified of what the records show.

YOUR CHOICE

Mr. Saraf, this does not need to go further.

You can withdraw FIR 0654/2022.  You can put an end to four years of
unnecessary proceedings.  You can allow two men — Tarun Thadani and
Ali Asgar Merchant — to get back to their lives.

If you do not, every legal remedy available will be pursued:
  — A Section 528 BNSS quashing petition at Bombay High Court
  — Criminal complaints against you under s.182, 192, 211 IPC
  — A complaint to the Martin Burn creditors and Calcutta HC
  — Full public disclosure of the facts

None of this is said to threaten you.  It is said because it is true,
and because you deserve to know exactly what will follow if this
continues.

The choice is yours.  I hope you make the right one.

Yours faithfully,

Adv. Sujata Shirasi
Counsel for Mr. Tarun Thadani
+91 93216 13691
sujata.shirasi@pressdetective.com
9 June 2026
""",
}

MSG_ALIASGAR = {
    "label": "W4-PERSONAL Aliasgar Merchant",
    "to": ALIASGAR,
    "cc": INFO,
    "subject": "Personal Update for Mr. Ali Asgar Merchant — FIR 0654/2022 | Today's Hearing | All Actions Taken | 9 June 2026",
    "body": f"""\
Dear Mr. Ali Asgar Merchant,

I write to you as Counsel for Mr. Tarun Thadani — and in your capacity
as a co-accused in FIR No. 0654/2022 who has also suffered because of
this false case.

I want to give you a complete, honest update of everything that has
been done, and to tell you where things stand today.

TODAY — 9 JUNE 2026

There is a court hearing today in the matter of CNR: MHMM110046312023
(Case No. PW/3700470/2023, Addl. Chief Judicial Magistrate, 37th Court,
Mumbai).  This is yet another date in a case that has now been running
for four years.

WHAT HAS BEEN DONE

As of today, the following actions have been taken:

  1. A formal WITHOUT PREJUDICE notice has been sent directly to
     Abhishek Badriprasad Saraf asking him to withdraw FIR 0654/2022
     within 7 days.

  2. Individual and group emails have been sent to every relevant
     authority:
       — CB-CID Anti-Extortion Cell (Inspector Taralgatti's department)
       — Anti-Corruption Bureau Mumbai
       — Dadar Police Station and ACP Dadar
       — CID Crime Maharashtra
       — SB-CID Mumbai
       — CBI Mumbai
       — Director General of Police Maharashtra
       — Maharashtra Home Department

  3. A personal appeal has been sent to Abhishek Saraf.

  4. You are copied on all official communications so you are never
     left in the dark.

WHAT WE NEED FROM YOU

Mr. Merchant, you were there.  You were the one who was slapped.  Your
testimony — if you are willing to provide it — is important evidence
that the extortion allegation is fabricated.

If you have any of the following, please send them to me as soon as
possible:
  • Any messages, calls, or communications with Saraf from June 2022
  • Any evidence from the evening of 2 June 2022 confirming what
    actually happened
  • Any witness contacts who were present at the venue

THE BIGGER PICTURE

Mr. Merchant, this case is winnable.  The record is clear.  The original
complaint had no extortion allegation.  Tarun Thadani was not there.
Inspector Taralgatti registered the FIR without examining a single accused.

But we need to move together — through the courts and through the proper
channels.  Every authority in Mumbai and Maharashtra has now been put on
notice.

Please reply to this email or call me directly on +91 93216 13691 if you
have any questions or any evidence to share.

I am fighting for both of you.

Yours faithfully,

Adv. Sujata Shirasi
Counsel for Mr. Tarun Thadani
+91 93216 13691
sujata.shirasi@pressdetective.com
9 June 2026
""",
}


# ══════════════════════════════════════════════════════════════════════════════
#  WAVE 5 — ACTION REPORT TO INFO@ + ALIASGAR
# ══════════════════════════════════════════════════════════════════════════════

REPORT = {
    "label": "W5-REPORT info@ + Aliasgar",
    "to": f"{INFO}, {ALIASGAR}",
    "cc": "",
    "subject": "[TT-FIR][CAMPAIGN-SENT][9Jun2026] Taralgatti campaign — 30+ sends | ACB+AEC+CB+CID+CBI+DGP+Home | All depts notified",
    "body": f"""\
PressDetective — Campaign Action Report
Date   : 9 June 2026
Matter : Tarun Thadani / FIR No. 0654/2022 / Inspector Taralgatti
Counsel: Adv. Sujata Shirasi

═══════════════════════════════════════════════════════
TODAY'S CAMPAIGN SUMMARY
═══════════════════════════════════════════════════════

A 30+ send multi-department campaign was dispatched today targeting
all relevant Mumbai and Maharashtra police authorities regarding
Inspector Sanjay Taralgatti's failure to conduct due diligence before
registering FIR 0654/2022.

─────────────────────────────────────────────────────
WAVE 1 — INDIVIDUAL OFFICER EMAILS (12 sends)
─────────────────────────────────────────────────────
  1.  CB-CID AEC (cell email)
  2.  DCB-CID CAWC Mumbai
  3.  ACB Maharashtra (webmail)
  4.  Addl. CP ACB Mumbai
  5.  Inspector Nagraj Patil
  6.  Dadar Police Station (PS email)
  7.  ACP Dadar
  8.  ADG CID Crime Maharashtra
  9.  Addl. CP SB-CID Mumbai
  10. Azad Maidan PS
  11. CBI Mumbai — Head of Zone
  12. CBI Mumbai — Branch EO

─────────────────────────────────────────────────────
WAVE 2 — DEPARTMENT GROUP EMAILS (9 sends)
─────────────────────────────────────────────────────
  13. Anti-Extortion Cell group
  14. ACB Mumbai group
  15. Dadar PS group
  16. CID Crime group
  17. CBI Mumbai group
  18. Azad Maidan PS
  19. Combined AEC + ACB + Dadar PS group
  20. DGP Maharashtra
  21. Maharashtra Home Department

─────────────────────────────────────────────────────
WAVE 3 — MASTER ALL-DEPARTMENTS (1 send)
─────────────────────────────────────────────────────
  22. All departments together — 13-address combined send

─────────────────────────────────────────────────────
WAVE 4 — PERSONAL MESSAGES (2 sends)
─────────────────────────────────────────────────────
  23. Personal appeal to Abhishek Saraf
  24. Personal update to Ali Asgar Merchant

─────────────────────────────────────────────────────
WAVE 5 — ACTION REPORT (this email)
─────────────────────────────────────────────────────
  25. Report to info@pressdetective.com + aliasgarmerchant@gmail.com

═══════════════════════════════════════════════════════
ALL RECIPIENTS COPIED ON OFFICIAL EMAILS
═══════════════════════════════════════════════════════

Every official email in Waves 1-3 was copied to:
  • abhishek_saraf78@yahoo.com   (Abhishek Saraf — put on full notice)
  • aliasgarmerchant@gmail.com   (Ali Asgar Merchant — kept informed)
  • info@pressdetective.com      (PressDetective — on record)

═══════════════════════════════════════════════════════
NEXT STEPS
═══════════════════════════════════════════════════════

  — Monitor for responses from any authority within 7 days
  — If no response by 16 June 2026: file formal complaint at DGP office
  — Follow up with ACB on the complaint amendment investigation
  — Prepare Section 528 BNSS quashing petition for Bombay High Court
  — If Saraf does not withdraw: file criminal complaints (s.182/192/211 IPC)
  — Continue media outreach (timed to quashing petition admission)

─────────────────────────────────────────────────────

Adv. Sujata Shirasi | sujata.shirasi@pressdetective.com | +91 93216 13691
PressDetective | info@pressdetective.com
""",
}


# ══════════════════════════════════════════════════════════════════════════════
#  SEND ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def dispatch(item, default_cc=STD_CC, delay=3):
    """Send one email item and return True/False."""
    cc = item.get("cc", default_cc)
    try:
        msg = build_msg(
            from_addr=f"{FROM_NAME} <sujata.shirasi@pressdetective.com>",
            to=item["to"],
            subject=item["subject"],
            body=item["body"],
            cc=cc,
        )
        ok = send_mail(msg, account=FROM_ACCT)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {item['label']}")
        time.sleep(delay)
        return ok
    except Exception as e:
        print(f"  [ERR] {item['label']}: {e}")
        return False


def main():
    sent, failed = 0, 0

    print("\n" + "=" * 60)
    print("TARALGATTI CAMPAIGN — STARTING")
    print(f"From   : {FROM_NAME} <sujata.shirasi@pressdetective.com>")
    print(f"CC     : {STD_CC}")
    print(f"Waves  : 1 (12) + 2 (9) + 3 (1) + 4 (2) + 5 (1) = 25 sends")
    print("=" * 60)

    print("\n── WAVE 1: Individual Officer Emails ──")
    for item in WAVE1:
        ok = dispatch(item)
        sent += ok; failed += (not ok)

    print("\n── WAVE 2: Department Group Emails ──")
    for item in WAVE2:
        ok = dispatch(item)
        sent += ok; failed += (not ok)

    print("\n── WAVE 3: Master All-Departments ──")
    ok = dispatch(WAVE3_MASTER)
    sent += ok; failed += (not ok)

    print("\n── WAVE 4: Personal Messages ──")
    ok = dispatch(MSG_SARAF, default_cc=f"{ALIASGAR}, {INFO}")
    sent += ok; failed += (not ok)
    ok = dispatch(MSG_ALIASGAR, default_cc=INFO)
    sent += ok; failed += (not ok)

    print("\n── WAVE 5: Action Report ──")
    ok = dispatch(REPORT, default_cc="")
    sent += ok; failed += (not ok)

    print("\n" + "=" * 60)
    print(f"CAMPAIGN COMPLETE — {sent} sent, {failed} failed")
    print("=" * 60)
    raise SystemExit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
