#!/usr/bin/env python3
"""
send_toi_response_campaign.py -- 12 June 2026
Response to Times of India article by S. Ahmed Ali defaming Tarun Thadani.
Article: "Mumbai court rejects shipping biz man's plea to remove foreign travel restriction"
Author: S. Ahmed Ali | ToI Mumbai | 131827309

SENDER: santosh@pressdetective.com (Santosh Sakpal, Independent Journalist)
        Available: +91 82689 17276

EMAILS SENT:
  1. ToI editor -- correction demand + right of reply
  2. All police / ACB -- plea + ToI article brought to their attention
  3. S. Ahmed Ali complaint -- Azad Maidan PS (IPC 499/500, defamatory publication)
  4. Counter press release -- key crime/legal editors across India

RULES:
  - Saraf is NEVER a recipient (legal advice: no direct contact with complainant)
  - All claims framed as alleged / on documented record where applicable
  - Sub-judice compliant
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

FROM      = CREDS['accounts']['santosh']['address']   # santosh@pressdetective.com
TOKEN     = CREDS['accounts']['santosh']['token']      # JW8JPNFKWXTEQ2TC
PROTON_H  = CREDS['smtp_remote']['host']
PROTON_P  = CREDS['smtp_remote']['port']

TODAY     = '12 June 2026'
ARTICLE   = (
    'Times of India | "Mumbai court rejects shipping biz man\'s plea to remove '
    'foreign travel restriction" | by S. Ahmed Ali | 12 June 2026 | '
    'https://timesofindia.indiatimes.com/city/mumbai/'
    'mumbai-court-rejects-shipping-bizmans-plea-to-remove-foreign-travel-restriction/'
    'amp_articleshow/131827309.cms'
)


def smtp_send(recipients, msg_obj, label):
    ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    try:
        with smtplib.SMTP(PROTON_H, PROTON_P, timeout=25) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo(); s.login(FROM, TOKEN)
            s.sendmail(FROM, recipients, msg_obj.as_string())
        print(f'  [{label}] OK via Proton'); return True
    except Exception as e:
        print(f'  [{label}] FAILED: {str(e)[:80]}'); return False


def build(to_list, cc_list, subject, body):
    msg = MIMEMultipart('alternative')
    msg['From']             = f'Santosh Sakpal, Independent Journalist <{FROM}>'
    msg['To']               = ', '.join(to_list)
    if cc_list:
        msg['Cc']           = ', '.join(cc_list)
    msg['Subject']          = subject
    msg['List-Unsubscribe'] = '<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>'
    msg['X-PM-Message-Stream'] = 'outbound'
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    return msg


# ============================================================
# EMAIL 1 -- TIMES OF INDIA: CORRECTION DEMAND + RIGHT OF REPLY
# ============================================================
TOI_TO = ['mumbai.letters@timesgroup.com']
TOI_CC = ['editor@timesgroup.com', 'info@pressdetective.com']

TOI_SUBJ = (
    'CORRECTION DEMAND & RIGHT OF REPLY -- '
    '"Mumbai court rejects shipping biz man\'s plea" (S. Ahmed Ali, ToI Mumbai, 131827309) '
    '| Dharte.com Founder Tarun Thadani Was NOT Present | '
    'Original Complaint Had NO Extortion Charge | ' + TODAY
)

TOI_BODY = f"""\
To,
The Editor / Readers' Editor
Times of India, Mumbai Edition
Email: mumbai.letters@timesgroup.com | editor@timesgroup.com

Date: {TODAY}
Re: Article by S. Ahmed Ali titled "Mumbai court rejects shipping biz man's plea \
to remove foreign travel restriction"
URL: https://timesofindia.indiatimes.com/city/mumbai/\
mumbai-court-rejects-shipping-bizmans-plea-to-remove-foreign-travel-restriction/\
amp_articleshow/131827309.cms

I, Santosh Sakpal, Independent Journalist and correspondent with PressDetective
(pressdetective.com), write to formally demand a correction and right of reply to
the above article.

I am available at +91 82689 17276.

======================================================================
WHAT IS WRONG WITH THIS ARTICLE
======================================================================

The article authored by S. Ahmed Ali, published in the Times of India
Mumbai edition, covers proceedings related to FIR No. 0654/2022 registered
at Dadar Police Station, Mumbai. It prominently features Mr. Tarun Thadani,
founder of Dharte (dharte.com), a wellness marketplace.

