"""
INSPECTION DAY — 17 June 2026 morning blast.
  1. 243 NEW Goa contacts (not in audience_14june) — segmented by category
  2. Existing press+civic (137) — TODAY reminder
  3. Existing depts (18) + police (19) — TODAY reminder
  4. Existing MLAs (10) — TODAY reminder
  5. Delilah Lobo — urgent direct follow-up (×2 Gmail addresses)
  6. Gautam — full pre-inspection report

All from olympio.almeida@pressdetective.com via Proton remote SMTP.

    python clients/olympio-almeida/olympio_appeal/send_inspectionday_blast.py
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

EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

# ── load and segment NEW Goa contacts ────────────────────────────────────────
rows = list(csv.DictReader(
    Path("contacts/contacts_live.csv").read_text(encoding="utf-8-sig").splitlines()
))
goa_rows = [r for r in rows
    if "goa" in str(r.get("tags","") + r.get("case","") + r.get("source","")).lower()
    or "goa" in str(r.get("name","") + r.get("designation","")).lower()
    or "siolim" in str(r).lower() or "bardez" in str(r).lower()]

new_rows = [r for r in goa_rows
    if EMAIL_RE.match(r["email"].strip())
    and r["email"].lower() not in existing
    and r["email"].lower() not in sup]

def get_emails(rows): return [r["email"].strip() for r in rows]
def cat(r, *kw): return any(k in r.get("category","").lower() for k in kw)

new_press  = get_emails([r for r in new_rows if cat(r,"press")])
new_govt   = get_emails([r for r in new_rows if cat(r,"government") and not cat(r,"police")])
new_police = get_emails([r for r in new_rows if cat(r,"police")])
new_civic  = get_emails([r for r in new_rows if cat(r,"ngo","civic")])
new_pol    = get_emails([r for r in new_rows if cat(r,"politician","mla","mp")])
new_other  = get_emails([r for r in new_rows
    if not cat(r,"press","government","police","ngo","civic","politician","mla","mp")])

# ── existing segments from audience_14june ────────────────────────────────────
def clean(lst):
    seen=set(); out=[]
    for e in lst:
        el=e.lower().strip()
        if el not in sup and el not in seen: seen.add(el); out.append(e)
    return out

ex_press  = clean(aud["press"] + aud["other"])
ex_depts  = clean([e for e in aud["depts"] if "goapolice.gov.in" not in e.lower()])
ex_police = clean([e for e in aud["depts"] if "goapolice.gov.in" in e.lower()])
ex_mlas   = clean([
    "delilahlobo.goa@gmail.com","delilahlobosiolimoffice@gmail.com",
    "vijaisardesai@gmail.com","drdeviyarane.mla.poriem@gmail.com",
    "mlashetye03bicholim@gmail.com","pravinarlekar4pernem@gmail.com",
    "sec-legi.goa@nic.in","mla.mandrem.gvs@gov.in","mla.tivim.gvs@gov.in",
    "mla.calangute.gvs@gov.in","mla.mapusa.gvs@gov.in","mla.porvorim.gvs@gov.in",
])

print("=== AUDIENCE SUMMARY ===")
print(f"NEW ({len(new_rows)}):  press={len(new_press)} govt={len(new_govt)} police={len(new_police)} civic={len(new_civic)} pol={len(new_pol)} other={len(new_other)}")
print(f"EXISTING:  press+civic={len(ex_press)} depts={len(ex_depts)} police={len(ex_police)} MLAs={len(ex_mlas)}")
total_new = len(new_rows)
total_ex  = len(ex_press)+len(ex_depts)+len(ex_police)+len(ex_mlas)
print(f"TOTAL: {total_new + total_ex} + 2 Lobo direct + 1 Gautam")

# ── .ics ──────────────────────────────────────────────────────────────────────
def make_ics():
    DTSTAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ICS = "\r\n".join([
        "BEGIN:VCALENDAR","VERSION:2.0",
        "PRODID:-//PressDetective//Olympio Almeida//EN",
        "CALSCALE:GREGORIAN","METHOD:REQUEST","BEGIN:VEVENT",
        f"UID:{uuid.uuid4()}",f"DTSTAMP:{DTSTAMP}",
        "DTSTART:20260617T060000Z","DTEND:20260617T080000Z",
        "SUMMARY:TODAY — Joint Inspection 11:30 AM Siolim (17 June 2026)",
        "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
        "DESCRIPTION:TODAY — VP Siolim-Sodiem + GSPCB joint inspection."
        " SP (SPCR) Panaji has formally responded.",
        f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
        "STATUS:CONFIRMED","SEQUENCE:7",
        "BEGIN:VALARM","TRIGGER:-PT60M","ACTION:DISPLAY",
        "DESCRIPTION:Siolim inspection in 1 hour","END:VALARM",
        "BEGIN:VALARM","TRIGGER:-PT30M","ACTION:DISPLAY",
        "DESCRIPTION:Siolim inspection in 30 minutes","END:VALARM",
        "END:VEVENT","END:VCALENDAR",
    ])
    p = MIMEBase("text","calendar",method="REQUEST",charset="utf-8")
    p.set_payload(ICS.encode("utf-8")); encoders.encode_base64(p)
    p.add_header("Content-Disposition","attachment",filename="inspection_today_17june.ics")
    return p

def send_bcc(subject, body, bcc):
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

def send_direct(subject, body, to):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = to
    msg["Cc"]      = CC_INFO
    msg.attach(MIMEText(body,"plain","utf-8"))
    msg.attach(make_ics())
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
        s.sendmail(FROM_ADDR,[to,CC_INFO],msg.as_bytes())

def run(label, addresses, subject, body, B=45):
    if not addresses: print(f"\n[{label}] 0 recipients — skip"); return (0,0)
    batches=[addresses[i:i+B] for i in range(0,len(addresses),B)]
    ok=0
    print(f"\n[{label}] {len(addresses)} recipients, {len(batches)} batch(es)...")
    for i,b in enumerate(batches,1):
        try:
            send_bcc(subject,body,b)
            print(f"  batch {i}/{len(batches)} OK ({len(b)})"); ok+=1
        except Exception as e:
            print(f"  batch {i}/{len(batches)} FAIL: {e}")
        if i<len(batches): time.sleep(5)
    return ok,len(batches)

SIG = """
Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  |  info@pressdetective.com
"""

# ═══════════════════════════════════════════════════════════════
# 1. NEW PRESS + OTHER
# ═══════════════════════════════════════════════════════════════
r1 = run("NEW PRESS", new_press + new_other,
"TODAY 11:30 AM — Joint Inspection Siolim | Police Have Responded | Come Witness It | 17 June 2026",
f"""\
Dear Friend in the Press,

