"""
Department final follow-up + Lobo direct personal appeal.
PressDetective Proton ONLY.

    python clients/olympio-almeida/olympio_appeal/send_dept_lobo_followup.py
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
assert FROM_ADDR.endswith("@pressdetective.com")

sup_raw = json.loads((HERE / "suppress_14june.json").read_text())
dead_raw= json.loads((HERE / "dead_14june.json").read_text())
new_raw = json.loads((HERE / "newdead_followup.json").read_text())
TODAY_DEAD = {
    "anto.dias@timesgroup.com","goa.city@timesgroup.com","goa.online@timesgroup.com",
    "goa.toi@timesgroup.com","hcnscript@gmail.com","kanzilrodrigues@gmail.com",
    "nolasco.dsouza@timesgroup.com","pankaj.sharma@timesgroup.com","sanjay123@gmail.com",
    "timesarunsinha3000@gmail.com","timesofindia.goa@timesgroup.com",
}
sup = set(e.lower() for e in list(sup_raw)+list(dead_raw)+list(new_raw)) | set(e.lower() for e in TODAY_DEAD)
aud = json.loads((HERE / "audience_14june.json").read_text())
def clean(lst):
    seen=set(); out=[]
    for e in lst:
        el=e.lower().strip()
        if el not in sup and el not in seen: seen.add(el); out.append(e)
    return out

# .ics helper
def make_ics(uid_str):
    DTSTAMP=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ICS="\r\n".join([
        "BEGIN:VCALENDAR","VERSION:2.0",
        "PRODID:-//PressDetective//Olympio Almeida//EN",
        "CALSCALE:GREGORIAN","METHOD:REQUEST","BEGIN:VEVENT",
        f"UID:{uid_str}",f"DTSTAMP:{DTSTAMP}",
        "DTSTART:20260617T060000Z","DTEND:20260617T080000Z",
        "SUMMARY:TOMORROW — Siolim Inspection 11:30 AM Wed 17 June 2026",
        "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
        "DESCRIPTION:Joint inspection VP Siolim-Sodiem + GSPCB. Your attendance requested.",
        f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
        "STATUS:CONFIRMED","SEQUENCE:2",
        "BEGIN:VALARM","TRIGGER:-PT120M","ACTION:DISPLAY",
        "DESCRIPTION:Siolim inspection in 2 hours","END:VALARM",
        "END:VEVENT","END:VCALENDAR",
    ])
    p=MIMEBase("text","calendar",method="REQUEST",charset="utf-8")
    p.set_payload(ICS.encode("utf-8")); encoders.encode_base64(p)
    p.add_header("Content-Disposition","attachment",filename="inspection_17june2026.ics")
    return p

def send_bcc(subject, body, bcc):
    msg=MIMEMultipart("mixed")
    msg["Subject"]=subject; msg["From"]=f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]=FROM_ADDR; msg["Cc"]=CC_INFO; msg["Bcc"]=", ".join(bcc)
    msg.attach(MIMEText(body,"plain","utf-8")); msg.attach(make_ics(str(uuid.uuid4())))
    rcpts=[FROM_ADDR,CC_INFO]+list(bcc)
    ctx=ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
        s.sendmail(FROM_ADDR,rcpts,msg.as_bytes())

def send_direct(subject, body, to):
    msg=MIMEMultipart("mixed")
    msg["Subject"]=subject; msg["From"]=f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]=to; msg["Cc"]=CC_INFO
    msg.attach(MIMEText(body,"plain","utf-8")); msg.attach(make_ics(str(uuid.uuid4())))
    rcpts=[to,CC_INFO]
    ctx=ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
        s.sendmail(FROM_ADDR,rcpts,msg.as_bytes())

SIG="""
Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  |  Press: info@pressdetective.com
"""

# ── 1. DEPARTMENTS final follow-up ────────────────────────────────────────────
depts = clean(aud["depts"])
DEPT_SUBJ = "Last Call — You Are Expected TOMORROW: Joint Inspection 11:30 AM Wednesday 17 June, Siolim | Please Confirm Attendance"
DEPT_BODY = f"""\
To the concerned Department / Authority,

This is a final follow-up. The inspection is TOMORROW.

We have written to you multiple times over the past week regarding
the joint site inspection called by Village Panchayat Siolim-Sodiem
(Notice Ref. VPSS/2026-27/site insp/648, dated 08 June 2026).

TOMORROW — FINAL DETAILS
  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM (arrive by 11:15 AM)
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The matter — "Sunday Racquet and Social Club" padel courts at
House No. 47/3, Gaunsawaddo, Sodiem, Siolim — remains unresolved:
  - Noise: 68-75 dB(A) against the 55 dB(A) residential limit
  - Encroachment on private land (Survey No. 197/A)
  - 2008 Panchayat licence-revocation order still not enforced
  - GSPCB complaint filed 9 March 2026 — 9 months, no response

A written record of departmental attendance will be maintained.
Your department's response — or absence — will be formally noted.

Please depute an officer and bring your departmental record.
The calendar invite attached will add the event to your calendar.
{SIG}"""

print(f"\n[DEPARTMENTS] {len(depts)} addresses...")
try:
    send_bcc(DEPT_SUBJ, DEPT_BODY, depts)
    print(f"  OK ({len(depts)})")
except Exception as e:
    print(f"  FAIL: {e}")
time.sleep(4)

# ── 2. POLICE follow-up ───────────────────────────────────────────────────────
POLICE = [e for e in aud["depts"] if "goapolice.gov.in" in e.lower()]
police = [e for e in dict.fromkeys(POLICE) if e.lower() not in sup]
POLICE_SUBJ = "Last Call — Police Presence Required TOMORROW 11:30 AM, Siolim (17 June 2026)"
POLICE_BODY = f"""\
To the Superintendent of Police / Officer in Charge,

