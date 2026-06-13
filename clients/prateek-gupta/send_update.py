"""Send execution update to Sagar Zaveri — 9 June 2026"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from lib.mailer import build_msg, send_mail

FROM_ADDR = "Santosh | Press Detective <santosh@pressdetective.com>"
TO_ADDR   = "sagarzaveri.tbz@gmail.com"
CC        = "tonymony@gmail.com"
SUBJECT   = "Prateek Gupta — Update: corrections filed, website & LinkedIn ready | Press Detective"

BODY = """\
Dear Sagar,

Quick update on where we stand. We have been executing since this morning.

─────────────────────────────────────
DONE — no input needed from your side
─────────────────────────────────────

1. CORRECTION REQUESTS FILED
   We have formally written to both publications that ran the wrong "$600 million"
   figure (the correct judgment sum is ~US$500 million):

   - Insurance Journal  →  newsdesk@insurancejournal.com
   - Claims Journal     →  djergler@claimsjournal.com (editor Don Jergler)

   Both letters request correction of the headline and article figure, and invite
   them to add a note that Mr Gupta disputes the judgment and is pursuing legal
   steps. Copies available on request.

2. PERSONAL WEBSITE — BUILT AND READY TO DEPLOY
   We have built a full personal website for Mr Gupta:

     Sections: About · Expertise · Career · Contact
     Design:   Professional — navy, teal, gold
     SEO:      Title tag, meta description, og tags all set to rank for
               "Prateek Gupta commodities" and related queries

   The site is complete. The moment Mr Gupta supplies his bio (200–400 words
   in his own words) and headshot, we update the placeholder text and go live.
   Domain registration takes 10 minutes. Google indexes new sites within days.

3. LINKEDIN PROFILE — COPY FULLY DRAFTED
   We have written:
   - Headline (220 chars, optimised for search)
   - Full About section (1,200 chars — within LinkedIn's limit)
   - Experience entries for TMT Metals and Ushdev International
   - 12 skills to add
   - Featured section plan
   - Recommended posting cadence (1–2 posts/week, nickel/commodities commentary)

   As with the website, this is ready to publish the moment we have his career
   timeline confirmed.

─────────────────────────────────────
URGENT — we need these from Mr Gupta
─────────────────────────────────────

A. DIFC COURT OF APPEAL JUDGMENT — TODAY
   The Dubai (DIFC) Court of Appeal judgment in Trafigura v Gupta & Ginni Gupta
   [2025] DIFC CA 001 was issued on 9 June 2026 — today. Please obtain the full
   text and send it to us immediately. Depending on the outcome, this may
   significantly change the picture for the England & Wales appeal and for the
   public narrative.

B. SOLICITOR STATUS — THIS WEEK
   The 21-day CPR window to renew the appeal at the England & Wales Court of
   Appeal expired around 19 March 2026. An extension-of-time application is now
   required — and the longer it waits, the harder it becomes to justify the delay.
   Please confirm: does Mr Gupta currently have a solicitor? Name and contact if
   yes; if no, we will prepare a KC/solicitor shortlist within 24 hours.

C. BIO + CAREER TIMELINE — THIS WEEK
   200–400 words in Mr Gupta's own words, or a bullet-point timeline we can
   write from. This is the only thing standing between us and a live website
   and LinkedIn profile.

D. HEADSHOT
   Any recent professional photo. Smartphone is fine for now.

─────────────────────────────────────
NEXT STEPS ONCE WE HEAR FROM YOU
─────────────────────────────────────

- Domain registered + website live within 3 days of receiving bio
- LinkedIn profile published within 2 days of receiving bio
- Right-of-reply statement issued to GTR, Trade Finance Global, and Mining.com
  once solicitor confirms it is safe to do so
- First commodities commentary article published under Mr Gupta's name
  (LinkedIn + third-party platform) within 2 weeks

Please revert on items A and B today if at all possible — both are time-sensitive.

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
    ok = send_mail(msg, account="santosh")
    print("Sent" if ok else "FAILED — check mailer logs")

if __name__ == "__main__":
    send()