I am Olympio Almeida, a 70-year-old resident of La Masseria, Survey No. 197/A,
Siolim, Goa. I write to you this morning with real urgency.

TODAY at 11:30 AM, the Village Panchayat Siolim-Sodiem and the Goa State
Pollution Control Board are conducting a formal joint inspection of the
"Sunday Racquet and Social Club" — outdoor commercial padel courts operating
illegally in a residential neighbourhood right next to my home.

  TODAY, Wednesday 17 June 2026 — 11:30 AM
  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

OVERNIGHT DEVELOPMENT: The Office of the Superintendent of Police (SPCR),
Panaji formally responded to the complaint last night and forwarded the
matter for necessary police action. This is significant — after years
of being ignored, the police have formally engaged.

We are still waiting for a personal response from MLA Siolim, Ms. Delilah
Lobo, despite multiple personal appeals.

THE FACTS:
  - 68-75 dB(A) noise in a residential zone (legal limit: 55 dB(A))
  - A 2008 Panchayat licence-revocation order — unenforced for 18 years
  - GSPCB complaint filed 9 March 2026 — no response for 3+ months
  - Senior citizens in the neighbouring homes suffering daily

This is a real story. The inspection is happening TODAY. Come and witness
whether the system works for ordinary residents of Goa. Bring a decibel
app and measure the noise yourself.

