"""
False-case / wrongful-prosecution allies — batch 2 (Mumbai + national)
Research date: 21 Jun 2026 (6 parallel agents, STRICT verified-only: every email
seen on a live source page; no pattern-guessed addresses -- deliverability is
critical after the bounce cleanup).

Net-new focus the existing list was thin on: the literal "fake case" niche
(498A / false-FIR / men's-rights orgs), Marathi Mumbai crime desks, legal
YouTubers/influencers, fact-checkers, more Mumbai criminal-defence lawyers,
criminal-justice academics & justice NGOs.
"""
import csv
from pathlib import Path

ROOT   = Path(__file__).parent.parent
FINAL  = ROOT / "contacts" / "contacts_final.csv"
SUPP   = ROOT / "contacts" / "suppression_list.csv"
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]
CASE   = "tarun-thadani"
SOURCE = "falsecase_allies_batch2_21jun2026"

NEW_CONTACTS = [

    # ── 498A / FALSE-CASE / MEN'S-RIGHTS ORGS (the literal "fake case" niche) ──
    ("info@daaman.org",                 "Daaman Welfare Society",    "Men's rights / false-498A support","NGO/Civic","false-fir|498a|mens-rights|wrongful-prosecution|ngo-civic|national"),
    ("menwelfaretrust@gmail.com",       "Men Welfare Trust (SIF)",   "498A-misuse helpline / counselling","NGO/Civic","false-fir|498a|mens-rights|wrongful-prosecution|ngo-civic|national"),
    ("menhelpline.official@gmail.com",  "Men Helpline Org",          "Men falsely accused 498A/DV — helpline","NGO/Civic","false-fir|498a|mens-rights|wrongful-prosecution|ngo-civic|national"),

    # ── MARATHI / REGIONAL MUMBAI CRIME & COURT DESKS ──
    ("write2us@saamana.com",            "Saamana",                   "Editorial desk (Shiv Sena daily)","Press","press|crime-beat|marathi|mumbai|maharashtra"),
    ("mumbaiadvt@pudhari.co.in",        "Pudhari",                   "Mumbai (Kalbadevi) office","Press","press|marathi|mumbai|maharashtra"),
    ("news.kop@pudhari.co.in",          "Pudhari",                   "News desk","Press","press|crime-beat|marathi|maharashtra"),
    ("news@navakal.in",                 "Navakal",                   "News/editorial desk (Mumbai Marathi)","Press","press|crime-beat|marathi|mumbai"),
    ("contact@sakalmediagroup.com",     "Sakal Media Group",         "Group editorial contact","Press","press|crime-beat|marathi|maharashtra"),
    ("admin@mahamtb.com",               "Mumbai Tarun Bharat",       "Office / editorial inbox","Press","press|crime-beat|marathi|mumbai"),
    ("contact@mymahanagar.com",         "Aapla Mahanagar",           "General / web desk (Mumbai)","Press","press|crime-beat|marathi|mumbai"),
    ("mymahanagarweb@gmail.com",        "Aapla Mahanagar",           "Web desk","Press","press|marathi|mumbai"),
    ("mahanagar91@gmail.com",           "Aapla Mahanagar",           "Editorial","Press","press|marathi|mumbai"),
    ("ibnl.feedback@news18.com",        "News18 Lokmat",             "News feedback desk","Press","press|crime-beat|marathi|mumbai|maharashtra"),
    ("feedback@marathi.news18.com",     "News18 Marathi",            "Marathi-edition feedback","Press","press|crime-beat|marathi|maharashtra"),
    ("mmps.president@gmail.com",         "Mumbai Marathi Patrakar Sangh","Journalist union (official)","Press","press|press-body|marathi|mumbai"),

    # ── MUMBAI LEGAL INFLUENCERS / ADVOCATE-CREATORS ──
    ("adv.vikasdongre@gmail.com",       "Adv. Vikas Dongre",         "Criminal/bail advocate + creator (Mumbai)","Influencer","legal-commentator|criminal-defence|fir-quashing|influencer|mumbai"),
    ("contact@advocateakshayshah.com",  "Adv. Akshay Shah",          "Criminal — bail/FIR/498A + creator (Mumbai)","Influencer","legal-commentator|criminal-defence|498a|influencer|mumbai"),
    ("info@shoneekapoor.com",           "Shonee Kapoor",             "Men's rights / 498A-misuse creator","Influencer","legal-commentator|498a|mens-rights|wrongful-prosecution|influencer|national"),
    ("advocate.kapilc@gmail.com",       "Adv. Kapil Chandna",        "Bail / FIR quashing + creator","Influencer","legal-commentator|criminal-defence|fir-quashing|influencer|national"),
    ("info@marathikayda.org",           "Marathi Kayda",             "Marathi legal-awareness creator","Influencer","legal-commentator|influencer|youtuber|marathi|maharashtra"),
    ("marathikayda@gmail.com",          "Marathi Kayda",             "Marathi legal-awareness (alt)","Influencer","legal-commentator|influencer|youtuber|marathi|maharashtra"),
    ("enquire@lawchakra.in",            "LawChakra",                 "Legal news/explainer — FIR/498A","Press","legal-press|legal-commentator|criminal-justice|national"),

    # ── MUMBAI CRIMINAL-DEFENCE LAWYERS / 498A DEFENCE (net-new) ──
    ("info@kamalandcoadvocates.com",    "Kamal & Co. Advocates",     "FIR quashing, 498A, anticipatory bail","Lawyer","criminal-defence|fir-quashing|498a|legal|mumbai"),
    ("mum@fariaandco.com",              "Faria & Co.",               "Bail, criminal complaints, 498A (Fort)","Lawyer","criminal-defence|498a|legal|mumbai"),
    ("info@shreeyanshlegal.com",        "Shreeyansh Legal",          "498A, criminal defence","Lawyer","criminal-defence|498a|legal|mumbai"),
    ("advjanakchitre@gmail.com",        "Adv. Janak Chitre",         "Bail, FIR quashing (Vasai-Virar/Thane)","Lawyer","criminal-defence|fir-quashing|legal|thane|mumbai"),
    ("advdharmendraassociates@gmail.com","Adv. Dharmendra Chawla",   "Criminal, NDPS, 498A/DV (Chembur)","Lawyer","criminal-defence|498a|legal|mumbai"),
    ("trshetty@yahoo.co.in",            "Tripti Shetty & Associates","Bail, POCSO, economic offences (Goregaon)","Lawyer","criminal-defence|legal|mumbai"),
    ("info@advocaterahulshelke.com",    "Adv. Rahul Shelke",         "Criminal trials, bail, DV (Thane W)","Lawyer","criminal-defence|legal|thane"),
    ("info@highcourtlawyer.com",        "Adv. Rohan Yemul",          "498A & DV defence (Mumbai)","Lawyer","criminal-defence|498a|legal|mumbai"),
    ("advsandeepdongre@gmail.com",      "Adv. Sandeep Dongre",       "Dowry/498A litigation, DV defence (Thane)","Lawyer","criminal-defence|498a|legal|thane"),
    ("honsec@bombaybar.com",            "Bombay Bar Association",    "Hon. Secretary",                 "Bar Body","bar-association|legal|mumbai"),
    ("info.at.bils@gmail.com",          "Bombay Incorporated Law Society","Law society (Fort)",        "Bar Body","bar-association|legal|mumbai"),
    ("hclsc-mum.mh@bhc.gov.in",         "HC Legal Services Committee Bombay","Pro bono / legal aid (HC)","Legal Aid","legal-aid|legal|mumbai"),
    ("legalaidcommittee.glc@gmail.com", "Govt Law College Mumbai — Legal Aid","Pro bono / legal-aid clinic","Legal Aid","legal-aid|legal|mumbai"),
    ("majlislaw@majlislaw.com",         "Majlis Legal Centre",       "DV / women's legal aid (Mumbai)","NGO/Civic","civil-liberties|legal|ngo-civic|mumbai"),

    # ── FACT-CHECKERS / INVESTIGATIVE (fabricated-allegation beat) ──
    ("claims@boomlive.in",              "BOOM Live",                 "Claims/tip desk (Mumbai HQ)","Press","fact-checker|press|investigative|wrongful-prosecution|mumbai"),
    ("assist@boomlive.in",              "BOOM Live",                 "Corrections / editorial","Press","fact-checker|press|investigative|mumbai"),
    ("contact@altnews.in",              "Alt News",                  "General / tips","Press","fact-checker|press|investigative|wrongful-prosecution|national"),
    ("complaints@altnews.in",           "Alt News",                  "Complaints / corrections","Press","fact-checker|press|investigative|national"),
    ("webqoof@thequint.com",            "The Quint — WebQoof",       "Fact-check / false-narrative desk","Press","fact-checker|press|investigative|national"),
    ("hi@factly.in",                    "Factly",                    "Data journalism + fact-checking","Press","fact-checker|press|investigative|national"),
    ("checkthis@newschecker.in",        "Newschecker",               "Fact-check tip desk","Press","fact-checker|press|investigative|national"),
    ("respond@factchecker.in",          "FactChecker.in",            "Fact-check; reader tips (Mumbai)","Press","fact-checker|press|investigative|mumbai"),
    ("edit@reporters-collective.in",    "The Reporters' Collective", "Accountability investigations","Press","legal-press|press|investigative|national"),
    ("respond@indiaspend.org",          "IndiaSpend",                "Data journalism (Mumbai)","Press","press|investigative|mumbai"),
    ("grievance@indiaspend.org",        "IndiaSpend",                "Grievance Officer (right-of-reply)","Press","press|right-of-reply|investigative|mumbai"),

    # ── CRIMINAL-JUSTICE ACADEMICS / SCHOLARS ──
    ("kavita.singh@nujs.edu",           "Prof. Kavita Singh",        "NUJS — Centre for Criminal Law & Victimology","Academic","legal-academia|criminal-justice|wrongful-prosecution|national"),
    ("renjith@nlujodhpur.ac.in",        "Dr. Renjith Thomas",        "NLU Jodhpur — Criminal Law & Forensic Justice","Academic","legal-academia|criminal-justice|national"),
    ("mmirdha@nlujodhpur.ac.in",        "Dr. Manisha Mirdha",        "NLU Jodhpur — Criminology","Academic","legal-academia|criminal-justice|national"),
    ("marisport@gnlu.ac.in",            "Dr. Marisport A.",          "GNLU — Criminology & Victimology","Academic","legal-academia|criminal-justice|national"),
    ("asapre@gnlu.ac.in",               "Dr. Abhilash Sapre",        "GNLU — Prisoners' rights","Academic","legal-academia|criminal-justice|wrongful-prosecution|national"),
    ("abindal@jgu.edu.in",              "Prof. Amit Bindal",         "JGLS — Penology & Criminal Justice","Academic","legal-academia|criminal-justice|national"),

    # ── SENIOR ADVOCATES / EX-IPS / JUSTICE NGOs ──
    ("abhasinghlawoffices@gmail.com",   "Abha Singh",                "Advocate Bombay HC — false cases, misconduct","Influencer","legal-commentator|criminal-defence|wrongful-prosecution|influencer|mumbai"),
    ("contact@hrln.org",                "HRLN (Colin Gonsalves)",    "Human Rights Law Network — custodial/PIL","NGO/Civic","civil-liberties|criminal-justice|wrongful-prosecution|ngo-civic|national"),
    ("pune@hrln.org",                   "HRLN Pune",                 "Human Rights Law Network — Pune desk","NGO/Civic","civil-liberties|criminal-justice|ngo-civic|maharashtra"),
    ("nagpur@hrln.org",                 "HRLN Nagpur",               "Human Rights Law Network — Nagpur desk","NGO/Civic","civil-liberties|criminal-justice|ngo-civic|maharashtra"),
    ("info@natstratindia.org",          "N. Ramachandran (ex-DGP)",  "Indian Police Foundation — police reform","NGO/Civic","police-accountability|criminal-justice|ngo-civic|national"),
    ("cedeyourcapital@gmail.com",       "CEDE",                      "Senior criminal-defence advocates network","NGO/Civic","criminal-defence|criminal-justice|ngo-civic|national"),
    ("admin@ibjindia.org",              "International Bridges to Justice India","Right to defence / fair trial","NGO/Civic","civil-liberties|criminal-justice|wrongful-prosecution|ngo-civic|national"),
    ("contact@hrf.net.in",              "HRAF Custodial Justice",    "Custodial torture / police reform","NGO/Civic","police-accountability|criminal-justice|ngo-civic|national"),
    ("office@humanrightscouncil.in",    "AICHLS Human Rights Council","Wrongful custody / false-accusation defence","NGO/Civic","civil-liberties|wrongful-prosecution|ngo-civic|national"),
    ("communications@i-probono.com",    "iProbono India",            "Pro bono legal network","NGO/Civic","civil-liberties|criminal-justice|ngo-civic|national"),

    # ── LEGAL PODCASTS / EXPLAINERS / NEWSLETTERS ──
    ("contactus@thedailylawyer.in",     "The Daily Lawyer Podcast",  "Court rulings, white-collar crime","Influencer","legal-commentator|criminal-justice|influencer|national"),
    ("anshuman@thelawblog.in",          "The Law Blog",              "Law & society — criminal law commentary","Influencer","legal-commentator|criminal-justice|national"),
    ("info@lawstreet.media",            "LawStreet Journal",         "Court news incl. crime & law-enforcement","Press","legal-press|press|criminal-justice|national"),
    ("contact@nyaaya.in",               "Nyaaya",                    "Plain-language rights (arrest/FIR/bail)","NGO/Civic","legal-commentator|criminal-justice|ngo-civic|national"),
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
        new_rows.append({"email": el, "name": name.strip(), "designation": desig.strip(),
                         "category": cat.strip(), "tags": tags.strip().lower(),
                         "case": CASE, "source": SOURCE, "mobile": ""})
        added += 1

if new_rows:
    with open(FINAL, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerows(new_rows)

print(f"Batch 2 added:  {added}")
print(f"Skipped (dup):  {dup}")
print(f"Skipped (supp): {supp_skip}")
print(f"Total final:    {len(final_rows) + added}")
