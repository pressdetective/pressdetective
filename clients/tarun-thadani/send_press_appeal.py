#!/usr/bin/env python3
"""
send_press_appeal.py
Press outreach â€” Adv. Sujata Shirasi's statement on FIR 0654/2022 (Tarun Thadani)
Sender : sujata.shirasi@pressdetective.com
To     : all legal_press_contacts.csv (279 new legal press contacts)
CC     : info@pressdetective.com (always)
Report : aliasgarmerchant@gmail.com + info@pressdetective.com
"""

import csv, sys, time, pathlib, json, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict
import datetime

BASE   = pathlib.Path(__file__).parents[2]
CREDS  = json.loads((BASE / '.creds/proton_accounts.json').read_text(encoding='utf-8-sig'))

FROM_ADDR = CREDS['accounts']['sujata']['address']    # sujata.shirasi@pressdetective.com
CC_ALWAYS = CREDS['accounts']['info']['address']       # info@pressdetective.com
REPORT_TO = ['aliasgarmerchant@gmail.com', 'info@pressdetective.com']
BRIDGE_PW = CREDS['accounts']['sujata']['bridge_password']
HOST, PORT = '127.0.0.1', 1025

SUPPRESS_CSV  = BASE / 'contacts/suppression_list.csv'
PRESS_CSV     = BASE / 'contacts/legal_press_contacts.csv'
LOG_CSV       = BASE / 'contacts/send_log_press_appeal.csv'

# â”€â”€ SUBJECT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SUBJECT = (
    "Press Statement â€” Four Years of a False FIR: "
    "FIR No. 0654/2022, Dadar Police Station, Mumbai [Seeking Comment from Complainant]"
)

