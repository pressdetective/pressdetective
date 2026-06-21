"""
Send press release to remaining 49 Goa press contacts (batch 5+6)
via olympio.almeida@pressdetective.com remote SMTP.

    python clients/olympio-almeida/olympio_appeal/send_press_release_remainder.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import csv, json, re, smtplib, ssl, uuid, datetime, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
HERE  = Path(__file__).parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
CC_INFO   = "info@pressdetective.com"

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
for e in ex_press+new_press:
    if e.lower() not in seen_all: seen_all.add(e.lower()); all_press.append(e)

# Only the 49 contacts that failed (index 180 onwards)
remaining = all_press[180:]
print(f"Remaining press contacts: {len(remaining)}")

def make_ics():
    DTSTAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ICS = "\r\n".join([
        "BEGIN:VCALENDAR","VERSION:2.0",
        "PRODID:-//PressDetective//Olympio Almeida//EN",
        "CALSCALE:GREGORIAN","METHOD:REQUEST","BEGIN:VEVENT",
        f"UID:{uuid.uuid4()}",f"DTSTAMP:{DTSTAMP}",
        "DTSTART:20260617T060000Z","DTEND:20260617T080000Z",
        "SUMMARY:TODAY 11:30 AM — Siolim Noise Inspection | Press Welcome",
        "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
        "DESCRIPTION:Joint inspection VP Siolim-Sodiem + GSPCB. Press invited to attend and cover.",
        f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
        "STATUS:CONFIRMED","SEQUENCE:7",
        "BEGIN:VALARM","TRIGGER:-PT60M","ACTION:DISPLAY",
        "DESCRIPTION:Siolim inspection 1 hour","END:VALARM",
        "END:VEVENT","END:VCALENDAR",
    ])
    p = MIMEBase("text","calendar",method="REQUEST",charset="utf-8")
    p.set_payload(ICS.encode("utf-8")); encoders.encode_base64(p)
    p.add_header("Content-Disposition","attachment",filename="siolim_inspection_press.ics")
    return p

SUBJ = ("PRESS RELEASE | Siolim: Police Respond After 18 Years of Unenforced Order "
        "| Joint Inspection TODAY 11:30 AM | Story & Evidence Available")

PR = """\
FOR IMMEDIATE RELEASE
17 June 2026 | Siolim, Goa
Contact: olympio.almeida@pressdetective.com | info@pressdetective.com
Evidence packet (26 pages) available on request — reply to this email.


POLICE RESPOND TO SIOLIM SENIOR CITIZEN'S NOISE COMPLAINT —
JOINT INSPECTION TAKES PLACE TODAY AT 11:30 AM

18-year-old Panchayat revocation order still unenforced; GSPCB
silent for 3 months; MLA Siolim has not responded.


SIOLIM, GOA — In a significant development overnight, the Office of
the Superintendent of Police (SPCR), Panaji has formally acknowledged
a noise-pollution complaint from a 70-year-old Siolim resident and
forwarded the matter for necessary police action.

The inspection — called by Village Panchayat Siolim-Sodiem, co-conducted
by GSPCB — takes place TODAY at 11:30 AM. Press are welcome to attend.

  WHEN:  TODAY, Wednesday 17 June 2026 — 11:30 AM
  WHERE: Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa


THE COMPLAINANT

Olympio Almeida, 70, resident of La Masseria, Survey No. 197/A, Siolim.
Next door: "Sunday Racquet and Social Club" — outdoor commercial padel
courts in a residential zone. Noise measured at 68-75 dB(A). Legal
limit: 55 dB(A). Excess: 13-20 dB above the law.

"I am 70 years old. I bought my home in Siolim for peace and quiet.
For years we could not sit in our own garden. When I measured the
noise it read 72 decibels. All I want is for the law to be enforced."
— Olympio Almeida


AN 18-YEAR-OLD ORDER NEVER ENFORCED

The Siolim-Sodiem Panchayat issued a formal licence-revocation order
against this plot in 2008 — on Almeida's own complaint. It has never
been enforced. 18 years later, the operations continue at full volume.
Almeida also documents encroachment on his own land (Survey No. 197/A).


GSPCB COMPLAINT — 3 MONTHS, NO RESPONSE

On 9 March 2026, Almeida filed a formal GSPCB complaint with noise
measurements, photographs, and legal citations. As of today — more than
three months later — GSPCB has sent no acknowledgement, no inspector,
no response of any kind.


OVERNIGHT: POLICE RESPOND

On 16 June 2026, the SP (SPCR) Panaji formally acknowledged the complaint
and forwarded it for police action — the first meaningful government
response since the GSPCB complaint was filed in March.

MLA Siolim, Ms. Delilah Lobo, has been contacted repeatedly this week
with personal appeals. As of this morning, no response has been received.


THE STORY FOR GOA'S PRESS

Can a Panchayat revocation order be ignored for 18 years? What recourse
does a senior citizen have when GSPCB doesn't respond for 3 months?
Does Goa's noise law protect residents in residential zones — or only
on paper? Will the MLA respond when a constituent asks for help?

TODAY'S INSPECTION is the moment to find out. Come. Observe. Report.
Bring a phone with a decibel app (NIOSH SLM or Decibel X, both free)
and measure the noise yourself.


EVIDENCE AVAILABLE (26 pages) — reply to this email for immediate access:

  1. Decibel measurements with timestamps and location data
  2. Photographs — courts and their proximity to homes
  3. 2008 Panchayat licence-revocation order (full document)
  4. March 2026 GSPCB complaint (full text and submission record)
  5. Panchayat inspection notice VPSS/2026-27/site insp/648
  6. SP (SPCR) formal acknowledgement — 16 June 2026

Complainant available for interview. All documents genuine and verifiable.


BRIEF CHRONOLOGY

  Pre-2008:      Club begins operations in residential zone
  2008:          Panchayat issues licence-revocation order — never enforced
  9 March 2026:  Formal GSPCB complaint filed
  March-June:    GSPCB silent — no acknowledgement, no inspection
  8 June 2026:   VP Siolim-Sodiem issues joint inspection notice
  16 June 2026:  SP (SPCR) Panaji formally responds; forwards for action
  16 June 2026:  MLA Siolim (Delilah Lobo) — still no response
  17 June 2026:  INSPECTION TODAY at 11:30 AM


CONTACT

  Olympio Almeida — complainant
  Email: olympio.almeida@pressdetective.com
  Press: info@pressdetective.com

[Calendar invite attached. Add to calendar and come today.]
"""

batches = [remaining[i:i+45] for i in range(0, len(remaining), 45)]
ok = 0
print(f"Sending to {len(remaining)} remaining contacts in {len(batches)} batch(es) ...")
for i, b in enumerate(batches, 1):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = SUBJ
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = FROM_ADDR
    msg["Cc"]      = CC_INFO
    msg["Bcc"]     = ", ".join(b)
    msg.attach(MIMEText(PR, "plain", "utf-8"))
    msg.attach(make_ics())
    rcpts = [FROM_ADDR, CC_INFO] + list(b)
    ctx = ssl.create_default_context()
    try:
        with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
            s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())
        print(f"  batch {i}/{len(batches)} OK ({len(b)})"); ok += 1
    except Exception as e:
        print(f"  batch {i}/{len(batches)} FAIL: {e}")
    if i < len(batches): time.sleep(4)

print(f"\nRemainder press release: {ok}/{len(batches)} batches OK — FROM @pressdetective.com")
