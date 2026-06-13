"""
Send correction requests to Insurance Journal and Claims Journal
re: wrong "$600M" judgment figure (correct is ~$500M).
Both are part of Wells Media Group — shared SMTP contact confirmed.

From:  santosh@pressdetective.com
To:    newsdesk@insurancejournal.com, djergler@claimsjournal.com
CC:    tonymony@gmail.com
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from lib.mailer import build_msg, send_mail

FROM_ADDR = "Santosh | Press Detective <santosh@pressdetective.com>"
CC_ALWAYS = "tonymony@gmail.com"

CORRECTIONS = [
    {
        "to": "newsdesk@insurancejournal.com",
        "publication": "Insurance Journal",
        "editor": "Editor",
        "headline": "Trafigura Wins $600 Million Nickel Fraud Lawsuit Against Businessman Gupta",
        "url": "https://www.insurancejournal.com/news/international/2026/02/02/856429.htm",
        "date": "2 February 2026",
        "subject": "Correction request — wrong judgment figure — Trafigura v Gupta coverage",
    },
    {
        "to": "djergler@claimsjournal.com",
        "publication": "Claims Journal",
        "editor": "Don Jergler",
        "headline": "Trafigura Wins $600M Nickel Fraud Suit Against Businessman Gupta",
        "url": "https://www.claimsjournal.com/news/national/2026/02/02/335434.htm",
        "date": "2 February 2026",
        "subject": "Correction request — wrong judgment figure — Trafigura v Gupta coverage",
    },
]

BODY_TEMPLATE = """\
Dear {editor},

I write on behalf of Mr Prateek Gupta regarding the following article published by {publication}:

  Headline: "{headline}"
  Date:     {date}
  URL:      {url}

We are not asking {publication} to revisit the court's findings or to withdraw the article.
We are requesting correction of one specific, verifiable factual inaccuracy.

THE ERROR
The headline and article state that Trafigura won a "$600 million" (or "$600M") fraud
lawsuit. This figure is incorrect.

THE CORRECT POSITION
The UK High Court judgment of 30 January 2026 (Trafigura Pte Ltd & Anor v Prateek Gupta
& Ors [2026] EWHC 159 (Comm), Mr Justice Saini) awarded Trafigura recovery of
approximately US$500 million — not $600 million. The $600M–$625M figure cited in some
coverage refers to the earlier worldwide freezing order, a procedural asset-preservation
measure, not the judgment sum itself.

This is confirmed by:
- The judgment text (judiciary.uk — Trafigura v Gupta and others)
- Global Trade Review: "Trafigura wins blockbuster US$500mn nickel fraud claim"
- Trade Finance Global: "Trafigura wins $500mn in High Court case against Gupta"

We would be grateful if you would correct the figure to US$500 million in both the
headline and the article body, and — where editorially appropriate — add a note that
Mr Gupta disputes the judgment and is pursuing further legal steps.

Please treat this as a request under your publication's standard corrections policy.

Yours sincerely,
Santosh
Press Detective
santosh@pressdetective.com

---
Sent on behalf of Mr Prateek Gupta. This correspondence is not legal advice.
"""


def send_all():
    for c in CORRECTIONS:
        body = BODY_TEMPLATE.format(**c)
        msg = build_msg(
            from_addr=FROM_ADDR,
            to=c["to"],
            subject=c["subject"],
            body=body,
            cc=CC_ALWAYS,
        )
        ok = send_mail(msg, account="santosh")
        status = "OK" if ok else "FAILED"
        print(f"[{status}] {c['to']} ({c['publication']})")


if __name__ == "__main__":
    send_all()
