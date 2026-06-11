#!/usr/bin/env python3
"""
Send 30-day reputation cleanup plan to Tarun Thadani and CC tonymony.
Run from repo root: python clients/tarun-thadani/send_30day_plan.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.mailer import send_mail, build_msg

FROM         = "Adv. Sujata Shirasi <sujata.shirasi@pressdetective.com>"
TO           = "tarun@dharte.com"
CC           = "info@pressdetective.com, tonymony@gmail.com"
SUBJECT      = "Your 30-Day Reputation Cleanup Plan — Tarun Thadani / PressDetective"

BODY = """\
Dear Tarun,

Following our audit and the immediate actions already taken (press corrections sent
to Times of India and Hindustan Times, media pitches sent to YourStory / Inc42 /
Mint Lounge / The Ken, Radaris correction filed), here is your full 30-day execution
calendar.

The core finding from your digital audit: the FIR does NOT appear on Google page 1
for your name. The window to build permanent narrative armour is open right now.
We are acting fast.

────────────────────────────────────
ALREADY DONE (Days 0–1, 10–11 June)
────────────────────────────────────

✅  Online reputation audit completed and sent to you
✅  30-track cleanup plan sent
✅  Factual correction → Times of India (mumbainews@timesgroup.com)
✅  Pre-publication notice → Hindustan Times (htfeedback + mumbai.desk)
✅  Extended corrections sent to: Midday, Free Press Journal, Maharashtra Times,
    NDTV India, Mumbai Mirror/Mirror Now
✅  Media pitches: YourStory, Inc42, Mint Lounge, The Ken
✅  Radaris India correction/removal request filed
✅  Wikipedia article draft ready (pending your review)
✅  Crunchbase bio copy prepared
✅  Google Alerts setup guide prepared
✅  LinkedIn optimization brief prepared
✅  Press Council complaint drafted (ready to file Day 22 if ToI doesn't correct)
✅  Off-record journalist briefing prepared (The Wire / Scroll / Quint)

────────────────────────────────────
WEEK 1 (12–17 June): YOUR ACTIONS NEEDED
────────────────────────────────────

These 5 things can only be done by you. Please complete them this week:

1. CRUNCHBASE UPDATE (30 mins)
   Log into crunchbase.com → your profile → paste the text I will attach.
   This creates a permanent, Google-indexed founder profile.

2. GOOGLE ALERTS (10 mins)
   I will attach a step-by-step guide. Set up these 6 alerts:
   • "Tarun Thadani"
   • "Tarun Thadani Dharte"
   • "FIR 0654"
   • "Abhishek Saraf"
   • "Dharte.com"
   • "Abhishek Badriprasad Saraf"

3. GOOGLE SEARCH CONSOLE ACCESS (5 mins)
   Add sujata.shirasi@pressdetective.com as a property owner at:
   search.google.com/search-console
   Select dharte.com → Settings → Users and permissions → Add user
   This lets us claim your Google Knowledge Panel officially.

4. FACEBOOK DUPLICATE PROFILE (15 mins)
   Deactivate your secondary profile (tarun.thadani1) — keep only the primary.
   Having two profiles splits your SEO authority and creates confusion.

5. LINKEDIN CREATOR MODE (5 mins)
   Settings → Visibility → Creator mode → ON
   See the LinkedIn brief I will attach for the full optimized bio to paste in.

────────────────────────────────────
WEEK 2 (18–24 June): MEDIA + LEGAL
────────────────────────────────────

PressDetective will:
- Follow up on all 4 media pitches (YourStory, Inc42, Mint Lounge, The Ken)
- Submit new pitches: Scroll, The Print, Times Now Digital, CNBC-TV18
- Compile Saraf antecedents dossier for Adv. Shirasi

You will:
- Share next HC court date as soon as known

────────────────────────────────────
WEEK 3 (25 June – 1 July): COUNTER-NARRATIVE
────────────────────────────────────

PressDetective will:
- Finalise press release on Saraf (pending counsel sign-off)
- Begin off-record journalist briefings (The Wire / Scroll / Quint)
- Escalate to Press Council if ToI has not corrected by Day 16

You will:
- Begin Change.org signature push (181 → 500+) through your Dharte community
- Confirm court date

────────────────────────────────────
WEEK 4 (2–10 July): LOCK IN
────────────────────────────────────

PressDetective will:
- Deploy press release timed to HC admission date
- File Press Council complaint if ToI still has not corrected
- Confirm Wikipedia article live, Google Knowledge Panel live, Radaris corrected
- Deliver final 30-day report

────────────────────────────────────
CRITICAL PATH
────────────────────────────────────

If you do only one thing this week: grant Google Search Console access.
If we do only one thing: get the Wikipedia article submitted via a neutral editor.
These two actions create permanent, Google-indexed positive content that will
push any negative result down.

────────────────────────────────────
YOUR DEDICATED CONTACTS
────────────────────────────────────

PressDetective editorial desk: info@pressdetective.com
Legal / press enquiries: sujata.shirasi@pressdetective.com (+91 93216 13691)

All documents (LinkedIn brief, Crunchbase bio, Google Alerts guide, Wikipedia
draft) are available on request — just reply to this email.

We are moving fast. The window is open.

Warm regards,

Adv. Sujata Shirasi
PressDetective
sujata.shirasi@pressdetective.com
+91 93216 13691
"""


def main():
    msg = build_msg(
        from_addr=FROM,
        to=TO,
        subject=SUBJECT,
        body=BODY,
        cc=CC,
    )
    ok = send_mail(msg, account="sujata")
    if ok:
        print(f"[OK] 30-day plan sent -> {TO}")
    else:
        print(f"[FAILED] 30-day plan NOT sent -> {TO}")


if __name__ == "__main__":
    main()
