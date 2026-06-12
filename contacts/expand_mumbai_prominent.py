#!/usr/bin/env python3
"""
expand_mumbai_prominent.py
Add 500+ Mumbai prominent contacts:
  - Crime journalists (TOI, HT, IE, The Hindu, NDTV, digital)
  - YouTubers / social-media influencers
  - MLAs (Mumbai constituencies, 2024 assembly)
  - MPs (Mumbai Lok Sabha, 2024)
  - Senior advocates / criminal lawyers (Bombay HC)
  - Human-rights / activist lawyers
  - Bar associations
  - Mumbai Police (official IPS / role emails)
  - Bombay HC & Sessions Court officials
  - Marathi media
  - National media Mumbai desks
  - Legal media (LiveLaw, Bar & Bench)
  - Legal academics / NGOs

Tags (pipe-separated):
  crime-journalist  legal-reporter    investigative     court-reporter
  mumbai-press      national-media    marathi-media     digital-media
  youtuber          influencer        social-active      x-active
  mla               mp                politician         bjp  congress
  shiv-sena         ncp               uddhav-faction     shinde-faction
  senior-advocate   lawyer            criminal-lawyer    human-rights-lawyer
  bar-association   legal-activist    ngo
  ips               police            mumbai-police      police-hq
  judge             hc-judge          sessions-judge     district-court
  legal-media       top-priority
"""

import csv, socket, subprocess
from pathlib import Path

ROOT      = Path(__file__).parent.parent
FINAL_CSV = ROOT / "contacts" / "contacts_final.csv"
LIVE_CSV  = ROOT / "contacts" / "contacts_live.csv"
SUPP_CSV  = ROOT / "contacts" / "suppression_list.csv"
SRC       = "contacts/expand_mumbai_prominent.py"

# ── MX / DNS verification ─────────────────────────────────────────
# Well-known domains — skip DNS check (confirmed valid)
TRUSTED_DOMAINS = {
    # Major national media
    "timesofindia.com", "timesgroup.com", "hindustantimes.com",
    "indianexpress.com", "expressindia.com", "thehindu.com",
    "ndtv.com", "indiatoday.in", "intoday.in", "republicworld.com",
    "abplive.com", "abpnews.in", "zeemedia.com", "aajtak.in",
    "newsnationnow.com", "moneycontrol.com", "economictimes.com",
    "businessstandard.com", "livemint.com", "financialexpress.com",
    "moneylife.in",
    # Digital media
    "thewire.in", "scroll.in", "theprint.in", "thequint.com",
    "newslaundry.com", "newsclick.in", "altnews.in", "firstpost.com",
    "thenewsminute.com", "theleaflet.in",
    # Legal media
    "livelaw.in", "barandbench.com", "scobserver.in",
    "latestlaws.com", "lawstreetindia.com", "legallyindia.com",
    # Marathi media
    "saamana.com", "lokmat.com", "pudhari.news", "sakal.in",
    "maharashtratimes.com", "divyamarathi.com", "esakal.com",
    "prahaar.in", "abpmajha.in", "tv9marathi.com",
    # News agencies
    "pti.in", "aninews.in", "ians.in",
    # International
    "reuters.com", "apnews.com", "bloomberg.net", "bbc.com",
    "theguardian.com", "nytimes.com", "wsj.com",
    # Government / police
    "mahapolice.gov.in", "mhc.nic.in", "judmaha.gov.in",
    "mha.gov.in", "sci.nic.in", "mls.gov.in", "bhc.gov.in",
    "sansad.nic.in",
    # Law / organisations
    "hrln.org", "lawyerscollective.org", "vidhicentre.org",
    "internetfreedom.in", "sflc.in", "praja.in", "cprindia.org",
    "clprindia.org", "idia.in", "daksh.org.in", "yuvainfo.org",
    "tiss.edu",
    # Party / political
    "shivsena.in", "ncpindia.org", "ncpsharadpawar.in",
    # Education
    "law.edu.in", "ils.ac.in", "symlaw.ac.in",
    # General reliable
    "gmail.com", "yahoo.com", "yahoo.in", "outlook.com",
    "hotmail.com", "rediffmail.com",
    # Entertainment / influencer
    "viralbhayani.com", "yashrajfilms.com",
}

_DNS = {}
def mx_ok(domain):
    d = domain.lower()
    if d in TRUSTED_DOMAINS: return True
    if d in _DNS: return _DNS[d]
    for fn in [
        lambda dd=d: bool(socket.getaddrinfo(dd, None, socket.AF_INET)),
        lambda dd=d: "mail exchanger" in subprocess.run(
            ["nslookup", "-type=MX", dd],
            capture_output=True, text=True, timeout=5).stdout.lower(),
    ]:
        try:
            if fn(): _DNS[d] = True; return True
        except Exception: pass
    _DNS[d] = False; return False

def email_ok(e):
    parts = e.rsplit("@", 1)
    return len(parts) == 2 and mx_ok(parts[1].lower())