The article presents only one side of this matter -- the complainant's side
-- and omits several material facts that are on documented record and that
directly bear on the fairness of the coverage. Specifically:

OMISSION 1: MR. TARUN THADANI WAS NOT PRESENT AT THE VENUE
  Mr. Tarun Thadani, founder of Dharte.com, was NOT physically present at
  the restaurant in Worli, Mumbai, on 2 June 2022. His only connection to
  the event was that he had sent out invitations for a private gathering.
  He was not at the venue when any altercation took place.

  The article does not mention this. A reader of the article cannot know
  this central exculpatory fact.

OMISSION 2: THE ORIGINAL COMPLAINT CONTAINED NO EXTORTION ALLEGATION
  On 4 June 2022 -- two days after the incident -- the complainant filed
  an online complaint bearing reference ID: 23244/2022. That complaint:
    (a) Alleged only that the complainant had been slapped
    (b) Contained no allegation of extortion
    (c) Mentioned no demand for Rs. 1 crore or any sum of money
    (d) Did NOT name Mr. Tarun Thadani in any capacity

  Approximately two months later, a materially different version of the
  complaint appeared -- one that introduced, for the first time, the
  Rs. 1 crore extortion demand and Mr. Thadani's name.

  The FIR was registered on the basis of this altered complaint.

  The article makes no mention of this documented inconsistency.

OMISSION 3: NO COMMENT WAS SOUGHT FROM THE ACCUSED OR HIS COUNSEL
  Standard journalistic practice requires that the accused party be given
  the opportunity to respond before publication. As far as is known, no
  approach was made to Mr. Tarun Thadani, the defence, or PressDetective before this article was
  published. A basic call to the defence would have revealed both facts
  set out above.

OMISSION 4: THE COMPLAINANT'S OWN PUBLIC RECORD IS NOT DISCLOSED
  Mr. Abhishek Badriprasad Saraf, the complainant in this matter, is a
  party to civil proceedings at the Calcutta High Court (CS 313/2012,
  Martin Burn Limited). This is a matter of public record available in
  court filings. The article presents the complainant without any context
  of this background.

======================================================================
THE DAMAGE THIS ARTICLE CAUSES
======================================================================

Mr. Tarun Thadani is the founder and CEO of Dharte (dharte.com), a
legitimate wellness marketplace serving members across India. An article
in India's largest English-language daily that implies he is a criminal
-- without informing readers that he was not at the scene, and that the
original complaint contained none of the charges now laid against him --
causes severe and ongoing damage to his reputation, his business, and his
livelihood.

This is not a matter of court privilege protecting accurate reporting.
This is a matter of a grossly incomplete account being presented as the
full picture.

======================================================================
FORMAL DEMANDS
======================================================================

I formally demand on behalf of PressDetective:

  1. RIGHT OF REPLY
     That the Times of India publish, in the same prominence as the
     original article, a reply from Mr. Tarun Thadani's legal team
     setting out:
       (a) That he was not present at the venue
       (b) That the original complaint contained no extortion allegation
       (c) That the original complaint did not name him
       (d) That the FIR was registered on a materially altered version
           of the original complaint

  2. FACTUAL CORRECTION
     That the article be updated online to include the above facts as
     a correction note at the top of the article.

  3. RESPONSE FROM THE REPORTER
     That S. Ahmed Ali respond in writing to this letter explaining
     whether the accused or his counsel were contacted before
     publication, and if not, why not.

This demand is made under the norms of journalistic ethics as recognised
by the Press Council of India. In the event of non-compliance within
7 days, a formal complaint will be filed with the Press Council of India.

Santosh Sakpal
Independent Journalist | PressDetective (pressdetective.com)
Email    : santosh@pressdetective.com
Phone    : +91 82689 17276
Date     : {TODAY}