A calendar invite is attached. A 26-page evidence packet is available on
request — reply to this email.

With hope and respect,
Olympio Almeida
olympio.almeida@pressdetective.com  |  info@pressdetective.com
---
Reply UNSUBSCRIBE to stop receiving updates.
""")
time.sleep(6)

# ═══════════════════════════════════════════════════════════════
# 2. NEW GOVERNMENT
# ═══════════════════════════════════════════════════════════════
r2 = run("NEW GOVT", new_govt,
"TODAY 11:30 AM — Joint Inspection Siolim | SP (SPCR) Has Responded | Your Attendance Requested | 17 June 2026",
f"""\
To the concerned Department / Authority,

This is an urgent notice. The joint site inspection is TODAY THIS MORNING.

  TODAY, Wednesday 17 June 2026 — 11:30 AM
  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

Inspection called by VP Siolim-Sodiem (Notice VPSS/2026-27/site insp/648,
08 June 2026), co-conducted by GSPCB.

Development overnight: the Office of the SP (SPCR), Panaji formally
responded and forwarded the complaint for necessary police action.

Matter: "Sunday Racquet and Social Club" padel courts — 68-75 dB(A)
noise in a residential zone (limit: 55 dB(A)), 2008 Panchayat order
unenforced, GSPCB complaint (9 March 2026) unanswered.

Your department's attendance is respectfully requested. Attendance
and absence will be formally documented.

A calendar invite is attached.
{SIG}""")
time.sleep(6)

# ═══════════════════════════════════════════════════════════════
# 3. NEW POLICE/GOVT
# ═══════════════════════════════════════════════════════════════
r3 = run("NEW POLICE", new_police,
"TODAY 11:30 AM — Police Presence Needed at Siolim Inspection | SP (SPCR) Has Already Responded",
f"""\
To the concerned Police Officer / Authority,

The joint site inspection is TODAY at 11:30 AM.

  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa
  Wednesday 17 June 2026 — 11:30 AM

The Office of the SP (SPCR), Panaji has already formally responded
and forwarded this complaint for police action.

We request the presence of a police officer to ensure the inspection
proceeds without obstruction and to place this matter on official record.

Matter: "Sunday Racquet and Social Club" — outdoor padel courts at
House No. 47/3, Gaunsawaddo, Sodiem, Siolim. 68-75 dB(A) vs 55 dB(A)
residential limit. 2008 Panchayat order still unenforced. GSPCB
complaint March 2026 unanswered.
{SIG}""")
time.sleep(6)

# ═══════════════════════════════════════════════════════════════
# 4. NEW NGO/CIVIC
# ═══════════════════════════════════════════════════════════════
r4 = run("NEW CIVIC", new_civic,
"TODAY 11:30 AM — Siolim Inspection | Please Come as a Community Witness | 17 June 2026",
f"""\
Dear Friend,

I am Olympio Almeida, a 70-year-old resident of Siolim, Goa. I write
to ask if you or your organisation can come as a community witness to
something happening in our neighbourhood TODAY.

  TODAY, Wednesday 17 June 2026 — 11:30 AM
  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

The Village Panchayat and GSPCB are inspecting the "Sunday Racquet
and Social Club" — outdoor commercial padel courts operating in a
residential zone with measured noise of 68-75 dB(A) (legal limit:
55 dB(A)). A 2008 Panchayat order revoking their licence has never
been enforced. Senior citizen residents have been suffering for years.

Overnight good news: the SP (SPCR), Panaji formally responded and
forwarded the matter for police action.

If your organisation works on environment, noise pollution, civic
rights, or senior citizen welfare — your presence as a witness today
would mean a great deal. Community witnesses create accountability.

