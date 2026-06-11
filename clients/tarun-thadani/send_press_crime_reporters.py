#!/usr/bin/env python3
"""
send_press_crime_reporters.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Press campaign — FIR 0654/2022 / Tarun Thadani case
Target : Mumbai crime reporters + influencers (Press / Press/Legal Media
         categories in contacts_live.csv, tagged mumbai-press)
Method : 6 BCC batches (~48 per batch)
From   : sujata.shirasi@pressdetective.com
CC     : info@pressdetective.com
         abhishek_saraf78@yahoo.com   (formal notice to complainant)
         aliasgarmerchant@gmail.com   (co-accused kept in loop)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import csv, json, math, smtplib, ssl, time, pathlib, datetime

BASE      = pathlib.Path(__file__).parents[2]
CREDS     = json.loads((BASE / '.creds/proton_accounts.json').read_text(encoding='utf-8'))
LIVE_CSV  = BASE / 'contacts/contacts_live.csv'
SUPP_CSV  = BASE / 'contacts/suppression_list.csv'
LOG_CSV   = BASE / 'clients/tarun-thadani/send_log_press_crime.csv'

FROM_ADDR   = CREDS['accounts']['sujata']['address']       # sujata.shirasi@pressdetective.com
BRIDGE_PW   = CREDS['accounts']['sujata']['bridge_password']
CC_ALWAYS   = CREDS['accounts']['info']['address']          # info@pressdetective.com
CC_NOTICE   = 'abhishek_saraf78@yahoo.com'                  # complainant — formal notice
CC_COACCUSED= 'aliasgarmerchant@gmail.com'                  # Ali Asgar Merchant

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

NUM_BATCHES = 6
DELAY_BETWEEN_BATCHES = 90   # seconds between batches (ProtonMail rate safety)
DELAY_BETWEEN_SENDS   = 5    # seconds between individual connections per batch


def load_targets():
    """Load Press + Press/Legal Media mumbai-press contacts from live list."""
    suppressed = set()
    if SUPP_CSV.exists():
        for row in csv.DictReader(open(SUPP_CSV, encoding='utf-8-sig')):
            suppressed.add(row['email'].strip().lower())

    targets = []
    for row in csv.DictReader(open(LIVE_CSV, encoding='utf-8-sig')):
        email = row.get('email','').strip().lower()
        tags  = row.get('tags','')
        cat   = row.get('category','')
        if not email: continue
        if email in suppressed: continue
        # Press journalists + influencers with mumbai-press tag
        if 'mumbai-press' not in tags: continue
        if cat not in ('Press', 'Press/Legal Media'): continue
        targets.append(row)
    return targets


def make_batch_message(batch_recipients):
    """Build one MIME message with batch_recipients as BCC."""
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    bcc_list = [r['email'].strip() for r in batch_recipients]
    cc_list  = [CC_ALWAYS, CC_NOTICE, CC_COACCUSED]

    msg = MIMEMultipart('alternative')
    msg['From']     = f'Adv. Sujata Shirasi <{FROM_ADDR}>'
    msg['To']       = f'Undisclosed Recipients <{FROM_ADDR}>'
    msg['Cc']       = ', '.join(cc_list)
    msg['Bcc']      = ', '.join(bcc_list)
    msg['Subject']  = SUBJECT
    msg['Reply-To'] = FROM_ADDR
    msg['List-Unsubscribe']      = '<mailto:info@pressdetective.com?subject=unsubscribe>'
    msg['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'
    msg.attach(MIMEText(BODY, 'plain'))

    all_rcpts = bcc_list + cc_list
    return msg, all_rcpts


def send_batch(batch_num, batch_recipients, ctx):
    """Send one BCC batch. Returns (sent_count, error_msg|None)."""
    msg, all_rcpts = make_batch_message(batch_recipients)
    for attempt in range(3):
        try:
            with smtplib.SMTP('127.0.0.1', 1025, timeout=30) as s:
                s.ehlo()
                s.starttls(context=ctx)
                s.ehlo()
                s.login(FROM_ADDR, BRIDGE_PW)
                s.sendmail(FROM_ADDR, all_rcpts, msg.as_string())
            return len(batch_recipients), None
        except Exception as e:
            if attempt == 2:
                return 0, str(e)
            time.sleep(5)
    return 0, 'max retries exceeded'


def send_completion_report(batches_done, total_sent, total_contacts, errors):
    """Send completion summary to info@ and Ali."""
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    lines = [
        f"PRESS CAMPAIGN SEND REPORT — FIR 0654/2022 / Tarun Thadani",
        f"Completed : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"From      : {FROM_ADDR}",
        f"Subject   : {SUBJECT[:80]}...",
        f"",
        f"SUMMARY",
        f"-------",
        f"Total targets   : {total_contacts}",
        f"Batches sent    : {batches_done}/{NUM_BATCHES}",
        f"Contacts reached: {total_sent}",
        f"CC'd on all     : {CC_NOTICE}, {CC_COACCUSED}",
        f"",
    ]
    if errors:
        lines += ["BATCH ERRORS:", ""]
        for b, e in errors:
            lines.append(f"  Batch {b}: {e}")
        lines.append("")

    msg = MIMEMultipart('alternative')
    msg['From']    = FROM_ADDR
    msg['To']      = ', '.join([CC_ALWAYS, CC_COACCUSED])
    msg['Subject'] = f"[REPORT] Mumbai Press Campaign Sent — {total_sent}/{total_contacts} | FIR 0654/2022"
    msg['Reply-To'] = FROM_ADDR
    msg.attach(MIMEText('\n'.join(lines), 'plain'))

    ctx2 = ssl.create_default_context()
    ctx2.check_hostname = False
    ctx2.verify_mode = ssl.CERT_NONE
    try:
        with smtplib.SMTP('127.0.0.1', 1025, timeout=15) as s:
            s.ehlo(); s.starttls(context=ctx2); s.ehlo()
            s.login(FROM_ADDR, BRIDGE_PW)
            s.sendmail(FROM_ADDR, [CC_ALWAYS, CC_COACCUSED], msg.as_string())
        print(f"Report sent -> {CC_ALWAYS}, {CC_COACCUSED}")
    except Exception as e:
        print(f"Report send failed: {e}")


def main():
    targets = load_targets()
    total = len(targets)
    if total == 0:
        print("No targets found. Check contacts_live.csv.")
        return

    batch_size = math.ceil(total / NUM_BATCHES)
    batches = [targets[i:i+batch_size] for i in range(0, total, batch_size)]

    print("=" * 65)
    print("PRESS CAMPAIGN — FIR 0654/2022 / TARUN THADANI")
    print("=" * 65)
    print(f"From         : {FROM_ADDR}")
    print(f"CC always    : {CC_ALWAYS}")
    print(f"CC notice    : {CC_NOTICE}  (Abhishek Saraf — formal notice)")
    print(f"CC co-accused: {CC_COACCUSED}  (Ali Asgar Merchant)")
    print(f"Total targets: {total} Mumbai press journalists + influencers")
    print(f"Batches      : {len(batches)} x ~{batch_size} recipients per batch")
    print(f"Method       : BCC — each batch is one email, all in BCC")
    print()
    print("BATCH BREAKDOWN:")
    for i, b in enumerate(batches, 1):
        print(f"  Batch {i}: {len(b)} contacts")
    print()
    print("Subject:")
    print(f"  {SUBJECT}")
    print()

    confirm = input("Type 'SEND' to start, or anything else to abort: ").strip()
    if confirm != 'SEND':
        print("Aborted.")
        return

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    total_sent = 0
    errors = []
    log_rows = []
    ts = datetime.datetime.now().isoformat()

    for i, batch in enumerate(batches, 1):
        print(f"\n[Batch {i}/{len(batches)}] Sending to {len(batch)} contacts...")
        for r in batch:
            print(f"  BCC: {r['email']:45} {r.get('name','')}")

        sent_count, err = send_batch(i, batch, ctx)

        if err:
            print(f"  ERROR: {err}")
            errors.append((i, err))
            status = f'error: {err[:60]}'
        else:
            print(f"  OK — batch {i} sent to {sent_count} contacts")
            total_sent += sent_count
            status = 'sent'

        for r in batch:
            log_rows.append({
                'batch': i,
                'email': r['email'],
                'name': r.get('name',''),
                'designation': r.get('designation',''),
                'tags': r.get('tags',''),
                'status': status,
                'timestamp': ts,
            })

        if i < len(batches):
            print(f"  Waiting {DELAY_BETWEEN_BATCHES}s before next batch...")
            time.sleep(DELAY_BETWEEN_BATCHES)

    # Write log
    LOG_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['batch','email','name','designation','tags','status','timestamp'])
        w.writeheader()
        w.writerows(log_rows)

    print(f"\n{'=' * 65}")
    print(f"DONE")
    print(f"  Batches sent : {len(batches) - len(errors)}/{len(batches)}")
    print(f"  Contacts     : {total_sent}/{total}")
    print(f"  Log          : {LOG_CSV}")
    print(f"  Errors       : {len(errors)}")
    if errors:
        for b, e in errors: print(f"    Batch {b}: {e}")
    print(f"{'=' * 65}")

    send_completion_report(len(batches) - len(errors), total_sent, total, errors)


if __name__ == '__main__':
    main()