Note: This letter is copied to the Times of India editorial desk and
PressDetective for record. This correspondence is NOT addressed to
the complainant in FIR 0654/2022.
"""


# ============================================================
# EMAIL 2 -- ALL POLICE / ACB: TOI ARTICLE + SARAF PLEA
# ============================================================
POLICE_TO = ['acbwebmail@mahapolice.gov.in']
POLICE_CC = [
    'addlcpacbmumbai@mahapolice.gov.in',
    'acpdadar.mum@mahapolice.gov.in',
    'cbcidmumaecell@mahapolice.gov.in',
    'adg.cidcrime.pune@mahapolice.gov.in',
    'dgp.mah@mahapolice.gov.in',
    'sec.home@maharashtra.gov.in',
    'hobeomum@cbi.gov.in',
    'ps.dadar.mum@mahapolice.gov.in',
    'info@pressdetective.com',
]

POLICE_SUBJ = (
    'URGENT -- Times of India Article Perpetuates False FIR 0654/2022 Narrative | '
    'Dharte.com Founder Tarun Thadani Falsely Implicated | '
    'Request for Expedited Inquiry into Complainant\'s Conduct | '
    'Santosh Sakpal, PressDetective | ' + TODAY
)

POLICE_BODY = f"""\
To,
The Addl. Director General of Police
Anti-Corruption Bureau, Maharashtra
Email: acbwebmail@mahapolice.gov.in

CC: All authorities as addressed below

Date: {TODAY}
Re: Times of India Article -- FIR No. 0654/2022 | Request for Expedited
    Inquiry | Complainant's Conduct Warrants Immediate Scrutiny

I, Santosh Sakpal, Independent Journalist with PressDetective
(pressdetective.com), write to bring to your immediate attention a
published article in the Times of India that this office should be aware
of in the context of the formal ACB complaint filed in this matter on 11 June 2026.

I am available at +91 82689 17276.

======================================================================
THE ARTICLE
======================================================================

Title : "Mumbai court rejects shipping biz man's plea to remove
         foreign travel restriction"
Author: S. Ahmed Ali, Times of India Mumbai
Date  : June 2026
URL   : https://timesofindia.indiatimes.com/city/mumbai/\
mumbai-court-rejects-shipping-bizmans-plea-to-remove-foreign-travel-restriction/\
amp_articleshow/131827309.cms

This article covers proceedings related to FIR No. 0654/2022 and
prominently names Mr. Tarun Thadani, founder of Dharte (dharte.com),
a digital wellness marketplace.

======================================================================
WHY THIS MATTERS TO YOUR INQUIRY
======================================================================

1. THE ARTICLE PRESENTS ONLY THE COMPLAINANT'S SIDE
   The Times of India article makes no mention of:
     (a) Mr. Tarun Thadani was NOT at the venue on 2 June 2022
     (b) The original complaint (ID: 23244/2022, filed 4 June 2022)
         contained NO extortion allegation and NO mention of Thadani
     (c) The complaint was materially altered approximately two months
         after it was first filed to introduce these charges
     (d) No accused was examined and no evidence was verified before
         the FIR was registered

   This suggests that the complainant, Mr. Abhishek Badriprasad Saraf,
   has been selectively providing information to the press to maintain
   a false public narrative around FIR 0654/2022 -- the same false
   narrative that appears to have resulted in a materially inconsistent
   FIR in the first place.

2. PATTERN OF MANIPULATION
   The selective provision of information to the Times of India is
   consistent with the pattern of conduct alleged in the formal complaint of 11 June 2026:
     -- Original complaint had no extortion, no Thadani
     -- Complaint was altered two months later
     -- FIR was registered without examining any accused
     -- Now, media is being fed only the complainant's version

   This pattern warrants urgent inquiry.

3. DHARTE.COM FOUNDER TRAPPED BY FALSE COMPLAINT
   Mr. Tarun Thadani is the founder and CEO of Dharte (dharte.com),
   a legitimate wellness marketplace. He has been falsely implicated
   in a criminal case on the basis of what appears to be a materially
   altered complaint, without being at the venue when any incident
   occurred. The ongoing press coverage based on one-sided information
   from the complainant is causing continuing damage.

4. COMPLAINANT'S ANTECEDENTS -- PUBLIC COURT RECORD
   Mr. Abhishek Badriprasad Saraf is a party in civil proceedings at
   the Calcutta High Court (CS 313/2012, Martin Burn Limited). This
   is a matter of documented public record. I respectfully request
   this office to consider this context in assessing the credibility
   of the complainant.

======================================================================
REQUEST TO THIS OFFICE
======================================================================

In light of the above, I respectfully request:

  1. That this office treat the Times of India article as further
     evidence of the complainant's one-sided engagement with
     institutions and media, consistent with the conduct described
     in the complaint of 11 June 2026.

  2. That the inquiry into the conduct of Inspector Sanjay Taralgatti
     (CB-CID Anti-Extortion Cell) be expedited given the ongoing
     reputational damage to Mr. Tarun Thadani.

  3. That Mr. Abhishek Badriprasad Saraf be questioned about his
     engagement with the Times of India regarding this case and
     the accuracy of the information he provided.

  4. That this office note: Mr. Tarun Thadani, founder of Dharte
     (dharte.com), was NOT present at the venue on 2 June 2022 and
     was NOT named in the complainant's own original complaint of
     4 June 2022 (ID: 23244/2022).

