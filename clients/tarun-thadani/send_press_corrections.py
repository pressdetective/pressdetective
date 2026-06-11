#!/usr/bin/env python3
"""
send_press_corrections.py
Factual correction letters to Times of India and Hindustan Times.

ToI: specific correction of published article —
     "Two bizmen chargesheeted for assault, Rs 1cr extortion bid in '22"
     byline S Ahmed Ali, Times of India Mumbai edition

HT:  proactive pre-publication right-of-reply / factual background

From : sujata.shirasi@pressdetective.com  (Proton Bridge / Postmark fallback)
CC   : info@pressdetective.com
Usage: python send_press_corrections.py [--dry-run]
"""
import sys, time, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from lib.mailer import send_mail, build_msg

FROM_ACC  = 'sujata'
FROM_ADDR = 'sujata.shirasi@pressdetective.com'

# ─────────────────────────────────────────────────────────────────────────────
# TIMES OF INDIA — specific correction referencing the published article
# ─────────────────────────────────────────────────────────────────────────────

TOI_SUBJECT = (
    'Factual Correction — "Two bizmen chargesheeted for assault, '
    'Rs 1cr extortion bid in \'22" (Times of India, S Ahmed Ali) '
    '— Tarun Thadani / FIR 0654/2022'
)

TOI_BODY = """\
Dear Editor / Corrections Desk,
Dear Mr. S Ahmed Ali,

We write on behalf of Mr. Tarun Thadani, Founder and Group CEO of Dharte
(dharte.com), a wellness and sustainability marketplace based in Mumbai.

Your publication carried an article titled:

  "Two bizmen chargesheeted for assault, Rs 1cr extortion bid in '22"
  Byline  : S Ahmed Ali
  Publication: Times of India, Mumbai Edition

The article's digital URL is behind a paywall and not publicly indexed, but
we hold a copy of the published text. The article contains four specific
factual errors and a fundamental procedural failure that have caused serious
and ongoing reputational harm to Mr. Thadani. We request an urgent
correction and right-of-reply.

========================================================
ERROR 1 — MR. THADANI IS ATTRIBUTED ACTIONS HE DID NOT COMMIT
========================================================

WHAT YOUR ARTICLE SAYS:
  Tarun Thadani and Ali Asgar Merchant "hatched a criminal conspiracy,"
  "slapped him, recorded the incident on their phone," and "demanded
  Rs 1 crore to not make the video viral."

THE FACT:
  Mr. Thadani was NOT present at the Worli restaurant event on the night
  of 2-3 June 2022. His sole connection to that event was sending
  invitations. Not a single independent witness places him at the venue.
  The chargesheet's assertion that he participated in an assault or extortion
  is disputed by documentary evidence, which was available to the reporter
  and was not sought before publication.

========================================================
ERROR 2 — THE EXTORTION ALLEGATION DID NOT EXIST IN THE ORIGINAL COMPLAINT
========================================================

WHAT YOUR ARTICLE SAYS:
  The article presents the Rs 1 crore extortion demand as an established
  part of the case from the outset.

THE FACT:
  The complainant, Mr. Abhishek Badriprasad Saraf, filed his original
  complaint on 4 June 2022. That complaint alleged assault only. It
  contained NO mention of extortion and NO mention of Mr. Thadani.
  Both the extortion allegation and Mr. Thadani's name were introduced
  approximately two months later when the FIR was registered in August 2022
  — without any accused being examined and without any corroborating
  evidence being produced. The dated original complaint is available on
  request and is verifiable by any journalist.

========================================================
ERROR 3 — THE COMPLAINANT'S OWN RECORD WAS NOT DISCLOSED
========================================================

WHAT YOUR ARTICLE SAYS:
  The complainant, Mr. Abhishek Badriprasad Saraf, is described without
  reference to his own history of litigation and alleged fraud.

THE FACT:
  Mr. Saraf is the subject of a public Change.org petition (181 signatures)
  and court filings alleging that he fraudulently occupies the third floor of
  Esplanade House — the historic home of Jamsetji Tata, a UNESCO Heritage
  building — using a forged power of attorney, in a scheme valued at over
  Rs 150 crore. Additionally, a senior corporate executive (Nitin Chamaria,
  then CFO of Blue Energy Motors) has alleged in a sworn statement that he
  was coerced by Mr. Saraf into providing a false statement in this very
  chargesheet. This background is material to a fair account of the case
  and was omitted entirely.

========================================================
ERROR 4 — NO RESPONSE FROM THE ACCUSED WAS SOUGHT
========================================================

THE FACT:
  The article is sourced entirely from the chargesheet and the investigating
  officer. There is no indication that Mr. Thadani, his co-accused, or their
  counsel was contacted for a response before publication. This is contrary
  to Press Council of India Norms of Journalistic Conduct (Norm 7 — right
  of reply) and the basic principles of fair reporting.

========================================================
OUR FOUR REQUESTS
========================================================

  1. CORRECTION — Publish a correction to the article noting that:
     (a) Mr. Thadani was not present at the event on 2-3 June 2022;
     (b) the Rs 1 crore extortion allegation was absent from the original
         complaint of 4 June 2022 and was introduced months later;
     (c) Mr. Thadani denies all allegations and is actively challenging the
         chargesheet at the Bombay High Court (s.528 BNSS quashing petition
         and Criminal Revision petition, both pending).

  2. RIGHT OF REPLY — Publish a response from Mr. Thadani alongside or
     appended to the existing article.

  3. EVIDENCE PACKAGE — Available on request:
     - Original complaint dated 4 June 2022 (showing no extortion, no
       mention of Thadani)
     - Sessions Court order of 31 March 2024 (a procedural ruling on prima
       facie sufficiency, not a finding of guilt)
     - Bombay High Court filing reference (quashing petition)
     - Change.org petition and court records on Mr. Saraf's fraud history
     - Statement by Nitin Chamaria on coerced testimony

  4. WRITTEN ACKNOWLEDGEMENT that this letter has been received and forwarded
     to the responsible editor and the legal desk.

Failure to publish a correction may result in a formal complaint to the
Press Council of India and, where appropriate, legal proceedings.

We trust your commitment to factual and fair reporting.

Yours faithfully,
Sujata Shirasi
PressDetective — Legal & Media Relations
On behalf of Mr. Tarun Thadani
sujata.shirasi@pressdetective.com
+91 93216 13691

Counsel of record: Adv. Sujata Shirasi, Bombay High Court
"""

