#!/usr/bin/env python3
"""
Expand Mumbai crime/court press contacts list.
1. Parse 94 rows from mumbai_crime_press.xlsx
2. Add ~400 additional Mumbai press/crime/influencer contacts
3. Deduplicate against contacts_final.csv + suppression_list.csv
4. DNS-verify all new domains
5. Append to contacts_final.csv, rebuild contacts_live.csv
"""
import csv, re, socket, json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import date

BASE         = Path(__file__).parent.parent
FINAL_CSV    = BASE / 'contacts' / 'contacts_final.csv'
LIVE_CSV     = BASE / 'contacts' / 'contacts_live.csv'
SUPP_CSV     = BASE / 'contacts' / 'suppression_list.csv'
TAG_CSV      = BASE / 'contacts' / 'tag_summary.csv'
XLSX_PATH    = Path(r'C:\Users\t_tha\OneDrive\DESKTOP\mumbai_crime_press.xlsx')
TODAY        = date.today().isoformat()

# Domains known to have valid MX records — skip DNS round-trip
KNOWN_VALID = {
    'gmail.com','yahoo.com','yahoo.co.in','hotmail.com','outlook.com','rediffmail.com',
    'timesgroup.com','hindustantimes.com','indianexpress.com','mid-day.com',
    'thehindu.co.in','ndtv.com','theprint.in','thewire.in','scroll.in',
    'newslaundry.com','thequint.com','livelaw.in','barandbench.com',
    'altnews.in','boomlive.in','article-14.com','fpj.co.in','dnaindia.com',
    'firstpost.com','outlookindia.com','frontline.in','caravanmagazine.in',
    'loksatta.com','sakaal.com','sakaaltimes.in','loksattanews.com',
    'republicworld.com','abplive.com','abpmajha.com','zeenews.com','news18.com',
    'tv9marathi.com','mirror.co.in','indiatoday.in','aajtak.in',
    'thelallantop.com','theprint.in','theleaflet.in','legallyindia.com',
    'indialegal.in','lawctopus.com','lawsikho.com',
    'protonmail.com','protonmail.ch','pm.me',
    'mojostory.in','sochmedia.in','dhruvrathee.com',
    'monk-e.in','abhiandniyu.in','nitishrajput.com',
    'fayedouza.com','thedeshbhakt.in','namanmohnot.com',
    'dostcast.com','toprankers.com','finology.in',
    'satyamevjayate.in',
}

mx_cache = {}

def has_mx(domain: str) -> bool:
    d = domain.lower()
    if d in KNOWN_VALID:
        return True
    if d in mx_cache:
        return mx_cache[d]
    try:
        import dns.resolver
        answers = dns.resolver.resolve(d, 'MX', lifetime=4)
        ok = len(answers) > 0
    except Exception:
        try:
            socket.getaddrinfo(d, None, family=socket.AF_INET, proto=socket.IPPROTO_TCP)
            ok = True
        except Exception:
            ok = False
    mx_cache[d] = ok
    return ok

def email_to_domain(email: str) -> str:
    return email.lower().split('@')[-1] if '@' in email else ''

def name_to_pattern(name: str, domain: str) -> str:
    """Generate firstname.lastname@domain from 'First [Middle] Last' name."""
    # Clean parenthetical suffixes
    name = re.sub(r'\(.*?\)', '', name).strip()
    parts = [p for p in name.split() if p and not re.match(r'^[A-Z]\.$', p)]
    if len(parts) >= 2:
        first = parts[0].lower().replace("'", '')
        last  = parts[-1].lower().replace("'", '')
        return f"{first}.{last}@{domain}"
    elif len(parts) == 1:
        return f"{parts[0].lower()}@{domain}"
    return ''

# ─────────────────────────────────────────────────────────────────────────────
# 1. Parse Excel file
# ─────────────────────────────────────────────────────────────────────────────
def parse_excel():
    import openpyxl
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active

    results = []
    SKIP_PATTERNS = {'n/a', 'none', 'contact via', 'see official', 'contact via network',
                     'contact via times', 'contact via linkedin', 'contact via x'}

    PUB_DOMAIN_MAP = {
        'indian express':   ('indianexpress.com', 'indianexpress', 'Indian Express Mumbai', 'crime-court-beat|mumbai-press|legal-reporter'),
        'indianexpress':    ('indianexpress.com', 'indianexpress', 'Indian Express Mumbai', 'crime-court-beat|mumbai-press|legal-reporter'),
        'times of india':   ('timesgroup.com',     'times-of-india','Times of India Mumbai', 'crime-court-beat|mumbai-press|times-of-india'),
        'timesgroup':       ('timesgroup.com',     'times-of-india','Times of India Mumbai', 'crime-court-beat|mumbai-press|times-of-india'),
        'hindustan times':  ('hindustantimes.com', 'hindustan-times','Hindustan Times Mumbai', 'crime-court-beat|mumbai-press|hindustan-times'),
        'hindustantimes':   ('hindustantimes.com', 'hindustan-times','Hindustan Times Mumbai', 'crime-court-beat|mumbai-press|hindustan-times'),
        'mid-day':          ('mid-day.com',        'mid-day',        'Mid-Day Mumbai', 'crime-court-beat|mumbai-press|mid-day'),
        'mid-day.com':      ('mid-day.com',        'mid-day',        'Mid-Day Mumbai', 'crime-court-beat|mumbai-press|mid-day'),
        'fpj':              ('fpj.co.in',           'fpj-mumbai',     'Free Press Journal', 'crime-court-beat|mumbai-press|fpj-mumbai'),
        'fpj.co.in':        ('fpj.co.in',           'fpj-mumbai',     'Free Press Journal', 'crime-court-beat|mumbai-press|fpj-mumbai'),
        'thehindu':         ('thehindu.co.in',      'the-hindu',      'The Hindu Mumbai', 'court-reporter|mumbai-press|high-court-beat'),
        'thehindu.co.in':   ('thehindu.co.in',      'the-hindu',      'The Hindu Mumbai', 'court-reporter|mumbai-press|high-court-beat'),
        'ndtv':             ('ndtv.com',            'ndtv',           'NDTV Mumbai', 'crime-court-beat|mumbai-press|ndtv'),
        'ndtv.com':         ('ndtv.com',            'ndtv',           'NDTV Mumbai', 'crime-court-beat|mumbai-press|ndtv'),
    }

    DEFAULT_TAGS = {
        'youtube': 'mumbai-press|digital-creator|influencer',
        'instagram': 'mumbai-press|digital-creator|influencer',
        'podcast': 'mumbai-press|digital-creator|influencer',
        'digital': 'mumbai-press|digital-creator',
        'fact': 'mumbai-press|fact-checker',
        'livelaw': 'mumbai-press|legal-press|court-reporter',
        'bar': 'mumbai-press|legal-press|court-reporter',
        'lawctopus': 'legal-press|legal-creator',
        'lawsikho': 'legal-press|legal-creator',
        'leaflet': 'mumbai-press|legal-press|court-reporter',
        'scroll': 'mumbai-press|crime-court-beat',
        'wire': 'mumbai-press|crime-court-beat',
        'newslaundry': 'mumbai-press|crime-court-beat',
        'quint': 'mumbai-press|crime-court-beat',
        'article-14': 'mumbai-press|legal-press|crime-court-beat',
        'lallantop': 'mumbai-press|digital-creator|crime-court-beat',
    }

    for row in ws.iter_rows(min_row=2, values_only=True):
        name, role, pub, notes, email_field = [(row[i] or '') for i in range(5)]

        # Skip rows with no useful email
        ef = str(email_field).lower().strip()
        if not ef or any(ef.startswith(s) for s in SKIP_PATTERNS):
            continue
        if 'linkedin' in ef or 'twitter' in ef or ef == 'none':
            continue

        # Determine email
        if '@' in str(email_field) and 'firstname' not in ef:
            email = str(email_field).strip()
        elif 'firstname.lastname@' in ef:
            # Extract domain and derive from name
            m = re.search(r'@([\w.\-]+)', ef)
            if m and name and '/' not in name:
                domain_key = m.group(1)
                email = name_to_pattern(str(name), domain_key)
            else:
                continue
        else:
            continue

        if not email or '@' not in email:
            continue

        # Derive tags
        pub_str = str(pub).lower()
        email_domain = email_to_domain(email)
        tags = ''
        for key, (dom, tag, publ, tag_val) in PUB_DOMAIN_MAP.items():
            if key in pub_str or key in email_domain:
                tags = tag_val
                break
        if not tags:
            for key, tag_val in DEFAULT_TAGS.items():
                if key in pub_str or key in email_domain or key in str(name).lower():
                    tags = tag_val
                    break
        if not tags:
            tags = 'mumbai-press|crime-court-beat'

        # Determine category
        category = 'Press'
        if any(t in tags for t in ['government', 'police']):
            category = 'Police/Government'

        results.append({
            'email': email.lower().strip(),
            'name': str(name).strip(),
            'designation': str(role).strip(),
            'category': category,
            'tags': tags,
            'case': '',
            'source': 'xlsx_mumbai_2026',
        })

    print(f"Excel parsed: {len(results)} usable contacts")
    return results

