#!/usr/bin/env python3
"""
send_press_resume.py  —  Individual-send resume for press release broadcast.

Resumes from where the BCC-batch run left off.  Sends each journalist
their own individual email (TO: journalist, CC: info@) to avoid Proton's
bulk-email / BCC detection that froze sujata after Batch 1.

Usage:
    python send_press_resume.py --dry-run --start 40 --limit 5
    python send_press_resume.py --start 40 --limit 100
    python send_press_resume.py --start 40          # all remaining (no limit)

Default --start is 40 (skip first BCC batch already delivered 9 June).
Pauses 12s between each send to keep traffic pattern human-looking.
"""
import smtplib, ssl, csv, sys, re, socket, time, json, argparse, subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import datetime

ROOT = Path(__file__).parents[2]
CREDS = json.loads((ROOT / ".creds/proton_accounts.json").read_text(encoding="utf-8"))
HOST      = CREDS["smtp_bridge"]["host"]
PORT      = CREDS["smtp_bridge"]["port"]
SMTP_USER = CREDS["accounts"]["sujata"]["address"]
SMTP_PASS = CREDS["accounts"]["sujata"]["bridge_password"]
FROM_ADDR = CREDS["accounts"]["sujata"]["address"]
FROM_NAME = "Adv. Sujata Shirasi"
CC_ALWAYS = CREDS["accounts"]["info"]["address"]
REPORT_TO = ["aliasgarmerchant@gmail.com", "info@pressdetective.com"]

LOG_FILE = ROOT / "contacts" / "send_log_press_resume.csv"

SUBJECT = (
    "FOR IMMEDIATE RELEASE: Advocate Demands Inquiry Into Fabricated FIR Against "
    "Mumbai Businessman Tarun Thadani | FIR 0654/2022, Dadar PS"
)

