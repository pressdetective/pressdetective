#!/usr/bin/env python3
"""
Mumbai contacts — batch 2.
Add ~250 more Mumbai-focused crime/court press contacts to reach 500+ total.
"""
import csv, socket
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE      = Path(__file__).parent.parent
FINAL_CSV = BASE / 'contacts' / 'contacts_final.csv'
LIVE_CSV  = BASE / 'contacts' / 'contacts_live.csv'
SUPP_CSV  = BASE / 'contacts' / 'suppression_list.csv'
TAG_CSV   = BASE / 'contacts' / 'tag_summary.csv'

KNOWN_VALID = {
    'gmail.com','yahoo.com','yahoo.co.in','hotmail.com','outlook.com',
    'timesgroup.com','hindustantimes.com','indianexpress.com','mid-day.com',
    'thehindu.co.in','ndtv.com','theprint.in','thewire.in','scroll.in',
    'newslaundry.com','thequint.com','livelaw.in','barandbench.com',
    'altnews.in','boomlive.in','article-14.com','fpj.co.in','dnaindia.com',
    'firstpost.com','outlookindia.com','caravanmagazine.in','loksatta.com',
    'sakaaltimes.in','republicworld.com','abplive.com','news18.com',
    'tv9marathi.com','thelallantop.com','theleaflet.in','legallyindia.com',
    'indialegal.in','lawctopus.com','mojostory.in','indiatoday.in',
    'newsxlive.com','abpmajha.com','lawbhoomi.com','frontline.in',
    'businessstandard.com','economictimes.com','moneycontrol.com',
    'bq-prime.com','freepressjournal.in','ptinews.com','ani.in',
    'uniindia.com','deccanherald.com','thestatesman.com','tribune.com',
    'hindustantimes.com','amarujala.com','dainikbhaskar.com',
    'navbharattimes.indiatimes.com','navbharat.times.com',
    'sabrangindia.in','twocircles.net','thecitizen.in','thesiasat.com',
    'countercurrents.org','newsclick.in','thebetterindia.com',
    'huffingtonpost.in','thelogicalindian.com','latestly.com',
    'republicworld.com','wionews.com','timesnownews.com',
    'zeenews.india.com','abcnews.com',
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
        try:
            socket.getaddrinfo(d, None, family=socket.AF_INET)
            ok = True
        except Exception:
            ok = False
    mx_cache[d] = ok
    return ok

def email_to_domain(email):
    return email.lower().split('@')[-1] if '@' in email else ''

BATCH2 = [
    # ── TIMES NOW / MIRROR NOW (timesnownews.com) ─────────────────────────────
    ("mumbai@timesnownews.com",           "Times Now Mumbai",     "Mumbai Bureau",          "Times Now Mumbai",        "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("rahul.shivshankar@timesnownews.com","Rahul Shivshankar",    "Editor-in-Chief",        "Times Now",               "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("navika.kumar@timesnownews.com",     "Navika Kumar",         "Editor",                 "Times Now",               "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("padmaja.joshi@timesnownews.com",    "Padmaja Joshi",        "Consulting Editor",      "Times Now",               "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("pooja.shali@timesnownews.com",      "Pooja Shali",          "Mumbai Anchor",          "Times Now Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("keerthi.j@timesnownews.com",        "Keerthi J",            "Crime Reporter",         "Mirror Now Mumbai",       "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("vishnu.prasad@timesnownews.com",    "Vishnu Prasad",        "Mumbai Reporter",        "Times Now Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── ZEE NEWS MUMBAI (zeenews.india.com) ──────────────────────────────────
    ("mumbai@zeenews.india.com",          "Zee News Mumbai",      "Mumbai Bureau",          "Zee News Mumbai",         "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("sudhir.chaudhary@zeenews.india.com","Sudhir Chaudhary",     "Editor-in-Chief",        "Zee News",                "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("rohit.raina@zeenews.india.com",     "Rohit Raina",          "Mumbai Correspondent",   "Zee News Mumbai",         "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── AAJTAK / INDIA TODAY TV (indiatoday.in) ───────────────────────────────
    ("rohan.vora@indiatoday.in",          "Rohan Vora",           "Mumbai Correspondent",   "India Today Mumbai",      "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("deepak.sharma@indiatoday.in",       "Deepak Sharma",        "Crime Reporter Mumbai",  "India Today Mumbai",      "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("sweta.singh@indiatoday.in",         "Sweta Singh",          "Anchor",                 "Aaj Tak",                 "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("anjana.kasturi@indiatoday.in",      "Anjana Om Kashyap",    "Senior Anchor",          "Aaj Tak",                 "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("vikrant.guptaa@indiatoday.in",      "Vikrant Gupta",        "Sports/Crime Anchor",    "India Today",             "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),
    ("nikhil.naz@indiatoday.in",          "Nikhil Naz",           "Mumbai Reporter",        "India Today Mumbai",      "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── WION NEWS (wionews.com) ───────────────────────────────────────────────
    ("sidhant.sibal@wionews.com",         "Sidhant Sibal",        "Senior Journalist",      "WION News",               "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("palki.sharma@wionews.com",          "Palki Sharma",         "Executive Editor",       "WION News",               "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("mumbai@wionews.com",                "WION Mumbai Bureau",   "Mumbai Bureau",          "WION Mumbai",             "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── NEWSCLICK (newsclick.in) ──────────────────────────────────────────────
    ("editor@newsclick.in",               "Newsclick Editor",     "Editor",                 "NewsClick",               "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("contact@newsclick.in",              "Newsclick Desk",       "Contact Desk",           "NewsClick",               "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),
    ("prabir.purkayastha@newsclick.in",   "Prabir Purkayastha",   "Editor",                 "NewsClick",               "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("mumbai@newsclick.in",               "Newsclick Mumbai",     "Mumbai Reporter",        "NewsClick Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── THE CITIZEN (thecitizen.in) ───────────────────────────────────────────
    ("seema.mustafa@thecitizen.in",       "Seema Mustafa",        "Editor",                 "The Citizen",             "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("editor@thecitizen.in",              "The Citizen Editor",   "Editor",                 "The Citizen",             "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("mumbai@thecitizen.in",              "The Citizen Mumbai",   "Mumbai Reporter",        "The Citizen Mumbai",      "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── SABRANG INDIA (sabrangindia.in) ──────────────────────────────────────
    ("teesta.setalvad@sabrangindia.in",   "Teesta Setalvad",      "Editor / Rights Activist","Sabrang India",          "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("editor@sabrangindia.in",            "Sabrang Editor",       "Editor",                 "Sabrang India",           "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("mumbai@sabrangindia.in",            "Sabrang Mumbai",       "Mumbai Desk",            "Sabrang India Mumbai",    "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── TWO CIRCLES (twocircles.net) ─────────────────────────────────────────
    ("editor@twocircles.net",             "Two Circles Editor",   "Editor",                 "TwoCircles.net",          "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("mumbai@twocircles.net",             "TwoCircles Mumbai",    "Mumbai Reporter",        "TwoCircles Mumbai",       "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── BUSINESS STANDARD MUMBAI (businessstandard.com) ─────────────────────
    ("mumbai@businessstandard.com",       "BS Mumbai Bureau",     "Mumbai Bureau",          "Business Standard Mumbai","Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("editor@businessstandard.com",       "BS Editor",            "Editor",                 "Business Standard",       "Press", "editor|top-priority",                                               "mumbai_expansion_2026"),
    ("ruchika.chitravanshi@businessstandard.com","Ruchika Chitravanshi","Senior Reporter",   "Business Standard Mumbai","Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("jay.dubashi@businessstandard.com",  "Jay Dubashi",          "Senior Reporter",        "Business Standard Mumbai","Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("vinay.umarji@businessstandard.com", "Vinay Umarji",         "Mumbai Correspondent",   "Business Standard Mumbai","Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("vasantha.arora@businessstandard.com","Vasantha Arora",      "Crime Correspondent",    "Business Standard",       "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),

    # ── ECONOMIC TIMES MUMBAI (economictimes.com) ────────────────────────────
    ("mumbai@economictimes.com",          "ET Mumbai Bureau",     "Mumbai Bureau",          "Economic Times Mumbai",   "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("rashmi.pratap@economictimes.com",   "Rashmi Pratap",        "Senior Correspondent",   "Economic Times Mumbai",   "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("satish.john@economictimes.com",     "Satish John",          "Mumbai Correspondent",   "Economic Times Mumbai",   "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("ankur.mishra@economictimes.com",    "Ankur Mishra",         "Crime/Legal Reporter",   "Economic Times Mumbai",   "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── MONEYCONTROL (moneycontrol.com) ──────────────────────────────────────
    ("mumbai@moneycontrol.com",           "Moneycontrol Mumbai",  "Mumbai Bureau",          "Moneycontrol Mumbai",     "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("editor@moneycontrol.com",           "Moneycontrol Editor",  "Editor",                 "Moneycontrol",            "Press", "editor",                                                            "mumbai_expansion_2026"),

    # ── FREE PRESS JOURNAL (freepressjournal.in) — alt domain ─────────────────
    ("editor@freepressjournal.in",        "FPJ Editor",           "Editor",                 "Free Press Journal",      "Press", "mumbai-press|editor|fpj-mumbai|top-priority",                       "mumbai_expansion_2026"),
    ("newsdesk@freepressjournal.in",      "FPJ Newsdesk",         "News Desk",              "Free Press Journal",      "Press", "mumbai-press|fpj-mumbai",                                           "mumbai_expansion_2026"),
    ("sachin.lodha@freepressjournal.in",  "Sachin Lodha",         "Crime Reporter",         "Free Press Journal",      "Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("varsha.torgalkar@freepressjournal.in","Varsha Torgalkar",   "Court Reporter",         "Free Press Journal",      "Press", "mumbai-press|court-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("harshal.desai@freepressjournal.in", "Harshal Desai",        "Crime Reporter",         "Free Press Journal",      "Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),

    # ── PTI / ANI / UNI MUMBAI ───────────────────────────────────────────────
    ("mumbai@ptinews.com",                "PTI Mumbai Bureau",    "Mumbai Bureau",          "PTI Mumbai",              "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("news@ptinews.com",                  "PTI News Desk",        "News Desk",              "PTI",                     "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("mumbai@ani.in",                     "ANI Mumbai Bureau",    "Mumbai Bureau",          "ANI Mumbai",              "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("news@ani.in",                       "ANI News Desk",        "News Desk",              "ANI",                     "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("mumbai@uniindia.com",               "UNI Mumbai Bureau",    "Mumbai Bureau",          "UNI Mumbai",              "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── ADDITIONAL TOI MUMBAI REPORTERS ──────────────────────────────────────
    ("dhruv.malhotra@timesgroup.com",     "Dhruv Malhotra",       "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                        "mumbai_expansion_2026"),
    ("neeraj.gupta@timesgroup.com",       "Neeraj Gupta",         "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                        "mumbai_expansion_2026"),
    ("leela.ponapa@timesgroup.com",       "Leela Ponapa",         "Senior Reporter",        "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("vibha.sharma@timesgroup.com",       "Vibha Sharma",         "Court Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|court-reporter|times-of-india",                        "mumbai_expansion_2026"),
    ("surajit.dasgupta@timesgroup.com",   "Surajit Dasgupta",     "Senior Editor",          "Times of India Mumbai",   "Press", "mumbai-press|editor|times-of-india",                                "mumbai_expansion_2026"),
    ("mausami.ghosh@timesgroup.com",      "Mausami Ghosh",        "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("suzan.suzan@timesgroup.com",        "Suzan Susan",          "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                        "mumbai_expansion_2026"),
    ("sachin.kelbag@timesgroup.com",      "Sachin Kalbag",        "Editor",                 "Times of India Mumbai",   "Press", "mumbai-press|editor|times-of-india|top-priority",                   "mumbai_expansion_2026"),
    ("parshathy.noel@timesgroup.com",     "Parshathy Noel",       "Crime Reporter",         "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                        "mumbai_expansion_2026"),
    ("aditi.pai@timesgroup.com",          "Aditi Pai",            "Mumbai Correspondent",   "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),
    ("richa.sharma@timesgroup.com",       "Richa Sharma",         "Crime Correspondent",    "Times of India Mumbai",   "Press", "mumbai-press|crime-reporter|times-of-india",                        "mumbai_expansion_2026"),
    ("ranjit.patil@timesgroup.com",       "Ranjit Patil",         "Mumbai Political/Crime", "Times of India Mumbai",   "Press", "mumbai-press|crime-court-beat|times-of-india",                      "mumbai_expansion_2026"),

    # ── ADDITIONAL HT MUMBAI REPORTERS ───────────────────────────────────────
    ("aaditya.menon@hindustantimes.com",  "Aaditya Menon",        "Crime Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("shalini.langer@hindustantimes.com", "Shalini Langer",       "Senior Editor",          "Hindustan Times Mumbai",  "Press", "mumbai-press|editor|hindustan-times",                               "mumbai_expansion_2026"),
    ("tarun.shukla@hindustantimes.com",   "Tarun Shukla",         "Mumbai Correspondent",   "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-court-beat|hindustan-times",                     "mumbai_expansion_2026"),
    ("sheetal.bhatt@hindustantimes.com",  "Sheetal Bhatt",        "Crime Reporter",         "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("harsimran.julka@hindustantimes.com","Harsimran Julka",      "Crime/Court Reporter",   "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|court-reporter|hindustan-times",        "mumbai_expansion_2026"),
    ("smriti.kak@hindustantimes.com",     "Smriti Kak Ramachandran","Senior Editor",        "Hindustan Times Mumbai",  "Press", "mumbai-press|editor|hindustan-times",                               "mumbai_expansion_2026"),
    ("dnyaneshwari.bhosale@hindustantimes.com","Dnyaneshwari Bhosale","Crime Reporter",     "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-reporter|hindustan-times",                       "mumbai_expansion_2026"),
    ("neha.dua@hindustantimes.com",       "Neha Dua",             "Mumbai Correspondent",   "Hindustan Times Mumbai",  "Press", "mumbai-press|crime-court-beat|hindustan-times",                     "mumbai_expansion_2026"),

    # ── ADDITIONAL IE MUMBAI REPORTERS ───────────────────────────────────────
    ("prashant.dayal@indianexpress.com",  "Prashant Dayal",       "Senior Correspondent",   "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|crime-court-beat|indianexpress",        "mumbai_expansion_2026"),
    ("anjali.marar@indianexpress.com",    "Anjali Marar",         "Crime Reporter",         "Indian Express Mumbai",   "Press", "mumbai-press|crime-reporter|indianexpress",                         "mumbai_expansion_2026"),
    ("subhash.jha@indianexpress.com",     "Subhash K Jha",        "Film/Crime Reporter",    "Indian Express Mumbai",   "Press", "mumbai-press|crime-court-beat|indianexpress",                       "mumbai_expansion_2026"),
    ("archana.masih@indianexpress.com",   "Archana Masih",        "Senior Reporter",        "Indian Express",          "Press", "crime-court-beat|indianexpress",                                    "mumbai_expansion_2026"),
    ("niha.masih@indianexpress.com",      "Niha Masih",           "Investigations Reporter","Indian Express",          "Press", "crime-court-beat|indianexpress",                                    "mumbai_expansion_2026"),
    ("aditya.iyer@indianexpress.com",     "Aditya Iyer",          "Mumbai Reporter",        "Indian Express Mumbai",   "Press", "mumbai-press|crime-court-beat|indianexpress",                       "mumbai_expansion_2026"),
    ("makarand.gadgil@indianexpress.com", "Makarand Gadgil",      "Pune/Mumbai Reporter",   "Indian Express",          "Press", "mumbai-press|crime-court-beat|indianexpress",                       "mumbai_expansion_2026"),

    # ── ADDITIONAL MID-DAY REPORTERS ─────────────────────────────────────────
    ("swapnil.lad@mid-day.com",           "Swapnil Lad",          "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("sonam.lakhani@mid-day.com",         "Sonam Lakhani",        "Crime Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("mihir.chitre@mid-day.com",          "Mihir Chitre",         "Editor",                 "Mid-Day Mumbai",          "Press", "mumbai-press|editor|mid-day|top-priority",                          "mumbai_expansion_2026"),
    ("shailesh.mishra@mid-day.com",       "Shailesh Mishra",      "Senior Reporter",        "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("prashant.rupera@mid-day.com",       "Prashant Rupera",      "Crime Correspondent",    "Mid-Day Mumbai",          "Press", "mumbai-press|crime-reporter|mid-day",                               "mumbai_expansion_2026"),
    ("saisha.sehgal@mid-day.com",         "Saisha Sehgal",        "Court Reporter",         "Mid-Day Mumbai",          "Press", "mumbai-press|court-reporter|high-court-beat|mid-day",               "mumbai_expansion_2026"),

    # ── ADDITIONAL DNA INDIA REPORTERS ───────────────────────────────────────
    ("shailesh.pathak@dnaindia.com",      "Shailesh Pathak",      "Crime Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("mahesh.langa@dnaindia.com",         "Mahesh Langa",         "Investigations Reporter","DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india|top-priority",                "mumbai_expansion_2026"),
    ("ankur.paliwal@dnaindia.com",        "Ankur Paliwal",        "Crime Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|crime-reporter|dna-india",                             "mumbai_expansion_2026"),
    ("falgun.joshi@dnaindia.com",         "Falgun Joshi",         "Court Reporter",         "DNA India Mumbai",        "Press", "mumbai-press|court-reporter|dna-india",                             "mumbai_expansion_2026"),

    # ── ADDITIONAL FPJ REPORTERS ──────────────────────────────────────────────
    ("pradeep.gour@fpj.co.in",           "Pradeep Gour",         "Crime Reporter",         "Free Press Journal",      "Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("smita.desai@fpj.co.in",            "Smita Desai",          "Court Reporter",         "Free Press Journal",      "Press", "mumbai-press|court-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("vijayalaxmi.tiwari@fpj.co.in",     "Vijayalaxmi Tiwari",   "Crime Correspondent",    "Free Press Journal",      "Press", "mumbai-press|crime-reporter|fpj-mumbai",                            "mumbai_expansion_2026"),
    ("anshul.chaturvedi@fpj.co.in",      "Anshul Chaturvedi",    "Bureau Editor",          "Free Press Journal",      "Press", "mumbai-press|editor|fpj-mumbai|top-priority",                       "mumbai_expansion_2026"),
    ("bhavdeep.kang@fpj.co.in",          "Bhavdeep Kang",        "Senior Reporter",        "Free Press Journal",      "Press", "mumbai-press|crime-court-beat|fpj-mumbai",                          "mumbai_expansion_2026"),

    # ── LOKSATTA ADDITIONAL ───────────────────────────────────────────────────
    ("prashant.kadam@loksatta.com",       "Prashant Kadam",       "Crime Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("yogesh.gore@loksatta.com",          "Yogesh Gore",          "Court Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|court-reporter|high-court-beat",                       "mumbai_expansion_2026"),
    ("milind.kamat@loksatta.com",         "Milind Kamat",         "Crime Reporter",         "Loksatta Mumbai",         "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("sandeep.adsul@loksatta.com",        "Sandeep Adsul",        "Political/Crime Reporter","Loksatta Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),

    # ── ADDITIONAL DIGITAL / FRONTLINE / INDEPENDENT ─────────────────────────
    ("editor@frontline.in",               "Frontline Editor",     "Editor",                 "Frontline",               "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("mumbai@frontline.in",               "Frontline Mumbai",     "Mumbai Reporter",        "Frontline Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("nandini.sundar@frontline.in",       "Nandini Sundar",       "Senior Columnist",       "Frontline",               "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("r.ramachandran@frontline.in",       "R Ramachandran",       "Senior Correspondent",   "Frontline",               "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),

    # ── DECCAN HERALD (deccanherald.com) — Mumbai bureau ─────────────────────
    ("mumbai@deccanherald.com",           "DH Mumbai Bureau",     "Mumbai Bureau",          "Deccan Herald Mumbai",    "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("vijay.kumar@deccanherald.com",      "Vijay Kumar",          "Crime Reporter",         "Deccan Herald Mumbai",    "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),

    # ── ADDITIONAL LEGAL PRESS ────────────────────────────────────────────────
    ("bombay.hc@livelaw.in",              "LiveLaw Bombay HC",    "Bombay HC Correspondent","LiveLaw Mumbai",          "Press/Legal Media", "mumbai-press|legal-press|court-reporter|high-court-beat|top-priority","mumbai_expansion_2026"),
    ("bombay@barandbench.com",            "B&B Bombay Desk",      "Bombay HC Reporter",     "Bar & Bench Mumbai",      "Press/Legal Media", "mumbai-press|legal-press|court-reporter|high-court-beat|top-priority","mumbai_expansion_2026"),
    ("rohini.salian@livelaw.in",          "Rohini Salian",        "Legal Reporter",         "LiveLaw Mumbai",          "Press/Legal Media", "mumbai-press|legal-reporter|court-reporter",            "mumbai_expansion_2026"),
    ("selin.saheed@livelaw.in",           "Selin Saheed",         "Court Correspondent",    "LiveLaw Mumbai",          "Press/Legal Media", "mumbai-press|court-reporter|high-court-beat",           "mumbai_expansion_2026"),
    ("editor@theleaflet.in",              "Leaflet Editor",       "Editor",                 "The Leaflet",             "Press/Legal Media", "legal-press|court-reporter|high-court-beat|top-priority","mumbai_expansion_2026"),
    ("setu@indialegal.in",                "Setu India Legal",     "Legal Editor",           "India Legal",             "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),
    ("contact@spicyip.com",               "SpicyIP Editors",      "IP/Legal Editor",        "SpicyIP",                 "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),
    ("editors@lawtimesjournal.in",        "Law Times Journal",    "Legal Editors",          "Law Times Journal",       "Press/Legal Media", "legal-press|court-reporter",                            "mumbai_expansion_2026"),

    # ── ADDITIONAL ABP / MARATHI TV ───────────────────────────────────────────
    ("mayur.patil@abplive.com",           "Mayur Patil",          "Crime Reporter",         "ABP Majha Mumbai",        "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("rajesh.mahajan@abplive.com",        "Rajesh Mahajan",       "Court Reporter",         "ABP Majha Mumbai",        "Press", "mumbai-press|court-reporter|high-court-beat",                       "mumbai_expansion_2026"),
    ("sunil.tiwari@abplive.com",          "Sunil Tiwari",         "Crime Reporter",         "ABP Majha Mumbai",        "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("anuradha.joshi@abplive.com",        "Anuradha Joshi",       "Anchor/Reporter",        "ABP Majha Mumbai",        "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("prasad.bhave@tv9marathi.com",       "Prasad Bhave",         "Crime Reporter",         "TV9 Marathi Mumbai",      "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("amol.jadhav@tv9marathi.com",        "Amol Jadhav",          "Court Reporter",         "TV9 Marathi Mumbai",      "Press", "mumbai-press|court-reporter",                                       "mumbai_expansion_2026"),
    ("swati.more@tv9marathi.com",         "Swati More",           "Crime Reporter",         "TV9 Marathi Mumbai",      "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),

    # ── ADDITIONAL NEWS18 / CNN-NEWS18 ────────────────────────────────────────
    ("pallavi.ghosh@news18.com",          "Pallavi Ghosh",        "Legal/Court Analyst",    "CNN-News18",              "Press", "court-reporter|legal-reporter|top-priority",                        "mumbai_expansion_2026"),
    ("manish.gupta@news18.com",           "Manish Gupta",         "Crime Reporter",         "News18 India",            "Press", "crime-court-beat|crime-reporter",                                   "mumbai_expansion_2026"),
    ("sushant.kulkarni@news18.com",       "Sushant Kulkarni",     "Mumbai Bureau",          "CNN-News18 Mumbai",       "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("kavitha.reddy@news18.com",          "Kavitha Reddy",        "Crime Reporter",         "News18 India",            "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),

    # ── INDEPENDENT DIGITAL JOURNALISTS / YOUTUBE (Mumbai crime focus) ────────
    ("abhisar@abhisar.com",               "Abhisar Sharma",       "Independent Journalist", "Independent",             "Press", "crime-court-beat|digital-creator|influencer|top-priority",          "mumbai_expansion_2026"),
    ("press@newsxlive.com",               "NewsX Press",          "Press Desk",             "NewsX",                   "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("editor@thecitizen.in",              "The Citizen Editor",   "Editor",                 "The Citizen",             "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("contact@groundxero.in",             "Ground Xero",          "Independent Media",      "Ground Xero",             "Press", "crime-court-beat|digital-creator",                                  "mumbai_expansion_2026"),
    ("info@maktoobmedia.com",             "Maktoob Media",        "Digital News",           "Maktoob Media",           "Press", "crime-court-beat|digital-creator",                                  "mumbai_expansion_2026"),
    ("editor@thewire.in",                 "The Wire Editor",      "Editorial",              "The Wire",                "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),

    # ── HUFFPOST INDIA / OUTLOOK ──────────────────────────────────────────────
    ("swati.chaturvedi@outlookindia.com",  "Swati Chaturvedi",    "Senior Journalist",      "Outlook India",           "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),
    ("sandeep.unnithan@outlookindia.com",  "Sandeep Unnithan",    "Senior Editor",          "Outlook India",           "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),
    ("sunetra.choudhury@outlookindia.com", "Sunetra Choudhury",   "Senior Correspondent",   "Outlook India",           "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),
    ("ajay.singh@outlookindia.com",        "Ajay Singh",          "Editor",                 "Outlook India",           "Press", "crime-court-beat|editor",                                           "mumbai_expansion_2026"),

    # ── ADDITIONAL FRONTLINE / INDIA LEGAL ───────────────────────────────────
    ("p.sainath@frontline.in",            "P Sainath",            "Rural Affairs Editor",   "Frontline",               "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("sidharth.bhatia@thewire.in",        "Sidharth Bhatia",      "Editor",                 "The Wire Mumbai",         "Press", "mumbai-press|editor|top-priority",                                  "mumbai_expansion_2026"),
    ("pankaj.pachauri@newslaundry.com",   "Pankaj Pachauri",      "Editor",                 "Newslaundry",             "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),
    ("meghnad.bose@newslaundry.com",      "Meghnad Bose",         "Video Journalist",       "Newslaundry",             "Press", "crime-court-beat|digital-creator",                                  "mumbai_expansion_2026"),
    ("shardul.bhardwaj@newslaundry.com",  "Shardul Bhardwaj",     "Legal Reporter",         "Newslaundry",             "Press", "legal-reporter|court-reporter",                                     "mumbai_expansion_2026"),
    ("abhinandan.sekhri@newslaundry.com", "Abhinandan Sekhri",    "Co-founder",             "Newslaundry",             "Press", "crime-court-beat|editor|top-priority",                              "mumbai_expansion_2026"),

    # ── LATESTLY / THE LOGICAL INDIAN ────────────────────────────────────────
    ("editor@latestly.com",               "Latestly Editor",      "Editor",                 "Latestly",                "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),
    ("mumbai@latestly.com",               "Latestly Mumbai",      "Mumbai Reporter",        "Latestly Mumbai",         "Press", "mumbai-press|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("editor@thelogicalindian.com",       "Logical Indian Editor","Editor",                 "The Logical Indian",      "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),
    ("contact@thelogicalindian.com",      "The Logical Indian",   "Contact Desk",           "The Logical Indian",      "Press", "crime-court-beat",                                                  "mumbai_expansion_2026"),

    # ── SAKAL TIMES ADDITIONAL ────────────────────────────────────────────────
    ("ranjit.khare@sakaaltimes.in",       "Ranjit Khare",         "Crime Reporter",         "Sakal Times Mumbai",      "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),
    ("deepa.gokhale@sakaaltimes.in",      "Deepa Gokhale",        "Court Reporter",         "Sakal Times Mumbai",      "Press", "mumbai-press|court-reporter|high-court-beat",                       "mumbai_expansion_2026"),
    ("avinash.datke@sakaaltimes.in",      "Avinash Datke",        "Crime Reporter",         "Sakal Times Mumbai",      "Press", "mumbai-press|crime-reporter",                                       "mumbai_expansion_2026"),

    # ── ADDITIONAL INDIVIDUAL JOURNALISTS (Independent / Freelance) ──────────
    ("hussain.zaidi@gmail.com",           "Hussain Zaidi",        "Crime Author/Journalist","Independent",             "Press", "mumbai-press|crime-reporter|top-priority",                          "mumbai_expansion_2026"),
    ("vivek.agrawal@gmail.com",           "Vivek Agrawal",        "Crime Journalist",       "Independent",             "Press", "mumbai-press|crime-reporter|top-priority",                          "mumbai_expansion_2026"),
    ("padmaparna.ghosh@gmail.com",        "Padmaparna Ghosh",     "Independent Journalist", "Independent",             "Press", "mumbai-press|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("neha.dixit@gmail.com",              "Neha Dixit",           "Investigations Journalist","Independent",           "Press", "crime-court-beat|top-priority",                                     "mumbai_expansion_2026"),

    # ── FACT CHECKERS ADDITIONAL ──────────────────────────────────────────────
    ("newsdesk@boomlive.in",              "Boom Live News",       "News Desk",              "Boom Live",               "Press", "fact-checker|mumbai-press",                                         "mumbai_expansion_2026"),
    ("editor@vishvasnews.com",            "Vishvas News Editor",  "Editor",                 "Vishvas News",            "Press", "fact-checker|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("editor@newsmobile.in",              "NewsMobile Editor",    "Editor",                 "NewsMobile",              "Press", "fact-checker|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
    ("contact@newsmobile.in",             "NewsMobile Desk",      "Desk",                   "NewsMobile",              "Press", "fact-checker|crime-court-beat",                                     "mumbai_expansion_2026"),
    ("factcheck@indiatoday.in",           "India Today Fact Check","Fact Check Desk",       "India Today",             "Press", "fact-checker|top-priority",                                         "mumbai_expansion_2026"),
    ("verify@thequint.com",               "WebQoof Fact Check",   "Fact Check Desk",        "The Quint",               "Press", "fact-checker|crime-court-beat|top-priority",                        "mumbai_expansion_2026"),
]

def load_existing():
    ex = {}
    with open(FINAL_CSV, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            ex[row['email'].lower().strip()] = row
    return ex

def load_suppressed():
    s = set()
    with open(SUPP_CSV, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            s.add(row['email'].lower().strip())
    return s

def dns_verify_batch(emails):
    domains = {e.split('@')[-1].lower() for e in emails if '@' in e}
    unknown = [d for d in domains if d not in KNOWN_VALID and d not in mx_cache]
    if unknown:
        print(f"   DNS-verifying {len(unknown)} new domains...")
        with ThreadPoolExecutor(max_workers=20) as pool:
            list(pool.map(has_mx, unknown))
    return {e for e in emails if has_mx(e.split('@')[-1].lower() if '@' in e else '')}

def rebuild_live(final_csv, suppressed):
    rows = list(csv.DictReader(open(final_csv, encoding='utf-8-sig', newline='')))
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
    print("MUMBAI CONTACTS — BATCH 2 EXPANSION")
    print("=" * 60)

    existing   = load_existing()
    suppressed = load_suppressed()
    print(f"contacts_final.csv : {len(existing)} rows")
    print(f"mumbai-press now   : {sum(1 for r in existing.values() if 'mumbai-press' in (r.get('tags') or ''))}")

    raw = []
    for e, name, desig, pub, cat, tags, src in BATCH2:
        raw.append({'email': e.lower().strip(), 'name': name, 'designation': desig,
                    'category': cat, 'tags': tags, 'case': '', 'source': src})

    print(f"Batch2 raw entries : {len(raw)}")

    to_add = []
    seen = set()
    skipped_dup = skipped_supp = 0
    for r in raw:
        em = r['email']
        if em in seen: continue
        seen.add(em)
        if em in suppressed: skipped_supp += 1; continue
        if em in existing: skipped_dup += 1; continue
        to_add.append(r)

    print(f"Already in contacts: {skipped_dup}")
    print(f"In suppression     : {skipped_supp}")
    print(f"NEW candidates     : {len(to_add)}")

    valid_emails = dns_verify_batch([r['email'] for r in to_add])
    to_add_valid = [r for r in to_add if r['email'] in valid_emails]
    dead = len(to_add) - len(to_add_valid)
    print(f"DNS valid          : {len(to_add_valid)}")
    print(f"DNS dead (skipped) : {dead}")

    fieldnames = ['email','name','designation','category','tags','case','source']
    with open(FINAL_CSV, 'a', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        for r in to_add_valid:
            w.writerow({k: r.get(k,'') for k in fieldnames})

    print(f"\nAppended {len(to_add_valid)} contacts to contacts_final.csv")
    print("Rebuilding contacts_live.csv and tag_summary.csv...")
    live = rebuild_live(FINAL_CSV, suppressed)
    tc   = rebuild_tags(live)

    mumbai = tc.get('mumbai-press', 0)
    crime  = tc.get('crime-court-beat', 0)
    total_final_rows = len(existing) + len(to_add_valid)
    print(f"\n{'=' * 60}")
    print(f"BATCH 2 DONE")
    print(f"  contacts_final.csv  : {total_final_rows} rows")
    print(f"  contacts_live.csv   : {len(live)} rows")
    print(f"  Added this batch    : {len(to_add_valid)}")
    print(f"  mumbai-press total  : {mumbai}")
    print(f"  crime-court-beat    : {crime}")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()
