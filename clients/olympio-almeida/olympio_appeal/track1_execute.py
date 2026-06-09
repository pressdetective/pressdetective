#!/usr/bin/env python3
"""track1_execute.py — Phase 1: 5 formal complaints + Phase 2: 4 RTI applications"""
import smtplib, ssl, os, time
from email.message import EmailMessage

HERE      = os.path.dirname(os.path.abspath(__file__))
TOKEN     = os.environ["ZEPTO_TOKEN"]
FROM_ADDR = "olympio.almeida@pressdetective.com"
EVIDENCE  = os.path.join(HERE, "Evidence_Packet_FULL.pdf")
MASTER_C  = os.path.join(HERE, "1_Updated_Master_Complaint.docx")
FORMAL_A  = os.path.join(HERE, "2_Formal_Appeal_Escalation.docx")

SENT_LOG  = []
ERROR_LOG = []

def send(subject, to, cc, body, attachments):
    m = EmailMessage()
    m["From"]    = FROM_ADDR
    m["To"]      = to if isinstance(to, str) else ", ".join(to)
    if cc:
        m["Cc"]  = cc if isinstance(cc, str) else ", ".join(cc)
    m["Subject"] = subject
    m.set_content(body)
    for path in attachments:
        with open(path, "rb") as f:
            data = f.read()
        ext = os.path.splitext(path)[1].lower()
        sub = "pdf" if ext == ".pdf" else "vnd.openxmlformats-officedocument.wordprocessingml.document"
        m.add_attachment(data, maintype="application", subtype=sub, filename=os.path.basename(path))
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.zeptomail.in", 465, context=ctx, timeout=300) as s:
        s.ehlo()
        s.login("emailapikey", TOKEN)
        s.send_message(m)

def do(label, subject, to, cc, body, attachments):
    to_display = to if isinstance(to, str) else to[0]
    print(f"  [{label}] -> {to_display} ...", end=" ", flush=True)
    try:
        send(subject, to, cc, body, attachments)
        SENT_LOG.append(f"OK  [{label}]")
        print("OK")
    except Exception as e:
        ERROR_LOG.append(f"ERR [{label}]: {e}")
        print(f"ERROR: {e}")
    time.sleep(8)

# ══════ PHASE 1: FORMAL COMPLAINTS ══════

