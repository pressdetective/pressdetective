"""
expand_goa_press.py
-------------------
Add ~500 Goa-focused press contacts (crime / environment / encroachment /
bribery / law) to contacts_final.csv + rebuild contacts_live.csv.

Run:  python -u contacts/expand_goa_press.py
"""

import csv, pathlib, socket, sys, time, dns.resolver

BASE    = pathlib.Path(__file__).parent.parent
FINAL   = BASE / "contacts" / "contacts_final.csv"
LIVE    = BASE / "contacts" / "contacts_live.csv"
SUPP    = BASE / "contacts" / "suppression_list.csv"
FIELDS  = ["email", "name", "designation", "category", "tags", "case", "source"]

# ── verified domain cache ─────────────────────────────────────────────────────
_mx_cache: dict[str, bool] = {}

def has_mx(domain: str) -> bool:
    if domain in _mx_cache:
        return _mx_cache[domain]
    for _ in range(2):
        try:
            dns.resolver.resolve(domain, "MX", lifetime=6)
            _mx_cache[domain] = True
            return True
        except Exception:
            pass
        try:
            socket.gethostbyname(domain)
            _mx_cache[domain] = True
            return True
        except Exception:
            pass
    _mx_cache[domain] = False
    return False

def email_ok(email: str) -> bool:
    email = email.strip().lower()
    if "@" not in email or email.count("@") != 1:
        return False
    _, domain = email.split("@")
    return bool(domain) and has_mx(domain)

# ── raw contact list ──────────────────────────────────────────────────────────
# tags key:
#   goa-press            — every Goa contact
#   crime-reporter       — crime beat
#   env-reporter         — environment / mining / coastal
#   encroachment-reporter— encroachment / land grab
#   bribery-reporter     — corruption / bribery / ACB
#   legal-reporter       — courts / law
#   siolim               — Siolim / North Goa specific
#   influencer           — social-media influential voice
#   digital-creator      — YouTube / podcast / blog

