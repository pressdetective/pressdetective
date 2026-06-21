"""
Final press follow-up — direct ask for publication. All 229 Goa press.
FROM olympio.almeida@pressdetective.com via Proton remote SMTP.

    python clients/olympio-almeida/olympio_appeal/send_press_publish_ask.py
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

sup = set()
# Load suppression from the live CSV
sup_csv = Path("contacts/suppression_list.csv")
if sup_csv.exists():
    for row in csv.DictReader(sup_csv.read_text(encoding="utf-8-sig").splitlines()):
        e = row.get("email","").strip().lower()
        if e:
            sup.add(e)
# Hard-coded dead/bounced addresses from prior sends
sup.update(e.lower() for e in [
    "anto.dias@timesgroup.com","goa.city@timesgroup.com","goa.online@timesgroup.com",
    "goa.toi@timesgroup.com","hcnscript@gmail.com","kanzilrodrigues@gmail.com",
    "nolasco.dsouza@timesgroup.com","pankaj.sharma@timesgroup.com","sanjay123@gmail.com",
    "timesarunsinha3000@gmail.com","timesofindia.goa@timesgroup.com",
    ".gvs@gov.in","tn@berkeley.edu","ctcourt-mazgoan@bhc.gov.in",
])
print(f"Suppression list: {len(sup)} addresses")

EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

rows = list(csv.DictReader(
    Path("contacts/contacts_live.csv").read_text(encoding="utf-8-sig").splitlines()
))
goa_rows = [r for r in rows
    if "goa" in str(r.get("tags","") + r.get("case","") + r.get("source","")).lower()
    or "goa" in str(r.get("name","") + r.get("designation","")).lower()]

seen_all=set(); all_press=[]
for r in goa_rows:
    e = r.get("email","").strip()
    cat = r.get("category","").lower()
    if (EMAIL_RE.match(e)
            and e.lower() not in sup
            and e.lower() not in seen_all
            and ("press" in cat or "media" in cat or "journalist" in cat or "other" in cat)):
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

SUBJ = ("FOLLOW-UP | Please Publish This Story — Siolim: Pollution Board No-Show "
        "| 18 Years, No Enforcement | Senior Resident Needs Press Help | Article Inside")

MAILER = """\
Dear Editor / Reporter,

This is a follow-up from Olympio Almeida, a 70-year-old resident of
Siolim, Goa. I have written to you before. I am writing again because
I need the press to help me and I am asking directly: will you publish
this story?

I will keep this short and give you everything.


IN ONE PARAGRAPH:

I am a senior citizen. Commercial padel courts were built next door
to my home in a residential zone. The noise hits 72 decibels -- 17
above the legal limit. A Panchayat order to shut them down was
issued in 2008 and never enforced. I filed a formal complaint with
the Goa Pollution Control Board on 9 March 2026. They never replied.
A joint inspection was held on 17 June 2026. They did not come. The
only government body that responded was the police. The MLA has
not replied. I am 70 years old and I cannot sit in my garden.


THE LATEST DEVELOPMENT:

On 17 June 2026 a formal joint inspection was scheduled at 11:30 AM
at the Village Panchayat Siolim-Sodiem office. The GSPCB -- named
as the co-inspecting authority -- was given 9 days' advance notice
under official notice VPSS/2026-27/site insp/648.

GSPCB did not attend.

This is 104 days after my formal complaint to them. They have not
sent a single word in response. And when the Panchayat called them
to a formal inspection, they still did not come.

Call GSPCB and ask them why. That conversation -- whatever they say
or refuse to say -- is a story.


MY QUOTE:

"I am 70 years old. I bought my home in Siolim for peace and quiet.
The noise is 72 decibels. The limit is 55. There is a 2008 order
saying those courts should be shut -- it was never enforced. I filed
a complaint with the pollution board four months ago. They didn't
reply. They didn't come to the inspection. What more can I do?
I am asking the press: please help me. Please write about this."
-- Olympio Almeida, Siolim


FOUR ANGLES FOR YOUR STORY:

  1. HUMAN INTEREST: A 70-year-old cannot sit in his garden. He
     has been fighting this for 18 years. He has the documents.
     He has the noise readings. He attended the inspection himself.
     And the regulatory board still didn't come.

  2. REGULATORY FAILURE: GSPCB had a legal duty to respond to a
     formal complaint. It did not. It had an obligation to attend
     an inspection. It did not. Is this how the Goa Pollution
     Control Board treats residents? How many others are waiting?

  3. THE 2008 ORDER: A Panchayat can issue a licence-revocation
     order and have it ignored for 18 years without consequence.
     What enforcement mechanism exists? Who is accountable?

  4. POLITICAL ACCOUNTABILITY: MLA Siolim Delilah Lobo has not
     responded to formal written appeals from a constituent in
     her own ward. Is this acceptable?


