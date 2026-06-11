#!/usr/bin/env python3
"""
send_press_release.py - Distribute Tarun Thadani false-FIR press release.

Step 0: Preview to info@pressdetective.com
Step 1: Verify all press contact addresses (format + DNS)
Step 2: Batched BCC broadcast (40/batch, 20s pause) via Proton Bridge

From    : sujata.shirasi@pressdetective.com
SMTP    : Proton Bridge 127.0.0.1:1025 STARTTLS

Compliance (per project rule feedback_truth_and_law.md):
  - Truth: only verified facts; antecedent claims framed as 'alleged' with source
  - Sub-judice safe: factual recital, no prejudicial commentary
  - GDPR Art. 6(1)(f) / Indian DPDP 2023: unsubscribe footer in every email

Usage:
    python send_press_release.py --dry-run --limit 3
    python send_press_release.py
"""
import smtplib, ssl, csv, sys, time, re, socket, argparse, subprocess, json
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).parents[2]
_creds = json.loads((ROOT / '.creds/proton_accounts.json').read_text())
HOST       = _creds['smtp_bridge']['host']
PORT       = _creds['smtp_bridge']['port']
SMTP_USER  = _creds['accounts']['sujata']['address']
SMTP_PASS  = _creds['accounts']['sujata']['bridge_password']
FROM_ADDR  = _creds['accounts']['sujata']['address']
FROM_NAME  = 'Adv. Sujata Shirasi'

CC = ['info@pressdetective.com']

SUBJECT = (
    'FOR IMMEDIATE RELEASE: Advocate Demands Inquiry Into Fabricated FIR Against '
    'Mumbai Businessman Tarun Thadani | FIR 0654/2022, Dadar PS'
)

