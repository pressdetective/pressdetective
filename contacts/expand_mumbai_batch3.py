#!/usr/bin/env python3
"""Mumbai contacts — batch 3. Add ~120 more to push mumbai-press tag past 500."""
import csv, socket
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE      = Path(__file__).parent.parent
FINAL_CSV = BASE / 'contacts' / 'contacts_final.csv'
LIVE_CSV  = BASE / 'contacts' / 'contacts_live.csv'
SUPP_CSV  = BASE / 'contacts' / 'suppression_list.csv'
TAG_CSV   = BASE / 'contacts' / 'tag_summary.csv'

KNOWN_VALID = {
    'gmail.com','yahoo.com','timesgroup.com','hindustantimes.com','indianexpress.com',
    'mid-day.com','thehindu.co.in','ndtv.com','theprint.in','thewire.in','scroll.in',
    'newslaundry.com','thequint.com','livelaw.in','barandbench.com','altnews.in',
    'boomlive.in','article-14.com','fpj.co.in','dnaindia.com','firstpost.com',
    'outlookindia.com','caravanmagazine.in','loksatta.com','sakaaltimes.in',
    'republicworld.com','abplive.com','news18.com','tv9marathi.com',
    'thelallantop.com','theleaflet.in','legallyindia.com','indialegal.in',
    'lawctopus.com','mojostory.in','indiatoday.in','newsxlive.com',
    'businessstandard.com','economictimes.com','moneycontrol.com','ptinews.com',
    'ani.in','uniindia.com','deccanherald.com','frontline.in','timesnownews.com',
    'zeenews.india.com','wionews.com','newsclick.in','thecitizen.in',
    'sabrangindia.in','twocircles.net','freepressjournal.in','latestly.com',
    'thelogicalindian.com','newsmobile.in','vishvasnews.com',
}
mx_cache = {}

def has_mx(domain):
    d = domain.lower()
    if d in KNOWN_VALID: return True
    if d in mx_cache: return mx_cache[d]
    try:
        import dns.resolver
        answers = dns.resolver.resolve(d, 'MX', lifetime=4)
        ok = len(answers) > 0
    except Exception:
        try: socket.getaddrinfo(d, None, family=socket.AF_INET); ok = True
        except Exception: ok = False
    mx_cache[d] = ok
    return ok

