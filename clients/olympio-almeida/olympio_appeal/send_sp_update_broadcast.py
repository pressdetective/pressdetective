"""
Broadcast — SP (SPCR) Panaji has responded; still awaiting MLA Lobo.
Sends to: press+civic, depts (non-police), MLAs — via @pressdetective.com remote SMTP.

    python clients/olympio-almeida/olympio_appeal/send_sp_update_broadcast.py
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

FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
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
mlas        = clean([
    "delilahlobo.goa@gmail.com","delilahlobosiolimoffice@gmail.com",
    "vijaisardesai@gmail.com","drdeviyarane.mla.poriem@gmail.com",
    "mlashetye03bicholim@gmail.com","pravinarlekar4pernem@gmail.com",
    "sec-legi.goa@nic.in","mla.mandrem.gvs@gov.in","mla.tivim.gvs@gov.in",
    "mla.calangute.gvs@gov.in","mla.mapusa.gvs@gov.in","mla.porvorim.gvs@gov.in",
])

print(f"Press+civic: {len(press_civic)}")
print(f"Departments: {len(depts)}")
print(f"MLAs:        {len(mlas)}")

# ── .ics ──────────────────────────────────────────────────────────────────────
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
        "DESCRIPTION:Joint inspection — VP Siolim-Sodiem + GSPCB. "
        "SP (SPCR) Panaji has formally responded. Please attend.",
        f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
        "STATUS:CONFIRMED","SEQUENCE:6",
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
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
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
olympio.almeida@pressdetective.com  |  Press: info@pressdetective.com
"""

# ═══════════════════════════════════════════════════════════════
# COMMON BODY — press, civic, dept, MLA versions
# ═══════════════════════════════════════════════════════════════
UPDATE_SUBJ = ("IMPORTANT UPDATE — Superintendent of Police (SPCR) Panaji Has Formally Responded | "
               "Still Awaiting MLA Siolim | Inspection TOMORROW 11:30 AM")

PRESS_BODY = f"""\
Dear Friend in the Press,

I am writing with an important development.

Tonight, the Office of the Superintendent of Police (SPCR), Panaji has
formally acknowledged receipt of my complaint and forwarded the matter
internally for necessary action. This is significant — the police have
now formally engaged with the issue.

We are still awaiting a personal response from our MLA, Ms. Delilah
Lobo. I have written to her multiple times, most recently tonight with
a personal appeal. The inspection tomorrow provides her an opportunity
to stand with her senior citizen constituents.

TOMORROW — THE INSPECTION IS STILL GOING AHEAD
  Day:    Wednesday, 17 June 2026
  Time:   11:30 AM sharp
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The facts remain:
  - "Sunday Racquet and Social Club" padel courts: 68-75 dB(A) noise
    in a residential zone. Legal limit: 55 dB(A).
  - 2008 Panchayat licence-revocation order — still unenforced after 18 years
  - GSPCB complaint filed 9 March 2026 — over 3 months, no response
  - Encroachment on my private land (Survey No. 197/A), ongoing

The police have responded. The Panchayat called the inspection. GSPCB
will co-conduct it. Now we need you — as the press — to be there to
witness what happens, to record who attends and who does not, and to
report on whether the system works for ordinary residents of Goa.

This is a real story. Please come.

A calendar invite is attached. One click adds it with reminders.

With hope and respect,
Olympio Almeida
olympio.almeida@pressdetective.com
---
Reply UNSUBSCRIBE to be removed from further updates.
"""

DEPT_BODY = f"""\
To the concerned Department / Authority,

I am writing with an important update.

Tonight, the Office of the Superintendent of Police (SPCR), Panaji
has formally responded to my complaint and forwarded the matter
internally for necessary action. I am grateful that the police have
engaged with this serious issue.

We are still awaiting a personal response from MLA Siolim (Delilah Lobo).

THE INSPECTION IS TOMORROW — PLEASE BE THERE
  Day:    Wednesday, 17 June 2026
  Time:   11:30 AM  (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

I thank you for your attention to this matter. A record of departmental
attendance at tomorrow's inspection will be formally maintained. I hope
your department will be represented.

A calendar invite is attached.
{SIG}"""

MLA_BODY = f"""\
To the Honourable Member of the Goa Legislative Assembly,

I am writing with an important update on the Siolim noise-pollution matter.

Tonight, the Office of the Superintendent of Police (SPCR), Panaji has
formally acknowledged my complaint and forwarded it for necessary action
within the police department. This is a significant development.

We are still waiting for a personal response from MLA Siolim, Ms. Delilah
Lobo. I have written to her directly multiple times. The inspection tomorrow
is an opportunity for elected representatives to show they stand with their
senior citizen constituents.

TOMORROW — JOINT SITE INSPECTION
  Day:    Wednesday, 17 June 2026
  Time:   11:30 AM
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The matter: "Sunday Racquet and Social Club" padel courts in Siolim —
68-75 dB(A) noise, residential zone, 2008 order unenforced. The police
have now responded. Your voice now matters more than ever.

Please attend or depute a representative tomorrow.
{SIG}"""

r1 = run("PRESS + CIVIC", press_civic, UPDATE_SUBJ, PRESS_BODY)
time.sleep(5)
r2 = run("DEPARTMENTS", depts, UPDATE_SUBJ, DEPT_BODY)
time.sleep(5)
r3 = run("MLAs", mlas, UPDATE_SUBJ, MLA_BODY)

total = len(press_civic)+len(depts)+len(mlas)
print(f"\n{'='*60}")
print(f"SP UPDATE BROADCAST COMPLETE — FROM: {FROM_ADDR}")
print(f"  Press+civic: {r1[0]}/{r1[1]} batches ({len(press_civic)})")
print(f"  Departments: {r2[0]}/{r2[1]} batches ({len(depts)})")
print(f"  MLAs:        {r3[0]}/{r3[1]} batches ({len(mlas)})")
print(f"  TOTAL:       {total}")
