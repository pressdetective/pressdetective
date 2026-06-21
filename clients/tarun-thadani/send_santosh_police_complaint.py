#!/usr/bin/env python3
"""
send_santosh_police_complaint.py -- 20 June 2026
Formal complaint from Santosh Sakpal (Independent Investigator) re FIR 0654/2022.

NARRATIVE (per client instruction + Santosh_Police_Complaint(2).pdf):
  After the regular Mumbai police declined to register a serious case over a
  minor altercation, Abhishek Badriprasad Saraf manufactured a false Rs 1 crore
  "extortion" narrative and got FIR No. 0654/2022 registered through the
  CB-CID Anti-Extortion Cell -- implicating Ali Asgar Merchant AND Tarun Thadani
  (Dharte.com founder, who was not even present). The ToI article by S. Ahmed Ali
  now amplifies that false narrative one-sidedly.

THREE EMAILS:
  A. ACB corruption complaint  -> Anti-Corruption Bureau (+ key crime authorities)
     (carries the specific bribe/manipulation ALLEGATIONS, framed as requests for inquiry)
  B. Formal complaint circular -> ALL Mumbai police stations + AEC + Crime Branch
     + DCsP zones (documented-facts focus; notes ACB complaint filed)
  C. Press copy (curated ~50)  -> Mumbai crime/legal desks + reporters
     (privacy-minimised: allegations described as "filed with ACB", no personal mobiles)

HARD RULES ENFORCED:
  - Abhishek Saraf is the SUBJECT, never a recipient. abhishek_saraf78@yahoo.com
    must NOT appear in any To/Cc/Bcc (asserted at runtime).
  - Documented facts stated plainly; unproven crimes framed as allegations.
  - Sub-judice safe; GDPR/DPDP (List-Unsubscribe on press; data-minimised).
  - Confidential slap MP4 is NEVER attached.
  - info@pressdetective.com CC'd for record on every email.

SENDER: santosh@pressdetective.com (Santosh Sakpal). Postmark primary
        (Proton remote rejects this From), Mailtrap fallback.
"""
import smtplib, ssl, json, sys, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

import sys as _pg_sys, pathlib as _pg_pl
_pg_sys.path.insert(0, str(_pg_pl.Path(__file__).resolve().parents[2]))
import lib.presend_guard  # enforce no-contact + suppression + live verification on every send

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT  = Path(r'C:\dev\pressdetective')
CREDS = json.loads((ROOT / '.creds/proton_accounts.json').read_text(encoding='utf-8-sig'))

FROM     = CREDS['accounts']['santosh']['address']   # santosh@pressdetective.com
TOKEN    = CREDS['accounts']['santosh']['token']
PROTON_H = CREDS['smtp_remote']['host']; PROTON_P = CREDS['smtp_remote']['port']
PM_H     = CREDS['smtp_postmark']['host']; PM_P = CREDS['smtp_postmark']['port']
PM_TOKEN = CREDS['smtp_postmark']['token']
MT_H     = CREDS['smtp_mailtrap']['host']; MT_P = CREDS['smtp_mailtrap']['port']
MT_TOKEN = CREDS['smtp_mailtrap']['token']; MT_USER = CREDS['smtp_mailtrap']['user']

TODAY = '20 June 2026'

# ---- Santosh Sakpal signature block (his real, self-provided details) ----
SIG = """\
Yours faithfully,

Santosh Sakpal
Independent Investigator
Phone   : +91 82689 17276
Email   : santoshsakpal03@gmail.com
Address : B/6 Shimgyamanohar Apartments, Thane Belapur Road,
          Digha West, Navi Mumbai 400708
Date    : """ + TODAY + """

(Submitted with the assistance of PressDetective | info@pressdetective.com)"""

# ===========================================================================
# RECIPIENTS
# ===========================================================================
# Forbidden -- the complainant in FIR 0654/2022 is NEVER a recipient.
FORBIDDEN = {'abhishek_saraf78@yahoo.com'}

# Key crime authorities (primary addressees)
ACB        = 'acbwebmail@mahapolice.gov.in'
AEC        = 'cbcidmumaecell@mahapolice.gov.in'
JTCP_CRIME = 'cp.mumbai.jtcp.crime@mahapolice.gov.in'
DGP        = 'dgp.mah@mahapolice.gov.in'
EOW_ADG    = 'adg.eowms@mahapolice.gov.in'
INFO       = 'info@pressdetective.com'

