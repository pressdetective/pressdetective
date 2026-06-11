#!/usr/bin/env python3
"""
send_audit.py — Send the online reputation audit to tarun@dharte.com
Via     : Proton Bridge SMTP (127.0.0.1:1025 STARTTLS)
From    : sujata.shirasi@pressdetective.com
To      : tarun@dharte.com
CC      : tonymony@gmail.com, info@pressdetective.com

Usage: python send_audit.py [--dry-run]
"""
import sys, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))
from lib.mailer import send_mail, build_msg

FROM_ACC = 'sujata'
TO_ADDR  = 'tarun@dharte.com'
CC_ADDRS = ['tonymony@gmail.com', 'info@pressdetective.com']

SUBJECT = "PressDetective — Online Reputation Audit & Cleanup Plan: Tarun Thadani"

BODY = """\
Dear Tarun,

PressDetective has completed a full audit of your online reputation across Google,
LinkedIn, Instagram, Twitter/X, Facebook, Crunchbase, Radaris India, UK Companies
House, and multiple news archives.

The headline finding is encouraging: FIR No. 0654/2022 does NOT appear on the
first page of Google for any common search of your name. No Times of India, Midday,
or Mumbai Mirror article linking you to the case was found. Your professional
identity currently dominates all search results. However, the window to build
lasting narrative armour must be used NOW -- before the quashing petition at Bombay
High Court attracts press attention.

Below is the complete audit report.

=============================================================
SECTION 1 -- WHAT WE FOUND
=============================================================

POSITIVE / CONTROLLED ASSETS
  * LinkedIn (thadanitarun) -- active, professional, ranks page 1
  * Dharte member profile (dharte.in) -- active, positive
  * Instagram @tarunthadanii -- 102 posts, 453 followers, active
  * Instagram @bharatblogs -- active
  * Twitter/X @tarunthadani and @TarunThadani1 -- exist (activity unconfirmed)
  * Facebook facebook.com/tarun.thadani.14 -- active
  * Facebook facebook.com/tarun.thadani1 -- DUPLICATE (risk: see below)
  * Crunchbase -- KPT Hospitality / DHARTE Group CEO listed
  * Dharte Fest 2025 (gospiritualindia.in) -- strong positive press coverage
  * Instagram "I Am Peacekeeper -- Mr. Tarun Thadani, Founder" -- positive

RISKS THAT NEED FIXING
  1. Radaris India -- MEDIUM RISK
     The site mixes your profile with 3-4 other "Tarun Thadani" individuals
     (a Wipro IT analyst, an IBM/Canon marketing manager, a Deepak Insurance GM).
     False professional associations. Submit a data removal/correction request.

  2. Two Facebook profiles -- LOW RISK
     Having two personal profiles violates Facebook's terms and creates
     impersonation risk. Merge or deactivate the older one (tarun.thadani1).

  3. UK Companies House (GOV.UK) -- UNKNOWN RISK
     Your director appointments are publicly indexed. We do not yet know which
     companies are listed. If any are dissolved with adverse notes, this needs
     to be addressed. Please share the company names.

  4. Stale profiles (Indiblogger, SlideShare) -- LOW RISK
     Old "Fashionablyin CEO" branding from years ago. Update or delete.

ABHISHEK SARAF'S DOCUMENTED RECORD ONLINE (works in your favour)
  * Change.org petition (181 signatures): "Justice for Jamsetji Tata's Home --
    Reclaiming the Third Floor from Abhishek Saraf." Documents the Rs. 150 crore
    Esplanade House property fraud, forged power of attorney, parallel bank
    account to divert rent.
  * openpr.com: "Master Fake Extortion Complainer Unmasked -- Abhishek Badriprasad
    Saraf's Shocking Deceit Exposed!" -- already indexed on Google.
  * openpr.com: "Power of Attorney: Mumbai Conman's Elaborate Scheme Costs
    Fatehpuria Family INR 150 Crores" -- documents property fraud in detail.
  * openpr.com: "Abhishek Saraf and Nitin Chamaria: A Tale of Deceit" -- names
    Nitin Chamaria (CFO, Blue Energy Motors) as a coerced witness.
  All three articles rank when anyone searches "Abhishek Saraf Mumbai." This is
  strong material. We will amplify it further.

=============================================================
SECTION 2 -- CLEANUP PLAN
=============================================================

TRACK A -- NARRATIVE ARMOUR (start this week)

  A1. Wikipedia article for Dharte.com / Tarun Thadani
      Wikipedia ranks on Google page 1 for brand/founder names and feeds the
      Google Knowledge Panel. We will draft a neutral, well-sourced article
      covering Silkworks (founded 1989 by your father Prakash A. Thadani),
      your takeover, the Dharte rebrand (2021), and the wellness ecosystem.
      You review; a neutral editor submits. No legal content.

  A2. Google Knowledge Panel claim
      With GSC access for dharte.com we submit entity data so Google shows
      an authoritative info box for "Tarun Thadani" -- immediately dominates
      the visual real estate on the results page.

  A3. Crunchbase profile -- expand to full Dharte narrative
      Current listing is minimal. PressDetective will draft the copy;
      you log in and update.

  A4. National founder profile interview
      Pitch to The Ken, Mint Lounge, YourStory, or Inc42.
      Angle: "How a Mumbai home-furnishings family business became India's
      first integrated wellness marketplace."
      Published articles are permanent, search-indexed, and impossible to remove.

TRACK B -- DIGITAL CLEANUP (30-60 days)

  B1. Radaris India data removal -- submit opt-out/correction form.
  B2. Facebook consolidation -- deactivate duplicate older profile.
  B3. Indiblogger / SlideShare -- update with Dharte content or delete.
  B4. GOV.UK Companies House -- review all listed entities; flag any risk.

TRACK C -- SARAF COUNTER-NARRATIVE (60-90 days, after legal filing)

  C1. Amplify Change.org petition: 181 -> 1,000+ signatures via Dharte network.
  C2. Consolidated press release linking Martin Burn fraud + fake FIR + Nitin
      Chamaria coercion (requires Adv. Sujata Shirasi sign-off).
  C3. Off-record briefing to The Wire / Scroll / The Quint investigative desks
      on Saraf's pattern of property fraud + abuse of criminal process.

TRACK D -- MONITORING (ongoing from Day 1)

  Google Alerts daily: "Tarun Thadani", "Tarun Thadani Dharte", "FIR 0654/2022"
  Google Alerts weekly: "Abhishek Saraf"
  Social listening: Twitter/X, Reddit, LinkedIn
  Court date advance notice -> PressDetective prepares press release for same day.

=============================================================
SECTION 3 -- EIGHT THINGS WE NEED FROM YOU
=============================================================

Please reply to this email with answers to the following:

  1. SOCIAL MEDIA HANDLES -- Confirm all accounts you officially control.
     We found: LinkedIn (thadanitarun), Instagram (@tarunthadanii, @bharatblogs),
     Twitter (@tarunthadani, @TarunThadani1), Facebook (two profiles).
     Are any of these not yours? Are there others we missed?

  2. UK COMPANIES HOUSE -- Your director appointments are publicly indexed on
     GOV.UK. Please list the company names and current status (active/dissolved)
     so we can assess any association risk.

  3. TIMES OF INDIA / MIDDAY -- Has any article naming you in connection with
     FIR 0654/2022 been published? We found none. If you have seen one, please
     share the URL so we can pursue a right-of-reply / correction.

  4. GOOGLE SEARCH CONSOLE -- Do you have GSC access for dharte.com? If yes,
     please add sujata.shirasi@pressdetective.com as a verified user so we can
     claim the Knowledge Panel.

  5. POSITIVE PRESS -- List any interviews, features, or profiles published about
     you or Dharte in the last 3 years (print or online). We will amplify these.

  6. OPENPR.COM ARTICLES -- Were the three openpr.com press releases about Saraf
     published by PressDetective / your team, or by a third party? This affects
     how we cite and build on them.

  7. NEXT COURT DATE -- What is the next hearing date for FIR 0654/2022
     or the quashing petition? PressDetective needs this to time the press
     release deployment.

  8. ADV. SUJATA SHIRASI -- Has she been briefed on Tracks 1A and 1B from the
     Name Cleanup Plan sent on 9 June 2026?

=============================================================
TIMELINE SUMMARY
=============================================================

  Days 1-7   : Google Alerts live; Facebook dedup; Crunchbase updated;
               social handles confirmed; GSC access requested
  Days 8-30  : Wikipedia drafted + submitted; Radaris removal; media pitch
  Days 30-60 : Indiblogger/SlideShare cleaned; GOV.UK reviewed; profile published
  Days 60-90 : Saraf press release (post legal filing); Change.org amplification;
               journalist briefings
  Day 90+    : Wikipedia live; Knowledge Panel active; full monitoring running

=============================================================

Please reply at your earliest convenience. The faster we receive your answers,
the faster we can begin building the narrative armour before the next court date.

Warm regards,
Sujata Shirasi
PressDetective
sujata.shirasi@pressdetective.com

--
This report is confidential and prepared solely for Tarun Thadani.
PressDetective does not provide legal advice. All press releases and court
filings require sign-off by Adv. Sujata Shirasi before release.
"""


def main():
    ap = argparse.ArgumentParser(description='Send reputation audit to Tarun via Proton Bridge')
    ap.add_argument('--dry-run', action='store_true', help='Preview only -- send nothing')
    args = ap.parse_args()

    msg = build_msg(
        from_acc=FROM_ACC,
        to=TO_ADDR,
        subject=SUBJECT,
        body=BODY,
        cc=CC_ADDRS,
    )
    send_mail(msg, from_acc=FROM_ACC, dry_run=args.dry_run)
    if args.dry_run:
        print('DRY RUN -- no email sent')
    else:
        print(f'OK -- sent to {TO_ADDR}, CC: {", ".join(CC_ADDRS)}')


if __name__ == '__main__':
    main()