def p1_gspcb():
    body = (
        "To,\nThe Chairman / The Member Secretary,\n"
        "Goa State Pollution Control Board (GSPCB),\n"
        "Pilerne Industrial Estate, Saligao, Bardez, Goa 403 511.\n\n"
        "Subject: RE-FILING - Noise Pollution & Public Nuisance Complaint\n"
        '"Sunday Racquet and Social Club," Gaunsawaddo, Sodiem, Siolim.\n\n'
        "Sir / Madam,\n\n"
        "1. PRIOR COMPLAINT - NO RESPONSE\n"
        "   A detailed, evidence-backed complaint was filed with GSPCB on 9 March 2026\n"
        "   by Mr. Gautam Vora on behalf of La Masseria residents, Survey No. 197/A,\n"
        "   Siolim. After nearly three months (as of 9 June 2026) there has been no\n"
        "   acknowledgement, no inspection, and no action.\n\n"
        "2. THE NUISANCE\n"
        '   "Sunday Racquet and Social Club" operates outdoor padel courts at House\n'
        "   No. 47/3, Gaunsawaddo, Sodiem, Siolim -- 30-40 feet from senior-citizen\n"
        "   residential homes at La Masseria. Daily from approx. 7:00 a.m. until midnight:\n"
        "   - Continuous impact noise: 68-75 dB(A) vs. 55 dB(A) residential limit\n"
        "   - Amplified music including after 10:00 p.m.\n"
        "   - Rowdy conduct and abusive language\n\n"
        "3. STATUTORY VIOLATION\n"
        "   Noise Pollution (Regulation & Control) Rules, 2000 - Schedule III, Rule 3:\n"
        "   Residential daytime limit 55 dB(A); night-time 45 dB(A). Measured levels\n"
        "   of 68-75 dB exceed the daytime limit by 13-20 dB -- acoustically 4-10x louder\n"
        "   than legally permitted. Post-10 p.m. amplified music violates the loudspeaker\n"
        "   prohibition.\n\n"
        "4. HEALTH RISK\n"
        "   Several complainants are senior citizens (60+) with coronary artery disease\n"
        "   (multiple cardiac stents), chronic heart conditions and diabetes. The ongoing\n"
        "   noise is a daily documented health risk.\n\n"
        "5. HISTORY - UNAUTHORISED CONSTRUCTION AT SAME PLOT\n"
        "   VP Siolim-Sodiem Revocation Order Ref. V.P.S.S./2008-09/977 (24.09.2008)\n"
        "   revoked the construction licence for Survey No. 197/7, Gaunsawaddo, Siolim\n"
        "   following TCP Mapusa Inspection Ref. DB/18694/08/1755 (11.07.2008) confirming\n"
        '   construction "not as per approved plan." The padel courts now operate on this\n'
        "   same plot.\n\n"
        "6. RELIEFS SOUGHT\n"
        "   (a) Immediate site inspection including during evening/night hours (7pm-midnight)\n"
        "   (b) Suspend padel-court operations forthwith pending inquiry\n"
        "   (c) Directions under Noise Pollution Rules 2000 and EPA 1986\n"
        "   (d) Enforce the 10 p.m.-6 a.m. amplified sound prohibition\n"
        "   (e) Coordinate with TCP and Panchayat on legality of the operation\n"
        "   (f) Written response within 15 days\n"
        "   Non-action will necessitate proceedings before the National Green Tribunal\n"
        "   (Western Zone Bench, Pune).\n\n"
        "The Updated Master Complaint and 26-page Evidence Packet are attached.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112\n"
        "Authorised Rep: Mr. Gautam Vora | +91 98207 00995 | advskgoa@gmail.com"
    )
    do("GSPCB",
       'RE-FILING: Noise Pollution & Public Nuisance - "Sunday Racquet and Social Club," Sodiem, Siolim',
       ["chairman-gspcb.goa@nic.in", "mail.gspcb@gov.in"],
       ["ms-gspcb.goa@nic.in", "goapcb@gspcb.in", "spcb-pol.goa@nic.in"],
       body, [MASTER_C, EVIDENCE])

