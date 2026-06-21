"""
Personal press appeal — "come and see the truth tomorrow".
Tone is warm, direct, journalistic — asking for real help, not just coverage.
PressDetective Proton ONLY.

    python clients/olympio-almeida/olympio_appeal/send_press_appeal_final.py
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
dead_raw = json.loads((HERE / "dead_14june.json").read_text())
new_raw  = json.loads((HERE / "newdead_followup.json").read_text())
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

press = clean(aud["press"])
civic = clean(aud["other"])
all_press = list(dict.fromkeys(press + civic))
print(f"Press + civic: {len(all_press)} recipients")

# .ics
DTSTART="20260617T060000Z"; DTEND="20260617T080000Z"
DTSTAMP=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
ICS="\r\n".join([
    "BEGIN:VCALENDAR","VERSION:2.0",
    "PRODID:-//PressDetective//Olympio Almeida//EN",
    "CALSCALE:GREGORIAN","METHOD:REQUEST","BEGIN:VEVENT",
    f"UID:{uuid.uuid4()}",f"DTSTAMP:{DTSTAMP}",
    f"DTSTART:{DTSTART}",f"DTEND:{DTEND}",
    "SUMMARY:Come Tomorrow — Siolim Inspection 11:30 AM Wed 17 June 2026",
    "LOCATION:Village Panchayat Siolim-Sodiem office\\, Sodiem\\, Siolim\\, Goa",
    "DESCRIPTION:Joint site inspection — Sunday Racquet and Social Club padel courts."
    " Village Panchayat Siolim-Sodiem + GSPCB. Media welcome. 11:30 AM.",
    f"ORGANIZER;CN={FROM_NAME}:mailto:{FROM_ADDR}",
    "STATUS:CONFIRMED","SEQUENCE:2",
    "BEGIN:VALARM","TRIGGER:-PT120M","ACTION:DISPLAY",
    "DESCRIPTION:Siolim inspection in 2 hours","END:VALARM",
    "END:VEVENT","END:VCALENDAR",
])
def make_ics():
    p=MIMEBase("text","calendar",method="REQUEST",charset="utf-8")
    p.set_payload(ICS.encode("utf-8")); encoders.encode_base64(p)
    p.add_header("Content-Disposition","attachment",filename="inspection_17june2026.ics")
    return p

SUBJ = "A personal request — please come to Siolim tomorrow, 11:30 AM | You will see the truth for yourself"

BODY = """\
Dear Friend in the Press,

I am writing to you personally — not as a press release, but as a resident
asking for your help.

Tomorrow morning at 11:30 AM, the Village Panchayat Siolim-Sodiem and the
Goa State Pollution Control Board will conduct a joint inspection of an
outdoor padel court club that has been destroying the peace of our
neighbourhood for years.

I am Olympio Almeida. I am 70 years old. I live at La Masseria, Survey
No. 197/A, Siolim — right next to these courts. So do my neighbours,
fellow senior citizens who bought homes here for a quiet retirement.

What has happened to us:
  - The "Sunday Racquet and Social Club" runs outdoor padel courts
    at House No. 47/3, Gaunsawaddo, Sodiem — a residential zone —
    ~30-40 feet from our homes.
  - We have measured the noise at 68-75 decibels. The legal limit
    for a residential area is 55 decibels.
  - The same plot had a Panchayat licence revoked in 2008 for
    unauthorised construction. That order was never enforced.
  - We filed a formal complaint with the Goa State Pollution Control
    Board on 9 March 2026. Six months on — no response.
  - The inspection tomorrow was called by the Panchayat after we
    escalated. It has taken this long to get even an inspection.

I have sent formal letters to every department, every MLA, and every
press contact I could reach. The officials have been notified. The
question now is: who will actually show up and witness this?

That is where I need your help.

COME TOMORROW AND HEAR IT FOR YOURSELF.

  Date:   Wednesday, 17 June 2026
  Time:   11:30 AM
  Venue:  Village Panchayat Siolim-Sodiem office, Sodiem, Siolim, Goa

You do not need to take my word for anything. Come, bring a phone
with a free decibel app (NIOSH SLM or Decibel X), and measure it
yourself. The numbers will speak.

I have a 26-page evidence packet — noise readings, photographs, the
2008 order, the March 2026 complaint, the full timeline — that I will
share with any journalist who asks. Simply reply to this email.

I am not asking you to take sides. I am asking you to bear witness.
A senior citizen's home should be his sanctuary. That is a story
worth covering — and tomorrow, it will be happening in front of you.

A calendar invite is attached. Please click "Add to Calendar" to save
the event with a reminder.

With hope and respect,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com

Press contact: info@pressdetective.com

---
Reply UNSUBSCRIBE to be removed from further updates.
"""

def send_batch(bcc):
    msg=MIMEMultipart("mixed")
    msg["Subject"]=SUBJ; msg["From"]=f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]=FROM_ADDR; msg["Cc"]=CC_INFO; msg["Bcc"]=", ".join(bcc)
    msg.attach(MIMEText(BODY,"plain","utf-8")); msg.attach(make_ics())
    rcpts=[FROM_ADDR,CC_INFO]+list(bcc)
    ctx=ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
        s.sendmail(FROM_ADDR,rcpts,msg.as_bytes())

B=45; batches=[all_press[i:i+B] for i in range(0,len(all_press),B)]; ok=0
for i,b in enumerate(batches,1):
    try:
        send_batch(b); print(f"  batch {i}/{len(batches)} OK ({len(b)})"); ok+=1
    except Exception as e: print(f"  batch {i}/{len(batches)} FAIL: {e}")
    if i<len(batches): time.sleep(4)
print(f"Press appeal: {ok}/{len(batches)} batches, {len(all_press)} recipients")