# â”€â”€ PRESS STATEMENT BODY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
STATEMENT = """\
FOR IMMEDIATE RELEASE
From: Adv. Sujata Shirasi, Advocate â€” Investigating False FIR No. 0654/2022
Acting for: Mr. Tarun Thadani and Mr. Ali Asgar Merchant
Date: 9 June 2026
Contact: +91 93216 13691 | sujata.shirasi@pressdetective.com

â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
FOUR YEARS OF A FALSE CRIMINAL CASE
FIR No. 0654/2022 | Dadar Police Station, Mumbai
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

Dear {name},

I write to you in my capacity as counsel for Mr. Tarun Thadani, entrepreneur
and founder of dharte.com, currently facing a false criminal case now in its
fourth year. I request your attention to this matter, which raises serious
questions about the conduct of a complainant and the procedural integrity of a
police investigation.


THE FACTS OF THE CASE
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

1. THE INCIDENT (2 June 2022)
   On the evening of 2 June 2022, a private restaurant event took place in
   Worli, Mumbai. Mr. Tarun Thadani was NOT present at the venue. His only
   connection to the event was having sent invitations for it. The altercation
   was between Mr. Ali Asgar Merchant and Mr. Abhishek Badriprasad Saraf.
   Mr. Ali Asgar Merchant slapped Saraf. Mr. Thadani was not there.

2. THE ORIGINAL COMPLAINT (4 June 2022)
   On 4 June 2022, Abhishek Badriprasad Saraf filed an online complaint
   (ID: 23244/2022). That complaint alleged assault only. It contained
   NO mention of any extortion demand. It contained NO allegation against
   Mr. Tarun Thadani whatsoever.

3. THE ALTERED COMPLAINT (~August 2022)
   Approximately two months later, a materially different version of events
   was presented to police. This new version alleged â€” for the first time â€”
   that a demand of Rs. 1 crore (extortion) had been made. Mr. Tarun Thadani's
   name was now included as an alleged co-conspirator.

4. THE FIR (12-13 August 2022)
   FIR No. 0654/2022 was registered at Dadar Police Station under IPC
   Sections 384/385/387 and 506 r/w 34 (extortion + criminal intimidation).
   According to our records, no accused was examined before registration.
   No CDR (call detail records) were checked. No bank records were verified.
   No CCTV footage was reviewed prior to the FIR.

5. THE CHARGE-SHEET AND DISCHARGE (2023â€“2024)
   A charge-sheet was filed. In June 2023, the Times of India reported the
   chargesheet, naming Mr. Thadani in the headline ("Two bizmen chargesheeted
   for assault, Rs 1 crore extortion bid in '22"), causing irreparable damage
   to his reputation.

   On 31 March 2024, the Sessions Court refused discharge.
   Mr. Thadani has been living as a criminal accused for four years for an
   incident at which he was not present.


KEY QUESTIONS WE INVITE YOU TO INVESTIGATE
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

   1. How did a complaint that contained zero reference to extortion become
      the basis for an extortion FIR two months later?

   2. How did Mr. Thadani's name enter a complaint he was not part of?

   3. Why was the FIR registered without examination of any accused, without
      CDR verification, and without any tangible evidence?

   4. What is the documented background of Mr. Abhishek Badriprasad Saraf?
      Court records from the Calcutta High Court (Martin Burn Ltd. v. Saraf,
      2012 onwards) document allegations of document forgery, misuse of power
      of attorney, and illegal occupation of a heritage property at Esplanade
      House, Mumbai â€” a Rs. 150 crore property that was once the home of
      Jamsetji Tata.


ABOUT THE COMPLAINANT â€” CONTACT FOR COMMENT
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

As per standard journalistic practice, we provide the complainant's details
so you may seek his response before any publication.

   Name    : Mr. Abhishek Badriprasad Saraf
   Address : 3rd Floor, Esplanade House, 29, Hazarimal Somani Marg,
             Fort, Mumbai 400001
   Email   : abhishek_saraf78@yahoo.com

All statements in this press release regarding Mr. Saraf's alleged conduct
are framed as allegations. We invite his response and will include any
factual correction in subsequent communications.


LEGAL NOTE (SUB JUDICE)
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
This matter is currently pending before the Bombay High Court. This press
statement is issued for journalistic record and does not seek to prejudge
the outcome of any court proceeding. All statements are either drawn from
public court documents (FIR, charge-sheet, court orders) or expressly
framed as alleged. We request any publication to clearly identify this as
a statement by counsel and to exercise standard editorial judgment.

Counsel is available for interview or clarification on request.


Adv. Sujata Shirasi
Advocate â€” Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
+91 93216 13691
sujata.shirasi@pressdetective.com

â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
This press communication is sent to you as a professional journalist /
legal media professional. It is a legitimate press statement under India's
Digital Personal Data Protection Act 2023 (DPDP Act) and IT Act 2000.
To stop receiving communications from PressDetective, reply "UNSUBSCRIBE"
or write to info@pressdetective.com. Requests are processed within 48 hours.
Grievance Officer: info@pressdetective.com
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
"""


def load_suppressed():
    s = set()
    if SUPPRESS_CSV.exists():
        for row in csv.DictReader(SUPPRESS_CSV.open(encoding='utf-8-sig')):
            if row.get('email'):
                s.add(row['email'].strip().lower())
    return s


