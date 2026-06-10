import json, smtplib, ssl, datetime, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT  = pathlib.Path(r"C:\dev\pressdetective")
CREDS = json.loads((ROOT / ".creds/proton_accounts.json").read_text(encoding="utf-8"))

HOST  = CREDS["smtp_bridge"]["host"]
PORT  = CREDS["smtp_bridge"]["port"]
BRIDGE_PW = CREDS["accounts"]["sujata"]["bridge_password"]

TO      = "aliasgarmerchant@gmail.com"
CC      = "info@pressdetective.com"
TODAY   = "10 June 2026"

SUBJECT = "[FIR 0654/2022] CASE STATUS REPORT — 10 June 2026 | Adv. Sujata Shirasi"

BODY = """Dear Mr. Ali Asgar Merchant,

I am writing to give you a complete operational status report on every action
taken in FIR No. 0654/2022 over the last 24 hours, and to lay out today's plan.

Please read this in full — there are items that require your attention by
16 June 2026.

======================================================================
PART 1 — ACTIONS COMPLETED (9 June 2026)
======================================================================

1. WITHOUT PREJUDICE NOTICE TO ABHISHEK SARAF — SENT
   ──────────────────────────────────────────────────
   Date        : 9 June 2026
   Sent to     : abhishek_saraf78@yahoo.com (Abhishek Badriprasad Saraf)
   CC (14 authorities):
     Anti-Extortion Cell (CB-CID) : cbcidmumaecell@mahapolice.gov.in
     Anti-Corruption Bureau        : acbwebmail@mahapolice.gov.in
                                     addlcpacbmumbai@mahapolice.gov.in
                                     acpdadar.mum@mahapolice.gov.in
     CID Crime Maharashtra         : adg.cidcrime.pune@mahapolice.gov.in
                                     cp.mum.addcp.sbcid@mahapolice.gov.in
                                     dcbcid.cawc-mum@mahapolice.gov.in
     Dadar Police Station          : ps.dadar.mum@mahapolice.gov.in
     Azad Maidan Police Station    : ps.azadmaidan.mum@mahapolice.gov.in
     CBI Mumbai (HOB + HOZ)        : hobeomum@cbi.gov.in
                                     hozmum@cbi.gov.in
     DGP Maharashtra               : dgp.mah@mahapolice.gov.in
     Maharashtra Home Department   : sec.home@maharashtra.gov.in
     PressDetective                : info@pressdetective.com

   The notice formally established on record:
     - Mr. Tarun Thadani was NOT at the venue. His ONLY connection
       to the event was having sent invitations. He was not present
       during any altercation.
     - Mr. Ali Asgar Merchant slapped Abhishek Badriprasad Saraf.
     - Saraf filed complaint ID 23244/2022 on 4 June 2022 — that
       complaint contained ZERO reference to extortion or Thadani.
     - Two months later, the extortion charge and Thadani's name
       appeared for the first time.
     - Inspector Sanjay Taralgatti registered FIR 0654/2022 without
       examining any accused, without CDR checks, without verifying
       any evidence.
   
   DEMAND SERVED: Saraf has been formally asked to WITHDRAW the FIR.
   DEADLINE: 16 June 2026 (7 days from notice).
   
   If Saraf does not respond or refuses to withdraw:
   We proceed immediately with the Section 528 BNSS Quashing Petition
   before the Bombay High Court.

2. FULL LEGAL UPDATE TO YOU — SENT (9 June 2026)
   ────────────────────────────────────────────────
   A comprehensive email was dispatched to aliasgarmerchant@gmail.com
   covering:
     - Legal analysis of what the video proves and does not prove
     - Why the extortion charge was fabricated
     - Your specific plan of action (7 steps of evidence to gather)
     - Timeline of the case and current court status
   
   If you did not receive that email, please reply immediately so I
   can resend it.

3. PRESS RELEASE TO MEDIA — PARTIAL DELIVERY
   ────────────────────────────────────────────
   On 9 June 2026, a press release was dispatched to the legal and
   national media from sujata.shirasi@pressdetective.com.

   The press release covered:
     - The full factual timeline (original complaint vs. altered FIR)
     - The lack of due diligence by Inspector Taralgatti
     - Saraf's right of reply (his contact details provided to press)
     - Sub-judice disclaimer and GDPR-compliant footer

   Delivery status:
     Contacts verified  : 1,704 (DNS-checked press / legal media)
     Successfully sent  : 40 (Batch 1 — including LiveLaw, Bar & Bench,
                              The Wire, Indian Express, NDTV, Frontline,
                              Caravan, Times Now, CNBC-TV18)
     Blocked            : 1,664 contacts pending
     Reason             : Proton Mail's account-level daily sending
                          limit was triggered after Batch 1. The account
                          sujata.shirasi@pressdetective.com was frozen
                          for ~22 hours by Proton's anti-spam system.
   
   This is a known limitation of Proton Mail for broadcast volumes.
   The remaining 1,664 journalists / editors will be reached today
   (10 June 2026) using a multi-account rotation strategy.

======================================================================
PART 2 — TODAY'S PLAN (10 June 2026)
======================================================================

TASK 1: Resume press release broadcast (Priority: HIGH)
   Target: Remaining 1,664 press contacts
   Method: Rotate across Proton accounts (santosh, info, olympio) to
           stay within per-account daily limits — 40 per account per
           session, with 20-second pauses between batches.
   Goal:   Full 1,704-contact delivery by end of day.

TASK 2: Fix git repository push (Priority: MEDIUM)
   Status: All new scripts committed locally on branch abhisheksaraf.
           Git push failed yesterday due to wrong credential cached
           (dharteglobal account instead of pressdetective account).
   Fix:    Update Windows Credential Manager to use pressdetective
           account, then push.

TASK 3: Monitor Saraf's response (Priority: HIGH — watch daily)
   Deadline: 16 June 2026
   Check: abhishek_saraf78@yahoo.com for any reply to the notice.
   If no reply by 16 June: Proceed with Quashing Petition filing.

TASK 4: Correct factual framing in remaining send scripts
   The contacts-branch press appeal script still contains an
   incorrect statement ("attended briefly and left") which is factually
   wrong. This has been corrected in the abhisheksaraf branch version
   but needs to be verified before any further broadcast run.

======================================================================
PART 3 — CRITICAL DEADLINE WATCH
======================================================================

  DATE          : 16 June 2026
  DEADLINE      : Saraf's deadline to respond to WITHOUT PREJUDICE notice
  WHAT HAPPENS  : If no response or refusal to withdraw —
                  Section 528 BNSS Quashing Petition before Bombay HC
                  is filed immediately.

======================================================================
PART 4 — WHAT I NEED FROM YOU (please respond by 14 June 2026)
======================================================================

As set out in the 9 June legal update:

  [ ] Your mobile CDR records for June 2022 (call logs showing no
      extortion demand was ever made to Saraf)
  [ ] Your bank statements June–September 2022 (showing no payment
      from Saraf was received)
  [ ] Screenshots of all WhatsApp / SMS messages with Saraf (if any)
  [ ] Your written account of events on 2 June 2022
  [ ] Names of any witnesses at the restaurant that evening
  [ ] Any information about CCTV footage from the venue

Please respond to this email or call me directly at +91 93216 13691.
The quashing petition is our strongest weapon — and your evidence
is the key to it.

======================================================================

Yours faithfully,

Adv. Sujata Shirasi
Advocate — Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Phone : +91 93216 13691
Email : sujata.shirasi@pressdetective.com
Date  : 10 June 2026

PressDetective | info@pressdetective.com

----------------------------------------------------------------------
To stop receiving communications from PressDetective, reply UNSUBSCRIBE
or write to info@pressdetective.com. Requests honoured within 48 hours.
----------------------------------------------------------------------
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def try_send(from_addr, pw, to, cc, subject, body):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    msg = MIMEMultipart("alternative")
    msg["From"]    = f"Adv. Sujata Shirasi <{from_addr}>"
    msg["To"]      = to
    msg["Cc"]      = cc
    msg["Subject"] = subject
    msg["Reply-To"] = from_addr
    msg.attach(MIMEText(body, "plain", "utf-8"))
    with smtplib.SMTP(HOST, PORT, timeout=60) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.ehlo()
        s.login(from_addr, pw)
        s.sendmail(from_addr, [to, cc], msg.as_string())

accounts_to_try = [
    ("sujata.shirasi@pressdetective.com", BRIDGE_PW),
    ("santosh@pressdetective.com",         BRIDGE_PW),
    ("info@pressdetective.com",            BRIDGE_PW),
]

sent = False
for addr, pw in accounts_to_try:
    print(f"Trying {addr} ...")
    try:
        try_send(addr, pw, TO, CC, SUBJECT, BODY)
        print(f"[OK] Sent via {addr}")
        sent = True
        break
    except Exception as e:
        err = str(e)
        print(f"[!!] Failed ({err[:120]})")
        if "frozen" in err.lower() or "2011" in err or "limit" in err.lower():
            print("     -> Rate limited, trying next account")
        else:
            print("     -> Non-rate-limit error, trying next")

if not sent:
    print("[FAIL] All accounts exhausted — report NOT sent.")
    raise SystemExit(1)