"""
Activity status report to Sagar Zaveri — all initiated actions for
Prateek Gupta ORM cleanup. Sent via Postmark directly.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from lib.mailer import build_msg, send_mail

FROM_ADDR = "Santosh | Press Detective <santosh@pressdetective.com>"
TO_ADDR   = "sagarzaveri.tbz@gmail.com"
CC        = "tonymony@gmail.com"
SUBJECT   = "Prateek Gupta — Activity Report: All Actions Initiated | Press Detective"

BODY = """\
Dear Sagar,

This is a full record of every action we have initiated for Mr Prateek Gupta's
online reputation cleanup as of 9 June 2026. You can share this with Mr Gupta
directly.

═══════════════════════════════════════════
ACTIONS INITIATED & COMPLETED
═══════════════════════════════════════════

1. LIVE SERP AUDIT — COMPLETE
   We conducted a full live search audit of every significant URL appearing for
   "Prateek Gupta" across Google and trade press. We mapped 13 URLs, rated each
   for damage level (CRITICAL / HIGH / OPPORTUNITY), and identified the two
   outlets carrying a specific verifiable factual error.

   Key findings:
   - 4 CRITICAL outlets (GTR, Moneylife, Mining.com, Public Eye)
   - 2 HIGH outlets with correctable error (Insurance Journal, Claims Journal)
   - No Wikipedia page, no LinkedIn profile, no personal website currently
     exists for the correct Prateek Gupta — major first-mover opportunity

2. CORRECTION REQUEST — INSURANCE JOURNAL — FILED
   Sent to: newsdesk@insurancejournal.com
   Re: Headline "Trafigura Wins $600 Million Nickel Fraud Lawsuit Against
       Businessman Gupta" — the judgment figure is ~US$500M, not $600M.
   Status: Delivered. Awaiting response.

3. CORRECTION REQUEST — CLAIMS JOURNAL — FILED
   Sent to: djergler@claimsjournal.com (Editor Don Jergler)
   Re: Same $600M/$500M error in their coverage.
   Status: Delivered. Awaiting response.

4. PERSONAL WEBSITE — BUILT, READY TO DEPLOY
   A full 5-section professional website has been designed and built:
     - Hero: "Prateek Gupta — Commodities & Trade Finance Professional"
     - About: Career summary (placeholder — awaiting Mr Gupta's bio)
     - Expertise: Base Metals, Trade Finance, Cross-Border, Market Analysis
     - Career: TMT Metals (2016–) and Ushdev International (2009–2018)
     - Contact: Email + LinkedIn

   SEO: Title tag, meta description, and Open Graph tags configured to rank
   for "Prateek Gupta" and "Prateek Gupta commodities" queries.

   To go live we need: (a) domain registered, (b) Mr Gupta's bio replacing
   the placeholder text. We can have the site indexed within 72 hours of
   receiving his bio.

5. LINKEDIN PROFILE COPY — DRAFTED, READY TO PUBLISH
   Complete profile written:
     Headline:  "Commodities & Trade Finance | Base Metals & Nickel |
                 International Trading | Asia · Europe · Middle East · Dubai"
     About:     1,200-character professional summary
     Experience: TMT Metals + Ushdev International entries
     Skills:    12 relevant skills
     Activity:  Recommended cadence — 1–2 posts/week on nickel/commodities

   LinkedIn pages rank on page 1 for personal names within weeks of creation.
   This is the fastest suppression asset we can deploy. Needs career timeline
   confirmation from Mr Gupta before publishing.

6. RIGHT-OF-REPLY STATEMENT — DRAFTED, READY TO ISSUE
   A single, accurate statement in Mr Gupta's name has been prepared. It
   states that he disputes the judgment and is pursuing legal remedies. It
   does not assert innocence as established fact and does not re-accuse the
   court-cleared Trafigura employees.

   Earmarked for: GTR, Trade Finance Global, Mining.com.
   Condition: Must be cleared by Mr Gupta's current solicitor before release.

═══════════════════════════════════════════
CRITICAL LEGAL ALERTS — REQUIRE IMMEDIATE ACTION
═══════════════════════════════════════════

A. DIFC COURT OF APPEAL JUDGMENT — ISSUED TODAY (9 JUNE 2026)
   The Dubai (DIFC) Court of Appeal judgment in [2025] DIFC CA 001
   (Trafigura v Mr Prateek Gupta & Mrs Ginni Gupta) was handed down today.
   We do not yet have the text. Please obtain and send to us immediately.
   If Mr Gupta succeeded on any ground in Dubai, this materially changes the
   England & Wales appeal narrative and extension-of-time application.

B. ENGLAND & WALES COURT OF APPEAL — EXTENSION OF TIME NEEDED
   The High Court refused permission to appeal on 26 February 2026.
   The 21-day CPR deadline to renew at the Court of Appeal passed on
   approximately 19 March 2026. An extension-of-time application is now
   required. Every additional week of delay weakens that application.
   A solicitor must file this. Please confirm representation TODAY.

═══════════════════════════════════════════
WHAT WE NEED FROM MR GUPTA — 4 ITEMS
═══════════════════════════════════════════

   1. DIFC judgment text — today
   2. Solicitor name & contact (or confirmation he is unrepresented)
   3. Professional bio (200–400 words) + career timeline
   4. Headshot (any recent photo)

Items 1 and 2 are time-critical. Items 3 and 4 unlock the website and
LinkedIn publish — both of which are built and waiting.

═══════════════════════════════════════════
WHAT HAPPENS NEXT — SEQUENCE
═══════════════════════════════════════════

   Day 1–3  : Receive bio → register domain → website live
   Day 2–3  : Receive timeline → publish LinkedIn profile
   Day 3–7  : Issue right-of-reply to GTR / TFG / Mining.com (solicitor cleared)
   Week 2   : First commodities commentary article published under Mr Gupta's name
   Week 3–4 : Begin monitoring Insurance Journal / Claims Journal for correction
              publication; follow up if no response within 14 days
   Day 30   : First SERP measurement — track search rank movement
   Day 90   : Full assessment + strategy review

We are ready to move the moment you reply. Please send the four items above
to this address and we will begin immediately.

Santosh
Press Detective
santosh@pressdetective.com
"""

def send():
    msg = build_msg(
        from_addr=FROM_ADDR,
        to=TO_ADDR,
        subject=SUBJECT,
        body=BODY,
        cc=CC,
    )
    # Force Postmark as the provider
    ok = send_mail(msg, account="santosh", providers=["postmark"])
    print("Sent via Postmark" if ok else "Postmark failed — check token")

if __name__ == "__main__":
    send()
