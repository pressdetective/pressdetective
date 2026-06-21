"""
False-case / wrongful-prosecution DEFENCE ALLIES — Mumbai & Maharashtra + national.
Research date: 21 Jun 2026 (6 parallel agents, every email seen on a live source page).

Purpose: a contact set of people who WORK ON / COVER wrongful prosecution and
false FIRs — specialist defence lawyers, legal-aid bodies, legal press, court
reporters, civil-liberties NGOs, and legal commentators. Tagged by professional
BEAT, for finding defence counsel and seeking fair-hearing coverage.

NOT a name-and-shame target list. No defamatory framing of any named individual.
All outputs that use these contacts must stay truthful, sub-judice safe and
defamation safe. CC info@pressdetective.com per project rule.
"""
import csv
from pathlib import Path

ROOT   = Path(__file__).parent.parent
FINAL  = ROOT / "contacts" / "contacts_final.csv"
SUPP   = ROOT / "contacts" / "suppression_list.csv"
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]
CASE   = "tarun-thadani"
SOURCE = "falsecase_allies_research_21jun2026"

NEW_CONTACTS = [

    # ════════════════ MUMBAI CRIMINAL-DEFENCE / FIR-QUASHING FIRMS ════════════════
    ("info@whiteandbrief.com",          "White & Brief Advocates",   "White-collar + criminal defence, FIR quashing","Lawyer","criminal-defence|fir-quashing|white-collar|legal|mumbai"),
    ("lawyers@mzmlegal.com",            "MZM Legal LLP",             "White-collar crime defence","Lawyer","criminal-defence|white-collar|legal|mumbai"),
    ("legal@saroshdamania.com",         "Sarosh Damania & Co",       "Criminal defence, FIR quashing, bail","Lawyer","criminal-defence|fir-quashing|legal|mumbai"),
    ("info@elixirlegalservices.com",    "Elixir Legal Services",     "FIR quashing & false-FIR defence","Lawyer","criminal-defence|fir-quashing|legal|mumbai"),
    ("info@kaleeyantey.com",            "Kaleeyantey Law Firm",      "FIR quashing, false-FIR defence","Lawyer","criminal-defence|fir-quashing|legal|mumbai|thane|navi-mumbai"),
    ("law@solicislex.com",              "Solicis Lex",               "Criminal defence litigation","Lawyer","criminal-defence|legal|mumbai"),
    ("saifmobhani@gmail.com",           "Adv. Saif Mobhani",         "Quashing of FIR, criminal writs, bail","Lawyer","criminal-defence|fir-quashing|legal|mumbai|thane"),
    ("purvishahassociates@gmail.com",   "Purvi Shah Associates",     "FIR quashing, anticipatory bail","Lawyer","criminal-defence|fir-quashing|legal|mumbai|navi-mumbai"),
    ("contact@advocateakashchikate.com","Adv. Akash R. Chikate",     "FIR quashing at Bombay High Court","Lawyer","criminal-defence|fir-quashing|legal|pune|mumbai"),
    ("info@bharucha.in",                "Bharucha & Partners",       "White-collar crime, PMLA/PCA defence","Lawyer","criminal-defence|white-collar|legal|mumbai"),
    ("mp.bharucha@bharucha.in",         "M.P. Bharucha",             "Sr Partner, Bharucha & Partners","Lawyer","criminal-defence|white-collar|legal|mumbai"),
    ("justin.bharucha@bharucha.in",     "Justin Bharucha",           "Managing Partner — fraud/anti-corruption","Lawyer","criminal-defence|white-collar|legal|mumbai"),
    ("mumbai@azbpartners.com",          "AZB & Partners",            "White-collar crime & investigations","Lawyer","criminal-defence|white-collar|legal|mumbai"),
    ("contact@parinamlaw.com",          "Parinam Law Associates",    "Criminal disputes, white-collar","Lawyer","criminal-defence|white-collar|legal|mumbai"),
    ("service.mumbai@parinamlaw.com",   "Parinam Law Associates",    "Criminal litigation intake","Lawyer","criminal-defence|legal|mumbai"),
    ("contactus@dsklegal.com",          "DSK Legal",                 "White-collar crime defence","Lawyer","criminal-defence|white-collar|legal|mumbai"),
    ("contact@wadiaghandy.com",         "Wadia Ghandy & Co",         "Criminal & civil litigation","Lawyer","criminal-defence|legal|mumbai"),

    # ════════════════ MAHARASHTRA CRIMINAL-DEFENCE LAWYERS ════════════════
    # Pune
    ("advocateabhishekupadhye@gmail.com","Adv. Upadhye & Associates","Criminal & cyber law","Lawyer","criminal-defence|legal|pune"),
    ("info@anevagi.com",                "Abhay Nevagi & Associates", "Criminal litigation","Lawyer","criminal-defence|legal|pune"),
    ("info@vidyamlegal.com",            "Vidyam Legal",              "Criminal litigation","Lawyer","criminal-defence|legal|pune"),
    ("jurisarmor@gmail.com",            "Juris Armor Advocates",     "Criminal (NDPS, POCSO, cyber)","Lawyer","criminal-defence|legal|pune"),
    # Nagpur (Bombay HC Nagpur Bench)
    ("info@dewaniassociates.com",       "Dewani Associates",         "Criminal defence & appeals","Lawyer","criminal-defence|legal|nagpur"),
    ("adv.ashishfule@gmail.com",        "ARF Legal (Adv. Ashish Fule)","Criminal defence, bail/appeals","Lawyer","criminal-defence|legal|nagpur"),
    ("support@nagpuradvocates.com",     "Adv. Ashish Kumar Patel",   "Criminal litigation, HC Nagpur Bench","Lawyer","criminal-defence|legal|nagpur"),
    ("desailegal3@gmail.com",           "Desai Legal",               "Criminal law","Lawyer","criminal-defence|legal|nagpur"),
    ("ngp.hcbaoffice@gmail.com",        "High Court Bar Assoc Nagpur","Bar association, HC Nagpur Bench","Bar Body","bar-association|legal|nagpur"),
    ("info@dbanagpur.com",              "District Bar Assoc Nagpur",  "District bar association","Bar Body","bar-association|legal|nagpur"),
    # Aurangabad (Bombay HC Aurangabad Bench)
    ("office.advocategovindsharma@gmail.com","Adv. Govind M. Sharma","Criminal defence","Lawyer","criminal-defence|legal|aurangabad"),
    ("advsdkoli@gmail.com",             "Adv. Sujit D. Koli",        "Criminal defence, anticipatory bail","Lawyer","criminal-defence|legal|aurangabad"),
    ("info@advocatesanketkulkarni.com", "Adv. Sanket S. Kulkarni",   "Anticipatory bail & FIR quashing","Lawyer","criminal-defence|fir-quashing|legal|aurangabad"),
    # Thane / Navi Mumbai / Nashik
    ("info@tdcba.com",                  "Thane District Courts Bar Assoc","District court bar association","Bar Body","bar-association|legal|thane"),
    ("jaideepthakker@gmail.com",        "Thakker Chambers",          "Criminal defence (IPC/economic)","Lawyer","criminal-defence|legal|thane"),
    ("adv.indraraj@gmail.com",          "Adv. Indraraj Yadav",       "Bail, anticipatory bail, writs","Lawyer","criminal-defence|fir-quashing|legal|thane"),
    ("info@advrameshtripathi.com",      "Adv. Ramesh Tripathi & Assoc","Criminal litigation","Lawyer","criminal-defence|legal|navi-mumbai"),
    ("sarita.vikram6991@gmail.com",     "Adv. Sarita V. Singh",      "Criminal, bail","Lawyer","criminal-defence|legal|navi-mumbai"),
    ("advocatevikramsingh47@gmail.com", "Adv. Vikram Singh",         "Criminal defence","Lawyer","criminal-defence|legal|navi-mumbai"),
    # Other districts
    ("info@kdba.in",                    "Kolhapur District Bar Assoc","District bar association","Bar Body","bar-association|legal|kolhapur"),
    ("contact@mehtaadvocate.com",       "Mehta & Mehta Advocates",   "Criminal & civil litigation","Lawyer","criminal-defence|legal|kolhapur"),

    # ════════════════ BAR COUNCILS ════════════════
    ("barcouncilmahgoa@gmail.com",      "Bar Council of Maharashtra & Goa","State bar council","Bar Body","bar-council|legal|maharashtra"),
    ("bciinfo21@gmail.com",             "Bar Council of India",      "Apex bar council","Bar Body","bar-council|legal|national"),
    ("sensrimantosecy.bci@gmail.com",   "Bar Council of India",      "Secretary — grievances/complaints","Bar Body","bar-council|legal|national"),
    ("dcdepartment.bci@gmail.com",      "Bar Council of India",      "Disciplinary committee","Bar Body","bar-council|legal|national"),

    # ════════════════ STATUTORY LEGAL AID ════════════════
    ("mslsa-bhc@nic.in",                "Maharashtra State Legal Services Auth","Free legal aid (incl. criminal)","Legal Aid","legal-aid|legal|maharashtra|mumbai"),
    ("mumbai-dlsa.mh@bhc.gov.in",       "DLSA Mumbai City",          "District legal aid","Legal Aid","legal-aid|legal|mumbai"),
    ("mumbai-sub.dlsa@bhc.gov.in",      "DLSA Mumbai Suburban",      "District legal aid","Legal Aid","legal-aid|legal|mumbai"),
    ("pune-dlsa.mh@bhc.gov.in",         "DLSA Pune",                 "District legal aid","Legal Aid","legal-aid|legal|pune"),
    ("nagpur-dlsa.mh@bhc.gov.in",       "DLSA Nagpur",               "District legal aid","Legal Aid","legal-aid|legal|nagpur"),
    ("thane-dlsa.mh@bhc.gov.in",        "DLSA Thane",                "District legal aid","Legal Aid","legal-aid|legal|thane"),
    ("dlsa.aurangabad@gmail.com",       "DLSA Aurangabad",           "District legal aid","Legal Aid","legal-aid|legal|aurangabad"),
    ("dlsa-nashik@bhc.gov.in",          "DLSA Nashik",               "District legal aid","Legal Aid","legal-aid|legal|nashik"),
    ("nalsa-dla@nic.in",                "National Legal Services Auth","National legal aid","Legal Aid","legal-aid|legal|national"),

    # ════════════════ NATIONAL LEGAL PRESS ════════════════
    ("info@livelaw.in",                 "LiveLaw",                   "Legal/courts editorial desk","Press","legal-press|press|courts-beat|national"),
    ("columns@livelaw.in",              "LiveLaw",                   "Columns / article submissions","Press","legal-press|press|courts-beat|national"),
    ("manu@livelaw.in",                 "Manu Sebastian",            "Managing Editor, LiveLaw","Press","legal-press|press|courts-beat|influencer|national"),
    ("pallavi@barandbench.com",         "Pallavi Saluja",            "Editor, Bar & Bench","Press","legal-press|press|courts-beat|national"),
    ("murali@barandbench.com",          "Murali Krishnan",          "Editor Court News, Bar & Bench","Press","legal-press|press|courts-beat|national"),
    ("aditya@barandbench.com",          "Aditya AK",                 "Associate Editor, Bar & Bench","Press","legal-press|press|courts-beat|national"),
    ("debayan@barandbench.com",         "Debayan Roy",               "Special Correspondent, Bar & Bench","Press","legal-press|press|courts-beat|national"),
    ("editor@article-14.com",           "Article 14",                "Justice / wrongful-prosecution longform","Press","legal-press|press|wrongful-prosecution|investigative|national"),
    ("editorial@theleaflet.in",         "The Leaflet",               "Legal / civil-liberties editorial","Press","legal-press|press|civil-liberties|national"),
    ("blog@scconline.com",              "SCC Online Blog",           "Legal news submissions","Press","legal-press|press|national"),
    ("articles@scconline.com",          "SCC Online",                "Article submissions","Press","legal-press|press|national"),
    ("ombudsperson@thewire.in",         "The Wire",                  "Ombudsperson","Press","legal-press|press|investigative|national"),
    ("sv@thewire.in",                   "Siddharth Varadarajan",     "Founding Editor, The Wire","Press","legal-press|press|investigative|influencer|national"),
    ("livewire@thewire.in",             "The Wire (LiveWire)",       "Pitches / essays","Press","legal-press|press|national"),
    ("letters@scroll.in",               "Scroll.in",                 "Letters to the Editor","Press","legal-press|press|national"),
    ("readerseditor@scroll.in",         "Scroll.in",                 "Readers' Editor","Press","legal-press|press|national"),
    ("submissions@newslaundry.com",     "Newslaundry",               "Story submissions","Press","legal-press|press|investigative|national"),
    ("editor.thecaravan@delhipress.in", "The Caravan",               "Long-form / investigations","Press","legal-press|press|investigative|national"),
    ("admin@scobserver.in",             "Supreme Court Observer",    "Supreme Court coverage","Press","legal-press|press|courts-beat|national"),
    ("adv.areebuddin@gmail.com",        "Areeb Uddin Ahmed",         "Freelance legal journalist","Press","legal-press|press|courts-beat|freelance|national"),

    # ════════════════ MUMBAI/MAHARASHTRA CRIME & COURTS PRESS ════════════════
    ("secretary@mumbaipressclub.com",   "Mumbai Press Club",         "Press body — secretariat","Press","press|press-body|mumbai"),
    ("mail@fpj.co.in",                  "Free Press Journal",        "General editorial","Press","press|crime-beat|courts-beat|mumbai"),
    ("webeditor@fpj.co.in",             "Free Press Journal",        "Web editor","Press","press|mumbai"),
    ("rajeshs@fpj.co.in",               "Rajesh Sitaraman",          "FPJ Grievance Officer (right-of-reply)","Press","press|right-of-reply|mumbai"),
    ("editorial@lokmat.com",            "Lokmat",                    "Editorial desk (Marathi)","Press","press|crime-beat|marathi|mumbai|maharashtra"),
    ("editorial@lokmatnews.in",         "Lokmat Times",              "Editorial desk (English)","Press","press|crime-beat|mumbai|maharashtra"),
    ("editor.mumbai@esakal.com",        "Sakal Mumbai",              "Mumbai editorial (Marathi)","Press","press|crime-beat|marathi|mumbai"),
    ("parel@esakal.com",                "Sakal Mumbai",              "Parel city desk","Press","press|mumbai"),
    ("grievance@mid-day.com",           "Mid-Day",                   "Grievance Officer (right-of-reply)","Press","press|right-of-reply|mumbai"),

    # ════════════════ CIVIL-LIBERTIES / CRIMINAL-JUSTICE NGOs ════════════════
    ("puclnat@gmail.com",               "PUCL National",             "Civil liberties (national)","NGO/Civic","civil-liberties|criminal-justice|ngo-civic|national"),
    ("pucl.maharashtra@gmail.com",      "PUCL Maharashtra",          "Civil liberties (Mihir Desai / Lara Jesani)","NGO/Civic","civil-liberties|criminal-justice|ngo-civic|maharashtra|mumbai"),
    ("cjpindia@gmail.com",              "Citizens for Justice & Peace","Rights litigation (Mumbai)","NGO/Civic","civil-liberties|criminal-justice|ngo-civic|mumbai"),
    ("teestateesta@gmail.com",          "Teesta Setalvad",           "Secretary, CJP","NGO/Civic","civil-liberties|ngo-civic|activist|influencer|mumbai"),
    ("info@humanrightsinitiative.org",  "CHRI",                      "Police & prison reform","NGO/Civic","civil-liberties|police-accountability|ngo-civic|national"),
    ("p39a@nludelhi.ac.in",             "Project 39A",               "Criminal justice, wrongful conviction","NGO/Civic","criminal-justice|wrongful-prosecution|legal-academia|national"),
    ("contact@commoncause.in",          "Common Cause India",        "Police-reform PILs, accountability","NGO/Civic","civil-liberties|police-accountability|ngo-civic|national"),
    ("aidslaw@lawyerscollective.org",   "Lawyers Collective",        "Public-interest law (Mumbai)","NGO/Civic","civil-liberties|ngo-civic|legal|mumbai"),
    ("info@uncat.org",                  "Natl Campaign Against Torture","Custodial torture / accountability","NGO/Civic","civil-liberties|police-accountability|ngo-civic|national"),
    ("prayas@tiss.edu",                 "Prayas (TISS Mumbai)",      "Undertrials, custodial rights","NGO/Civic","criminal-justice|ngo-civic|mumbai"),
    ("cpapcommunication@gmail.com",     "CPA Project (Bhopal)",      "Police accountability, false FIRs","NGO/Civic","civil-liberties|police-accountability|wrongful-prosecution|ngo-civic|national"),
    ("reachout@clpr.org.in",            "Centre for Law & Policy Research","Access to justice","NGO/Civic","civil-liberties|criminal-justice|ngo-civic|national"),
    ("indiajusticereport@gmail.com",    "India Justice Report",      "Justice-system data (Tata Trusts)","NGO/Civic","criminal-justice|research|national"),
    ("communication@indiavisionfoundation.org.in","India Vision Foundation","Prison/police reform (Kiran Bedi)","NGO/Civic","police-accountability|criminal-justice|ngo-civic|national"),

    # ════════════════ HUMAN-RIGHTS COMMISSIONS (complaint channels) ════════════════
    ("cr.nhrc@nic.in",                  "NHRC",                      "Complaints — custodial/police excess","Government","police-accountability|human-rights|national"),
    ("complaint-mshrc@mah.gov.in",      "Maharashtra State HR Commission","HR violations within Maharashtra","Government","police-accountability|human-rights|maharashtra"),

    # ════════════════ LEGAL COMMENTATORS / ACADEMICS / INFLUENCERS ════════════════
    ("helpline.tli@gmail.com",          "Adv. Vivek Kumar Gaurav",   "'The Legal Indian' YouTube — rights explainers","Influencer","legal-commentator|influencer|youtuber|criminal-justice|national"),
    ("sidhantdhingra@advocatesidhantdhingra.com","Adv. Sidhant Dhingra","Criminal-defence advocate & explainer","Influencer","legal-commentator|criminal-defence|influencer|national"),
    ("namanmohnot@thelegalshots.com",   "Adv. Naman Mohnot",         "'Legal Shots' YouTube","Influencer","legal-commentator|influencer|youtuber|national"),
    ("sanyogvyaslawclasses@gmail.com",  "Adv. Sanyog Vyas",          "Law-explainer YouTube (Hindi)","Influencer","legal-commentator|influencer|youtuber|national"),
    ("anup.surendranath@nalsar.ac.in",  "Prof. Anup Surendranath",   "NALSAR / Square Circle Clinic (ex-P39A)","Academic","legal-academia|criminal-justice|wrongful-prosecution|influencer|national"),
    ("faisal@nujs.edu",                 "Faisal Fasih",              "NUJS Asst Prof — criminal law/CrPC","Academic","legal-academia|criminal-justice|national"),
    ("rangintripathy@nluo.ac.in",       "Prof. Rangin P. Tripathy",  "NLU Odisha — criminal law/civil liberties","Academic","legal-academia|criminal-justice|national"),
    ("p39ablog@nludelhi.ac.in",         "Project 39A Criminal Law Blog","Criminal-justice research","Academic","criminal-justice|wrongful-prosecution|legal-academia|national"),
    ("mishi@softwarefreedom.org",       "Mishi Choudhary",           "SFLC.in founder — civil liberties","Influencer","civil-liberties|legal-commentator|influencer|national"),
    ("prashant.mali@cyberlawconsulting.com","Adv. Dr. Prashant Mali","Cyber-law advocate (Bombay HC), columnist","Influencer","legal-commentator|criminal-defence|cyber-law|influencer|mumbai"),
    ("info@skochlaw.in",                "Abhinav Sekhri (SKOCH Law)","Criminal law — 'Proof of Guilt'","Influencer","legal-commentator|criminal-defence|criminal-justice|national"),
    ("info@dakshindia.org",             "DAKSH Society",             "Judicial-reform research & podcast","Influencer","criminal-justice|research|legal-commentator|national"),
    ("contact@amranaventures.com",      "'Know Your Kanoon' (Adv. Amber Rana)","Legal-awareness podcast","Influencer","legal-commentator|influencer|national"),
]

def load_csv(path):
    if path.exists():
        with open(path, encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    return []

final_rows = load_csv(FINAL)
supp_rows  = load_csv(SUPP)
existing   = {r["email"].lower().strip() for r in final_rows}
suppressed = {r["email"].lower().strip() for r in supp_rows}

added = dup = supp_skip = 0
new_rows = []

for (email, name, desig, cat, tags) in NEW_CONTACTS:
    el = email.strip().lower()
    if el in suppressed:
        supp_skip += 1
    elif el in existing:
        dup += 1
    else:
        existing.add(el)
        new_rows.append({
            "email": el, "name": name.strip(), "designation": desig.strip(),
            "category": cat.strip(), "tags": tags.strip().lower(),
            "case": CASE, "source": SOURCE, "mobile": "",
        })
        added += 1

if new_rows:
    with open(FINAL, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerows(new_rows)

print(f"False-case allies added: {added}")
print(f"Skipped (dup):           {dup}")
print(f"Skipped (suppressed):    {supp_skip}")
print(f"Total final:             {len(final_rows) + added}")