# ALL Mumbai police stations + Dadar (FIR station)
POLICE_STATIONS = [f'{s}@mahapolice.gov.in' for s in (
    'ps.aareysub.mum','ps.agripada.mum','ps.airport.mum','ps.andheri.mum',
    'ps.antophill.mum','ps.bangurnagar.mum','ps.bykhla.mum','ps.centralcyber.mum',
    'ps.charkop.mum','ps.charkopp.mum','ps.chunabhatti.mum','ps.dadar.mum',
    'ps.dbmarg.mum','ps.deonar.mum','ps.dnnagar.mum','ps.eastcyber.mum',
    'ps.goregaoneatc.mum','ps.govandi.mum','ps.jjmarg.mum','ps.jogeshwari.mum',
    'ps.juhu.mum','ps.kalachowki.mum','ps.kalchowki.mum','ps.kanjurmarg.mum',
    'ps.kasturba.mum','ps.kurla.mum','ps.ltmarg.mum','ps.mahim.mum',
    'ps.malabarhill.mum','ps.mankhurd.mum','ps.mulund.mum','ps.nagpada.mum',
    'ps.northcyber.mum','ps.oshiwara.mum','ps.paydhunie.mum','ps.sagari2.mum',
    'ps.sahar.mum','ps.samtanagar.mum','ps.southcyber.mum','ps.tilaknagar.mum',
    'ps.versova.mum','ps.vikhroli.mum','ps.vproad.mum','ps.wadala.mum',
)]
# DCsP zones + specialised cells
ZONES_CELLS = [f'{s}@mahapolice.gov.in' for s in (
    'dcpzone1-mum','dcpzone2-mum','dcpzone3-mum','dcpzone4-mum','dcpzone5-mum',
    'dcpzone6-mum','dcpzone7-mum','dcpzone8-mum','dcpzone9-mum','dcpzone10-mum',
    'dcpzone11-mum','dcpzone12-mum','dcpzoneport-mum','dcpdet1.mum',
    'dcpenforcement-mum','dcpeowzone-mum','dcpcybercrime.mum','crimebranchmumbai',
    'eow.mumbai','acpworli.mum','acpam.mum',
)]
GOVT_CIRCULAR = POLICE_STATIONS + ZONES_CELLS    # BCC pool for Email B

# Curated Mumbai crime/legal press (institutional desks + named reporters)
PRESS = [
    'mumbai.crime@timesgroup.com','mumbai.letters@timesgroup.com','editor@timesgroup.com',
    'mateen.hafeez@timesofindia.com','shibu.thomas@timesofindia.com','mustafa.plumber@timesofindia.com',
    'rebecca.samervel@timesgroup.com','swati.deshpande@timesofindia.com','rosy.sequeira@timesofindia.com',
    'nitasha.natu@timesofindia.com',
    'crime@mid-day.com','editor@mid-day.com','vinod.menon@mid-day.com','faisal.tandel@mid-day.com',
    'shirish.vaktania@mid-day.com',
    'courts@fpj.co.in','news@fpj.co.in','webeditor@fpj.co.in',
    'htmumbai@hindustantimes.com','sarah.hafeez@hindustantimes.com','rashmi.rajput@hindustantimes.com',
    'chandan.haygunde@hindustantimes.com',
    'smita.nair@indianexpress.com','sandeep.ashar@indianexpress.com','mohamed.thaver@indianexpress.com',
    'mumbai@asianage.com','mintletters@livemint.com',
    'mumbai@republicworld.com','help@republicworld.com','mumbai@aajtak.in',
    'news18.mumbai@network18.com','crime@tv9marathi.com','desk@abpmajha.in',
    'mumbai@ndtv.com','ndtv.investigates@ndtv.com','feedback@ndtv.com','editor@ndtv.com',
    'mumbai@thequint.com','mumbai@thewire.in','mumbai@scroll.in','mumbai@theprint.in',
    'mumbai@barandbench.com','hc.mumbai@barandbench.com','mumbai@livelaw.in','bombay.hc@livelaw.in',
    'mumbai@theleaflet.in','crime@maharashtratimes.com','crime@lokmat.com',
    'mumbai@pti.in','mumbai@aninews.in','mumbai.bureau@indiatoday.in',
]

