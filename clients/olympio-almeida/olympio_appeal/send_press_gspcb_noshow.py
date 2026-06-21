"""
Press alert — GSPCB no-show at inspection. All 229 Goa press contacts.
FROM olympio.almeida@pressdetective.com via Proton remote SMTP.

    python clients/olympio-almeida/olympio_appeal/send_press_gspcb_noshow.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import csv, json, re, smtplib, ssl, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
HERE  = Path(__file__).parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"

# ── suppression ────────────────────────────────────────────────────────────────
sup = set()
for fname in ("suppress_14june.json","dead_14june.json","newdead_followup.json"):
    sup.update(e.lower() for e in json.loads((HERE/fname).read_text()))
sup.update(e.lower() for e in [
    "anto.dias@timesgroup.com","goa.city@timesgroup.com","goa.online@timesgroup.com",
    "goa.toi@timesgroup.com","hcnscript@gmail.com","kanzilrodrigues@gmail.com",
    "nolasco.dsouza@timesgroup.com","pankaj.sharma@timesgroup.com","sanjay123@gmail.com",
    "timesarunsinha3000@gmail.com","timesofindia.goa@timesgroup.com",
    ".gvs@gov.in","tn@berkeley.edu","ctcourt-mazgoan@bhc.gov.in",
])

aud = json.loads((HERE/"audience_14june.json").read_text())
existing = set(e.lower() for lst in aud.values() for e in lst)
EMAIL_RE  = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

def clean(lst):
    seen=set(); out=[]
    for e in lst:
        el=e.lower().strip()
        if el not in sup and el not in seen: seen.add(el); out.append(e)
    return out

ex_press = clean(aud["press"] + aud["other"])

rows = list(csv.DictReader(
    Path("contacts/contacts_live.csv").read_text(encoding="utf-8-sig").splitlines()
))
goa_rows = [r for r in rows
    if "goa" in str(r.get("tags","") + r.get("case","") + r.get("source","")).lower()
    or "goa" in str(r.get("name","") + r.get("designation","")).lower()]
new_press = [r["email"].strip() for r in goa_rows
    if EMAIL_RE.match(r["email"].strip())
    and r["email"].lower() not in existing
    and r["email"].lower() not in sup
    and "press" in r.get("category","").lower()]

seen_all=set(); all_press=[]
for e in ex_press + new_press:
    if e.lower() not in seen_all:
        seen_all.add(e.lower())
        all_press.append(e)

print(f"Press contacts: {len(all_press)}")

def send_batch(subject, body, bcc):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = FROM_ADDR
    msg["Cc"]      = CC_INFO
    msg["Bcc"]     = ", ".join(bcc)
    msg.attach(MIMEText(body, "plain", "utf-8"))
    rcpts = [FROM_ADDR, CC_INFO] + list(bcc)
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())

SUBJ = ("PRESS ALERT | Siolim Noise Case: GSPCB Failed to Attend Its Own Inspection "
        "| 4 Months of Silence + Now a No-Show | Please Investigate")

MAILER = """\
Dear Editor / Reporter,

We are following up on the Siolim noise-pollution case we wrote to
you about earlier this week. There is a new and significant development
that we believe warrants press investigation.

The Goa State Pollution Control Board (GSPCB) did not attend the
joint inspection on Wednesday 17 June 2026.

They had been formally notified of the inspection 9 days in advance.
They were the co-inspecting authority named in the Panchayat notice.
They did not send anyone.

This is now the story. Please read the full account below.

Contact us at info@pressdetective.com or reply to this email.
Evidence packet (26 pages) available immediately on request.
The resident is available for interview.

-----------------------------------------------------------------

PRESS ALERT | 19 June 2026

GSPCB FAILS TO ATTEND FORMAL INSPECTION —
SIOLIM NOISE CASE NOW A STORY OF REGULATORY FAILURE

-----------------------------------------------------------------

WHAT HAPPENED

On Wednesday 17 June 2026, a formal joint site inspection of the
"Sunday Racquet and Social Club," House No. 47/3, Sodiem, Siolim
was scheduled for 11:30 AM at the Village Panchayat Siolim-Sodiem
office.

The inspection was called by the Village Panchayat Siolim-Sodiem
under Inspection Notice Ref. VPSS/2026-27/site insp/648 (dated
08 June 2026). The co-inspecting authority named in that notice
was the Goa State Pollution Control Board.

The GSPCB did not attend.

-----------------------------------------------------------------

THE TIMELINE OF GSPCB'S FAILURES

  9 March 2026:
    Olympio Almeida, 70, a senior citizen resident of Siolim, filed
    a formal noise-pollution complaint with GSPCB. The complaint
    documented noise at 68-75 dB(A) from commercial padel courts
    operating in a residential zone -- 13-20 dB above the 55 dB(A)
    legal limit (Noise Pollution Rules 2000).

    It included decibel measurements with timestamps, photographs,
    legal citations, and a formal request for inspection.

  March -- June 2026 (3 months):
    GSPCB sent no acknowledgement.
    GSPCB sent no receipt.
    GSPCB sent no inspector.
    GSPCB sent no reply of any kind.

  8 June 2026:
    The Village Panchayat Siolim-Sodiem issued Inspection Notice
    VPSS/2026-27/site insp/648 formally calling a joint inspection
    for 17 June 2026 at 11:30 AM. GSPCB was a named co-inspecting
    authority in this notice.

  17 June 2026:
    The inspection took place at the Village Panchayat office.
    GSPCB did not attend.

  19 June 2026 (today):
    4 months and 10 days since the formal complaint.
    GSPCB has still not communicated with the complainant.

