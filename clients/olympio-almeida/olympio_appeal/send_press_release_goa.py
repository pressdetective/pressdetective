"""
PRESS RELEASE — All 229 Goa press contacts, 17 June 2026.
FROM olympio.almeida@protonmail.com via Proton Bridge.

    python clients/olympio-almeida/olympio_appeal/send_press_release_goa.py
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

FROM_ADDR = "olympio.almeida@protonmail.com"
FROM_NAME = "Olympio Almeida"
BRIDGE_PW = CREDS["accounts"]["olympio"]["bridge_password"]
CC_INFO   = "info@pressdetective.com"

# ── suppression ───────────────────────────────────────────────────────────────
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

seen_all = set()
all_press = []
for e in ex_press + new_press:
    if e.lower() not in seen_all:
        seen_all.add(e.lower())
        all_press.append(e)

print(f"Total press contacts: {len(all_press)} ({len(ex_press)} existing + {len(new_press)} new)")

# ── .ics ──────────────────────────────────────────────────────────────────────
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
        "DESCRIPTION:Siolim inspection — 1 hour","END:VALARM",
        "END:VEVENT","END:VCALENDAR",
    ])
    p = MIMEBase("text","calendar",method="REQUEST",charset="utf-8")
    p.set_payload(ICS.encode("utf-8")); encoders.encode_base64(p)
    p.add_header("Content-Disposition","attachment",filename="siolim_inspection_press.ics")
    return p

def send_batch(subject, body, bcc):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = FROM_ADDR
    msg["Cc"]      = CC_INFO
    msg["Bcc"]     = ", ".join(bcc)
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(make_ics())
    rcpts = [FROM_ADDR, CC_INFO] + list(bcc)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP("127.0.0.1", 1025, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, BRIDGE_PW)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())

# ═══════════════════════════════════════════════════════════════
# THE PRESS RELEASE
# ═══════════════════════════════════════════════════════════════

SUBJ = ("PRESS RELEASE | Siolim: Police Respond After 18 Years of Unenforced Order "
        "| Joint Inspection TODAY 11:30 AM | Story & Evidence Available")

PR = """\
FOR IMMEDIATE RELEASE
17 June 2026 | Siolim, Goa
Contact: olympio.almeida@protonmail.com | info@pressdetective.com
Evidence packet (26 pages) available on request — reply to this email.


POLICE RESPOND TO SIOLIM SENIOR CITIZEN'S NOISE COMPLAINT —
JOINT INSPECTION TAKES PLACE TODAY AT 11:30 AM

18-year-old Panchayat revocation order still unenforced; GSPCB
silent for 3 months; MLA Siolim has not responded.


SIOLIM, GOA — In a significant development overnight, the Office of
the Superintendent of Police (SPCR), Panaji has formally acknowledged
a noise-pollution complaint from a 70-year-old Siolim resident and
forwarded the matter for necessary police action.

The acknowledgement comes on the morning of a formal joint inspection
being conducted TODAY by the Village Panchayat Siolim-Sodiem and the
Goa State Pollution Control Board (GSPCB):

  WHAT:  Joint site inspection — noise pollution, encroachment
  WHEN:  TODAY, Wednesday 17 June 2026 — 11:30 AM
  WHERE: Village Panchayat Siolim-Sodiem office,
         Sodiem, Siolim, Bardez, Goa
  PRESS: Welcome to attend and cover

---

THE COMPLAINANT

Olympio Almeida, 70, has lived at La Masseria, Survey No. 197/A,
Sodiem, Siolim for decades. He is a senior citizen and retired
resident. Next door to his home, at House No. 47/3, Gaunsawaddo,
Sodiem, the "Sunday Racquet and Social Club" operates outdoor
commercial padel tennis courts in what is a residential zone.

The noise from those courts, measured from Almeida's property,
runs at 68 to 75 decibels.

India's Noise Pollution (Regulation and Control) Rules, 2000 set
the ambient noise standard for residential areas at 55 dB(A) during
daytime hours. The padel courts exceed this limit by 13 to 20
decibels on a regular basis.

"I am 70 years old. I bought my home in Siolim for peace and quiet.
For years we could not sit in our own garden. When I measured the
noise it read 72 decibels. My doctor says this level of sustained
noise causes permanent hearing damage. All I want is for the law to
be enforced." — Olympio Almeida

---

AN 18-YEAR-OLD PANCHAYAT ORDER THAT WAS NEVER ENFORCED

What makes this case particularly striking is that the Village
Panchayat Siolim-Sodiem issued a formal licence-revocation order
against the plot at Survey No. 197/7 as long ago as 2008 — on
Almeida's original complaint about unauthorised construction on that
plot.

That 2008 order has never been enforced. Eighteen years later, the
construction has continued, commercial operations run at full volume,
and the noise continues without interruption.

