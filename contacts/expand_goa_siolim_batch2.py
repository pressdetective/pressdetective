"""
Goa Siolim inspection contacts — batch 2
Research date: 17 Jun 2026
All emails sourced from official .gov.in / .nic.in pages, official org websites,
or verified public directories. No guesses.
"""
import csv
from pathlib import Path

ROOT   = Path(__file__).parent.parent
FINAL  = ROOT / "contacts" / "contacts_final.csv"
SUPP   = ROOT / "contacts" / "suppression_list.csv"
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]
CASE   = "olympio-almeida"
SOURCE = "expand_goa_siolim_batch2_17jun2026"

NEW_CONTACTS = [

    # ── O HERALDO (herald-goa.com domain, confirmed multiple public dirs) ──────
    ("advt@herald-goa.com",          "O Heraldo",               "Advertisement",             "Press",            "goa-press|press|goa|english-daily"),
    ("mail@herald-goa.com",          "O Heraldo",               "General Queries",           "Press",            "goa-press|press|goa|english-daily"),
    ("desk@herald-goa.com",          "O Heraldo",               "Desk",                      "Press",            "goa-press|press|goa|english-daily"),
    ("online@herald-goa.com",        "O Heraldo",               "Online/Digital",            "Press",            "goa-press|press|goa|english-daily"),
    ("circulation@herald-goa.com",   "O Heraldo",               "Circulation",               "Press",            "goa-press|press|goa|english-daily"),

    # ── NAVHIND TIMES ─────────────────────────────────────────────────────────
    ("navhind@navhindtimes.in",      "Navhind Times",           "Editorial",                 "Press",            "goa-press|press|goa|english-daily"),
    ("navhind@gmail.com",            "Navhind Times",           "General/Online",            "Press",            "goa-press|press|goa|english-daily"),

    # ── DAINIK GOMANTAK (esakal.com page confirmed) ───────────────────────────
    ("info@dainikgomantak.com",      "Dainik Gomantak",         "Editorial",                 "Press",            "goa-press|press|goa|marathi-daily"),
    ("gomantak2014@gmail.com",       "Dainik Gomantak",         "General Contact",           "Press",            "goa-press|press|goa|marathi-daily"),
    ("gomantak.advt@gmail.com",      "Dainik Gomantak",         "Advertisement",             "Press",            "goa-press|press|goa|marathi-daily"),

    # ── GOA CHRONICLE extra ───────────────────────────────────────────────────
    ("info@goachronicle.com",        "Goa Chronicle",           "General Contact",           "Press",            "goa-press|press|goa|english-daily"),
    ("news@goachronicle.com",        "Goa Chronicle",           "News Desk",                 "Press",            "goa-press|press|goa|english-daily"),

    # ── GOAN VARTA extra ──────────────────────────────────────────────────────
    ("news@goanvarta.net",           "Goan Varta",              "News Desk",                 "Press",            "goa-press|press|goa|marathi-daily"),
    ("news.varta@thegoan.net",       "Goan Varta (The Goan)",   "News Desk",                 "Press",            "goa-press|press|goa|marathi-daily"),

    # ── PRUDENT MEDIA extra ───────────────────────────────────────────────────
    ("marketing@prudentmedia.in",    "Prudent Media",           "Marketing",                 "Press",            "goa-press|press|goa|tv"),

    # ── RDX GOA TV (confirmed contact page) ───────────────────────────────────
    ("rdxgoa@gmail.com",             "RDXGOA / Darshan Lolienkar", "Editor (since 2011)",    "Press",            "goa-press|press|goa|tv|digital-creator|influencer"),

    # ── AIR GOA (confirmed newsonair.gov.in) ──────────────────────────────────
    ("airpanaji@gmail.com",          "All India Radio Panaji",  "Head of Office",            "Press",            "goa-press|press|goa|radio"),
    ("rnuairpanaji@gmail.com",       "All India Radio Panaji",  "Regional News Unit",        "Press",            "goa-press|press|goa|radio"),

    # ── DIGITAL PORTALS ───────────────────────────────────────────────────────
    ("truegoanews@gmail.com",        "The True Goa News",       "YouTube news channel",      "Press",            "goa-press|press|goa|youtuber|digital-creator|social-active"),
    ("goanlines@rediffmail.com",     "Goan Reporter",           "Editor",                    "Press",            "goa-press|press|goa|digital-creator"),
    ("goanewslink@gmail.com",        "Goa News Link",           "General Contact",           "Press",            "goa-press|press|goa|digital-creator"),
    ("news@goanews.com",             "GoaNews.com",             "News Desk",                 "Press",            "goa-press|press|goa|digital-creator|investigative"),
    ("goanews@goanews.com",          "GoaNews.com",             "Editorial",                 "Press",            "goa-press|press|goa|digital-creator|investigative"),

    # ── INDIVIDUAL JOURNALISTS (confirmed public profiles) ────────────────────
    ("sandeshprabhudesai@gmail.com", "Sandesh Prabhudesai",     "Editor GoaNews.com",        "Press",            "goa-press|press|goa|investigative|influencer|social-active"),
    ("fn@goa-india.org",             "Frederick Noronha",       "Journalist/Publisher (alt)","Press",            "goa-press|press|goa|investigative|influencer"),
    ("goa1556books@gmail.com",       "Frederick Noronha",       "Publisher Goa 1556",        "Press",            "goa-press|press|goa|investigative"),
    ("nkamat@unigoa.ac.in",          "Nandkumar Kamat",         "Science Columnist / Goa Uni","Press",           "goa-press|press|goa|investigative|environment"),
    ("itsallwrite@outlook.in",       "Joanna Lobo",             "Freelance Journalist",      "Press",            "goa-press|press|goa|influencer|social-active"),

    # ── GOA FOUNDATION extra ──────────────────────────────────────────────────
    ("gflegalclinic@gmail.com",      "Goa Foundation Legal Aid","Legal Aid / PIL",           "NGO/Civic",        "goa|ngo-civic|activist|environment|legal"),

    # ── GOA POLICE (from citizen.goapolice.gov.in) ────────────────────────────
    ("spn-pol.goa@nic.in",           "Akshat Kaushal IPS",      "SP North Goa",              "Police/Government","police-hq|goa|north-goa|top-priority"),
    ("digpgoa@goapolice.gov.in",     "DIG Crime & Range",       "DIG Police Goa",            "Police/Government","police-hq|goa"),
    ("spcb-pol.goa@nic.in",          "SP Crime Branch",         "Superintendent Crime Branch","Police/Government","police-hq|goa|crime-branch"),
    ("spcyber@goapolice.gov.in",     "SP Cyber Crime Goa",      "Superintendent Cyber Crime","Police/Government","police-hq|goa|cyber-crime"),
    ("sphq@goapolice.gov.in",        "SP Headquarters",         "Superintendent HQ",         "Police/Government","police-hq|goa"),
    ("menezesbraz@yahoo.com",        "Braz T Menezes",          "Superintendent Police (GPS)","Police/Government","police-hq|goa"),
    ("dysptraffichq@gmail.com",      "DySP Traffic HQ Goa",     "DySP Traffic",              "Police/Government","police-hq|goa"),
    ("crospcr@gmail.com",            "Crime Records Office",    "SP Crime Records",          "Police/Government","police-hq|goa"),
    ("frrogoa@nic.in",               "FRRO Goa",                "Foreigners Reg Office",     "Police/Government","police-hq|goa"),

    # ── NORTH GOA COLLECTORATE extra ─────────────────────────────────────────
    ("ac1-north.goa@nic.in",         "Gurudas S T Dessai",      "Additional Collector I North Goa","Government","govt-state|goa|north-goa|collector"),
    ("ac2-north.goa@nic.in",         "Pravin Hire Parab",       "Additional Collector II North Goa","Government","govt-state|goa|north-goa|collector"),
    ("ac3-north.goa@nic.in",         "Pundalik Khorjuvenkar",   "Additional Collector III North Goa","Government","govt-state|goa|north-goa|collector"),

    # ── BDO BARDEZ (covers Siolim) ────────────────────────────────────────────
    ("bdo-bardez.goa@nic.in",        "Prathamesh Anil Shankardas","BDO Bardez (NIC)",        "Government",       "govt-state|goa|north-goa|bardez|siolim|bdo|top-priority"),
    ("bdobardez@gmail.com",          "BDO Bardez",              "Block Dev Officer Bardez",  "Government",       "govt-state|goa|north-goa|bardez|siolim|bdo|top-priority"),

    # ── NGPDA / TCP / COASTAL ────────────────────────────────────────────────
    ("membersecretaryngpda@gmail.com","K Ashok Kumar",           "Member Secretary NGPDA",   "Government",       "govt-state|goa|north-goa|land-use|top-priority"),
    ("goacoastalzone@gmail.com",      "GCZMA",                  "CRZ Violations Complaints", "Government",       "govt-state|goa|north-goa|environment|coastal"),

    # ── PANAJI CIVIC ─────────────────────────────────────────────────────────
    ("office@imaginepanaji.com",     "Imagine Panaji Smart City","General Queries IPSCDL",   "Government",       "govt-state|goa|north-goa"),
    ("office@ccpgoa.com",            "CCP Panaji",              "Corporation of City of Panaji","Government",    "govt-state|goa|north-goa"),
    ("commissioner@ccpgoa.com",      "Clen Madeira",            "Commissioner CCP Panaji",   "Government",       "govt-state|goa|north-goa"),

    # ── GTDC (confirmed goa-tourism.com) ──────────────────────────────────────
    ("reservations@goa-tourism.com", "GTDC",                    "Reservations",              "Government",       "govt-state|goa"),
    ("chairman@goa-tourism.com",     "Kedar J Naik MLA",        "Chairman GTDC",             "Government",       "govt-state|goa|mla|politician"),
    ("md@goa-tourism.com",           "Kuldeep Arolkar",         "Managing Director GTDC",    "Government",       "govt-state|goa"),
    ("sachingore@goa-tourism.com",   "Sachin A Gore",           "GM Engineering GTDC",       "Government",       "govt-state|goa"),
    ("gavindias@goa-tourism.com",    "Gavin Dias",              "GM Marketing GTDC",         "Government",       "govt-state|goa"),
    ("laxmikant@goa-tourism.com",    "Laxmikant Vaigankar",     "GM IT GTDC",                "Government",       "govt-state|goa"),
    ("kapil@goa-tourism.com",        "Kapil Painguinkar",       "GM Finance GTDC",           "Government",       "govt-state|goa"),
    ("deepak@goa-tourism.com",       "Deepak Narvekar",         "DGM Marketing GTDC",        "Government",       "govt-state|goa"),
    ("kundan@goa-tourism.com",       "Kundan Naik",             "DGM Finance GTDC",          "Government",       "govt-state|goa"),
    ("pritesh@goa-tourism.com",      "Pritesh Palyekar",        "Sr Manager IT GTDC",        "Government",       "govt-state|goa"),
    ("itmanagergtdc@gmail.com",      "GTDC IT Manager",         "IT Manager GTDC",           "Government",       "govt-state|goa"),

    # ── GIDC (confirmed iGOOD directory) ─────────────────────────────────────
    ("goa-idc@goa.gov.in",           "GIDC",                    "Industrial Dev Corp Goa",   "Government",       "govt-state|goa"),
    ("goaidc1965@gmail.com",         "GIDC",                    "Industrial Dev Corp (alt)",  "Government",       "govt-state|goa"),
    ("ithelpdesk-gidc@goa.gov.in",   "GIDC IT Helpdesk",        "IT Helpdesk GIDC",          "Government",       "govt-state|goa"),

    # ── OTHER GOA DEPTS ───────────────────────────────────────────────────────
    ("dir-heal.goa@nic.in",          "Director Health Services", "Directorate of Health Goa", "Government",      "govt-state|goa"),
    ("cee-elec.goa@nic.in",          "Dipak Bhajekar",          "Chief Electrical Engineer",  "Government",      "govt-state|goa"),
    ("ed.tsag-goa@gov.in",           "Dr Geeta S Nagvenkar",    "Executive Director Sports Auth Goa","Government","govt-state|goa"),

    # ── MLA Saligao ───────────────────────────────────────────────────────────
    ("kedarnaikoffice@gmail.com",    "Kedar Naik",              "MLA Saligao North Goa",     "Politician/MLA",   "goa|mla|north-goa|politician"),

    # ── PANCHAYAT ─────────────────────────────────────────────────────────────
    ("villagepanchayatcalangute@gmail.com","VP Calangute",       "Village Panchayat",         "Government",       "govt-state|goa|north-goa|bardez|panchayat"),
    ("info@calangutepanchayat.com",  "VP Calangute",            "Village Panchayat",         "Government",       "govt-state|goa|north-goa|bardez|panchayat"),
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

print(f"Batch 2 added:  {added}")
print(f"Skipped (dup):  {dup}")
print(f"Skipped (supp): {supp_skip}")
print(f"Total final:    {len(final_rows) + added}")
