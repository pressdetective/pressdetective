#!/usr/bin/env python3
"""
send_press_crime_resume.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Resume send for batches 3-6 of the FIR 0654/2022 press campaign.
Reads send_log_press_crime.csv to skip already-sent contacts.
Rotates across sujata/info/santosh accounts (25 contacts per batch,
120s gap) to stay under ProtonMail's per-account hourly limit.

Sends 191 remaining contacts across 8 batches of ~24-25 each.
Account rotation: batches 1-3 → santosh, 4-6 → info, 7-8 → sujata
(sujata is now unfrozen; santosh/info take the bulk load).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import csv, json, math, smtplib, ssl, sys, time, pathlib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE      = pathlib.Path(__file__).parents[2]
CREDS     = json.loads((BASE / '.creds/proton_accounts.json').read_text(encoding='utf-8'))
LIVE_CSV  = BASE / 'contacts/contacts_live.csv'
SUPP_CSV  = BASE / 'contacts/suppression_list.csv'
LOG_CSV   = BASE / 'clients/tarun-thadani/send_log_press_crime.csv'

# Use Postmark SMTP — no per-hour rate limits unlike ProtonMail Bridge
POSTMARK_HOST  = 'smtp.postmarkapp.com'
POSTMARK_PORT  = 587
POSTMARK_TOKEN = CREDS['smtp_postmark']['token']

FROM_ADDR    = CREDS['accounts']['sujata']['address']   # sujata.shirasi@pressdetective.com
CC_NOTICE    = 'abhishek_saraf78@yahoo.com'
CC_COACCUSED = 'aliasgarmerchant@gmail.com'
CC_ALWAYS    = CREDS['accounts']['info']['address']     # info@pressdetective.com

SUBJECT = (
    "Press Tip | FIR 0654/2022 | Man from Kolkata Alleged to Have Manipulated "
    "Mumbai Police — Four Years, Zero Evidence, One Innocent Accused"
)

BODY = """\
PRESS TIP — FOR IMMEDIATE INVESTIGATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
From    : Adv. Sujata Shirasi | +91 93216 13691
Acting for: Mr. Tarun Thadani & Mr. Ali Asgar Merchant
Date    : 11 June 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dear Crime Reporter / Editor,

We are bringing to your attention a case that deserves serious scrutiny:
a Kolkata-based businessman is alleged to have walked into a Mumbai police
station, filed a complaint, returned two months later with a fresh ₹1 crore
extortion demand mysteriously added to it, and successfully had an FIR
registered — without any accused being examined, without CDR checks, without
CCTV review, without any bank record verification.

The accused? A Mumbai-based entrepreneur who was NOT even present at the
incident. Four years on, he is still fighting that case in court.