BODY_TEMPLATE = """\
FOR IMMEDIATE RELEASE
Date: 9 June 2026

=============================================================
ADVOCATE DEMANDS INQUIRY INTO HOW A SLAP BECAME A RS. 1 CRORE
EXTORTION FIR -- MUMBAI BUSINESSMAN TARUN THADANI ENTERS YEAR
FOUR OF DEFENDING A CASE THE RECORDS SHOW NEVER INVOLVED HIM
=============================================================

Dear {salutation},

MUMBAI, 9 June 2026 -- Mumbai businessman Tarun Thadani, founder of
the wellness marketplace dharte.com, has attended court today for
the fourth consecutive year in connection with FIR No. 0654/2022
registered at Dadar Police Station -- a case the documentary record
shows was registered on a complaint that was materially altered two
months after it was originally filed.

Adv. Sujata Shirasi, an Advocate currently investigating the false
FIR and acting for Mr. Tarun Thadani and Mr. Ali Asgar Merchant, has
written formally to the Anti-Corruption Bureau of Maharashtra, the
CB-CID Anti-Extortion Cell and CBI Mumbai requesting an inquiry into
how the FIR came to be registered.

"This case is, on the documentary record, a textbook example of how
the criminal process can be misused," says Adv. Sujata Shirasi. "A
man who was not at the venue, whose only connection to the event
was having sent invitations for it, has been in court for four
years on a Rs. 1 crore extortion allegation that did not appear in
the original complaint. We seek a transparent inquiry into how this
happened."

=============================================================
THE FACTS ON THE RECORD
=============================================================

On 2 June 2022, a restaurant opening was held in Worli, Mumbai. An
altercation took place between Mr. Ali Asgar Merchant and Mr.
Abhishek Badriprasad Saraf. Mr. Tarun Thadani was NOT present at
the venue; his only connection to the event was having sent
invitations for it. He was not there when the altercation occurred.

On 4 June 2022, Mr. Saraf filed an online complaint
(ID: 23244/2022) alleging only that he had been slapped. The
complaint as originally filed did not mention extortion, did not
allege any demand for money, and did not name Mr. Tarun Thadani.

Approximately two months later, the complaint was materially
changed. A new allegation -- that Rs. 1 crore had been demanded as
extortion -- was added. For the first time, Mr. Tarun Thadani's
name was inserted as an accused.

On 12-13 August 2022, FIR No. 0654/2022 was registered at Dadar
Police Station, with the matter handled by Inspector Sanjay
Taralgatti of the CB-CID Anti-Extortion Cell. The investigating
Advocate's position is that the FIR was registered without due
diligence -- no accused was examined before registration, no call
records or bank transactions were verified, and CCTV footage
available from the venue was not reviewed.

In June 2023, The Times of India published a story relating to the
chargesheet. In March 2024, the Sessions Court refused to discharge
Mr. Thadani.

Today, 9 June 2026, is his fourth year of court attendance arising
from these proceedings.

=============================================================
ANTECEDENTS OF THE COMPLAINANT (PUBLIC RECORD)
=============================================================

The following statements concerning Mr. Abhishek Badriprasad Saraf
are drawn entirely from court records, filed civil proceedings and
publicly accessible documents. They are stated here as a matter of
public record.

Mr. Saraf currently occupies the third floor of Esplanade House,
29 Hazarimal Somani Marg, Fort, Mumbai. The tenancy of that floor
is held by Martin Burn Limited, a Calcutta-based company. Martin
Burn Limited has been pursuing civil proceedings against Mr. Saraf
in the High Court at Calcutta (CS No. 313 of 2012) for over a
decade. The pleadings filed in that suit allege misuse of three
Powers of Attorney obtained from the Fatehpuria family in March
2009, forged documents, diversion of rental income, and unlawful
occupation of the third floor.

Those proceedings are ongoing. The allegations are matters before
the Hon'ble High Court at Calcutta and are reproduced here strictly
for the purpose of public-interest journalism.

=============================================================
WHAT THE INVESTIGATING ADVOCATE IS REQUESTING
=============================================================

Adv. Sujata Shirasi has formally written to:

  1. The Anti-Corruption Bureau of Maharashtra requesting an inquiry
     into how the complaint of 4 June 2022 was materially altered to
     add a Rs. 1 crore extortion charge, and by whom.

  2. The Commissioner's Office and senior officers of the CB-CID
     Anti-Extortion Cell requesting an inquiry into the lack of due
     diligence by the investigating officer in registering FIR
     0654/2022 without examining any accused or verifying available
     evidence.

  3. CBI Mumbai for record.

A WITHOUT PREJUDICE notice has also been sent directly to Mr. Saraf
requesting withdrawal of the case within 7 days (deadline: 16 June 2026).

Counsel has indicated that, if the case is not withdrawn, criminal
complaints will be considered under Sections 182, 192 and 211 IPC
(false information, fabricating evidence, false charge of offence
with intent to injure). The matter may also be moved before the
Hon'ble Bombay High Court by way of a quashing petition under
Section 528 BNSS (formerly Section 482 CrPC).

=============================================================
CASE DETAILS
=============================================================

  FIR        : No. 0654/2022
  PS         : Dadar Police Station, Mumbai
  Accused    : Mr. Tarun Thadani and Mr. Ali Asgar Merchant
  Complainant: Mr. Abhishek Badriprasad Saraf
  Court      : Addl. Chief Judicial Magistrate, 37th Court, Mumbai
  CNR        : MHMM110046312023 | Case PW/3700470/2023
  Date       : 9 June 2026 (fourth year of proceedings)
  Deadline   : 16 June 2026 (FIR withdrawal demand)

=============================================================
ABOUT THE INVESTIGATING ADVOCATE
=============================================================

Adv. Sujata Shirasi is an Advocate currently investigating false
FIR No. 0654/2022 and acting for Mr. Tarun Thadani and Mr. Ali
Asgar Merchant. She is an independent legal activist focused on
exposing the misuse of criminal machinery against innocent persons.

  Phone : +91 93216 13691
  Email : sujata.shirasi@pressdetective.com
  Org   : PressDetective

###

EDITORIAL NOTE: All factual statements in this release are drawn
from (a) court records including FIR 0654/2022, the chargesheet,
the Sessions Court order of 31 March 2024 and pleadings in CS
No. 313 of 2012 (HC Calcutta); (b) the complaint of 4 June 2022
filed online by Mr. Saraf (ID 23244/2022); and (c) publicly
accessible documents. The matter is sub judice. Allegations against
identified persons are reported as such; this release does not seek
to prejudge any pending proceeding. Journalists are invited to
verify facts directly with the investigating Advocate, the relevant
police authorities and the courts.

--------------------------------------------------------------
UNSUBSCRIBE: Reply UNSUBSCRIBE or email info@pressdetective.com.
Your address will be removed within 24 hours. Sent on public-interest
journalism basis under Indian DPDP Act 2023 and GDPR Art. 6(1)(f).
--------------------------------------------------------------
"""

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')
_DNS_CACHE = {}