def send_one(addr, name, suppressed, ctx):
    if addr.lower() in suppressed:
        return 'suppressed'
    display_name = name.strip() or 'Dear Journalist'
    if display_name and not display_name.lower().startswith('dear'):
        salutation = display_name.split()[0]
    else:
        salutation = 'Journalist'

    body = STATEMENT.replace('{name}', salutation)

    msg = MIMEMultipart('alternative')
    msg['From']     = f'Adv. Sujata Shirasi <{FROM_ADDR}>'
    msg['To']       = addr
    msg['Cc']       = CC_ALWAYS
    msg['Subject']  = SUBJECT
    msg['Reply-To'] = FROM_ADDR
    msg['List-Unsubscribe']      = '<mailto:info@pressdetective.com?subject=unsubscribe>'
    msg['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'
    msg.attach(MIMEText(body, 'plain'))

    for attempt in range(3):
        try:
            with smtplib.SMTP('127.0.0.1', 1025, timeout=15) as s:
                s.ehlo()
                s.starttls(context=ctx)
                s.ehlo()
                s.login(FROM_ADDR, BRIDGE_PW)
                s.sendmail(FROM_ADDR, [addr, CC_ALWAYS], msg.as_string())
            return 'sent'
        except Exception as e:
            if attempt == 2:
                return f'error: {str(e)[:80]}'
            time.sleep(3)
    return 'failed'


def send_report(results):
    sent_ok  = [r for r in results if r['status'] == 'sent']
    failed   = [r for r in results if r['status'].startswith('error') or r['status'] == 'failed']
    suppressed = [r for r in results if r['status'] == 'suppressed']

    lines = [
        f"PRESS APPEAL SEND REPORT â€” {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"From     : {FROM_ADDR}",
        f"Subject  : {SUBJECT[:80]}...",
        f"",
        f"SUMMARY",
        f"-------",
        f"Total contacts : {len(results)}",
        f"Sent OK        : {len(sent_ok)}",
        f"Suppressed     : {len(suppressed)}",
        f"Failed/Error   : {len(failed)}",
        f"",
    ]

    if failed:
        lines += ["FAILURES:", ""]
        for r in failed:
            lines.append(f"  {r['email']:<45} {r['status']}")
        lines.append("")

    lines += [
        "SENT TO (all):",
        "",
    ]
    for r in sent_ok:
        pub = r.get('designation','').split(',')[-1].strip() if ',' in r.get('designation','') else r.get('designation','')
        lines.append(f"  {r['name']:<30} {r['email']:<45} {pub}")

    report_body = "\n".join(lines)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    msg = MIMEMultipart('alternative')
    msg['From']    = FROM_ADDR
    msg['To']      = ', '.join(REPORT_TO)
    msg['Subject'] = f"[REPORT] Press Appeal Sent â€” {len(sent_ok)}/{len(results)} delivered"
    msg['Reply-To'] = FROM_ADDR
    msg.attach(MIMEText(report_body, 'plain'))

    try:
        with smtplib.SMTP('127.0.0.1', 1025, timeout=15) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(FROM_ADDR, BRIDGE_PW)
            s.sendmail(FROM_ADDR, REPORT_TO, msg.as_string())
        print(f"\nReport sent to: {', '.join(REPORT_TO)}")
    except Exception as e:
        print(f"\nReport send failed: {e}")

    return report_body


def main():
    contacts = list(csv.DictReader(PRESS_CSV.open(encoding='utf-8-sig')))
    suppressed = load_suppressed()
    print(f"Contacts to send: {len(contacts)}")
    print(f"Suppressed:       {len(suppressed)}")
    print(f"From:             {FROM_ADDR}")
    print(f"Subject:          {SUBJECT[:70]}...\n")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    results = []
    log_rows = []
    sent = failed = skipped = 0

    for i, row in enumerate(contacts):
        addr = row['email'].strip().lower()
        name = row.get('name','').strip()
        desig = row.get('designation','').strip()

        status = send_one(addr, name, suppressed, ctx)
        results.append({'email': addr, 'name': name, 'designation': desig, 'status': status})

        if status == 'sent':
            sent += 1
            sym = '[OK]'
        elif status == 'suppressed':
            skipped += 1
            sym = '[--]'
        else:
            failed += 1
            sym = '[!!]'

        print(f"  {sym} {i+1:>3}/{len(contacts)}  {addr:<45}  {status}")

        log_rows.append({
            'email': addr, 'name': name, 'designation': desig,
            'status': status, 'timestamp': datetime.datetime.now().isoformat()
        })

        # Rate-limit: pause every 10 sends
        if (i + 1) % 10 == 0 and status == 'sent':
            time.sleep(2)

    # Write send log
    with LOG_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['email','name','designation','status','timestamp'])
        w.writeheader()
        w.writerows(log_rows)

    print(f"\n{'='*60}")
    print(f"DONE â€” Sent: {sent}  |  Skipped: {skipped}  |  Failed: {failed}")
    print(f"Log: {LOG_CSV}")

    # Send report to aliasgar + info@
    report = send_report(results)
    print(report[:500])


if __name__ == '__main__':
    main()