BODY = """\
FOR IMMEDIATE RELEASE
Date: 9 June 2026

=============================================================
ADVOCATE DEMANDS INQUIRY INTO HOW A SLAP BECAME A RS. 1 CRORE
EXTORTION FIR -- MUMBAI BUSINESSMAN TARUN THADANI ENTERS YEAR
FOUR OF DEFENDING A CASE THE RECORDS SHOW NEVER INVOLVED HIM
=============================================================

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
Abhishek Badriprasad Saraf. Mr. Tarun Thadani was not present at
the venue; his only connection to the event was having sent
invitations for it.

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
requesting withdrawal of the case within 7 days.

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
  Today      : 9 June 2026 (hearing day, four years on)

=============================================================
ABOUT THE INVESTIGATING ADVOCATE
=============================================================

Adv. Sujata Shirasi is an Advocate currently investigating false
FIR No. 0654/2022 and acting for Mr. Tarun Thadani and Mr. Ali
Asgar Merchant. She is an independent legal activist focused on
exposing the misuse of criminal machinery against innocent persons.

=============================================================
MEDIA CONTACT
=============================================================

  Adv. Sujata Shirasi
  Phone : +91 93216 13691
  Email : sujata.shirasi@pressdetective.com
  Org   : PressDetective
  Web   : pressdetective.com

###

EDITORIAL NOTE: All factual statements in this release are drawn
from (a) court records including FIR 0654/2022, the chargesheet,
the Sessions Court order of 31 March 2024 and pleadings in CS
No. 313 of 2012 (HC Calcutta); (b) the complaint of 4 June 2022
filed online by Mr. Saraf (ID 23244/2022); and (c) publicly
accessible documents. The matter is sub judice. Allegations against
identified persons are reported as such; this release does not seek
to prejudice any pending proceeding. Journalists are invited to
verify facts directly with the investigating Advocate, the relevant
police authorities and the courts.

UNSUBSCRIBE / OPT-OUT: If you do not wish to receive further
communications from PressDetective, reply to this email with the
word UNSUBSCRIBE in the subject line, or email
info@pressdetective.com. Your address will be removed within 24
hours. This communication is sent on a public-interest journalism
basis under the Indian DPDP Act 2023 and GDPR Art. 6(1)(f)
legitimate-interest provisions.
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
    here = Path(__file__).parent
    root = here.parents[1]
    import sys
    sys.path.insert(0, str(root))
    from lib.compliance import load_suppression_set
    suppressed = load_suppression_set()
    seen, out = set(), []
    legal = root / 'contacts' / 'legal_press_contacts.csv'
    if legal.exists():
        with open(legal, encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                e = row.get('email', '').strip().lower()
                if e and e not in seen and e not in suppressed:
                    seen.add(e); out.append(e)
    live = root / 'contacts' / 'contacts_live.csv'
    if live.exists():
        with open(live, encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                e = row.get('email', '').strip().lower()
                case = row.get('case', '').strip().lower()
                cat  = row.get('category', '').strip().lower()
                if e and e not in seen and e not in suppressed and (
                    case == 'general' or 'press' in cat or 'media' in cat
                ):
                    seen.add(e); out.append(e)
    return out


def smtp_conn():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    s = smtplib.SMTP(HOST, PORT, timeout=300)
    s.ehlo()
    s.starttls(context=ctx)
    s.ehlo()
    s.login(SMTP_USER, SMTP_PASS)
    return s


def send_one(to_addrs, cc_addrs, subject, body, bcc_addrs=None, dry_run=False):
    m = EmailMessage()
    m['From']    = f'{FROM_NAME} <{FROM_ADDR}>'
    m['To']      = ', '.join(to_addrs)
    if cc_addrs:
        m['Cc'] = ', '.join(cc_addrs)
    if bcc_addrs:
        m['Bcc'] = ', '.join(bcc_addrs)
    m['Subject'] = subject
    m['List-Unsubscribe'] = '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    m['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'
    m.set_content(body)
    if dry_run:
        recipients = list(to_addrs) + (cc_addrs or []) + (bcc_addrs or [])
        print(f'  [DRY] would send to {len(recipients)} addresses')
        return
    with smtp_conn() as s:
        s.send_message(m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    contacts = load_contacts()
    print(f'Loaded {len(contacts)} press contacts')

    # Step 0: preview to info@
    print('Step 0: Sending preview to info@pressdetective.com ...')
    send_one(
        to_addrs=['info@pressdetective.com'],
        cc_addrs=None,
        subject=f'[PRESS RELEASE PREVIEW] {SUBJECT}',
        body=BODY,
        dry_run=args.dry_run,
    )
    print('  OK\n')

    # Step 1: verify
    print(f'Step 1: Verifying {len(contacts)} addresses ...')
    valid, invalid = [], []
    for e in contacts:
        ok, why = verify(e)
        if ok:
            valid.append(e)
        else:
            invalid.append((e, why))
    print(f'  valid={len(valid)} invalid={len(invalid)}\n')

    # Step 2: slice + batch
    targets = valid[args.start:]
    if args.limit:
        targets = targets[:args.limit]
    batches = [targets[i:i+40] for i in range(0, len(targets), 40)]
    print(f'Step 2: Broadcasting {len(targets)} contacts in {len(batches)} batches of 40\n')

    sent, errors = 0, []
    for i, batch in enumerate(batches, 1):
        print(f'  Batch {i}/{len(batches)} ({len(batch)} recipients) ... ', end='', flush=True)
        try:
            send_one(
                to_addrs=[FROM_ADDR],
                cc_addrs=CC,
                bcc_addrs=batch,
                subject=SUBJECT,
                body=BODY,
                dry_run=args.dry_run,
            )
            sent += len(batch)
            print(f'OK [{sent}/{len(targets)}]')
        except Exception as e:
            errors.append(f'Batch {i}: {e}')
            print(f'ERROR: {e}')
        if i < len(batches):
            time.sleep(20)

    # Step 3: distribution report to info@
    print('\nStep 3: Sending distribution report to info@pressdetective.com ...')
    status = 'OK' if not errors else f'{len(errors)} ERRORS'
    lines = [
        'Press Release Distribution Report',
        f'Date    : 9 June 2026',
        f'From    : {FROM_ADDR}',
        f'Subject : {SUBJECT[:80]}',
        f'Loaded  : {len(contacts)} contacts',
        f'Verified: {len(valid)} valid, {len(invalid)} dropped',
        f'Sent    : {sent}',
        f'Batches : {len(batches)} x 40',
        '',
    ]
    if errors:
        lines += [f'ERRORS ({len(errors)}):', *[f'  {e}' for e in errors]]
    else:
        lines.append('All batches delivered. No errors.')
    if invalid:
        lines += ['', f'Invalid addresses (first 30):',
                  *[f'  {a} - {w}' for a, w in invalid[:30]]]

    send_one(
        to_addrs=['info@pressdetective.com'],
        cc_addrs=None,
        subject=f'[TT-FIR][PR-DIST][{status}][9Jun2026] Press release: {sent} sent',
        body='\n'.join(lines),
        dry_run=args.dry_run,
    )
    print(f'  OK\n\nDone. {sent} press contacts notified.')


if __name__ == '__main__':
    main()