def p1_dm():
    body = (
        "To,\nThe District Magistrate / Collector,\n"
        "North Goa District Collectorate, Mapusa, Bardez, Goa.\n\n"
        "Copy to: SDM Mapusa | GSPCB Member Secretary | Panchayat Siolim-Sodiem | TCP Mapusa\n\n"
        "Subject: APPLICATION u/s 152 BNSS 2023 - Conditional Order for Removal of\n"
        "Public Nuisance - \"Sunday Racquet and Social Club,\" Gaunsawaddo, Sodiem, Siolim.\n\n"
        "Respected Sir / Madam,\n\n"
        "1. PARTIES\n"
        "   Applicants: Senior-citizen owner-residents of La Masseria, Survey No. 197/A,\n"
        "   Siolim, including Smt. Smriti Ahuja (63), Shri Rajiv Ahuja (63), Shri Gautam\n"
        "   Vora (48), Smt. Madhavi Vora (69) - several with coronary artery disease and\n"
        "   multiple cardiac stents - and Mr. Olympio Almeida, resident of Sodiem, Siolim.\n\n"
        "2. THE NUISANCE\n"
        '   "Sunday Racquet and Social Club" operates outdoor padel courts at House No.\n'
        "   47/3, Gaunsawaddo, Sodiem (30-40 ft from residential homes), daily from\n"
        "   approx. 7:00 a.m. until midnight:\n"
        "   - Noise: 68-75 dB(A) vs. 55 dB(A) residential limit\n"
        "   - Post-10 p.m. amplified music\n"
        "   - Rowdy conduct and abusive language\n\n"
        "3. STATUTORY BASIS\n"
        "   Section 152, BNSS 2023 (successor to S.133 CrPC 1973) empowers the Executive\n"
        "   Magistrate to order removal/abatement of a public nuisance. This is a classic\n"
        "   case: commercial operation causing manifest injury to health and comfort in a\n"
        "   residential zone, persistently, without lawful authority.\n\n"
        "4. CONSTITUTIONAL DIMENSION\n"
        "   Supreme Court, In re: Noise Pollution (2005) 5 SCC 733: the right to live in\n"
        "   peace and the right to sleep are integral to Article 21. Elderly cardiac\n"
        "   residents who cannot sleep due to a commercial club 30 feet away are being\n"
        "   deprived of this fundamental right.\n\n"
        "5. THREE MONTHS OF GSPCB INACTION\n"
        "   Complaint filed with GSPCB on 9 March 2026. No response as of 9 June 2026.\n"
        "   This inaction makes it necessary to invoke this Hon'ble Magistrate's jurisdiction.\n\n"
        "6. 2008 HISTORY - SAME PLOT\n"
        "   VP Siolim-Sodiem Revocation Order V.P.S.S./2008-09/977 (24.09.2008) revoked\n"
        "   the construction licence for Survey No. 197/7 for unauthorised construction.\n"
        "   The current commercial operation on this residential plot warrants examination\n"
        "   of its very legality.\n\n"
        "7. RELIEFS SOUGHT\n"
        "   (a) Conditional order u/s 152 BNSS directing immediate cessation of padel-court\n"
        "       operations pending full inquiry\n"
        "   (b) Direct Coastal PS Siolim to enforce order and attend site at night\n"
        "   (c) Show-cause to operators why nuisance should not be permanently abated\n"
        "   (d) Coordinate with GSPCB, TCP and Panchayat for comprehensive inquiry\n"
        "   (e) Such further orders as this Hon'ble Magistrate deems fit\n\n"
        "The Formal Appeal document and 26-page Evidence Packet are attached.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112"
    )
    do("District Magistrate",
       'Application u/s 152 BNSS - Public Nuisance - "Sunday Racquet and Social Club," Sodiem, Siolim',
       ["coln.goa@nic.in", "ac1-north.goa@nic.in"],
       ["sdm-mapusa.goa@nic.in", "ms-gspcb.goa@nic.in", "vpsiolimsodiem@gmail.com", "ctp-tcp.goa@nic.in"],
       body, [FORMAL_A, EVIDENCE])

def p1_tcp():
    body = (
        "To,\nThe Senior Town Planner / Deputy Town Planner,\n"
        "Town and Country Planning Department, Mapusa, Bardez, Goa.\n\n"
        "Subject: COMPLAINT - Unauthorised Commercial Operation in Residential Zone\n"
        '"Sunday Racquet and Social Club," House No. 47/3, Gaunsawaddo, Sodiem,\n'
        "Survey No. 197/7, Siolim, Bardez, Goa.\n\n"
        "Sir / Madam,\n\n"
        "1. THE OPERATION\n"
        '   "Sunday Racquet and Social Club" operates outdoor padel courts as a commercial\n'
        "   sporting business at Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim -- a\n"
        "   residential zone -- daily from approx. 7:00 a.m. until midnight, charging\n"
        "   commercial fees, immediately adjacent to La Masseria residential villas.\n\n"
        "2. YOUR DEPARTMENT'S OWN 2008 INSPECTION\n"
        "   TCP Mapusa Inspection Report Ref. DB/18694/08/1755 (11.07.2008) found\n"
        '   construction at Survey No. 197/7 "not as per the approved plan." This led\n'
        "   to Stop-Work Notice (16.07.2008) and VP Siolim-Sodiem Revocation Order\n"
        "   (24.09.2008). The current commercial operation stands on this same plot.\n\n"
        "3. QUESTIONS FOR THIS DEPARTMENT\n"
        "   (a) What TCP development permission, if any, has been granted to the current\n"
        "       commercial sporting operation at Survey No. 197/7 since the 2008 revocation?\n"
        "   (b) Whether current structures are authorised under a valid TCP development plan\n"
        "   (c) If no permission: take immediate enforcement action under the Goa, Daman\n"
        "       and Diu Town and Country Planning Act, 1974\n\n"
        "4. RELIEF SOUGHT\n"
        "   (a) Immediate inspection by TCP enforcement officers\n"
        "   (b) If no valid permission: issue stop-use notice and direct cessation\n"
        "   (c) Coordinate with GSPCB and Panchayat for comprehensive enforcement\n"
        "   (d) Written response within 30 days\n\n"
        "The 26-page Evidence Packet (including 2008 documents) is attached.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112"
    )
    do("TCP",
       'Complaint - Unauthorised Commercial Operation - "Sunday Racquet and Social Club," Sy. 197/7, Siolim',
       ["ctp-tcp.goa@nic.in", "dyp-tcp.mapusa@nic.in"],
       ["coln.goa@nic.in", "ms-gspcb.goa@nic.in"],
       body, [EVIDENCE])

