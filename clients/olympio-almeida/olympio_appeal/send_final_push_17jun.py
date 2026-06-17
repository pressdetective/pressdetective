"""
FINAL PRE-INSPECTION PUSH — Wednesday 17 June 2026, 11:30 AM
Sends email + .ics calendar invite to ALL segments via Proton remote SMTP.
Segments: Police | Departments | MLAs | Press + Civic
Gautam gets a dedicated full update.

    python clients/olympio-almeida/olympio_appeal/send_final_push_17jun.py

DNS status (verified 16 Jun): DMARC p=none (1 record) + SPF + DKIM all passing.
NIC/gov.in/goapolice.gov.in remain policy-blocked at their gateway — we send
anyway so the attempt is on record; gmail-hosted addresses in every segment will
deliver fine.
"""
import json, smtplib, ssl, uuid, datetime, time
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
assert FROM_ADDR.endswith("@pressdetective.com"), "PressDetective only"

# ── combined suppression (dead only — not policy-blocked) ─────────────────────
def load_dead(*paths):
    dead = set()
    for p in paths:
        p = HERE / p
        if p.exists():
            data = json.loads(p.read_text())
            dead.update(e.lower() for e in data.keys())
    return dead

sup = load_dead("suppress_14june.json", "dead_14june.json", "newdead_followup.json")
# 11 new dead confirmed today (16 Jun bounce forensics)
TODAY_DEAD = {
    "anto.dias@timesgroup.com","goa.city@timesgroup.com","goa.online@timesgroup.com",
    "goa.toi@timesgroup.com","hcnscript@gmail.com","kanzilrodrigues@gmail.com",
    "nolasco.dsouza@timesgroup.com","pankaj.sharma@timesgroup.com","sanjay123@gmail.com",
    "timesarunsinha3000@gmail.com","timesofindia.goa@timesgroup.com",
}
sup.update(e.lower() for e in TODAY_DEAD)

def clean(lst):
    seen = set(); out = []
    for e in lst:
        el = e.lower().strip()
        if el not in sup and el not in seen:
            seen.add(el); out.append(e)
    return out

# ── audience ──────────────────────────────────────────────────────────────────
aud = json.loads((HERE / "audience_14june.json").read_text())

# Police — dedicated segment (all goapolice.gov.in addresses)
POLICE = [e for e in aud["depts"] if "goapolice.gov.in" in e.lower()]
police = clean(POLICE)

# Departments (non-police gov addresses)
NON_POLICE_DEPTS = [e for e in aud["depts"] if "goapolice.gov.in" not in e.lower()]
depts = clean(NON_POLICE_DEPTS)

# MLAs
MLA_LIST = [
    "delilahlobo.goa@gmail.com",         # Siolim MLA — KEY jurisdiction
    "delilahlobosiolimoffice@gmail.com",  # Siolim MLA office
    "vijaisardesai@gmail.com",            # Fatorda MLA / GFP leader
    "drdeviyarane.mla.poriem@gmail.com",
    "mlashetye03bicholim@gmail.com",
    "pravinarlekar4pernem@gmail.com",
    "sec-legi.goa@nic.in",               # Goa Legislature Secretariat
    "mla.mandrem.gvs@gov.in",
    "mla.tivim.gvs@gov.in",
    "mla.calangute.gvs@gov.in",
    "mla.mapusa.gvs@gov.in",
    "mla.porvorim.gvs@gov.in",
]
mlas = clean(MLA_LIST)

# Press + civic combined (BCC batches)
press_civic = clean(aud["press"] + aud["other"])

print(f"Audience (cleaned, dead suppressed):")
print(f"  Police:      {len(police)}")
print(f"  Departments: {len(depts)}")
print(f"  MLAs:        {len(mlas)}")
print(f"  Press+civic: {len(press_civic)}")
print(f"  Total:       {len(police)+len(depts)+len(mlas)+len(press_civic)}")

# ── .ics calendar invite ──────────────────────────────────────────────────────
DTSTART = "20260617T060000Z"   # 11:30 AM IST = 06:00 UTC
DTEND   = "20260617T080000Z"   # 01:30 PM IST = 08:00 UTC
DTSTAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
UID     = str(uuid.uuid4())