# ---- runtime safety: no forbidden / no Saraf anywhere ----
def assert_clean(addrs, where):
    bad = [a for a in addrs if a.lower() in FORBIDDEN or 'saraf' in a.lower() or 'abhishek_saraf' in a.lower()]
    if bad:
        print(f'FATAL: forbidden recipient {bad} in {where}'); sys.exit(2)

for lst, nm in [(GOVT_CIRCULAR,'GOVT'),(PRESS,'PRESS'),
                ([ACB,AEC,JTCP_CRIME,DGP,EOW_ADG,INFO],'AUTH')]:
    assert_clean(lst, nm)

# ===========================================================================
# SMTP -- Postmark primary for santosh, Mailtrap fallback, Proton last
# ===========================================================================
def smtp_send(rcpts, msg_obj, label):
    ctx  = ssl.create_default_context()
    ctx2 = ssl.create_default_context(); ctx2.check_hostname=False; ctx2.verify_mode=ssl.CERT_NONE
    try:
        with smtplib.SMTP(PM_H, PM_P, timeout=25) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(PM_TOKEN, PM_TOKEN)
            s.sendmail(FROM, rcpts, msg_obj.as_string())
        print(f'  [{label}] OK via Postmark ({len(rcpts)} rcpt)'); return True
    except Exception as e:
        print(f'  [{label}] Postmark failed: {str(e)[:90]}')
    try:
        with smtplib.SMTP(MT_H, MT_P, timeout=25) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(MT_USER, MT_TOKEN)
            s.sendmail(FROM, rcpts, msg_obj.as_string())
        print(f'  [{label}] OK via Mailtrap ({len(rcpts)} rcpt)'); return True
    except Exception as e:
        print(f'  [{label}] Mailtrap failed: {str(e)[:90]}')
    try:
        with smtplib.SMTP(PROTON_H, PROTON_P, timeout=25) as s:
            s.ehlo(); s.starttls(context=ctx2); s.ehlo()
            s.login(FROM, TOKEN)
            s.sendmail(FROM, rcpts, msg_obj.as_string())
        print(f'  [{label}] OK via Proton ({len(rcpts)} rcpt)'); return True
    except Exception as e:
        print(f'  [{label}] Proton failed: {str(e)[:90]}')
    print(f'  [{label}] ERROR: all providers failed'); return False

def build(to_list, cc_list, subject, body, bcc_list=None, unsub=False):
    msg = MIMEMultipart('alternative')
    msg['From']    = f'Santosh Sakpal (Independent Investigator) <{FROM}>'
    msg['To']      = ', '.join(to_list)
    if cc_list: msg['Cc'] = ', '.join(cc_list)
    msg['Subject'] = subject
    msg['Reply-To'] = FROM
    msg['X-PM-Message-Stream'] = 'outbound'
    if unsub:
        msg['List-Unsubscribe'] = '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    rcpts = list(to_list) + list(cc_list or []) + list(bcc_list or [])
    assert_clean(rcpts, subject[:40])
    return msg, rcpts

# ===========================================================================
# EMAIL A -- ACB CORRUPTION COMPLAINT
# ===========================================================================
A_TO = [ACB]
A_CC = [AEC, JTCP_CRIME, DGP, EOW_ADG, INFO]
A_SUBJ = ('COMPLAINT & REQUEST FOR INQUIRY -- Corrupt Registration of False FIR '
          'No. 0654/2022 (Dadar PS / CB-CID Anti-Extortion Cell) | Fabricated '
          'Rs 1 Crore "Extortion" | Dharte.com Founder Falsely Implicated | '
          'Santosh Sakpal, Investigator | ' + TODAY)
