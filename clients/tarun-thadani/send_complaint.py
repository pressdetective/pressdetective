#!/usr/bin/env python3
"""
send_complaint.py  Formal complaint broadcast: False FIR against Tarun Thadani
Sender  : sujata.shirasi@pressdetective.com
Via     : Proton Bridge SMTP (127.0.0.1:1025 STARTTLS)
To      : All contacts in contacts_master.csv EXCEPT olympio-almeida (Goa)
CC      : info@pressdetective.com
Body    : Letter in email body, no attachments
Verify  : Format + DNS check on every address before sending

Usage:
    python send_complaint.py --dry-run    # preview only
    python send_complaint.py              # send for real
    python send_complaint.py --start 500  # resume from position 500
    python send_complaint.py --limit 20   # send to first 20 only
"""
import sys, csv, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))
from lib.mailer import send_batched, send_mail, build_msg, load_account

FROM_ACC = 'sujata'
CC       = ['info@pressdetective.com']

SUBJECT = (
    'Formal Complaint: Fabricated FIR Against dharte.com Founder Tarun Thadani '
    '— Abhishek Badriprasad Saraf, False FIR No. 0654/2022, Dadar Police Station'
)

BODY = """\
Respected Sir / Madam,

I, Adv. Sujata Shirasi, Advocate, write to you as Counsel for Mr. Tarun Thadani \
— founder of dharte.com and a family man residing in Mumbai — to place before you \
a matter of serious concern involving the misuse of the criminal justice system by \
one Abhishek Badriprasad Saraf.

Today, 9 June 2026, Mr. Thadani attends court for the fourth consecutive year in \
a case that is built entirely on a fabricated and altered complaint. I respectfully \
request your attention to the facts below.

---------------------------------------------
THE INCIDENT
---------------------------------------------

On the evening of 2 June 2022, a restaurant opening was held in Worli, Mumbai. \
Mr. Thadani attended briefly and left. After he left, a personal altercation took \
place between Ali Asgar Merchant and Abhishek Badriprasad Saraf. Ali Asgar Merchant \
slapped Saraf. That was the extent of the incident.

Saraf went to the police. He was told that a slap was a minor offence and that no \
serious criminal case would be registered.

He was not satisfied with that answer.

---------------------------------------------
HOW THE FALSE FIR WAS MANUFACTURED
---------------------------------------------

On 4 June 2022, Saraf filed an online complaint (ID: 23244/2022) alleging assault \
only. There was no mention of extortion. No demand for money. No mention of \
Mr. Thadani.

Nearly two months later, the complaint was materially changed. A new allegation \
appeared: that Rs. 1 crore had been demanded as extortion. For the first time, the \
name of Mr. Tarun Thadani — who had left before the incident even occurred — was \
inserted.

On 12-13 August 2022, FIR No. 0654/2022 was registered at Dadar Police Station. \
Not a single accused was examined before registration. No call records were checked. \
No bank transactions were verified. No CCTV evidence was reviewed.

Investigation by our team has established that Inspector Sanjay Taralgatti of the \
Anti-Extortion Cell appears to have been manipulated into registering this FIR on \
the basis of a fabricated extortion story, without tangible evidence. A witness was \
also allegedly coerced into giving a false statement supporting the extortion \
claim — a claim contradicted by all available CCTV footage.

---------------------------------------------
WHO IS ABHISHEK BADRIPRASAD SARAF?
---------------------------------------------

Abhishek Badriprasad Saraf
Phone: +91 98201 80065
Address: 3rd Floor, Esplanade House, 29, Hazarimal Somani Marg, Fort, Mumbai 400001

This is not an isolated incident of misuse of process. Saraf has a well-documented \
history of fraud, forgery and manipulation across Mumbai and Calcutta.

He currently illegally occupies the entire third floor of Esplanade House — a \
UNESCO-listed heritage building once home to Jamsetji Tata — valued at over \
Rs. 150 crores. This property is held under tenancy by Martin Burn Limited, a \
Calcutta-based company (the Fatehpuria family).

Saraf ingratiated himself with the Fatehpuria family, obtained three Powers of \
Attorney in March 2009, and then:

  - Forged documents in his own favour
  - Opened a parallel bank account to divert their rental income
  - Extracted Rs. 40 lakhs from the family directly
  - Took loans from Martin Burn Ltd that remain unpaid
  - Took over the electricity meter and gradually occupied the entire third floor \
    without any legal right

Martin Burn Ltd sued Saraf in the High Court at Calcutta (CS No. 313 of 2012, \
before Hon'ble Justice I.P. Mukerji). That case has run for over a decade. \
Despite complaints to the Prime Minister's Office, the Anti-Corruption Bureau and \
multiple departments, Saraf continues to live at the property and has, until now, \
evaded accountability.

HOW IS A SINGLE INDIVIDUAL ABLE TO MANIPULATE THE MUMBAI POLICE?

Saraf could not get the police to file a serious FIR for a slap. So he rewrote \
his complaint, invented a Rs. 1 crore extortion charge, and inserted the name of \
a man who had already left the venue. Inspector Sanjay Taralgatti of the \
Anti-Extortion Cell registered the FIR without examining a single accused or \
verifying a single piece of evidence.

We also bring to your attention that ACP Dattatray Nale (D/South) had taken \
cognisance of this matter. His PA, Inspector Milind Kamble (+91 98705 64941), \
was the point of contact. Despite initial engagement, ACP Nale has provided no \
update and has effectively left the matter to the courts.

We respectfully but strongly urge the concerned authorities: SUMMON ABHISHEK \
BADRIPRASAD SARAF FOR IMMEDIATE QUESTIONING. He is reachable at +91 98201 80065 \
and resides at the address above.

---------------------------------------------
THE ONGOING DAMAGE TO MR. THADANI
---------------------------------------------

Since August 2022, Mr. Thadani has been publicly labelled a criminal accused. \
In June 2023, the Times of India published a story on the chargesheet naming him. \
In March 2024, the Sessions Court refused to discharge him. He continues to attend \
court dates, bearing the personal, professional and financial burden of defending a \
case that should never have been registered.

Today -- 9 June 2026 -- is yet another hearing.

---------------------------------------------
WHAT WE ARE REQUESTING
---------------------------------------------

1. An inquiry into how the original complaint of 4 June 2022 was materially altered \
   to add an extortion charge that did not exist -- and by whom.

2. An inquiry into the role of Inspector Sanjay Taralgatti and the Anti-Extortion \
   Cell in registering FIR No. 0654/2022 without examining any accused or \
   verifying any evidence.

3. A comprehensive investigation into Abhishek Badriprasad Saraf -- his fraudulent \
   occupation of Esplanade House, his fraud proceedings in the Calcutta High Court, \
   and any attempts by him to influence, bribe or manipulate police officers in Mumbai.

4. Appropriate relief to Mr. Tarun Thadani, who has suffered four years of \
   reputational and personal damage as a result of a fabricated complaint.

I am available to provide any further information, documents or assistance required \
by your office. Please feel free to contact me directly.

Yours faithfully,

Adv. Sujata Shirasi
Counsel for Mr. Tarun Thadani
Phone: +91 93216 13691
E-mail: sujata.shirasi@pressdetective.com

Note: This letter is issued on behalf of Mr. Tarun Thadani in the public interest. \
All allegations against Abhishek Badriprasad Saraf are drawn from court records, \
filed complaints and investigation documents. This is not a media release. \
Journalists may contact the above number for further information.
"""