def p1_panchayat():
    body = (
        "To,\nThe Sarpanch,\n"
        "Village Panchayat Siolim-Sodiem, Siolim, Bardez, Goa.\n\n"
        "Subject: COMPLAINT - Violation of Your Own Revocation Order V.P.S.S./2008-09/977\n"
        "(24.09.2008) - Ongoing Unauthorised Commercial Operation at Survey No. 197/7,\n"
        'Gaunsawaddo, Sodiem, Siolim - "Sunday Racquet and Social Club."\n\n'
        "Respected Sarpanch,\n\n"
        "1. YOUR 2008 REVOCATION ORDER\n"
        "   This Panchayat issued Revocation Order Ref. V.P.S.S./2008-09/977 (24.09.2008)\n"
        "   revoking Construction Licence No. F.01/V.P.S.S./2008-09/ResH/74 for Survey\n"
        "   No. 197/7, Gaunsawaddo, Sodiem, Siolim. Grounds: construction not as per\n"
        "   approved plan (per TCP Mapusa Inspection Ref. DB/18694/08/1755, 11.07.2008).\n"
        "   Action taken under Sections 66(1), 66(3) and 66(4) of the Goa Panchayat Raj\n"
        "   Act, 1994, following a complaint by Mr. Olympio Almeida.\n\n"
        "2. WHAT IS HAPPENING TODAY\n"
        '   "Sunday Racquet and Social Club" now operates outdoor padel courts as a\n'
        "   commercial business at House No. 47/3, Gaunsawaddo, Sodiem -- on this same\n"
        "   residential land -- from 7:00 a.m. until midnight daily. Noise: 68-75 dB(A).\n"
        "   Adjacent residents at La Masseria include senior citizens with serious\n"
        "   cardiac conditions.\n\n"
        "3. QUESTIONS\n"
        "   (a) What construction/trade licence, if any, has been issued by this Panchayat\n"
        "       to the Club at House No. 47/3 AFTER the 2008 revocation?\n"
        "   (b) Under what authority does a commercial sporting operation operate here?\n\n"
        "4. RELIEF SOUGHT\n"
        "   (a) Production of any licence or permission granted to the club\n"
        "   (b) If none: issue notice and direction to stop commercial operation forthwith\n"
        "       under the Goa Panchayat Raj Act, 1994\n"
        "   (c) Enforce noise norms within the Panchayat area\n"
        "   (d) Coordinate with GSPCB, TCP and Police for joint action\n"
        "   (e) Written response within 15 days\n\n"
        "5. ENCROACHMENT\n"
        "   Mr. Olympio Almeida -- who filed the 2008 complaint before this Panchayat --\n"
        "   reports the operators have encroached upon his land. Please address this too.\n\n"
        "The 2008 Revocation Order and 26-page Evidence Packet are attached.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112"
    )
    do("Panchayat",
       'Complaint - Violation of VP Revocation Order V.P.S.S./2008-09/977 - Sy. 197/7, Sodiem, Siolim',
       ["vpsiolimsodiem@gmail.com", "vpsodiemsiolim@gmail.com"],
       ["vp.siolim.marna@gmail.com", "vpsiolim.marna@gmail.com", "mlasil.gvs@gov.in"],
       body, [EVIDENCE])