ICS = "\r\n".join([
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//PressDetective//Olympio Almeida//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:REQUEST",
    "BEGIN:VEVENT",
    f"UID:{UID}",
    f"DTSTAMP:{DTSTAMP}",
    f"DTSTART:{DTSTART}",
    f"DTEND:{DTEND}",
    "SUMMARY:TOMORROW — Joint Site Inspection 11:30 AM Siolim (17 June 2026)",
    "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
    "DESCRIPTION:Joint site inspection by VP Siolim-Sodiem + GSPCB"
    " (Notice VPSS/2026-27/site insp/648\\, 08 June 2026).\\n"
    "Sunday Racquet and Social Club — padel courts at House No. 47/3\\,"
    " Gaunsawaddo\\, Sodiem\\, Siolim (Survey No. 197/7).\\n"
    "Noise: 68-75 dB(A) vs 55 dB(A) limit. GSPCB complaint 9 March 2026.\\n"
    "Arrive by 11:15 AM. All departments + police requested to depute a rep.",
    f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
    "STATUS:CONFIRMED",
    "SEQUENCE:1",
    "BEGIN:VALARM",
    "TRIGGER:-PT120M",
    "ACTION:DISPLAY",
    "DESCRIPTION:Inspection in 2 hours — depart now",
    "END:VALARM",
    "BEGIN:VALARM",
    "TRIGGER:-PT30M",
    "ACTION:DISPLAY",
    "DESCRIPTION:Inspection starts in 30 minutes",
    "END:VALARM",
    "END:VEVENT",
    "END:VCALENDAR",
])

def make_ics():
    p = MIMEBase("text", "calendar", method="REQUEST", charset="utf-8")
    p.set_payload(ICS.encode("utf-8"))
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment",
                 filename="inspection_17june2026.ics")
    return p

# ── send helper ───────────────────────────────────────────────────────────────
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
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, msg.as_bytes())

def run_segment(label, addresses, subject, body, batch_size=45):
    batches = [addresses[i:i+batch_size] for i in range(0, len(addresses), batch_size)]
    ok = 0
    print(f"\n[{label}] {len(addresses)} recipients, {len(batches)} batch(es)...")
    for i, b in enumerate(batches, 1):
        try:
            send_batch(subject, body, b)
            print(f"  batch {i}/{len(batches)} OK ({len(b)})")
            ok += 1
        except Exception as e:
            print(f"  batch {i}/{len(batches)} FAIL: {e}")
        if i < len(batches):
            time.sleep(4)
    return ok, len(batches)

SIG = """
Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  |  Press: info@pressdetective.com
"""

# ── POLICE ────────────────────────────────────────────────────────────────────
POLICE_SUBJ = "URGENT — Police Presence Requested: Joint Site Inspection TOMORROW Wednesday 17 June 2026, 11:30 AM, Siolim [Calendar Invite Attached]"
POLICE_BODY = f"""\
To the Superintendent of Police / Station House Officer / Concerned Officer,

A calendar invite is attached. Please click "Add to Calendar" to save the event.

JOINT SITE INSPECTION — TOMORROW
  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat Siolim-Sodiem (Notice Ref. VPSS/2026-27/site insp/648,
dated 08 June 2026) and the Goa State Pollution Control Board are conducting
a joint site inspection of the "Sunday Racquet and Social Club" — outdoor
padel courts operating commercially at House No. 47/3, Gaunsawaddo, Sodiem,
Siolim in a residential zone.

The matter involves:
  - Noise pollution: 68-75 dB(A) measured against the 55 dB(A) residential
    limit under the Noise Pollution (Regulation & Control) Rules, 2000
  - Unauthorised commercial use in a residential zone
  - Encroachment on private land (Survey No. 197/A)
  - Non-enforcement of a 2008 Panchayat licence-revocation order on
    Survey No. 197/7 (same plot)

Senior citizen residents have been suffering for years. A complaint was filed
with GSPCB on 9 March 2026 — it remains unanswered.

We respectfully request the police to:
  1. Depute an officer to attend tomorrow's joint inspection at 11:30 AM.
  2. Bring any records relating to prior complaints at this address.
  3. Ensure the inspection proceeds without interference.
{SIG}"""

