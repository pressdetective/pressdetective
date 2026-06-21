"""
Full send from olympio.almeida@protonmail.com via Proton Bridge:
  1. Press + civic  — personal appeal + .ics (BCC batches 45)
  2. Departments    — reminder + .ics
  3. Police         — reminder + .ics
  4. MLAs           — reminder + .ics

    python clients/olympio-almeida/olympio_appeal/send_all_protonmail.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import json, smtplib, ssl, uuid, datetime, time
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

# ── bridge auth test ──────────────────────────────────────────────────────────
print(f"Auth test: {FROM_ADDR} via Bridge...")
bctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
bctx.check_hostname = False; bctx.verify_mode = ssl.CERT_NONE
with smtplib.SMTP("127.0.0.1", 1025, timeout=15) as s:
    s.ehlo(); s.starttls(context=bctx); s.login(FROM_ADDR, BRIDGE_PW)
print("  AUTH OK\n")

# ── suppression ───────────────────────────────────────────────────────────────
sup = set()
for fname in ("suppress_14june.json","dead_14june.json","newdead_followup.json"):
    sup.update(e.lower() for e in json.loads((HERE/fname).read_text()))
sup.update(e.lower() for e in [
    "anto.dias@timesgroup.com","goa.city@timesgroup.com","goa.online@timesgroup.com",
    "goa.toi@timesgroup.com","hcnscript@gmail.com","kanzilrodrigues@gmail.com",
    "nolasco.dsouza@timesgroup.com","pankaj.sharma@timesgroup.com","sanjay123@gmail.com",
    "timesarunsinha3000@gmail.com","timesofindia.goa@timesgroup.com",
])

aud = json.loads((HERE/"audience_14june.json").read_text())
def clean(lst):
    seen=set(); out=[]
    for e in lst:
        el=e.lower().strip()
        if el not in sup and el not in seen: seen.add(el); out.append(e)
    return out

press_civic = clean(aud["press"] + aud["other"])
depts       = clean([e for e in aud["depts"] if "goapolice.gov.in" not in e.lower()])
police      = clean([e for e in aud["depts"] if "goapolice.gov.in" in e.lower()])
mlas        = clean([
    "delilahlobo.goa@gmail.com","delilahlobosiolimoffice@gmail.com",
    "vijaisardesai@gmail.com","drdeviyarane.mla.poriem@gmail.com",
    "mlashetye03bicholim@gmail.com","pravinarlekar4pernem@gmail.com",
    "sec-legi.goa@nic.in","mla.mandrem.gvs@gov.in","mla.tivim.gvs@gov.in",
    "mla.calangute.gvs@gov.in","mla.mapusa.gvs@gov.in","mla.porvorim.gvs@gov.in",
])

print(f"Audience:")
print(f"  Press+civic: {len(press_civic)}")
print(f"  Departments: {len(depts)}")
print(f"  Police:      {len(police)}")
print(f"  MLAs:        {len(mlas)}")
print(f"  TOTAL:       {len(press_civic)+len(depts)+len(police)+len(mlas)}")

# ── .ics factory ─────────────────────────────────────────────────────────────
def make_ics():
    DTSTAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ICS = "\r\n".join([
        "BEGIN:VCALENDAR","VERSION:2.0",
        "PRODID:-//PressDetective//Olympio Almeida//EN",
        "CALSCALE:GREGORIAN","METHOD:REQUEST","BEGIN:VEVENT",
        f"UID:{uuid.uuid4()}",f"DTSTAMP:{DTSTAMP}",
        "DTSTART:20260617T060000Z","DTEND:20260617T080000Z",
        "SUMMARY:TOMORROW — Joint Inspection 11:30 AM Siolim (Wed 17 June 2026)",
        "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
        "DESCRIPTION:Joint site inspection — VP Siolim-Sodiem + GSPCB."
        " Sunday Racquet and Social Club padel courts."
        " All departments\\, police\\, MLAs and media invited.",
        f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
        "STATUS:CONFIRMED","SEQUENCE:5",
        "BEGIN:VALARM","TRIGGER:-PT120M","ACTION:DISPLAY",
        "DESCRIPTION:Siolim inspection in 2 hours","END:VALARM",
        "BEGIN:VALARM","TRIGGER:-PT30M","ACTION:DISPLAY",
        "DESCRIPTION:Siolim inspection in 30 minutes","END:VALARM",
        "END:VEVENT","END:VCALENDAR",
    ])
    p = MIMEBase("text","calendar",method="REQUEST",charset="utf-8")
    p.set_payload(ICS.encode("utf-8")); encoders.encode_base64(p)
    p.add_header("Content-Disposition","attachment",filename="inspection_17june2026.ics")
    return p

# ── send helper ───────────────────────────────────────────────────────────────
def send(subject, body, bcc):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = FROM_ADDR
    msg["Cc"]      = CC_INFO
    msg["Bcc"]     = ", ".join(bcc)
    msg.attach(MIMEText(body,"plain","utf-8"))
    msg.attach(make_ics())
    rcpts = [FROM_ADDR, CC_INFO] + list(bcc)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP("127.0.0.1",1025,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,BRIDGE_PW)
        s.sendmail(FROM_ADDR,rcpts,msg.as_bytes())

def run(label, addresses, subject, body, B=45):
    batches=[addresses[i:i+B] for i in range(0,len(addresses),B)]
    ok=0
    print(f"\n[{label}] {len(addresses)} recipients, {len(batches)} batch(es)...")
    for i,b in enumerate(batches,1):
        try:
            send(subject,body,b); print(f"  batch {i}/{len(batches)} OK ({len(b)})"); ok+=1
        except Exception as e: print(f"  batch {i}/{len(batches)} FAIL: {e}")
        if i<len(batches): time.sleep(4)
    return ok,len(batches)

SIG = """
Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@protonmail.com  |  Press: info@pressdetective.com
"""

# ═══════════════════════════════════════════════════════════════
# 1. PRESS + CIVIC — personal appeal + calendar invite
# ═══════════════════════════════════════════════════════════════
PRESS_SUBJ = "A personal request — please come to Siolim TOMORROW 11:30 AM | Inspection | Calendar Invite Attached"
PRESS_BODY = f"""\
Dear Friend in the Press,