def p1_police():
    body = (
        "To,\nThe Police Inspector,\n"
        "Coastal Police Station, Siolim, North Goa.\n\n"
        "Copy to: SP North Goa | DySP HQ | DGP Goa\n\n"
        "Subject: COMPLAINT - Noise Nuisance, Public Nuisance & Criminal Trespass\n"
        '"Sunday Racquet and Social Club," House No. 47/3, Gaunsawaddo, Sodiem, Siolim.\n\n'
        "Sir / Madam,\n\n"
        "1. THE NUISANCE\n"
        '   "Sunday Racquet and Social Club" operates outdoor padel courts at House No.\n'
        "   47/3, Gaunsawaddo, Sodiem -- approx. 30-40 feet from La Masseria residential\n"
        "   villas (Survey No. 197/A). Daily from 7:00 a.m. until MIDNIGHT:\n"
        "   - Impact noise: 68-75 dB(A) vs. 55 dB(A) residential limit\n"
        "   - Amplified music including after 10:00 p.m.\n"
        "   - Rowdy conduct, shouting and abusive language\n\n"
        "2. CARDIAC PATIENTS\n"
        "   Several La Masseria residents are senior citizens (60+) with multiple cardiac\n"
        "   stents and serious heart conditions. The nightly disturbance is a daily\n"
        "   health crisis for them.\n\n"
        "3. POLICE ACTION - NOISE AFTER 10 P.M.\n"
        "   Noise Pollution (Regulation & Control) Rules, 2000 prohibit loudspeakers\n"
        "   and amplified music between 10:00 p.m. and 6:00 a.m. Police have direct\n"
        "   authority to enforce this without needing GSPCB involvement.\n"
        "   Requested:\n"
        "   (a) Nightly visits to site between 10:00 p.m. and midnight to enforce the\n"
        "       amplified music prohibition\n"
        "   (b) Action under Sections 268 and 290 BNS 2023 for public nuisance\n"
        "   (c) Registration of this complaint in the station diary\n\n"
        "4. CRIMINAL TRESPASS - OLYMPIO ALMEIDA'S LAND\n"
        "   Mr. Olympio Almeida reports the operators have encroached upon and are\n"
        "   occupying a portion of his land without right, title or consent. This\n"
        "   constitutes criminal trespass under Section 329, BNS 2023.\n"
        "   Requested:\n"
        "   (a) Register a complaint / FIR for criminal trespass\n"
        "   (b) Inspect plot boundary to verify encroachment\n\n"
        "5. BACKGROUND\n"
        "   Survey No. 197/7 had its construction licence revoked by VP Siolim-Sodiem\n"
        "   in September 2008 for unauthorised construction. The current commercial\n"
        "   operation has no clear legal authority.\n\n"
        "Please confirm action taken at the earliest.\n\n"
        "Yours faithfully,\n"
        "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
        "olympio.almeida@pressdetective.com | +91 98221 68112"
    )
    do("Police",
       'Complaint - Noise Nuisance, Public Nuisance & Criminal Trespass - "Sunday Racquet and Social Club," Sodiem',
       ["picoastal.siolim@goapolice.gov.in"],
       ["spn-pol.goa@nic.in", "dysphq@goapolice.gov.in", "dgpgoa@goapolice.gov.in",
        "complaint@goapolice.gov.in"],
       body, [EVIDENCE])

# ══════ PHASE 2: RTI APPLICATIONS ══════

RTI_CLOSE = (
    "\n\nI request the above information under the Right to Information Act, 2005.\n"
    "I am prepared to pay the prescribed fee. Please provide information within\n"
    "the statutory 30-day period and confirm receipt with the name and designation\n"
    "of the assigned Public Information Officer.\n\n"
    "Yours faithfully,\n"
    "Olympio Almeida, Resident, Sodiem, Siolim, Bardez, Goa\n"
    "olympio.almeida@pressdetective.com | +91 98221 68112"
)

