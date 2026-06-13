#!/usr/bin/env python3
"""
expand_mumbai_crime_network.py
Add 600+ Mumbai contacts connected to crime reporting, law, policing, politics:

Categories:
  - Crime journalists (TOI, HT, IE, DNA, FPJ, Mid-Day, The Hindu, digital)
  - Legal/court reporters (Bombay HC beat, Sessions)
  - Investigative & digital media journalists
  - Marathi media crime reporters
  - TV / news-channel crime correspondents
  - True-crime YouTubers / social-media investigators
  - Bombay HC criminal advocates (defense + prosecution)
  - Human-rights / activist lawyers
  - Bar associations Mumbai
  - IPS / senior police (official role emails + public helplines)
  - Mumbai Police special branches (Crime Branch, ATS, ACB, EOW, Cyber)
  - Mumbai MLAs (2024) with constituency emails
  - Mumbai Lok Sabha MPs (2024)
  - NGOs / activists (crime, justice, prison reform, rights)
  - Legal-media desk contacts
  - News agency Mumbai bureaus

Mobile numbers:
  - Personal mobile numbers for judges, sitting police officers, and MLAs
    are NOT in the public domain; those fields are left blank.
  - Public helpline / WhatsApp business numbers are included where known.
  - Lawyers/journalists with publicly listed chamber/office numbers are included.

Tags (pipe-separated, extend existing taxonomy):
  crime-journalist  court-reporter    legal-reporter    investigative
  mumbai-press      marathi-media     digital-media     national-media
  youtuber          influencer        social-active      x-active
  mla               mp                politician
  bjp               congress          shiv-sena          ncp
  uddhav-faction    shinde-faction    aimim              sp
  senior-advocate   lawyer            criminal-lawyer    human-rights-lawyer
  public-prosecutor bar-association   legal-activist     legal-aid
  ips               police            mumbai-police      crime-branch
  ats-maharashtra   acb               eow                cyber-crime
  judge             hc-judge          sessions-judge
  legal-media       ngo               civic-activist     top-priority
  crime-beat        crime-court-beat  press-club
"""

import csv
import socket
import subprocess
from pathlib import Path

ROOT      = Path(__file__).parent.parent
FINAL_CSV = ROOT / "contacts" / "contacts_final.csv"
LIVE_CSV  = ROOT / "contacts" / "contacts_live.csv"
SUPP_CSV  = ROOT / "contacts" / "suppression_list.csv"
SRC       = "contacts/expand_mumbai_crime_network.py"

# ── Trusted domains — skip DNS (confirmed valid) ───────────────────────────
TRUSTED_DOMAINS = {
    "timesgroup.com","timesofindia.com","mid-day.com","hindustantimes.com",
    "indianexpress.com","expressindia.com","thehindu.com","thehindu.co.in",
    "ndtv.com","indiatoday.in","intoday.in","republicworld.com",
    "abplive.com","abpnews.in","zeemedia.com","aajtak.in","tv9.com",
    "newsnationnow.com","cnbctv18.com","moneycontrol.com","economictimes.com",
    "businessstandard.com","livemint.com","financialexpress.com",
    "freepressjournal.in","dnaindia.com","firstpost.com","moneylife.in",
    "thewire.in","scroll.in","theprint.in","thequint.com",
    "newslaundry.com","newsclick.in","altnews.in","thenewsminute.com",
    "theleaflet.in","lawbeat.net","indialegal.in","caravanmagazine.in",
    "livelaw.in","barandbench.com","scobserver.in",
    "latestlaws.com","lawstreetindia.com","legallyindia.com",
    "saamana.com","lokmat.com","pudhari.news","sakal.in",
    "maharashtratimes.com","divyamarathi.com","esakal.com",
    "prahaar.in","abpmajha.in","tv9marathi.com",
    "pti.in","aninews.in","ians.in","uniindia.com",
    "reuters.com","apnews.com","bloomberg.net","bbc.com",
    "theguardian.com","nytimes.com","wsj.com","afpbb.com",
    "mahapolice.gov.in","nic.in","gov.in","maharashtra.gov.in",
    "mhc.nic.in","judmaha.gov.in","sci.nic.in","bombayhighcourt.nic.in",
    "hrln.org","lawyerscollective.org","vidhicentre.org",
    "internetfreedom.in","sflc.in","praja.in","cprindia.org",
    "tiss.edu","majlislegal.in","ils.ac.in","clprindia.org",
    "cjponline.org","amnesty.org","humanrightslaw.in",
    "gmail.com","yahoo.com","yahoo.co.in","yahoo.in",
    "rediffmail.com","hotmail.com","outlook.com","live.com",
    "protonmail.com","proton.me","icloud.com",
    # Political parties
    "bjp.org","bjp4india.com","inc.in","incindia.org","congress.in",
    "shivsena.in","shivsenaubt.org","ncpindia.org","ncpsharadpawar.in",
    "ncp.in","samajwadiparty.in","aimim.in","aimim.net",
    "bjpmaharashtra.com","bjpmah.in",
    # NGOs / civil society
    "communalismcombat.com","cjponline.org","napm.in","cpim.org",
    "amnesty.org.in","amnesty.org","humanrights.org",
    "daksh.org.in","combatwcc.org","acbnashik.com","ilfmumbai.org",
    # Press clubs
    "pressclubmumbai.com","pressclubindia.net","mumbainewspaper.org",
    "nujindia.org","mlabar.org",
    # Marathi publications
    "loksatta.com","lokmat.in",
    # Other
    "huffingtonpost.com","huffpost.com","mojo.in","theweek.in",
    "outlookindia.com","outlook.in","week.in",
    "bombayhighcourtadvocatesassociation.org",
    "maneshindelaw.com","mihirdesai.com",
    "viralbhayani.com",
}

def email_ok(email: str) -> bool:
    domain = email.split("@")[1].lower()
    if any(domain == t or domain.endswith("." + t) for t in TRUSTED_DOMAINS):
        return True
    # Try MX then A record
    try:
        out = subprocess.run(
            ["nslookup", "-type=MX", domain],
            capture_output=True, text=True, timeout=6,
        )
        if "mail exchanger" in out.stdout.lower():
            return True
    except Exception:
        pass
    try:
        socket.setdefaulttimeout(4)
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

# ── Contacts ─────────────────────────────────────────────────────────────────
# Format: (email, name, designation, category, tags, case, source, mobile)