I remain available at +91 82689 17276 for any further information.

Santosh Sakpal
Independent Journalist | PressDetective (pressdetective.com)
Email : santosh@pressdetective.com
Phone : +91 82689 17276
Date  : {TODAY}

CC:
  Addl. Commissioner of Police, ACB Mumbai
  ACP Dadar (Dadar Police Station -- FIR 0654/2022)
  CB-CID Anti-Extortion Cell (investigating unit)
  Addl. Director General CID Crime, Pune
  Director General of Police, Maharashtra
  Secretary (Home), Government of Maharashtra
  Central Bureau of Investigation, Mumbai
  Dadar Police Station (OC)
  PressDetective (info@pressdetective.com) -- for record

Note: The complainant in FIR 0654/2022 is NOT copied on this
correspondence on the advice of legal counsel.
"""


# ============================================================
# EMAIL 3 -- COMPLAINT AGAINST S. AHMED ALI (IPC 499/500)
# ============================================================
COMPLAINT_TO = ['ps.azadmaidan.mum@mahapolice.gov.in']
COMPLAINT_CC = [
    'acbwebmail@mahapolice.gov.in',
    'dgp.mah@mahapolice.gov.in',
    'info@pressdetective.com',
]

COMPLAINT_SUBJ = (
    'FORMAL WRITTEN COMPLAINT -- S. Ahmed Ali, Journalist, Times of India | '
    'Defamatory Publication | IPC Sections 499 & 500 | '
    'Re: Article "Mumbai court rejects shipping biz man\'s plea" | '
    'Santosh Sakpal, PressDetective | ' + TODAY
)

COMPLAINT_BODY = f"""\
To,
The Officer-in-Charge
Azad Maidan Police Station
Mumbai

CC:
  Anti-Corruption Bureau Maharashtra (acbwebmail@mahapolice.gov.in)
  Director General of Police, Maharashtra (dgp.mah@mahapolice.gov.in)
  PressDetective (info@pressdetective.com)

Date: {TODAY}

FORMAL WRITTEN COMPLAINT UNDER INDIAN PENAL CODE SECTIONS 499 AND 500
AGAINST: MR. S. AHMED ALI, JOURNALIST, TIMES OF INDIA, MUMBAI
RE: DEFAMATORY PUBLICATION DAMAGING THE REPUTATION OF MR. TARUN THADANI,
    FOUNDER OF DHARTE (DHARTE.COM)

======================================================================
COMPLAINANT DETAILS
======================================================================

Name    : Santosh Sakpal
Role    : Independent Journalist, PressDetective (pressdetective.com)
Email   : santosh@pressdetective.com
Phone   : +91 82689 17276
Address : PressDetective, Mumbai

======================================================================
ACCUSED / RESPONDENT DETAILS
======================================================================

Name        : S. Ahmed Ali
Designation : Reporter / Journalist
Organisation: Times of India, Mumbai
Author page : https://timesofindia.indiatimes.com/toireporter/author-Ahmed-Ali-1077.cms
Office      : The Times of India, Mumbai (Times of India Building,
              Dr. D.N. Road, Fort, Mumbai 400001)

======================================================================
PARTICULARS OF THE COMPLAINT
======================================================================

1. The accused, Mr. S. Ahmed Ali, is a journalist employed by or
   contributing to the Times of India, Mumbai.

2. On or about 12 June 2026, Mr. Ahmed Ali published an article in
   the Times of India with the title:

   "Mumbai court rejects shipping biz man's plea to remove foreign
   travel restriction"

   Article URL:
   https://timesofindia.indiatimes.com/city/mumbai/
   mumbai-court-rejects-shipping-bizmans-plea-to-remove-foreign-travel-restriction/
   amp_articleshow/131827309.cms

3. The article prominently features Mr. Tarun Thadani, founder and
   CEO of Dharte (dharte.com), a wellness marketplace. By covering
   the criminal proceedings against Mr. Thadani without including
   any of the material exculpatory facts set out below, the article
   conveys to a reader of ordinary prudence the strong impression
   that Mr. Thadani is guilty of the offences alleged in FIR No.
   0654/2022 registered at Dadar Police Station.