Almeida also documents ongoing encroachment onto his own private
land at Survey No. 197/A, adjacent to the club's operations.

---

THE GSPCB COMPLAINT

On 9 March 2026, Almeida filed a formal written complaint with the
Goa State Pollution Control Board, the statutory authority for
noise-pollution enforcement in Goa. The complaint:

  - Documented noise levels with measurements
  - Included timestamped photographs
  - Cited the Noise Pollution Rules 2000 and E.P. Act 1986
  - Identified the source (the padel courts)
  - Requested immediate inspection and enforcement

As of today — more than three months later — the GSPCB has not
acknowledged receipt of the complaint, sent an inspector to the site,
or communicated any response to the complainant.

---

THE INSPECTION — AND WHAT HAPPENED OVERNIGHT

After continued formal advocacy, the Village Panchayat Siolim-Sodiem
issued Inspection Notice Ref. VPSS/2026-27/site insp/648 dated
08 June 2026, calling a joint inspection with GSPCB.

On the evening of 16 June 2026, the Office of the Superintendent of
Police (SPCR), Panaji formally responded to the complaint and
forwarded it within the police department for necessary action —
described by the complainant as "the first meaningful response from
any government body since the GSPCB complaint was filed in March."

MLA Siolim, Ms. Delilah Lobo, has been contacted multiple times this
week with personal requests to attend or send a representative. As of
this morning, no response has been received from her office.

---

THE STORY FOR GOA'S PRESS

This is not simply a noise complaint. It raises questions that matter
to every Goan resident:

  - Can a Panchayat revocation order be ignored for 18 years
    without consequence?
  - What recourse does a senior citizen have when the GSPCB does
    not respond for three months to a documented complaint?
  - Does Goa's noise-pollution law actually protect residents in
    residential zones — or only on paper?
  - Will an MLA respond when a constituent asks for help?

TODAY'S INSPECTION is the moment to find out. Come and witness
whether the system works. Bring a decibel meter app (free: NIOSH SLM
or Decibel X). Speak to the resident. Read the 2008 order. Ask the
GSPCB officials why their March complaint went unanswered.

---

EVIDENCE AVAILABLE TO PRESS

A 26-page evidence packet is available on immediate request:

  1. Decibel measurements (multiple dates, timestamped, location data)
  2. Photographs of the courts and proximity to residential homes
  3. The 2008 Panchayat licence-revocation order (full document copy)
  4. The March 2026 GSPCB complaint (full text and submission record)
  5. Panchayat inspection notice VPSS/2026-27/site insp/648
  6. SP (SPCR) formal acknowledgement (received 16 June 2026)

Reply to this email for immediate access. All documents are genuine
and verifiable. The complainant is available for interview.

---

BRIEF CHRONOLOGY

  Pre-2008:      "Sunday Racquet and Social Club" begins operations
  2008:          Panchayat issues licence-revocation order on
                 Almeida's complaint. Order never enforced.
  2008–2026:     18 years of ongoing commercial operations and noise
  9 March 2026:  Almeida files formal GSPCB complaint
  March–June:    GSPCB silent — no acknowledgement, no inspection
  8 June 2026:   VP Siolim-Sodiem issues joint inspection notice
  9–16 June:     Formal notices sent to police, departments, MLAs
  16 June 2026:  SP (SPCR) Panaji formally responds; forwards for action
  16 June 2026:  MLA Siolim (Delilah Lobo) — still no response
  17 June 2026:  INSPECTION TODAY at 11:30 AM

---

CONTACT

  Olympio Almeida — complainant and resident
  Email:  olympio.almeida@protonmail.com
  Press:  info@pressdetective.com

  For interview, evidence packet, or further details — reply to this
  email. Response within the hour.

---

END OF PRESS RELEASE

Note: Calendar invite for the 11:30 AM inspection is attached.
Add it to your calendar and come today.
"""

batches = [all_press[i:i+45] for i in range(0, len(all_press), 45)]
ok = 0
print(f"Sending to {len(all_press)} contacts in {len(batches)} batches ...\n")
for i, b in enumerate(batches, 1):
    try:
        send_batch(SUBJ, PR, b)
        print(f"  batch {i}/{len(batches)} OK ({len(b)})")
        ok += 1
    except Exception as e:
        print(f"  batch {i}/{len(batches)} FAIL: {e}")
    if i < len(batches):
        time.sleep(5)

print(f"\n{'='*60}")
print(f"PRESS RELEASE — SENT")
print(f"  FROM:    {FROM_ADDR} via Proton Bridge")
print(f"  Batches: {ok}/{len(batches)} OK")
print(f"  Total:   {len(all_press)} Goa press contacts")
print(f"  Outlets: Herald, Navhind Times, The Goan, Tarun Bharat,")
print(f"           Prudent Media, HT Goa, News18, UNI India,")
print(f"           Loksatta, Sakal, The Statesman, Telegraph +200 more")