This is a final follow-up before tomorrow's joint inspection.

  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The "Sunday Racquet and Social Club" operates commercial padel courts in
a residential zone with measured noise of 68-75 dB(A) vs the 55 dB(A)
limit, encroachment on private land, and a 2008 Panchayat order that
has never been enforced. Senior citizens have been suffering for years.

The Panchayat and GSPCB are conducting the inspection tomorrow. Police
presence is requested to ensure the proceedings take place without
obstruction or interference, and to register a formal record of the
complaint. A written record of who attended will be maintained.
{SIG}"""

print(f"\n[POLICE follow-up] {len(police)} addresses...")
try:
    send_bcc(POLICE_SUBJ, POLICE_BODY, police)
    print(f"  OK ({len(police)})")
except Exception as e:
    print(f"  FAIL: {e}")
time.sleep(4)

# ── 3. DELILAH LOBO — direct personal appeal (TO field, not BCC) ──────────────
LOBO_SUBJ = "Siolim — Your Constituency Needs You TOMORROW: Inspection 11:30 AM, 17 June 2026 | Personal Request"
LOBO_BODY = f"""\
Dear Ms. Delilah Lobo,

I am writing to you directly and personally.

You are the MLA for Siolim — my home constituency. The matter I am writing
about is happening in your ward, on your watch, affecting your senior
citizen constituents.

TOMORROW — WEDNESDAY 17 JUNE 2026 AT 11:30 AM
Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat has called a joint inspection with the Goa State
Pollution Control Board of the "Sunday Racquet and Social Club" — commercial
padel courts at House No. 47/3, Gaunsawaddo, Sodiem — operating in a
residential zone adjacent to our homes.

The facts:
  - Measured noise: 68-75 dB(A). Legal limit: 55 dB(A).
  - The same plot (Survey No. 197/7) had its Panchayat licence revoked
    in 2008. That order has never been enforced.
  - I encroachment on my land (Survey No. 197/A) is ongoing.
  - I filed a formal complaint with GSPCB on 9 March 2026.
    It is now June. I have received no response.

We are senior citizens. We bought our homes here for peace and quiet.
What is happening to us is a violation of the law — and it is happening
in your constituency.

I have been to every channel: the Panchayat, the GSPCB, the Collector,
the departments. Tomorrow is the first time an inspection will actually
take place. I am asking you, as my MLA, to attend or to send a
representative — not because of politics, but because this is your job.

A calendar invite is attached. Please come.

I have a 26-page evidence packet available on request.

Yours sincerely,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com
"""

print(f"\n[DELILAH LOBO — direct] delilahlobo.goa@gmail.com...")
try:
    send_direct(LOBO_SUBJ, LOBO_BODY, "delilahlobo.goa@gmail.com")
    print("  OK -> delilahlobo.goa@gmail.com (direct TO)")
except Exception as e:
    print(f"  FAIL: {e}")
time.sleep(4)

# ── 4. OTHER MLAs follow-up ───────────────────────────────────────────────────
OTHER_MLAS = [
    "vijaisardesai@gmail.com",
    "drdeviyarane.mla.poriem@gmail.com",
    "mlashetye03bicholim@gmail.com",
    "pravinarlekar4pernem@gmail.com",
    "sec-legi.goa@nic.in",
    "mla.mandrem.gvs@gov.in",
    "mla.tivim.gvs@gov.in",
    "mla.calangute.gvs@gov.in",
    "mla.mapusa.gvs@gov.in",
    "mla.porvorim.gvs@gov.in",
]
other_mlas = [e for e in dict.fromkeys(OTHER_MLAS) if e.lower() not in sup]
MLA_SUBJ = "Final Follow-up — Siolim Inspection TOMORROW 11:30 AM Wednesday 17 June | Senior Citizens Need Your Voice"
MLA_BODY = f"""\
Dear Honourable Member of the Legislative Assembly,

This is a final follow-up. The inspection is TOMORROW.

  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

We have written to you multiple times this week regarding the "Sunday
Racquet and Social Club" — outdoor padel courts operating in a Siolim
residential zone with noise at 68-75 dB(A) (limit: 55 dB(A)),
encroachment on private land, and a 2008 Panchayat order still unenforced.

Senior citizens who have lived in this neighbourhood for decades are
suffering daily. A formal GSPCB complaint filed in March 2026 has received
no response. Tomorrow's inspection is the first formal action in months.

We respectfully ask you once more:
  1. Attend or depute a representative at 11:30 AM tomorrow.
  2. Publicly state your position on noise-pollution enforcement.
  3. Use your office to ensure that the inspection report is acted upon.

A calendar invite is attached. Silence from elected representatives at
this moment will also be noted.
{SIG}"""

print(f"\n[OTHER MLAs] {len(other_mlas)} addresses...")
try:
    send_bcc(MLA_SUBJ, MLA_BODY, other_mlas)
    print(f"  OK ({len(other_mlas)})")
except Exception as e:
    print(f"  FAIL: {e}")

print("\nDept + Police + Lobo + MLA follow-ups: COMPLETE")