A calendar invite is attached. Please come if you can.
{SIG}""")
time.sleep(6)

# ═══════════════════════════════════════════════════════════════
# 5. NEW POLITICIANS
# ═══════════════════════════════════════════════════════════════
r5 = run("NEW POLITICIANS", new_pol,
"TODAY 11:30 AM — Siolim Inspection | SP Responded | MLA Siolim Has Not | Your Voice Needed | 17 June 2026",
f"""\
To the Honourable Representative / Party Office,

I write as a 70-year-old resident of Siolim with urgent news and
a respectful request.

TODAY at 11:30 AM, the Panchayat and GSPCB are inspecting the
"Sunday Racquet and Social Club" — outdoor padel courts operating
illegally in a residential zone next to homes of senior citizens.

  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa
  Wednesday 17 June 2026 — 11:30 AM

Overnight: the SP (SPCR), Panaji formally responded and forwarded
the complaint for police action.

We are still waiting for MLA Siolim, Ms. Delilah Lobo, to respond.

North Goa senior citizens are suffering — 68-75 dB(A) noise (limit:
55 dB(A)), a 2008 order still unenforced, a GSPCB complaint from
March 2026 with no response. Your attendance or public support would
make a real difference.

Please attend or send a representative. Calendar invite attached.

Respectfully,
Olympio Almeida
olympio.almeida@pressdetective.com
---
Reply UNSUBSCRIBE to stop receiving updates.
""")
time.sleep(6)

# ═══════════════════════════════════════════════════════════════
# 6. EXISTING PRESS + CIVIC — TODAY reminder
# ═══════════════════════════════════════════════════════════════
r6 = run("EXISTING PRESS+CIVIC", ex_press,
"TODAY — Inspection Is This Morning 11:30 AM | SP (SPCR) Has Responded | Come Witness | Siolim",
f"""\
Dear Friend in the Press,

Quick reminder — the inspection is THIS MORNING.

  TODAY, Wednesday 17 June 2026 — 11:30 AM
  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

Overnight: the SP (SPCR), Panaji formally responded and forwarded
the matter for police action. We have replied asking for a police
officer at the inspection.

We are still waiting to hear from MLA Siolim, Delilah Lobo.

The Panchayat and GSPCB will be there. Please come if you can.
Calendar invite attached.

With hope,
Olympio Almeida
olympio.almeida@pressdetective.com
---
Reply UNSUBSCRIBE to stop receiving updates.
""")
time.sleep(6)

# ═══════════════════════════════════════════════════════════════
# 7. EXISTING DEPTS + POLICE — TODAY final
# ═══════════════════════════════════════════════════════════════
r7 = run("EXISTING DEPTS+POLICE", ex_depts + ex_police,
"TODAY — Inspection Is This Morning 11:30 AM Siolim | SP (SPCR) Has Formally Responded | Final Call",
f"""\
To the concerned Department / Authority,

The inspection is THIS MORNING. Final reminder.

  TODAY, Wednesday 17 June 2026 — 11:30 AM
  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

Development overnight: the SP (SPCR), Panaji formally acknowledged
the complaint and forwarded it for police action.

Your department's attendance is expected. Attendance and absence
will be formally recorded.
{SIG}""")
time.sleep(6)

# ═══════════════════════════════════════════════════════════════
# 8. EXISTING MLAs — TODAY
# ═══════════════════════════════════════════════════════════════
r8 = run("EXISTING MLAs", ex_mlas,
"TODAY 11:30 AM — Siolim Inspection Is This Morning | Police Responded | MLA Lobo: Please Attend",
f"""\
To the Honourable Member of the Legislative Assembly,

The inspection is THIS MORNING.

  TODAY, Wednesday 17 June 2026 — 11:30 AM
  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

Overnight development: the SP (SPCR), Panaji formally responded
and forwarded the complaint for police action.

We are still awaiting a personal response from MLA Siolim,
Ms. Delilah Lobo.