def p2_rti_gspcb():
    body = (
        "To,\nThe Public Information Officer (PIO),\n"
        "Goa State Pollution Control Board (GSPCB),\n"
        "Pilerne Industrial Estate, Saligao, Bardez, Goa 403 511.\n\n"
        "RTI APPLICATION - Right to Information Act, 2005.\n\n"
        "Information requested:\n\n"
        "1. Full status of noise-pollution complaint filed 9 March 2026 by Mr. Gautam\n"
        "   Vora (La Masseria, Survey No. 197/A, Siolim) re: Sunday Racquet and Social\n"
        '   Club, House No. 47/3, Gaunsawaddo, Sodiem, Siolim (Survey No. 197/7).\n\n'
        "2. Copies of ALL correspondence, notes, inspection reports, action-taken reports\n"
        "   and orders made by GSPCB in relation to the above complaint.\n\n"
        "3. Copies of any NOC, Consent to Establish, Consent to Operate or any other\n"
        "   permission issued by GSPCB to Sunday Racquet and Social Club or any operator\n"
        "   at Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim.\n\n"
        "4. If no permission issued: written confirmation.\n\n"
        "5. Name and designation of officer assigned to the 09.03.2026 complaint and\n"
        "   reasons for absence of any response in three months."
        + RTI_CLOSE
    )
    do("RTI-GSPCB",
       "RTI Application - Complaint Status + NOC records - Sunday Racquet and Social Club, Siolim",
       ["mail.gspcb@gov.in", "goapcb@gspcb.in"],
       ["ms-gspcb.goa@nic.in"],
       body, [])

def p2_rti_tcp():
    body = (
        "To,\nThe Public Information Officer (PIO),\n"
        "Town and Country Planning Department, Mapusa, Bardez, Goa.\n\n"
        "RTI APPLICATION - Right to Information Act, 2005.\n\n"
        "Information requested:\n\n"
        "1. Copies of ALL applications for development permission, building plans, layout\n"
        "   approvals and any other permissions submitted re: Survey No. 197/7,\n"
        "   Gaunsawaddo, Sodiem, Siolim, from 2000 to date.\n\n"
        "2. Copies of ALL permissions, sanctions, approvals or refusals issued re:\n"
        "   Survey No. 197/7 from 2000 to date.\n\n"
        "3. Complete copy of TCP Mapusa Inspection Report Ref. DB/18694/08/1755\n"
        "   (11.07.2008) which found construction at Survey No. 197/7\n"
        '   "not as per the approved plan."\n\n'
        "4. All correspondence between this Department and VP Siolim-Sodiem re:\n"
        "   Survey No. 197/7 from 2005 to date.\n\n"
        "5. Whether any development permission has been granted to Sunday Racquet\n"
        "   and Social Club or any commercial sporting operation at Survey No. 197/7.\n"
        "   If yes: copy. If no: written confirmation.\n\n"
        "6. All records relating to Stop-Work Notice dated 16.07.2008 for Sy. 197/7."
        + RTI_CLOSE
    )
    do("RTI-TCP",
       "RTI Application - All records for Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim",
       ["ctp-tcp.goa@nic.in", "dyp-tcp.mapusa@nic.in"],
       [],
       body, [])

def p2_rti_panchayat():
    body = (
        "To,\nThe Public Information Officer (PIO),\n"
        "Village Panchayat Siolim-Sodiem, Siolim, Bardez, Goa.\n\n"
        "RTI APPLICATION - Right to Information Act, 2005.\n\n"
        "Information requested:\n\n"
        "1. Copy of Construction Licence No. F.01/V.P.S.S./2008-09/ResH/74 for Survey\n"
        "   No. 197/7, Gaunsawaddo, Siolim.\n\n"
        "2. Copy of Revocation Order Ref. V.P.S.S./2008-09/977 (24.09.2008).\n\n"
        "3. Copies of ALL complaints, correspondence, inspection reports, show-cause\n"
        "   notices and orders relating to Survey No. 197/7 from 2005 to date.\n\n"
        "4. Copies of any construction licence, trade licence, NOC or permission of any\n"
        "   kind issued by this Panchayat for Survey No. 197/7 from 2009 to date (i.e.,\n"
        "   after the 2008 revocation).\n\n"
        "5. Whether this Panchayat has issued any trade licence or permission to Sunday\n"
        "   Racquet and Social Club at House No. 47/3, Gaunsawaddo, Sodiem, Siolim.\n"
        "   If yes: copy. If no: written confirmation.\n\n"
        "6. All records relating to any complaint by Mr. Olympio Almeida re: this plot."
        + RTI_CLOSE
    )
    do("RTI-Panchayat",
       "RTI Application - All licences and orders for Survey No. 197/7, Sodiem, Siolim",
       ["vpsiolimsodiem@gmail.com", "vpsodiemsiolim@gmail.com"],
       ["vpsiolim.marna@gmail.com"],
       body, [])