# ─────────────────────────────────────────────────────────────────────────────
# HINDUSTAN TIMES — proactive pre-publication right-of-reply
# ─────────────────────────────────────────────────────────────────────────────

HT_SUBJECT = (
    "Right of Reply & Pre-Publication Notice — Tarun Thadani / "
    "FIR No. 0654/2022, Dadar PS, Mumbai"
)

HT_BODY = """\
Dear Editor / News Desk,

We write on behalf of Mr. Tarun Thadani, Founder and Group CEO of Dharte
(dharte.com), a wellness and sustainability marketplace based in Mumbai.

FIR No. 0654 of 2022 (Dadar Police Station, Mumbai), in which Mr. Thadani
is named as an accused, has received press coverage. The Times of India
(Mumbai edition) published an article on this matter under the headline:

  "Two bizmen chargesheeted for assault, Rs 1cr extortion bid in '22"
  Byline: S Ahmed Ali

That article contained material factual errors — including false attribution
of actions Mr. Thadani did not commit, omission of the fact that the
extortion allegation was added months after the original complaint, and no
right of reply sought from the accused — causing serious reputational harm
to Mr. Thadani.

We write to Hindustan Times proactively, so that should your publication
cover this matter, it does so with the benefit of the following verified facts.

========================================================
KEY VERIFIED FACTS
========================================================

1. MR. THADANI WAS NOT PRESENT AT THE INCIDENT
   The alleged incident occurred at a private event at a restaurant in Worli,
   Mumbai, on the night of 2-3 June 2022. Mr. Thadani's sole involvement was
   sending invitations. He was not present at the venue. Not a single
   independent witness places him there.

2. EXTORTION ALLEGATION ADDED MONTHS AFTER THE ORIGINAL COMPLAINT
   The complainant's original complaint (4 June 2022) alleged assault only
   — no extortion, no mention of Mr. Thadani. Both the Rs 1 crore extortion
   charge and Mr. Thadani's name first appeared approximately two months
   later when the FIR was registered in August 2022, without any accused
   being examined. The dated original complaint is available on request.

3. THE COMPLAINANT HAS A DOCUMENTED RECORD OF ALLEGED FRAUD
   Complainant Abhishek Badriprasad Saraf is the subject of a Change.org
   petition (181 signatures) and court filings alleging he fraudulently
   occupies the third floor of Esplanade House — the historic home of
   Jamsetji Tata, a UNESCO Heritage building — through a forged power of
   attorney (scheme valued at Rs 150+ crore). A CFO has alleged he was
   coerced into providing a false statement in this very chargesheet.

4. THE CASE IS BEING CHALLENGED AT BOMBAY HIGH COURT
   A Section 528 BNSS quashing petition and a Criminal Revision petition
   are pending before the Bombay High Court. The Sessions Court's discharge
   refusal (31 March 2024) is a procedural ruling on prima facie sufficiency
   — it does not constitute any finding of guilt.

========================================================
OUR REQUEST
========================================================

Should Hindustan Times cover this matter, we request that you:
  - Contact us BEFORE publication for Mr. Thadani's formal statement.
  - Not report chargesheet allegations as established facts.
  - Allow us to provide the full evidence package (original complaint,
    court orders, HC filing, Saraf fraud records) to the assigned journalist.

Please confirm receipt of this letter and that it has been forwarded to the
relevant editor.

Yours faithfully,
Sujata Shirasi
PressDetective — Legal & Media Relations
On behalf of Mr. Tarun Thadani
sujata.shirasi@pressdetective.com
+91 93216 13691

Counsel of record: Adv. Sujata Shirasi, Bombay High Court
"""