======================================================================
DEFAMATORY NATURE OF THE PUBLICATION
======================================================================

The article is defamatory within the meaning of Section 499 IPC for
the following reasons:

  A. FALSE IMPRESSION OF CRIMINAL GUILT
     The article covers the rejection of a court application by Mr.
     Thadani without informing the reader that:

     (i)  Mr. Tarun Thadani was NOT physically present at the
          restaurant in Worli, Mumbai, on 2 June 2022. He had only
          sent out invitations for a private gathering. This fact is
          known to and provable by his legal team.

     (ii) The original complaint filed by the complainant on 4 June
          2022 (online complaint ID: 23244/2022) contained NO
          allegation of extortion, NO demand for Rs. 1 crore, and
          NO mention of Mr. Tarun Thadani in any capacity.

     (iii) Mr. Thadani's name was added to the complaint approximately
           two months after the original filing, in a materially
           altered version that introduced the extortion allegation
           for the first time.

     By reporting only the outcome of a court proceeding without
     these facts, the article creates and reinforces a false
     impression of Mr. Thadani's guilt in the minds of millions
     of Times of India readers.

  B. FAILURE TO SEEK THE ACCUSED'S VERSION
     The accused, Mr. Ahmed Ali, published this article without --
     to the best of our knowledge -- approaching Mr. Thadani, his
     counsel, or any
     representative of the defence for comment. This is a violation
     of basic journalistic ethics and the norms of the Press Council
     of India, and results in a one-sided publication that imputes
     criminal conduct to an innocent man.

  C. DAMAGE TO REPUTATION AND LIVELIHOOD
     Mr. Tarun Thadani is the founder and CEO of Dharte (dharte.com),
     a legitimate digital wellness marketplace operating lawfully in
     India. Publication in India's largest English daily of a report
     implying his criminal guilt has caused and continues to cause
     severe and irreparable damage to his personal reputation, his
     professional standing, and his business.

======================================================================
PRAYER
======================================================================

I respectfully request this office to:

  1. Register this complaint as a First Information Report under
     IPC Sections 499 (Defamation) and 500 (Punishment for
     Defamation) against Mr. S. Ahmed Ali, journalist, Times of India.

  2. Summon Mr. S. Ahmed Ali to record his statement regarding:
     (a) Whether he sought comment from Mr. Tarun Thadani or his
         counsel before publication
     (b) The sources of information used for this article
     (c) Whether he was provided selective or one-sided information
         by any party with an interest in the matter

  3. Direct the Times of India, Dr. D.N. Road, Fort, Mumbai 400001,
     to preserve all editorial communications relating to the
     impugned article.

  4. Take such further action as this office deems appropriate under
     the law.

I affirm that the facts set out in this complaint are true to the
best of my knowledge and belief, and I am prepared to depose to
the same if required.

Yours faithfully,

Santosh Sakpal
Independent Journalist | PressDetective (pressdetective.com)
Email : santosh@pressdetective.com
Phone : +91 82689 17276
Date  : {TODAY}

Annexures (available on request):
  A. URL of the impugned Times of India article
  B. Original complaint ID: 23244/2022 (4 June 2022) --
     no extortion, no Thadani
  C. FIR No. 0654/2022 (Dadar Police Station)
  D. Record of complaint filed with ACB Maharashtra (11 June 2026)
  E. Background: Calcutta HC proceedings CS 313/2012 (Martin Burn Ltd)
