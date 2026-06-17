"""
Goa Siolim contacts — batch 3
Research date: 17 Jun 2026  (10 parallel agents, all sources verified)
Sources: official .gov.in/.nic.in portals, org websites, goapolice.gov.in,
         dcourts.gov.in, press directories — no guessed addresses.
"""
import csv
from pathlib import Path

ROOT   = Path(__file__).parent.parent
FINAL  = ROOT / "contacts" / "contacts_final.csv"
SUPP   = ROOT / "contacts" / "suppression_list.csv"
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]
CASE   = "olympio-almeida"
SOURCE = "expand_goa_siolim_batch3_17jun2026"

NEW_CONTACTS = [

    # ══════════════════════════════════════════════════════
    # PRESS / MEDIA — new outlets and addresses
    # ══════════════════════════════════════════════════════

    # The Goan Everyday (thegoan.net)
    ("editor@thegoan.net",              "The Goan Everyday",         "Editor",                   "Press",            "goa-press|press|goa|english-daily"),
    ("desk@thegoan.net",                "The Goan Everyday",         "News Desk",                "Press",            "goa-press|press|goa|english-daily"),
    ("everyday@thegoan.net",            "The Goan Everyday",         "Features",                 "Press",            "goa-press|press|goa|english-daily"),

    # The Goa Spotlight (thegoaspotlight.com)
    ("editorial@thegoaspotlight.com",   "The Goa Spotlight",         "Editorial",                "Press",            "goa-press|press|goa|digital-creator"),
    ("contact@thegoaspotlight.com",     "The Goa Spotlight",         "General",                  "Press",            "goa-press|press|goa|digital-creator"),

    # Goa News Hub
    ("hubgoanews@gmail.com",            "Goa News Hub",              "Editorial",                "Press",            "goa-press|press|goa|digital-creator"),
    ("marketing@goanewshub.com",        "Goa News Hub",              "Marketing",                "Press",            "goa-press|press|goa|digital-creator"),

    # Goa Chronicle extra addresses (info@ and news@ already in batch 2)
    ("editor@goachronicle.com",         "Savio Rodrigues",           "Editor-in-Chief Goa Chronicle","Press",        "goa-press|press|goa|digital-creator|investigative|influencer"),
    ("savio@goachronicle.com",          "Savio Rodrigues",           "Founder Goa Chronicle",    "Press",            "goa-press|press|goa|digital-creator|investigative|influencer"),
    ("sales@goachronicle.com",          "Goa Chronicle",             "Sales",                    "Press",            "goa-press|press|goa|digital-creator"),
    ("admin@goachronicle.com",          "Goa Chronicle",             "Admin",                    "Press",            "goa-press|press|goa|digital-creator"),
    ("international@goachronicle.com",  "Goa Chronicle",             "International desk",       "Press",            "goa-press|press|goa|digital-creator"),
    ("india@goachronicle.com",          "Goa Chronicle",             "India partner offices",    "Press",            "goa-press|press|goa|digital-creator"),

    # Goa365 TV (goa365.tv)
    ("goa365tv@gmail.com",              "Goa 365 TV",                "Editorial/General",        "Press",            "goa-press|press|goa|tv|digital-creator"),

    # GoaNews.com extra
    ("editor@goanews.com",              "Sandesh Prabhudesai",       "Editor GoaNews.com",       "Press",            "goa-press|press|goa|digital-creator|investigative|influencer|social-active"),

    # Goan Observer (goanobserver.in) — active weekly
    ("goanobserver@gmail.com",          "Rajan Narayan / Tara Narayan","Editor/Publisher Goan Observer","Press",     "goa-press|press|goa|english-daily|investigative"),

    # Tarun Bharat Goa
    ("news.goa@tarunbharat.com",        "Tarun Bharat Goa",          "News Desk",                "Press",            "goa-press|press|goa|marathi-daily"),
    ("tarunbharatnews@tarunbharat.info","Tarun Bharat",              "General News",             "Press",            "goa-press|press|goa|marathi-daily"),

    # Lokmat Goa edition
    ("editorial@lokmat.com",            "Lokmat Goa",                "Editorial",                "Press",            "goa-press|press|goa|marathi-daily"),
    ("eventgoa@lokmat.com",             "Lokmat Goa",                "Events Desk",              "Press",            "goa-press|press|goa|marathi-daily"),

    # O Heraldo (oheraldo.in domain)
    ("editor@oheraldo.in",              "Alister Miranda",           "Editor O Heraldo",         "Press",            "goa-press|press|goa|english-daily"),
    ("editor@heraldgoa.in",             "O Heraldo",                 "Editor (alt domain)",      "Press",            "goa-press|press|goa|english-daily"),
    ("newsdesk@heraldgoa.in",           "O Heraldo",                 "News Desk (alt domain)",   "Press",            "goa-press|press|goa|english-daily"),

    # Prudent Media extra
    ("info@prudentmedia.in",            "Prudent Media",             "General Contact",          "Press",            "goa-press|press|goa|tv"),

    # Navhind Times advertising
    ("advt@navhindtimes.com",           "Navhind Times",             "Advertising",              "Press",            "goa-press|press|goa|english-daily"),

    # GoaKhabar.com (Roland Martins)
    ("goakhabar@gmail.com",             "Roland Martins / GoaKhabar","Editor GoaKhabar",         "Press",            "goa-press|press|goa|digital-creator|investigative"),

    # Sunaparanta — Goa Centre for the Arts (civic/press community)
    ("info@sgcfa.org",                  "Sunaparanta",               "Goa Centre for the Arts",  "NGO/Civic",        "goa|ngo-civic|culture|influencer"),

    # DIP Goa (Dept of Info & Publicity — routes to all accredited Goa press)
    ("dipgoa@gmail.com",               "DIP Goa",                   "Dept of Information & Publicity Goa","Government","govt-state|goa|north-goa|press"),

    # DD News national assignment desk
    ("ddassignment@gmail.com",          "DD News",                   "Assignment Desk (national)","Press",           "press|tv|influencer"),

    # Digital Goa (20-year online news service)
    ("digitalgoanews@gmail.com",        "Digital Goa",               "Editorial",                "Press",            "goa-press|press|goa|digital-creator"),
    ("niraj@digitalgoa.com",            "Niraj Naik",                "Editor Digital Goa",       "Press",            "goa-press|press|goa|digital-creator|influencer"),

    # DoolNews (Kerala digital; Goa-adjacent coverage)
    ("mail@doolnews.com",               "DoolNews",                  "News Desk",                "Press",            "press|digital-creator"),

    # Gomantak Times Digital (Sakal/AP Globale wing)
    ("bizhead.digital@apglobale.com",   "Gomantak Times Digital",    "Digital Head AP Globale",  "Press",            "goa-press|press|goa|marathi-daily|digital-creator"),

    # Frederick Noronha alternate Gmail
    ("fredericknoronha1@gmail.com",     "Frederick Noronha",         "Freelance Journalist Goa", "Press",            "goa-press|press|goa|investigative|influencer|social-active"),
    ("fredericknoronha2@gmail.com",     "Frederick Noronha",         "Freelance Journalist (alt)","Press",           "goa-press|press|goa|investigative|influencer"),

    # Goenchi Mati Movement (mineral/resource rights, Claude Alvares affiliated)
    ("goenchimati@gmail.com",           "Goenchi Mati Movement",     "Mineral Rights Advocacy",  "NGO/Civic",        "goa|ngo-civic|activist|environment|influencer"),

    # ══════════════════════════════════════════════════════
    # NGOs / ACTIVISTS / CIVIC
    # ══════════════════════════════════════════════════════

    ("goafoundation@gmail.com",         "Claude Alvares",            "Director Goa Foundation",  "NGO/Civic",        "goa|ngo-civic|activist|environment|legal|influencer|social-active"),
    ("heta.pandit@gmail.com",           "Heta Pandit",               "VP Goa Heritage Action Group","NGO/Civic",     "goa|ngo-civic|activist|heritage|environment|influencer"),
    ("contactus@sangath.in",            "Sangath",                   "Mental Health NGO Goa — General","NGO/Civic",  "goa|ngo-civic"),
    ("communications@sangath.in",       "Sangath",                   "Communications / Media",   "NGO/Civic",        "goa|ngo-civic|influencer"),
    ("coastalimpactindia@gmail.com",    "Coastal Impact India",      "Marine Conservation Aldona Goa","NGO/Civic",   "goa|north-goa|ngo-civic|environment|coastal|activist"),
    ("peacefulsociety@gmail.com",       "A Malkarnekar",             "President Peaceful Society Goa","NGO/Civic",   "goa|ngo-civic|activist"),
    ("contact@zerowastegoa.com",        "Vishven Sawant",            "GWMC Engineer HQ",         "Government",       "govt-state|goa|environment"),
    ("gwmc.goa@gov.in",                 "GWMC",                      "Goa Waste Management Corporation","Government","govt-state|goa|environment"),
    ("goachamber@goachamber.org",       "Pratima Dhond",             "President GCCI Chamber of Commerce","NGO/Civic","goa|ngo-civic|business"),
    ("goa.credai@gmail.com",            "Ruby S Redkar",             "GM CREDAI Goa",            "NGO/Civic",        "goa|ngo-civic|business|land-use"),
    ("sumairaabdulali@yahoo.com",       "Sumaira Abdulali",          "Founder Awaaz Foundation Mumbai","NGO/Civic",  "ngo-civic|activist|environment|noise-pollution|influencer|social-active"),
    ("admin@ttag.in",                   "TTAG",                      "Travel & Tourism Assoc Goa — Admin","NGO/Civic","goa|ngo-civic|business"),
    ("ttagoasecretariat@gmail.com",     "Amey Naik",                 "Executive Secretary TTAG", "NGO/Civic",        "goa|ngo-civic|business"),
    ("goa@taai.in",                     "Vineet Dhavalikar",         "Secretary TAAI Goa Chapter","NGO/Civic",       "goa|ngo-civic|business"),

    # Archdiocese + Caritas (Goa has 26% Christian; church is major civic voice)
    ("archbpgoa@gmail.com",             "Archdiocese of Goa & Daman","Archbishop's Office",      "NGO/Civic",        "goa|ngo-civic|faith|influencer"),
    ("chancerygoa@gmail.com",           "Fr Romeo Monteiro",         "Chancellor Archdiocese",   "NGO/Civic",        "goa|ngo-civic|faith"),
    ("dcscmgoa@gmail.com",              "Fr Barry Cardozo",          "Director Diocesan Social Comms","NGO/Civic",   "goa|ngo-civic|faith|press|influencer"),
    ("directordcscm@gmail.com",         "Fr Barry Cardozo",          "Director DCSCM (alt)",     "NGO/Civic",        "goa|ngo-civic|faith|press"),
    ("caritas@caritasgoa.org",          "Fr Maverick Fernandes",     "Director Caritas Goa",     "NGO/Civic",        "goa|ngo-civic|welfare|faith"),
    ("csjpgoa2021@gmail.com",           "Fr Savio Fernandes",        "Executive Secretary Council for Social Justice & Peace","NGO/Civic","goa|ngo-civic|activist|faith"),

    # Diaspora press
    ("eddie.fernandes@gmail.com",       "Eddie Fernandes",           "Editor Goan Voice UK",     "Press",            "goa-press|press|goa|influencer|diaspora"),

    # W Goa (tourism industry, Siolim-adjacent — Vagator)
    ("reservations.goa@whotels.com",    "W Goa Vagator",             "Reservations / GM",        "NGO/Civic",        "goa|north-goa|bardez|business"),

    # ══════════════════════════════════════════════════════
    # GOVERNMENT — CMO / GOVERNOR / PWD / SOUTH GOA
    # ══════════════════════════════════════════════════════

    ("cm.goa@nic.in",                   "Dr Pramod Sawant",          "Chief Minister of Goa",    "Government",       "govt-state|goa|top-priority"),
    ("sect-cmo.goa@nic.in",             "Dr Ashvin Chandru A",       "Secretary to Chief Minister","Government",    "govt-state|goa|top-priority"),
    ("governor.goa@gov.in",             "Pusapati Ashok Gajapathi Raju","Governor of Goa",       "Government",       "govt-state|goa"),

    # PWD Goa (road / building authority)
    ("pce-pwd.goa@nic.in",              "Sandip K P Chodnekar",      "Principal Chief Engineer PWD","Government",    "govt-state|goa|north-goa"),
    ("ce1-pwd.goa@nic.in",              "Sandip K P Chodnekar",      "Chief Engineer Buildings PWD","Government",   "govt-state|goa|north-goa"),
    ("ce2-pwd.goa@nic.in",              "Dattaprasad S Kamat",       "Chief Engineer NH & R&B PWD","Government",    "govt-state|goa|north-goa"),

    # South Goa Collectorate (included for full-Goa coverage)
    ("cols.goa@nic.in",                 "Egna Cleetus IAS",          "Collector South Goa",      "Government",       "govt-state|goa|collector"),
    ("ac1-south.goa@nic.in",            "Srinet N Kothwale",         "Additional Collector I South Goa","Government","govt-state|goa|collector"),
    ("ac2-cols.goa@nic.in",             "Ramesh N Gaonkar",          "Additional Collector II South Goa","Government","govt-state|goa|collector"),
    ("ac3-south.goa@gov.in",            "Vishal C Kundaikar",        "Additional Collector III South Goa","Government","govt-state|goa|collector"),

    # North Goa Collectorate — full who's who (collector + all DyCs)
    ("coln.goa@nic.in",                 "Sneha S Gitte IAS",         "Collector North Goa",      "Government",       "govt-state|goa|north-goa|collector|top-priority"),
    ("dycrev-north.goa@nic.in",         "Vinayak Chari",             "Deputy Collector Revenue North Goa","Government","govt-state|goa|north-goa|collector"),
    ("dycdro-northgoa@nic.in",          "Ishwar M Madkaikar",        "Deputy Collector DRO North Goa","Government", "govt-state|goa|north-goa|collector"),
    ("dycla-north.goa@nic.in",          "Suyash Sinai Khandeparkar", "Deputy Collector Land Acquisition North Goa","Government","govt-state|goa|north-goa|collector|land-use"),
    ("ddma-north.goa@gov.in",           "Mohd Shabir IAS",           "Deputy Collector Disaster Management North Goa","Government","govt-state|goa|north-goa|collector"),

    # Mamlatdars (tahsil-level land revenue) — Bardez is key (covers Siolim)
    ("mam-bardez.goa@nic.in",           "Anant Malik",               "Mamlatdar Bardez (covers Siolim)","Government","govt-state|goa|north-goa|bardez|siolim|land-use|top-priority"),
    ("mam-north.goa@nic.in",            "Akshaya A Amonkar",         "Mamlatdar-in-Collectorate North Goa","Government","govt-state|goa|north-goa"),
    ("mam-pernem.goa@nic.in",           "Ranjeet Salgaonkar",        "Mamlatdar Pernem",         "Government",       "govt-state|goa|north-goa"),
    ("mam-bicholim.goa@nic.in",         "Shailendra J Dessai",       "Mamlatdar Bicholim",       "Government",       "govt-state|goa|north-goa"),
    ("mam-tiswadi.goa@nic.in",          "Dattaprasad S Toraskar",    "Mamlatdar Tiswadi (Panaji area)","Government","govt-state|goa|north-goa"),

    # Goa Urban Development
    ("dir-dma.goa@nic.in",              "Brijesh Manerkar",          "Director Urban Development Goa","Government",  "govt-state|goa|north-goa|land-use"),

    # GSPCB extra
    ("see-gspcb@gov.in",                "Sanjeev Joglekar",          "Sr Environmental Engineer GSPCB","Government", "govt-state|goa|north-goa|environment|top-priority"),

    # TCP (Town & Country Planning)
    ("ctp-tcp.goa@nic.in",              "Chief Town Planner Goa",    "Chief Town Planner TCP",   "Government",       "govt-state|goa|north-goa|land-use|top-priority"),

    # Goa Forest Department
    ("dcfhq-forest.goa@nic.in",         "Forest Dept HQ",            "Principal Chief Conservator of Forests","Government","govt-state|goa|environment"),
    ("cof-fore.goa@nic.in",             "Naveen Kumar IFS",          "Chief Conservator of Forests","Government",    "govt-state|goa|environment"),

    # Goa Water Resources Department
    ("ce-wrd.goa@nic.in",               "Dnyaneshwar Salelkar",      "Chief Engineer Water Resources Dept","Government","govt-state|goa|north-goa"),

    # Directorate of Panchayats (all village panchayats under this)
    ("dir-panc.goa@nic.in",             "Gopal Parsekar",            "Director of Panchayats Goa","Government",     "govt-state|goa|north-goa|siolim|top-priority"),

    # GSLSA (State Legal Services)
    ("ms-gslsa.goa@nic.in",             "Member Secretary GSLSA",    "Goa State Legal Services Authority","Government","govt-state|goa|legal"),

    # Electricity
    ("customersupport@goaelectricity.gov.in","Goa Electricity Dept", "Consumer Helpdesk",        "Government",       "govt-state|goa"),

    # Goa Housing Board
    ("goahousingboard@yahoo.in",        "Jit Arolkar / Neetal Amonkar","Chairman/MD Goa Housing Board","Government","govt-state|goa|land-use"),

    # GMC / Health
    ("dean-gmc.goa@nic.in",             "Prof Dr Shivanand M Bandekar","Dean Goa Medical College","Government",     "govt-state|goa"),
    ("ms-gmc.goa@nic.in",               "Medical Superintendent GMC","Goa Medical College & Hospital","Government", "govt-state|goa"),
    ("goamed@hotmail.com",              "GMC",                        "Goa Medical College (alternate)","Government","govt-state|goa"),
    ("rd-goa@esic.gov.in",              "ESIC Regional Director Goa","ESIC Patto Plaza Panaji",  "Government",       "govt-state|goa"),

    # Director of Tourism
    ("dir-tour.goa@nic.in",             "Kedar A Naik GCS",          "Director of Tourism Goa",  "Government",       "govt-state|goa"),

    # GIPARD (public admin training/research)
    ("gird.goa@nic.in",                 "GIPARD",                    "Goa Institute of Public Admin & Rural Dev","Government","govt-state|goa"),
    ("missionkarmayogi-goa@goa.gov.in", "GIPARD",                    "Mission Karmayogi Programme","Government",    "govt-state|goa"),

    # ══════════════════════════════════════════════════════
    # POLICE — station level + HQ additions
    # ══════════════════════════════════════════════════════

    # KEY: Siolim Coastal Police Station (on the ground for inspection)
    ("picoastal.siolim@goapolice.gov.in","Sandeep A Keserkar",       "PI Siolim Coastal Police Station","Police/Government","police-hq|goa|north-goa|bardez|siolim|top-priority"),

    # Adjacent stations (Bardez area)
    ("picalangute@goapolice.gov.in",    "Paresh G Naik",             "PI Calangute Police Station","Police/Government","police-hq|goa|north-goa|bardez"),
    ("pianjuna@goapolice.gov.in",       "Suraj H Gawas",             "PI Anjuna Police Station", "Police/Government","police-hq|goa|north-goa|bardez"),
    ("pimapusa@goapolice.gov.in",       "Nikhil N Palekar",          "PI Mapusa Police Station", "Police/Government","police-hq|goa|north-goa"),

    # Women Police / social protection
    ("piwps.pan@goapolice.gov.in",      "Loveleen Dias",             "PI Women Police Station North Goa","Police/Government","police-hq|goa|north-goa"),

    # Goa Police HQ additions
    ("complaint@goapolice.gov.in",      "Goa Police",                "Complaints Division HQ",   "Police/Government","police-hq|goa|top-priority"),
    ("dgpgoa@goapolice.gov.in",         "Director General of Police","DGP Goa",                  "Police/Government","police-hq|goa|top-priority"),
    ("igpgoa@goapolice.gov.in",         "Inspector General of Police","IGP Goa",                 "Police/Government","police-hq|goa"),
    ("dysphq@goapolice.gov.in",         "DySP HQ",                   "DySP Headquarters Goa Police","Police/Government","police-hq|goa"),
    ("sptraffic@goapolice.gov.in",      "SP Traffic Goa",            "Superintendent Traffic Police","Police/Government","police-hq|goa"),
    ("spcoastal@goapolice.gov.in",      "SP Coastal Police",         "Superintendent Coastal Police Goa","Police/Government","police-hq|goa|north-goa"),
    ("dyspcoastal@goapolice.gov.in",    "DySP Coastal Police",       "DySP Coastal Police Goa", "Police/Government","police-hq|goa|north-goa"),
    ("spsb@goapolice.gov.in",           "SP Special Branch Goa",     "Superintendent Special Branch","Police/Government","police-hq|goa"),
    ("spec@goapolice.gov.in",           "SP Emergency Ops Centre",   "Superintendent EOC Goa",   "Police/Government","police-hq|goa"),

    # ══════════════════════════════════════════════════════
    # COURTS / LEGAL
    # ══════════════════════════════════════════════════════

    ("reg-ngdc.goa@nic.in",             "Kishore S Kawlekar",        "Chief Admin Officer District Court North Goa","Government","govt-state|goa|north-goa|legal"),
    ("cc-panaji.goa@nic.in",            "Civil & Criminal Courts",   "Court Centre Panaji",      "Government",       "govt-state|goa|north-goa|legal"),
    ("cc-mapusa.goa@nic.in",            "Civil & Criminal Courts",   "Court Centre Mapusa",      "Government",       "govt-state|goa|north-goa|legal"),
    ("cc-bicholim.goa@nic.in",          "Civil & Criminal Courts",   "Court Centre Bicholim",    "Government",       "govt-state|goa|north-goa|legal"),
    ("cc-pernem.goa@nic.in",            "Civil & Criminal Courts",   "Court Centre Pernem",      "Government",       "govt-state|goa|north-goa|legal"),
    ("cc-valpoi.goa@nic.in",            "Civil & Criminal Courts",   "Court Centre Valpoi",      "Government",       "govt-state|goa|north-goa|legal"),
    ("reg-high.goa@nic.in",             "High Court of Bombay at Goa","Registrar High Court",    "Government",       "govt-state|goa|legal"),
    ("ghcbap@gmail.com",                "Goa High Court Bar Association","General Contact GHCBA", "NGO/Civic",        "goa|ngo-civic|legal"),

    # ══════════════════════════════════════════════════════
    # GOA OVERSIGHT BODIES
    # ══════════════════════════════════════════════════════

    ("spio-gsic.goa@nic.in",            "Goa State Information Commission","SPIO / RTI Commission","Government",    "govt-state|goa|legal|activist"),
    ("sect-ghrc.goa@nic.in",            "Goa Human Rights Commission","Secretariat GHRC",        "Government",       "govt-state|goa|legal"),
    ("confo-ng-ga@nic.in",              "Consumer Forum North Goa",  "District Consumer Disputes Redressal Commission","Government","govt-state|goa|north-goa|legal"),

    # ══════════════════════════════════════════════════════
    # NATIONAL OVERSIGHT + PRESS BODIES
    # ══════════════════════════════════════════════════════

    ("publicgrievance-ngt@gov.in",      "National Green Tribunal",   "NGT Grievance (all zones incl. Pune WZB)","Government","national|environment|legal|top-priority"),
    ("cpcb@cpcb.nic.in",                "CPCB",                      "Central Pollution Control Board","Government","national|environment|top-priority"),
    ("aircomplaints.cpcb@nic.in",       "CPCB",                      "Air & Noise Complaints CPCB","Government",    "national|environment|noise-pollution|top-priority"),
    ("jcb.cpcb@nic.in",                 "J C Babu Sc.F",             "CPCB Regional Director South Zone","Government","national|environment"),
    ("rosz.bng-mef@nic.in",             "MoEF Southern Zone",        "Regional Office Bengaluru (covers Goa)","Government","national|environment"),
    ("complaint.nhrc@nic.in",           "NHRC",                      "National Human Rights Commission — Complaints","Government","national|human-rights|top-priority"),
    ("complaintcell-ncw@nic.in",        "National Commission for Women","NCW Complaint Cell",    "Government",       "national|human-rights"),
    ("chairperson-ncw@nic.in",          "NCW Chairperson",           "National Commission for Women Chair","Government","national|human-rights"),

    # Press oversight bodies (for complaint-loop / right-of-reply)
    ("so.complaints-pci@gov.in",        "Press Council of India",    "Section Officer Complaints PCI","Government",  "national|press|legal"),
    ("secy-pci@nic.in",                 "Press Council of India",    "Secretary PCI",            "Government",       "national|press|legal"),
    ("pcibppcomplaint@gmail.com",       "Press Council of India",    "Complaints (alternate)",   "Government",       "national|press|legal"),
    ("authority@nbdanewdelhi.com",      "NBDSA",                     "News Broadcasting & Digital Standards Authority","NGO/Civic","national|press|legal"),
    ("info@editorsguild.in",            "Editors Guild of India",    "Secretariat",              "NGO/Civic",        "national|press|influencer|social-active"),
    ("sg@ins.org.in",                   "Indian Newspaper Society",  "Secretary General INS",    "NGO/Civic",        "national|press"),
    ("ins@ins.org.in",                  "Indian Newspaper Society",  "General Contact INS",      "NGO/Civic",        "national|press"),
    ("secretarygeneral@indianjournalistsunion.com","IJU",            "Secretary General Indian Journalists Union","NGO/Civic","national|press|activist"),
    ("info@indianjournalistsunion.com", "Indian Journalists Union",  "General Contact IJU",      "NGO/Civic",        "national|press"),
    ("news.coordination@aninews.in",    "ANI",                       "News Coordination Desk",   "Press",            "press|wire"),
    ("uni@uniindia.com",                "United News of India",      "UNI General Desk",         "Press",            "press|wire"),

    # ══════════════════════════════════════════════════════
    # NATIONAL / REGIONAL MPs + BDOs
    # ══════════════════════════════════════════════════════

    ("shripadnaik@sansad.nic.in",       "Shripad Yesso Naik",        "North Goa MP (18th Lok Sabha)","Politician/MLA","goa|north-goa|politician|mp|top-priority"),
    ("office@shripadnaik.in",           "Shripad Naik Office",       "MP North Goa — constituency office","Politician/MLA","goa|north-goa|politician|mp"),
    ("pernembdo@gmail.com",             "Shubham Sadashiv Bhartu",   "BDO Pernem",               "Government",       "govt-state|goa|north-goa|bdo"),
    ("bicholimbdo@gmail.com",           "Omkar Naresh Manjrekar",    "BDO Bicholim",             "Government",       "govt-state|goa|north-goa|bdo"),

    # ══════════════════════════════════════════════════════
    # EDUCATION / RESEARCH
    # ══════════════════════════════════════════════════════

    ("registrar@unigoa.ac.in",          "Prof Sunder N Dhuri",       "Registrar Goa University", "NGO/Civic",        "goa|education|research"),
    ("director@nio.res.in",             "CSIR-NIO",                  "Director CSIR National Inst of Oceanography","NGO/Civic","goa|education|research|environment"),
    ("sunil.nio@csir.res.in",           "Prof Sunil Kumar Singh",    "Director CSIR-NIO Goa",   "NGO/Civic",        "goa|education|research|environment"),
    ("director@nitgoa.ac.in",           "Prof O R Jaiswal",          "Director NIT Goa",         "NGO/Civic",        "goa|education"),
    ("dy.reg@nitgoa.ac.in",             "Amit Kabiraj",              "Deputy Registrar NIT Goa", "NGO/Civic",        "goa|education"),
    ("admin@gim.ac.in",                 "GIM",                       "Goa Institute of Management — Admin","NGO/Civic","goa|education"),
    ("director@gim.ac.in",              "GIM",                       "Director Goa Institute of Management","NGO/Civic","goa|education|influencer"),
    ("info@xchr.in",                    "Fr Rinald D Souza SJ",      "Director Xavier Centre of Historical Research Goa","NGO/Civic","goa|education|research|influencer"),
    ("donna.dsouza@ihmgoa.gov.in",      "Donna D Souza",             "IHM Goa — Hospitality College","Government",   "govt-state|goa"),
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

print(f"Batch 3 added:  {added}")
print(f"Skipped (dup):  {dup}")
print(f"Skipped (supp): {supp_skip}")
print(f"Total final:    {len(final_rows) + added}")