def domain_ok(domain):
    if domain in _DNS_CACHE:
        return _DNS_CACHE[domain]
    try:
        socket.setdefaulttimeout(5)
        socket.gethostbyname(domain)
        _DNS_CACHE[domain] = True
        return True
    except socket.gaierror:
        pass
    try:
        r = subprocess.run(['nslookup', '-type=MX', domain],
                           capture_output=True, text=True, timeout=5)
        if 'mail exchanger' in r.stdout.lower():
            _DNS_CACHE[domain] = True
            return True
    except Exception:
        pass
    _DNS_CACHE[domain] = False
    return False


def verify(addr):
    a = addr.strip()
    if not EMAIL_RE.match(a):
        return False, 'bad format'
    if not domain_ok(a.split('@', 1)[1].lower()):
        return False, 'DNS fail'
    return True, 'ok'


def load_contacts():
    """Load (email, name) pairs for press/media contacts, deduped."""
    seen, out = set(), []
    legal = ROOT / 'contacts' / 'legal_press_contacts.csv'
    if legal.exists():
        for row in csv.DictReader(legal.open(encoding='utf-8-sig')):
            e = row.get('email', '').strip().lower()
            n = row.get('name', '').strip()
            if e and e not in seen:
                seen.add(e)
                out.append((e, n))
    merged = ROOT / 'contacts' / 'contacts_final_merged.csv'
    if merged.exists():
        for row in csv.DictReader(merged.open(encoding='utf-8-sig')):
            e = row.get('email', '').strip().lower()
            n = row.get('name', '').strip()
            case = row.get('case', '').strip().lower()
            cat  = row.get('category', '').strip().lower()
            if e and e not in seen and (
                case == 'general' or 'press' in cat or 'media' in cat
            ):
                seen.add(e)
                out.append((e, n))
    return out


def smtp_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    return ctx


def send_individual(to_addr, name, dry_run=False):
    """Send one personalised email to one journalist."""
    # Build salutation
    if name:
        first = name.strip().split()[0]
        salutation = f"{first}"
    else:
        salutation = "Editor"

    body = BODY_TEMPLATE.replace("{salutation}", salutation)

    msg = MIMEMultipart("alternative")
    msg["From"]     = f'{FROM_NAME} <{FROM_ADDR}>'
    msg["To"]       = to_addr
    msg["Cc"]       = CC_ALWAYS
    msg["Subject"]  = SUBJECT
    msg["Reply-To"] = FROM_ADDR
    msg["List-Unsubscribe"]      = "<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>"
    msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if dry_run:
        print(f"    [DRY] TO:{to_addr} CC:{CC_ALWAYS}")
        return

    ctx = smtp_ctx()
    with smtplib.SMTP(HOST, PORT, timeout=60) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.ehlo()
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(FROM_ADDR, [to_addr, CC_ALWAYS], msg.as_string())