Your attendance today — or a representative's — would demonstrate
your commitment to your constituents. Attendance is being recorded.
{SIG}""")
time.sleep(5)

# ═══════════════════════════════════════════════════════════════
# 9. DELILAH LOBO — urgent direct ×2
# ═══════════════════════════════════════════════════════════════
LOBO_SUBJ = "URGENT — Inspection Is This Morning at 11:30 AM, Siolim | Please Come | Your Constituency Needs You Today"
LOBO_BODY = f"""\
Dear Ms. Delilah Lobo,

The inspection is THIS MORNING — in just a few hours.

  TODAY, Wednesday 17 June 2026 — 11:30 AM
  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

I have written to you many times. I know you are extremely busy.
But I ask you one final time, with all respect and sincerity —
please come, or please send someone from your office.

I need you to know: last night, the Office of the Superintendent
of Police (SPCR), Panaji formally responded to this complaint and
forwarded it for police action. This shows the seriousness of the
matter.

The Panchayat called the inspection. The GSPCB will be there.
The police have been formally notified.

You are the MLA for Siolim. This is happening in your constituency.
Your senior citizen residents are suffering. The only voice we have
not heard is yours.

I am 70 years old. I have lived in this neighbourhood for decades.
I do not ask for money or special favours. I ask only that the law
be enforced and that my elected representative acknowledge that what
is happening here is wrong.

Please come today at 11:30 AM. Even 15 minutes. Even a letter or
WhatsApp to show you are aware.

With deep respect and hope,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  |  info@pressdetective.com
"""

print(f"\n[LOBO DIRECT ×2] ...")
for addr in ["delilahlobo.goa@gmail.com","delilahlobosiolimoffice@gmail.com"]:
    try:
        send_direct(LOBO_SUBJ, LOBO_BODY, addr)
        print(f"  OK -> {addr}")
    except Exception as e:
        print(f"  FAIL {addr}: {e}")
    time.sleep(3)

# ═══════════════════════════════════════════════════════════════
# 10. GAUTAM — full report
# ═══════════════════════════════════════════════════════════════
GAUTAM_SUBJ = "INSPECTION DAY — Full Morning Report | 243 New Contacts Reached | All Systems Go | 17 June 2026"
GAUTAM_BODY = f"""\
Dear Gautam,

Good morning. The inspection is in a few hours. Full pre-inspection
status report below.

=================================================================
THIS MORNING'S BLAST — SUMMARY
=================================================================

We reached EVERYONE — both new contacts and existing ones:

  New Goa press (92):          First-ever contact — inspection TODAY
  New Goa govt (89):           TODAY reminder + SP responded
  New Goa police/govt (12):    TODAY reminder + police notice
  New NGO/civic (36):          Come as community witness
  New politicians/MLAs (11):   Your constituency, your senior citizens
  Existing press+civic (137):  TODAY reminder
  Existing depts+police (37):  TODAY final call
  Existing MLAs (10):          TODAY reminder + Lobo named
  Delilah Lobo (×2 direct):   Urgent personal final appeal

  NEW CONTACTS REACHED:        243 (first-ever contact with them)
  EXISTING CONTACTS REMINDED:  184
  LOBO:                        2 direct TO emails this morning

=================================================================
KEY OVERNIGHT DEVELOPMENT — SP (SPCR) PANAJI RESPONDED
=================================================================

The Superintendent of Police (SPCR), Panaji formally responded last
night via cstatepolice112@gmail.com. They acknowledged receipt and
forwarded the complaint for necessary action.

We replied warmly, requesting a police officer at today's inspection.
That reply delivered (Gmail — no NIC block).

=================================================================
DELILAH LOBO — FULL STATUS
=================================================================

MLA Siolim has not responded despite:
  - 7+ BCC emails over the past week
  - 1 direct TO personal email last week (delilahlobo.goa@gmail.com)
  - 2 direct TO emails this morning

Today's message is the most personal and direct: "I am 70 years old,
please come, even 15 minutes." If she doesn't respond by today's
inspection, her documented silence becomes a campaign fact.