I am Olympio Almeida. I am 70 years old. I live at La Masseria, Survey
No. 197/A, Siolim — right next to the "Sunday Racquet and Social Club"
padel courts at Gaunsawaddo, Sodiem that have been destroying the peace
of our neighbourhood for years.

Tomorrow morning, the Village Panchayat Siolim-Sodiem and the Goa State
Pollution Control Board will conduct a joint inspection. I am writing to
you personally — not with a press release, but as a resident asking for
your help.

COME TOMORROW AND SEE THE TRUTH FOR YOURSELF.

  Day:    WEDNESDAY, 17 JUNE 2026
  Time:   11:30 AM
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

You do not need to take my word for anything. Bring a phone with a free
decibel app (NIOSH SLM or Decibel X) and measure the noise yourself. The
courts run at 68-75 dB(A) — the legal limit for residential areas is 55.

The facts at a glance:
  - Outdoor padel courts running commercially in a residential zone
  - 68-75 dB(A) measured noise vs 55 dB(A) legal limit
  - 2008 Panchayat licence-revocation order on this plot — never enforced
  - Formal GSPCB complaint filed 9 March 2026 — zero response in 9 months
  - Senior citizens in the neighbouring homes suffering every day

Departments, all area MLAs, and police have been formally asked to attend.
A 26-page evidence packet (noise readings, photographs, the 2008 order,
the full complaint) is available on request — simply reply to this email.

A calendar invite is attached. One click adds it to your calendar with
reminders. Please come. Bear witness. This is a real story.

With hope and respect,
Olympio Almeida
olympio.almeida@protonmail.com
Press contact: info@pressdetective.com
---
Reply UNSUBSCRIBE to be removed from further updates.
"""
r1 = run("PRESS + CIVIC", press_civic, PRESS_SUBJ, PRESS_BODY)

time.sleep(5)

# ═══════════════════════════════════════════════════════════════
# 2. DEPARTMENTS — calendar invite + final reminder
# ═══════════════════════════════════════════════════════════════
DEPT_SUBJ = "Calendar Invite — Joint Inspection TOMORROW 11:30 AM Wednesday 17 June 2026, Siolim | Your Department Is Expected"
DEPT_BODY = f"""\
To the concerned Department / Authority,