# ─────────────────────────────────────────────────────────────────────────────
OUTLETS = [
    {
        "label": "Times of India — Corrections Desk",
        "to": "reader@timesgroup.com",
        "cc_extra": "mumbainews@timesgroup.com",
        "subject": TOI_SUBJECT,
        "body": TOI_BODY,
    },
    {
        "label": "Times of India — Mumbai Desk (S Ahmed Ali)",
        "to": "mumbainews@timesgroup.com",
        "cc_extra": None,
        "subject": TOI_SUBJECT,
        "body": TOI_BODY,
    },
    {
        "label": "Hindustan Times — Feedback / Corrections",
        "to": "htfeedback@hindustantimes.com",
        "cc_extra": "mumbai.desk@hindustantimes.com",
        "subject": HT_SUBJECT,
        "body": HT_BODY,
    },
    {
        "label": "Hindustan Times — Mumbai Desk",
        "to": "mumbai.desk@hindustantimes.com",
        "cc_extra": None,
        "subject": HT_SUBJECT,
        "body": HT_BODY,
    },
]


def main(dry_run=False):
    seen = set()
    for outlet in OUTLETS:
        to = outlet["to"]
        if to in seen:
            continue
        seen.add(to)
        label   = outlet["label"]
        cc_base = "info@pressdetective.com"
        cc_extra = outlet.get("cc_extra")
        cc = f"{cc_base}, {cc_extra}" if cc_extra else cc_base
        msg = build_msg(
            from_addr=FROM_ADDR,
            to=to,
            subject=outlet["subject"],
            body=outlet["body"],
            cc=cc,
        )
        if dry_run:
            print(f"[dry-run] {label} -> {to}")
            continue
        ok = send_mail(msg, account=FROM_ACC)
        print(f"[{'OK' if ok else 'FAILED'}] {label} -> {to}")
        time.sleep(4)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