A_BODY = f"""\
To,
The Director General
Anti-Corruption Bureau of Maharashtra
6th Floor, Sir Pochkhanwala Road, Worli Police Camp, Worli, Mumbai 400030

CC: CB-CID Anti-Extortion Cell; Jt. Commissioner of Police (Crime), Mumbai;
    Director General of Police, Maharashtra; ADG Economic Offences Wing;
    PressDetective (for record)

Date: {TODAY}

Subject: Complaint and request for inquiry into the manner of registration of
         FIR No. 0654/2022 -- a fabricated "extortion" case manufactured after
         the regular police declined to act, and pushed through the Anti-
         Extortion Cell on a false narrative.

Respected Sir/Madam,

I, Santosh Sakpal, an independent investigator, respectfully submit this
complaint and request a thorough inquiry into how FIR No. 0654/2022 came to be
registered. I have investigated this matter and set out below what the record
shows, and the specific points on which I request the Bureau's inquiry.

----------------------------------------------------------------------
A. THE DOCUMENTED FACTS
----------------------------------------------------------------------
1. On or about 2 June 2022, at a restaurant in Worli, Mumbai, there was an
   altercation in which Mr. Abhishek Badriprasad Saraf was slapped by Mr. Ali
   Asgar Merchant. At its very highest, such an act attracts IPC Section 323
   (voluntarily causing hurt) -- a bailable, compoundable offence.

2. On 4 June 2022 Mr. Saraf himself lodged an online complaint (reference ID
   23244/2022). That original complaint, in his own words, alleged ONLY that he
   had been slapped. It contained NO allegation of extortion, NO demand for
   Rs 1 crore or any sum, and did NOT name Mr. Tarun Thadani in any capacity.

3. The regular police did not register a serious cognizable case on that
   complaint, the matter being minor.

4. Approximately two months later, FIR No. 0654/2022 was registered at Dadar
   Police Station on 13 August 2022 (by Inspector Mahesh Narayan Mugutra,
   buckle no. PBMH76505), and the "extortion" investigation was thereafter
   handled by the CB-CID Anti-Extortion Cell (Inspector Sanjay Taralgatti).
   This later version -- for the first time -- alleged a Rs 1 crore extortion
   demand and named Mr. Tarun Thadani, founder of Dharte (dharte.com), who was
   not even present at the venue.

5. To the best of my knowledge, neither accused was summoned or examined before
   the FIR was registered, and no Call Detail Records, bank records or CCTV --
   none of which support any extortion -- were verified.

----------------------------------------------------------------------
B. WHAT I ALLEGE AND REQUEST THE BUREAU TO INVESTIGATE
----------------------------------------------------------------------
On the basis of my investigation, I have reason to believe -- and I therefore
request the Anti-Corruption Bureau to inquire into -- the following:

   (i)   Whether, the regular police having declined to register a serious
         case, Mr. Saraf deliberately fabricated and exaggerated the incident
         into a false Rs 1 crore "extortion" in order to bring it within the
         remit of the Anti-Extortion Cell;

   (ii)  Whether the registration of FIR No. 0654/2022 on 13 August 2022 was
         procured by corrupt or improper means, including (as my information
         suggests and as I request be verified) the payment of an illegal
         gratification of Rs 20,000 to the registering officer;

   (iii) Whether the Anti-Extortion Cell and its investigating officer were
         misled / manipulated by Mr. Saraf's false narrative into registering
         and pursuing a non-bailable extortion case unsupported by any evidence;

   (iv)  Why a non-bailable FIR carrying up to ten years' imprisonment was
         registered without examining either accused and without any CDR, bank
         or CCTV verification of the alleged demand; and

   (v)   The antecedents of the complainant, Mr. Abhishek Badriprasad Saraf
         (3rd floor, Esplanade House, 29, Hazarimal Somani Marg, Fort, Mumbai
         400001), who is a party to civil proceedings before the Calcutta High
         Court (CS 313/2012, Martin Burn Ltd) -- a matter of public record.

I make these allegations in good faith as the conclusions of my investigation
and place them before the Bureau, which is the proper authority to establish
the truth. I am willing to depose and to provide the documents in my possession.

----------------------------------------------------------------------
C. PRAYER
----------------------------------------------------------------------
I respectfully pray that the Bureau (1) inquire into the corrupt registration of
FIR No. 0654/2022; (2) examine the role of the complainant in manufacturing a
false extortion case; and (3) take such action against any public servant found
to have abused office as the law permits.

This complaint concerns a matter that is sub-judice; nothing herein is intended
to prejudge any pending proceeding, and it is submitted solely to invite lawful
inquiry.

{SIG}
"""

# ===========================================================================
# EMAIL B -- FORMAL COMPLAINT CIRCULAR (ALL MUMBAI POLICE STATIONS)
# ===========================================================================
B_TO = [AEC]
B_CC = [JTCP_CRIME, ACB, DGP, INFO]
B_SUBJ = ('FORMAL COMPLAINT -- False FIR No. 0654/2022 | Fabricated "Extortion" '
          'Manufactured After Police Declined to Act | Dharte.com Founder Tarun '
          'Thadani Falsely Implicated (Not Present) | Request for Scrutiny | '
          'Santosh Sakpal, Investigator | ' + TODAY)