REPORT_SUBJECT_TMPL = (
    '[TT-FIR][{status}][9Jun2026] Tarun Thadani complaint broadcast -- '
    '{sent}/3031 sent | Abhishek Saraf FIR 0654/2022 | '
    'sujata.shirasi@pressdetective.com | 9 Jun 2026'
)


def load_contacts() -> list[str]:
    here     = Path(__file__).parent
    csv_path = here.parents[1] / 'contacts' / 'contacts_master.csv'
    if not csv_path.exists():
        raise FileNotFoundError(f'contacts_master.csv not found at {csv_path}')
    contacts = []
    with open(csv_path, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            email = row.get('email', '').strip().lower()
            case  = row.get('case', '').strip().lower()
            if email and case != 'olympio-almeida':
                contacts.append(email)
    seen, out = set(), []
    for e in contacts:
        if e not in seen:
            seen.add(e); out.append(e)
    return out


def send_report(result: dict, dry_run: bool = False) -> None:
    status = 'OK' if not result['errors'] else f"{len(result['errors'])} ERRORS"
    lines = [
        'Tarun Thadani Formal Complaint -- Send Report',
        f'Date   : 9 June 2026',
        f'From   : sujata.shirasi@pressdetective.com',
        f'Sent   : {result["sent"]}',
        f'Skipped: {result["skipped"]} (invalid emails)',
        '',
    ]
    if result['errors']:
        lines.append(f'ERRORS ({len(result["errors"])}):')
        lines += [f'  {e}' for e in result['errors']]
    else:
        lines.append('All batches sent successfully. No errors.')
    if result['invalid']:
        lines += ['', f'Invalid addresses ({len(result["invalid"])}):']
        lines += [f'  {e}' for e in result['invalid'][:50]]

    report_body = '\n'.join(lines)
    msg = build_msg(
        from_acc=FROM_ACC,
        to='info@pressdetective.com',
        subject=REPORT_SUBJECT_TMPL.format(status=status, sent=result['sent']),
        body=report_body,
    )
    send_mail(msg, from_acc=FROM_ACC, dry_run=dry_run)
    if not dry_run:
        print('Report sent to info@pressdetective.com')


def main():
    ap = argparse.ArgumentParser(description='Broadcast Tarun Thadani complaint via Proton Bridge')
    ap.add_argument('--dry-run', action='store_true', help='Preview only -- send nothing')
    ap.add_argument('--start',   type=int, default=0, help='Skip first N recipients (resume)')
    ap.add_argument('--limit',   type=int, default=0, help='Send to at most N (0=all)')
    args = ap.parse_args()

    contacts = load_contacts()
    print(f'Loaded {len(contacts)} contacts (excluding Goa)\n')

    # Preview email copy to info@ first
    if not args.dry_run:
        print('Step 0: Sending preview copy to info@pressdetective.com ...')
        preview = build_msg(
            from_acc=FROM_ACC,
            to='info@pressdetective.com',
            subject=f'[PREVIEW] {SUBJECT}',
            body=BODY,
        )
        send_mail(preview, from_acc=FROM_ACC)
        print('  OK\n')

    result = send_batched(
        recipients=contacts,
        from_acc=FROM_ACC,
        subject=SUBJECT,
        body=BODY,
        cc=CC,
        batch_size=40,
        pause=20,
        dry_run=args.dry_run,
        start=args.start,
        limit=args.limit,
        verify=True,
    )

    send_report(result, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