-----------------------------------------------------------------

THE COMPLAINT ITSELF

Olympio Almeida is 70 years old. He lives at La Masseria, Survey
No. 197/A, Sodiem, Siolim. He has lived there for decades. Next
door, the "Sunday Racquet and Social Club" operates outdoor
commercial padel tennis courts.

Noise from those courts, measured from his property, runs at 68
to 75 decibels. The legal residential limit is 55 decibels.

There is also an 18-year-old Panchayat licence-revocation order
from 2008 -- issued on Almeida's original complaint about
unauthorised construction on the same plot. That order has never
been enforced. Not once.

"I am 70 years old. I bought my home in Siolim for peace and
quiet. All I want is for the law to be enforced. The 2008 order
exists. The complaint exists. The inspection notice exists. And
the pollution board still didn't come."
-- Olympio Almeida

-----------------------------------------------------------------

WHY THIS IS AN INVESTIGATIVE STORY

The Goa State Pollution Control Board is a statutory authority
created under the Environment Protection Act 1986. It exists
specifically to respond to noise and pollution complaints. The
Board has enforcement powers. It has inspection powers. It has
a legal duty to act on complaints.

What GSPCB has demonstrably done in this case:

  -- Failed to acknowledge a formal complaint for 4+ months
  -- Failed to respond in any form for 4+ months
  -- Failed to appear at a formal joint inspection despite
     receiving 9 days' advance notice from the Panchayat

Questions for your investigation:

  1. Did GSPCB receive the Panchayat inspection notice
     VPSS/2026-27/site insp/648 dated 08 June 2026?

  2. Which GSPCB officer is responsible for handling noise
     complaints in North Goa?

  3. Why was no inspector sent to the 17 June joint inspection?

  4. What is the current status of the complaint filed on
     9 March 2026?

  5. Under what authority can a statutory board simply ignore
     a formal complaint for 4 months -- and then not attend
     an inspection it was notified about?

Call GSPCB's North Goa office. Ask them directly. We would very
much like to know their answer.

-----------------------------------------------------------------

ALSO ON THE RECORD: MLA SIOLIM HAS NOT RESPONDED

MLA Siolim, Ms. Delilah Lobo, has been formally written to on
multiple occasions over the past two weeks. Her direct email
addresses were used. Her constituency includes Sodiem, the
affected neighbourhood. Her constituents include senior citizens
suffering from this noise every weekend.

As of today -- 19 June 2026 -- her office has not responded.

-----------------------------------------------------------------

WHAT DID HAPPEN AT THE INSPECTION

The Village Panchayat Siolim-Sodiem and the complainant attended.
The Superintendent of Police (SPCR), Panaji had formally
acknowledged the complaint on 16 June and forwarded it for police
action -- the first and only meaningful government response in
four months.

-----------------------------------------------------------------

RTI FILED / TO BE FILED

A Right to Information application is being prepared to GSPCB
demanding:

  -- Confirmation of receipt of the 9 March 2026 complaint
  -- Name and designation of the officer assigned to the complaint
  -- Reason for non-attendance at the 17 June inspection
  -- Current status and next steps

The RTI response (or non-response) will itself become a matter
of public record.

-----------------------------------------------------------------

FOR REPORTERS: EVIDENCE AVAILABLE

Reply to this email for immediate access to the full 26-page
evidence packet:

  1. Decibel measurements with timestamps and location
  2. Photographs -- courts, proximity to homes
  3. 2008 Panchayat licence-revocation order (full document)
  4. 9 March 2026 GSPCB complaint (full text)
  5. Panchayat inspection notice VPSS/2026-27/site insp/648
  6. SP (SPCR) acknowledgement letter -- 16 June 2026

The complainant is available for interview.
All documents are genuine and verifiable.

Contact: info@pressdetective.com
         olympio.almeida@pressdetective.com

-----------------------------------------------------------------

This is a story about whether Goa's environmental enforcement
machinery actually works for the ordinary resident -- or whether
it only functions on paper.

The facts are on the record. We ask you to investigate.

Olympio Almeida
Siolim, Goa
olympio.almeida@pressdetective.com
---
Reply UNSUBSCRIBE to stop receiving updates on this matter.
"""

batches = [all_press[i:i+45] for i in range(0, len(all_press), 45)]
ok = 0
print(f"\nSending GSPCB no-show alert to {len(all_press)} press in {len(batches)} batches...\n")
for i, b in enumerate(batches, 1):
    try:
        send_batch(SUBJ, MAILER, b)
        print(f"  batch {i}/{len(batches)} OK ({len(b)})")
        ok += 1
    except Exception as e:
        print(f"  batch {i}/{len(batches)} FAIL: {e}")
    if i < len(batches):
        time.sleep(5)

print(f"\n{'='*60}")
print(f"GSPCB NO-SHOW PRESS ALERT")
print(f"  FROM:    {FROM_ADDR}")
print(f"  Batches: {ok}/{len(batches)} OK")
print(f"  Total:   {len(all_press)} Goa press contacts")