# ── DEPARTMENTS ───────────────────────────────────────────────────────────────
DEPT_SUBJ = "FINAL NOTICE — Joint Inspection TOMORROW Wednesday 17 June 2026, 11:30 AM, Siolim | Please Depute a Rep [Calendar Invite]"
DEPT_BODY = f"""\
To the concerned Department / Authority,

A calendar invite is attached. Please click "Add to Calendar" to save the event.

JOINT SITE INSPECTION — TOMORROW
  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

This is a final reminder. The inspection was called by Village Panchayat
Siolim-Sodiem (Notice Ref. VPSS/2026-27/site insp/648, 08 June 2026) for
the "Sunday Racquet and Social Club" — outdoor padel courts at Gaunsawaddo,
Sodiem, Siolim — operating in a residential zone with:
  - Noise: 68-75 dB(A) vs the 55 dB(A) residential limit
  - Encroachment on adjoining private land
  - A 2008 Panchayat licence-revocation order (same plot) still unenforced
  - GSPCB complaint filed 9 March 2026, no response received

Your department is requested to:
  1. Depute a representative to attend the inspection at 11:30 AM tomorrow.
  2. Bring the departmental record (consent-to-operate / land-use / survey
     position / prior complaints, as applicable to your department).
  3. Place your department's response to the 9 March 2026 complaint on record.
{SIG}"""

# ── MLAs ──────────────────────────────────────────────────────────────────────
MLA_SUBJ = "Your Presence Requested TOMORROW — Siolim Inspection Wednesday 17 June, 11:30 AM | Please Attend or Depute [Calendar Invite]"
MLA_BODY = f"""\
To the Honourable Member of the Goa Legislative Assembly,

A calendar invite is attached. Please click "Add to Calendar" to save the event.

JOINT SITE INSPECTION — TOMORROW
  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat Siolim-Sodiem + Goa State Pollution Control Board
are conducting a joint inspection of the "Sunday Racquet and Social Club" —
outdoor padel courts at Gaunsawaddo, Sodiem, Siolim — with measured noise
of 68-75 dB(A) against the 55 dB(A) residential limit, encroachment, and
a 2008 Panchayat licence-revocation order still unenforced.

As our elected representative, we respectfully request you to:
  1. Attend or depute a representative to the inspection at 11:30 AM tomorrow.
  2. State your position on noise-pollution and land-use enforcement.
  3. Raise the long-pending GSPCB complaint (9 March 2026) with the relevant
     authorities and follow through on enforcement.

Residents are senior citizens who have endured years of disruption. Tomorrow
is the formal opportunity for the system to act.
{SIG}"""

# ── PRESS + CIVIC ─────────────────────────────────────────────────────────────
PRESS_SUBJ = "TOMORROW 11:30 AM — Siolim Racquet Club Inspection | Media Welcome | Wednesday 17 June [Updated Calendar Invite]"
PRESS_BODY = f"""\
Dear Editor / Colleague,

An updated calendar invite is attached for tomorrow's official inspection.
Please click "Add to Calendar" — reminders are pre-set.

JOINT SITE INSPECTION — TOMORROW
  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat Siolim-Sodiem and the Goa State Pollution Control Board
will conduct a joint inspection of the "Sunday Racquet and Social Club" — outdoor
padel courts at Gaunsawaddo, Sodiem, Siolim — operating commercially in a
residential area with:
  - Noise: 68-75 dB(A) against the 55 dB(A) residential limit
  - A 2008 Panchayat licence-revocation order (same plot) still unenforced
  - A GSPCB complaint filed March 2026 with no response to date
  - Encroachment on neighbouring private land

Departments, area MLAs, and police have been formally asked to attend.
Media are welcome to observe. A 26-page evidence packet is available on
request by return email.
{SIG}
---
Reply UNSUBSCRIBE to be removed from further updates.
"""

# ── execute all segments ──────────────────────────────────────────────────────
log = {}

r = run_segment("POLICE", police, POLICE_SUBJ, POLICE_BODY)
log["police"] = f"{r[0]}/{r[1]} batches, {len(police)} recipients"
time.sleep(4)

r = run_segment("DEPARTMENTS", depts, DEPT_SUBJ, DEPT_BODY)
log["depts"] = f"{r[0]}/{r[1]} batches, {len(depts)} recipients"
time.sleep(4)

r = run_segment("MLAs", mlas, MLA_SUBJ, MLA_BODY)
log["mlas"] = f"{r[0]}/{r[1]} batches, {len(mlas)} recipients"
time.sleep(4)

r = run_segment("PRESS+CIVIC", press_civic, PRESS_SUBJ, PRESS_BODY)
log["press_civic"] = f"{r[0]}/{r[1]} batches, {len(press_civic)} recipients"

(HERE / "finalpush_17jun_log.json").write_text(json.dumps(log, indent=2))
print(f"\n{'='*60}")
print("FINAL PUSH COMPLETE")
print(json.dumps(log, indent=2))
total = len(police)+len(depts)+len(mlas)+len(press_civic)
print(f"Total recipients attempted: {total}")