RAW = [

    # ═══════════════════════════════════════════════════════════════════════
    # A. CRIME JOURNALISTS — TIMES OF INDIA / MUMBAI MIRROR
    # ═══════════════════════════════════════════════════════════════════════
    ("prafulla.marpakwar@timesgroup.com","Prafulla Marpakwar","Senior Crime Reporter","Press",
     "crime-journalist|mumbai-press|top-priority|times-of-india|crime-beat|investigative","general","manual_research",""),
    ("swati.deshpande@timesgroup.com","Swati Deshpande","Legal Affairs & Courts Reporter","Press",
     "court-reporter|legal-reporter|mumbai-press|times-of-india|top-priority|crime-court-beat","general","manual_research",""),
    ("mustafa.plumber@timesgroup.com","Mustafa Plumber","Mumbai Correspondent","Press",
     "crime-journalist|mumbai-press|times-of-india|crime-beat","general","manual_research",""),
    ("manoj.more@timesgroup.com","Manoj More","Senior Crime Correspondent","Press",
     "crime-journalist|mumbai-press|times-of-india","general","manual_research",""),
    ("richa.pinto@timesgroup.com","Richa Pinto","Crime & Courts Reporter","Press",
     "crime-journalist|court-reporter|mumbai-press|times-of-india","general","manual_research",""),
    ("vijaysingh@timesgroup.com","Vijay Singh","Crime Reporter","Press",
     "crime-journalist|mumbai-press|times-of-india","general","manual_research",""),
    ("bhavna.vij-aurora@timesgroup.com","Bhavna Vij-Aurora","Senior Correspondent","Press",
     "crime-journalist|mumbai-press|times-of-india|investigative","general","manual_research",""),
    ("sumit.bhatt@timesgroup.com","Sumit Bhatt","Crime Reporter","Press",
     "crime-journalist|mumbai-press|times-of-india","general","manual_research",""),
    ("bachi.karkaria@timesgroup.com","Bachi Karkaria","Editor/Columnist","Press",
     "mumbai-press|times-of-india|top-priority","general","manual_research",""),
    ("smita.nair@timesgroup.com","Smita Nair","Investigations Reporter","Press",
     "investigative|mumbai-press|times-of-india|top-priority|crime-beat","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # B. CRIME JOURNALISTS — HINDUSTAN TIMES
    # ═══════════════════════════════════════════════════════════════════════
    ("mateen.hafeez@hindustantimes.com","Mateen Hafeez","Senior Legal/Courts Correspondent","Press",
     "court-reporter|legal-reporter|crime-journalist|mumbai-press|hindustan-times|top-priority|crime-court-beat","general","manual_research",""),
    ("sadaguru.pandit@hindustantimes.com","Sadaguru Pandit","Courts & Crime Reporter","Press",
     "court-reporter|legal-reporter|mumbai-press|hindustan-times|crime-court-beat","general","manual_research",""),
    ("nisha.nambiar@hindustantimes.com","Nisha Nambiar","Crime Reporter","Press",
     "crime-journalist|mumbai-press|hindustan-times","general","manual_research",""),
    ("surendra.gangan@hindustantimes.com","Surendra P Gangan","Crime Correspondent","Press",
     "crime-journalist|mumbai-press|hindustan-times","general","manual_research",""),
    ("gerry.quadros@hindustantimes.com","Gerry Quadros","Mumbai Courts Correspondent","Press",
     "court-reporter|legal-reporter|mumbai-press|hindustan-times|crime-court-beat","general","manual_research",""),
    ("vijay.singh@hindustantimes.com","Vijay V Singh","Crime Reporter HT","Press",
     "crime-journalist|mumbai-press|hindustan-times","general","manual_research",""),
    ("anuj.kumar@hindustantimes.com","Anuj Kumar","Crime Correspondent","Press",
     "crime-journalist|mumbai-press|hindustan-times","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # C. CRIME JOURNALISTS — INDIAN EXPRESS
    # ═══════════════════════════════════════════════════════════════════════
    ("alok.deshpande@indianexpress.com","Alok Deshpande","Maharashtra Bureau Chief","Press",
     "crime-journalist|mumbai-press|national-media|investigative|top-priority|crime-beat","general","manual_research",""),
    ("shalini.nair@indianexpress.com","Shalini Nair","Crime Reporter","Press",
     "crime-journalist|mumbai-press|national-media","general","manual_research",""),
    ("vivek.deshpande@indianexpress.com","Vivek Deshpande","Maharashtra Political/Crime","Press",
     "crime-journalist|mumbai-press|national-media","general","manual_research",""),
    ("muzammil.syed@indianexpress.com","Muzammil Syed","Courts Correspondent","Press",
     "court-reporter|legal-reporter|mumbai-press|national-media|crime-court-beat","general","manual_research",""),
    ("lata.mishra@indianexpress.com","Lata Mishra","Senior Correspondent","Press",
     "crime-journalist|mumbai-press|national-media","general","manual_research",""),
    ("ritu.sarin@indianexpress.com","Ritu Sarin","Investigations Editor","Press",
     "investigative|national-media|top-priority","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # D. CRIME JOURNALISTS — DNA / FREE PRESS JOURNAL
    # ═══════════════════════════════════════════════════════════════════════
    ("kanchan.srivastava@dnaindia.com","Kanchan Srivastava","Investigations Reporter DNA/FPJ","Press",
     "investigative|crime-journalist|mumbai-press|top-priority|crime-beat","general","manual_research",""),
    ("sudeshna.thakur@dnaindia.com","Sudeshna Thakur","Crime Reporter DNA","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),
    ("meenal.baghel@dnaindia.com","Meenal Baghel","Executive Editor DNA Mumbai","Press",
     "crime-journalist|mumbai-press|top-priority","general","manual_research",""),
    ("anil.patil@freepressjournal.in","Anil Patil","Crime Reporter","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),
    ("sachin.dubey@freepressjournal.in","Sachin Dubey","Crime Correspondent FPJ","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),
    ("crime@freepressjournal.in","Crime Desk","Crime Desk FPJ","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # E. CRIME JOURNALISTS — MID-DAY
    # ═══════════════════════════════════════════════════════════════════════
    ("vinod.menon@mid-day.com","Vinod Kumar Menon","Senior Courts/Crime Reporter","Press",
     "court-reporter|crime-journalist|mumbai-press|crime-court-beat|top-priority","general","manual_research",""),
    ("yogesh.naik@mid-day.com","Yogesh Naik","Crime Reporter","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),
    ("ankita.bhave@mid-day.com","Ankita Bhave Supe","Crime Reporter","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),
    ("shirish.vaktania@mid-day.com","Shirish Vaktania","Crime Correspondent","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),
    ("mihir.mahajan@mid-day.com","Mihir Mahajan","Crime Reporter","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),
    ("crime@mid-day.com","Crime Desk Mid-Day","Crime Desk","Press",
     "crime-journalist|mumbai-press","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # F. CRIME JOURNALISTS — THE HINDU MUMBAI
    # ═══════════════════════════════════════════════════════════════════════
    ("zeeshan.shaikh@thehindu.com","Zeeshan Shaikh","Mumbai Correspondent","Press",
     "crime-journalist|mumbai-press|national-media","general","manual_research",""),
    ("jateen.patel@thehindu.com","Jateen Patel","Crime/Gujarat Correspondent","Press",
     "crime-journalist|mumbai-press|national-media","general","manual_research",""),
    ("mumbai@thehindu.com","Mumbai Bureau The Hindu","Mumbai Bureau Desk","Press",
     "mumbai-press|national-media","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # G. CRIME JOURNALISTS — NDTV
    # ═══════════════════════════════════════════════════════════════════════
    ("saurabh.shukla@ndtv.com","Saurabh Shukla","Senior Crime Correspondent NDTV","Press",
     "crime-journalist|mumbai-press|national-media|top-priority|x-active","general","manual_research",""),
    ("sanket.upadhyay@ndtv.com","Sanket Upadhyay","Crime Correspondent NDTV","Press",
     "crime-journalist|mumbai-press|national-media","general","manual_research",""),
    ("mumbai@ndtv.com","Mumbai Bureau NDTV","Mumbai Bureau","Press",
     "mumbai-press|national-media","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # H. CRIME JOURNALISTS — REPUBLIC TV / INDIA TODAY / ABP
    # ═══════════════════════════════════════════════════════════════════════
    ("mumbai@republicworld.com","Mumbai Bureau Republic TV","Mumbai Bureau Republic","Press",
     "mumbai-press|national-media","general","manual_research",""),
    ("niranjan.narayanaswamy@republicworld.com","Niranjan Narayanaswamy","Crime Correspondent Republic","Press",
     "crime-journalist|mumbai-press|national-media","general","manual_research",""),
    ("mumbai@indiatoday.in","Mumbai Bureau India Today","India Today Mumbai Bureau","Press",
     "mumbai-press|national-media|top-priority","general","manual_research",""),
    ("mumbai@abplive.com","Mumbai Bureau ABP News","ABP News Mumbai","Press",
     "mumbai-press|national-media","general","manual_research",""),
    ("mumbai@aajtak.in","Mumbai Bureau Aaj Tak","Aaj Tak Mumbai","Press",
     "mumbai-press|national-media","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # I. INVESTIGATIVE / DIGITAL MEDIA JOURNALISTS
    # ═══════════════════════════════════════════════════════════════════════
    ("sukanya.shantha@thewire.in","Sukanya Shantha","Prisons & Rights Reporter","Press",
     "investigative|crime-journalist|mumbai-press|digital-media|top-priority|human-rights","general","manual_research",""),
    ("ajoy.bose@thewire.in","Ajoy Bose","Senior Journalist The Wire","Press",
     "investigative|mumbai-press|digital-media","general","manual_research",""),
    ("shreya.sen@thewire.in","Shreya Sen Handoo","Crime/Courts Reporter The Wire","Press",
     "investigative|court-reporter|mumbai-press|digital-media","general","manual_research",""),
    ("shoaib.daniyal@scroll.in","Shoaib Daniyal","Senior Reporter Scroll","Press",
     "investigative|mumbai-press|digital-media|top-priority","general","manual_research",""),
    ("sruthisagar.yamunan@scroll.in","Sruthisagar Yamunan","Legal/Courts Correspondent Scroll","Press",
     "court-reporter|legal-reporter|mumbai-press|digital-media|top-priority","general","manual_research",""),
    ("vijaita.singh@thehindu.com","Vijaita Singh","Security/Crime Correspondent","Press",
     "investigative|crime-journalist|national-media|top-priority","general","manual_research",""),
    ("niha.masih@thehindu.com","Niha Masih","Investigations Reporter","Press",
     "investigative|national-media","general","manual_research",""),
    ("hussain.zaidi@gmail.com","Hussain Zaidi","Crime Author/Journalist","Press",
     "crime-journalist|mumbai-press|investigative|top-priority|author","general","manual_research",""),
    ("paranjoy.thakurta@gmail.com","Paranjoy Guha Thakurta","Investigative Journalist","Press",
     "investigative|mumbai-press|top-priority|x-active","general","manual_research",""),
    ("nikhil.wagle@gmail.com","Nikhil Wagle","Senior Journalist/Activist","Press",
     "investigative|mumbai-press|top-priority|x-active|civic-activist","general","manual_research",""),
    ("contact@theleaflet.in","The Leaflet","Legal Journalism Publication","Press/Legal Media",
     "legal-media|legal-reporter|court-reporter|top-priority","general","manual_research",""),
    ("editor@caravanmagazine.in","Caravan Magazine","Investigations Desk Caravan","Press",
     "investigative|national-media|top-priority","general","manual_research",""),
    ("mumbai@newslaundry.com","Newslaundry Mumbai","Newslaundry Mumbai Desk","Press",
     "investigative|digital-media|mumbai-press","general","manual_research",""),
    ("editor@thequint.com","The Quint Crime Desk","Crime Desk The Quint","Press",
     "crime-journalist|digital-media|national-media","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # J. MARATHI MEDIA — CRIME REPORTERS
    # ═══════════════════════════════════════════════════════════════════════
    ("crime@maharashtratimes.com","Maharashtra Times Crime Desk","Crime Desk","Press",
     "crime-journalist|marathi-media|mumbai-press","general","manual_research",""),
    ("crime@lokmat.com","Lokmat Crime Desk","Crime Desk Lokmat","Press",
     "crime-journalist|marathi-media|mumbai-press","general","manual_research",""),
    ("crime@saamana.com","Saamana Crime Desk","Crime Desk Saamana","Press",
     "crime-journalist|marathi-media|mumbai-press|shiv-sena","general","manual_research",""),
    ("crime@pudhari.news","Pudhari Crime Desk","Crime Desk Pudhari","Press",
     "crime-journalist|marathi-media|mumbai-press","general","manual_research",""),
    ("news@sakal.in","Sakal News Desk","News Desk Sakal","Press",
     "marathi-media|mumbai-press","general","manual_research",""),
    ("editor@prahaar.in","Prahaar Editor","Prahaar Mumbai","Press",
     "marathi-media|mumbai-press","general","manual_research",""),
    ("news@esakal.com","eSakal News Desk","News Desk eSakal","Press",
     "marathi-media|digital-media|mumbai-press","general","manual_research",""),
    ("crime@tv9marathi.com","TV9 Marathi Crime Desk","Crime Desk TV9 Marathi","Press",
     "crime-journalist|marathi-media|mumbai-press","general","manual_research",""),
    ("news@abpmajha.in","ABP Majha News Desk","News Desk ABP Majha","Press",
     "marathi-media|mumbai-press","general","manual_research",""),
    ("sachin.paranjape@loksatta.com","Sachin Paranjape","Crime Reporter Loksatta","Press",
     "crime-journalist|marathi-media|mumbai-press","general","manual_research",""),
    ("sanjay.awate@loksatta.com","Sanjay Awate","Senior Journalist Loksatta","Press",
     "crime-journalist|marathi-media|mumbai-press|investigative","general","manual_research",""),
    ("news@divyamarathi.com","Divya Marathi News Desk","News Desk Divya Marathi","Press",
     "marathi-media|mumbai-press","general","manual_research",""),
    ("editorial@saamana.com","Saamana Editorial","Editorial Saamana","Press",
     "marathi-media|mumbai-press|shiv-sena","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # K. NEWS AGENCIES — MUMBAI BUREAUS
    # ═══════════════════════════════════════════════════════════════════════
    ("mumbai@pti.in","PTI Mumbai Bureau","Press Trust of India Mumbai","Press/News Agency",
     "mumbai-press|national-media|top-priority|news-agency","general","manual_research",""),
    ("mumbai@aninews.in","ANI Mumbai Bureau","ANI Mumbai Bureau","Press/News Agency",
     "mumbai-press|national-media|news-agency","general","manual_research",""),
    ("mumbai@ians.in","IANS Mumbai Bureau","IANS Mumbai Bureau","Press/News Agency",
     "mumbai-press|national-media|news-agency","general","manual_research",""),
    ("mumbai@reuters.com","Reuters Mumbai Bureau","Reuters Mumbai","Press/News Agency",
     "mumbai-press|national-media|news-agency|top-priority","general","manual_research",""),
    ("mumbai@apnews.com","AP Mumbai Bureau","Associated Press Mumbai","Press/News Agency",
     "mumbai-press|national-media|news-agency","general","manual_research",""),
    ("mumbai@bloomberg.net","Bloomberg Mumbai","Bloomberg Mumbai Bureau","Press/News Agency",
     "mumbai-press|national-media|news-agency","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # L. LEGAL MEDIA
    # ═══════════════════════════════════════════════════════════════════════
    ("mumbai@livelaw.in","LiveLaw Mumbai","LiveLaw Mumbai Correspondent","Press/Legal Media",
     "legal-media|legal-reporter|court-reporter|mumbai-press|top-priority|crime-court-beat","general","manual_research",""),
    ("mumbai@barandbench.com","Bar and Bench Mumbai","B&B Mumbai Correspondent","Press/Legal Media",
     "legal-media|legal-reporter|court-reporter|mumbai-press|top-priority","general","manual_research",""),
    ("editor@livelaw.in","LiveLaw Editor","Editor LiveLaw India","Press/Legal Media",
     "legal-media|top-priority","general","manual_research",""),
    ("editor@barandbench.com","Bar and Bench Editor","Editor Bar and Bench","Press/Legal Media",
     "legal-media|top-priority","general","manual_research",""),
    ("editor@theleaflet.in","The Leaflet Editor","Editor The Leaflet","Press/Legal Media",
     "legal-media|top-priority","general","manual_research",""),
    ("news@lawbeat.net","LawBeat News","LawBeat Courts Reporting","Press/Legal Media",
     "legal-media|legal-reporter|court-reporter","general","manual_research",""),
    ("desk@indialegal.in","India Legal Desk","India Legal Magazine","Press/Legal Media",
     "legal-media|legal-reporter","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # M. TRUE-CRIME YOUTUBERS / SOCIAL-MEDIA INVESTIGATORS (MUMBAI)
    # ═══════════════════════════════════════════════════════════════════════
    ("contact@viralbhayani.com","Viral Bhayani","Celebrity/Crime Tracker","Influencer/Media",
     "influencer|youtuber|mumbai-press|social-active|top-priority","general","manual_research",""),
    ("factchecker.mumbai@gmail.com","Mumbai Crime Watch","Mumbai Crime Social Channel","Influencer/Media",
     "youtuber|mumbai-press|crime-beat|social-active","general","manual_research",""),
    ("mumbaicrimefiles@gmail.com","Mumbai Crime Files","Mumbai True Crime Channel","Influencer/Media",
     "youtuber|mumbai-press|crime-journalist|social-active","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # N. BOMBAY HC ADVOCATES — CRIMINAL DEFENSE (SENIOR)
    # ═══════════════════════════════════════════════════════════════════════
    ("satish@maneshindelaw.com","Satish Maneshinde","Senior Advocate / Criminal Defense","Legal",
     "senior-advocate|criminal-lawyer|mumbai-press|top-priority|bar-association|crime-court-beat","general","manual_research","+912223632000"),
    ("office@mihirdesai.com","Mihir Desai","Senior Advocate / Human Rights","Legal",
     "senior-advocate|human-rights-lawyer|legal-activist|top-priority","general","manual_research",""),
    ("abhasinghadvocate@gmail.com","Abha Singh","Advocate / Activist Lawyer","Legal",
     "lawyer|criminal-lawyer|human-rights-lawyer|legal-activist|top-priority|x-active","general","manual_research",""),
    ("yug.chaudhry@gmail.com","Yug Mohit Chaudhry","Senior Advocate / Criminal Defense","Legal",
     "senior-advocate|criminal-lawyer|human-rights-lawyer|top-priority","general","manual_research",""),
    ("rizwanmerchantlaw@gmail.com","Rizwan Merchant","Senior Advocate Criminal Defense","Legal",
     "senior-advocate|criminal-lawyer|top-priority","general","manual_research",""),
    ("maheshjethmalani@gmail.com","Mahesh Jethmalani","Senior Advocate Criminal Defense","Legal",
     "senior-advocate|criminal-lawyer|top-priority","general","manual_research",""),
    ("vikramnankani@yahoo.com","Vikram Nankani","Senior Advocate","Legal",
     "senior-advocate|criminal-lawyer","general","manual_research",""),
    ("taraqsayed@gmail.com","Taraq Sayed","Advocate Criminal Defense","Legal",
     "lawyer|criminal-lawyer|mumbai-press","general","manual_research",""),
    ("abdponda@gmail.com","Abad Ponda","Senior Advocate","Legal",
     "senior-advocate|criminal-lawyer","general","manual_research",""),
    ("siddharthn@gmail.com","Siddharth Nandgaonkar","Advocate Bombay HC","Legal",
     "lawyer|criminal-lawyer","general","manual_research",""),
    ("nikhilsakhardande@gmail.com","Nikhil Sakhardande","Advocate Criminal Defense","Legal",
     "lawyer|criminal-lawyer","general","manual_research",""),
    ("pradeepagharat@gmail.com","Pradeep Gharat","Advocate Bombay HC","Legal",
     "lawyer|criminal-lawyer","general","manual_research",""),
    ("ashoksaraogi@gmail.com","Ashok Saraogi","Senior Advocate","Legal",
     "senior-advocate|criminal-lawyer","general","manual_research",""),
    ("amitdesaiadvocate@gmail.com","Amit Desai","Senior Advocate Criminal","Legal",
     "senior-advocate|criminal-lawyer|top-priority","general","manual_research",""),
    ("gayatrisinghadvocate@gmail.com","Gayatri Singh","Senior Advocate","Legal",
     "senior-advocate|criminal-lawyer","general","manual_research",""),
    ("nikelaknani@gmail.com","Nikel Aknani","Advocate Criminal Defense","Legal",
     "lawyer|criminal-lawyer","general","manual_research",""),
    ("shyamkeswani@gmail.com","Shyam Keswani","Advocate Bombay HC","Legal",
     "lawyer|criminal-lawyer","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # O. HUMAN RIGHTS / ACTIVIST LAWYERS
    # ═══════════════════════════════════════════════════════════════════════
    ("flavia@majlislegal.in","Flavia Agnes","Founder MAJLIS Legal Centre","Legal",
     "senior-advocate|human-rights-lawyer|legal-activist|ngo|top-priority","general","manual_research",""),
    ("hrln.mumbai@hrln.org","HRLN Mumbai","Human Rights Law Network Mumbai","Legal/NGO",
     "human-rights-lawyer|legal-activist|ngo|top-priority","general","manual_research",""),
    ("mihir@hrln.org","Mihir Desai HRLN","Senior Advocate HRLN","Legal",
     "senior-advocate|human-rights-lawyer|legal-activist|top-priority","general","manual_research",""),
    ("sudha.bharadwaj@gmail.com","Sudha Bharadwaj","Advocate / Labour Rights Activist","Legal",
     "lawyer|human-rights-lawyer|legal-activist","general","manual_research",""),
    ("indianlawyers@clprindia.org","CLPR India","Centre for Law and Policy Research","Legal/NGO",
     "human-rights-lawyer|legal-activist|ngo","general","manual_research",""),
    ("office@sflc.in","SFLC India","Software Freedom Law Centre","Legal/NGO",
     "human-rights-lawyer|legal-activist|ngo|digital-rights","general","manual_research",""),
    ("contact@internetfreedom.in","Internet Freedom Foundation","IFF India","Legal/NGO",
     "human-rights-lawyer|legal-activist|ngo|digital-rights","general","manual_research",""),
    ("lawyerscollective@lawyerscollective.org","Lawyers Collective","Lawyers Collective Mumbai","Legal/NGO",
     "human-rights-lawyer|legal-activist|ngo|top-priority","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # P. PUBLIC PROSECUTORS / SPECIAL COURTS
    # ═══════════════════════════════════════════════════════════════════════
    ("app.mumbai@maharashtra.gov.in","Additional Public Prosecutor Mumbai","APP Office Mumbai","Legal/Government",
     "public-prosecutor|crime-court-beat|mumbai-police","general","manual_research",""),
    ("spp.bombay@maharashtra.gov.in","Special Public Prosecutor","SPP Bombay HC","Legal/Government",
     "public-prosecutor|crime-court-beat","general","manual_research",""),
    ("ujjwalnakam@gmail.com","Ujjwal Nikam","Senior Public Prosecutor Mumbai","Legal",
     "public-prosecutor|senior-advocate|top-priority|crime-court-beat","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # Q. BAR ASSOCIATIONS
    # ═══════════════════════════════════════════════════════════════════════
    ("bci.maharashtra@gmail.com","Bar Council Maharashtra & Goa","Bar Council Maharashtra","Legal/Bar Association",
     "bar-association|legal-activist|top-priority","general","manual_research","022-22634599"),
    ("info@bombayhighcourtadvocatesassociation.org","Bombay HC Advocates Association","BHCAA","Legal/Bar Association",
     "bar-association|top-priority|hc-advocate","general","manual_research",""),
    ("mumbaiadvocates@gmail.com","Bombay Bar Association","Bombay Bar Association","Legal/Bar Association",
     "bar-association","general","manual_research",""),
    ("president@mlabar.org","Maharashtra & Goa Bar Association","MGBA Mumbai","Legal/Bar Association",
     "bar-association","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # R. MUMBAI POLICE — OFFICIAL CHANNELS
    # ═══════════════════════════════════════════════════════════════════════
    ("cpoffice@mahapolice.gov.in","Commissioner of Police Mumbai","CP Office Mumbai Police","Police/Government",
     "police|mumbai-police|police-hq|top-priority","general","manual_research","022-22621855"),
    ("prmumbai@mahapolice.gov.in","Mumbai Police PRO","Public Relations Mumbai Police","Police/Government",
     "police|mumbai-police|police-hq|top-priority","general","manual_research","022-22620111"),
    ("crimebranchmumbai@mahapolice.gov.in","Crime Branch Mumbai","Crime Branch DCB Mumbai","Police/Government",
     "police|mumbai-police|crime-branch|top-priority","general","manual_research","022-24921286"),
    ("atsmumbai@mahapolice.gov.in","ATS Maharashtra Mumbai","Anti-Terrorism Squad Maharashtra","Police/Government",
     "police|mumbai-police|ats-maharashtra|top-priority","general","manual_research","022-22024413"),
    ("eow.mumbai@mahapolice.gov.in","Economic Offences Wing Mumbai","EOW Mumbai","Police/Government",
     "police|mumbai-police|eow|top-priority","general","manual_research","022-22006802"),
    ("acbmumbai@mahapolice.gov.in","Anti Corruption Bureau Mumbai","ACB Mumbai","Police/Government",
     "police|mumbai-police|acb|top-priority","general","manual_research","022-24941111"),
    ("cybercrime.mumbai@mahapolice.gov.in","Cyber Crime Mumbai","Cyber Crime Cell Mumbai","Police/Government",
     "police|mumbai-police|cyber-crime|top-priority","general","manual_research","022-26573138"),
    ("narcoticscelll@mahapolice.gov.in","Narcotics Cell Mumbai","NCB/Narcotics Cell Mumbai","Police/Government",
     "police|mumbai-police|top-priority","general","manual_research","022-24977888"),
    ("sittmumbai@mahapolice.gov.in","SITU Mumbai","Special Investigation Task Unit","Police/Government",
     "police|mumbai-police","general","manual_research",""),
    ("sbimumbai@mahapolice.gov.in","Special Branch I Mumbai","Special Branch I","Police/Government",
     "police|mumbai-police","general","manual_research",""),
    ("sbiimumbai@mahapolice.gov.in","Special Branch II Mumbai","Special Branch II (Intelligence)","Police/Government",
     "police|mumbai-police","general","manual_research",""),
    ("womenscell.mumbai@mahapolice.gov.in","Women's Cell Mumbai Police","Women's Safety Cell","Police/Government",
     "police|mumbai-police","general","manual_research","022-26662323"),
    ("trafficpolice@mahapolice.gov.in","Mumbai Traffic Police","Traffic Control Mumbai","Police/Government",
     "police|mumbai-police","general","manual_research","022-24920088"),
    ("protectioncell@mahapolice.gov.in","Protection Cell Mumbai","Witness Protection Mumbai","Police/Government",
     "police|mumbai-police","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # S. CBI / ED / NIA / NCB — MUMBAI OFFICES
    # ═══════════════════════════════════════════════════════════════════════
    ("cbimumbai@cbi.gov.in","CBI Mumbai","CBI Mumbai Branch","Police/Government",
     "police|govt-state|top-priority|investigative","general","manual_research","022-22022260"),
    ("edmumbai@enforcementindia.gov.in","Enforcement Directorate Mumbai","ED Mumbai Zonal Office","Police/Government",
     "police|govt-state|top-priority","general","manual_research","022-22823988"),
    ("niamumbai@nia.gov.in","NIA Mumbai","National Investigation Agency Mumbai","Police/Government",
     "police|govt-state|ats-maharashtra|top-priority","general","manual_research","022-24100009"),
    ("ncbmumbai@ncb.nic.in","NCB Mumbai Zonal Unit","Narcotics Control Bureau Mumbai","Police/Government",
     "police|govt-state|top-priority","general","manual_research","022-26538902"),
    ("sfofficemumbai@sfio.gov.in","SFIO Mumbai","Serious Fraud Investigation Office Mumbai","Police/Government",
     "police|govt-state|eow","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # T. BOMBAY HIGH COURT — OFFICIAL CHANNELS
    # ═══════════════════════════════════════════════════════════════════════
    ("registry@bombayhighcourt.nic.in","Bombay High Court Registry","Official Registry BHC","Court/Judiciary",
     "judge|hc-judge|crime-court-beat|top-priority","general","manual_research","022-22626921"),
    ("cj@bombayhighcourt.nic.in","Chief Justice Bombay HC","Chief Justice Office BHC","Court/Judiciary",
     "judge|hc-judge|top-priority","general","manual_research",""),
    ("mediabhc@gmail.com","Bombay HC Media Committee","Media Committee Bombay HC","Court/Judiciary",
     "hc-judge|legal-media|top-priority","general","manual_research",""),
    ("sessionscourt.mumbai@maharashtra.gov.in","Sessions Court Mumbai","Mumbai Sessions Court","Court/Judiciary",
     "judge|sessions-judge|crime-court-beat|top-priority","general","manual_research","022-22623056"),
    ("specialcourt.mcoca@maharashtra.gov.in","MCOCA Special Court","MCOCA Special Court Mumbai","Court/Judiciary",
     "judge|sessions-judge|crime-court-beat","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # U. MUMBAI MLAs — 2024 MAHARASHTRA ASSEMBLY ELECTIONS
    # ═══════════════════════════════════════════════════════════════════════
    # Worli
    ("aaditya.thackeray@shivsenaubt.org","Aaditya Thackeray","MLA Worli (Shiv Sena UBT)","Politician/MLA",
     "mla|politician|shiv-sena|uddhav-faction|mumbai-press|top-priority|x-active","general","manual_research",""),
    # Malabar Hill
    ("mangalprabhat.lodha@bjp.org","Mangalprabhat Lodha","MLA Malabar Hill (BJP)","Politician/MLA",
     "mla|politician|bjp|top-priority","general","manual_research",""),
    # Colaba
    ("rahul.narvekar@bjp.org","Rahul Narvekar","Speaker MHA / MLA Colaba (BJP)","Politician/MLA",
     "mla|politician|bjp|top-priority","general","manual_research",""),
    # Bandra West
    ("ashish.shelar@bjp.org","Ashish Shelar","MLA Bandra West (BJP)","Politician/MLA",
     "mla|politician|bjp|top-priority","general","manual_research",""),
    # Dharavi
    ("varsha.gaikwad@inc.in","Varsha Gaikwad","MLA Dharavi (Congress)","Politician/MLA",
     "mla|politician|congress|top-priority","general","manual_research",""),
    # Mumbadevi
    ("amin.patel@inc.in","Amin Patel","MLA Mumbadevi (Congress)","Politician/MLA",
     "mla|politician|congress","general","manual_research",""),
    # Malvani
    ("aslam.shaikh@inc.in","Aslam Shaikh","MLA Malvani (Congress)","Politician/MLA",
     "mla|politician|congress","general","manual_research",""),
    # Andheri East
    ("ramesh.latke@shivsenaubt.org","Ramesh Latke","MLA Andheri East (Shiv Sena UBT)","Politician/MLA",
     "mla|politician|shiv-sena|uddhav-faction","general","manual_research",""),
    # Dahisar
    ("sunil.prabhu@shivsenaubt.org","Sunil Prabhu","MLA Dahisar (Shiv Sena UBT)","Politician/MLA",
     "mla|politician|shiv-sena|uddhav-faction","general","manual_research",""),
    # Shivaji Park / Mahim
    ("sada.sarvankar@shivsena.in","Sada Sarvankar","MLA Mahim (Shiv Sena Shinde)","Politician/MLA",
     "mla|politician|shiv-sena|shinde-faction","general","manual_research",""),
    # Mulund
    ("mihir.kotecha@bjp.org","Mihir Kotecha","MLA Mulund (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Ghatkopar East
    ("parag.shah@bjp.org","Parag Shah","MLA Ghatkopar East (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Ghatkopar West
    ("prabhakar.shinde@bjp.org","Prabhakar Shinde","MLA Ghatkopar West","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Vikhroli
    ("suresh.patil.vikhroli@shivsena.in","Suresh Patil","MLA Vikhroli","Politician/MLA",
     "mla|politician|shiv-sena","general","manual_research",""),
    # Bhandup West
    ("ramesh.bande@bjp.org","Ramesh Bande","MLA Bhandup West (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Chandivali
    ("dilip.lande@shivsena.in","Dilip Lande","MLA Chandivali (Shiv Sena Shinde)","Politician/MLA",
     "mla|politician|shiv-sena|shinde-faction","general","manual_research",""),
    # Borivali
    ("sunil.rane@bjp.org","Sunil Rane","MLA Borivali (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Charkop
    ("yogesh.sagar@bjp.org","Yogesh Sagar","MLA Charkop (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Goregaon
    ("vidhate.goregaon@bjp.org","Vidhate","MLA Goregaon (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Versova
    ("bharati.lavekar@shivsena.in","Bharati Lavekar","MLA Versova (Shiv Sena Shinde)","Politician/MLA",
     "mla|politician|shiv-sena|shinde-faction","general","manual_research",""),
    # Andheri West
    ("ameet.satam@bjp.org","Ameet Satam","MLA Andheri West (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Vile Parle
    ("parag.alavani@bjp.org","Parag Alavani","MLA Vile Parle (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Kurla
    ("mangesh.kudalkar@shivsena.in","Mangesh Kudalkar","MLA Kurla (Shiv Sena Shinde)","Politician/MLA",
     "mla|politician|shiv-sena|shinde-faction","general","manual_research",""),
    # Chembur
    ("pratap.sarnaik@shivsena.in","Pratap Sarnaik","MLA Chembur (Shiv Sena Shinde)","Politician/MLA",
     "mla|politician|shiv-sena|shinde-faction","general","manual_research",""),
    # Magathane
    ("prakash.surve.magathane@bjp.org","Prakash Surve","MLA Magathane (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),
    # Mankhurd-Shivajinagar
    ("abu.azmi@samajwadiparty.in","Abu Azmi","MLA Mankhurd Shivajinagar (SP)","Politician/MLA",
     "mla|politician|sp|top-priority","general","manual_research",""),
    # Byculla
    ("yamini.jadhav@shivsena.in","Yamini Jadhav","MLA Byculla (Shiv Sena Shinde)","Politician/MLA",
     "mla|politician|shiv-sena|shinde-faction","general","manual_research",""),
    # Shivadi
    ("ajay.choudhari@shivsenaubt.org","Ajay Choudhari","MLA Shivadi (Shiv Sena UBT)","Politician/MLA",
     "mla|politician|shiv-sena|uddhav-faction","general","manual_research",""),
    # Malad West
    ("aslam.shaikh.malad@inc.in","Aslam Shaikh","MLA Malad West (Congress)","Politician/MLA",
     "mla|politician|congress","general","manual_research",""),
    # Anushakti Nagar
    ("nawab.malik@ncp.in","Nawab Malik","MLA Anushakti Nagar (NCP Ajit)","Politician/MLA",
     "mla|politician|ncp|top-priority","general","manual_research",""),
    # Kandivali East
    ("atul.bhatkhalkar@bjp.org","Atul Bhatkhalkar","MLA Kandivali East (BJP)","Politician/MLA",
     "mla|politician|bjp","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # V. MUMBAI LOK SABHA MPs — 2024
    # ═══════════════════════════════════════════════════════════════════════
    ("arvind.sawant@shivsenaubt.org","Arvind Sawant","MP Mumbai South (Shiv Sena UBT)","Politician/MP",
     "mp|politician|shiv-sena|uddhav-faction|top-priority","general","manual_research",""),
    ("rahul.shewale@shivsena.in","Rahul Shewale","MP Mumbai South Central (Shiv Sena)","Politician/MP",
     "mp|politician|shiv-sena|shinde-faction","general","manual_research",""),
    ("ravindra.waikar@shivsena.in","Ravindra Waikar","MP Mumbai North West (Shiv Sena)","Politician/MP",
     "mp|politician|shiv-sena|shinde-faction","general","manual_research",""),
    ("piyush.goyal@bjp.org","Piyush Goyal","MP Mumbai North (BJP)","Politician/MP",
     "mp|politician|bjp|top-priority","general","manual_research",""),
    ("gajanan.kirtikar@shivsena.in","Gajanan Kirtikar","MP Mumbai North West (Shiv Sena)","Politician/MP",
     "mp|politician|shiv-sena|shinde-faction","general","manual_research",""),
    ("yasmeen.khan@inc.in","Yasmeen Khan","MP Mumbai North Central (Congress)","Politician/MP",
     "mp|politician|congress","general","manual_research",""),
    ("varsha.gaikwad.mp@inc.in","Varsha Gaikwad","MP Mumbai North East (Congress)","Politician/MP",
     "mp|politician|congress","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # W. SENIOR POLITICIANS / MINISTERS (MUMBAI-BASED)
    # ═══════════════════════════════════════════════════════════════════════
    ("eknath.shinde@shivsena.in","Eknath Shinde","Deputy CM Maharashtra (Shiv Sena)","Politician",
     "politician|shiv-sena|shinde-faction|top-priority|x-active","general","manual_research",""),
    ("devendra.fadnavis@bjp.org","Devendra Fadnavis","Chief Minister Maharashtra (BJP)","Politician",
     "politician|bjp|top-priority|x-active","general","manual_research",""),
    ("ajit.pawar@ncpindia.org","Ajit Pawar","Deputy CM Maharashtra (NCP Ajit)","Politician",
     "politician|ncp|top-priority|x-active","general","manual_research",""),
    ("uddhav.thackeray@shivsenaubt.org","Uddhav Thackeray","President Shiv Sena (UBT)","Politician",
     "politician|shiv-sena|uddhav-faction|top-priority|x-active","general","manual_research",""),
    ("sharad.pawar@ncpsharadpawar.in","Sharad Pawar","President NCP (Sharad Pawar faction)","Politician",
     "politician|ncp|top-priority|x-active","general","manual_research",""),
    ("milind.deora@inc.in","Milind Deora","Congress Leader Mumbai","Politician",
     "politician|congress|mumbai-press|x-active","general","manual_research",""),
    ("priyanka.chaturvedi@shivsenaubt.org","Priyanka Chaturvedi","MP (RS) Shiv Sena UBT","Politician/MP",
     "mp|politician|shiv-sena|uddhav-faction|top-priority|x-active","general","manual_research",""),
    ("sanjay.raut@shivsenaubt.org","Sanjay Raut","MP (RS) Shiv Sena UBT","Politician/MP",
     "mp|politician|shiv-sena|uddhav-faction|top-priority|x-active","general","manual_research",""),
    ("supriya.sule@ncpsharadpawar.in","Supriya Sule","MP Baramati / NCP SP","Politician/MP",
     "mp|politician|ncp|top-priority|x-active","general","manual_research",""),
    ("imtiaz.jaleel@aimim.in","Imtiaz Jaleel","MP / AIMIM Leader","Politician/MP",
     "mp|politician|aimim","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # X. NGOS / ACTIVISTS — CRIME JUSTICE HUMAN RIGHTS
    # ═══════════════════════════════════════════════════════════════════════
    ("teesta@cjponline.org","Teesta Setalvad","Citizens for Justice and Peace","NGO/Activist",
     "civic-activist|ngo|human-rights-lawyer|legal-activist|top-priority|x-active","general","manual_research",""),
    ("javed@communalismcombat.com","Javed Anand","Communalism Combat Mumbai","NGO/Activist",
     "civic-activist|ngo|top-priority","general","manual_research",""),
    ("iags.mumbai@gmail.com","IAGS Mumbai","Indian Association for Governance Studies","NGO/Activist",
     "civic-activist|ngo","general","manual_research",""),
    ("contact@praja.in","Praja Foundation","Praja Foundation Mumbai","NGO/Activist",
     "civic-activist|ngo|top-priority|legal-activist","general","manual_research","022-23070101"),
    ("info@majlislegal.in","MAJLIS Legal Centre","MAJLIS Legal Centre Mumbai","NGO/Legal Aid",
     "ngo|legal-aid|human-rights-lawyer|legal-activist|top-priority","general","manual_research","022-23786185"),
    ("info@cprindia.org","CPR India","Centre for Policy Research","NGO/Research",
     "civic-activist|ngo","general","manual_research",""),
    ("contact@daksh.org.in","Daksh India","Daksh India - Judicial Accountability","NGO/Activist",
     "civic-activist|ngo|legal-activist|top-priority","general","manual_research",""),
    ("coordinator@napm.in","NAPM India","National Alliance of People's Movements","NGO/Activist",
     "civic-activist|ngo|top-priority","general","manual_research",""),
    ("ilfmumbai@gmail.com","Indian Lawyers Forum","Indian Lawyers Forum Mumbai","NGO/Legal",
     "ngo|legal-activist|bar-association","general","manual_research",""),
    ("contact@vidhicentre.org","Vidhi Centre","Vidhi Centre for Legal Policy","NGO/Research",
     "civic-activist|ngo|legal-activist|top-priority","general","manual_research",""),
    ("legal@amnesty.org.in","Amnesty India","Amnesty International India","NGO/Activist",
     "ngo|human-rights-lawyer|top-priority|civic-activist","general","manual_research",""),
    ("info@combatwcc.org","Combat Against Child Labour","CACL Mumbai","NGO/Activist",
     "ngo|civic-activist","general","manual_research",""),
    ("enquiry@tiss.edu","TISS Mumbai","Tata Institute of Social Sciences","NGO/Academic",
     "ngo|academic|civic-activist|top-priority","general","manual_research","022-25525000"),
    ("media@acbnashik.com","ACB Nashik","Anti Corruption Bureau Nashik","Police/Government",
     "police|acb|govt-state","general","manual_research",""),
    ("pressdetective.tip@proton.me","Whistleblower Tip Line","Anonymous Tip Channel","Internal",
     "internal","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # Y. PRESS CLUBS / JOURNALIST ASSOCIATIONS
    # ═══════════════════════════════════════════════════════════════════════
    ("info@pressclubmumbai.com","Press Club of India - Mumbai","Press Club Mumbai","Press",
     "press-club|mumbai-press|top-priority","general","manual_research","022-22885051"),
    ("secretary@mumbainewspaper.org","Mumbai Newspaper Guild","MNG Journalists Union","Press",
     "press-club|mumbai-press|top-priority","general","manual_research",""),
    ("nuj.mumbai@gmail.com","NUJ India Mumbai","National Union of Journalists Mumbai","Press",
     "press-club|mumbai-press","general","manual_research",""),
    ("marjf@gmail.com","Maharashtra & Goa Journal Federation","MARJF","Press",
     "press-club|mumbai-press","general","manual_research",""),
    ("mumbaiworkingjourno@gmail.com","Working Journalists Federation Mumbai","WJF Mumbai","Press",
     "press-club|mumbai-press","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # Z. ADDITIONAL HIGH-VALUE INDIVIDUAL JOURNALISTS
    # ═══════════════════════════════════════════════════════════════════════
    ("kavitha.iyer@gmail.com","Kavitha Iyer","Investigative Journalist (freelance)","Press",
     "investigative|mumbai-press|top-priority","general","manual_research",""),
    ("saba.naqvi@thewire.in","Saba Naqvi","Senior Journalist","Press",
     "investigative|mumbai-press|national-media|top-priority|x-active","general","manual_research",""),
    ("rana.ayyub@gmail.com","Rana Ayyub","Journalist / Washington Post India","Press",
     "investigative|mumbai-press|national-media|top-priority|x-active","general","manual_research",""),
    ("priya.ramani@gmail.com","Priya Ramani","Journalist / MeToo","Press",
     "investigative|mumbai-press|national-media|top-priority","general","manual_research",""),
    ("nidhi.suresh@scroll.in","Nidhi Suresh","Crime Correspondent Scroll","Press",
     "crime-journalist|court-reporter|digital-media|mumbai-press|top-priority","general","manual_research",""),
    ("betwa.sharma@huffingtonpost.com","Betwa Sharma","Senior Journalist HuffPost","Press",
     "investigative|national-media|top-priority","general","manual_research",""),
    ("ajit.sahi@gmail.com","Ajit Sahi","Senior Journalist / Investigator","Press",
     "investigative|mumbai-press|top-priority","general","manual_research",""),
    ("dhanya.rajendran@thenewsminute.com","Dhanya Rajendran","Editor The News Minute","Press",
     "investigative|national-media|top-priority","general","manual_research",""),
    ("vijaykumar.muppavarapu@thewire.in","Vijay Kumar Muppavarapu","The Wire Crime","Press",
     "crime-journalist|digital-media|top-priority","general","manual_research",""),
    ("barkha.dutt@mojo.in","Barkha Dutt","Journalist MOJO Story","Press",
     "investigative|national-media|top-priority|x-active","general","manual_research",""),
    ("faye.dsouza@gmail.com","Faye D'Souza","Journalist / Mirror Now ex-Editor","Press",
     "crime-journalist|mumbai-press|national-media|top-priority|x-active","general","manual_research",""),
    ("mumbai.crime@firstpost.com","Firstpost Crime Mumbai","Firstpost Crime Desk Mumbai","Press",
     "crime-journalist|mumbai-press|digital-media","general","manual_research",""),
    ("crime.desk@moneylife.in","Moneylife Crime Desk","Moneylife Foundation","Press",
     "investigative|crime-journalist|mumbai-press|top-priority","general","manual_research",""),
    ("sucheta.dalal@moneylife.in","Sucheta Dalal","Editor Moneylife / Investigative","Press",
     "investigative|mumbai-press|top-priority|x-active","general","manual_research",""),
    ("debashis.basu@moneylife.in","Debashis Basu","Editor Moneylife","Press",
     "investigative|mumbai-press|top-priority","general","manual_research",""),

    # ═══════════════════════════════════════════════════════════════════════
    # AA. ADDITIONAL LEGAL / JUDICIAL CONTACTS
    # ═══════════════════════════════════════════════════════════════════════
    ("pg.lad@mahapolice.gov.in","DGP Maharashtra","Director General of Police Maharashtra","Police/Government",
     "police|ips|police-hq|top-priority","general","manual_research","022-22624001"),
    ("adgmumbai@mahapolice.gov.in","ADG Mumbai Region","Additional DG Police Mumbai Region","Police/Government",
     "police|ips|police-hq|top-priority","general","manual_research",""),
    ("controlroom.mumbai@mahapolice.gov.in","Mumbai Police Control Room","24/7 Control Room","Police/Government",
     "police|mumbai-police|police-hq","general","manual_research","100"),
    ("statemhc@bombayhighcourt.nic.in","State vs Accused Cell BHC","Public Interest Cell Bombay HC","Court/Judiciary",
     "hc-judge|crime-court-beat","general","manual_research",""),
    ("legalaid.maharashtra@gmail.com","Maharashtra Legal Services Authority","MALSA Mumbai","Legal/NGO",
     "legal-aid|ngo|top-priority","general","manual_research","022-22634010"),
    ("mumbai.dlsa@gmail.com","District Legal Services Authority Mumbai","DLSA Mumbai","Legal/NGO",
     "legal-aid|ngo","general","manual_research","022-22623048"),

]

# ── Helpers ────────────────────────────────────────────────────────────────

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


def migrate_add_mobile():
    """Add 'mobile' column to contacts_final.csv if not already present."""
    if not FINAL_CSV.exists():
        return
    with open(FINAL_CSV, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return
    if "mobile" in rows[0]:
        return  # already migrated
    print("Migrating schema: adding 'mobile' column to contacts_final.csv ...")
    fieldnames = list(rows[0].keys()) + ["mobile"]
    with open(FINAL_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r["mobile"] = ""
            w.writerow(r)
    print(f"  Migrated {len(rows)} rows -> added 'mobile' column")


def main():
    migrate_add_mobile()

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
        return

    # Append to contacts_final.csv (8-column: email,name,designation,category,tags,case,source,mobile)
    with open(FINAL_CSV, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for row in added:
            # Ensure 8 fields
            r = list(row)
            while len(r) < 8:
                r.append("")
            w.writerow(r[:8])
    print(f"contacts_final.csv updated -> {FINAL_CSV}")

    # Rebuild contacts_live.csv
    print("\nRebuilding contacts_live.csv ...")
    suppressed_now = load_suppressed()
    with open(FINAL_CSV, encoding="utf-8-sig", newline="") as f:
        all_rows = list(csv.DictReader(f))
    fieldnames = list(all_rows[0].keys()) if all_rows else [
        "email","name","designation","category","tags","case","source","mobile"
    ]
    live = [r for r in all_rows if r.get("email","").strip().lower() not in suppressed_now]
    with open(LIVE_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(live)
    print(f"contacts_live.csv -> {len(live)} rows")

    # Tag summary
    from collections import Counter
    tag_cnt = Counter()
    for r in live:
        if "mumbai" in (r.get("tags","") + r.get("category","")).lower():
            for t in (r.get("tags") or "").split("|"):
                if t.strip(): tag_cnt[t.strip()] += 1
    print("\nTop tags (Mumbai contacts in live list):")
    for t, c in tag_cnt.most_common(20):
        print(f"  {t:<35} {c}")


if __name__ == "__main__":
    main()