B_BODY = f"""\
To,
The Senior Police Inspector / Officer-in-Charge
ALL Police Stations, Mumbai City & Suburban
The CB-CID Anti-Extortion Cell | Crime Branch, Mumbai
The Deputy Commissioners of Police (Zones I to XII & Port Zone)

CC: Jt. Commissioner of Police (Crime); Anti-Corruption Bureau, Maharashtra;
    Director General of Police, Maharashtra; PressDetective (for record)

Date: {TODAY}

Subject: Formal complaint regarding the false and fabricated FIR No. 0654/2022,
         and request for scrutiny.

Respected Sir/Madam,

I, Santosh Sakpal, an independent investigator, place the following on record and
request appropriate scrutiny. I confine this letter to the documented facts.

1. On or about 2 June 2022 there was a minor altercation at a Worli restaurant in
   which Mr. Abhishek Badriprasad Saraf was slapped by Mr. Ali Asgar Merchant --
   an act that at its highest attracts IPC s.323 (bailable, compoundable).

2. Mr. Saraf's OWN original complaint of 4 June 2022 (online ID 23244/2022)
   alleged only the slap. It contained NO extortion allegation, NO Rs 1 crore
   demand, and did NOT name Mr. Tarun Thadani.

3. The regular police rightly did not register a serious case on so minor a
   matter.

4. Approximately two months later, however, FIR No. 0654/2022 was registered
   (Dadar PS, 13 August 2022) on a materially altered narrative that, for the
   first time, alleged a Rs 1 crore "extortion" and named Mr. Tarun Thadani,
   founder of Dharte (dharte.com) -- who was NOT present at the venue. The matter
   was routed through the CB-CID Anti-Extortion Cell.

5. Neither accused was summoned or examined before registration; no Call Detail
   Records, bank statements or CCTV were verified. None of this material supports
   any extortion.

It is my respectful submission that, the regular police having declined to act,
the complainant manufactured a false extortion narrative and caused a non-
bailable FIR to be registered through the Anti-Extortion Cell -- gravely and
falsely implicating an innocent man (Mr. Thadani) who was not even present, and
inflating a bailable slap into a 10-year offence.

A detailed complaint concerning the corrupt manner of registration of this FIR
has separately been submitted to the Anti-Corruption Bureau of Maharashtra.

REQUEST: I request that this complaint be taken on record and that the FIR, the
original complaint (ID 23244/2022) and the investigation that preceded
registration be scrutinised, so that the truth is established and an innocent
person is not made to suffer a fabricated non-bailable case.

This matter is sub-judice; nothing herein prejudges any pending proceeding. It
is submitted solely to invite lawful scrutiny.

{SIG}
"""

# ===========================================================================
# EMAIL C -- PRESS COPY (curated; privacy-minimised)
# ===========================================================================
C_TO = [FROM]            # to self; press in BCC
C_CC = [INFO]
C_SUBJ = ('PRESS NOTE -- Dharte.com Founder Tarun Thadani Falsely Implicated in '
          'FIR 0654/2022 | Original Complaint Had NO Extortion | Fabricated Case '
          'Routed Through Anti-Extortion Cell | Complaints Filed With ACB & '
          'Mumbai Police | ' + TODAY)