WHAT I NEED FROM YOU:

  -- Publish the story, OR
  -- Tell me you are looking into it, OR
  -- Tell me who at your publication covers environment / civic
     affairs / North Goa and I will write to them directly.

Even a reply saying "received, we'll look at it" is meaningful.


EVIDENCE PACKET (26 pages) -- reply and I send immediately:

  1. Noise readings -- timestamped, with coordinates
  2. Photographs of courts and their distance from homes
  3. 2008 Panchayat licence-revocation order (full scan)
  4. 9 March 2026 GSPCB complaint (full text)
  5. Panchayat inspection notice VPSS/2026-27/site insp/648
  6. SP (SPCR) Panaji formal acknowledgement, 16 June 2026

I am available for interview. I can show you the site.


--------------------------------------------------------------
PRESS RELEASE (for your files)
--------------------------------------------------------------

FOR IMMEDIATE RELEASE -- 21 June 2026
Siolim, Goa
Contact: olympio.almeida@pressdetective.com | info@pressdetective.com


GSPCB FAILS TO ATTEND FORMAL INSPECTION -- SIOLIM RESIDENT'S
NOISE COMPLAINT NOW 104 DAYS OLD WITH NO RESPONSE

Joint inspection of padel court noise and encroachment held
17 June at VP Siolim-Sodiem; pollution board absent despite
9 days' advance notice from Panchayat; 18-year-old order
still unenforced; MLA constituency response still pending.


SIOLIM, GOA -- The Goa State Pollution Control Board failed to
attend a formal joint inspection of a residential noise-pollution
complaint on 17 June 2026, more than 100 days after the complaint
was filed and despite formal advance notice issued by the Village
Panchayat Siolim-Sodiem.

The complainant, Olympio Almeida, 70, resident of La Masseria,
Survey No. 197/A, Sodiem, Siolim, filed a detailed noise-pollution
complaint with GSPCB on 9 March 2026. The complaint documented
noise at 68-75 dB(A) from the "Sunday Racquet and Social Club"
-- commercial padel courts operating at House No. 47/3, Gaunsawaddo,
Sodiem -- against a residential legal limit of 55 dB(A).

GSPCB sent no acknowledgement, no receipt and no response of any
kind in the 104 days since the complaint was filed.

The Village Panchayat Siolim-Sodiem issued Inspection Notice
VPSS/2026-27/site insp/648 on 8 June 2026, formally notifying
GSPCB of a joint inspection to be held at 11:30 AM on 17 June
2026. GSPCB did not send a representative.

The complainant and Panchayat representatives attended the
inspection. The Superintendent of Police (SPCR), Panaji had
formally acknowledged the complaint on 16 June 2026 and forwarded
it for police action -- the only government response received in
four months.

MLA Siolim, Ms. Delilah Lobo, whose constituency includes Sodiem,
has been formally written to on multiple occasions between 6 and
19 June 2026. Her office has not responded.

The case also involves a 2008 Panchayat licence-revocation order
for the same plot, issued on the complainant's original complaint
about unauthorised construction. That order has not been enforced
in 18 years.

An RTI application is being prepared demanding GSPCB confirm
receipt of the complaint, identify the officer responsible, and
explain the non-attendance at the 17 June inspection.

The complainant is available for interview. A 26-page evidence
packet is available immediately on request.

CONTACT:
Olympio Almeida -- olympio.almeida@pressdetective.com
Press enquiries -- info@pressdetective.com

--------------------------------------------------------------

Thank you for reading. I hope you will tell this story. It is
true, it is documented, and it matters to every Goa resident who
has ever filed a complaint and waited in silence for an answer.

Olympio Almeida
Siolim, Goa
olympio.almeida@pressdetective.com
---
Reply UNSUBSCRIBE to stop receiving updates on this matter.
"""

batches = [all_press[i:i+45] for i in range(0, len(all_press), 45)]
ok = 0
print(f"\nSending final publish-ask to {len(all_press)} press in {len(batches)} batches...\n")
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
print(f"FINAL PUBLISH ASK SENT")
print(f"  FROM:    {FROM_ADDR}")
print(f"  Batches: {ok}/{len(batches)} OK")
print(f"  Total:   {len(all_press)} Goa press contacts")