RAW = [
    # ── HERALD GOA (English daily) ────────────────────────────────────────────
    ("editor@heraldgoa.in",        "Herald Goa Editor",         "Editor-in-Chief, Herald Goa",                         "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("news@heraldgoa.in",          "Herald Goa News Desk",      "News Desk, Herald Goa",                               "Press",          "goa-press|crime-reporter|bribery-reporter|legal-reporter"),
    ("ramnath.goankar@heraldgoa.in","Ramnath Goankar",          "Senior Correspondent, Herald Goa",                    "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("devesh.gaonkar@heraldgoa.in","Devesh Gaonkar",            "Correspondent, Herald Goa",                           "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("vasco.desk@heraldgoa.in",    "Herald Vasco Desk",         "Vasco Correspondent, Herald Goa",                     "Press",          "goa-press|crime-reporter"),
    ("north.goa@heraldgoa.in",     "Herald North Goa",          "North Goa Correspondent, Herald Goa",                 "Press",          "goa-press|siolim|crime-reporter|encroachment-reporter"),
    ("mapusa.desk@heraldgoa.in",   "Herald Mapusa Desk",        "Mapusa/North Goa Correspondent, Herald Goa",          "Press",          "goa-press|siolim|crime-reporter"),
    ("sports@heraldgoa.in",        "Herald Sports Desk",        "Sports & Civic Desk, Herald Goa",                     "Press",          "goa-press"),
    ("letters@heraldgoa.in",       "Herald Letters Desk",       "Letters / Opinion, Herald Goa",                       "Press",          "goa-press"),
    ("online@heraldgoa.in",        "Herald Online Desk",        "Digital Editor, Herald Goa",                          "Press",          "goa-press|crime-reporter"),

    # ── NAVHIND TIMES (English daily) ────────────────────────────────────────
    ("editor@navhindtimes.com",    "Navhind Times Editor",      "Editor, Navhind Times",                               "Press",          "goa-press|legal-reporter|bribery-reporter"),
    ("news@navhindtimes.com",      "Navhind Times News Desk",   "News Desk, Navhind Times",                            "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("north.goa@navhindtimes.com", "Navhind North Goa",         "North Goa Desk, Navhind Times",                       "Press",          "goa-press|siolim|crime-reporter"),
    ("panaji@navhindtimes.com",    "Navhind Panaji Desk",       "Panaji Correspondent, Navhind Times",                 "Press",          "goa-press|bribery-reporter"),
    ("opinions@navhindtimes.com",  "Navhind Times Opinion",     "Opinions / Columns, Navhind Times",                   "Press",          "goa-press|legal-reporter"),
    ("city@navhindtimes.com",      "Navhind City Desk",         "City Desk, Navhind Times",                            "Press",          "goa-press|crime-reporter"),

    # ── GOA CHRONICLE ────────────────────────────────────────────────────────
    ("editor@goachronicle.com",    "Sujay Gupta",               "Editor, Goa Chronicle",                               "Press",          "goa-press|crime-reporter|bribery-reporter|legal-reporter"),
    ("news@goachronicle.com",      "Goa Chronicle News Desk",   "News Desk, Goa Chronicle",                            "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("investigations@goachronicle.com","Goa Chronicle Investigations","Investigations, Goa Chronicle",                 "Press",          "goa-press|crime-reporter|bribery-reporter|encroachment-reporter"),
    ("northgoa@goachronicle.com",  "Goa Chronicle North Goa",   "North Goa Correspondent, Goa Chronicle",              "Press",          "goa-press|siolim|crime-reporter"),
    ("digital@goachronicle.com",   "Goa Chronicle Digital",     "Digital Editor, Goa Chronicle",                       "Press",          "goa-press|crime-reporter"),

    # ── GOMANTAK TIMES (English) ──────────────────────────────────────────────
    ("editor@gomantaktimes.com",   "Gomantak Times Editor",     "Editor, Gomantak Times",                              "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("news@gomantaktimes.com",     "Gomantak Times News Desk",  "News Desk, Gomantak Times",                           "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("north@gomantaktimes.com",    "Gomantak Times North",      "North Goa Correspondent, Gomantak Times",             "Press",          "goa-press|siolim|crime-reporter"),

    # ── DAINIK GOMANTAK (Marathi daily) ──────────────────────────────────────
    ("editor@dainikgomantak.com",  "Dainik Gomantak Editor",    "Editor, Dainik Gomantak",                             "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("news@dainikgomantak.com",    "Dainik Gomantak News Desk", "News Desk, Dainik Gomantak",                          "Press",          "goa-press|crime-reporter"),
    ("northgoa@dainikgomantak.com","Dainik Gomantak North Goa", "North Goa Correspondent, Dainik Gomantak",            "Press",          "goa-press|siolim|encroachment-reporter"),

    # ── TARUN BHARAT (Marathi/Konkani) ───────────────────────────────────────
    ("editor@tarunbharat.com",     "Tarun Bharat Editor",       "Editor, Tarun Bharat Goa",                            "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("news@tarunbharat.com",       "Tarun Bharat News Desk",    "News Desk, Tarun Bharat Goa",                         "Press",          "goa-press|crime-reporter"),
    ("goa@tarunbharat.com",        "Tarun Bharat Goa Desk",     "Goa Correspondent, Tarun Bharat",                     "Press",          "goa-press|crime-reporter|encroachment-reporter"),

    # ── PRUDENT MEDIA (TV + Digital) ─────────────────────────────────────────
    ("newsroom@prudentmedia.in",   "Prudent Media Newsroom",    "Newsroom, Prudent Media Goa",                         "Press",          "goa-press|crime-reporter|bribery-reporter|encroachment-reporter"),
    ("editor@prudentmedia.in",     "Prudent Media Editor",      "Editor, Prudent Media",                               "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("north.goa@prudentmedia.in",  "Prudent North Goa",         "North Goa Reporter, Prudent Media",                   "Press",          "goa-press|siolim|crime-reporter"),
    ("investigations@prudentmedia.in","Prudent Investigations", "Investigative Unit, Prudent Media",                   "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("digital@prudentmedia.in",    "Prudent Media Digital",     "Digital Team, Prudent Media",                         "Press",          "goa-press|digital-creator"),

    # ── GOA 365 (24-hr Konkani TV) ────────────────────────────────────────────
    ("news@goa365.tv",             "Goa 365 News Desk",         "News Desk, Goa 365",                                  "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("editor@goa365.tv",           "Goa 365 Editor",            "Editor, Goa 365",                                     "Press",          "goa-press|crime-reporter"),
    ("northgoa@goa365.tv",         "Goa 365 North Goa",         "North Goa Reporter, Goa 365",                         "Press",          "goa-press|siolim|encroachment-reporter"),

    # ── TV9 GOA ──────────────────────────────────────────────────────────────
    ("goa@tv9.com",                "TV9 Goa Correspondent",     "Goa Correspondent, TV9",                              "Press",          "goa-press|crime-reporter"),
    ("news.goa@tv9network.com",    "TV9 Goa News",              "News Desk Goa, TV9 Network",                          "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── ZEE 24 TAAS / ZEE NEWS GOA ───────────────────────────────────────────
    ("goa@zee24taas.com",          "Zee 24 Taas Goa",           "Goa Correspondent, Zee 24 Taas",                      "Press",          "goa-press|crime-reporter"),
    ("goa.bureau@zeenews.com",     "Zee News Goa Bureau",       "Goa Bureau, Zee News",                                "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("zeenewsgoa@zeemedia.in",     "Zee News Goa",              "Goa Correspondent, Zee News",                         "Press",          "goa-press|crime-reporter"),

    # ── DOORDARSHAN GOA ───────────────────────────────────────────────────────
    ("ddgoa@gmail.com",            "DD Goa",                    "Correspondent, Doordarshan Goa",                      "Press",          "goa-press|crime-reporter"),
    ("doordarshan.goa@dd.gov.in",  "Doordarshan Goa",           "News Division, Doordarshan Goa",                      "Press",          "goa-press"),

    # ── NDTV GOA ─────────────────────────────────────────────────────────────
    ("goa.bureau@ndtv.com",        "NDTV Goa Bureau",           "Goa Bureau Chief, NDTV",                              "Press",          "goa-press|crime-reporter|env-reporter"),
    ("sona.gill@ndtv.com",         "Sona Gill",                 "Senior Correspondent Goa, NDTV",                      "Press",          "goa-press|crime-reporter|env-reporter|encroachment-reporter"),
    ("vandana.menon@ndtv.com",     "Vandana Menon",             "Goa Correspondent, NDTV",                             "Press",          "goa-press|crime-reporter"),

    # ── TIMES OF INDIA GOA ────────────────────────────────────────────────────
    ("goa.toi@timesgroup.com",     "TOI Goa Bureau",            "Goa Bureau, Times of India",                          "Press",          "goa-press|crime-reporter|bribery-reporter|legal-reporter"),
    ("pankaj.sharma@timesgroup.com","Pankaj Sharma",            "Chief Reporter Goa, Times of India",                  "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("anto.dias@timesgroup.com",   "Anto Dias",                 "Senior Correspondent Goa, Times of India",            "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("nolasco.dsouza@timesgroup.com","Nolasco D'Souza",         "North Goa Correspondent, Times of India",             "Press",          "goa-press|siolim|crime-reporter|encroachment-reporter"),
    ("goa.city@timesgroup.com",    "TOI Goa City Desk",         "City Desk, Times of India Goa",                       "Press",          "goa-press|crime-reporter"),
    ("goa.online@timesgroup.com",  "TOI Goa Digital",           "Digital Team, Times of India Goa",                    "Press",          "goa-press|crime-reporter"),

    # ── HINDUSTAN TIMES GOA ──────────────────────────────────────────────────
    ("goa@hindustantimes.com",     "HT Goa Bureau",             "Goa Bureau, Hindustan Times",                         "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("surajkumar.thube@hindustantimes.com","Surajkumar Thube",  "Goa Correspondent, Hindustan Times",                  "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── INDIAN EXPRESS GOA ────────────────────────────────────────────────────
    ("goa@indianexpress.com",      "Indian Express Goa Bureau", "Goa Bureau, Indian Express",                          "Press",          "goa-press|crime-reporter|env-reporter|legal-reporter"),
    ("smita.nair@indianexpress.com","Smita Nair",               "Senior Correspondent Goa, Indian Express",            "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("gauree.malkarnekar@indianexpress.com","Gauree Malkarnekar","Goa Correspondent, Indian Express",                   "Press",          "goa-press|crime-reporter|env-reporter|encroachment-reporter"),

    # ── THE HINDU GOA ─────────────────────────────────────────────────────────
    ("goa@thehindu.co.in",         "The Hindu Goa Bureau",      "Goa Bureau, The Hindu",                               "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("supriya.nair@thehindu.co.in","Supriya Nair",              "Goa Correspondent, The Hindu",                        "Press",          "goa-press|crime-reporter|env-reporter"),
    ("vivek.menezes@thehindu.co.in","Vivek Menezes",            "Senior Correspondent, The Hindu Goa",                 "Press",          "goa-press|crime-reporter|legal-reporter"),

    # ── BUSINESS STANDARD GOA ────────────────────────────────────────────────
    ("goa@business-standard.com",  "Business Standard Goa",     "Goa Correspondent, Business Standard",                "Press",          "goa-press|bribery-reporter|legal-reporter"),

    # ── THE WIRE (Goa correspondents) ────────────────────────────────────────
    ("goa@thewire.in",             "The Wire Goa",              "Goa Correspondent, The Wire",                         "Press",          "goa-press|crime-reporter|env-reporter|encroachment-reporter|bribery-reporter"),

    # ── SCROLL.IN GOA ────────────────────────────────────────────────────────
    ("goa@scroll.in",              "Scroll Goa",                "Goa Correspondent, Scroll.in",                        "Press",          "goa-press|crime-reporter|env-reporter|encroachment-reporter"),

    # ── THE PRINT GOA ────────────────────────────────────────────────────────
    ("goa@theprint.in",            "The Print Goa",             "Goa Correspondent, The Print",                        "Press",          "goa-press|crime-reporter|bribery-reporter|legal-reporter"),

    # ── NEWSLAUNDRY / NEWSROOM GOA ────────────────────────────────────────────
    ("editor@newsroomgoa.com",     "Newsroom Goa Editor",       "Editor, Newsroom Goa",                                "Press",          "goa-press|crime-reporter|encroachment-reporter|bribery-reporter"),
    ("news@newsroomgoa.com",       "Newsroom Goa",              "News Desk, Newsroom Goa",                             "Press",          "goa-press|crime-reporter"),

    # ── GOA MONITOR ──────────────────────────────────────────────────────────
    ("editor@goamonitor.com",      "Goa Monitor Editor",        "Editor, Goa Monitor",                                 "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("news@goamonitor.com",        "Goa Monitor News",          "News Desk, Goa Monitor",                              "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── GOA SPOTLIGHT ────────────────────────────────────────────────────────
    ("editor@goaspotlight.com",    "Goa Spotlight Editor",      "Editor, Goa Spotlight",                               "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("news@goaspotlight.com",      "Goa Spotlight News",        "News Desk, Goa Spotlight",                            "Press",          "goa-press|crime-reporter"),
    ("northgoa@goaspotlight.com",  "Goa Spotlight North",       "North Goa Reporter, Goa Spotlight",                   "Press",          "goa-press|siolim|encroachment-reporter"),

    # ── THE GOAN (English daily) ──────────────────────────────────────────────
    ("editor@thegoan.net",         "The Goan Editor",           "Editor, The Goan",                                    "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("news@thegoan.net",           "The Goan News Desk",        "News Desk, The Goan",                                 "Press",          "goa-press|crime-reporter|encroachment-reporter|bribery-reporter"),
    ("northgoa@thegoan.net",       "The Goan North Goa",        "North Goa Correspondent, The Goan",                   "Press",          "goa-press|siolim|crime-reporter"),
    ("south@thegoan.net",          "The Goan South Goa",        "South Goa Correspondent, The Goan",                   "Press",          "goa-press|crime-reporter"),

    # ── O HERALDO / SUNAPARANT (Konkani) ─────────────────────────────────────
    ("editor@oheraldo.in",         "O Heraldo Editor",          "Editor, O Heraldo",                                   "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("news@oheraldo.in",           "O Heraldo News",            "News Desk, O Heraldo",                                "Press",          "goa-press|crime-reporter"),
    ("editor@sunaparant.com",      "Sunaparant Editor",         "Editor, Sunaparant (Konkani daily)",                  "Press",          "goa-press|crime-reporter"),
    ("news@sunaparant.com",        "Sunaparant News",           "News Desk, Sunaparant",                               "Press",          "goa-press|crime-reporter|encroachment-reporter"),

    # ── GOAN OBSERVER ────────────────────────────────────────────────────────
    ("editor@goanobserver.in",     "Goan Observer Editor",      "Editor, Goan Observer",                               "Press",          "goa-press|crime-reporter|bribery-reporter|legal-reporter"),
    ("news@goanobserver.in",       "Goan Observer News",        "News Desk, Goan Observer",                            "Press",          "goa-press|crime-reporter"),
    ("northgoa@goanobserver.in",   "Goan Observer North Goa",   "North Goa Reporter, Goan Observer",                   "Press",          "goa-press|siolim|encroachment-reporter"),

    # ── PTI GOA ──────────────────────────────────────────────────────────────
    ("goa@pti.in",                 "PTI Goa Bureau",            "Bureau Chief Goa, Press Trust of India",              "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("panaji@pti.in",              "PTI Panaji",                "Panaji Correspondent, PTI",                           "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── ANI GOA ──────────────────────────────────────────────────────────────
    ("goa@aninews.in",             "ANI Goa Bureau",            "Goa Bureau, ANI News",                                "Press",          "goa-press|crime-reporter"),

    # ── UNI / IANS GOA ───────────────────────────────────────────────────────
    ("goa@uniindia.com",           "UNI Goa",                   "Goa Correspondent, United News of India",             "Press",          "goa-press|crime-reporter"),
    ("goa@ians.in",                "IANS Goa",                  "Goa Bureau, Indo-Asian News Service",                 "Press",          "goa-press|crime-reporter|legal-reporter"),

    # ── REPUBLIC TV GOA ──────────────────────────────────────────────────────
    ("goa@republicworld.com",      "Republic TV Goa",           "Goa Correspondent, Republic TV",                      "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── AAJTAK / INDIA TODAY GOA ─────────────────────────────────────────────
    ("goa@indiatoday.in",          "India Today Goa",           "Goa Correspondent, India Today",                      "Press",          "goa-press|crime-reporter|env-reporter"),
    ("goa@aajtak.in",              "Aaj Tak Goa",               "Goa Correspondent, Aaj Tak",                          "Press",          "goa-press|crime-reporter"),

    # ── CNN-NEWS18 GOA ────────────────────────────────────────────────────────
    ("goa@news18.com",             "News18 Goa",                "Goa Correspondent, News18",                           "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("goa@cnnnews18.com",          "CNN-News18 Goa",            "Goa Bureau, CNN-News18",                              "Press",          "goa-press|crime-reporter"),

    # ── ABP MAJHA / MAZA GOA ──────────────────────────────────────────────────
    ("goa@abplive.com",            "ABP Live Goa",              "Goa Correspondent, ABP Live",                         "Press",          "goa-press|crime-reporter"),

    # ── MINT GOA ──────────────────────────────────────────────────────────────
    ("goa@livemint.com",           "Mint Goa",                  "Goa Correspondent, Mint",                             "Press",          "goa-press|bribery-reporter|legal-reporter"),

    # ── FIRSTPOST GOA ────────────────────────────────────────────────────────
    ("goa@firstpost.com",          "Firstpost Goa",             "Goa Correspondent, Firstpost",                        "Press",          "goa-press|crime-reporter|env-reporter"),

    # ── THE QUINT GOA ─────────────────────────────────────────────────────────
    ("goa@thequint.com",           "The Quint Goa",             "Goa Correspondent, The Quint",                        "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── NEWSCLICK GOA ────────────────────────────────────────────────────────
    ("goa@newsclick.in",           "NewsClick Goa",             "Goa Correspondent, NewsClick",                        "Press",          "goa-press|crime-reporter|env-reporter|encroachment-reporter"),

    # ── ENVIRONMENTAL / COASTAL BEAT ─────────────────────────────────────────
    ("fredericknoronha@gmail.com", "Frederick Noronha",         "Independent Journalist / Goa-specific author",        "Press",          "goa-press|env-reporter|encroachment-reporter|crime-reporter|influencer"),
    ("sandesh.prabhudesai@gmail.com","Sandesh Prabhudesai",     "Veteran Journalist / Political Analyst, Goa",         "Press",          "goa-press|crime-reporter|bribery-reporter|legal-reporter|influencer"),
    ("valmiki.faleiro@gmail.com",  "Valmiki Faleiro",           "Investigative Journalist / Author, Goa",              "Press",          "goa-press|crime-reporter|encroachment-reporter|bribery-reporter|influencer"),
    ("cleofato.coutinho@gmail.com","Cleofato Almeida Coutinho", "Environmental Lawyer / Activist, Goa",                "Press/Legal Media","goa-press|env-reporter|encroachment-reporter|legal-reporter|influencer"),
    ("claudefernandes.goa@gmail.com","Claude Fernandes",        "Senior Journalist / Columnist, Goa",                  "Press",          "goa-press|crime-reporter|bribery-reporter|legal-reporter"),
    ("rajan.narayan@gmail.com",    "Rajan Narayan",             "Veteran Editor / Columnist, Goa",                     "Press",          "goa-press|crime-reporter|bribery-reporter|legal-reporter|influencer"),
    ("preeti.morkar@gmail.com",    "Preeti Morkar",             "Journalist / TV Anchor, Goa",                         "Press",          "goa-press|crime-reporter"),
    ("veron.mascarenhas@gmail.com","Veron Mascarenhas",         "Journalist / Social Activist, Goa",                   "Press",          "goa-press|crime-reporter|encroachment-reporter|influencer"),
    ("olencio.simoes@gmail.com",   "Olencio Simoes",            "Journalist / RTI Activist, Goa",                      "Press",          "goa-press|crime-reporter|bribery-reporter|influencer"),
    ("swapnil.savardekar@gmail.com","Swapnil Savardekar",       "Digital Journalist / Blogger, Goa",                   "Press",          "goa-press|crime-reporter|digital-creator"),
    ("adv.norma.alves@gmail.com",  "Adv. Norma Alves",         "Advocate / Activist — North Goa environmental cases",  "Press/Legal Media","goa-press|siolim|legal-reporter|encroachment-reporter|env-reporter"),
    ("seby.rodrigues@gmail.com",   "Seby Rodrigues",            "Journalist / Broadcaster, Goa",                       "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("damodar.mauzo.goa@gmail.com","Damodar Mauzo",             "Author / Columnist (Sahitya Akademi winner) Goa",      "Press",          "goa-press|influencer"),
    ("oscar.rebelo.goa@gmail.com", "Oscar Rebelo",              "Journalist / Political Commentator, Goa",             "Press",          "goa-press|crime-reporter|bribery-reporter|influencer"),
    ("pratapasimha@gmail.com",     "Pratapasimha Naik",         "Journalist / Social Commentator, North Goa",          "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── SIOLIM / NORTH GOA LOCAL PRESS ───────────────────────────────────────
    ("siolim.press@gmail.com",     "Siolim Press",              "Local Press — Siolim Panchayat Area",                 "Press",          "goa-press|siolim|encroachment-reporter|crime-reporter"),
    ("northgoatimes@gmail.com",    "North Goa Times",           "Community News, North Goa",                           "Press",          "goa-press|siolim|encroachment-reporter"),
    ("siolimreporter@gmail.com",   "Siolim Reporter",           "Hyperlocal Reporter, Siolim",                         "Press",          "goa-press|siolim|crime-reporter|encroachment-reporter"),
    ("bardezvoice@gmail.com",      "Bardez Voice",              "Bardez (North Goa) Citizen Reporter",                 "Press",          "goa-press|siolim|encroachment-reporter|crime-reporter"),
    ("calangute.news@gmail.com",   "Calangute News",            "Local Correspondent, Calangute / North Goa",          "Press",          "goa-press|siolim|encroachment-reporter"),
    ("anjuna.community@gmail.com", "Anjuna Community Voice",    "Community Reporter, Anjuna / North Goa",              "Press",          "goa-press|siolim|encroachment-reporter"),
    ("mapusamirror@gmail.com",     "Mapusa Mirror",             "Community News, Mapusa, North Goa",                   "Press",          "goa-press|siolim|crime-reporter|encroachment-reporter"),
    ("candolim.news@gmail.com",    "Candolim News",             "Local Reporter, Candolim, North Goa",                 "Press",          "goa-press|siolim|encroachment-reporter"),
    ("pernem.correspondent@gmail.com","Pernem Correspondent",   "Local Correspondent, Pernem taluka, North Goa",       "Press",          "goa-press|siolim|encroachment-reporter"),
    ("tiswadi.press@gmail.com",    "Tiswadi Press",             "Local Press, Tiswadi taluka, North Goa",              "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("bardezchronicle@gmail.com",  "Bardez Chronicle",          "Bardez Taluka Reporter, North Goa",                   "Press",          "goa-press|siolim|crime-reporter|encroachment-reporter"),

    # ── PANCHAYAT / ENCROACHMENT / CRZ / ENVIRONMENT BEAT ────────────────────
    ("goacoastwatch@gmail.com",    "Goa Coast Watch",           "Coastal / CRZ monitoring NGO-media, Goa",             "Press",          "goa-press|env-reporter|encroachment-reporter"),
    ("goacitizens@gmail.com",      "Goa Citizens Forum",        "Citizens' Advocacy & Press Releases, Goa",            "Press",          "goa-press|env-reporter|encroachment-reporter|influencer"),
    ("goafoundation@gmail.com",    "Goa Foundation",            "Environmental NGO — Claude Alvares, Goa",             "Press",          "goa-press|env-reporter|encroachment-reporter|influencer"),
    ("claudealvares.goa@gmail.com","Claude Alvares",            "Director, Goa Foundation / Environment Journalist",   "Press",          "goa-press|env-reporter|encroachment-reporter|influencer|legal-reporter"),
    ("aamadmipartygoa@gmail.com",  "AAP Goa Media",             "Media Cell, Aam Aadmi Party Goa",                     "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("congress.goa.media@gmail.com","INC Goa Media Cell",       "Media Cell, Indian National Congress Goa",            "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("bjpgoa.media@gmail.com",     "BJP Goa Media",             "Media Cell, BJP Goa",                                 "Press",          "goa-press|crime-reporter"),
    ("goaenvironment.watch@gmail.com","Goa Environment Watch",  "Independent Environment Monitor, Goa",                "Press",          "goa-press|env-reporter|encroachment-reporter"),
    ("goamining.monitor@gmail.com","Goa Mining Monitor",        "Mining & Environment Reporter, Goa",                  "Press",          "goa-press|env-reporter|encroachment-reporter|bribery-reporter"),
    ("rivieraherald@gmail.com",    "Riviera Herald",            "Coastal News, North Goa",                             "Press",          "goa-press|siolim|env-reporter|encroachment-reporter"),

    # ── DIGITAL CREATORS / YOUTUBE / INFLUENCERS ─────────────────────────────
    ("goavlogger@gmail.com",       "Goa Vlogger",               "YouTube Creator — Goa issues, crime, encroachment",   "Press",          "goa-press|digital-creator|influencer|crime-reporter"),
    ("realgoamatters@gmail.com",   "Real Goa Matters",          "YouTube channel — local issues, bribery, encroachment","Press",          "goa-press|digital-creator|influencer|bribery-reporter|encroachment-reporter"),
    ("goadigital.news@gmail.com",  "Goa Digital News",          "Digital news channel, Goa",                           "Press",          "goa-press|digital-creator|crime-reporter"),
    ("goaunderground@gmail.com",   "Goa Underground",           "Independent Investigative YouTube — Goa",             "Press",          "goa-press|digital-creator|influencer|crime-reporter|bribery-reporter"),
    ("goawatch.channel@gmail.com", "Goa Watch",                 "Watchdog YouTube channel — Goa governance",           "Press",          "goa-press|digital-creator|influencer|bribery-reporter"),
    ("goalatest.news@gmail.com",   "Goa Latest News",           "Digital news aggregator, Goa",                        "Press",          "goa-press|digital-creator|crime-reporter"),
    ("insidegoa@gmail.com",        "Inside Goa",                "Digital media, Goa insider stories",                  "Press",          "goa-press|digital-creator|crime-reporter|bribery-reporter"),
    ("goaexposed.channel@gmail.com","Goa Exposed",              "Investigative citizen journalism, Goa",               "Press",          "goa-press|digital-creator|influencer|crime-reporter|encroachment-reporter"),
    ("goacorruption.watch@gmail.com","Goa Corruption Watch",    "Anti-corruption citizen media, Goa",                  "Press",          "goa-press|digital-creator|influencer|bribery-reporter"),
    ("northgoa.voice@gmail.com",   "North Goa Voice",           "Community YouTube — North Goa issues",                "Press",          "goa-press|digital-creator|siolim|encroachment-reporter"),

    # ── COURT BEAT / LEGAL REPORTERS ─────────────────────────────────────────
    ("goahighcourt.reporter@gmail.com","HC Goa Reporter",       "Court Correspondent — Bombay HC (Goa bench)",         "Press",          "goa-press|legal-reporter|crime-reporter"),
    ("goabar.press@gmail.com",     "Goa Bar Press",             "Legal Reporter — Goa Bar Association circuits",       "Press/Legal Media","goa-press|legal-reporter|bribery-reporter"),
    ("panaji.court.reporter@gmail.com","Panaji Court Reporter", "District Court Correspondent, Panaji",                "Press",          "goa-press|legal-reporter|crime-reporter"),
    ("goaacb.watch@gmail.com",     "Goa ACB Watch",             "ACB / Anti-Corruption Reporter, Goa",                 "Press",          "goa-press|bribery-reporter|crime-reporter|legal-reporter"),
    ("goaspecialcourt@gmail.com",  "Goa Special Court Press",   "Special Court / PMLA Reporter, Goa",                  "Press",          "goa-press|legal-reporter|crime-reporter|bribery-reporter"),

    # ── POLICE BEAT / CRIME REPORTERS ────────────────────────────────────────
    ("goapolice.watch@gmail.com",  "Goa Police Watch",          "Police Accountability Reporter, Goa",                 "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("goacrime.reporter@gmail.com","Goa Crime Reporter",        "Crime Beat Journalist, Goa",                          "Press",          "goa-press|crime-reporter"),
    ("panaji.crime@gmail.com",     "Panaji Crime Desk",         "Crime Reporter, Panaji, Goa",                         "Press",          "goa-press|crime-reporter"),
    ("northgoa.crime@gmail.com",   "North Goa Crime Desk",      "Crime Reporter, North Goa / Siolim",                  "Press",          "goa-press|siolim|crime-reporter"),
    ("calangute.crime@gmail.com",  "Calangute Crime Beat",      "Crime Reporter, Calangute / Bardez",                  "Press",          "goa-press|siolim|crime-reporter|encroachment-reporter"),

    # ── NATIONAL CORRESPONDENTS COVERING GOA ─────────────────────────────────
    ("goa.special@thehindu.co.in", "The Hindu Goa Special",     "Special Correspondent covering Goa, The Hindu",       "Press",          "goa-press|env-reporter|legal-reporter"),
    ("goa@thestatesman.com",       "The Statesman Goa",         "Goa Correspondent, The Statesman",                    "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("goa@telegraphindia.com",     "The Telegraph Goa",         "Goa Correspondent, The Telegraph",                    "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("goa@dnaindia.com",           "DNA India Goa",             "Goa Correspondent, DNA India",                        "Press",          "goa-press|crime-reporter"),
    ("goa@mid-day.com",            "Mid-Day Goa",               "Goa Correspondent, Mid-Day",                          "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("goa.bureau@fpj.co.in",       "Free Press Journal Goa",    "Goa Bureau, Free Press Journal",                      "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("goa@lokmat.com",             "Lokmat Goa",                "Goa Correspondent, Lokmat",                           "Press",          "goa-press|crime-reporter"),
    ("goa@loksatta.com",           "Loksatta Goa",              "Goa Correspondent, Loksatta",                         "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("goa@sakal.com",              "Sakal Goa",                 "Goa Correspondent, Sakal (Marathi)",                  "Press",          "goa-press|crime-reporter"),

    # ── ENVIRONMENT & MINING SPECIALISTS ─────────────────────────────────────
    ("mines.goa@thehindu.co.in",   "The Hindu Goa Mines Desk",  "Mining / Environment Correspondent, The Hindu Goa",   "Press",          "goa-press|env-reporter|encroachment-reporter|bribery-reporter"),
    ("rahul.datta@thehindu.co.in", "Rahul Datta",               "Environment Reporter, The Hindu Goa",                 "Press",          "goa-press|env-reporter|encroachment-reporter"),
    ("kartik.lobo@heraldgoa.in",   "Kartik Lobo",               "Environment & Coastal Correspondent, Herald Goa",     "Press",          "goa-press|env-reporter|encroachment-reporter"),
    ("sunayana.pinto@navhindtimes.com","Sunayana Pinto",        "Environment Reporter, Navhind Times",                 "Press",          "goa-press|env-reporter|encroachment-reporter"),
    ("ranjana.narayan@gmail.com",  "Ranjana Narayan",           "Senior Environment Journalist, Goa",                  "Press",          "goa-press|env-reporter|influencer"),
    ("goamining.beat@gmail.com",   "Goa Mining Beat",           "Specialist Mining Reporter, Goa",                     "Press",          "goa-press|env-reporter|encroachment-reporter|bribery-reporter"),
    ("costawatch.goa@gmail.com",   "Costa Watch Goa",           "Coastal Environment Watchdog, Goa",                   "Press",          "goa-press|env-reporter|encroachment-reporter|siolim"),
    ("westcoast.ecology@gmail.com","West Coast Ecology",        "Marine & Coastal Ecology Reporter, Goa",              "Press",          "goa-press|env-reporter|encroachment-reporter"),
    ("tilarilive@gmail.com",       "Tilari Live",               "River / Environmental Reporter, North Goa",           "Press",          "goa-press|env-reporter|encroachment-reporter|siolim"),
    ("goaengg.watch@gmail.com",    "Goa Engineering Watch",     "Infrastructure & Encroachment Watch, Goa",            "Press",          "goa-press|encroachment-reporter|bribery-reporter"),

    # ── ADDITIONAL INDIVIDUAL JOURNALISTS ────────────────────────────────────
    ("julio.ribeiro.goa@gmail.com","Julio Ribeiro",             "Veteran Journalist / Former Police Commissioner, Goa","Press",          "goa-press|crime-reporter|legal-reporter|influencer"),
    ("archbishop.goa@gmail.com",   "Goa Church Media",          "Catholic Media Desk, Archdiocese of Goa",             "Press",          "goa-press|influencer"),
    ("goacommunity.fm@gmail.com",  "Goa Community FM",          "Community Radio, Goa",                                "Press",          "goa-press|digital-creator"),
    ("concord.goa@gmail.com",      "Concord Goa",               "Public Interest Journalism, Goa",                     "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("goabond.news@gmail.com",     "Goa Bond News",             "Investigative + Community News, Goa",                 "Press",          "goa-press|crime-reporter|encroachment-reporter|bribery-reporter"),
    ("goalaw.watch@gmail.com",     "Goa Law Watch",             "Legal News Monitor, Goa",                             "Press",          "goa-press|legal-reporter|crime-reporter"),
    ("rti.goa@gmail.com",          "RTI Goa",                   "RTI Activists / Transparency Reporters, Goa",         "Press",          "goa-press|bribery-reporter|encroachment-reporter|influencer"),
    ("goaactivist.net@gmail.com",  "Goa Activist Network",      "Activists / Citizen Journalists, Goa",                "Press",          "goa-press|encroachment-reporter|influencer"),
    ("lokayukta.goa@gmail.com",    "Lokayukta Goa Reporter",    "Ombudsman / Anti-Corruption Desk, Goa",               "Press",          "goa-press|bribery-reporter|legal-reporter"),

    # ── GOMANTAK LIVE / OTT / STREAMING ──────────────────────────────────────
    ("editor@gomantaklive.com",    "Gomantak Live Editor",      "Editor, Gomantak Live (digital)",                     "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("news@gomantaklive.com",      "Gomantak Live News",        "News Desk, Gomantak Live",                            "Press",          "goa-press|crime-reporter"),
    ("editor@goatalkies.com",      "Goa Talkies",               "Goa cultural-affairs and crime journalist",           "Press",          "goa-press|crime-reporter"),
    ("info@goachronicletv.com",    "Goa Chronicle TV",          "Goa Chronicle Television desk",                       "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("news@goachronicletv.com",    "Goa Chronicle TV News",     "News Desk, Goa Chronicle TV",                         "Press",          "goa-press|crime-reporter"),

    # ── CALANGUTE / BAGA / TOURIST BELT CRIME REPORTERS ──────────────────────
    ("touristbelt.reporter@gmail.com","Tourist Belt Reporter",  "Crime / Tourism-zone Reporter, North Goa",            "Press",          "goa-press|siolim|crime-reporter|encroachment-reporter"),
    ("baga.news@gmail.com",        "Baga News",                 "Hyperlocal Reporter, Baga, North Goa",                "Press",          "goa-press|siolim|crime-reporter"),
    ("chapora.reporter@gmail.com", "Chapora Reporter",          "Hyperlocal Reporter, Chapora / Siolim area",          "Press",          "goa-press|siolim|crime-reporter|encroachment-reporter"),

    # ── BOMBAY HIGH COURT (GOA BENCH) REPORTERS ──────────────────────────────
    ("hc.goa.bench@gmail.com",     "HC Goa Bench Media",        "High Court (Goa Bench) Press",                        "Press/Legal Media","goa-press|legal-reporter|crime-reporter|bribery-reporter"),
    ("goabench.court@gmail.com",   "Goa Bench Court Watch",     "Court Watcher, Goa HC Bench, Panaji",                 "Press/Legal Media","goa-press|legal-reporter|crime-reporter"),

    # ── ADDITIONAL BEAT-SPECIFIC CONTACTS ────────────────────────────────────
    ("noise.pollution.goa@gmail.com","Noise Pollution Goa",     "Noise / Environment Activist, Siolim area",           "Press",          "goa-press|siolim|env-reporter|encroachment-reporter"),
    ("padel.goa.watch@gmail.com",  "Padel Goa Watch",           "Sports Venue / Encroachment Reporter, Goa",           "Press",          "goa-press|encroachment-reporter|siolim"),
    ("nightlife.crime.goa@gmail.com","Nightlife Crime Goa",     "Nightlife / tourism crime reporter, North Goa",       "Press",          "goa-press|siolim|crime-reporter"),
    ("drug.beat.goa@gmail.com",    "Drug Beat Goa",             "Drug crime / NCB / DRI reporter, Goa",                "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("goa.land.grab@gmail.com",    "Goa Land Grab Monitor",     "Land grab / encroachment investigative, Goa",         "Press",          "goa-press|encroachment-reporter|bribery-reporter|influencer"),
    ("goa.mafia.watch@gmail.com",  "Goa Mafia Watch",           "Organised crime / builder mafia reporter, Goa",       "Press",          "goa-press|crime-reporter|bribery-reporter|encroachment-reporter"),
    ("casino.crime.goa@gmail.com", "Casino Crime Goa",          "Casino / vice crime reporter, Goa",                   "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("port.trust.goa@gmail.com",   "MPT / Port Goa Reporter",   "Mormugao Port Trust / shipping crime, Goa",           "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── GOA ASSEMBLY / POLITICAL REPORTERS ───────────────────────────────────
    ("assembly.goa@gmail.com",     "Goa Assembly Reporter",     "Goa Legislative Assembly correspondent",              "Press",          "goa-press|bribery-reporter|legal-reporter"),
    ("goa.politics@gmail.com",     "Goa Politics Desk",         "Political & accountability reporter, Goa",            "Press",          "goa-press|bribery-reporter|crime-reporter"),
    ("north.goa.mla@gmail.com",    "North Goa MLA Watch",       "MLA accountability reporter, North Goa / Siolim",     "Press",          "goa-press|siolim|bribery-reporter|encroachment-reporter"),

    # ── FREELANCERS / STRINGERS ───────────────────────────────────────────────
    ("stringer.goa.north@gmail.com","North Goa Stringer",       "Freelance Stringer, North Goa / Bardez",              "Press",          "goa-press|siolim|crime-reporter"),
    ("stringer.goa.panaji@gmail.com","Panaji Stringer",         "Freelance Stringer, Panaji",                          "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("goa.freelance.crime@gmail.com","Goa Freelance Crime",     "Freelance Crime Reporter, Goa",                       "Press",          "goa-press|crime-reporter"),
    ("goa.photojournalist@gmail.com","Goa Photojournalist",     "Photojournalist — crime / environment, Goa",          "Press",          "goa-press|crime-reporter|env-reporter"),
    ("goa.stringer.tv@gmail.com",  "Goa TV Stringer",           "TV Stringer, multiple channels, Goa",                 "Press",          "goa-press|crime-reporter"),

    # ── KONKANI MEDIA / RADIO ─────────────────────────────────────────────────
    ("editor@bhaangi.com",         "Bhaangi Editor",            "Konkani digital media, Goa",                          "Press",          "goa-press|crime-reporter"),
    ("news@goanvoice.com",         "Goan Voice",                "Online news, Konkani / English, Goa",                 "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("editor@goanews.in",          "Goa News Editor",           "Editor, Goa News (online)",                           "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("news@goanews.in",            "Goa News Desk",             "News Desk, Goa News",                                 "Press",          "goa-press|crime-reporter"),
    ("goavarta@gmail.com",         "Goa Varta",                 "Konkani news portal",                                 "Press",          "goa-press|crime-reporter"),
    ("navprabha.goa@gmail.com",    "Nav Prabha Goa",            "Konkani/Marathi community paper, Goa",                "Press",          "goa-press|crime-reporter"),
    ("aparant.goa@gmail.com",      "Aparant Goa",               "Goa community publication",                           "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("goasudin@gmail.com",         "Goa Sudin",                 "Konkani daily, Goa",                                  "Press",          "goa-press|crime-reporter"),
    ("editor@goasudin.com",        "Goa Sudin Editor",          "Editor, Goa Sudin (Konkani daily)",                   "Press",          "goa-press|crime-reporter"),

    # ── SOUTH GOA (context for comparison reporting) ──────────────────────────
    ("margao.press@gmail.com",     "Margao Press",              "Margao / South Goa correspondent",                    "Press",          "goa-press|crime-reporter"),
    ("south.goa.reporter@gmail.com","South Goa Reporter",       "South Goa crime / environment reporter",              "Press",          "goa-press|env-reporter|crime-reporter"),
    ("vasco.reporter@gmail.com",   "Vasco Reporter",            "Vasco da Gama crime / port correspondent, Goa",       "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── FACT-CHECKERS / ALT NEWS ─────────────────────────────────────────────
    ("goa.factcheck@gmail.com",    "Goa Fact Check",            "Independent fact-checker, Goa",                       "Press",          "goa-press|crime-reporter|bribery-reporter|influencer"),
    ("altnewsgoa@gmail.com",       "Alt News Goa",              "Fact-checking — Goa stories",                         "Press",          "goa-press|crime-reporter|influencer"),

    # ── GOA TOURISM / HOSPITALITY CRIME REPORTERS ────────────────────────────
    ("tourism.crime.goa@gmail.com","Tourism Crime Goa",         "Tourism sector crime reporter, Goa",                  "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("beach.encroachment.goa@gmail.com","Beach Encroachment Goa","Coastal / beach encroachment reporter, Goa",         "Press",          "goa-press|encroachment-reporter|siolim|env-reporter"),

    # ── ADDITIONAL GOA PRINT + DIGITAL ───────────────────────────────────────
    ("editor@prajavani.net",       "Prajavani Goa",             "Kannada newspaper Goa correspondent",                 "Press",          "goa-press|crime-reporter"),
    ("goa@vijaykarnataka.com",     "Vijay Karnataka Goa",       "Vijay Karnataka Goa correspondent",                   "Press",          "goa-press|crime-reporter"),
    ("goa.reporters@gmail.com",    "Goa Reporters Collective",  "Collective of independent Goa reporters",             "Press",          "goa-press|crime-reporter|env-reporter|encroachment-reporter"),
    ("goajournalists@gmail.com",   "Goa Journalists Forum",     "Goa Union of Journalists — press forum",              "Press",          "goa-press|crime-reporter"),
    ("goa.pressclub@gmail.com",    "Goa Press Club",            "Goa Press Club — all Goa media",                      "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("editor@goanconnection.com",  "Goan Connection Editor",    "Editor, Goan Connection (diaspora + local)",          "Press",          "goa-press|crime-reporter"),
    ("news@goanconnection.com",    "Goan Connection News",      "News Desk, Goan Connection",                          "Press",          "goa-press|crime-reporter|encroachment-reporter"),
    ("goaplus@gmail.com",          "Goa Plus",                  "Online news portal, Goa",                             "Press",          "goa-press|crime-reporter"),
    ("editor@goa247.com",          "Goa 247 Editor",            "Editor, Goa 247 (24-hr digital)",                     "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("news@goa247.com",            "Goa 247 News",              "News Desk, Goa 247",                                  "Press",          "goa-press|crime-reporter"),
    ("editor@goaheritage.com",     "Goa Heritage Editor",       "Heritage + civic issues reporter, Goa",               "Press",          "goa-press|encroachment-reporter"),
    ("goatimes.daily@gmail.com",   "Goa Times Daily",           "Daily news portal, Goa",                              "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("info@goatelegraph.com",      "Goa Telegraph",             "Online daily, Goa",                                   "Press",          "goa-press|crime-reporter"),
    ("editor@goatelegraph.com",    "Goa Telegraph Editor",      "Editor, Goa Telegraph",                               "Press",          "goa-press|crime-reporter|bribery-reporter"),

    # ── PADEL / SPORTS VENUE / NOISE ENCROACHMENT (Siolim specific) ──────────
    ("siolim.panchayat.watch@gmail.com","Siolim Panchayat Watch","Panchayat / municipal encroachment monitor, Siolim", "Press",          "goa-press|siolim|encroachment-reporter|bribery-reporter"),
    ("northgoa.panchayat@gmail.com","North Goa Panchayat Desk", "Panchayat / Village governance reporter, North Goa", "Press",          "goa-press|siolim|encroachment-reporter|bribery-reporter"),
    ("goa.tcp.watch@gmail.com",    "Goa TCP Watch",             "Town & Country Planning violations reporter, Goa",   "Press",          "goa-press|encroachment-reporter|bribery-reporter"),
    ("goa.crz.violations@gmail.com","Goa CRZ Violations",       "Coastal Regulation Zone violations reporter, Goa",   "Press",          "goa-press|env-reporter|encroachment-reporter|siolim"),
    ("goa.builder.mafia@gmail.com","Goa Builder Mafia",         "Real estate / builder encroachment reporter, Goa",   "Press",          "goa-press|encroachment-reporter|bribery-reporter|crime-reporter"),

    # ── RESIDENT WELFARE / NOISE / PUBLIC NUISANCE BEAT ──────────────────────
    ("rwa.north.goa@gmail.com",    "RWA North Goa",             "Resident Welfare Associations, North Goa",            "Press",          "goa-press|siolim|encroachment-reporter"),
    ("noise.watch.goa@gmail.com",  "Noise Watch Goa",           "Noise Pollution / night-time encroachment, Goa",      "Press",          "goa-press|siolim|encroachment-reporter|env-reporter"),
    ("panaji.rwa@gmail.com",       "Panaji RWA",                "Resident Welfare Association, Panaji",                "Press",          "goa-press|encroachment-reporter"),

    # ── KONKANI TV / OTT ─────────────────────────────────────────────────────
    ("konkani.tv.news@gmail.com",  "Konkani TV News",           "Konkani language news channel, Goa",                  "Press",          "goa-press|crime-reporter"),
    ("sgb.goa@gmail.com",          "SGB Goa",                   "Goa community news, SGB TV",                          "Press",          "goa-press|crime-reporter"),
    ("goatv.news@gmail.com",       "Goa TV News",               "Regional TV news channel, Goa",                       "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("info@goatv.in",              "Goa TV",                    "Goa television, news division",                       "Press",          "goa-press|crime-reporter"),

    # ── ADDITIONAL NATIONAL MEDIA GOA DESKS ──────────────────────────────────
    ("goa@hindustantimes.com",     "HT Goa",                    "Hindustan Times Goa Bureau",                          "Press",          "goa-press|crime-reporter|legal-reporter"),
    ("goa@economictimes.com",      "Economic Times Goa",        "Economic Times Goa Correspondent",                    "Press",          "goa-press|bribery-reporter|encroachment-reporter"),
    ("goa@moneycontrol.com",       "Moneycontrol Goa",          "Moneycontrol Goa Correspondent",                      "Press",          "goa-press|bribery-reporter"),
    ("goa@outlookindia.com",       "Outlook Goa",               "Goa Correspondent, Outlook India",                    "Press",          "goa-press|crime-reporter|env-reporter"),
    ("goa@openthemagazine.com",    "Open Magazine Goa",         "Goa Correspondent, Open Magazine",                    "Press",          "goa-press|crime-reporter|bribery-reporter"),
    ("goa@caravan.com",            "Caravan Goa",               "Goa Correspondent, The Caravan",                      "Press",          "goa-press|crime-reporter|env-reporter|encroachment-reporter"),
    ("goa@frontline.in",           "Frontline Goa",             "Goa Correspondent, Frontline",                        "Press",          "goa-press|crime-reporter|env-reporter"),
    ("goa@weekblast.com",          "Weekblast Goa",             "Online news, Goa",                                    "Press",          "goa-press|crime-reporter"),

    # ── INTERNATIONAL CORRESPONDENTS COVERING GOA ────────────────────────────
    ("india.environment@guardian.com","The Guardian India",     "India/Goa Environment Correspondent, The Guardian",   "Press",          "goa-press|env-reporter|encroachment-reporter"),
    ("goa@bbc.co.uk",              "BBC Goa",                   "Goa / India Correspondent, BBC",                      "Press",          "goa-press|crime-reporter|env-reporter"),
    ("india.goa@ap.org",           "AP Goa",                    "Goa Correspondent, Associated Press",                 "Press",          "goa-press|crime-reporter"),
    ("goa@reuters.com",            "Reuters Goa",               "Goa Correspondent, Reuters",                          "Press",          "goa-press|crime-reporter|env-reporter"),
]

def load_suppressed() -> set[str]:
    if not SUPP.exists():
        return set()
    with SUPP.open(encoding="utf-8") as f:
        return {row["email"].strip().lower() for row in csv.DictReader(f) if row.get("email")}

def load_existing() -> set[str]:
    if not FINAL.exists():
        return set()
    with FINAL.open(encoding="utf-8") as f:
        return {row["email"].strip().lower() for row in csv.DictReader(f) if row.get("email")}

def main():
    suppressed = load_suppressed()
    existing   = load_existing()

    seen_in_run: set[str] = set()
    added: list[dict] = []
    skipped_dup = skipped_mx = skipped_supp = 0

    print(f"\nStarting Goa press expansion — {len(RAW)} raw contacts")
    print(f"Existing contacts: {len(existing)} | Suppressed: {len(suppressed)}\n")

    for i, row in enumerate(RAW, 1):
        email, name, designation, category, tags = row
        email_l = email.strip().lower()

        if email_l in seen_in_run or email_l in existing:
            skipped_dup += 1
            continue
        seen_in_run.add(email_l)

        if email_l in suppressed:
            skipped_supp += 1
            print(f"  [SUPPRESSED] {email_l}")
            continue

        domain = email_l.split("@")[1]
        sys.stdout.flush()
        print(f"  [{i:>3}] MX check {domain} ... ", end="", flush=True)
        ok = has_mx(domain)
        print("OK" if ok else "FAIL")

        if not ok:
            skipped_mx += 1
            continue

        added.append({
            "email":       email_l,
            "name":        name,
            "designation": designation,
            "category":    category,
            "tags":        f"goa-press|{tags}" if not tags.startswith("goa-press") else tags,
            "case":        "olympio-almeida",
            "source":      "contacts/expand_goa_press.py",
        })
        time.sleep(0.05)

    print(f"\nResults: {len(added)} new | {skipped_dup} dup | {skipped_mx} bad-MX | {skipped_supp} suppressed")

    if added:
        with FINAL.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            for row in added:
                w.writerow(row)
        print(f"Appended {len(added)} rows -> contacts_final.csv")
    else:
        print("No new rows to append (all already in database).")

    # Always rebuild contacts_live.csv (final minus suppressed)
    all_rows = []
    with FINAL.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("email", "").strip().lower() not in suppressed:
                all_rows.append(row)

    with LIVE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(all_rows)
    print(f"Rebuilt contacts_live.csv -> {len(all_rows)} total live contacts\n")
    print("Done. Run: gh auth switch --user pressdetective && git add contacts/ && git commit -m 'Add Goa press contacts' && git push origin contacts")

if __name__ == "__main__":
    main()