Calendar invite attached — click "Add to Calendar" to save with reminders.

JOINT SITE INSPECTION — TOMORROW WEDNESDAY 17 JUNE 2026
  Time:   11:30 AM  (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

Inspection called by Village Panchayat Siolim-Sodiem (Notice Ref.
VPSS/2026-27/site insp/648, 08 June 2026). Co-conducted by GSPCB.

Matter: "Sunday Racquet and Social Club" padel courts — 68-75 dB(A)
noise in a residential zone, encroachment, 2008 order unenforced,
GSPCB complaint (9 March 2026) unanswered.

Please depute a representative, bring your departmental record, and
place your response to the March 2026 complaint on the record.
Attendance and absence will be formally documented.
{SIG}"""
r2 = run("DEPARTMENTS", depts, DEPT_SUBJ, DEPT_BODY)

time.sleep(5)

# ═══════════════════════════════════════════════════════════════
# 3. POLICE — calendar invite + attendance request
# ═══════════════════════════════════════════════════════════════
POLICE_SUBJ = "Calendar Invite — Police Presence Required TOMORROW 11:30 AM Wednesday 17 June 2026, Siolim"
POLICE_BODY = f"""\
To the Superintendent of Police / Officer in Charge,

Calendar invite attached — click "Add to Calendar".

JOINT SITE INSPECTION — TOMORROW WEDNESDAY 17 JUNE 2026
  Time:   11:30 AM  (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat Siolim-Sodiem + GSPCB are inspecting the
"Sunday Racquet and Social Club" padel courts at Gaunsawaddo, Sodiem —
68-75 dB(A) noise in a residential zone, encroachment, and a 2008
Panchayat licence-revocation order that has never been enforced in
18 years. GSPCB complaint filed 9 March 2026, unanswered.

Police presence is formally requested to:
  1. Ensure the inspection proceeds without obstruction.
  2. Register this complaint in station records.
  3. Make available any prior complaint records for House No. 47/3,
     Gaunsawaddo, Sodiem, Siolim.

Attendance and absence will be formally noted in the inspection record.
{SIG}"""
r3 = run("POLICE", police, POLICE_SUBJ, POLICE_BODY)

time.sleep(5)

# ═══════════════════════════════════════════════════════════════
# 4. MLAs — calendar invite + final request
# ═══════════════════════════════════════════════════════════════
MLA_SUBJ = "Calendar Invite — Joint Inspection TOMORROW 11:30 AM Wednesday 17 June 2026, Siolim | Your Attendance Requested"
MLA_BODY = f"""\
To the Honourable Member of the Goa Legislative Assembly,

Calendar invite attached — click "Add to Calendar".

JOINT SITE INSPECTION — TOMORROW WEDNESDAY 17 JUNE 2026
  Time:   11:30 AM  (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat Siolim-Sodiem + GSPCB are inspecting the "Sunday
Racquet and Social Club" padel courts in Siolim — 68-75 dB(A) noise in
a residential zone, encroachment, and a 2008 Panchayat order unenforced.
Senior citizens are suffering. A GSPCB complaint from March 2026 has had
no response. Tomorrow is the first formal inspection in months.

Please attend or depute a representative, state your position on
noise-pollution enforcement, and raise the matter with GSPCB and the
Collector if you are unable to attend in person.
{SIG}"""
r4 = run("MLAs", mlas, MLA_SUBJ, MLA_BODY)

# ── summary ───────────────────────────────────────────────────────────────────
total = len(press_civic)+len(depts)+len(police)+len(mlas)
print(f"\n{'='*60}")
print(f"ALL SENDS COMPLETE — FROM: {FROM_ADDR} via Proton Bridge")
print(f"  Press+civic: {r1[0]}/{r1[1]} batches ({len(press_civic)})")
print(f"  Departments: {r2[0]}/{r2[1]} batches ({len(depts)})")
print(f"  Police:      {r3[0]}/{r3[1]} batches ({len(police)})")
print(f"  MLAs:        {r4[0]}/{r4[1]} batches ({len(mlas)})")
print(f"  TOTAL:       {total} recipients")
print(f"  .ics attached to every email")