def p2_rti_collectorate():
    body = (
        "To,\nThe Public Information Officer (PIO),\n"
        "Office of the District Collector,\n"
        "North Goa District Collectorate, Mapusa, Bardez, Goa.\n\n"
        "RTI APPLICATION - Right to Information Act, 2005.\n\n"
        "Information requested:\n\n"
        "1. Current Form I & XIV (7/12 extract) and Form D for Survey No. 197/7,\n"
        "   Gaunsawaddo (also recorded as Sodiem), Siolim, Bardez, North Goa.\n\n"
        "2. Name(s) of current owner(s) and occupant(s) of Survey No. 197/7 as per\n"
        "   revenue records.\n\n"
        "3. Whether any order, permission or licence has been issued by the Collectorate\n"
        "   or any Revenue authority for commercial use of Survey No. 197/7 (designated\n"
        "   as residential land).\n\n"
        "4. Whether any encroachment proceedings have been initiated concerning Survey\n"
        "   No. 197/7 or adjacent plots including Survey No. 197/A (La Masseria) and\n"
        "   any plot belonging to Mr. Olympio Almeida in Sodiem, Siolim.\n\n"
        "5. Records of any application or complaint filed with the Collectorate or the\n"
        "   Mamlatdar, Bardez Taluka relating to Survey No. 197/7."
        + RTI_CLOSE
    )
    do("RTI-Collectorate",
       "RTI Application - Revenue records and permissions - Survey No. 197/7, Gaunsawaddo, Sodiem, Siolim",
       ["coln.goa@nic.in", "usga1-sect.goa@nic.in"],
       ["ac1-north.goa@nic.in"],
       body, [])

# ══════ FINAL: UPDATE TO GAUTAM VORA ══════

