"""
Goa Siolim inspection contacts — batch 1
Research date: 17 Jun 2026
Sources: official .gov.in / .nic.in pages, official org websites, published directories.
NO guessed emails. All sourced verbatim from official contact pages.
"""
import csv, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
FINAL   = ROOT / "contacts" / "contacts_final.csv"
SUPP    = ROOT / "contacts" / "suppression_list.csv"

# ── Contacts sourced from research agents ─────────────────────────────────────
NEW_CONTACTS = [

    # ── GOA PRESS ──────────────────────────────────────────────────────────────
    # Prudent Media (from prudentmedia.in/contact-us/)
    ("pramod@prudentmedia.in",      "Pramod Acharya",    "Editor",              "Press",               "goa-press|press|goa|tv|prudent-media"),
    ("suyash@prudentmedia.in",      "Suyash Gaunekar",   "News Editor",         "Press",               "goa-press|press|goa|tv|prudent-media"),
    ("rohit@prudentmedia.in",       "Rohit Vadkar",      "Associate Producer",  "Press",               "goa-press|press|goa|tv|prudent-media"),
    ("info@prudentmedia.in",        "Prudent Media",     "General Contact",     "Press",               "goa-press|press|goa|tv|prudent-media"),

    # Goa Chronicle (from goachronicle.com/contact-us/)
    ("editorial@goachronicle.com",  "Goa Chronicle",     "Editorial",           "Press",               "goa-press|press|goa|english-daily"),
    ("sales@goachronicle.com",      "Goa Chronicle",     "Sales",               "Press",               "goa-press|press|goa|english-daily"),
    ("india@goachronicle.com",      "Goa Chronicle",     "India Desk",          "Press",               "goa-press|press|goa|english-daily"),

    # The Goan (from thegoan.net/contact-us/)
    ("editor@thegoan.net",          "The Goan",          "Editor",              "Press",               "goa-press|press|goa|english-daily"),
    ("desk@thegoan.net",            "The Goan",          "News Desk",           "Press",               "goa-press|press|goa|english-daily"),
    ("advertising@thegoan.net",     "The Goan",          "Advertising",         "Press",               "goa-press|press|goa|english-daily"),

    # Navhind Times
    ("navhind@navhindtimes.com",    "Navhind Times",     "Editorial",           "Press",               "goa-press|press|goa|english-daily"),
    ("advt@navhindtimes.com",       "Navhind Times",     "Advertisement",       "Press",               "goa-press|press|goa|english-daily"),

    # Tarun Bharat Goa (from tarunbharat.com/contact-us/)
    ("Kiranthakur@tarunbharat.com", "Kiran B. Thakur",   "Editor",              "Press",               "goa-press|press|goa|marathi-daily"),
    ("news.goa@tarunbharat.com",    "Tarun Bharat Goa",  "News Desk",           "Press",               "goa-press|press|goa|marathi-daily"),

    # Lokmat Goa
    ("editorial@lokmatnews.in",     "Lokmat",            "Editorial",           "Press",               "goa-press|press|goa|marathi-daily"),

    # Goa365 TV
    ("goa365tv@gmail.com",          "Goa365 TV",         "News Contact",        "Press",               "goa-press|press|goa|tv|digital-creator|influencer"),

    # Gomantak Times
    ("bizhead.digital@apglobale.com","Gomantak Times",   "Digital Head",        "Press",               "goa-press|press|goa|marathi-daily"),

    # Goan Varta
    ("editor@goanvarta.net",        "Goan Varta",        "Editor",              "Press",               "goa-press|press|goa|marathi-daily"),
    ("marketing@goanvarta.net",     "Goan Varta",        "Marketing",           "Press",               "goa-press|press|goa|marathi-daily"),

    # Digital Goa
    ("niraj@digitalgoa.com",        "Niraj Naik",        "Editor",              "Press",               "goa-press|press|goa|digital-creator|social-active"),
    ("digitalgoanews@gmail.com",    "Digital Goa",       "News",                "Press",               "goa-press|press|goa|digital-creator"),

    # Goa News Hub
    ("hubgoanews@gmail.com",        "Goa News Hub",      "News Contact",        "Press",               "goa-press|press|goa|digital-creator|influencer"),
    ("marketing@goanewshub.com",    "Goa News Hub",      "Marketing",           "Press",               "goa-press|press|goa|digital-creator"),

    # Goemkarponn
    ("goemkarponnnews@gmail.com",   "Goemkarponn",       "News Contact",        "Press",               "goa-press|press|goa|digital-creator"),

    # Frederick Noronha — investigative journalist
    ("fredericknoronha1@gmail.com", "Frederick Noronha", "Freelance Journalist","Press",               "goa-press|press|goa|investigative|influencer|social-active"),

    # DIP Goa (Dept of Information and Publicity)
    ("dipgoa@gmail.com",            "DIP Goa",           "Dept of Information & Publicity", "Government", "govt-state|goa|press-office"),

    # Goa Union of Journalists
    ("secretary.goauj@gmail.com",   "Goa Union of Journalists", "Secretary",   "Press",               "goa-press|press|goa|press-club"),

    # Sanatan Prabhat Goa
    ("editor@sanatanprabhat.org",   "Sanatan Prabhat",   "Editor",              "Press",               "goa-press|press|goa|marathi-daily"),

    # Herald Goa
    ("editor@herald-goa.com",       "O Heraldo",         "Editor",              "Press",               "goa-press|press|goa|english-daily"),

    # O Heraldo alternate
    ("oheraldo@gmail.com",          "O Heraldo",         "General Contact",     "Press",               "goa-press|press|goa|english-daily"),

    # ── GOA GOVERNMENT ─────────────────────────────────────────────────────────
    # GSPCB (goaspcb.gov.in)
    ("mail.gspcb@gov.in",               "GSPCB",                      "General/Grievances",         "Government",          "govt-state|goa|environment|gspcb|north-goa"),
    ("chairman-gspcb.goa@nic.in",       "Dr Levinson J Martins IAS",  "Chairman GSPCB",             "Government",          "govt-state|goa|environment|gspcb|north-goa|top-priority"),
    ("ms-gspcb.goa@nic.in",             "Dr Geeta S Nagvenkar",       "Member Secretary GSPCB",     "Government",          "govt-state|goa|environment|gspcb|north-goa|top-priority"),
    ("see-gspcb@gov.in",                "Shri Sanjeev Joglekar",      "Sr Environmental Engineer",  "Government",          "govt-state|goa|environment|gspcb|north-goa"),

    # TCP (Town and Country Planning)
    ("ctp-tcp.goa@nic.in",              "TCP Goa",                    "Chief Town Planner",         "Government",          "govt-state|goa|land-use|tcp|north-goa"),

    # North Goa Collectorate
    ("coln.goa@nic.in",                 "North Goa Collector",        "District Collector",         "Government",          "govt-state|goa|north-goa|collector|top-priority"),
    ("mam-bardez.goa@nic.in",           "Shri Anant Malik",           "Mamlatdar Bardez",           "Government",          "govt-state|goa|north-goa|revenue|bardez|siolim"),
    ("mam-north.goa@nic.in",            "Smt Akshaya A Amonkar",      "Mamlatdar-in-Collectorate",  "Government",          "govt-state|goa|north-goa|revenue"),
    ("dycrev-north.goa@nic.in",         "North Goa Dy Collector",     "Dy Collector Revenue",       "Government",          "govt-state|goa|north-goa|revenue"),
    ("ddma-north.goa@gov.in",           "DDMA North Goa",             "Control Room DDMA",          "Government",          "govt-state|goa|north-goa|disaster-mgmt"),

    # Environment Dept
    ("dir-env.goa@nic.in",              "Johnson B Fernandes",        "Director Environment",       "Government",          "govt-state|goa|environment|north-goa"),

    # Forest Dept
    ("dcfnorth-forest.goa@nic.in",      "North Goa Forest Division",  "Dy Conservator Forests",     "Government",          "govt-state|goa|forest|north-goa"),
    ("dcfhq-forest.goa@nic.in",         "Goa Forest Dept HQ",         "Pr Chief Conservator",       "Government",          "govt-state|goa|forest"),

    # Panchayat Directorate
    ("dir-panc.goa@nic.in",             "Smt Siddhi Halarnkar",       "Director of Panchayats",     "Government",          "govt-state|goa|panchayat"),

    # Goa Secretariat / CM / Governor
    ("cs-goa@nic.in",                   "Shri Parimal Rai",           "Chief Secretary Goa",        "Government",          "govt-state|goa|secretariat|top-priority"),
    ("cm.goa@nic.in",                   "Dr Pramod Sawant",           "Chief Minister Goa",         "Government",          "govt-state|goa|cm|top-priority"),
    ("governor.goa@gov.in",             "Governor of Goa",            "Governor / Raj Bhavan",      "Government",          "govt-state|goa|governor"),

    # PWD Goa
    ("pce-pwd.goa@nic.in",              "Sandip K P Chodnekar",       "Principal Chief Engineer PWD","Government",         "govt-state|goa|pwd"),

    # North Goa MP
    ("naik.shripad@sansad.nic.in",      "Shripad Yesso Naik",         "MP North Goa (Lok Sabha)",   "Politician/MP",       "govt-state|goa|mp|north-goa|politician"),
    ("shripadnaik@gmail.com",           "Shripad Yesso Naik",         "MP North Goa (personal)",    "Politician/MP",       "govt-state|goa|mp|north-goa|politician"),

    # MLA contacts
    ("mla.calangute.gvs@gov.in",        "Michael Lobo",               "MLA Calangute BJP",          "Politician/MLA",      "govt-state|goa|mla|north-goa|politician"),
    ("vijaisardesai4fatorda@gmail.com",  "Vijai Sardesai",             "MLA Fatorda / Goa Forward",  "Politician/MLA",      "goa|mla|politician|regional-party"),
    ("mla.fatorda.gvs@gov.in",          "Vijai Sardesai",             "MLA Fatorda Official",       "Politician/MLA",      "govt-state|goa|mla|politician"),
    ("mla.tivim.gvs@gov.in",            "Tivim MLA Office",           "MLA Tivim",                  "Politician/MLA",      "govt-state|goa|mla|north-goa|politician"),
    ("mla.mapusa.gvs@gov.in",           "Mapusa MLA Office",          "MLA Mapusa",                 "Politician/MLA",      "govt-state|goa|mla|north-goa|politician"),
    ("mla.porvorim.gvs@gov.in",         "Porvorim MLA Office",        "MLA Porvorim",               "Politician/MLA",      "govt-state|goa|mla|north-goa|politician"),
    ("mla.mandrem.gvs@gov.in",          "Mandrem MLA Office",         "MLA Mandrem",                "Politician/MLA",      "govt-state|goa|mla|north-goa|politician"),
    ("mla.pernem.gvs@gov.in",           "Pernem MLA Office",          "MLA Pernem",                 "Politician/MLA",      "govt-state|goa|mla|north-goa|politician"),

    # Goa Planning
    ("dir-dpse.goa@nic.in",             "DPSE Goa",                   "Director Planning Statistics","Government",          "govt-state|goa"),

    # Goa High Court
    ("reg-high.goa@nic.in",             "High Court of Bombay at Goa","Registrar Administration",   "Court/Judiciary",     "goa|court|judiciary|court-high"),
    ("regjud-high.goa@gov.in",          "Irshad Agha",                "Registrar Judicial HC Goa",  "Court/Judiciary",     "goa|court|judiciary|court-high"),

    # Goa Human Rights Commission
    ("sect-ghrc.goa@nic.in",            "Biju Naik",                  "Secretary GHRC",             "Government",          "govt-state|goa|human-rights"),

    # Goa State Legal Services Authority
    ("ms-gslsa.goa@nic.in",             "GSLSA",                      "Member Secretary",           "Legal",               "goa|legal|access-to-justice"),

    # GCZMA (Coastal Zone)
    ("gczma.goa@nic.in",                "GCZMA",                      "Goa Coastal Zone Mgmt Auth", "Government",          "govt-state|goa|environment|coastal|north-goa"),

    # ── NGOs / CIVIC / LEGAL ────────────────────────────────────────────────────
    ("goafoundation@gmail.com",          "Goa Foundation / Claude Alvares","Director",              "NGO/Civic",           "goa|ngo-civic|activist|environment|influencer"),
    ("contact@arannya.in",               "Arannya AERO",               "Environment Research Org",   "NGO/Civic",           "goa|ngo-civic|activist|environment"),
    ("arannyaero@gmail.com",             "Arannya AERO",               "Environment Research (alt)",  "NGO/Civic",           "goa|ngo-civic|activist|environment"),
    ("ghcbap@gmail.com",                 "Goa HC Bar Association",     "Bar Association",            "Legal",               "goa|legal|bar-association"),
    ("barcouncilmahgoa@gmail.com",       "Bar Council Mah & Goa",      "Bar Council",                "Legal",               "goa|legal|bar-council"),
    ("bjpgoa10@gmail.com",               "BJP Goa",                    "State Office",               "Politician",          "goa|political|bjp"),
    ("info@aamaadmiparty.org",           "AAP (Goa Unit)",             "State Office Panaji",        "Politician",          "goa|political|aap"),
    ("office@goaforward.in",             "Goa Forward Party",          "Party Office",               "Politician",          "goa|political|regional-party"),
    ("cjpindia@gmail.com",               "Citizens for Justice & Peace","National (covers Goa)",     "NGO/Civic",           "goa|ngo-civic|human-rights|activist"),
    ("fredericknoronha2@gmail.com",      "Frederick Noronha",          "Journalist/Publisher (alt)", "Press",               "goa-press|press|goa|investigative|influencer"),
]