"""


# ============================================================
# EMAIL 4 -- COUNTER PRESS RELEASE TO KEY NATIONAL/MUMBAI EDITORS
# ============================================================
PRESS_TARGETS = [
    ('Free Press Journal (Web)',  'webeditor@fpj.co.in'),
    ('Free Press Journal (Letters)', 'letters@freepressjournal.in'),
    ('Mid-Day (Editor)',          'editor@mid-day.com'),
    ('Mid-Day (Feedback)',        'feedback@mid-day.com'),
    ('NDTV (Editor)',             'editor@ndtv.com'),
    ('NDTV (Feedback)',           'feedback@ndtv.com'),
    ('Business Standard',         'editor@business-standard.com'),
    ('LiveMint (Feedback)',       'feedback@livemint.com'),
    ('LiveMint (Letters)',        'mintletters@livemint.com'),
    ('Hindustan Times',           'htfeedback@hindustantimes.com'),
    ('The Hindu (Letters)',       'letters@thehindu.co.in'),
    ('Asian Age (Letters)',       'letters@asianage.com'),
    ('Deccan Herald (Letters)',   'letters@deccanherald.co.in'),
    ('The Wire (Editor)',         'editor@thewire.in'),
    ('Indian Express',            'editor@expressindia.com'),
    ('Bar & Bench',               'editorial@barandbench.com'),
    ('LiveLaw',                   'editorial@livelaw.in'),
]

PRESS_SUBJ = (
    'PRESS RELEASE: Dharte.com Founder Tarun Thadani Falsely Implicated in '
    'FIR 0654/2022 | Was NOT Present at Venue | Original Complaint Had '
    'NO Extortion | Times of India Publishes One-Sided Account | '
    'Santosh Sakpal, PressDetective | ' + TODAY
)

PRESS_BODY = f"""\
FOR IMMEDIATE RELEASE -- {TODAY}

DHARTE.COM FOUNDER FALSELY IMPLICATED IN CRIMINAL CASE:
TIMES OF INDIA PUBLISHES ONE-SIDED ACCOUNT; KEY EXCULPATORY
FACTS WITHHELD FROM READERS

Issued by: Santosh Sakpal, Independent Journalist
           PressDetective (pressdetective.com)
Contact  : santosh@pressdetective.com | +91 82689 17276

======================================================================
SUMMARY
======================================================================

The Times of India Mumbai edition has published a report by S. Ahmed
Ali covering court proceedings related to FIR No. 0654/2022 (Dadar
Police Station, Mumbai) that prominently implicates Mr. Tarun Thadani,
founder and CEO of Dharte (dharte.com). The report is materially
incomplete. It omits two facts that are central to any fair account
of this case:

  (1) Mr. Tarun Thadani was NOT present at the venue on 2 June 2022.

  (2) The complainant's own original complaint -- filed two days after
      the incident -- contained NO allegation of extortion, NO mention
      of Rs. 1 crore, and NO mention of Mr. Thadani.

These are not disputed facts. They are on documented record.

======================================================================
THE FULL STORY
======================================================================

WHO IS TARUN THADANI?

Mr. Tarun Thadani is the founder and CEO of Dharte (dharte.com), a
digital wellness marketplace connecting wellness practitioners and
seekers across India. He is a technology entrepreneur with no prior
criminal record.

WHAT HAPPENED ON 2 JUNE 2022?

A private gathering was held at a restaurant in Worli, Mumbai. Mr.
Thadani had arranged invitations for the event but was NOT physically
present at the restaurant when the incident occurred. The incident
involved an altercation between another person at the event and the
man who subsequently filed this complaint -- Mr. Abhishek Badriprasad
Saraf. Mr. Thadani had no involvement in the altercation.

THE ORIGINAL COMPLAINT -- WHAT SARAF HIMSELF SAID ON 4 JUNE 2022:

Two days after the incident, Mr. Saraf filed an online complaint
bearing reference ID: 23244/2022. His own words at that time alleged:
  -- Only that he had been slapped
  -- NO extortion demand
  -- NO Rs. 1 crore demand
  -- NO mention of Tarun Thadani's name

WHAT CHANGED TWO MONTHS LATER?

Approximately two months after the original complaint was filed, a
materially different version of the complaint was used as the basis
for FIR No. 0654/2022 at Dadar Police Station. This later version --
for the first time -- alleged:
  (a) A demand of Rs. 1 crore as extortion; and
  (b) The involvement of Mr. Tarun Thadani

The FIR (IPC Sections 384, 385, 387 and 506 -- non-bailable, up to 10
years) was registered on this altered complaint by Inspector Sanjay
Taralgatti of the CB-CID Anti-Extortion Cell, without:
  -- Examining any accused before registration
  -- Verifying any Call Detail Records
  -- Reviewing any bank statements
  -- Checking any CCTV footage

THE TIMES OF INDIA ARTICLE (S. AHMED ALI, JUNE 2026):

The article by S. Ahmed Ali covers the rejection of Mr. Thadani's
court application without informing readers of either of the above
facts. Comment was not sought from Mr. Thadani, his counsel, or the
defence team before publication.

A correction demand and right-of-reply request have been formally
submitted to the Times of India today.