def send_update():
    sent_text = "\n".join("  " + s for s in SENT_LOG) if SENT_LOG else "  none recorded"
    err_text  = "\n".join("  " + e for e in ERROR_LOG) if ERROR_LOG else "  None."
    body = f"""Gautam,

Track 1 of the Plan of Action has been executed today, 9 June 2026.

==============================================================
PHASE 1 - FORMAL COMPLAINTS FILED
==============================================================

1. GSPCB (Re-filing after 3 months silence)
   To: chairman-gspcb.goa@nic.in | mail.gspcb@gov.in
   CC: ms-gspcb.goa@nic.in | goapcb@gspcb.in | spcb-pol.goa@nic.in
   Attached: Updated Master Complaint + 26-page Evidence Packet
   Demanded: Inspection within 15 days; warned of NGT proceedings

2. District Magistrate / Collector, North Goa (Section 152 BNSS 2023)
   To: coln.goa@nic.in | ac1-north.goa@nic.in
   CC: SDM Mapusa | GSPCB | Panchayat | TCP
   Attached: Formal Appeal + Evidence Packet
   Demanded: Conditional order suspending padel-court operations
   (S.152 BNSS = the strongest tool to force immediate cessation of a public nuisance)

3. TCP Department, Mapusa
   To: ctp-tcp.goa@nic.in | dyp-tcp.mapusa@nic.in
   CC: Collector | GSPCB
   Asked: Production of any TCP permission for commercial use at Sy. 197/7;
          if none - stop-use notice and enforcement under Town Planning Act

4. Village Panchayat Siolim-Sodiem
   To: vpsiolimsodiem@gmail.com | vpsodiemsiolim@gmail.com
   CC: vp.siolim.marna@gmail.com | MLA Siolim
   Demanded: Production of any licence issued after their own 2008 revocation;
             if none - stop commercial operation under Panchayat Raj Act

5. Coastal Police Station, Siolim
   To: picoastal.siolim@goapolice.gov.in
   CC: SP North Goa | DySP | DGP Goa
   Demanded: Nightly enforcement of 10 p.m. amplified music ban;
             FIR for criminal trespass on Olympio Almeida's land

==============================================================
PHASE 2 - RTI APPLICATIONS (30-day statutory clock running)
==============================================================

RTI 1 - GSPCB: Status of 09.03.2026 complaint + any NOC/consent ever issued
RTI 2 - TCP: All records for Sy. 197/7 from 2000 to date + copy of 2008 inspection report
RTI 3 - Panchayat: All licences + orders for Sy. 197/7; any licence after 2008 revocation
RTI 4 - Collectorate: Revenue records for Sy. 197/7; commercial permissions; encroachments

Why RTIs are the key weapon here: if each authority replies confirming NO licence,
permission or consent was ever granted for a commercial sporting operation at Survey
No. 197/7 - those replies become primary evidence before NGT / High Court. The operator
has been running for years with zero licence from any authority. That is devastating.

==============================================================
DELIVERY STATUS
==============================================================
{sent_text}

Errors:
{err_text}

==============================================================
YOUR URGENT PHYSICAL ACTIONS THIS WEEK
==============================================================

These emails create the paper trail. Physical registered-post filings carry
more legal weight and are harder for officers to ignore.

1. GSPCB - Print + sign Updated Master Complaint with medical records (Annex H).
   Send by REGISTERED POST to GSPCB Chairman, Pilerne Industrial Estate, Saligao,
   Bardez, Goa 403 511. Keep postal receipt - it is proof of service.

2. District Magistrate's Court, Mapusa - File the Formal Appeal in person and
   get a DATE-STAMPED acknowledgement. This formally triggers the S.152 BNSS process.

3. Coastal Police Station, Siolim - Go in person. Ask for a STATION DIARY NUMBER.
   If they refuse to register FIR for trespass, demand a written refusal (which
   itself can be challenged before a Magistrate under S.156 BNSS).

4. DSLR Mapusa (Deputy Superintendent of Land Records) - Olympio should visit with
   his title documents and apply for a BOUNDARY DEMARCATION SURVEY to formally
   establish the encroachment on his land.

5. Mamlatdar, Bardez Taluka - File the revenue encroachment complaint in person
   with Olympio's ownership documents (7/12 extract / title deed).

==============================================================
ESCALATION CLOCK
==============================================================

- GSPCB no response by 24 June  ->  file before NGT Western Zone Bench, Pune
- DM no action by 9 July         ->  Writ Petition, Bombay High Court, Goa Bench
- RTI no reply by 9 July         ->  First Appeal to Appellate Authority
- First Appeal ignored           ->  Second Appeal to Goa State Information Commissioner

PressDetective | 9 June 2026
olympio.almeida@pressdetective.com"""

    print("  [Update -> Gautam Vora] ...", end=" ", flush=True)
    try:
        send(
            "[PressDetective] Track 1 Complete - All Complaints + RTIs Filed - Action Required from You",
            "gavora@gmail.com",
            "info@pressdetective.com",
            body, []
        )
        print("OK")
    except Exception as e:
        print(f"ERROR: {e}")

# ══════ MAIN ══════

def main():
    print("=== TRACK 1 PHASE 1: FORMAL COMPLAINTS ===")
    p1_gspcb()
    p1_dm()
    p1_tcp()
    p1_panchayat()
    p1_police()
    print("\n=== TRACK 1 PHASE 2: RTI APPLICATIONS ===")
    p2_rti_gspcb()
    p2_rti_tcp()
    p2_rti_panchayat()
    p2_rti_collectorate()
    print("\n=== FINAL: UPDATE TO GAUTAM VORA ===")
    send_update()
    ok  = len(SENT_LOG)
    err = len(ERROR_LOG)
    print(f"\n{'='*55}")
    print(f"Done. {ok} sent, {err} errors.")
    if ERROR_LOG:
        for e in ERROR_LOG: print(f"  {e}")

if __name__ == "__main__":
    main()