"""
Re-send the inspection notice to the government + MLA addresses that were
BLOCKED by the DMARC permerror (554 5.7.7) on 14 June.

SAFETY: refuses to send unless pressdetective.com now has exactly ONE DMARC
record (i.e. the duplicate has been removed) — so we never re-bounce and
further damage sender reputation.

    python clients/olympio-almeida/olympio_appeal/resend_govt_after_dmarc.py
"""
import json, smtplib, ssl, sys, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT  = Path(__file__).parent.parent.parent.parent
HERE  = Path(__file__).parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))
FROM_ADDR="olympio.almeida@pressdetective.com"; FROM_NAME="Olympio Almeida"
TOKEN=CREDS["accounts"]["olympio"]["token"]; CC_INFO="info@pressdetective.com"

# ── SAFETY GATE: verify DMARC is fixed ────────────────────────────────────────
def dmarc_ok():
    try:
        import dns.resolver
        recs = [r.to_text().strip('"') for r in dns.resolver.resolve("_dmarc.pressdetective.com","TXT")]
        n = sum(1 for x in recs if x.replace('" "','').lstrip().startswith("v=DMARC1"))
        return n == 1, n
    except Exception as e:
        return False, f"dns error: {e}"

ok, n = dmarc_ok()
if not ok:
    print(f"ABORT — DMARC not fixed yet (found {n} records, need exactly 1).")
    print("Remove the duplicate _dmarc TXT record first, then re-run.")
    sys.exit(1)
print(f"DMARC OK (1 record). Proceeding with government re-send.")

# ── targets: the real addresses that were policy-blocked ──────────────────────
blocked = json.loads((HERE/"blocked_14june.json").read_text())
OFFICIAL = tuple([".gov.in",".nic.in","gspcb.in"])
def is_off(e):
    d=e.split("@",1)[1] if "@" in e else ""
    return d in ("nic.in","gov.in","gspcb.in") or d.endswith(OFFICIAL)
dept = sorted(e for e in blocked if is_off(e) and "mla" not in e)
mla  = sorted(e for e in blocked if "mla" in e or e.endswith("gmail.com"))
print(f"Dept targets: {len(dept)} | MLA targets: {len(mla)}")
if not dept and not mla:
    print("No blocked targets to resend."); sys.exit(0)

SIG = """

Warm regards,
Olympio Almeida
Resident, La Masseria, Survey No. 197/A, Siolim, Goa
olympio.almeida@pressdetective.com  ·  Press: info@pressdetective.com
"""

DEPT_BODY = f"""\
To the concerned Department,

Subject: RE-SENDING — Joint site inspection, Tuesday 17 June 2026, 11:30 AM,
Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim (our earlier emails may not
have reached you due to a sender-side email configuration issue, now resolved).

Respected Sir / Madam,

We recently wrote to your office regarding the "Sunday Racquet and Social Club"
operating outdoor padel courts in a residential zone at Gaunsawaddo, Sodiem,
Siolim — noise of 68-75 dB(A) against the 55 dB(A) limit, encroachment on
private land, and a 2008 Panchayat licence-revocation on the same plot
(Sy. No. 197/7). Those messages may not have been delivered to government
servers; we are therefore resending.

Village Panchayat Siolim-Sodiem has scheduled a JOINT SITE INSPECTION with the
Goa State Pollution Control Board for TUESDAY, 17 JUNE 2026 at 11:30 AM
(Notice Ref. VPSS/2026-27/site insp/648 dated 08 June 2026).

We respectfully request your department to:
  1. Depute an officer to attend the inspection on 17 June 2026.
  2. Carry the relevant departmental record (consent-to-operate / land-use /
     survey position / prior complaints, as applicable).
  3. Place on record your response to the complaint filed with GSPCB on
     9 March 2026, which remains unanswered.

The residents — several senior citizens — have waited three months. Your
presence on 17 June will help bring this to a fair, documented conclusion.
{SIG}"""

MLA_BODY = f"""\
To the Honourable Member of the Goa Legislative Assembly,

Subject: RE-SENDING — your position & presence at the 17 June 2026 Siolim
noise/encroachment inspection (our earlier email may not have reached you due
to a now-resolved technical issue).

Respected Sir / Madam,

I write as a senior-citizen resident of Siolim regarding the "Sunday Racquet
and Social Club" — outdoor padel courts in a residential zone at Gaunsawaddo,
Sodiem (68-75 dB(A) vs the 55 dB(A) limit, encroachment, and a 2008 Panchayat
licence-revocation on the same plot).

A joint inspection with the Goa State Pollution Control Board is set for
TUESDAY, 17 JUNE 2026 at 11:30 AM. As our elected representative I request you
to (1) state your position on noise/land-use enforcement, (2) attend or depute
a representative, and (3) raise the long-pending complaint with GSPCB and the
Collector, North Goa.
{SIG}"""

def send(to_list, subject, body):
    msg=MIMEMultipart("alternative")
    msg["Subject"]=subject; msg["From"]=f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"]=FROM_ADDR; msg["Cc"]=CC_INFO; msg["Bcc"]=", ".join(to_list)
    msg.attach(MIMEText(body,"plain","utf-8"))
    rcpts=[FROM_ADDR,CC_INFO]+to_list
    ctx=ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch",587,timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR,TOKEN)
        s.sendmail(FROM_ADDR,rcpts,msg.as_bytes())

if dept:
    send(dept, "Joint Site Inspection 17 June 2026 — Please Depute a Representative (Siolim)", DEPT_BODY)
    print(f"  Departments re-sent: {len(dept)}")
    time.sleep(3)
if mla:
    send(mla, "17 June Siolim Inspection — Your Position & Presence Requested", MLA_BODY)
    print(f"  MLAs re-sent: {len(mla)}")
print("Done. Re-check inbox for bounces in ~5 min to confirm delivery.")