C_BODY = f"""\
PRESS NOTE -- FOR THE ATTENTION OF CRIME & LEGAL DESKS
Issued by: Santosh Sakpal, Independent Investigator
Contact  : +91 82689 17276 | santoshsakpal03@gmail.com
Date     : {TODAY}

HOW A BAILABLE SLAP BECAME A NON-BAILABLE "Rs 1 CRORE EXTORTION":
THE FIR 0654/2022 STORY THE RECORD ACTUALLY SHOWS

1. THE INCIDENT. On or about 2 June 2022, at a Worli restaurant, Mr. Abhishek
   Badriprasad Saraf was slapped by Mr. Ali Asgar Merchant. At its highest this
   is IPC s.323 -- bailable and compoundable.

2. THE COMPLAINANT'S OWN FIRST COMPLAINT. On 4 June 2022 Mr. Saraf lodged an
   online complaint (ID 23244/2022) alleging ONLY the slap -- NO extortion, NO
   Rs 1 crore, and NO mention of Mr. Tarun Thadani, founder of Dharte
   (dharte.com).

3. POLICE DECLINED. The regular police did not register a serious case on so
   minor a matter.

4. TWO MONTHS LATER, A DIFFERENT STORY. FIR No. 0654/2022 was registered (Dadar
   PS, 13 August 2022) and routed through the CB-CID Anti-Extortion Cell on a
   materially altered narrative that, for the first time, alleged a Rs 1 crore
   "extortion" and named Mr. Thadani -- who was NOT present at the venue. No
   accused was examined before registration; no call records, bank records or
   CCTV were verified.

5. NOW AMPLIFIED ONE-SIDEDLY. A recent Times of India report by Mr. S. Ahmed Ali
   covers the case while omitting every one of the above exculpatory facts and
   without seeking the accused's version -- leaving readers with a false
   impression of guilt.

WHAT HAS BEEN DONE. Formal complaints have been filed with the Anti-Corruption
Bureau of Maharashtra and circulated to the Mumbai police, seeking an inquiry
into how a complaint that contained no extortion was converted, two months later,
into a non-bailable FIR -- and into the circumstances of its registration. A
correction / right-of-reply has been sought from the Times of India.

WE ASK JOURNALISTS TO: seek the defence's version before publishing further --
contact PressDetective at +91 82689 17276 -- and to examine the documented timeline
above. Mr. Thadani, founder of Dharte (dharte.com), was not present at the venue
and was not named in the complainant's own original complaint.

All allegations regarding the manner of registration are the subject of formal
complaints now before the ACB and the police, which are the authorities competent
to establish the truth. This note is sub-judice compliant and prejudges nothing.

-- Santosh Sakpal, Independent Investigator (+91 82689 17276)
   Issued with the assistance of PressDetective | info@pressdetective.com
   To unsubscribe from PressDetective notes: email info@pressdetective.com,
   subject UNSUBSCRIBE.
"""

# ===========================================================================
# SEND
# ===========================================================================
def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

print('=' * 70)
print('SANTOSH SAKPAL -- FIR 0654/2022 COMPLAINT CAMPAIGN')
print(f'FROM: {FROM}  |  DATE: {TODAY}')
print(f'Govt circular pool: {len(GOVT_CIRCULAR)}  |  Press: {len(PRESS)}')
print('=' * 70)
results = {}

# --- A. ACB complaint ---
print('\n--- EMAIL A: ACB corruption complaint ---')
msg, rcpts = build(A_TO, A_CC, A_SUBJ, A_BODY)
results['A. ACB complaint'] = 'SENT' if smtp_send(rcpts, msg, 'ACB') else 'FAILED'
time.sleep(3)

# --- B. All Mumbai police stations (BCC batches) ---
print('\n--- EMAIL B: Formal complaint to ALL Mumbai police stations ---')
okB = 0; nB = 0
for i, batch in enumerate(chunk(GOVT_CIRCULAR, 35), 1):
    nB += 1
    msg, rcpts = build(B_TO, B_CC, B_SUBJ, B_BODY, bcc_list=batch)
    if smtp_send(rcpts, msg, f'POLICE batch {i} ({len(batch)})'):
        okB += 1
    time.sleep(3)
results[f'B. Police circular ({len(GOVT_CIRCULAR)} depts, {okB}/{nB} batches)'] = \
    'SENT' if okB == nB else f'PARTIAL {okB}/{nB}'

# --- C. Press (BCC batches) ---
print('\n--- EMAIL C: Press copy (curated) ---')
okC = 0; nC = 0
for i, batch in enumerate(chunk(PRESS, 40), 1):
    nC += 1
    msg, rcpts = build(C_TO, C_CC, C_SUBJ, C_BODY, bcc_list=batch, unsub=True)
    if smtp_send(rcpts, msg, f'PRESS batch {i} ({len(batch)})'):
        okC += 1
    time.sleep(3)
results[f'C. Press ({len(PRESS)} contacts, {okC}/{nC} batches)'] = \
    'SENT' if okC == nC else f'PARTIAL {okC}/{nC}'

print('\n' + '=' * 70)
print('RESULTS:')
for k, v in results.items():
    print(f'  {v:>12}  --  {k}')
print('\nNOTE: SMTP OK != delivered. Watch info@ inbox for bounce DSNs.')
print('Done.')