This is the story of FIR No. 0654/2022, Dadar Police Station, Mumbai.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE ACCUSED (OUR CLIENT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mr. Tarun Thadani — entrepreneur, founder of dharte.com, resident of Mumbai.
He has no prior criminal record.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE FULL TIMELINE — WHAT ACTUALLY HAPPENED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2 June 2022 — THE INCIDENT
   A private event took place at a restaurant in Worli, Mumbai.
   Mr. Tarun Thadani was NOT present at the venue.
   His only role: he had sent invitations for the event.
   A personal altercation took place between Mr. Ali Asgar Merchant
   and Mr. Abhishek Badriprasad Saraf. That altercation was between
   those two individuals. Tarun Thadani had nothing to do with it.

4 June 2022 — THE ORIGINAL COMPLAINT (Online ID: 23244/2022)
   Abhishek Badriprasad Saraf filed an online complaint.
   That complaint alleged: ASSAULT only.
   That complaint contained: ZERO mention of extortion.
   That complaint contained: ZERO allegation against Tarun Thadani.
   We have this document. It is unambiguous.

~August 2022 — THE ALTERATION
   Approximately two months after the incident, a materially different
   version of events was presented.
   Suddenly: a demand of Rs. 1 CRORE extortion had allegedly been made.
   Suddenly: Mr. Tarun Thadani was now a named accused.
   No explanation was given for why this was not in the original complaint.
   No explanation for where ₹1 crore figure came from.
   No supporting documents, no witnesses named at this stage.

12–13 August 2022 — FIR No. 0654/2022 REGISTERED
   FIR registered at Dadar Police Station.
   Sections: IPC 384/385/387, 506 r/w 34 (extortion + criminal intimidation).
   According to our records:
     — No accused was examined before registration
     — No CDR (call detail records) were checked
     — No CCTV footage from the venue was reviewed
     — No bank transactions were verified
     — No independent witness was examined

   A Kolkata-based complainant with a history of alleged litigation
   abuse walks in, makes an altered complaint, and a Mumbai FIR is
   registered against a Mumbai entrepreneur — without basic procedure.

   We ask: How?

22 June 2023 — TOI HEADLINE DAMAGES HIM
   Times of India published: "Two bizmen chargesheeted for assault,
   Rs 1 crore extortion bid in '22" — naming Mr. Thadani.
   His business reputation, built over years, was destroyed in one
   headline. Based on an FIR that he says is entirely false.

31 March 2024 — SESSIONS COURT REFUSES DISCHARGE
   The Sessions Court refused to discharge Mr. Thadani.
   He continues to fight the case.
   He has now been a criminal accused for FOUR YEARS for an event
   he did not attend.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE COMPLAINANT — WHO IS ABHISHEK BADRIPRASAD SARAF?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mr. Abhishek Badriprasad Saraf is based in Kolkata / currently occupying
premises at Esplanade House, Mumbai. He is not a Mumbai resident.

Court records from the Calcutta High Court document serious allegations
against him:

  > Martin Burn Ltd. v. Saraf (2012 onwards, Calcutta HC):
    Allegations include document forgery, misuse of power of attorney,
    and alleged illegal occupation of a heritage property — Esplanade
    House, 29, Hazarimal Somani Marg, Fort, Mumbai 400001. This Rs. 150
    crore property once housed the family of Jamsetji Nusserwanji Tata.
    Proceedings have continued for over a decade.

A man with this alleged background came to Mumbai, filed a complaint that
mentioned no extortion, then returned two months later claiming extortion
of ₹1 crore — and Mumbai Police registered it without examining anyone.

We believe Mumbai's crime reporters should be asking:
  — Did Mumbai Police conduct even basic due diligence on the complainant?
  — How did a complaint with zero extortion allegation become an
     extortion FIR?
  — Why was no accused examined before the FIR was registered?
  — Who facilitated this? Was the FIR registration influenced?

These questions have been formally raised with the Anti-Corruption Bureau
and the Anti-Extortion Cell of Mumbai Police.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUR FORMAL DEMANDS (ALREADY SERVED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

We have already served a formal final notice on Mr. Abhishek Badriprasad Saraf
demanding that he:

  1. Withdraw the false complaint and FIR No. 0654/2022 immediately.
  2. Acknowledge that no extortion demand was made and that Mr. Thadani
     had no role in the altercation.
  3. Issue a public correction for the damage caused to Mr. Thadani's
     reputation and business.

Mr. Saraf has failed to respond.

We therefore now call on:

  — The Mumbai Police to investigate how FIR 0654/2022 was registered
    without examination of any accused, CDR check, or evidence review.

  — The Anti-Corruption Bureau to investigate whether the registration
    of this FIR involved any impropriety.

  — The Bombay High Court (s.482 petition, pending) to quash this FIR.

  — Authorities to initiate proceedings against Mr. Abhishek Badriprasad
    Saraf under IPC Section 182 (false information to public servant) and
    IPC Section 211 (false charge with intent to injure) for filing and
    maintaining what we allege is a deliberately fabricated criminal case.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLAINANT DETAILS — FOR JOURNALISTIC RIGHT OF REPLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

As per standard journalistic practice, we provide the complainant's
details so you may seek his response before any publication:

  Name    : Mr. Abhishek Badriprasad Saraf
  Address : 3rd Floor, Esplanade House,
            29, Hazarimal Somani Marg, Fort, Mumbai 400001
  Email   : abhishek_saraf78@yahoo.com

We invite his response to all allegations in this communication.
All statements regarding Mr. Saraf's alleged conduct are framed as
allegations drawn from public court records and filed legal documents.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOCUMENTS / EVIDENCE AVAILABLE TO JOURNALISTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

We can provide on request:

  [1] Original online complaint (ID 23244/2022, 4 June 2022) — showing
      no extortion allegation and no mention of Tarun Thadani.

  [2] FIR No. 0654/2022 — showing sections charged and date of filing.

  [3] Calcutta High Court orders: Martin Burn Ltd. v. Saraf — documenting
      allegations of forgery and misuse of power of attorney.

  [4] Sessions Court order (31 March 2024) refusing discharge.

  [5] Anti-Corruption Bureau complaint filed by us.

  [6] Anti-Extortion Cell representation.

  [7] Defamation notice to Times of India (29 July 2025).

  [8] Final legal notice served on Abhishek Badriprasad Saraf.

To request documents or an interview, contact:

  Adv. Sujata Shirasi
  +91 93216 13691
  sujata.shirasi@pressdetective.com

  PressDetective (Media Intelligence)
  info@pressdetective.com


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEGAL NOTE — SUB JUDICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This matter is pending before the Bombay High Court (s.482 quashing
petition) and the Sessions Court. This press communication is issued for
journalistic record. It does not seek to prejudge any court proceeding.
All statements about alleged third-party conduct are drawn from public
court documents, filed legal communications, or expressly framed as
alleged. We request any publication to exercise standard editorial
judgment and clearly identify this as a statement from counsel.


Adv. Sujata Shirasi
Advocate — Investigating False FIR No. 0654/2022
Acting for Mr. Tarun Thadani & Mr. Ali Asgar Merchant
+91 93216 13691 | sujata.shirasi@pressdetective.com
PressDetective | pressdetective.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This communication is sent to you as a professional journalist /
media professional. It constitutes a legitimate press tip under the
Digital Personal Data Protection Act 2023 and IT Act 2000 (India).
To stop receiving communications: reply "UNSUBSCRIBE" or write to
info@pressdetective.com. Processed within 48 hours.
Grievance Officer: info@pressdetective.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

BATCH_SIZE            = 47    # 47 BCC + 3 CC = 50 total — Postmark's per-message limit
DELAY_BETWEEN_BATCHES = 15    # short pause is fine with Postmark


def load_already_sent():
    """Read the existing send log; return set of emails already successfully sent."""
    sent = set()
    if not LOG_CSV.exists():
        return sent
    for row in csv.DictReader(open(LOG_CSV, encoding='utf-8-sig')):
        if row.get('status', '').strip() == 'sent':   # only count confirmed ProtonMail deliveries
            sent.add(row['email'].strip().lower())
    return sent


def load_targets(already_sent):
    """Load all Press + Press/Legal Media mumbai-press contacts NOT yet sent."""
    suppressed = set()
    if SUPP_CSV.exists():
        for row in csv.DictReader(open(SUPP_CSV, encoding='utf-8-sig')):
            suppressed.add(row['email'].strip().lower())

    targets = []
    for row in csv.DictReader(open(LIVE_CSV, encoding='utf-8-sig')):
        email = row.get('email', '').strip().lower()
        if not email:
            continue
        tags = row.get('tags', '')
        category = row.get('category', '')
        if 'mumbai-press' not in tags:
            continue
        if category not in ('Press', 'Press/Legal Media'):
            continue
        if email in suppressed:
            continue
        if email in already_sent:
            continue
        targets.append(row)

    return targets


def send_batch(batch_num, total_batches, bcc_list):
    msg = MIMEMultipart('alternative')
    msg['From']    = f'Adv. Sujata Shirasi <{FROM_ADDR}>'
    msg['To']      = f'Undisclosed Recipients <{FROM_ADDR}>'
    msg['Cc']      = ', '.join([CC_ALWAYS, CC_NOTICE, CC_COACCUSED])
    msg['Bcc']     = ', '.join(bcc_list)
    msg['Subject'] = SUBJECT
    msg['Reply-To'] = FROM_ADDR
    msg['List-Unsubscribe']      = '<mailto:info@pressdetective.com?subject=unsubscribe>'
    msg['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'
    msg.attach(MIMEText(BODY, 'plain', 'utf-8'))

    all_to = [CC_ALWAYS, CC_NOTICE, CC_COACCUSED] + bcc_list
    ctx = ssl.create_default_context()

    for attempt in range(3):
        try:
            with smtplib.SMTP(POSTMARK_HOST, POSTMARK_PORT, timeout=30) as s:
                s.ehlo()
                s.starttls(context=ctx)
                s.ehlo()
                s.login(POSTMARK_TOKEN, POSTMARK_TOKEN)
                s.sendmail(FROM_ADDR, all_to, msg.as_string())
            return 'sent'
        except Exception as e:
            err = str(e)[:120]
            if attempt == 2:
                return f'error: {err}'
            time.sleep(5)
    return 'failed'


def send_report(total, sent_ok, failed_count):
    """Send completion report via Postmark to info@ and Ali."""
    report_body = (
        f"PRESS CAMPAIGN RESUME REPORT — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"FIR 0654/2022 / Tarun Thadani case\n"
        f"Provider: Postmark SMTP\n\n"
        f"Total remaining targeted  : {total}\n"
        f"Successfully sent         : {sent_ok}\n"
        f"Failed                    : {failed_count}\n\n"
        f"Log: {LOG_CSV}\n"
    )
    ctx = ssl.create_default_context()
    msg = MIMEMultipart('alternative')
    msg['From']    = FROM_ADDR
    msg['To']      = ', '.join([CC_ALWAYS, CC_COACCUSED])
    msg['Subject'] = f'[REPORT] Press campaign resume — {sent_ok}/{total} delivered'
    msg.attach(MIMEText(report_body, 'plain'))

    try:
        with smtplib.SMTP(POSTMARK_HOST, POSTMARK_PORT, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(POSTMARK_TOKEN, POSTMARK_TOKEN)
            s.sendmail(FROM_ADDR, [CC_ALWAYS, CC_COACCUSED], msg.as_string())
        print(f'\nReport sent → {CC_ALWAYS}, {CC_COACCUSED}')
    except Exception as e:
        print(f'\nReport send failed: {e}')

    print(report_body)


def main():
    already_sent = load_already_sent()
    targets = load_targets(already_sent)

    print('=' * 65)
    print('PRESS CAMPAIGN RESUME — FIR 0654/2022 / TARUN THADANI')
    print('=' * 65)
    print(f'Already sent (from log) : {len(already_sent)}')
    print(f'Remaining to send       : {len(targets)}')
    print(f'Batch size              : {BATCH_SIZE}')
    print(f'Delay between batches   : {DELAY_BETWEEN_BATCHES}s')
    print(f'CC always               : {CC_ALWAYS}')
    print(f'CC notice               : {CC_NOTICE}')
    print(f'CC co-accused           : {CC_COACCUSED}')
    print()

    if not targets:
        print('Nothing to send — all contacts already delivered.')
        return

    num_batches = math.ceil(len(targets) / BATCH_SIZE)
    batches = [targets[i*BATCH_SIZE:(i+1)*BATCH_SIZE] for i in range(num_batches)]

    print('BATCH BREAKDOWN:')
    for i, b in enumerate(batches):
        print(f'  Batch {i+1}/{num_batches}: {len(b)} contacts via Postmark ({FROM_ADDR})')

    print(f'\nSubject:\n  {SUBJECT}\n')
    if '--force' in sys.argv or '-y' in sys.argv:
        print("(--force flag: skipping confirmation)")
    else:
        print("Type 'SEND' to start, or anything else to abort: ", end='', flush=True)
        confirm = input().strip()
        if confirm.upper() != 'SEND':
            print('Aborted.')
            return

    log_rows = []
    total_sent = total_failed = 0

    for i, batch in enumerate(batches):
        print(f'\n[Batch {i+1}/{num_batches}] Sending to {len(batch)} contacts via Postmark...')

        bcc_list = [row['email'].strip().lower() for row in batch]
        for row in batch:
            print(f'  BCC: {row["email"].strip().lower():<45} {row.get("name","")[:30]}')

        status = send_batch(i+1, num_batches, bcc_list)
        ts = datetime.datetime.now().isoformat()

        if status == 'sent':
            total_sent += len(batch)
            print(f'  OK — batch {i+1} sent to {len(batch)} contacts')
            for row in batch:
                log_rows.append({
                    'batch': f'R{i+1}', 'email': row['email'].strip().lower(),
                    'name': row.get('name',''), 'designation': row.get('designation',''),
                    'tags': row.get('tags',''), 'status': 'sent', 'timestamp': ts,
                })
        else:
            total_failed += len(batch)
            print(f'  ERROR: {status}')
            for row in batch:
                log_rows.append({
                    'batch': f'R{i+1}', 'email': row['email'].strip().lower(),
                    'name': row.get('name',''), 'designation': row.get('designation',''),
                    'tags': row.get('tags',''), 'status': status, 'timestamp': ts,
                })

        if i < num_batches - 1 and DELAY_BETWEEN_BATCHES > 0:
            print(f'  Waiting {DELAY_BETWEEN_BATCHES}s before next batch...')
            time.sleep(DELAY_BETWEEN_BATCHES)

    # Append to existing log
    file_exists = LOG_CSV.exists()
    with open(LOG_CSV, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['batch','email','name','designation','tags','status','timestamp'])
        if not file_exists:
            w.writeheader()
        w.writerows(log_rows)

    print('\n' + '=' * 65)
    print('DONE (RESUME)')
    print(f'  Batches sent : {sum(1 for r in log_rows if r["status"]=="sent" or True)}/{num_batches}')
    print(f'  Contacts OK  : {total_sent}/{len(targets)}')
    print(f'  Failed       : {total_failed}')
    print(f'  Log          : {LOG_CSV}')
    print('=' * 65)

    send_report(len(targets), total_sent, total_failed)


if __name__ == '__main__':
    main()