def send_report(sent_list, failed_list, start_idx, dry_run):
    lines = [
        f"PRESS RELEASE RESUME — Send Report",
        f"Generated : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Start offset : {start_idx}",
        f"Mode     : {'DRY RUN' if dry_run else 'LIVE'}",
        f"",
        f"SUMMARY",
        f"-------",
        f"Sent OK  : {len(sent_list)}",
        f"Failed   : {len(failed_list)}",
        f"",
    ]
    if failed_list:
        lines += ["FAILURES:"]
        for addr, err in failed_list:
            lines.append(f"  {addr:<45}  {str(err)[:80]}")
        lines.append("")
    lines += ["SENT TO:"]
    for addr, name in sent_list:
        lines.append(f"  {(name or '—'):<30}  {addr}")

    body = "\n".join(lines)
    subject = f"[TT-FIR][PR-RESUME][{'DRY' if dry_run else 'LIVE'}] {len(sent_list)} sent, {len(failed_list)} failed"

    msg = MIMEMultipart("alternative")
    msg["From"]    = f'{FROM_NAME} <{FROM_ADDR}>'
    msg["To"]      = ", ".join(REPORT_TO)
    msg["Subject"] = subject
    msg["Reply-To"] = FROM_ADDR
    msg.attach(MIMEText(body, "plain", "utf-8"))

    ctx = smtp_ctx()
    with smtplib.SMTP(HOST, PORT, timeout=60) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.ehlo()
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(FROM_ADDR, REPORT_TO, msg.as_string())
    print(f"Report sent to: {', '.join(REPORT_TO)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--start",   type=int, default=40,
                    help="Skip first N valid contacts (default 40 = skip Batch 1 already sent)")
    ap.add_argument("--limit",   type=int, default=0,
                    help="Max contacts to send this run (0 = no limit)")
    ap.add_argument("--pause",   type=int, default=12,
                    help="Seconds between individual sends (default 12)")
    args = ap.parse_args()

    print("=" * 60)
    print("PRESS RELEASE RESUME  —  Individual sends, no BCC")
    print("=" * 60)
    print(f"Mode   : {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Start  : {args.start}  (contacts 0-{args.start-1} were already sent)")
    print(f"Limit  : {args.limit if args.limit else 'unlimited'}")
    print(f"Pause  : {args.pause}s between sends")
    print()

    all_contacts = load_contacts()
    print(f"Total loaded : {len(all_contacts)} contacts")

    # Verify
    valid, invalid = [], []
    for e, n in all_contacts:
        ok, _ = verify(e)
        if ok:
            valid.append((e, n))
    print(f"Valid        : {len(valid)}")
    print(f"Invalid      : {len(all_contacts) - len(valid)}")

    # Slice
    targets = valid[args.start:]
    if args.limit:
        targets = targets[:args.limit]
    print(f"This run     : {len(targets)} contacts (starting at index {args.start})")
    print()

    sent_list, failed_list = [], []

    for idx, (addr, name) in enumerate(targets, 1):
        overall_idx = args.start + idx
        print(f"  [{idx:>4}/{len(targets)}] #{overall_idx}  {addr:<45}", end=" ", flush=True)
        try:
            send_individual(addr, name, dry_run=args.dry_run)
            sent_list.append((addr, name))
            print("OK")
        except Exception as e:
            err_str = str(e)
            failed_list.append((addr, err_str))
            print(f"ERR: {err_str[:80]}")
            # If Proton frozen again — stop immediately
            if "frozen" in err_str.lower() or "2011" in err_str or "limit" in err_str.lower():
                print()
                print("!!! Proton rate limit hit — stopping to protect account.")
                print(f"!!! Resume next run with: --start {args.start + idx}")
                break

        # Append to log
        with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            status = "sent" if (addr, name) in sent_list else "failed"
            w.writerow([addr, name, status, datetime.datetime.now().isoformat()])

        if idx < len(targets):
            time.sleep(args.pause)

    print()
    print("=" * 60)
    print(f"DONE  —  Sent: {len(sent_list)}  |  Failed: {len(failed_list)}")
    print("=" * 60)

    # Send report
    try:
        send_report(sent_list, failed_list, args.start, args.dry_run)
    except Exception as e:
        print(f"Report send failed: {e}")


if __name__ == "__main__":
    main()