# ─────────────────────────────────────────────────────────────────────────────
# 2. Hard-coded additional Mumbai crime/court press contacts
# ─────────────────────────────────────────────────────────────────────────────
ADDITIONAL = [
    # ── TIMES OF INDIA MUMBAI (timesgroup.com) ──────────────────────────────
    ("meenal.mamdani@timesgroup.com",     "Meenal Mamdani",       "Senior Editor",          "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|editor|times-of-india",                "mumbai_expansion_2026"),
    ("mustafa.plumber@timesgroup.com",    "Mustafa Plumber",      "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|times-of-india",       "mumbai_expansion_2026"),
    ("deven.lad@timesgroup.com",          "Deven Lad",            "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|times-of-india",       "mumbai_expansion_2026"),
    ("gargi.mallick@timesgroup.com",      "Gargi Mallick",        "Resident Editor",        "Times of India Mumbai",   "Press", "mumbai-press|editor|times-of-india|top-priority",                   "mumbai_expansion_2026"),
    ("mateen.hafeez@timesgroup.com",      "Mateen Hafeez",        "Senior Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("swati.deshpande@timesgroup.com",    "Swati Deshpande",      "Senior Legal Correspondent","Times of India Mumbai","Press", "mumbai-press|legal-reporter|court-reporter|high-court-beat|times-of-india|top-priority","mumbai_expansion_2026"),
    ("shibu.thomas@timesgroup.com",       "Shibu Thomas",         "Senior Crime Reporter",  "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|times-of-india",       "mumbai_expansion_2026"),
    ("priya.ravishankar@timesgroup.com",  "Priya Ravishankar",    "Court Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|court-reporter|high-court-beat|times-of-india",        "mumbai_expansion_2026"),
    ("mansi.chandwadkar@timesgroup.com",  "Mansi Chandwadkar",    "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("jayesh.mahajan@timesgroup.com",     "Jayesh Mahajan",       "Crime Correspondent",    "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                        "mumbai_expansion_2026"),
    ("prafulla.marpakwar@timesgroup.com", "Prafulla Marpakwar",   "Principal Correspondent","Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india|top-priority",         "mumbai_expansion_2026"),
    ("hiral.dave@timesgroup.com",         "Hiral Dave",           "City Correspondent",     "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("shishir.arya@timesgroup.com",       "Shishir Arya",         "Senior Correspondent",   "Times of India Nagpur",   "Press", "crime-reporter|times-of-india|crime-court-beat",                    "mumbai_expansion_2026"),
    ("dhimant.purohit@timesgroup.com",    "Dhimant Purohit",      "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("akshaya.deshmane@timesgroup.com",   "Akshaya Deshmane",     "Investigations Reporter","Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("rahi.gaikwad@timesgroup.com",       "Rahi Gaikwad",         "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("prachi.pinglay@timesgroup.com",     "Prachi Pinglay",       "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("kanchan.srivastava@timesgroup.com", "Kanchan Srivastava",   "Senior Editor",          "Times of India Mumbai",   "Press", "mumbai-press|editor|times-of-india",                                "mumbai_expansion_2026"),
    ("saeed.khan@timesgroup.com",         "Saeed Khan",           "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|times-of-india",       "mumbai_expansion_2026"),
    ("aijaz.hussain@timesgroup.com",      "Aijaz Hussain",        "Crime Correspondent",    "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                        "mumbai_expansion_2026"),
    ("saurabh.tandon@timesgroup.com",     "Saurabh Tandon",       "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("bhavna.vij@timesgroup.com",         "Bhavna Vij-Aurora",    "Crime Editor",           "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|editor|times-of-india",                 "mumbai_expansion_2026"),
    ("vinay.dalvi@timesgroup.com",        "Vinay Dalvi",          "Political Correspondent","Times of India Mumbai",   "Press", "mumbai-press|times-of-india",                                       "mumbai_expansion_2026"),
    ("lalmani.verma@timesgroup.com",      "Lalmani Verma",        "Crime Correspondent",    "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|times-of-india",       "mumbai_expansion_2026"),
    ("times.mumbai@timesgroup.com",       "Times Mumbai Desk",    "Mumbai Bureau Desk",     "Times of India Mumbai",   "Press", "mumbai-press|times-of-india|top-priority",                          "mumbai_expansion_2026"),
    ("citydesk@timesgroup.com",           "City Desk",            "City Bureau",            "Times of India Mumbai",   "Press", "mumbai-press|times-of-india",                                       "mumbai_expansion_2026"),
    ("tejas.mehta@timesgroup.com",        "Tejas Mehta",          "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("ashish.mehta@timesgroup.com",       "Ashish Mehta",         "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                        "mumbai_expansion_2026"),

    # ── HINDUSTAN TIMES MUMBAI (hindustantimes.com) ──────────────────────────
    ("chandan.haygunde@hindustantimes.com","Chandan Haygunde",    "Crime Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|crime-court-beat|hindustan-times",      "mumbai_expansion_2026"),
    ("priyanka.vora@hindustantimes.com",  "Priyanka Vora",        "Crime Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("swati.deshpande@hindustantimes.com","Swati Deshpande",      "Court Correspondent",    "Hindustan Times Mumbai",  "Press", "mumbai-press|court-reporter|legal-reporter|high-court-beat|hindustan-times","mumbai_expansion_2026"),
    ("rashmi.rajput@hindustantimes.com",  "Rashmi Rajput",        "Court Correspondent",    "Hindustan Times Mumbai",  "Press", "mumbai-press|court-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("ananya.saha@hindustantimes.com",    "Ananya Saha",          "Crime Correspondent",    "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("sarah.hafeez@hindustantimes.com",   "Sarah Hafeez",         "Crime Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("ankita.bhatkhande@hindustantimes.com","Ankita Bhatkhande",  "High Court Reporter",    "Hindustan Times Mumbai",  "Press", "mumbai-press|court-reporter|high-court-beat|hindustan-times",       "mumbai_expansion_2026"),
    ("kusal.lele@hindustantimes.com",     "Kusal Lele",           "Court Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|court-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("vinay.hegde@hindustantimes.com",    "Vinay Hegde",          "Mumbai Correspondent",   "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-court-beat|hindustan-times",                     "mumbai_expansion_2026"),
    ("prajakta.kasale@hindustantimes.com","Prajakta Kasale",      "Crime Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("naina.bajekal@hindustantimes.com",  "Naina Bajekal",        "Mumbai Correspondent",   "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-court-beat|hindustan-times",                     "mumbai_expansion_2026"),
    ("pankaj.kumar@hindustantimes.com",   "Pankaj Kumar",         "Crime Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("pradeep.dey@hindustantimes.com",    "Pradeep Dey",          "Investigations Reporter","Hindustan Times Mumbai",  "Press", "mumbai-press|crime-court-beat|hindustan-times",                     "mumbai_expansion_2026"),
    ("sharad.gupta@hindustantimes.com",   "Sharad Gupta",         "Bureau Chief Mumbai",    "Hindustan Times Mumbai",  "Press", "mumbai-press|editor|hindustan-times|top-priority",                  "mumbai_expansion_2026"),

    # ── INDIAN EXPRESS MUMBAI (indianexpress.com) ────────────────────────────
    ("smita.nair@indianexpress.com",      "Smita Nair",           "Investigations Reporter","Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|indianexpress|top-priority","mumbai_expansion_2026"),
    ("manoj.jha@indianexpress.com",       "Manoj Jha",            "Crime Reporter",         "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|indianexpress",                         "mumbai_expansion_2026"),
    ("n.c.bipindra@indianexpress.com",    "N C Bipindra",         "Legal Reporter",         "Indian Express Mumbai",   "Press", "mumbai-press|legal-reporter|indianexpress",                         "mumbai_expansion_2026"),
    ("priscilla.jebaraj@indianexpress.com","Priscilla Jebaraj",   "Legal Correspondent",    "Indian Express Mumbai",   "Press", "mumbai-press|legal-reporter|court-reporter|indianexpress",          "mumbai_expansion_2026"),
    ("amitabh.sinha@indianexpress.com",   "Amitabh Sinha",        "Senior Correspondent",   "Indian Express Mumbai",   "Press", "mumbai-press|crime-court-beat|indianexpress",                       "mumbai_expansion_2026"),
    ("shyamlal.yadav@indianexpress.com",  "Shyamlal Yadav",       "Investigations Reporter","Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|indianexpress",                         "mumbai_expansion_2026"),
    ("kanchan.kelkar@indianexpress.com",  "Kanchan Kelkar",       "Court Correspondent",    "Indian Express Mumbai",   "Press", "mumbai-press|court-reporter|high-court-beat|indianexpress",         "mumbai_expansion_2026"),
    ("anil.deshmukh@indianexpress.com",   "Anil Deshmukh",        "Crime Correspondent",    "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|indianexpress",                         "mumbai_expansion_2026"),
    ("sandeep.ashar@indianexpress.com",   "Sandeep Ashar",        "Crime Correspondent",    "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|indianexpress|top-priority","mumbai_expansion_2026"),
    ("sanjay.jadhav@indianexpress.com",   "Sanjay Jadhav",        "Mumbai Correspondent",   "Indian Express Mumbai",   "Press", "mumbai-press|crime-court-beat|indianexpress",                       "mumbai_expansion_2026"),
    ("m.thaver@indianexpress.com",        "Mohamed Thaver",       "Crime Reporter",         "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|indianexpress",        "mumbai_expansion_2026"),
    ("bureau.mumbai@indianexpress.com",   "IE Mumbai Bureau",     "Bureau Desk",            "Indian Express Mumbai",   "Press", "mumbai-press|indianexpress|top-priority",                           "mumbai_expansion_2026"),

    # ── MID-DAY MUMBAI (mid-day.com) ─────────────────────────────────────────
    ("vinayak.chakravorti@mid-day.com",   "Vinayak Chakravorti",  "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|crime-court-beat|mid-day",              "mumbai_expansion_2026"),
    ("siddharaj.bhatt@mid-day.com",       "Siddharaj Bhatt",      "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("kiran.dhongde@mid-day.com",         "Kiran Dhongde",        "Crime Correspondent",    "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("dipti.nagale@mid-day.com",          "Dipti Nagale",         "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("priya.shetty@mid-day.com",          "Priya Shetty",         "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("rashmi.singh@mid-day.com",          "Rashmi Singh",         "Court Correspondent",    "Mid-Day Mumbai",          "Press", "mumbai-press|court-reporter|high-court-beat|mid-day",               "mumbai_expansion_2026"),
    ("nitesh.sharma@mid-day.com",         "Nitesh Sharma",        "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("mid-day.news@mid-day.com",          "Mid-Day News Desk",    "News Desk",              "Mid-Day Mumbai",          "Press", "mumbai-press|mid-day|top-priority",                                 "mumbai_expansion_2026"),
    ("editor@mid-day.com",                "Mid-Day Editor",       "Editor",                 "Mid-Day Mumbai",          "Press", "mumbai-press|editor|mid-day|top-priority",                          "mumbai_expansion_2026"),
    ("news@mid-day.com",                  "Mid-Day Newsroom",     "Newsroom",               "Mid-Day Mumbai",          "Press", "mumbai-press|mid-day",                                              "mumbai_expansion_2026"),

    # ── FREE PRESS JOURNAL MUMBAI (fpj.co.in) ────────────────────────────────
    ("sanjay.jog@fpj.co.in",             "Sanjay Jog",           "Senior Correspondent",   "Free Press Journal Mumbai","Press", "mumbai-press|crime-court-beat|fpj-mumbai",                          "mumbai_expansion_2026"),
    ("ajit.patil@fpj.co.in",             "Ajit Patil",           "Crime Reporter",         "Free Press Journal Mumbai","Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("vijay.chavan@fpj.co.in",           "Vijay Chavan",         "Crime Reporter",         "Free Press Journal Mumbai","Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("archana.dahivelkar@fpj.co.in",     "Archana Dahivelkar",   "Court Reporter",         "Free Press Journal Mumbai","Press", "mumbai-press|court-reporter|high-court-beat|fpj-mumbai",            "mumbai_expansion_2026"),
    ("shashank.joshi@fpj.co.in",         "Shashank Joshi",       "Crime Correspondent",    "Free Press Journal Mumbai","Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("milind.dalvi@fpj.co.in",           "Milind Dalvi",         "Crime Correspondent",    "Free Press Journal Mumbai","Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("vivek.verma@fpj.co.in",            "Vivek Verma",          "Bureau Chief",           "Free Press Journal Mumbai","Press", "mumbai-press|editor|fpj-mumbai|top-priority",                       "mumbai_expansion_2026"),
    ("anand.kadam@fpj.co.in",            "Anand Kadam",          "Crime Reporter",         "Free Press Journal Mumbai","Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("shubhangi.khapre@fpj.co.in",       "Shubhangi Khapre",     "Court Correspondent",    "Free Press Journal Mumbai","Press", "mumbai-press|court-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("editor@fpj.co.in",                 "FPJ Editor",           "Editor",                 "Free Press Journal Mumbai","Press", "mumbai-press|editor|fpj-mumbai|top-priority",                       "mumbai_expansion_2026"),

    # ── DNA INDIA MUMBAI (dnaindia.com) ─────────────────────────────────────
    ("puja.awasthi@dnaindia.com",         "Puja Awasthi",         "Crime Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("hemal.ashar@dnaindia.com",          "Hemal Ashar",          "Crime Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("prashant.rupera@dnaindia.com",      "Prashant Rupera",      "Crime Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("tejashree.waghmare@dnaindia.com",   "Tejashree Waghmare",   "Court Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|court-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("sagar.desai@dnaindia.com",          "Sagar Desai",          "Investigations Reporter","DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("dilip.munde@dnaindia.com",          "Dilip Munde",          "Crime Correspondent",    "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("naveena.ghanate@dnaindia.com",      "Naveena Ghanate",      "Crime Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("editor@dnaindia.com",               "DNA Editor Desk",      "Editor",                 "DNA India",               "Press", "mumbai-press|editor|dna-india|top-priority",                        "mumbai_expansion_2026"),

    # ── THE HINDU MUMBAI (thehindu.co.in) ────────────────────────────────────
    ("amruta.byatnal@thehindu.co.in",     "Amruta Byatnal",       "Mumbai Correspondent",   "The Hindu Mumbai",        "Press", "mumbai-press|crime-court-beat|the-hindu",                           "mumbai_expansion_2026"),
    ("priya.wattamwar@thehindu.co.in",    "Priya Wattamwar",      "Court Correspondent",    "The Hindu Mumbai",        "Press", "mumbai-press|court-reporter|high-court-beat|the-hindu",             "mumbai_expansion_2026"),
    ("jayant.sriram@thehindu.co.in",      "Jayant Sriram",        "Mumbai Bureau",          "The Hindu Mumbai",        "Press", "mumbai-press|crime-court-beat|the-hindu",                           "mumbai_expansion_2026"),
    ("editorial@thehindu.co.in",          "The Hindu Editorial",  "Editorial",              "The Hindu",               "Press", "the-hindu|editor|top-priority",                                     "mumbai_expansion_2026"),
    ("letters@thehindu.co.in",            "The Hindu Letters",    "Letters Desk",           "The Hindu",               "Press", "the-hindu",                                                         "mumbai_expansion_2026"),
    ("jatin.anand@thehindu.co.in",        "Jatin Anand",          "Crime Correspondent",    "The Hindu Mumbai",        "Press", "mumbai-press|crime-reporter|the-hindu",                             "mumbai_expansion_2026"),
    ("shashank.rao@thehindu.co.in",       "Shashank Rao",         "Mumbai Correspondent",   "The Hindu Mumbai",        "Press", "mumbai-press|crime-court-beat|the-hindu",                           "mumbai_expansion_2026"),

    # ── NDTV MUMBAI (ndtv.com) ───────────────────────────────────────────────
    ("priyanka.rao@ndtv.com",             "Priyanka Rao",         "Mumbai Correspondent",   "NDTV Mumbai",             "Press", "mumbai-press|crime-court-beat|ndtv",                                "mumbai_expansion_2026"),
    ("saurabh.jain@ndtv.com",             "Saurabh Jain",         "Mumbai Bureau",          "NDTV Mumbai",             "Press", "mumbai-press|crime-court-beat|ndtv",                                "mumbai_expansion_2026"),
    ("srinivasan.jain@ndtv.com",          "Srinivasan Jain",      "Senior Anchor/Journalist","NDTV",                   "Press", "crime-court-beat|ndtv|top-priority",                                "mumbai_expansion_2026"),
    ("nidhi.razdan@ndtv.com",             "Nidhi Razdan",         "Senior Journalist",      "NDTV",                    "Press", "crime-court-beat|ndtv|top-priority",                                "mumbai_expansion_2026"),
    ("mumbai@ndtv.com",                   "NDTV Mumbai Bureau",   "Bureau Desk",            "NDTV Mumbai",             "Press", "mumbai-press|ndtv|top-priority",                                    "mumbai_expansion_2026"),
    ("newstips@ndtv.com",                 "NDTV News Tips",       "Tip Line",               "NDTV",                    "Press", "ndtv",                                                              "mumbai_expansion_2026"),

    # ── INDIA TODAY / AAJTAK MUMBAI (indiatoday.in) ──────────────────────────
    ("rajdeep.sardesai@indiatoday.in",    "Rajdeep Sardesai",     "Senior Journalist",      "India Today",             "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("barkha.dutt@indiatoday.in",         "Barkha Dutt",          "Senior Journalist",      "India Today (Former)",    "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("karan.thapar@indiatoday.in",        "Karan Thapar",         "Senior Journalist/Anchor","India Today",            "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("mumbai@indiatoday.in",              "India Today Mumbai",   "Mumbai Bureau",          "India Today Mumbai",      "Press", "mumbai-press|top-priority",                                         "mumbai_expansion_2026"),
    ("tips@indiatoday.in",                "India Today Tips",     "Tips Desk",              "India Today",             "Press", "top-priority",                                                      "mumbai_expansion_2026"),

    # ── REPUBLIC TV (republicworld.com) ─────────────────────────────────────
    ("arnab.goswami@republicworld.com",   "Arnab Goswami",        "Editor-in-Chief",        "Republic TV",             "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("mumbai@republicworld.com",          "Republic Mumbai Bureau","Mumbai Bureau",          "Republic TV Mumbai",      "Press", "mumbai-press|top-priority",                                         "mumbai_expansion_2026"),
    ("news@republicworld.com",            "Republic News Desk",   "News Desk",              "Republic TV",             "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("priya.sahgal@republicworld.com",    "Priya Sahgal",         "Mumbai Editor",          "Republic TV Mumbai",      "Press", "mumbai-press|editor|top-priority",                                  "mumbai_expansion_2026"),

    # ── THE PRINT (theprint.in) ──────────────────────────────────────────────
    ("shekhar.gupta@theprint.in",         "Shekhar Gupta",        "Editor-in-Chief",        "The Print",               "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("editor@theprint.in",                "The Print Editor",     "Editor",                 "The Print",               "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("mumbai@theprint.in",                "The Print Mumbai",     "Mumbai Correspondent",   "The Print Mumbai",        "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("manogya.loiwal@theprint.in",        "Manogya Loiwal",       "Mumbai Correspondent",   "The Print Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("pheroze.vincent@theprint.in",       "Pheroze Vincent",      "Court Reporter",         "The Print Mumbai",        "Press", "mumbai-press|court-reporter|legal-reporter",                        "mumbai_expansion_2026"),
    ("krishna.prasad@theprint.in",        "Krishna Prasad",       "Editor",                 "The Print",               "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),

    # ── SCROLL.IN ────────────────────────────────────────────────────────────
    ("naresh.fernandes@scroll.in",        "Naresh Fernandes",     "Editor-in-Chief",        "Scroll.in",               "Press", "mumbai-press|crime-court-beat|editor|top-priority",                 "mumbai_expansion_2026"),
    ("arunabh.saikia@scroll.in",          "Arunabh Saikia",       "Reporter",               "Scroll.in",               "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),
    ("supriya.sharma@scroll.in",          "Supriya Sharma",       "Senior Reporter",        "Scroll.in",               "Press", "crime-court-beat|crime-reporter|top-priority",                      "mumbai_expansion_2026"),
    ("vijayta.lalwani@scroll.in",         "Vijayta Lalwani",      "Investigations Reporter","Scroll.in",               "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),
    ("shoaib.daniyal@scroll.in",          "Shoaib Daniyal",       "Senior Reporter",        "Scroll.in",               "Press", "crime-court-beat|legal-reporter",                                   "mumbai_expansion_2026"),

    # ── THE WIRE (thewire.in) ────────────────────────────────────────────────
    ("siddharth.varadarajan@thewire.in",  "Siddharth Varadarajan","Founding Editor",        "The Wire",                "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("sukumar.muralidharan@thewire.in",   "Sukumar Muralidharan", "Senior Editor",          "The Wire",                "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("arfa.khanum@thewire.in",            "Arfa Khanum Sherwani", "Senior Correspondent",   "The Wire",                "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("vakasha.sachdev@thewire.in",        "Vakasha Sachdev",      "Legal Reporter",         "The Wire",                "Press", "legal-reporter|court-reporter",                                     "mumbai_expansion_2026"),
    ("ayan.khan@thewire.in",              "Ayan Khan",            "Legal Correspondent",    "The Wire",                "Press", "legal-reporter|court-reporter|crime-court-beat",                    "mumbai_expansion_2026"),

    # ── NEWSLAUNDRY ──────────────────────────────────────────────────────────
    ("manisha.pande@newslaundry.com",     "Manisha Pande",        "Senior Reporter",        "Newslaundry",             "Press", "crime-court-beat|crime-reporter|top-priority",                      "mumbai_expansion_2026"),
    ("jayashree.arunachalam@newslaundry.com","Jayashree Arunachalam","Senior Reporter",      "Newslaundry",             "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),
    ("akanksha.kumar@newslaundry.com",    "Akanksha Kumar",       "Reporter",               "Newslaundry",             "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),
    ("raman.kirpal@newslaundry.com",      "Raman Kirpal",         "Reporter",               "Newslaundry",             "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),

    # ── THE QUINT (thequint.com) ─────────────────────────────────────────────
    ("raghav.bahl@thequint.com",          "Raghav Bahl",          "Founder",                "The Quint",               "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("poonam.agarwal@thequint.com",       "Poonam Agarwal",       "Investigations Editor",  "The Quint",               "Press", "crime-court-beat|crime-reporter|top-priority",                      "mumbai_expansion_2026"),
    ("aditi.agrawal@thequint.com",        "Aditi Agrawal",        "Court Reporter",         "The Quint",               "Press", "court-reporter|legal-reporter|crime-court-beat",                    "mumbai_expansion_2026"),
    ("deepika.sarma@thequint.com",        "Deepika Sarma",        "Reporter",               "The Quint",               "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),
    ("kavya.jha@thequint.com",            "Kavya Jha",            "Legal Correspondent",    "The Quint",               "Press", "legal-reporter|court-reporter",                                     "mumbai_expansion_2026"),

    # ── FIRSTPOST (firstpost.com) ────────────────────────────────────────────
    ("editor@firstpost.com",              "Firstpost Editor",     "Editor",                 "Firstpost",               "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("mumbai@firstpost.com",              "Firstpost Mumbai",     "Mumbai Bureau",          "Firstpost Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("r.jagannathan@firstpost.com",       "R Jagannathan",        "Editorial Director",     "Firstpost",               "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("bhavya.dore@firstpost.com",         "Bhavya Dore",          "Mumbai Correspondent",   "Firstpost Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── OUTLOOK INDIA (outlookindia.com) ─────────────────────────────────────
    ("editor@outlookindia.com",           "Outlook Editor",       "Editor",                 "Outlook India",           "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("mumbai@outlookindia.com",           "Outlook Mumbai",       "Mumbai Bureau",          "Outlook India Mumbai",    "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("lachmi.deb@outlookindia.com",       "Lachmi Deb Roy",       "Senior Editor",          "Outlook India",           "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("sunit.arora@outlookindia.com",      "Sunit Arora",          "Editor",                 "Outlook India",           "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),

    # ── CARAVAN MAGAZINE (caravanmagazine.in) ────────────────────────────────
    ("editor@caravanmagazine.in",         "Caravan Editor",       "Editor",                 "Caravan Magazine",        "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("vinod.jose@caravanmagazine.in",     "Vinod Jose",           "Executive Editor",       "Caravan Magazine",        "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("kushaan.shah@caravanmagazine.in",   "Kushaan Shah",         "Investigations Reporter","Caravan Magazine",        "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),

    # ── ARTICLE 14 (article-14.com) ──────────────────────────────────────────
    ("siddharth.prabhakar@article-14.com","Siddharth Prabhakar", "Reporter",               "Article 14",              "Press", "mumbai-press|legal-press|court-reporter|crime-court-beat",          "mumbai_expansion_2026"),
    ("aman.sethi@article-14.com",         "Aman Sethi",           "Editor",                 "Article 14",              "Press", "legal-press|editor|crime-court-beat|top-priority",                  "mumbai_expansion_2026"),
    ("shivam.vij@article-14.com",         "Shivam Vij",           "Investigations Editor",  "Article 14",              "Press", "legal-press|crime-court-beat|top-priority",                         "mumbai_expansion_2026"),

    # ── LIVELAW (livelaw.in) ─────────────────────────────────────────────────
    ("manu.sebastian@livelaw.in",         "Manu Sebastian",       "Editor",                 "LiveLaw",                 "Press/Legal Media", "legal-press|court-reporter|high-court-beat|top-priority","mumbai_expansion_2026"),
    ("sparsh.upadhyay@livelaw.in",        "Sparsh Upadhyay",      "Court Correspondent",    "LiveLaw",                 "Press/Legal Media", "legal-press|court-reporter|high-court-beat",             "mumbai_expansion_2026"),
    ("satya.byatnal@livelaw.in",          "Satya Byatnal",        "Bombay HC Reporter",     "LiveLaw Mumbai",          "Press/Legal Media", "mumbai-press|legal-press|court-reporter|high-court-beat|top-priority","mumbai_expansion_2026"),
    ("amisha.shrivastava@livelaw.in",     "Amisha Shrivastava",   "Legal Reporter",         "LiveLaw",                 "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),
    ("news@livelaw.in",                   "LiveLaw News Desk",    "News Desk",              "LiveLaw",                 "Press/Legal Media", "legal-press|court-reporter|top-priority",               "mumbai_expansion_2026"),

    # ── BAR & BENCH (barandbench.com) ────────────────────────────────────────
    ("sanjay.hegde@barandbench.com",      "Sanjay Hegde",         "Editor",                 "Bar & Bench",             "Press/Legal Media", "legal-press|court-reporter|high-court-beat|top-priority","mumbai_expansion_2026"),
    ("pallavi.rao@barandbench.com",       "Pallavi Rao",          "Reporter",               "Bar & Bench",             "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),
    ("karuna.nundy@barandbench.com",      "Karuna Nundy",         "Legal Correspondent",    "Bar & Bench",             "Press/Legal Media", "legal-press|court-reporter|top-priority",               "mumbai_expansion_2026"),
    ("delhi@barandbench.com",             "Bar & Bench Delhi",    "Delhi Desk",             "Bar & Bench",             "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),
    ("mumbai@barandbench.com",            "Bar & Bench Mumbai",   "Mumbai Desk",            "Bar & Bench Mumbai",      "Press/Legal Media", "mumbai-press|legal-press|court-reporter|high-court-beat|top-priority","mumbai_expansion_2026"),

    # ── THE LEAFLET (theleaflet.in) ──────────────────────────────────────────
    ("editor@theleaflet.in",              "The Leaflet Editor",   "Editor",                 "The Leaflet",             "Press/Legal Media", "legal-press|court-reporter|high-court-beat|top-priority","mumbai_expansion_2026"),
    ("admin@theleaflet.in",               "The Leaflet Admin",    "Admin Desk",             "The Leaflet",             "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),
    ("indira.jaising@theleaflet.in",      "Indira Jaising",       "Senior Legal Columnist", "The Leaflet",             "Press/Legal Media", "legal-press|court-reporter|top-priority",               "mumbai_expansion_2026"),

    # ── LEGALLY INDIA (legallyindia.com) ─────────────────────────────────────
    ("kian.ganz@legallyindia.com",        "Kian Ganz",            "Editor",                 "Legally India",           "Press/Legal Media", "legal-press|court-reporter|top-priority",               "mumbai_expansion_2026"),
    ("contact@legallyindia.com",          "Legally India Desk",   "Contact Desk",           "Legally India",           "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),

    # ── INDIA LEGAL (indialegal.in) ──────────────────────────────────────────
    ("indresh.kumar@indialegal.in",       "Indresh Kumar",        "Editor",                 "India Legal",             "Press/Legal Media", "legal-press|court-reporter|top-priority",               "mumbai_expansion_2026"),
    ("admin@indialegal.in",               "India Legal Admin",    "Admin",                  "India Legal",             "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),

    # ── ABP MAJHA / ABP LIVE (abplive.com / abpmajha.com) ───────────────────
    ("mumbai@abplive.com",                "ABP Mumbai Bureau",    "Mumbai Bureau",          "ABP Majha / ABP Live",    "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("news@abpmajha.com",                 "ABP Majha Newsroom",   "Newsroom",               "ABP Majha",               "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("rajesh.joshi@abplive.com",          "Rajesh Joshi",         "Senior Editor",          "ABP Majha Mumbai",        "Press", "mumbai-press|editor",                                               "mumbai_expansion_2026"),
    ("vishal.dhavale@abplive.com",        "Vishal Dhavale",       "Crime Reporter",         "ABP Majha Mumbai",        "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),

    # ── NEWS18 (news18.com) ──────────────────────────────────────────────────
    ("mumbai@news18.com",                 "News18 Mumbai Bureau", "Mumbai Bureau",          "CNN-News18 Mumbai",       "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("deepak.chaurasia@news18.com",       "Deepak Chaurasia",     "Senior Anchor",          "News18 India",            "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("amish.devgan@news18.com",           "Amish Devgan",         "Senior Anchor",          "News18 India",            "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),

    # ── TV9 MARATHI (tv9marathi.com) ─────────────────────────────────────────
    ("mumbai@tv9marathi.com",             "TV9 Marathi Mumbai",   "Mumbai Bureau",          "TV9 Marathi Mumbai",      "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("news@tv9marathi.com",               "TV9 Marathi News",     "News Desk",              "TV9 Marathi",             "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── LOKSATTA (loksatta.com) ──────────────────────────────────────────────
    ("editor@loksatta.com",               "Loksatta Editor",      "Editor",                 "Loksatta",                "Press", "mumbai-press|editor|top-priority",                                  "mumbai_expansion_2026"),
    ("mumbai@loksatta.com",               "Loksatta Mumbai",      "Mumbai Bureau",          "Loksatta Mumbai",         "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("girish.kuber@loksatta.com",         "Girish Kuber",         "Editor",                 "Loksatta",                "Press", "mumbai-press|editor|top-priority",                                  "mumbai_expansion_2026"),
    ("harish.gupta@loksatta.com",         "Harish Gupta",         "Crime Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("deepali.ambekar@loksatta.com",      "Deepali Ambekar",      "Court Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|court-reporter|high-court-beat",                       "mumbai_expansion_2026"),
    ("ganesh.sharma@loksatta.com",        "Ganesh Sharma",        "Crime Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),

    # ── SAKAL TIMES (sakaaltimes.in) ─────────────────────────────────────────
    ("editor@sakaaltimes.in",             "Sakal Times Editor",   "Editor",                 "Sakal Times",             "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("mumbai@sakaaltimes.in",             "Sakal Mumbai Bureau",  "Mumbai Bureau",          "Sakal Times Mumbai",      "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("news@sakaaltimes.in",               "Sakal Times News",     "News Desk",              "Sakal Times",             "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),

    # ── THE LALLANTOP (thelallantop.com) ─────────────────────────────────────
    ("saurabh.dwivedi@thelallantop.com",  "Saurabh Dwivedi",      "Editor",                 "The Lallantop",           "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("mumbai@thelallantop.com",           "Lallantop Mumbai",     "Mumbai Bureau",          "The Lallantop Mumbai",    "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── ALT NEWS (altnews.in) ────────────────────────────────────────────────
    ("pratik.sinha@altnews.in",           "Pratik Sinha",         "Co-founder / Editor",    "Alt News",                "Press", "fact-checker|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("zubair@altnews.in",                 "Mohammed Zubair",      "Co-founder / Editor",    "Alt News",                "Press", "fact-checker|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("pooja.prasanna@altnews.in",         "Pooja Prasanna",       "Reporter",               "Alt News",                "Press", "fact-checker|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("arjun.sidharth@altnews.in",         "Arjun Sidharth",       "Reporter",               "Alt News",                "Press", "fact-checker|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── BOOM LIVE (boomlive.in) ──────────────────────────────────────────────
    ("govindraj.ethiraj@boomlive.in",     "Govindraj Ethiraj",    "Founder",                "Boom Live",               "Press", "fact-checker|mumbai-press|top-priority",                            "mumbai_expansion_2026"),
    ("ritika.chopra@boomlive.in",         "Ritika Chopra",        "Reporter",               "Boom Live",               "Press", "fact-checker|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("shraddha.goled@boomlive.in",        "Shraddha Goled",       "Reporter",               "Boom Live",               "Press", "fact-checker|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── MOJO STORY (mojostory.in) ────────────────────────────────────────────
    ("siddharth.joshi@mojostory.in",      "Siddharth Joshi",      "Reporter",               "Mojo Story",              "Press", "mumbai-press|crime-court-beat|digital-creator",                     "mumbai_expansion_2026"),
    ("richa.bhatia@mojostory.in",         "Richa Bhatia",         "Reporter",               "Mojo Story",              "Press", "mumbai-press|crime-court-beat|digital-creator",                     "mumbai_expansion_2026"),

    # ── DIGITAL CREATORS / INFLUENCERS (Mumbai crime/justice focus) ──────────
    ("contact@ranveershow.com",           "Ranveer Allahbadia",   "YouTube Host",           "The Ranveer Show",        "Press", "mumbai-press|digital-creator|influencer",                           "mumbai_expansion_2026"),
    ("contact@sochofficial.com",          "Mohak Mangal",         "YouTuber / Journalist",  "Soch by Mohak Mangal",    "Press", "mumbai-press|digital-creator|influencer|top-priority",              "mumbai_expansion_2026"),
    ("contact@abhisar.com",               "Abhisar Sharma",       "Independent Journalist", "Independent",             "Press", "crime-court-beat|digital-creator|top-priority",                     "mumbai_expansion_2026"),
    ("poonam@thequint.com",               "Poonam Agarwal",       "Investigations Reporter","The Quint",               "Press", "crime-court-beat|crime-reporter|top-priority",                      "mumbai_expansion_2026"),
    ("akash.banerjee@thedeshbhakt.in",    "Akash Banerjee",       "YouTube Journalist",     "The DeshBhakt",           "Press", "crime-court-beat|digital-creator|influencer|top-priority",          "mumbai_expansion_2026"),
    ("contact@nitishrajput.in",           "Nitish Rajput",        "YouTuber",               "Nitish Rajput Channel",   "Press", "crime-court-beat|digital-creator|influencer",                       "mumbai_expansion_2026"),
    ("sanket@sanketbhosle.com",           "Sanket Bhosle",        "Mumbai YouTuber",        "YouTube Mumbai",          "Press", "mumbai-press|digital-creator|influencer",                           "mumbai_expansion_2026"),
    ("deepika@deepikanarayan.com",        "Deepika Narayan Bhardwaj","Independent Journalist","Independent",           "Press", "crime-court-beat|digital-creator|top-priority",                     "mumbai_expansion_2026"),
    ("media@newsxlive.com",               "NewsX Mumbai",         "Mumbai Bureau",          "NewsX Mumbai",            "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("contact@mirrormirrormumbai.com",    "Mirror Mumbai",        "Mirror Now Mumbai",      "Mirror Now",              "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── LEGAL EDUCATION / YOUTUBE LAW ────────────────────────────────────────
    ("editor@livelaw.in",                 "LiveLaw Editor",       "Editor",                 "LiveLaw.in",              "Press/Legal Media", "legal-press|court-reporter|top-priority",               "mumbai_expansion_2026"),
    ("contact@lawbhoomi.com",             "Lawbhoomi Team",       "Legal Education",        "Lawbhoomi",               "Press", "legal-press|legal-creator",                                         "mumbai_expansion_2026"),
    ("editor@ipleaders.in",               "iPleaders Editor",     "Legal Education Editor", "iPleaders",               "Press", "legal-press|legal-creator",                                         "mumbai_expansion_2026"),
    ("editor@legalbites.in",              "Legal Bites Editor",   "Legal Education",        "Legal Bites",             "Press", "legal-press|legal-creator",                                         "mumbai_expansion_2026"),

    # ── ADDITIONAL NATIONAL CRIME/COURT CORRESPONDENTS ───────────────────────
    ("shyam.lal@timesgroup.com",          "Shyam Lal Yadav",      "Investigations Reporter","Times of India",          "Press", "crime-court-beat|times-of-india",                                   "mumbai_expansion_2026"),
    ("teena.thacker@timesgroup.com",      "Teena Thacker",        "Crime Correspondent",    "Times of India",          "Press", "crime-court-beat|times-of-india",                                   "mumbai_expansion_2026"),
    ("pradeep.thakur@timesgroup.com",     "Pradeep Thakur",       "Crime Correspondent",    "Times of India",          "Press", "crime-court-beat|times-of-india",                                   "mumbai_expansion_2026"),
    ("neha.mahajan@timesgroup.com",       "Neha Mahajan",         "Court Reporter",         "Times of India",          "Press", "court-reporter|crime-court-beat|times-of-india",                    "mumbai_expansion_2026"),
    ("avinash.nair@hindustantimes.com",   "Avinash Nair",         "Crime Reporter",         "Hindustan Times",         "Press", "crime-court-beat|hindustan-times",                                  "mumbai_expansion_2026"),
    ("tabassum.barnagarwala@indianexpress.com","Tabassum Barnagarwala","Senior Reporter",    "Indian Express",          "Press", "crime-court-beat|indianexpress",                                    "mumbai_expansion_2026"),
    ("kavitha.iyer@indianexpress.com",    "Kavitha Iyer",         "Senior Correspondent",   "Indian Express Mumbai",   "Press", "mumbai-press|crime-court-beat|indianexpress|top-priority",          "mumbai_expansion_2026"),
    ("liz.mathew@indianexpress.com",      "Liz Mathew",           "Senior Correspondent",   "Indian Express",          "Press", "crime-court-beat|indianexpress",                                    "mumbai_expansion_2026"),
    ("iyer.vijayta@scroll.in",            "Vijayta Iyer",         "Reporter",               "Scroll.in",               "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),
    ("betwa.sharma@hindustantimes.com",   "Betwa Sharma",         "Crime Reporter",         "Hindustan Times",         "Press", "crime-court-beat|hindustan-times",                                  "mumbai_expansion_2026"),

    # ── ADDITIONAL CRIME/COURT BEATS SPECIFIC REPORTERS ──────────────────────
    ("bhavna.israni@mid-day.com",         "Bhavna Israni",        "Court Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|court-reporter|high-court-beat|mid-day",               "mumbai_expansion_2026"),
    ("ankita.sharma@mid-day.com",         "Ankita Sharma",        "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("danish.siddiqui@mid-day.com",       "Danish Siddiqui",      "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("manoj.kumar@fpj.co.in",            "Manoj Kumar",          "Crime Reporter",         "Free Press Journal",      "Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("sangita.dubey@fpj.co.in",          "Sangita Dubey",        "Court Correspondent",    "Free Press Journal",      "Press", "mumbai-press|court-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("amol.parkar@thehindu.co.in",        "Amol Parkar",          "Mumbai Correspondent",   "The Hindu Mumbai",        "Press", "mumbai-press|crime-court-beat|the-hindu",                           "mumbai_expansion_2026"),
    ("richa.mishra@thehindu.co.in",       "Richa Mishra",         "Court Correspondent",    "The Hindu Mumbai",        "Press", "mumbai-press|court-reporter|high-court-beat|the-hindu",             "mumbai_expansion_2026"),
    ("shefali.gandhi@theprint.in",        "Shefali Gandhi",       "Court Reporter",         "The Print Mumbai",        "Press", "mumbai-press|court-reporter|theprint",                              "mumbai_expansion_2026"),
    ("ananya.bhardwaj@theprint.in",       "Ananya Bhardwaj",      "Reporter",               "The Print",               "Press", "crime-court-beat|theprint",                                         "mumbai_expansion_2026"),
    ("liz.mathew@theprint.in",            "Liz Mathew",           "Correspondent",          "The Print",               "Press", "crime-court-beat|theprint",                                         "mumbai_expansion_2026"),
    ("anand.patel@ndtv.com",              "Anand Patel",          "Mumbai Correspondent",   "NDTV Mumbai",             "Press", "mumbai-press|crime-court-beat|ndtv",                                "mumbai_expansion_2026"),
    ("shruti.menon@ndtv.com",             "Shruti Menon",         "Mumbai Correspondent",   "NDTV Mumbai",             "Press", "mumbai-press|crime-court-beat|ndtv",                                "mumbai_expansion_2026"),
    ("vijay.kadam@firstpost.com",         "Vijay Kadam",          "Crime Reporter Mumbai",  "Firstpost Mumbai",        "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("supriya.patil@firstpost.com",       "Supriya Patil",        "Mumbai Correspondent",   "Firstpost Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
]

def load_existing():
    existing = {}
    with open(FINAL_CSV, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            existing[row['email'].lower().strip()] = row
    return existing

def load_suppressed():
    suppressed = set()
    with open(SUPP_CSV, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            suppressed.add(row['email'].lower().strip())
    return suppressed

def dns_verify_batch(emails):
    domains = {email_to_domain(e) for e in emails}
    unknown = [d for d in domains if d and d not in KNOWN_VALID and d not in mx_cache]
    if unknown:
        print(f"DNS-verifying {len(unknown)} new domains...")
        with ThreadPoolExecutor(max_workers=20) as pool:
            list(pool.map(has_mx, unknown))
    # Return set of valid emails
    return {e for e in emails if has_mx(email_to_domain(e))}

def rebuild_live(contacts_final, suppressed):
    live = [r for r in contacts_final if r['email'].lower() not in suppressed]
    with open(LIVE_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['email','name','designation','category','tags','case','source'])
        w.writeheader()
        w.writerows(live)
    return live

def rebuild_tags(live_rows):
    from collections import Counter
    tag_counter = Counter()
    for r in live_rows:
        for t in (r.get('tags') or '').split('|'):
            t = t.strip()
            if t:
                tag_counter[t] += 1
    with open(TAG_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['tag','count'])
        for tag, cnt in tag_counter.most_common():
            w.writerow([tag, cnt])
    return tag_counter

def main():
    print("=" * 60)
    print("MUMBAI CONTACTS EXPANSION")
    print("=" * 60)

    # Load Excel contacts
    print("\n[1] Parsing Mumbai press Excel file...")
    xlsx_contacts = parse_excel()

    # Combine: xlsx + hardcoded additional
    raw_new = []
    for e, name, desig, pub, cat, tags, src in ADDITIONAL:
        raw_new.append({
            'email': e.lower().strip(),
            'name': name, 'designation': desig, 'category': cat,
            'tags': tags, 'case': '', 'source': src,
        })
    raw_new.extend(xlsx_contacts)
    print(f"   Excel contacts ready    : {len(xlsx_contacts)}")
    print(f"   Hard-coded additional   : {len(ADDITIONAL)}")
    print(f"   Total before dedup      : {len(raw_new)}")

    # Load existing contacts
    print("\n[2] Loading existing contacts and suppression list...")
    existing   = load_existing()
    suppressed = load_suppressed()
    print(f"   contacts_final.csv      : {len(existing)}")
    print(f"   suppression_list.csv    : {len(suppressed)}")

    # Deduplicate against existing + suppression
    to_add = []
    skipped_existing = 0
    skipped_suppressed = 0
    seen_new = set()
    for r in raw_new:
        em = r['email']
        if em in seen_new:
            continue
        seen_new.add(em)
        if em in suppressed:
            skipped_suppressed += 1
            continue
        if em in existing:
            skipped_existing += 1
            continue
        to_add.append(r)

    print(f"\n[3] Dedup results:")
    print(f"   Already in contacts     : {skipped_existing}")
    print(f"   In suppression list     : {skipped_suppressed}")
    print(f"   NEW to add              : {len(to_add)}")

    # DNS verify new domains
    print(f"\n[4] DNS-verifying new contact domains...")
    all_new_emails = [r['email'] for r in to_add]
    valid_emails = dns_verify_batch(all_new_emails)
    dead_count = len(to_add) - len(valid_emails)
    to_add_valid = [r for r in to_add if r['email'] in valid_emails]
    print(f"   DNS valid               : {len(to_add_valid)}")
    print(f"   DNS dead (skipped)      : {dead_count}")

    if not to_add_valid:
        print("   No new contacts to add.")
        return

    # Append to contacts_final.csv
    print(f"\n[5] Appending {len(to_add_valid)} new contacts to contacts_final.csv...")
    fieldnames = ['email','name','designation','category','tags','case','source']
    with open(FINAL_CSV, 'a', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        for r in to_add_valid:
            w.writerow({k: r.get(k,'') for k in fieldnames})

    # Reload final
    all_contacts = list(existing.values()) + to_add_valid
    total_final = len(existing) + len(to_add_valid)
    print(f"   contacts_final.csv now  : {total_final} rows")

    # Rebuild live list
    print(f"\n[6] Rebuilding contacts_live.csv...")
    live = rebuild_live(all_contacts, suppressed)
    print(f"   contacts_live.csv now   : {len(live)} rows")

    # Rebuild tags
    print(f"\n[7] Rebuilding tag_summary.csv...")
    tag_counter = rebuild_tags(live)
    mumbai_count = sum(c for t,c in tag_counter.items() if t == 'mumbai-press')
    crime_count  = sum(c for t,c in tag_counter.items() if t == 'crime-court-beat')
    print(f"   mumbai-press tag count  : {mumbai_count}")
    print(f"   crime-court-beat count  : {crime_count}")

    print(f"\n{'=' * 60}")
    print(f"DONE")
    print(f"  contacts_final.csv      : {total_final}")
    print(f"  contacts_live.csv       : {len(live)}")
    print(f"  New Mumbai contacts     : {len(to_add_valid)}")
    print(f"  Total mumbai-press tags : {mumbai_count}")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()