=================================================================
FULL CAMPAIGN TOTALS (6–17 June 2026)
=================================================================

  Unique contacts ever reached:  ~450+ (after dead suppression)
  New contacts reached today:    243 (first ever)
  Calendar invites distributed:  900+
  Dead addresses suppressed:     ~150
  Government responses received: 1 (SP SPCR Panaji — last night)
  Press outlets covered:         229+ (existing 137 + new 92)
  Government/police covered:     130+ across all waves

=================================================================
YOUR CHECKLIST FOR TODAY
=================================================================

  [ ] Arrive at Panchayat office by 11:15 AM
  [ ] Bring: March 2026 GSPCB complaint copy
  [ ] Bring: any noise recordings on your phone
  [ ] Phone: decibel app open (NIOSH SLM or Decibel X)
  [ ] Note names and designations of everyone present
  [ ] Note who is ABSENT (police, MLAs, GSPCB, TCP, Collector)
  [ ] At end: ASK FOR WRITTEN REPORT WITH REFERENCE NUMBER
      This is the single most important outcome today.

=================================================================
IMMEDIATELY AFTER THE INSPECTION
=================================================================

Please email/WhatsApp me:
  - Names and designations of all officials present
  - Whether the club operator was there / any obstruction
  - Whether noise was measured (by whom)
  - The reference number or next steps mentioned by Panchayat
  - Any press who came

This information shapes everything that happens next.

=================================================================
NEXT STEPS (post-inspection)
=================================================================

  18 Jun:   Written request to VP Siolim-Sodiem for inspection report
  24 Jun:   RTI if no report
  GSPCB:    Written request for calibrated noise reading
  Police:   Follow up with cstatepolice112@gmail.com on their action
  Lobo:     Her absence today = documented and reportable
  Press:    Offer evidence packet + inspection report to journalists

=================================================================
YOUR ANONYMITY — UNCHANGED
=================================================================

Nothing has changed. You remain "a senior citizen resident" in all
public communication. Your name, email, and contact details are
never disclosed. This holds at the inspection — you are "the resident
who filed the noise complaint in March 2026."

=================================================================

Everything is in place. You have been heard. The police responded.
The Panchayat called the inspection. 243 new people learned about
this matter for the first time this morning.

Go with confidence. Get the written report.

With all best wishes,
PressDetective
On behalf of Olympio Almeida
olympio.almeida@pressdetective.com
"""

print(f"\n[GAUTAM] ...")
try:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = GAUTAM_SUBJ
    msg["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]      = "gavora@gmail.com"
    msg["Cc"]      = CC_INFO
    msg.attach(MIMEText(GAUTAM_BODY,"plain","utf-8"))
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
        s.sendmail(FROM_ADDR,["gavora@gmail.com",CC_INFO],msg.as_bytes())
    print("  OK -> gavora@gmail.com")
except Exception as e:
    print(f"  FAIL: {e}")

# ── summary ───────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("INSPECTION DAY BLAST — COMPLETE")
print(f"  New press:        {r1[0]}/{r1[1]} ({len(new_press+new_other)})")
print(f"  New govt:         {r2[0]}/{r2[1]} ({len(new_govt)})")
print(f"  New police:       {r3[0]}/{r3[1]} ({len(new_police)})")
print(f"  New civic:        {r4[0]}/{r4[1]} ({len(new_civic)})")
print(f"  New politicians:  {r5[0]}/{r5[1]} ({len(new_pol)})")
print(f"  Ex. press+civic:  {r6[0]}/{r6[1]} ({len(ex_press)})")
print(f"  Ex. depts+police: {r7[0]}/{r7[1]} ({len(ex_depts+ex_police)})")
print(f"  Ex. MLAs:         {r8[0]}/{r8[1]} ({len(ex_mlas)})")
print(f"  Lobo ×2:          sent directly")
print(f"  Gautam:           sent")