CASE   = "olympio-almeida"
SOURCE = "expand_goa_siolim_17jun2026"

# ── Load existing data ────────────────────────────────────────────────────────
def load_csv(path):
    rows = []
    if path.exists():
        with open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    return rows

final_rows = load_csv(FINAL)
supp_rows  = load_csv(SUPP)

existing_emails = {r["email"].lower().strip() for r in final_rows}
suppressed      = {r["email"].lower().strip() for r in supp_rows}

# ── Fieldnames ────────────────────────────────────────────────────────────────
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]

def make_row(email, name, desig, cat, tags):
    return {
        "email":       email.strip().lower(),
        "name":        name.strip(),
        "designation": desig.strip(),
        "category":    cat.strip(),
        "tags":        tags.strip().lower(),
        "case":        CASE,
        "source":      SOURCE,
        "mobile":      "",
    }

added = skipped_dup = skipped_supp = 0
new_rows = []

for (email, name, desig, cat, tags) in NEW_CONTACTS:
    el = email.strip().lower()
    if el in suppressed:
        skipped_supp += 1
    elif el in existing_emails:
        skipped_dup += 1
    else:
        existing_emails.add(el)
        new_rows.append(make_row(email, name, desig, cat, tags))
        added += 1

# ── Append to contacts_final.csv ─────────────────────────────────────────────
if new_rows:
    write_header = not FINAL.exists()
    with open(FINAL, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            w.writeheader()
        w.writerows(new_rows)

print(f"Added:          {added}")
print(f"Skipped (dup):  {skipped_dup}")
print(f"Skipped (supp): {skipped_supp}")
print(f"Total final:    {len(final_rows) + added}")
print()
print("New contacts added:")
for r in new_rows:
    print(f"  {r['email']:50s} {r['tags'][:50]}")