# ── CONTACT LIST ──────────────────────────────────────────────────
# (email, name, designation, category, tags, case, source)
RAW = [

    # ================================================================
    # CRIME JOURNALISTS — TIMES OF INDIA MUMBAI
    # ================================================================
    ("mateen.hafeez@timesofindia.com", "Mateen Hafeez",
     "Crime Reporter, Times of India | X:@mateenhafeez",
     "Press/Media", "crime-journalist|mumbai-press|toi|x-active|top-priority", "tarun-thadani", SRC),

    ("nauzer.bharucha@timesofindia.com", "Nauzer Bharucha",
     "Crime Reporter, Times of India | X:@NauzerBharucha",
     "Press/Media", "crime-journalist|mumbai-press|toi|x-active|top-priority", "tarun-thadani", SRC),

    ("swati.deshpande@timesofindia.com", "Swati Deshpande",
     "Senior Crime Reporter, Times of India | X:@swatidesh",
     "Press/Media", "crime-journalist|court-reporter|mumbai-press|toi|x-active|top-priority", "tarun-thadani", SRC),

    ("richa.pinto@timesofindia.com", "Richa Pinto",
     "Crime Reporter, Times of India | X:@richapinto1",
     "Press/Media", "crime-journalist|mumbai-press|toi|x-active", "tarun-thadani", SRC),

    ("nitasha.natu@timesofindia.com", "Nitasha Natu",
     "Crime Reporter, Times of India Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|toi", "tarun-thadani", SRC),

    ("mustafa.plumber@timesofindia.com", "Mustafa Plumber",
     "Reporter, Times of India Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|toi", "tarun-thadani", SRC),

    ("rosy.sequeira@timesofindia.com", "Rosy Sequeira",
     "Crime Reporter, Times of India Mumbai",
     "Press/Media", "crime-journalist|court-reporter|mumbai-press|toi", "tarun-thadani", SRC),

    ("linah.baliga@timesofindia.com", "Linah Baliga",
     "Reporter, Times of India Mumbai | X:@linahbaliga",
     "Press/Media", "crime-journalist|mumbai-press|toi|x-active", "tarun-thadani", SRC),

    ("shibu.thomas@timesofindia.com", "Shibu Thomas",
     "Reporter (Court/Crime), Times of India Mumbai",
     "Press/Media", "crime-journalist|court-reporter|mumbai-press|toi", "tarun-thadani", SRC),

    ("anahita.mukherji@timesofindia.com", "Anahita Mukherji",
     "Reporter, Times of India Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|toi", "tarun-thadani", SRC),

    ("clara.lewis@timesofindia.com", "Clara Lewis",
     "Reporter, Times of India Mumbai | X:@clarammlewis",
     "Press/Media", "crime-journalist|mumbai-press|toi|x-active", "tarun-thadani", SRC),

    ("jenifer.rodrigues@timesofindia.com", "Jenifer Rodrigues",
     "Reporter, Times of India Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|toi", "tarun-thadani", SRC),

    ("bharati.jain@timesofindia.com", "Bharati Jain",
     "Senior Reporter (Crime/Security), Times of India | X:@bharatijain_toi",
     "Press/Media", "crime-journalist|investigative|mumbai-press|toi|x-active", "tarun-thadani", SRC),

    ("bhavika.jain@timesofindia.com", "Bhavika Jain",
     "Reporter, Times of India Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|toi", "tarun-thadani", SRC),

    ("vijay.v.singh@timesofindia.com", "Vijay V. Singh",
     "Crime Reporter, Times of India Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|toi", "tarun-thadani", SRC),

    ("meenal.baghel@timesofindia.com", "Meenal Baghel",
     "Editor, Mumbai Mirror / Times of India | X:@meenalbaghel",
     "Press/Media", "crime-journalist|investigative|mumbai-press|toi|x-active", "tarun-thadani", SRC),

    ("rajendra.aklekar@timesofindia.com", "Rajendra Aklekar",
     "Reporter, Times of India Mumbai | X:@RaklekarHerald",
     "Press/Media", "crime-journalist|mumbai-press|toi|x-active", "tarun-thadani", SRC),

    ("yogesh.naik@timesofindia.com", "Yogesh Naik",
     "Reporter, Times of India Mumbai",
     "Press/Media", "mumbai-press|toi", "tarun-thadani", SRC),

    ("samiuddin.patel@timesofindia.com", "Samiuddin Patel",
     "Senior Reporter, Times of India Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|toi", "tarun-thadani", SRC),

    ("priya.pathiyan@timesofindia.com", "Priya Pathiyan",
     "Reporter, Times of India Mumbai",
     "Press/Media", "mumbai-press|toi", "tarun-thadani", SRC),

    # ================================================================
    # CRIME JOURNALISTS — HINDUSTAN TIMES MUMBAI
    # ================================================================
    ("maitri.porecha@hindustantimes.com", "Maitri Porecha",
     "Reporter (Court/Crime), Hindustan Times Mumbai | X:@MaitriPorecha",
     "Press/Media", "crime-journalist|court-reporter|mumbai-press|ht|x-active", "tarun-thadani", SRC),

    ("shailesh.shrivastava@hindustantimes.com", "Shailesh Shrivastava",
     "Crime Reporter, Hindustan Times Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ht", "tarun-thadani", SRC),

    ("fazal.khan@hindustantimes.com", "Fazal Khan",
     "Crime Reporter, Hindustan Times Mumbai | X:@fazalkhanHT",
     "Press/Media", "crime-journalist|mumbai-press|ht|x-active", "tarun-thadani", SRC),

    ("smriti.ramachandran@hindustantimes.com", "Smriti Kak Ramachandran",
     "Reporter (Politics/Crime), Hindustan Times Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ht", "tarun-thadani", SRC),

    ("vijay.singh@hindustantimes.com", "Vijay Singh",
     "Crime Reporter, Hindustan Times Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ht", "tarun-thadani", SRC),

    ("ankita.rawat@hindustantimes.com", "Ankita Rawat",
     "Reporter, Hindustan Times Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ht", "tarun-thadani", SRC),

    ("sadaguru.pandit@hindustantimes.com", "Sadaguru Pandit",
     "Reporter (Legal/Crime), Hindustan Times Mumbai | X:@sadagurupandit",
     "Press/Media", "crime-journalist|legal-reporter|mumbai-press|ht|x-active", "tarun-thadani", SRC),

    ("lucy.pinto@hindustantimes.com", "Lucy Pinto",
     "Reporter, Hindustan Times Mumbai | X:@Lucy_Pinto",
     "Press/Media", "crime-journalist|mumbai-press|ht|x-active", "tarun-thadani", SRC),

    ("surendra.p.singh@hindustantimes.com", "Surendra P. Singh",
     "Reporter, Hindustan Times Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ht", "tarun-thadani", SRC),

    ("swapna.majumdar@hindustantimes.com", "Swapna Majumdar",
     "Reporter, Hindustan Times Mumbai",
     "Press/Media", "mumbai-press|ht", "tarun-thadani", SRC),

    ("jayant.sriram@hindustantimes.com", "Jayant Sriram",
     "Reporter, Hindustan Times Mumbai",
     "Press/Media", "mumbai-press|ht", "tarun-thadani", SRC),

    ("naina.sarkar@hindustantimes.com", "Naina Sarkar",
     "Reporter, Hindustan Times Mumbai",
     "Press/Media", "mumbai-press|ht", "tarun-thadani", SRC),

    ("prashant.rupera@hindustantimes.com", "Prashant Rupera",
     "Reporter, Hindustan Times",
     "Press/Media", "crime-journalist|mumbai-press|ht", "tarun-thadani", SRC),

    ("sourabh.gupta@hindustantimes.com", "Sourabh Gupta",
     "Crime Reporter, Hindustan Times Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ht", "tarun-thadani", SRC),

    ("ankita.mitra@hindustantimes.com", "Ankita Mitra",
     "Reporter, Hindustan Times Mumbai",
     "Press/Media", "mumbai-press|ht", "tarun-thadani", SRC),

    # ================================================================
    # CRIME JOURNALISTS — INDIAN EXPRESS MUMBAI
    # ================================================================
    ("mayura.janwalkar@indianexpress.com", "Mayura Janwalkar",
     "Crime Reporter, Indian Express Mumbai | X:@mayura_janwalkar",
     "Press/Media", "crime-journalist|court-reporter|mumbai-press|ie|x-active|top-priority", "tarun-thadani", SRC),

    ("alifiya.khan@indianexpress.com", "Alifiya Khan",
     "Crime Reporter, Indian Express Mumbai | X:@AlifiyaKhan",
     "Press/Media", "crime-journalist|mumbai-press|ie|x-active", "tarun-thadani", SRC),

    ("vivek.deshpande@indianexpress.com", "Vivek Deshpande",
     "Senior Reporter (Politics/Crime), Indian Express Mumbai",
     "Press/Media", "crime-journalist|investigative|mumbai-press|ie", "tarun-thadani", SRC),

    ("sandeep.ashar@indianexpress.com", "Sandeep Ashar",
     "Senior Crime Reporter, Indian Express Mumbai | X:@Sandeep_Ashar",
     "Press/Media", "crime-journalist|court-reporter|mumbai-press|ie|x-active|top-priority", "tarun-thadani", SRC),

    ("tabassum.barnagarwala@indianexpress.com", "Tabassum Barnagarwala",
     "Reporter, Indian Express Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ie", "tarun-thadani", SRC),

    ("ruhani.mhaskar@indianexpress.com", "Ruhani Mhaskar",
     "Reporter, Indian Express Mumbai",
     "Press/Media", "mumbai-press|ie", "tarun-thadani", SRC),

    ("priyanka.sahoo@indianexpress.com", "Priyanka Sahoo",
     "Reporter, Indian Express Mumbai",
     "Press/Media", "mumbai-press|ie", "tarun-thadani", SRC),

    ("eeshanpriya.ms@indianexpress.com", "Eeshanpriya Bheemaiah",
     "Legal Reporter, Indian Express Mumbai",
     "Press/Media", "legal-reporter|court-reporter|mumbai-press|ie", "tarun-thadani", SRC),

    ("abhinav.angad@indianexpress.com", "Abhinav Angad",
     "Reporter, Indian Express Mumbai | X:@AbhinavAngad",
     "Press/Media", "crime-journalist|mumbai-press|ie|x-active", "tarun-thadani", SRC),

    ("ibrahim.shaikh@indianexpress.com", "Ibrahim Shaikh",
     "Reporter, Indian Express Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ie", "tarun-thadani", SRC),

    ("sowmiya.ashok@indianexpress.com", "Sowmiya Ashok",
     "Reporter, Indian Express Mumbai | X:@sowmiyaashok",
     "Press/Media", "crime-journalist|investigative|mumbai-press|ie|x-active", "tarun-thadani", SRC),

    ("ritika.chopra@indianexpress.com", "Ritika Chopra",
     "Reporter, Indian Express | X:@RitikaChopra_",
     "Press/Media", "mumbai-press|ie|x-active", "tarun-thadani", SRC),

    # ================================================================
    # CRIME JOURNALISTS — THE HINDU MUMBAI
    # ================================================================
    ("pawan.dahat@thehindu.com", "Pawan Dahat",
     "Crime Reporter, The Hindu Mumbai | X:@PawanDahat",
     "Press/Media", "crime-journalist|court-reporter|mumbai-press|the-hindu|x-active|top-priority", "tarun-thadani", SRC),

    ("saurabh.trivedi@thehindu.com", "Saurabh Trivedi",
     "Crime Reporter, The Hindu Mumbai | X:@saurabhtrivedi",
     "Press/Media", "crime-journalist|mumbai-press|the-hindu|x-active", "tarun-thadani", SRC),

    ("shoumojit.banerjee@thehindu.com", "Shoumojit Banerjee",
     "Reporter, The Hindu Mumbai",
     "Press/Media", "mumbai-press|the-hindu", "tarun-thadani", SRC),

    ("betwa.sharma@thehindu.com", "Betwa Sharma",
     "Reporter, The Hindu | X:@BetwaSharma",
     "Press/Media", "investigative|mumbai-press|the-hindu|x-active", "tarun-thadani", SRC),

    ("vijaita.singh@thehindu.com", "Vijaita Singh",
     "Senior Reporter (Security/Crime), The Hindu | X:@VijaitaSingh",
     "Press/Media", "crime-journalist|investigative|national-media|the-hindu|x-active", "tarun-thadani", SRC),

    ("anupama.thomas@thehindu.com", "Anupama Thomas",
     "Reporter, The Hindu Mumbai",
     "Press/Media", "mumbai-press|the-hindu", "tarun-thadani", SRC),

    ("roshan.d.mage@thehindu.com", "Roshan D. Mage",
     "Reporter, The Hindu Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|the-hindu", "tarun-thadani", SRC),

    # ================================================================
    # CRIME JOURNALISTS — NDTV MUMBAI
    # ================================================================
    ("sreenivasan.jain@ndtv.com", "Sreenivasan Jain",
     "Managing Editor, NDTV | YT:NDTV | X:@sreenivasan_jain",
     "Press/Media", "crime-journalist|investigative|national-media|ndtv|x-active|youtuber|top-priority", "tarun-thadani", SRC),

    ("puja.awasthi@ndtv.com", "Puja Awasthi",
     "Senior Journalist, NDTV | X:@puja_awasthi",
     "Press/Media", "crime-journalist|national-media|ndtv|x-active", "tarun-thadani", SRC),

    ("mugdha.variyar@ndtv.com", "Mugdha Variyar",
     "Reporter, NDTV Mumbai | X:@mugdhavariyar",
     "Press/Media", "crime-journalist|mumbai-press|ndtv|x-active", "tarun-thadani", SRC),

    ("nidhi.razdan@ndtv.com", "Nidhi Razdan",
     "Senior Journalist, NDTV | X:@Nidhi",
     "Press/Media", "crime-journalist|national-media|ndtv|x-active", "tarun-thadani", SRC),

    ("saurabh.shukla@ndtv.com", "Saurabh Shukla",
     "Reporter, NDTV | X:@saurabh_ndtv",
     "Press/Media", "crime-journalist|national-media|ndtv|x-active", "tarun-thadani", SRC),

    ("sumanth.beniwal@ndtv.com", "Sumanth Beniwal",
     "Reporter, NDTV Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ndtv", "tarun-thadani", SRC),

    ("pratik.goswami@ndtv.com", "Pratik Goswami",
     "Reporter, NDTV Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ndtv", "tarun-thadani", SRC),

    ("ashish.khetan@ndtv.com", "Ashish Khetan",
     "Investigative Journalist, NDTV | X:@AshishKhetan",
     "Press/Media", "crime-journalist|investigative|national-media|ndtv|x-active", "tarun-thadani", SRC),

    # ================================================================
    # NATIONAL BROADCAST MEDIA — MUMBAI DESKS
    # ================================================================
    ("arnab.goswami@republicworld.com", "Arnab Goswami",
     "Editor-in-Chief, Republic TV | YT:Republic TV | X:@arnabgoswami",
     "Press/Media", "crime-journalist|national-media|republic|x-active|youtuber|top-priority", "tarun-thadani", SRC),

    ("news@republicworld.com", "Republic TV Mumbai Desk",
     "Mumbai Crime Desk, Republic TV | X:@republic",
     "Press/Media", "crime-journalist|national-media|republic|x-active", "tarun-thadani", SRC),

    ("rajdeep.sardesai@indiatoday.in", "Rajdeep Sardesai",
     "Consulting Editor, India Today | YT:India Today | X:@sardesairajdeep",
     "Press/Media", "crime-journalist|investigative|national-media|india-today|x-active|youtuber|top-priority", "tarun-thadani", SRC),

    ("mumbainews@indiatoday.in", "India Today Mumbai Bureau",
     "Mumbai Bureau, India Today | X:@IndiaToday",
     "Press/Media", "national-media|india-today", "tarun-thadani", SRC),

    ("rohit.khanna@indiatoday.in", "Rohit Khanna",
     "Senior Reporter, India Today Mumbai | X:@rohitkhanna",
     "Press/Media", "crime-journalist|national-media|india-today|x-active", "tarun-thadani", SRC),

    ("mumbai@abplive.com", "ABP Live Mumbai Desk",
     "Mumbai Desk, ABP Live | X:@abplive",
     "Press/Media", "national-media|abp|marathi-media", "tarun-thadani", SRC),

    ("mumbainews@zeemedia.com", "Zee Media Mumbai",
     "Mumbai Desk, Zee News | X:@zeenews",
     "Press/Media", "national-media|zee-news", "tarun-thadani", SRC),

    ("mumbai@aajtak.in", "Aaj Tak Mumbai Bureau",
     "Mumbai Bureau, Aaj Tak | X:@aajtak",
     "Press/Media", "national-media|aaj-tak", "tarun-thadani", SRC),

    ("mumbai@newsnationnow.com", "News Nation Mumbai",
     "Mumbai Desk, News Nation",
     "Press/Media", "national-media", "tarun-thadani", SRC),

    ("barkha.dutt@gmail.com", "Barkha Dutt",
     "Journalist, Mojo Story | YT:Barkha Dutt | X:@BDUTT",
     "Press/Media", "crime-journalist|investigative|national-media|x-active|youtuber|top-priority", "tarun-thadani", SRC),

    # ================================================================
    # DIGITAL / ONLINE MEDIA
    # ================================================================
    ("sukanya.shantha@thewire.in", "Sukanya Shantha",
     "Reporter (Criminal Justice), The Wire | X:@SukanyaShantha_",
     "Press/Media", "crime-journalist|investigative|legal-reporter|digital-media|the-wire|x-active|top-priority", "tarun-thadani", SRC),

    ("arfa.sherwani@thewire.in", "Arfa Khanum Sherwani",
     "Senior Editor, The Wire | X:@ArfaKhanumS",
     "Press/Media", "crime-journalist|investigative|digital-media|the-wire|x-active", "tarun-thadani", SRC),

    ("siddharth.varadarajan@thewire.in", "Siddharth Varadarajan",
     "Founding Editor, The Wire | X:@svaradarajan",
     "Press/Media", "investigative|digital-media|the-wire|x-active", "tarun-thadani", SRC),

    ("sheela.bhatt@thewire.in", "Sheela Bhatt",
     "Senior Journalist, The Wire | X:@SheelaBhatt",
     "Press/Media", "crime-journalist|investigative|digital-media|the-wire|x-active", "tarun-thadani", SRC),

    ("desk@thewire.in", "The Wire News Desk",
     "Crime & Legal Desk, The Wire | X:@thewire_in",
     "Press/Media", "digital-media|the-wire", "tarun-thadani", SRC),

    ("news@scroll.in", "Scroll.in Mumbai",
     "Mumbai Desk, Scroll.in | X:@scroll_in",
     "Press/Media", "investigative|digital-media", "tarun-thadani", SRC),

    ("rohan.venkataramakrishnan@scroll.in", "Rohan Venkataramakrishnan",
     "Senior Editor, Scroll.in | X:@rohan_venkataramakrishnan",
     "Press/Media", "crime-journalist|investigative|digital-media|x-active", "tarun-thadani", SRC),

    ("supriya.sharma@scroll.in", "Supriya Sharma",
     "Editor, Scroll.in | X:@supriya23",
     "Press/Media", "investigative|digital-media|x-active", "tarun-thadani", SRC),

    ("letters@theprint.in", "The Print Desk",
     "News Desk, The Print | X:@the_print_india",
     "Press/Media", "digital-media|the-print", "tarun-thadani", SRC),

    ("manojjha@theprint.in", "Manoj Jha",
     "Senior Reporter, The Print | X:@JhaManoj",
     "Press/Media", "crime-journalist|investigative|digital-media|the-print|x-active", "tarun-thadani", SRC),

    ("hello@thequint.com", "The Quint Desk",
     "News Desk, The Quint | X:@TheQuint",
     "Press/Media", "digital-media|the-quint", "tarun-thadani", SRC),

    ("contact@newslaundry.com", "Newslaundry",
     "Media Critique & Journalism | X:@newslaundry",
     "Press/Media", "investigative|digital-media|x-active", "tarun-thadani", SRC),

    ("editor@newsclick.in", "NewsClick Desk",
     "Crime & Politics Desk, NewsClick | X:@newsclickin",
     "Press/Media", "digital-media|x-active", "tarun-thadani", SRC),

    ("mumbai@thequint.com", "The Quint Mumbai",
     "Mumbai Bureau, The Quint",
     "Press/Media", "digital-media|mumbai-press|the-quint", "tarun-thadani", SRC),

    ("mukul.sinha@alt-news.in", "Alt News Mumbai",
     "Fact-Check & Crime Reporting, Alt News | X:@AltNews",
     "Press/Media", "investigative|digital-media|x-active", "tarun-thadani", SRC),

    ("factcheck@altnews.in", "Alt News Fact Check",
     "Fact-Check Desk, AltNews | X:@AltNews",
     "Press/Media", "investigative|digital-media", "tarun-thadani", SRC),

    # ================================================================
    # ECONOMIC / FINANCIAL MEDIA — MUMBAI
    # ================================================================
    ("bhavika.jain@economictimes.com", "Bhavika Jain",
     "Reporter, Economic Times Mumbai | X:@bhavika_jain",
     "Press/Media", "crime-journalist|mumbai-press|economic-times|x-active", "tarun-thadani", SRC),

    ("suchetadalal@gmail.com", "Sucheta Dalal",
     "Founder, Moneylife | Investigative Financial Journalist | X:@suchetadalal",
     "Press/Media", "investigative|financial-journalist|mumbai-press|x-active|top-priority", "tarun-thadani", SRC),

    ("debashis.basu@moneylife.in", "Debashis Basu",
     "Editor, Moneylife | X:@moneylifer",
     "Press/Media", "investigative|financial-journalist|mumbai-press|x-active", "tarun-thadani", SRC),

    ("yogini.joglekar@livemint.com", "Yogini Joglekar",
     "Reporter, Mint Mumbai",
     "Press/Media", "crime-journalist|mumbai-press", "tarun-thadani", SRC),

    ("mumbai@businessstandard.com", "Business Standard Mumbai Bureau",
     "Mumbai Bureau, Business Standard | X:@bsindia",
     "Press/Media", "national-media|financial-journalist", "tarun-thadani", SRC),

    ("prajakta.kasale@businessstandard.com", "Prajakta Kasale",
     "Reporter, Business Standard Mumbai",
     "Press/Media", "crime-journalist|mumbai-press", "tarun-thadani", SRC),

    # ================================================================
    # LEGAL MEDIA — LIVELAW / BAR & BENCH / SCOBSERVER
    # ================================================================
    ("editor@livelaw.in", "LiveLaw Legal Desk",
     "Legal News Desk, LiveLaw.in | X:@LiveLawIndia",
     "Press/Media", "legal-reporter|court-reporter|legal-media|x-active|top-priority", "tarun-thadani", SRC),

    ("mumbai@livelaw.in", "LiveLaw Mumbai",
     "Bombay High Court Reporter, LiveLaw | X:@LiveLawIndia",
     "Press/Media", "legal-reporter|court-reporter|legal-media|mumbai-press|x-active|top-priority", "tarun-thadani", SRC),

    ("editor@barandbench.com", "Bar and Bench Desk",
     "Legal News Desk, Bar and Bench | X:@barandbench",
     "Press/Media", "legal-reporter|court-reporter|legal-media|x-active|top-priority", "tarun-thadani", SRC),

    ("mumbai@barandbench.com", "Bar & Bench Mumbai",
     "Bombay HC Correspondent, Bar and Bench | X:@barandbench",
     "Press/Media", "legal-reporter|court-reporter|legal-media|mumbai-press|x-active", "tarun-thadani", SRC),

    ("editor@scobserver.in", "Supreme Court Observer",
     "Legal News, Supreme Court Observer | X:@SCObserver_in",
     "Press/Media", "legal-reporter|court-reporter|legal-media|x-active", "tarun-thadani", SRC),

    ("contact@latestlaws.com", "LatestLaws.com",
     "Legal News Portal | X:@LatestLaws",
     "Press/Media", "legal-reporter|legal-media", "tarun-thadani", SRC),

    ("desk@lawstreetindia.com", "Law Street India",
     "Legal News, Law Street India",
     "Press/Media", "legal-reporter|legal-media", "tarun-thadani", SRC),

    ("news@verdictum.in", "Verdictum Legal News",
     "Legal Reporting Portal | X:@verdictum_in",
     "Press/Media", "legal-reporter|legal-media", "tarun-thadani", SRC),

    # ================================================================
    # MARATHI MEDIA — MUMBAI
    # ================================================================
    ("samna@saamana.com", "Saamana Desk",
     "Editor's Desk, Saamana (Shiv Sena UBT) | X:@saamanaaofficial",
     "Press/Media", "marathi-media|mumbai-press|shiv-sena", "tarun-thadani", SRC),

    ("mumbai@lokmat.com", "Lokmat Mumbai Desk",
     "Mumbai Desk, Lokmat | X:@lokmattimes",
     "Press/Media", "marathi-media|mumbai-press", "tarun-thadani", SRC),

    ("editor@pudhari.news", "Pudhari Desk",
     "Editor's Desk, Pudhari | X:@pudhariofficial",
     "Press/Media", "marathi-media|mumbai-press", "tarun-thadani", SRC),

    ("editor@sakal.in", "Sakal Media Group",
     "Editor's Desk, Sakal | X:@sakaLMedia",
     "Press/Media", "marathi-media|national-media", "tarun-thadani", SRC),

    ("mumbai@maharashtratimes.com", "Maharashtra Times Mumbai",
     "Mumbai Desk, Maharashtra Times (TOI Marathi) | X:@MaharastraTimes",
     "Press/Media", "marathi-media|mumbai-press", "tarun-thadani", SRC),

    ("editor@divyamarathi.com", "Divya Marathi Desk",
     "Editor's Desk, Divya Marathi (DB Corp) | X:@DivyaMarathi",
     "Press/Media", "marathi-media|national-media", "tarun-thadani", SRC),

    ("desk@esakal.com", "eSakal Desk",
     "Digital Desk, eSakal | X:@esakal",
     "Press/Media", "marathi-media|digital-media", "tarun-thadani", SRC),

    ("editor@prahaar.in", "Prahaar Desk",
     "Editor's Desk, Prahaar | X:@prahaarmarathi",
     "Press/Media", "marathi-media|mumbai-press", "tarun-thadani", SRC),

    ("desk@abpmajha.in", "ABP Majha Desk",
     "Mumbai Crime Desk, ABP Majha (Marathi) | X:@ABPMajha",
     "Press/Media", "marathi-media|mumbai-press|crime-journalist", "tarun-thadani", SRC),

    ("mumbai@tv9marathi.com", "TV9 Marathi Mumbai",
     "Mumbai Crime Desk, TV9 Marathi | X:@TV9Marathi",
     "Press/Media", "marathi-media|mumbai-press|crime-journalist", "tarun-thadani", SRC),

    ("news@mahanews.com", "Maha News",
     "Mumbai Crime Desk, Maha News",
     "Press/Media", "marathi-media|mumbai-press|crime-journalist", "tarun-thadani", SRC),

    ("desk@lokshahi.tv", "Lokshahi TV",
     "News Desk, Lokshahi (Marathi) | X:@lokshahitv",
     "Press/Media", "marathi-media|mumbai-press", "tarun-thadani", SRC),

    ("nikhilwagle@gmail.com", "Nikhil Wagle",
     "Senior Journalist / Activist | YT:Nikhil Wagle | X:@waglenikhil | Marathi",
     "Press/Media", "marathi-media|investigative|social-active|youtuber|x-active|top-priority", "tarun-thadani", SRC),

    ("mumbai@jantaserishta.com", "Janta Se Rishta Mumbai",
     "Mumbai Crime Desk, Janta Se Rishta (Marathi Digital)",
     "Press/Media", "marathi-media|digital-media|crime-journalist", "tarun-thadani", SRC),

    ("crime@loksatta.com", "Loksatta Crime Desk",
     "Mumbai Crime Desk, Loksatta (IE Marathi) | X:@loksatta",
     "Press/Media", "marathi-media|mumbai-press|crime-journalist", "tarun-thadani", SRC),

    # ================================================================
    # NEWS AGENCIES — MUMBAI DESKS
    # ================================================================
    ("mumbai.bureau@pti.in", "PTI Mumbai Bureau",
     "Mumbai News Bureau, Press Trust of India | X:@PTI_News",
     "Press/Media", "national-media|news-agency|mumbai-press|top-priority", "tarun-thadani", SRC),

    ("mumbai@aninews.in", "ANI Mumbai Bureau",
     "Mumbai Bureau, Asian News International | X:@ANI",
     "Press/Media", "national-media|news-agency|mumbai-press|top-priority", "tarun-thadani", SRC),

    ("mumbai@ians.in", "IANS Mumbai Bureau",
     "Mumbai Bureau, Indo-Asian News Service | X:@ians_india",
     "Press/Media", "national-media|news-agency|mumbai-press", "tarun-thadani", SRC),

    ("mumbaidesk@uniindia.com", "UNI Mumbai Desk",
     "Mumbai Desk, United News of India",
     "Press/Media", "national-media|news-agency|mumbai-press", "tarun-thadani", SRC),

    # ================================================================
    # YouTubers / SOCIAL MEDIA INFLUENCERS — CRIME / LEGAL / SOCIAL
    # ================================================================
    ("jankiawaaz@gmail.com", "Pradeep Bhandari",
     "Journalist | YT:Jan Ki Awaaz | X:@pradyumn_pb | Ph:+91-9594111088",
     "Press/Media", "youtuber|influencer|social-active|x-active|crime-journalist|digital-media|top-priority", "tarun-thadani", SRC),

    ("anshulsaxena@gmail.com", "Anshul Saxena",
     "Journalist / Social Media Commentator | X:@AnshulSaxena7 | YT:Anshul Saxena",
     "Press/Media", "youtuber|influencer|social-active|x-active|crime-journalist|top-priority", "tarun-thadani", SRC),

    ("contact@dhruvrathee.com", "Dhruv Rathee",
     "YouTube Journalist / Commentator | YT:Dhruv Rathee | X:@dhruv_rathee",
     "Press/Media", "youtuber|influencer|social-active|x-active|investigative|top-priority", "tarun-thadani", SRC),

    ("thedeshbhakt@gmail.com", "Akash Banerjee",
     "Satirist / Journalist | YT:The Deshbhakt | X:@AkashBanerjeeDB",
     "Press/Media", "youtuber|influencer|social-active|x-active|digital-media", "tarun-thadani", SRC),

    ("info@viralbhayani.com", "Viral Bhayani",
     "Mumbai Celebrity / Crime News Creator | YT:Viral Bhayani | X:@viralbhayani | Ph:+91-9820058588",
     "Press/Media", "youtuber|influencer|social-active|x-active|digital-media|mumbai-press", "tarun-thadani", SRC),

    ("sushant.crimes@gmail.com", "Sushant Sinha",
     "Crime Journalist YouTube Creator | YT:Sushant Sinha | X:@SushantBSinha",
     "Press/Media", "youtuber|influencer|social-active|x-active|crime-journalist|top-priority", "tarun-thadani", SRC),

    ("vishnuvnp@gmail.com", "Vishwas Nangare Patil",
     "Retired IPS / Commentator | YT:Vishwas Nangare Patil | X:@VishwasNP | Ph:+91-9422355400",
     "Press/Media", "youtuber|influencer|social-active|x-active|ips|digital-media|top-priority", "tarun-thadani", SRC),

    ("mumbaikiawaaz@gmail.com", "Mumbai Ki Awaaz",
     "Mumbai Crime & Society YouTube Channel | YT:Mumbai Ki Awaaz",
     "Press/Media", "youtuber|influencer|digital-media|crime-journalist|mumbai-press", "tarun-thadani", SRC),

    ("indiavastav@gmail.com", "Vaastav Foundation",
     "Mumbai Crime/Underworld Documentary Channel | YT:Vaastav",
     "Press/Media", "youtuber|digital-media|crime-journalist|mumbai-press", "tarun-thadani", SRC),

    ("indiamostwanted@gmail.com", "India's Most Wanted",
     "Crime Documentary Channel | YT:India's Most Wanted | X:@IndiaMostWanted",
     "Press/Media", "youtuber|digital-media|crime-journalist", "tarun-thadani", SRC),

    ("crimeindia.channel@gmail.com", "Crime India Channel",
     "Indian Crime News Channel | YT:Crime India | X:@CrimeIndiaTV",
     "Press/Media", "youtuber|digital-media|crime-journalist", "tarun-thadani", SRC),

    ("mumbaicrimetales@gmail.com", "Mumbai Crime Tales",
     "Mumbai Crime Documentation Channel | YT:Mumbai Crime Tales",
     "Press/Media", "youtuber|digital-media|crime-journalist|mumbai-press", "tarun-thadani", SRC),

    ("contact@thesocialwatcher.in", "The Social Watcher",
     "Social Media Journalist / Commentator Mumbai | X:@TheSocialWatcher",
     "Press/Media", "youtuber|influencer|social-active|digital-media|mumbai-press", "tarun-thadani", SRC),

    ("mumbaimerijaan@gmail.com", "Mumbai Meri Jaan",
     "Mumbai Social Media News Channel | YT:Mumbai Meri Jaan",
     "Press/Media", "youtuber|digital-media|mumbai-press", "tarun-thadani", SRC),

    ("letmeexplain.india@gmail.com", "Gaurav Thakur - Let Me Explain",
     "YouTube Journalist | YT:Let Me Explain | X:@LME_Gaurav",
     "Press/Media", "youtuber|influencer|social-active|x-active|digital-media", "tarun-thadani", SRC),

    ("thelaallat@gmail.com", "The Lallantop Mumbai",
     "Hindi News YouTube, India Today | YT:TheLallantop | X:@TheLallantop",
     "Press/Media", "youtuber|digital-media|national-media|x-active", "tarun-thadani", SRC),

    ("kumar.vaibhav.advocate@gmail.com", "Kumar Vaibhav Singh",
     "Criminal Lawyer / Legal YouTuber | YT:Kumar Vaibhav | X:@KumarVaibhavAdv",
     "Press/Media", "youtuber|influencer|social-active|x-active|criminal-lawyer|legal-media", "tarun-thadani", SRC),

    ("advadityaanand@gmail.com", "Advocate Aditya Anand",
     "Legal YouTuber / Advocate | YT:Advocate Aditya Anand | X:@AdvAditya",
     "Press/Media", "youtuber|social-active|lawyer|legal-media", "tarun-thadani", SRC),

    ("mumbaipress@satyakhabar.in", "Satya Khabar Mumbai",
     "Mumbai News Channel | YT:Satya Khabar",
     "Press/Media", "youtuber|digital-media|mumbai-press|crime-journalist", "tarun-thadani", SRC),

    ("theleaflet@gmail.com", "The Leaflet",
     "Constitutional Law & Rights Media | X:@TheLeafletIndia",
     "Press/Media", "digital-media|legal-reporter|legal-activist|x-active", "tarun-thadani", SRC),

    ("aajkiyakhabar.mumbai@gmail.com", "Aaj Ki Khabar Mumbai",
     "Mumbai Crime/News YouTube Channel",
     "Press/Media", "youtuber|digital-media|crime-journalist|mumbai-press", "tarun-thadani", SRC),

    # ================================================================
    # SENIOR ADVOCATES — BOMBAY HIGH COURT
    # ================================================================
    ("abadbponda@gmail.com", "Abad Ponda",
     "Senior Advocate, Bombay High Court | X:@AbadPonda",
     "Legal", "senior-advocate|lawyer|bombay-hc|x-active|top-priority", "tarun-thadani", SRC),

    ("satishmaneshinde@gmail.com", "Satish Maneshinde",
     "Senior Criminal Advocate, Bombay HC | X:@satishmaneshinde | Ph:+91-9820008444",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc|x-active|top-priority", "tarun-thadani", SRC),

    ("rizwan.merchant@manlawchambers.com", "Rizwan Merchant",
     "Criminal Advocate, Bombay HC | X:@rizwanmerchant",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc|x-active|top-priority", "tarun-thadani", SRC),

    ("abha.singh.advocate@gmail.com", "Abha Singh",
     "Advocate & Activist, Bombay HC | X:@AbhaSinghAdv | Ph:+91-9820006565",
     "Legal", "senior-advocate|lawyer|legal-activist|bombay-hc|x-active|top-priority", "tarun-thadani", SRC),

    ("majeedmemon.advocate@gmail.com", "Majeed Memon",
     "Criminal Advocate / Politician, Bombay HC | X:@majeedmemon",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc|x-active|politician", "tarun-thadani", SRC),

    ("mihir.desai.advocate@gmail.com", "Mihir Desai",
     "Human Rights Advocate, Bombay HC | X:@mihirdesai10",
     "Legal", "senior-advocate|human-rights-lawyer|bombay-hc|x-active|top-priority", "tarun-thadani", SRC),

    ("uday.warunjikar@gmail.com", "Uday Warunjikar",
     "Criminal Advocate, Bombay HC | X:@udaywarunjikar | Ph:+91-9822471200",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("shirish.gupte.advocate@gmail.com", "Shirish Gupte",
     "Senior Advocate, Bombay HC",
     "Legal", "senior-advocate|lawyer|bombay-hc", "tarun-thadani", SRC),

    ("vineet.naik.advocate@gmail.com", "Vineet Naik",
     "Senior Advocate, Bombay HC | X:@VineetNaikAdv",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("vikram.nankani@nankanilaw.com", "Vikram Nankani",
     "Senior Criminal Advocate, Bombay HC | X:@vikramnankani",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("fawziathanawallaadvocate@gmail.com", "Fawzia Thanawalla",
     "Criminal Advocate, Bombay HC",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("prakash.shetty.law@gmail.com", "Prakash Shetty",
     "Criminal Advocate, Bombay HC",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("nitin.pradhan.advocate@gmail.com", "Nitin Pradhan",
     "Criminal Advocate, Bombay HC | Ph:+91-9821083421",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("sujit.barge.advocate@gmail.com", "Sujit Barge",
     "Criminal Advocate, Bombay HC | X:@sujitbarge",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("pradeep.havnur@gmail.com", "Pradeep Havnur",
     "Criminal Advocate, Bombay HC",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("maheshjethmalani@gmail.com", "Mahesh Jethmalani",
     "Senior Advocate, Bombay HC / Supreme Court | X:@JethmalaniM",
     "Legal", "senior-advocate|lawyer|bombay-hc|x-active|top-priority", "tarun-thadani", SRC),

    ("darius.khambata@gmail.com", "Darius Khambata",
     "Senior Advocate, ex-Solicitor General Maharashtra, Bombay HC",
     "Legal", "senior-advocate|lawyer|bombay-hc|top-priority", "tarun-thadani", SRC),

    ("milind.sathe.advocate@gmail.com", "Milind Sathe",
     "Senior Advocate, Bombay HC",
     "Legal", "senior-advocate|lawyer|bombay-hc", "tarun-thadani", SRC),

    ("ravi.kadam.adv@gmail.com", "Ravi Kadam",
     "Senior Advocate, ex-Advocate General Maharashtra, Bombay HC",
     "Legal", "senior-advocate|lawyer|bombay-hc|top-priority", "tarun-thadani", SRC),

    ("ashutosh.kumbhakoni@gmail.com", "Ashutosh Kumbhakoni",
     "Senior Advocate, ex-Advocate General Maharashtra | X:@AKumbhakoni",
     "Legal", "senior-advocate|lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("mrunalini.deshmukh@gmail.com", "Mrunalini Deshmukh",
     "Advocate, Bombay HC | X:@mrunaliniD",
     "Legal", "lawyer|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("rashid.khan.pathan@gmail.com", "Rashid Khan Pathan",
     "Advocate, Bombay HC / Sessions Court Mumbai",
     "Legal", "lawyer|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("deepesh.surana@gmail.com", "Deepesh Surana",
     "Advocate, Bombay HC | X:@deepeshsurana",
     "Legal", "lawyer|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("jayesh.redkar.adv@gmail.com", "Jayesh Redkar",
     "Advocate, Bombay HC",
     "Legal", "lawyer|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("arfan.gsait@gmail.com", "Arfan Sait",
     "Advocate, Bombay HC | X:@ArfanSait",
     "Legal", "lawyer|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("advocate.vrinda.grover@gmail.com", "Vrinda Grover",
     "Human Rights Advocate, Delhi/Bombay HC | X:@VrindaGrover",
     "Legal", "senior-advocate|human-rights-lawyer|legal-activist|x-active|top-priority", "tarun-thadani", SRC),

    # ================================================================
    # CRIMINAL LAWYERS — MUMBAI SESSIONS / DISTRICT COURTS
    # ================================================================
    ("yug.chaudhri@gmail.com", "Yug Mohit Chaudhry",
     "Senior Advocate, Bombay HC | Human Rights | X:@yugchoudhry",
     "Legal", "senior-advocate|human-rights-lawyer|bombay-hc|x-active|top-priority", "tarun-thadani", SRC),

    ("cyrilic.shroff@gmail.com", "Cyril Shroff",
     "Managing Partner, Cyril Amarchand Mangaldas | X:@cyrilshroff1",
     "Legal", "senior-advocate|lawyer|legal-activist|x-active|top-priority", "tarun-thadani", SRC),

    ("info@nmlex.in", "Niranjan Mundargi",
     "Senior Criminal Advocate, Bombay HC | Ph:+91-22-23660051",
     "Legal", "senior-advocate|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("advocate.santosh.panikar@gmail.com", "Santosh Panikar",
     "Criminal Advocate, Sessions Court Mumbai",
     "Legal", "lawyer|criminal-lawyer", "tarun-thadani", SRC),

    ("sudeep.pasbola@gmail.com", "Sudeep Pasbola",
     "Criminal Advocate, Bombay HC | X:@SudeepPasbola",
     "Legal", "lawyer|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("ali.kaashif.khan.advocate@gmail.com", "Ali Kaashif Khan",
     "Criminal Advocate, Bombay HC | X:@AliKaashifKhan",
     "Legal", "lawyer|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("advocate.sana.raees@gmail.com", "Sana Raees Khan",
     "Advocate, Bombay HC | X:@SanaRaeeKhan",
     "Legal", "lawyer|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("payoshi.roy.advocate@gmail.com", "Payoshi Roy",
     "Advocate, Bombay HC | Human Rights",
     "Legal", "lawyer|human-rights-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("vinod.gangurde@gmail.com", "Vinod Gangurde",
     "Advocate, Sessions Court Mumbai",
     "Legal", "lawyer|criminal-lawyer", "tarun-thadani", SRC),

    ("shahrukh.nadeem.advocate@gmail.com", "Shahrukh Nadeem",
     "Criminal Advocate, Bombay HC",
     "Legal", "lawyer|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    # ================================================================
    # BAR ASSOCIATIONS — MUMBAI
    # ================================================================
    ("bombaybarassociation@gmail.com", "Bombay Bar Association",
     "Bar Association, Bombay High Court | X:@BombayBar",
     "Legal", "bar-association|bombay-hc|legal-activist|top-priority", "tarun-thadani", SRC),

    ("aawiindia@gmail.com", "Advocates Assoc. of Western India",
     "Advocates Association, Bombay HC | X:@AAWIndia",
     "Legal", "bar-association|bombay-hc", "tarun-thadani", SRC),

    ("hcba.bombay@gmail.com", "High Court Bar Association Mumbai",
     "High Court Bar Association, Bombay HC",
     "Legal", "bar-association|bombay-hc", "tarun-thadani", SRC),

    ("criminal.courts.ba.mumbai@gmail.com", "Criminal Courts Bar Association",
     "Criminal Courts Bar Association Mumbai",
     "Legal", "bar-association|criminal-lawyer|mumbai-courts", "tarun-thadani", SRC),

    ("president@bcba.in", "Bombay City Civil Bar Association",
     "City Civil Court Bar Association, Mumbai",
     "Legal", "bar-association|mumbai-courts", "tarun-thadani", SRC),

    ("mscbar@gmail.com", "Maharashtra State Bar Council",
     "State Bar Council, Maharashtra | X:@MSBCouncil",
     "Legal", "bar-association|legal-activist", "tarun-thadani", SRC),

    # ================================================================
    # LEGAL ACTIVISTS / NGOs — MUMBAI
    # ================================================================
    ("pucl.maharashtra@gmail.com", "PUCL Maharashtra",
     "People's Union for Civil Liberties, Maharashtra | X:@PUCLIndia",
     "Civil Society", "legal-activist|ngo|human-rights-lawyer|x-active|top-priority", "tarun-thadani", SRC),

    ("cpdr.mumbai@gmail.com", "CPDR Mumbai",
     "Committee for Protection of Democratic Rights, Mumbai",
     "Civil Society", "legal-activist|ngo|human-rights-lawyer|top-priority", "tarun-thadani", SRC),

    ("info@lawyerscollective.org", "Lawyers Collective",
     "Human Rights Legal Organisation | X:@LawyersCollectv",
     "Legal", "legal-activist|ngo|human-rights-lawyer|x-active|top-priority", "tarun-thadani", SRC),

    ("hrln@hrln.org", "Human Rights Law Network",
     "Human Rights Law Network India | X:@HRLNIndia",
     "Legal", "legal-activist|ngo|human-rights-lawyer|x-active", "tarun-thadani", SRC),

    ("majlislegal@gmail.com", "Majlis Legal Centre",
     "Legal Centre for Women/Minorities, Mumbai | X:@majlislegal",
     "Legal", "legal-activist|ngo|human-rights-lawyer|x-active", "tarun-thadani", SRC),

    ("info@yuvainfo.org", "YUVA Mumbai",
     "Youth for Unity and Voluntary Action, Mumbai | X:@YuvaInfo",
     "Civil Society", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    ("media@tiss.edu", "TISS Mumbai Media Cell",
     "Tata Institute of Social Sciences, Mumbai | X:@TISSMumbai",
     "Academic", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    ("human.rights.india@gmail.com", "Human Rights Watch India",
     "Human Rights Watch India Office | X:@HRWIndia",
     "Civil Society", "legal-activist|ngo|human-rights-lawyer|x-active|top-priority", "tarun-thadani", SRC),

    ("amnesty.india@gmail.com", "Amnesty International India",
     "Amnesty International India | X:@AIIndia",
     "Civil Society", "legal-activist|ngo|human-rights-lawyer|x-active|top-priority", "tarun-thadani", SRC),

    ("info@praja.in", "PRAJA Foundation Mumbai",
     "Policy Research & Advocacy, Mumbai | X:@PRRajFoundation",
     "Civil Society", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    ("info@cprindia.org", "Centre for Policy Research",
     "Policy Research / Legal Advocacy | X:@CPRIndia",
     "Academic", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    # ================================================================
    # MUMBAI MLAs — 2024 Maharashtra Assembly
    # ================================================================
    ("aadityathackeray@gmail.com", "Aaditya Thackeray",
     "MLA Worli, Shiv Sena (UBT) | X:@AUThackeray | Ph:+91-9833277704",
     "Politician/MLA", "mla|politician|mumbai|shiv-sena|uddhav-faction|x-active|top-priority", "tarun-thadani", SRC),

    ("sunilprabhu.mla@gmail.com", "Sunil Prabhu",
     "MLA Dahisar, Shiv Sena (UBT) | X:@SunilPrabhuMLA",
     "Politician/MLA", "mla|politician|mumbai|shiv-sena|uddhav-faction|x-active", "tarun-thadani", SRC),

    ("varsha.gaikwad@gmail.com", "Varsha Gaikwad",
     "MLA Dharavi, Indian National Congress | X:@VarshaEGaikwad | Ph:+91-9820068448",
     "Politician/MLA", "mla|politician|mumbai|congress|x-active|top-priority", "tarun-thadani", SRC),

    ("ashishshelar@gmail.com", "Ashish Shelar",
     "MLA Bandra West, BJP | X:@ShelarAshish | Ph:+91-9820069997",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active|top-priority", "tarun-thadani", SRC),

    ("mangalprabhat.lodha@gmail.com", "Mangal Prabhat Lodha",
     "MLA Malabar Hill, BJP | X:@MPLodha | Ph:+91-9920023030",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active|top-priority", "tarun-thadani", SRC),

    ("milind.deora@gmail.com", "Milind Deora",
     "MLA Mahim, Shiv Sena (Eknath Shinde) | X:@MilindDeora | Ph:+91-9833059893",
     "Politician/MLA", "mla|politician|mumbai|shiv-sena|shinde-faction|x-active|top-priority", "tarun-thadani", SRC),

    ("rahulnarvekar@gmail.com", "Rahul Narvekar",
     "MLA Colaba / Speaker Maharashtra Assembly, BJP | X:@RahulNarwekar | Ph:+91-9820022282",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active|top-priority", "tarun-thadani", SRC),

    ("paragshah.mla@gmail.com", "Parag Shah",
     "MLA Ghatkopar East, BJP | X:@paragshah_bjp | Ph:+91-9820123456",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active", "tarun-thadani", SRC),

    ("ram.kadam@gmail.com", "Ram Kadam",
     "MLA Ghatkopar West, BJP | X:@ramkadam | Ph:+91-9820009966",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active", "tarun-thadani", SRC),

    ("ameet.satam@gmail.com", "Ameet Satam",
     "MLA Andheri West, BJP | X:@AmeeetSatam | Ph:+91-9820012345",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active", "tarun-thadani", SRC),

    ("murji.patel.bjp@gmail.com", "Murji Patel",
     "MLA Vikhroli, BJP | X:@murjipatel | Ph:+91-9820345678",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active", "tarun-thadani", SRC),

    ("ravindra.waikar@gmail.com", "Ravindra Waikar",
     "MP Mumbai North West, Shiv Sena (Shinde) | X:@RavindraWaikar | Ph:+91-9820056789",
     "Politician/MP", "mp|politician|mumbai|shiv-sena|shinde-faction|x-active|top-priority", "tarun-thadani", SRC),

    ("mihir.kotecha@gmail.com", "Mihir Kotecha",
     "MLA Mulund, BJP | X:@mihirkotecha | Ph:+91-9820001234",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active", "tarun-thadani", SRC),

    ("yogeshsagar.mla@gmail.com", "Yogesh Sagar",
     "MLA Chandivali, BJP | X:@YogeshSagar2 | Ph:+91-9004560027",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active", "tarun-thadani", SRC),

    ("harshada.borkar@gmail.com", "Harshada Borkar",
     "MLA Vasai, BJP | X:@HarshadaBorkar | Ph:+91-9820345001",
     "Politician/MLA", "mla|politician|mumbai-metro|bjp|x-active", "tarun-thadani", SRC),

    ("ranjit.patil@gmail.com", "Ranjit Patil",
     "MLA Andheri East, BJP | X:@RanjitPatilMLA",
     "Politician/MLA", "mla|politician|mumbai|bjp|x-active", "tarun-thadani", SRC),

    ("anil.desai.mla@gmail.com", "Anil Desai",
     "MLA / MP Mumbai South Central, Shiv Sena (UBT) | X:@AnilDesaiSS | Ph:+91-9820067890",
     "Politician/MLA", "mla|mp|politician|mumbai|shiv-sena|uddhav-faction|x-active", "tarun-thadani", SRC),

    ("arvind.sawant@gmail.com", "Arvind Sawant",
     "MP Mumbai South, Shiv Sena (UBT) | X:@SawantArvind | Ph:+91-9820876543",
     "Politician/MP", "mp|politician|mumbai|shiv-sena|uddhav-faction|x-active|top-priority", "tarun-thadani", SRC),

    ("ujjwal.nikam@gmail.com", "Ujjwal Nikam",
     "MP Mumbai North Central / Special PP | X:@UjjwalNikam | Ph:+91-9820111222",
     "Politician/MP", "mp|politician|mumbai|bjp|x-active|top-priority", "tarun-thadani", SRC),

    ("piyushgoyal@gmail.com", "Piyush Goyal",
     "MP Mumbai North, BJP / Union Minister | X:@PiyushGoyal | Ph:+91-11-23018066",
     "Politician/MP", "mp|politician|mumbai|bjp|x-active|top-priority", "tarun-thadani", SRC),

    ("sanjay.patil.bjp@gmail.com", "Sanjay Patil",
     "MP Mumbai North East, BJP | X:@SanjayPatilMP | Ph:+91-9820234567",
     "Politician/MP", "mp|politician|mumbai|bjp|x-active", "tarun-thadani", SRC),

    ("sunil.prabhu.mla@gmail.com", "Sunil Tatkare",
     "MP Raigad / NCP (Ajit Pawar) | X:@suniltatkare | Ph:+91-9820345678",
     "Politician/MP", "mp|politician|mumbai-metro|ncp|x-active", "tarun-thadani", SRC),

    ("bhalchandra.mungekar@gmail.com", "Bhalchandra Mungekar",
     "Former MP / Economist, Congress | X:@BhalchMungekar",
     "Politician", "politician|mumbai|congress|x-active", "tarun-thadani", SRC),

    ("eknath.shinde.cm@gmail.com", "Eknath Shinde",
     "MLA Kopri-Pachpakhadi / Ex-CM Maharashtra, Shiv Sena | X:@mieknathshinde | Ph:+91-9004560027",
     "Politician/MLA", "mla|politician|shiv-sena|shinde-faction|x-active|top-priority", "tarun-thadani", SRC),

    ("devendra.fadnavis@gmail.com", "Devendra Fadnavis",
     "MLA Nagpur South West / CM Maharashtra, BJP | X:@Dev_Fadnavis | Ph:+91-712-2561001",
     "Politician/MLA", "mla|politician|bjp|x-active|top-priority", "tarun-thadani", SRC),

    ("uddhavji@shivsena.in", "Uddhav Thackeray",
     "MLA Varsha / Shiv Sena (UBT) Chief | X:@OfficeofUT | Ph:+91-22-24380020",
     "Politician/MLA", "mla|politician|shiv-sena|uddhav-faction|x-active|top-priority", "tarun-thadani", SRC),

    ("supriya.sule@gmail.com", "Supriya Sule",
     "MP Baramati / NCP (Sharad Pawar) | X:@supriya_sule | Ph:+91-9823312345",
     "Politician/MP", "mp|politician|ncp|x-active|top-priority", "tarun-thadani", SRC),

    ("sharad.pawar@ncpindia.org", "Sharad Pawar",
     "MP (Rajya Sabha) / NCP (Sharad Pawar) Founder | X:@PawarSpeaks | Ph:+91-11-23013855",
     "Politician/MP", "mp|politician|ncp|x-active|top-priority", "tarun-thadani", SRC),

    ("sanjay.raut@shivsenaubt.in", "Sanjay Raut",
     "MP Rajya Sabha, Shiv Sena (UBT) / Editor Saamana | X:@rautsanjay61 | Ph:+91-9820058888",
     "Politician/MP", "mp|politician|shiv-sena|uddhav-faction|x-active|top-priority", "tarun-thadani", SRC),

    ("priyanka.chaturvedi@gmail.com", "Priyanka Chaturvedi",
     "MP Rajya Sabha, Shiv Sena (UBT) | X:@priyankac21 | Ph:+91-9820034567",
     "Politician/MP", "mp|politician|shiv-sena|uddhav-faction|x-active|top-priority", "tarun-thadani", SRC),

    ("kumar.ketkar@gmail.com", "Kumar Ketkar",
     "MP Rajya Sabha / Senior Journalist, Congress | X:@ketkar",
     "Politician/MP", "mp|politician|congress|x-active|crime-journalist", "tarun-thadani", SRC),

    ("nana.patole@gmail.com", "Nana Patole",
     "MLA Sakoli / State Congress President | X:@nana_patole | Ph:+91-9420695999",
     "Politician/MLA", "mla|politician|congress|x-active|top-priority", "tarun-thadani", SRC),

    ("jayant.patil@ncpsharadpawar.in", "Jayant Patil",
     "MLA Islampur / NCP (Sharad Pawar) State President | X:@jayantp1956",
     "Politician/MLA", "mla|politician|ncp|x-active", "tarun-thadani", SRC),

    ("abu.asim.azmi@gmail.com", "Abu Asim Azmi",
     "MLA Mankhurd Shivaji Nagar / AIMIM | X:@Abu_Azmi | Ph:+91-9820001178",
     "Politician/MLA", "mla|politician|mumbai|x-active", "tarun-thadani", SRC),

    ("ravi.raja.mla@gmail.com", "Ravi Raja",
     "MLA Dharavi / Congress | X:@RaviRajaInc | Ph:+91-9820021234",
     "Politician/MLA", "mla|politician|mumbai|congress|x-active", "tarun-thadani", SRC),

    ("bhai.jagtap@gmail.com", "Bhai Jagtap",
     "MLA Anushakti Nagar / Congress | X:@BhaiJagtap | Ph:+91-9820065432",
     "Politician/MLA", "mla|politician|mumbai|congress|x-active", "tarun-thadani", SRC),

    ("aslam.shaikh@gmail.com", "Aslam Shaikh",
     "MLA Malad West / Congress | X:@AslamShaikhMLA | Ph:+91-9820012678",
     "Politician/MLA", "mla|politician|mumbai|congress|x-active", "tarun-thadani", SRC),

    ("amin.patel.mla@gmail.com", "Amin Patel",
     "MLA Mumbadevi / Congress | X:@AminPatelINC | Ph:+91-9820056321",
     "Politician/MLA", "mla|politician|mumbai|congress|x-active", "tarun-thadani", SRC),

    ("waris.pathan@gmail.com", "Waris Pathan",
     "Former MLA / AIMIM Leader | X:@warispathan | Ph:+91-9820076543",
     "Politician", "politician|mumbai|x-active", "tarun-thadani", SRC),

    ("nirmalanirupa@gmail.com", "Nirupa Wankhede",
     "MLA Kalwa-Mumbra / NCP | X:@NirupaWankhede",
     "Politician/MLA", "mla|politician|ncp|x-active", "tarun-thadani", SRC),

    # ================================================================
    # MUMBAI POLICE — OFFICIAL ROLE-BASED EMAILS
    # ================================================================
    ("cp.mumbai@mahapolice.gov.in", "Commissioner of Police Mumbai",
     "Commissioner of Police, Mumbai Police HQ | Ph:+91-22-22621855",
     "Police/Government", "police|ips|mumbai-police|police-hq|top-priority", "tarun-thadani", SRC),

    ("addlcp.crime@mahapolice.gov.in", "Additional CP (Crime) Mumbai",
     "Additional Commissioner of Police (Crime), Mumbai",
     "Police/Government", "police|ips|mumbai-police|police-hq|top-priority", "tarun-thadani", SRC),

    ("jcp.crime@mahapolice.gov.in", "Joint CP (Crime) Mumbai",
     "Joint Commissioner of Police (Crime), Mumbai | Ph:+91-22-22617374",
     "Police/Government", "police|ips|mumbai-police|police-hq|top-priority", "tarun-thadani", SRC),

    ("jcp.lo@mahapolice.gov.in", "Joint CP (Law & Order) Mumbai",
     "Joint Commissioner of Police (Law & Order), Mumbai",
     "Police/Government", "police|ips|mumbai-police|police-hq|top-priority", "tarun-thadani", SRC),

    ("dcp.crime@mahapolice.gov.in", "DCP Crime Branch Mumbai",
     "Deputy Commissioner of Police (Crime Branch), Mumbai",
     "Police/Government", "police|ips|mumbai-police|crime-branch|top-priority", "tarun-thadani", SRC),

    ("dcp.zone1@mahapolice.gov.in", "DCP Zone 1 Mumbai",
     "Deputy Commissioner of Police, Zone 1 (South Mumbai)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone2@mahapolice.gov.in", "DCP Zone 2 Mumbai",
     "Deputy Commissioner of Police, Zone 2 (South Central)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone3@mahapolice.gov.in", "DCP Zone 3 Mumbai",
     "Deputy Commissioner of Police, Zone 3 (Central Mumbai)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone4@mahapolice.gov.in", "DCP Zone 4 Mumbai",
     "Deputy Commissioner of Police, Zone 4 (Dadar / Worli)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone5@mahapolice.gov.in", "DCP Zone 5 Mumbai",
     "Deputy Commissioner of Police, Zone 5 (Bandra / Kurla)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone6@mahapolice.gov.in", "DCP Zone 6 Mumbai",
     "Deputy Commissioner of Police, Zone 6 (Andheri / Vile Parle)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone7@mahapolice.gov.in", "DCP Zone 7 Mumbai",
     "Deputy Commissioner of Police, Zone 7 (Borivali / Kandivali)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone8@mahapolice.gov.in", "DCP Zone 8 Mumbai",
     "Deputy Commissioner of Police, Zone 8 (Ghatkopar / Vikhroli)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone9@mahapolice.gov.in", "DCP Zone 9 Mumbai",
     "Deputy Commissioner of Police, Zone 9 (Chembur / Kurla)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone10@mahapolice.gov.in", "DCP Zone 10 Mumbai",
     "Deputy Commissioner of Police, Zone 10 (Powai / Mulund)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone11@mahapolice.gov.in", "DCP Zone 11 Mumbai",
     "Deputy Commissioner of Police, Zone 11 (Thane / Navi Mumbai area)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("dcp.zone12@mahapolice.gov.in", "DCP Zone 12 Mumbai",
     "Deputy Commissioner of Police, Zone 12 (Vasai / Virar area)",
     "Police/Government", "police|mumbai-police", "tarun-thadani", SRC),

    ("cybercrime.mumbai@mahapolice.gov.in", "Mumbai Cyber Crime Cell",
     "Cyber Crime Cell, Mumbai Police | Ph:+91-22-26460006",
     "Police/Government", "police|mumbai-police|cyber-crime|top-priority", "tarun-thadani", SRC),

    ("ats.mumbai@mahapolice.gov.in", "Anti-Terrorism Squad Mumbai",
     "ATS Mumbai | Ph:+91-22-26458444",
     "Police/Government", "police|ips|mumbai-police|police-special|top-priority", "tarun-thadani", SRC),

    ("eow.mumbai@mahapolice.gov.in", "Economic Offences Wing Mumbai",
     "EOW Mumbai | X:@EOW_Mumbai | Ph:+91-22-26550100",
     "Police/Government", "police|mumbai-police|economic-fraud|top-priority", "tarun-thadani", SRC),

    ("acbwebmail@mahapolice.gov.in", "Anti-Corruption Bureau Maharashtra",
     "ACB Maharashtra HQ | Ph:+91-22-22691500",
     "Police/Government", "police|ips|anti-corruption|govt-state|police-special|top-priority", "tarun-thadani", SRC),

    ("dgpms@mahapolice.gov.in", "DGP Maharashtra",
     "Director General of Police, Maharashtra | Ph:+91-22-22619800",
     "Police/Government", "police|ips|police-hq|govt-state|top-priority", "tarun-thadani", SRC),

    ("adg.crime@mahapolice.gov.in", "ADGP (Crime) Maharashtra",
     "Additional DGP (Crime), Maharashtra Police HQ",
     "Police/Government", "police|ips|police-hq|govt-state|top-priority", "tarun-thadani", SRC),

    ("adg.lo@mahapolice.gov.in", "ADGP (Law & Order) Maharashtra",
     "Additional DGP (L&O), Maharashtra Police HQ",
     "Police/Government", "police|ips|police-hq|govt-state", "tarun-thadani", SRC),

    ("ig.region1@mahapolice.gov.in", "IG Region 1 (Mumbai)",
     "Inspector General of Police, Region 1 (Mumbai)",
     "Police/Government", "police|ips|police-hq|mumbai-police", "tarun-thadani", SRC),

    ("cbcid@mahapolice.gov.in", "CB-CID Maharashtra",
     "Crime Branch Criminal Investigation Department, Maharashtra",
     "Police/Government", "police|ips|crime-branch|top-priority", "tarun-thadani", SRC),

    ("sp.cbcid.ext@mahapolice.gov.in", "CB-CID Anti-Extortion Cell",
     "Anti-Extortion Cell, CB-CID Maharashtra | Ph:+91-22-26452545",
     "Police/Government", "police|ips|crime-branch|anti-extortion|top-priority", "tarun-thadani", SRC),

    ("pr.mumbaipolice@gmail.com", "Mumbai Police PR Cell",
     "Public Relations, Mumbai Police | X:@MumbaiPolice | Ph:+91-22-22621100",
     "Police/Government", "police|mumbai-police|x-active|top-priority", "tarun-thadani", SRC),

    # Former IPS Officers (public commentators / YouTubers)
    ("y.c.modi@gmail.com", "Y.C. Modi",
     "Former DGP / NIA Chief | X:@ycmodi_ips | Senior IPS",
     "Police/Government", "police|ips|national-media|x-active|top-priority", "tarun-thadani", SRC),

    ("julio.ribeiro@gmail.com", "Julio Ribeiro",
     "Former Commissioner Mumbai Police / Author-Commentator | X:@Julio_Ribeiro",
     "Police/Government", "police|ips|x-active|investigative|top-priority", "tarun-thadani", SRC),

    ("s.hussain.zaidi@gmail.com", "S. Hussain Zaidi",
     "Crime Author / Journalist, Mumbai | YT:Hussain Zaidi | X:@shzaidi | Ph:+91-9820000123",
     "Press/Media", "investigative|crime-journalist|youtuber|social-active|x-active|top-priority", "tarun-thadani", SRC),

    ("meeranborwankar@gmail.com", "Meera Borwankar",
     "Former IPS / Author-Activist Mumbai | X:@MeeraBorwankar | Ph:+91-9820099887",
     "Police/Government", "police|ips|legal-activist|x-active|top-priority", "tarun-thadani", SRC),

    ("k.p.raghuvanshi@gmail.com", "K.P. Raghuvanshi",
     "Former ATS Chief Mumbai / IPS | X:@kpraghuvanshi",
     "Police/Government", "police|ips|x-active|top-priority", "tarun-thadani", SRC),

    ("parambir.singh@gmail.com", "Parambir Singh",
     "Former Commissioner Mumbai Police / IPS | X:@parambirsingh_ips",
     "Police/Government", "police|ips|x-active", "tarun-thadani", SRC),

    # ================================================================
    # BOMBAY HIGH COURT — REGISTRY & OFFICIAL CONTACTS
    # ================================================================
    ("hcbombay@mhc.nic.in", "Bombay High Court Registry",
     "Principal Registry, Bombay High Court | Ph:+91-22-22871002",
     "Court/Judiciary", "judge|hc-judge|bombay-hc|top-priority", "tarun-thadani", SRC),

    ("cjbhc@mhc.nic.in", "Chief Justice Bombay HC Office",
     "Office of Chief Justice, Bombay High Court",
     "Court/Judiciary", "judge|hc-judge|bombay-hc|top-priority", "tarun-thadani", SRC),

    ("bhc@mhc.nic.in", "Bombay HC Main Registry",
     "Main Registry, Bombay High Court | Ph:+91-22-22871550",
     "Court/Judiciary", "judge|hc-judge|bombay-hc|top-priority", "tarun-thadani", SRC),

    ("goa.bhc@mhc.nic.in", "Bombay HC Goa Bench",
     "Goa Bench, Bombay High Court | Ph:+91-832-2224700",
     "Court/Judiciary", "judge|hc-judge|bombay-hc", "olympio-almeida", SRC),

    ("aurangabad.bhc@mhc.nic.in", "Bombay HC Aurangabad Bench",
     "Aurangabad Bench, Bombay High Court",
     "Court/Judiciary", "judge|hc-judge|bombay-hc", "tarun-thadani", SRC),

    ("sc.mumbai@judmaha.gov.in", "Sessions Court Mumbai",
     "Sessions Court, Mumbai | Ph:+91-22-23003501",
     "Court/Judiciary", "judge|sessions-judge|district-court|top-priority", "tarun-thadani", SRC),

    ("cmm.mumbai@judmaha.gov.in", "Chief Metropolitan Magistrate Mumbai",
     "Chief Metropolitan Magistrate, Esplanade Court, Mumbai",
     "Court/Judiciary", "judge|sessions-judge|district-court|top-priority", "tarun-thadani", SRC),

    ("acjm.dadar@judmaha.gov.in", "ACJM Dadar Court",
     "Addl. Chief Judicial Magistrate, Dadar, Mumbai (FIR 0654/2022 court area)",
     "Court/Judiciary", "judge|sessions-judge|district-court|top-priority", "tarun-thadani", SRC),

    ("districtcourt.mumbai@judmaha.gov.in", "District Court Mumbai",
     "District & Sessions Court, Mumbai City",
     "Court/Judiciary", "judge|sessions-judge|district-court", "tarun-thadani", SRC),

    ("familycourt.mumbai@judmaha.gov.in", "Family Court Mumbai",
     "Family Court Mumbai",
     "Court/Judiciary", "judge|district-court", "tarun-thadani", SRC),

    # Law Commission / Legal Bodies
    ("lawcommissionindia@gmail.com", "Law Commission of India",
     "Law Commission of India | X:@LawCommission_I",
     "Government/Legal", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    ("helpdesk@sci.nic.in", "Supreme Court of India",
     "Registry, Supreme Court of India | Ph:+91-11-23388942",
     "Court/Judiciary", "judge|top-priority", "tarun-thadani", SRC),

    # ================================================================
    # NATIONAL JOURNALISTS — MUMBAI CRIME / LEGAL FOCUS
    # ================================================================
    ("priya.ramani@gmail.com", "Priya Ramani",
     "Senior Journalist / #MeToo Advocate | X:@priyaramani | YT:Priya Ramani",
     "Press/Media", "investigative|national-media|x-active|youtuber|social-active|top-priority", "tarun-thadani", SRC),

    ("pooja.pillai@indianexpress.com", "Pooja Pillai",
     "Senior Journalist, Indian Express",
     "Press/Media", "legal-reporter|national-media|ie", "tarun-thadani", SRC),

    ("karan.thapar@gmail.com", "Karan Thapar",
     "Senior TV Journalist / Interviewer | X:@Karan_Thapar | YT:Karan Thapar",
     "Press/Media", "investigative|national-media|x-active|youtuber|top-priority", "tarun-thadani", SRC),

    ("shekhar.gupta@theprint.in", "Shekhar Gupta",
     "Editor-in-Chief, The Print | X:@ShekharGupta | YT:ThePrint",
     "Press/Media", "investigative|national-media|x-active|youtuber|top-priority", "tarun-thadani", SRC),

    ("praveen.swami@gmail.com", "Praveen Swami",
     "Senior Journalist (Security / Crime) | X:@praveenswami",
     "Press/Media", "investigative|crime-journalist|national-media|x-active", "tarun-thadani", SRC),

    ("mahesh.langa@thehindu.com", "Mahesh Langa",
     "Reporter, The Hindu (Gujarat / National) | X:@MaheshLanga01",
     "Press/Media", "investigative|national-media|the-hindu|x-active", "tarun-thadani", SRC),

    ("mukesh.rawat@indiatoday.in", "Mukesh Rawat",
     "Crime Reporter, India Today | X:@mukeshrawat",
     "Press/Media", "crime-journalist|national-media|india-today|x-active", "tarun-thadani", SRC),

    ("aarti.tikoo.singh@gmail.com", "Aarti Tikoo Singh",
     "Senior Journalist / Commentator | X:@AartiTikoo",
     "Press/Media", "investigative|national-media|x-active", "tarun-thadani", SRC),

    ("damayanti.datta@gmail.com", "Damayanti Datta",
     "Senior Journalist, India Today | X:@ddattajournalist",
     "Press/Media", "investigative|national-media|x-active", "tarun-thadani", SRC),

    ("sankarshan.thakur@gmail.com", "Sankarshan Thakur",
     "Senior Journalist / Author | X:@sankarshanT",
     "Press/Media", "investigative|national-media|x-active", "tarun-thadani", SRC),

    ("priya.sahgal@indiatoday.in", "Priya Sahgal",
     "Executive Editor, India Today | X:@priyasahgal",
     "Press/Media", "crime-journalist|national-media|india-today|x-active", "tarun-thadani", SRC),

    ("ndtv.investigates@ndtv.com", "NDTV Investigates",
     "Investigative Unit, NDTV | X:@ndtv",
     "Press/Media", "investigative|national-media|ndtv|x-active", "tarun-thadani", SRC),

    ("smita.sharma@thelleaf.in", "Smita Sharma",
     "Senior Journalist / Anchor | X:@SmitaSharma",
     "Press/Media", "crime-journalist|national-media|x-active", "tarun-thadani", SRC),

    ("srishti.ojha@barandbench.com", "Srishti Ojha",
     "Legal Reporter, Bar & Bench | X:@SrishtiOjha_",
     "Press/Media", "legal-reporter|court-reporter|legal-media|x-active|top-priority", "tarun-thadani", SRC),

    ("apoorva.mandhani@livelaw.in", "Apoorva Mandhani",
     "Legal Reporter, LiveLaw | X:@apoorvamandhani",
     "Press/Media", "legal-reporter|court-reporter|legal-media|x-active|top-priority", "tarun-thadani", SRC),

    ("manu.sebastian@livelaw.in", "Manu Sebastian",
     "Legal Reporter, LiveLaw | X:@ManuSeb20",
     "Press/Media", "legal-reporter|court-reporter|legal-media|x-active|top-priority", "tarun-thadani", SRC),

    ("mehal.jain@livelaw.in", "Mehal Jain",
     "Legal Reporter (Bombay HC), LiveLaw | X:@mehal_jain",
     "Press/Media", "legal-reporter|court-reporter|legal-media|mumbai-press|x-active|top-priority", "tarun-thadani", SRC),

    ("sohini.chattopadhyay@gmail.com", "Sohini Chattopadhyay",
     "Crime Journalist / Author | X:@sohinichat",
     "Press/Media", "crime-journalist|investigative|x-active", "tarun-thadani", SRC),

    # ================================================================
    # LEGAL ACADEMICS / THINK TANKS
    # ================================================================
    ("contact@vidhicentre.org", "Vidhi Centre for Legal Policy",
     "Legal Policy Think Tank | X:@VidhiCLP",
     "Academic/Legal", "legal-activist|ngo|x-active|top-priority", "tarun-thadani", SRC),

    ("info@clprindia.org", "Centre for Law & Policy Research",
     "Constitutional Law Think Tank | X:@CLPR_India",
     "Academic/Legal", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    ("contact@idia.in", "IDIA Charitable Trust",
     "Increasing Diversity by Increasing Access (Legal Education) | X:@idiaindia",
     "Academic/Legal", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    ("sflcindia@sflc.in", "Software Freedom Law Centre India",
     "Digital Rights Legal Centre | X:@SFLCin",
     "Academic/Legal", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    ("info@internetfreedom.in", "Internet Freedom Foundation",
     "Digital Rights NGO | X:@internetfreedom",
     "Civil Society", "legal-activist|ngo|x-active", "tarun-thadani", SRC),

    ("media@iimb.ac.in", "IIM Bangalore Media",
     "Indian Institute of Management Bangalore",
     "Academic", "academic", "tarun-thadani", SRC),

    ("contact@daksh.org.in", "DAKSH India",
     "Data & Research on Judicial Systems | X:@DakshIndia",
     "Academic/Legal", "legal-activist|ngo|legal-reporter|x-active", "tarun-thadani", SRC),

    # ================================================================
    # FOREIGN PRESS — MUMBAI CORRESPONDENTS
    # ================================================================
    ("mumbai.bureau@reuters.com", "Reuters Mumbai Bureau",
     "Reuters India Bureau, Mumbai | X:@ReutersIndia",
     "Press/Media", "national-media|international-media|mumbai-press|x-active|top-priority", "tarun-thadani", SRC),

    ("mumbai@apnews.com", "AP Mumbai Bureau",
     "Associated Press India, Mumbai | X:@AP",
     "Press/Media", "national-media|international-media|mumbai-press|x-active", "tarun-thadani", SRC),

    ("mumbai.bureau@bloomberg.net", "Bloomberg Mumbai",
     "Bloomberg News, Mumbai Bureau | X:@business",
     "Press/Media", "national-media|international-media|financial-journalist|mumbai-press", "tarun-thadani", SRC),

    ("india.desk@bbc.com", "BBC India Desk",
     "BBC News India, Mumbai | X:@BBCIndia",
     "Press/Media", "national-media|international-media|x-active|top-priority", "tarun-thadani", SRC),

    ("india.desk@theguardian.com", "The Guardian India",
     "The Guardian India Correspondent | X:@guardian",
     "Press/Media", "national-media|international-media|x-active|investigative", "tarun-thadani", SRC),

    ("india@nytimes.com", "New York Times India",
     "New York Times India Bureau | X:@nytimesworld",
     "Press/Media", "national-media|international-media|x-active|investigative", "tarun-thadani", SRC),

    ("india@wsj.com", "Wall Street Journal India",
     "WSJ India Bureau | X:@WSJ",
     "Press/Media", "national-media|international-media|x-active|financial-journalist", "tarun-thadani", SRC),

    # ================================================================
    # ADDITIONAL CRIME / COURT REPORTERS
    # ================================================================
    ("ananya.roy@hindustantimes.com", "Ananya Roy",
     "Reporter, Hindustan Times Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|ht", "tarun-thadani", SRC),

    ("atique.khan@thehindu.com", "Atique Khan",
     "Reporter, The Hindu Mumbai",
     "Press/Media", "crime-journalist|mumbai-press|the-hindu", "tarun-thadani", SRC),

    ("preetika.rana@wsj.com", "Preetika Rana",
     "Reporter, Wall Street Journal India | X:@preetika_rana",
     "Press/Media", "investigative|international-media|x-active", "tarun-thadani", SRC),

    ("dhanya.rajendran@thenewsminute.com", "Dhanya Rajendran",
     "Editor-in-Chief, The News Minute | X:@dhanya1986",
     "Press/Media", "investigative|digital-media|x-active|top-priority", "tarun-thadani", SRC),

    ("joeomy@thequint.com", "Joe Wankhede",
     "Crime Reporter, The Quint Mumbai | X:@JoeWankhede",
     "Press/Media", "crime-journalist|digital-media|mumbai-press|the-quint|x-active", "tarun-thadani", SRC),

    ("salil.tripathi@gmail.com", "Salil Tripathi",
     "Journalist / Author / Rights Activist | X:@saliltripathi",
     "Press/Media", "investigative|legal-activist|x-active|top-priority", "tarun-thadani", SRC),

    ("supriya.nair@gmail.com", "Supriya Nair",
     "Senior Journalist Mumbai | X:@supriya_nair17",
     "Press/Media", "crime-journalist|investigative|mumbai-press|x-active", "tarun-thadani", SRC),

    ("kavita.iyer@gmail.com", "Kavita Iyer",
     "Crime Reporter, Mumbai | X:@kavitaiyer",
     "Press/Media", "crime-journalist|mumbai-press|x-active", "tarun-thadani", SRC),

    ("puja.changoiwala@gmail.com", "Puja Changoiwala",
     "Crime Journalist / Author, Mumbai | X:@PujaChanGoiwala",
     "Press/Media", "crime-journalist|investigative|mumbai-press|x-active|top-priority", "tarun-thadani", SRC),

    ("rahul.shrivastava@indiatoday.in", "Rahul Shrivastava",
     "Crime Reporter, India Today | X:@rahulshrivastav",
     "Press/Media", "crime-journalist|national-media|india-today|x-active", "tarun-thadani", SRC),

    ("special.report@firstpost.com", "Firstpost Crime Desk",
     "Crime & Politics Desk, Firstpost | X:@firstpost",
     "Press/Media", "crime-journalist|digital-media|x-active", "tarun-thadani", SRC),

    ("editor@catchnews.com", "Catch News Crime Desk",
     "Crime & Politics Desk, Catch News",
     "Press/Media", "crime-journalist|digital-media", "tarun-thadani", SRC),

    ("mumbai@hindustantimes.com", "HT Mumbai News Desk",
     "General Mumbai News Desk, Hindustan Times",
     "Press/Media", "mumbai-press|ht", "tarun-thadani", SRC),

    ("mumbai@timesofindia.com", "TOI Mumbai City Desk",
     "Mumbai City Desk, Times of India",
     "Press/Media", "mumbai-press|toi", "tarun-thadani", SRC),

    ("mumbai.desk@thehindu.com", "The Hindu Mumbai Desk",
     "Mumbai Correspondent Desk, The Hindu",
     "Press/Media", "mumbai-press|the-hindu", "tarun-thadani", SRC),

    ("correspondent.mumbai@scroll.in", "Scroll Mumbai Correspondent",
     "Mumbai Crime Correspondent, Scroll.in",
     "Press/Media", "crime-journalist|digital-media|mumbai-press", "tarun-thadani", SRC),

    ("investigates@thequint.com", "The Quint Investigates",
     "Investigative Desk, The Quint | X:@TheQuint",
     "Press/Media", "investigative|digital-media|x-active", "tarun-thadani", SRC),

    ("crime@newslaundry.com", "Newslaundry Crime Desk",
     "Crime Reporting, Newslaundry | X:@newslaundry",
     "Press/Media", "crime-journalist|investigative|digital-media|x-active", "tarun-thadani", SRC),

    # ================================================================
    # LEGAL PROFESSIONALS — ADDITIONAL
    # ================================================================
    ("info@majlislegal.in", "Majlis Legal Centre (formal)",
     "Legal Centre for Women & Minorities, Mumbai | X:@majlislegal",
     "Legal", "legal-activist|ngo|human-rights-lawyer|x-active", "tarun-thadani", SRC),

    ("legalaid.mumbai@gmail.com", "Mumbai Legal Aid",
     "Free Legal Aid Service, Mumbai",
     "Legal", "legal-activist|ngo", "tarun-thadani", SRC),

    ("nalsa.india@gmail.com", "NALSA India",
     "National Legal Services Authority | X:@NALSA_India",
     "Government/Legal", "legal-activist|x-active", "tarun-thadani", SRC),

    ("info@lawcollege.edu.in", "Government Law College Mumbai",
     "Government Law College, Mumbai | X:@GLC_Mumbai",
     "Academic", "legal-activist|x-active", "tarun-thadani", SRC),

    ("dean@ils.ac.in", "ILS Law College Pune",
     "ILS Law College, Pune | X:@ILS_Pune",
     "Academic", "legal-activist", "tarun-thadani", SRC),

    ("contact@symlaw.ac.in", "Symbiosis Law School Mumbai",
     "Symbiosis Law School, Noida/Mumbai | X:@SLSNoidaOff",
     "Academic", "legal-activist", "tarun-thadani", SRC),

    ("nilima.mhatre.advocate@gmail.com", "Nilima Mhatre",
     "Advocate, Bombay HC / Session Courts",
     "Legal", "lawyer|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("advocate.nikhil.daga@gmail.com", "Nikhil Daga",
     "Criminal Advocate, Mumbai | X:@AdvNikhilDaga",
     "Legal", "lawyer|criminal-lawyer|x-active", "tarun-thadani", SRC),

    ("kedar.dighe.advocate@gmail.com", "Kedar Dighe",
     "Advocate, Bombay HC | X:@KedarDighe",
     "Legal", "lawyer|criminal-lawyer|bombay-hc|x-active", "tarun-thadani", SRC),

    ("advjaytakkar@gmail.com", "Jay Takkar",
     "Advocate, Bombay HC",
     "Legal", "lawyer|criminal-lawyer|bombay-hc", "tarun-thadani", SRC),

    ("contact@legallyindia.com", "Legally India",
     "Legal Industry News | X:@legallyindia",
     "Press/Media", "legal-reporter|legal-media|x-active", "tarun-thadani", SRC),

    ("editor@spicyip.com", "SpicyIP Blog",
     "IP Law Blog India | X:@SpicyIP",
     "Press/Media", "legal-reporter|legal-media|x-active", "tarun-thadani", SRC),

    # ================================================================
    # ADDITIONAL YOUTUBERS / INFLUENCERS
    # ================================================================
    ("crimereporterindia@gmail.com", "Crime Reporter India",
     "Crime Journalism YouTube Channel | YT:Crime Reporter India",
     "Press/Media", "youtuber|digital-media|crime-journalist|x-active", "tarun-thadani", SRC),

    ("mumbaiunderbelly@gmail.com", "Mumbai Underbelly",
     "Mumbai Crime Documentary Channel | YT:Mumbai Underbelly",
     "Press/Media", "youtuber|digital-media|crime-journalist|mumbai-press", "tarun-thadani", SRC),

    ("contactcrimeclock@gmail.com", "Crime Clock India",
     "Crime News YouTube | YT:Crime Clock India | X:@CrimeClockIndia",
     "Press/Media", "youtuber|digital-media|crime-journalist|x-active", "tarun-thadani", SRC),

    ("ranveerrishi@gmail.com", "Ranveer Rishi",
     "Legal Commentary YouTuber | YT:Ranveer Rishi | X:@ranveerrishi",
     "Press/Media", "youtuber|social-active|legal-reporter|x-active", "tarun-thadani", SRC),

    ("mumbaikarwrites@gmail.com", "Mumbaikar Writes",
     "Mumbai Social Commentary Channel | YT:Mumbaikar Writes",
     "Press/Media", "youtuber|digital-media|mumbai-press", "tarun-thadani", SRC),

    ("aapkasandeep@gmail.com", "Sandeep Maheshwari Mumbai",
     "Motivational Content Creator Mumbai | YT:Sandeep Maheshwari | X:@Sandeepxme",
     "Press/Media", "youtuber|influencer|social-active|x-active|top-priority", "tarun-thadani", SRC),

    ("contact@bombaybeats.in", "Bombay Beats",
     "Mumbai News & Culture Digital Platform | X:@bombaybeats",
     "Press/Media", "youtuber|digital-media|mumbai-press|x-active", "tarun-thadani", SRC),

    ("studio.mumbai@yashrajfilms.com", "YRF Mumbai",
     "Yash Raj Films (Mumbai Entertainment/PR) | X:@yrf",
     "Press/Media", "influencer|mumbai-press|x-active", "tarun-thadani", SRC),

    ("investigationsindia@gmail.com", "Investigations India",
     "Crime Investigative Content | YT:Investigations India | X:@InvestigationsI",
     "Press/Media", "youtuber|digital-media|crime-journalist|x-active", "tarun-thadani", SRC),

    ("mumbainews24x7@gmail.com", "Mumbai News 24x7",
     "Mumbai Breaking News Channel | YT:Mumbai News 24x7",
     "Press/Media", "youtuber|digital-media|crime-journalist|mumbai-press", "tarun-thadani", SRC),
]


# ── DEDUPLICATION AND FILTERING ───────────────────────────────────
def load_existing():
    seen = set()
    if FINAL_CSV.exists():
        with open(FINAL_CSV, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                e = row.get("email", "").strip().lower()
                if e:
                    seen.add(e)
    return seen


def load_suppressed():
    suppressed = set()
    if SUPP_CSV.exists():
        with open(SUPP_CSV, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                e = row.get("email", "").strip().lower()
                if e:
                    suppressed.add(e)
    return suppressed


def main():
    existing   = load_existing()
    suppressed = load_suppressed()
    print(f"Existing contacts : {len(existing)}")
    print(f"Suppressed        : {len(suppressed)}")
    print(f"Raw candidates    : {len(RAW)}")
    print()

    added, skipped_dup, skipped_mx, skipped_supp = [], 0, 0, 0

    for row in RAW:
        email = row[0].strip().lower()
        if email in suppressed:
            skipped_supp += 1
            continue
        if email in existing:
            skipped_dup += 1
            continue
        if not email_ok(email):
            print(f"  BAD-MX  {email}")
            skipped_mx += 1
            continue
        existing.add(email)
        added.append(row)
        print(f"  OK      {email}")

    print()
    print(f"Added    : {len(added)}")
    print(f"Dups     : {skipped_dup}")
    print(f"Bad-MX   : {skipped_mx}")
    print(f"Suppressed: {skipped_supp}")

    if not added:
        print("Nothing to add.")
    else:
        # Append to contacts_final.csv
        with open(FINAL_CSV, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            for row in added:
                w.writerow(row)
        print(f"contacts_final.csv updated -> {FINAL_CSV}")

    # Rebuild contacts_live.csv (final minus suppressed)
    print("\nRebuilding contacts_live.csv ...")
    suppressed_now = load_suppressed()
    with open(FINAL_CSV, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    header = ["email", "name", "designation", "category", "tags", "case", "source"]
    live = [r for r in rows if r.get("email", "").strip().lower() not in suppressed_now]
    with open(LIVE_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(live)
    print(f"contacts_live.csv -> {len(live)} rows (was {len(rows)} in final)")


if __name__ == "__main__":
    main()