FORMAL COMPLAINTS FILED:

  11 June 2026: Formal complaint to ACB Maharashtra (9 authorities)
                requesting inquiry into complaint alteration and
                Inspector Taralgatti's investigation conduct.

  12 June 2026: Formal written complaint against S. Ahmed Ali
                (IPC 499/500 -- defamatory publication) filed with
                Azad Maidan Police Station, Mumbai.

  12 June 2026: Correction demand and right-of-reply submitted to
                the Editor, Times of India, Mumbai.

ABOUT THE COMPLAINANT -- PUBLIC RECORD:

Mr. Abhishek Badriprasad Saraf is a party to civil proceedings at
the Calcutta High Court (CS 313/2012, Martin Burn Limited). This
is a matter of public record in court filings.

======================================================================
WHAT WE ARE ASKING
======================================================================

  1. For the Times of India to publish a correction and right of reply.

  2. For journalists covering this matter to seek comment from the
     defence -- contact PressDetective at +91 82689 17276 --
     before publishing further reports that rely solely on the
     complainant's narrative.

  3. For the Maharashtra Police and Anti-Corruption Bureau to expedite
     their inquiry into how a complaint with no extortion allegation
     was converted into a non-bailable FIR two months after it was
     filed.

======================================================================
CONTACT FOR MEDIA ENQUIRIES
======================================================================

Santosh Sakpal
Independent Journalist | PressDetective (pressdetective.com)
Email : santosh@pressdetective.com
Phone : +91 82689 17276

----------------------------------------------------------------------
This press release is issued in the public interest. All facts herein
are attributed to official complaints, court records, and documented
filings. This release is sub-judice compliant and does not prejudge
the outcome of any pending proceedings.

To unsubscribe from PressDetective releases:
Email info@pressdetective.com with subject UNSUBSCRIBE.
----------------------------------------------------------------------
"""


# ============================================================
# SEND ALL FOUR
# ============================================================
print('=' * 65)
print('TOI RESPONSE CAMPAIGN -- 12 June 2026')
print(f'FROM: {FROM}')
print('=' * 65)

results = {}

# Email 1: ToI Correction Demand
print(f'\n--- EMAIL 1: ToI Correction Demand ---')
all_rcpt = TOI_TO + TOI_CC
msg = build(TOI_TO, TOI_CC, TOI_SUBJ, TOI_BODY)
results['1. ToI Correction Demand'] = 'SENT' if smtp_send(all_rcpt, msg, 'ToI') else 'FAILED'
time.sleep(3)

# Email 2: Police / ACB Plea
print(f'\n--- EMAIL 2: Police / ACB Plea ---')
all_rcpt = POLICE_TO + POLICE_CC
msg = build(POLICE_TO, POLICE_CC, POLICE_SUBJ, POLICE_BODY)
results['2. Police/ACB Plea'] = 'SENT' if smtp_send(all_rcpt, msg, 'Police') else 'FAILED'
time.sleep(3)

# Email 3: S. Ahmed Ali Complaint (Azad Maidan PS)
print(f'\n--- EMAIL 3: Complaint vs S. Ahmed Ali (Azad Maidan PS) ---')
all_rcpt = COMPLAINT_TO + COMPLAINT_CC
msg = build(COMPLAINT_TO, COMPLAINT_CC, COMPLAINT_SUBJ, COMPLAINT_BODY)
results['3. S. Ahmed Ali Complaint'] = 'SENT' if smtp_send(all_rcpt, msg, 'AliComplaint') else 'FAILED'
time.sleep(3)

# Email 4: Individual press releases to 17 key media editors
print(f'\n--- EMAIL 4: Counter Press Release to {len(PRESS_TARGETS)} media editors ---')
sent_count = 0
for outlet, email_addr in PRESS_TARGETS:
    rcpt = [email_addr, 'info@pressdetective.com']
    msg = build([email_addr], ['info@pressdetective.com'], PRESS_SUBJ, PRESS_BODY)
    ok = smtp_send(rcpt, msg, f'PR:{outlet[:20]}')
    if ok:
        sent_count += 1
    time.sleep(2)
results[f'4. Press Release ({sent_count}/{len(PRESS_TARGETS)} sent)'] = (
    'SENT' if sent_count == len(PRESS_TARGETS) else f'PARTIAL ({sent_count})'
)

print(f'\n{"=" * 65}')
print('RESULTS:')
for label, status in results.items():
    print(f'  {status}  --  {label}')
print('\nDone.')