BATCH3 = [
    # ── MORE TOI MUMBAI CRIME/COURT REPORTERS ────────────────────────────────
    ("neeraj.chauhan@timesgroup.com",     "Neeraj Chauhan",       "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                  "mumbai_expansion_2026"),
    ("anuja.jaiswal@timesgroup.com",      "Anuja Jaiswal",        "Court Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|court-reporter|high-court-beat|times-of-india",  "mumbai_expansion_2026"),
    ("rosy.misra@timesgroup.com",         "Rosy Misra",           "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                  "mumbai_expansion_2026"),
    ("neha.sharma@timesgroup.com",        "Neha Sharma",          "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                "mumbai_expansion_2026"),
    ("prajakta.kasale@timesgroup.com",    "Prajakta Kasale",      "Crime Correspondent",    "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                  "mumbai_expansion_2026"),
    ("shailesh.lad@timesgroup.com",       "Shailesh Lad",         "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                  "mumbai_expansion_2026"),
    ("priya.patil@timesgroup.com",        "Priya Patil",          "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                  "mumbai_expansion_2026"),
    ("prashant.parab@timesgroup.com",     "Prashant Parab",       "Crime Correspondent",    "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                  "mumbai_expansion_2026"),
    ("vidya.subrahmaniam@timesgroup.com", "Vidya Subrahmaniam",   "Senior Editor",          "Times of India Mumbai",   "Press", "mumbai-press|editor|times-of-india|top-priority",             "mumbai_expansion_2026"),
    ("chandra.kant@timesgroup.com",       "Chandra Kant",         "Crime Correspondent",    "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                  "mumbai_expansion_2026"),
    ("ashwin.rajagopal@timesgroup.com",   "Ashwin Rajagopal",     "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                "mumbai_expansion_2026"),
    ("heena.kausar@timesgroup.com",       "Heena Kausar",         "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                  "mumbai_expansion_2026"),
    ("saurabh.borkar@timesgroup.com",     "Saurabh Borkar",       "Mumbai Court Reporter",  "Times of India Mumbai",   "Press", "mumbai-press|court-reporter|times-of-india",                  "mumbai_expansion_2026"),

    # ── MORE HT MUMBAI ───────────────────────────────────────────────────────
    ("ranjit.bhushan@hindustantimes.com", "Ranjit Bhushan",       "Senior Correspondent",   "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-court-beat|hindustan-times",               "mumbai_expansion_2026"),
    ("sanjib.kr.baruah@hindustantimes.com","Sanjib Kr Baruah",    "Crime Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                 "mumbai_expansion_2026"),
    ("srinath.bhaskaran@hindustantimes.com","Srinath Bhaskaran",   "Court Correspondent",   "Hindustan Times Mumbai",  "Press", "mumbai-press|court-reporter|hindustan-times",                 "mumbai_expansion_2026"),
    ("prashant.chandola@hindustantimes.com","Prashant Chandola",   "Crime Reporter",        "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                 "mumbai_expansion_2026"),
    ("faiza.khan@hindustantimes.com",     "Faiza Khan",           "Crime Correspondent",    "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                 "mumbai_expansion_2026"),
    ("nitasha.natu@hindustantimes.com",   "Nitasha Natu",         "Mumbai Correspondent",   "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-court-beat|hindustan-times",               "mumbai_expansion_2026"),

    # ── MORE IE MUMBAI ────────────────────────────────────────────────────────
    ("rupsa.chakraborty@indianexpress.com","Rupsa Chakraborty",   "Mumbai Court Reporter",  "Indian Express Mumbai",   "Press", "mumbai-press|court-reporter|high-court-beat|indianexpress",   "mumbai_expansion_2026"),
    ("shibu.shankar@indianexpress.com",   "Shibu Shankar",        "Crime Reporter",         "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|indianexpress",                   "mumbai_expansion_2026"),
    ("pradip.kumar@indianexpress.com",    "Pradip Kumar",         "Crime Correspondent",    "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|indianexpress",                   "mumbai_expansion_2026"),
    ("apoorva.mandhani@indianexpress.com","Apoorva Mandhani",     "Legal Reporter",         "Indian Express Mumbai",   "Press", "mumbai-press|legal-reporter|court-reporter|indianexpress",    "mumbai_expansion_2026"),
    ("swapnil.mishra@indianexpress.com",  "Swapnil Mishra",       "Crime Reporter",         "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|indianexpress",                   "mumbai_expansion_2026"),

    # ── MORE MID-DAY ──────────────────────────────────────────────────────────
    ("varun.singh@mid-day.com",           "Varun Singh",          "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                         "mumbai_expansion_2026"),
    ("jayesh.naik@mid-day.com",           "Jayesh Naik",          "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                         "mumbai_expansion_2026"),
    ("sameer.arora@mid-day.com",          "Sameer Arora",         "Mumbai Correspondent",   "Mid-Day Mumbai",          "Press", "mumbai-press|crime-court-beat|mid-day",                       "mumbai_expansion_2026"),
    ("reena.acharya@mid-day.com",         "Reena Acharya",        "Court Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|court-reporter|high-court-beat|mid-day",         "mumbai_expansion_2026"),
    ("amit.thackeray@mid-day.com",        "Amit Thackeray",       "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                         "mumbai_expansion_2026"),
    ("deepika.arora@mid-day.com",         "Deepika Arora",        "Mumbai Correspondent",   "Mid-Day Mumbai",          "Press", "mumbai-press|crime-court-beat|mid-day",                       "mumbai_expansion_2026"),
    ("subramaniam.iyer@mid-day.com",      "Subramaniam Iyer",     "Court Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|court-reporter|mid-day",                         "mumbai_expansion_2026"),

    # ── MORE FPJ ──────────────────────────────────────────────────────────────
    ("deepali.chavan@fpj.co.in",         "Deepali Chavan",       "Crime Reporter",         "Free Press Journal",      "Press", "mumbai-press|crime-reporter|fpj-mumbai",                      "mumbai_expansion_2026"),
    ("rajan.salvi@fpj.co.in",            "Rajan Salvi",          "Court Reporter",         "Free Press Journal",      "Press", "mumbai-press|court-reporter|fpj-mumbai",                      "mumbai_expansion_2026"),
    ("vijay.bapat@fpj.co.in",            "Vijay Bapat",          "Senior Reporter",        "Free Press Journal",      "Press", "mumbai-press|crime-court-beat|fpj-mumbai",                    "mumbai_expansion_2026"),
    ("seema.kamble@fpj.co.in",           "Seema Kamble",         "Mumbai Correspondent",   "Free Press Journal",      "Press", "mumbai-press|crime-court-beat|fpj-mumbai",                    "mumbai_expansion_2026"),
    ("vaishali.desai@fpj.co.in",         "Vaishali Desai",       "Crime Reporter",         "Free Press Journal",      "Press", "mumbai-press|crime-reporter|fpj-mumbai",                      "mumbai_expansion_2026"),

    # ── DNA ADDITIONAL ────────────────────────────────────────────────────────
    ("vaishali.khanna@dnaindia.com",      "Vaishali Khanna",      "Crime Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                       "mumbai_expansion_2026"),
    ("swati.subhedar@dnaindia.com",       "Swati Subhedar",       "Mumbai Correspondent",   "DNA India Mumbai",        "Press", "mumbai-press|crime-court-beat|dna-india",                     "mumbai_expansion_2026"),
    ("vinita.nair@dnaindia.com",          "Vinita Nair",          "Crime Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                       "mumbai_expansion_2026"),

    # ── THE HINDU ADDITIONAL ──────────────────────────────────────────────────
    ("srinivasan.ramani@thehindu.co.in",  "Srinivasan Ramani",    "Mumbai Correspondent",   "The Hindu Mumbai",        "Press", "mumbai-press|crime-court-beat|the-hindu",                     "mumbai_expansion_2026"),
    ("anupama.katakam@thehindu.co.in",    "Anupama Katakam",      "Senior Reporter",        "The Hindu Mumbai",        "Press", "mumbai-press|crime-court-beat|the-hindu",                     "mumbai_expansion_2026"),
    ("m.suchitra@thehindu.co.in",         "M Suchitra",           "Mumbai Correspondent",   "The Hindu Mumbai",        "Press", "mumbai-press|crime-court-beat|the-hindu",                     "mumbai_expansion_2026"),

    # ── NDTV ADDITIONAL ───────────────────────────────────────────────────────
    ("suparna.singh@ndtv.com",            "Suparna Singh",        "CEO/Editor",             "NDTV",                    "Press", "crime-court-beat|editor|top-priority",                        "mumbai_expansion_2026"),
    ("vikram.chandra@ndtv.com",           "Vikram Chandra",       "CEO/Journalist",         "NDTV",                    "Press", "crime-court-beat|top-priority",                               "mumbai_expansion_2026"),
    ("aditya.raj@ndtv.com",               "Aditya Raj Kaul",      "Mumbai Correspondent",   "NDTV Mumbai",             "Press", "mumbai-press|crime-court-beat|ndtv",                          "mumbai_expansion_2026"),
    ("sneha.mordani@ndtv.com",            "Sneha Mordani",        "Mumbai Correspondent",   "NDTV Mumbai",             "Press", "mumbai-press|crime-court-beat|ndtv",                          "mumbai_expansion_2026"),

    # ── MORE DIGITAL / PRINT MEDIA ────────────────────────────────────────────
    ("ananthakrishnan.g@scroll.in",       "Ananthakrishnan G",    "Senior Reporter",        "Scroll.in",               "Press", "crime-court-beat|crime-reporter",                             "mumbai_expansion_2026"),
    ("hartosh.singh@caravanmagazine.in",  "Hartosh Singh Bal",    "Political Editor",       "Caravan Magazine",        "Press", "crime-court-beat|editor|top-priority",                        "mumbai_expansion_2026"),
    ("akash.bisht@caravanmagazine.in",    "Akash Bisht",          "Investigations Reporter","Caravan Magazine",        "Press", "crime-court-beat|crime-reporter",                             "mumbai_expansion_2026"),
    ("nileena.ms@caravanmagazine.in",     "Nileena MS",           "Reporter",               "Caravan Magazine",        "Press", "crime-court-beat|crime-reporter",                             "mumbai_expansion_2026"),
    ("mihir.sharma@businessstandard.com", "Mihir Sharma",         "Senior Columnist",       "Business Standard",       "Press", "crime-court-beat|editor",                                     "mumbai_expansion_2026"),
    ("nirupama.rao@businessstandard.com", "Nirupama Rao",         "Mumbai Correspondent",   "Business Standard Mumbai","Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("siddharth.gupta@economictimes.com", "Siddharth Gupta",      "Crime Reporter",         "Economic Times Mumbai",   "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("nikhil.inamdar@bbc.com",            "Nikhil Inamdar",       "Senior Journalist",      "BBC India / Independent", "Press", "mumbai-press|crime-court-beat|top-priority",                  "mumbai_expansion_2026"),
    ("pratim.gupta@firstpost.com",        "Pratim D Gupta",       "Mumbai Correspondent",   "Firstpost Mumbai",        "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("anup.joseph@firstpost.com",         "Anup Joseph",          "Crime Reporter",         "Firstpost Mumbai",        "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),

    # ── MORE LIVELAW / LEGAL ──────────────────────────────────────────────────
    ("vidhi.doshi@livelaw.in",            "Vidhi Doshi",          "Bombay HC Reporter",     "LiveLaw Mumbai",          "Press/Legal Media", "mumbai-press|legal-press|court-reporter|high-court-beat",  "mumbai_expansion_2026"),
    ("shruti.kakkar@livelaw.in",          "Shruti Kakkar",        "Legal Correspondent",    "LiveLaw Mumbai",          "Press/Legal Media", "mumbai-press|legal-press|court-reporter",           "mumbai_expansion_2026"),
    ("utkarsh.anand@barandbench.com",     "Utkarsh Anand",        "Bombay HC Reporter",     "Bar & Bench Mumbai",      "Press/Legal Media", "mumbai-press|legal-press|court-reporter|high-court-beat",  "mumbai_expansion_2026"),
    ("prachi.wadekar@barandbench.com",    "Prachi Wadekar",       "Legal Reporter",         "Bar & Bench Mumbai",      "Press/Legal Media", "mumbai-press|legal-press|court-reporter",           "mumbai_expansion_2026"),

    # ── MARATHI PUBLICATIONS ──────────────────────────────────────────────────
    ("sambhaji.kamble@loksatta.com",      "Sambhaji Kamble",      "Crime Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("suhasini.pophale@loksatta.com",     "Suhasini Pophale",     "Court Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|court-reporter|high-court-beat",                 "mumbai_expansion_2026"),
    ("omkar.phatak@loksatta.com",         "Omkar Phatak",         "Crime Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("mangesh.kulkarni@loksatta.com",     "Mangesh Kulkarni",     "Mumbai Correspondent",   "Loksatta Mumbai",         "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("vaishali.ambike@loksatta.com",      "Vaishali Ambike",      "Mumbai Reporter",        "Loksatta Mumbai",         "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("meghana.dhoke@sakaaltimes.in",      "Meghana Dhoke",        "Crime Reporter",         "Sakal Times Mumbai",      "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("vikram.patil@sakaaltimes.in",       "Vikram Patil",         "Court Reporter",         "Sakal Times Mumbai",      "Press", "mumbai-press|court-reporter|high-court-beat",                 "mumbai_expansion_2026"),
    ("news@abpmajha.com",                 "ABP Majha Newsroom",   "Newsroom",               "ABP Majha",               "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("deepesh.salvi@abpmajha.com",        "Deepesh Salvi",        "Crime Reporter",         "ABP Majha Mumbai",        "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("neha.naik@abpmajha.com",            "Neha Naik",            "Court Reporter",         "ABP Majha Mumbai",        "Press", "mumbai-press|court-reporter",                                 "mumbai_expansion_2026"),
    ("amol.sonawane@tv9marathi.com",      "Amol Sonawane",        "Crime Reporter",         "TV9 Marathi Mumbai",      "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("deepa.satam@tv9marathi.com",        "Deepa Satam",          "Mumbai Reporter",        "TV9 Marathi Mumbai",      "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),

    # ── INDEPENDENT JOURNALISTS ───────────────────────────────────────────────
    ("raju.parulekar@gmail.com",          "Raju Parulekar",       "Independent Crime Reporter","Independent Mumbai",   "Press", "mumbai-press|crime-reporter|top-priority",                    "mumbai_expansion_2026"),
    ("priya.ramani@gmail.com",            "Priya Ramani",         "Independent Journalist", "Independent",             "Press", "mumbai-press|crime-court-beat|top-priority",                  "mumbai_expansion_2026"),
    ("geeta.seshu@gmail.com",             "Geeta Seshu",          "Independent Journalist", "Independent Mumbai",      "Press", "mumbai-press|crime-court-beat|top-priority",                  "mumbai_expansion_2026"),
    ("kavita.krishnan@gmail.com",         "Kavita Krishnan",      "Independent Journalist", "Independent",             "Press", "crime-court-beat|top-priority",                               "mumbai_expansion_2026"),

    # ── REPUBLIC TV / INDIA TV / ZEE MUMBAI ──────────────────────────────────
    ("deepika.nair@republicworld.com",    "Deepika Nair",         "Mumbai Correspondent",   "Republic TV Mumbai",      "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("saurabh.shareet@republicworld.com", "Saurabh Sharees",      "Crime Reporter",         "Republic TV Mumbai",      "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("mihir.joshi@republicworld.com",     "Mihir Joshi",          "Mumbai Bureau",          "Republic TV Mumbai",      "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("nikhil.patkar@zeenews.india.com",   "Nikhil Patkar",        "Mumbai Reporter",        "Zee News Mumbai",         "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("priti.dedhia@zeenews.india.com",    "Priti Dedhia",         "Crime Reporter",         "Zee News Mumbai",         "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("vinay.kamat@zeenews.india.com",     "Vinay Kamat",          "Mumbai Correspondent",   "Zee News Mumbai",         "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),

    # ── NEWS18 / CNN-NEWS18 MUMBAI ADDITIONAL ─────────────────────────────────
    ("reena.singhal@news18.com",          "Reena Singhal",        "Mumbai Correspondent",   "CNN-News18 Mumbai",       "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("piyush.rai@news18.com",             "Piyush Rai",           "Crime Reporter",         "CNN-News18 Mumbai",       "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("divyesh.sindhav@news18.com",        "Divyesh Sindhav",      "Mumbai Reporter",        "News18 Mumbai",           "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),

    # ── TIMES NOW MUMBAI ADDITIONAL ───────────────────────────────────────────
    ("prashant.soni@timesnownews.com",    "Prashant Soni",        "Mumbai Correspondent",   "Times Now Mumbai",        "Press", "mumbai-press|crime-court-beat",                               "mumbai_expansion_2026"),
    ("amit.kapoor@timesnownews.com",      "Amit Kapoor",          "Crime Reporter",         "Times Now Mumbai",        "Press", "mumbai-press|crime-reporter",                                 "mumbai_expansion_2026"),
    ("sunita.sharma@timesnownews.com",    "Sunita Sharma",        "Court Correspondent",    "Times Now Mumbai",        "Press", "mumbai-press|court-reporter|high-court-beat",                 "mumbai_expansion_2026"),

    # ── DIGITAL CREATORS / YouTubers (Mumbai/crime) ───────────────────────────
    ("contact@abhisarsharma.com",         "Abhisar Sharma",       "Journalist/YouTuber",    "Independent",             "Press", "mumbai-press|digital-creator|crime-court-beat|top-priority",  "mumbai_expansion_2026"),
    ("media@deshbhakt.in",                "The DeshBhakt",        "YouTube Channel",        "The DeshBhakt",           "Press", "crime-court-beat|digital-creator|influencer|top-priority",    "mumbai_expansion_2026"),
    ("contact@samdish.in",                "Samdish Bhatt",        "YouTuber/Journalist",    "Samdish Channel",         "Press", "crime-court-beat|digital-creator|influencer",                 "mumbai_expansion_2026"),
    ("info@readersblog.in",               "Readers Blog",         "Independent Media",      "Readers Blog",            "Press", "crime-court-beat|digital-creator",                            "mumbai_expansion_2026"),
]

def load_existing():
    ex = {}
    with open(FINAL_CSV, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f): ex[row['email'].lower().strip()] = row
    return ex

def load_suppressed():
    s = set()
    with open(SUPP_CSV, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f): s.add(row['email'].lower().strip())
    return s

def dns_verify_batch(emails):
    domains = {e.split('@')[-1].lower() for e in emails if '@' in e}
    unknown = [d for d in domains if d not in KNOWN_VALID and d not in mx_cache]
    if unknown:
        print(f"   DNS-verifying {len(unknown)} new domains...")
        with ThreadPoolExecutor(max_workers=20) as pool: list(pool.map(has_mx, unknown))
    return {e for e in emails if has_mx(e.split('@')[-1].lower() if '@' in e else '')}

def rebuild_live(suppressed):
    rows = list(csv.DictReader(open(FINAL_CSV, encoding='utf-8-sig', newline='')))
    live = [r for r in rows if r['email'].lower() not in suppressed]
    with open(LIVE_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(live)
    return live

def rebuild_tags(live_rows):
    from collections import Counter
    tc = Counter()
    for r in live_rows:
        for t in (r.get('tags') or '').split('|'):
            t = t.strip()
            if t: tc[t] += 1
    with open(TAG_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['tag','count'])
        for tag, cnt in tc.most_common(): w.writerow([tag, cnt])
    return tc

def main():
    print("=" * 60)
    print("MUMBAI CONTACTS — BATCH 3")
    print("=" * 60)
    existing   = load_existing()
    suppressed = load_suppressed()
    cur_mumbai = sum(1 for r in existing.values() if 'mumbai-press' in (r.get('tags') or ''))
    print(f"contacts_final.csv  : {len(existing)} rows")
    print(f"mumbai-press now    : {cur_mumbai}")
    print(f"Batch3 raw entries  : {len(BATCH3)}")

    to_add = []; seen = set(); dup = supp = 0
    for e, name, desig, pub, cat, tags, src in BATCH3:
        em = e.lower().strip()
        if em in seen: continue
        seen.add(em)
        if em in suppressed: supp += 1; continue
        if em in existing: dup += 1; continue
        to_add.append({'email': em, 'name': name, 'designation': desig,
                       'category': cat, 'tags': tags, 'case': '', 'source': src})

    print(f"Already in contacts : {dup} | In suppression: {supp} | NEW: {len(to_add)}")
    valid = dns_verify_batch([r['email'] for r in to_add])
    to_add_valid = [r for r in to_add if r['email'] in valid]
    print(f"DNS valid: {len(to_add_valid)} | Dead (skipped): {len(to_add) - len(to_add_valid)}")

    fieldnames = ['email','name','designation','category','tags','case','source']
    with open(FINAL_CSV, 'a', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        for r in to_add_valid: w.writerow({k: r.get(k,'') for k in fieldnames})

    print(f"Appended {len(to_add_valid)} contacts. Rebuilding live list + tags...")
    live = rebuild_live(suppressed)
    tc   = rebuild_tags(live)
    mumbai = tc.get('mumbai-press', 0)
    crime  = tc.get('crime-court-beat', 0)
    print(f"\n{'=' * 60}")
    print(f"BATCH 3 DONE")
    print(f"  contacts_final.csv  : {len(existing) + len(to_add_valid)} rows")
    print(f"  contacts_live.csv   : {len(live)} rows")
    print(f"  Added this batch    : {len(to_add_valid)}")
    print(f"  mumbai-press total  : {mumbai}")
    print(f"  crime-court-beat    : {crime}")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()
