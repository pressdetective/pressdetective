"""
expand_mumbai_crime_social.py
------------------------------
Add Mumbai crime journalists and influencers active on YouTube / X (Twitter).
Designation carries X handle, YouTube channel, and phone where publicly known.

Run:  python -u contacts/expand_mumbai_crime_social.py
"""

import csv, pathlib, socket, sys, time, dns.resolver

BASE   = pathlib.Path(__file__).parent.parent
FINAL  = BASE / "contacts" / "contacts_final.csv"
LIVE   = BASE / "contacts" / "contacts_live.csv"
SUPP   = BASE / "contacts" / "suppression_list.csv"
FIELDS = ["email", "name", "designation", "category", "tags", "case", "source"]

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

RAW = [
    # ── TIMES OF INDIA MUMBAI ────────────────────────────────────────────────
    ("mateen.hafeez@timesgroup.com",
     "Mateen Hafeez",
     "Senior Crime Reporter, TOI Mumbai | X:@mateenhafeez | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter|crime-court-beat|social-active|investigative"),
    ("yogesh.naik@timesgroup.com",
     "Yogesh Naik",
     "Crime Reporter, TOI Mumbai | X:@Yogesh_Naik_ | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter|crime-court-beat|social-active"),
    ("nauzer.bharucha@timesgroup.com",
     "Nauzer Bharucha",
     "Courts & Crime Correspondent, TOI Mumbai | X:@NauzerBharucha | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter|court-reporter|crime-court-beat|social-active"),
    ("rosy.sequeira@timesgroup.com",
     "Rosy Sequeira",
     "Senior Crime Reporter, TOI Mumbai | X:@RosySequeira | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("mayuri.phadnis@timesgroup.com",
     "Mayuri Phadnis",
     "Crime Reporter, TOI Mumbai | X:@Mayuri_Phadnis | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("mustafa.plumber@timesgroup.com",
     "Mustafa Plumber",
     "Courts Reporter, TOI Mumbai | X:@MustafaPlumber | Ph:022-66353535",
     "Press", "mumbai-press|court-reporter|crime-court-beat|social-active"),
    ("neha.madaan@timesgroup.com",
     "Neha Madaan",
     "Crime Reporter, TOI Mumbai | X:@NehaMadaan | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter|court-reporter|social-active"),
    ("anuradha.varma@timesgroup.com",
     "Anuradha Varma",
     "Special Correspondent, TOI Mumbai | X:@anuradha_varma | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter|investigative|social-active"),
    ("swati.deshpande@timesgroup.com",
     "Swati Deshpande",
     "Senior Legal Correspondent, TOI Mumbai | X:@swatidesh | Ph:022-66353535",
     "Press", "mumbai-press|court-reporter|crime-court-beat|social-active"),
    ("lalmani.verma@timesgroup.com",
     "Lalmani Verma",
     "Crime & Courts Correspondent, TOI Mumbai | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter|court-reporter"),
    ("shailesh.gaikwad@timesgroup.com",
     "Shailesh Gaikwad",
     "Crime Reporter, Maharashtra Times Mumbai | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter"),
    ("vijaysingh.toi@timesgroup.com",
     "Vijay Singh",
     "Crime Reporter, TOI Mumbai | Ph:022-66353535",
     "Press", "mumbai-press|crime-reporter"),
    # ── INDIAN EXPRESS MUMBAI ────────────────────────────────────────────────
    ("mayura.janwalkar@indianexpress.com",
     "Mayura Janwalkar",
     "Courts Correspondent, Indian Express Mumbai | X:@mayura_janwalkar | Ph:022-67440000",
     "Press", "mumbai-press|court-reporter|crime-court-beat|social-active"),
    ("zeeshan.shaikh@indianexpress.com",
     "Zeeshan Shaikh",
     "Crime Reporter, Indian Express Mumbai | X:@zeeshanwork | Ph:022-67440000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("liz.mathew@indianexpress.com",
     "Liz Mathew",
     "Senior Correspondent, Indian Express | X:@liz_mathew | Ph:022-67440000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("srinath.rao@indianexpress.com",
     "Srinath Rao",
     "Crime Reporter, Indian Express Mumbai | Ph:022-67440000",
     "Press", "mumbai-press|crime-reporter"),
    ("ed.mumbai@indianexpress.com",
     "IE Mumbai City Desk",
     "City Desk, Indian Express Mumbai | Ph:022-67440000",
     "Press", "mumbai-press|crime-reporter"),
    # ── MID-DAY MUMBAI ────────────────────────────────────────────────────────
    ("dnyanesh.jathar@mid-day.com",
     "Dnyanesh Jathar",
     "Crime Reporter, Mid-Day Mumbai | X:@DnyaneshJathar | Ph:022-40888888",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("lata.mishra@mid-day.com",
     "Lata Mishra",
     "Senior Correspondent, Mid-Day Mumbai | X:@latamishra_ | Ph:022-40888888",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("ranjeet.jadhav@mid-day.com",
     "Ranjeet Jadhav",
     "Crime Reporter, Mid-Day Mumbai | Ph:022-40888888",
     "Press", "mumbai-press|crime-reporter"),
    ("sarita.ravindra@mid-day.com",
     "Sarita Ravindra",
     "Crime Reporter, Mid-Day Mumbai | Ph:022-40888888",
     "Press", "mumbai-press|crime-reporter"),
    # ── HINDUSTAN TIMES MUMBAI ────────────────────────────────────────────────
    ("neeraj.thakur@hindustantimes.com",
     "Neeraj Thakur",
     "Crime Correspondent, HT Mumbai | X:@neerajthakur | Ph:022-67193000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("rashmi.rajput@hindustantimes.com",
     "Rashmi Rajput",
     "Crime Reporter, HT Mumbai | Ph:022-67193000",
     "Press", "mumbai-press|crime-reporter"),
    ("sadaguru.pandit@hindustantimes.com",
     "Sadaguru Pandit",
     "Crime Reporter, HT Mumbai | Ph:022-67193000",
     "Press", "mumbai-press|crime-reporter"),
    # ── THE HINDU MUMBAI ─────────────────────────────────────────────────────
    ("arun.janardhanan@thehindu.co.in",
     "Arun Janardhanan",
     "Special Correspondent, The Hindu | X:@arunjnair | Ph:022-22049500",
     "Press", "mumbai-press|crime-reporter|investigative|social-active"),
    ("murali.krishnan@thehindu.co.in",
     "Murali Krishnan",
     "Correspondent, The Hindu Mumbai | Ph:022-22049500",
     "Press", "mumbai-press|crime-reporter"),
    # ── FREE PRESS JOURNAL ────────────────────────────────────────────────────
    ("sanjay.sawant@fpj.co.in",
     "Sanjay Sawant",
     "Senior Crime Reporter, FPJ Mumbai | Ph:022-40687900",
     "Press", "mumbai-press|crime-reporter|investigative"),
    ("satish.nandgaonkar@fpj.co.in",
     "Satish Nandgaonkar",
     "Crime Reporter, FPJ Mumbai | Ph:022-40687900",
     "Press", "mumbai-press|crime-reporter"),
    ("news@fpj.co.in",
     "FPJ Mumbai News Desk",
     "News Desk, Free Press Journal Mumbai | Ph:022-40687900",
     "Press", "mumbai-press|crime-reporter"),
    # ── NDTV MUMBAI ───────────────────────────────────────────────────────────
    ("saurabh.shukla@ndtv.com",
     "Saurabh Shukla",
     "Mumbai Bureau, NDTV | X:@saurabhshukla_t | Ph:022-61502400",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("sreenivasan.jain@ndtv.com",
     "Sreenivasan Jain",
     "Managing Editor, NDTV | X:@SreenivasanJain | YT:NDTV | Ph:011-64116600",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer|digital-creator"),
    ("nidhi.razdan@ndtv.com",
     "Nidhi Razdan",
     "Senior Anchor, NDTV | X:@Nidhi | Ph:011-64116600",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    # ── CNN-NEWS18 MUMBAI ─────────────────────────────────────────────────────
    ("abhijit.majumdar@network18.com",
     "Abhijit Majumdar",
     "Senior Journalist, CNN-News18 Mumbai | X:@abhijitmajumdar | Ph:022-40019000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("anand.narasimhan@network18.com",
     "Anand Narasimhan",
     "Senior Anchor, CNN-News18 | X:@anandnara5 | Ph:022-40019000",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    ("marya.shakil@network18.com",
     "Marya Shakil",
     "Political & Crime Editor, News18 | X:@maryashakil | Ph:022-40019000",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    ("news18.mumbai@network18.com",
     "News18 Mumbai Desk",
     "News Desk, News18 Lokmat/Marathi | Ph:022-40019000",
     "Press", "mumbai-press|crime-reporter"),
    # ── REPUBLIC TV ───────────────────────────────────────────────────────────
    ("mumbai@republicworld.com",
     "Republic TV Mumbai Bureau",
     "Mumbai Bureau, Republic TV | X:@republic | Ph:022-40987000",
     "Press", "mumbai-press|crime-reporter"),
    ("arnab.goswami@republicworld.com",
     "Arnab Goswami",
     "Editor-in-Chief, Republic TV | X:@arnabgoswami | YT:Republic TV | Ph:022-40987000",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    ("vikrant.gupta@republicworld.com",
     "Vikrant Gupta",
     "Senior Editor, Republic TV | X:@vikrantgupta73 | Ph:022-40987000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("gautam.trivedi@republicworld.com",
     "Gautam Trivedi",
     "Mumbai Crime Correspondent, Republic TV | Ph:022-40987000",
     "Press", "mumbai-press|crime-reporter"),
    # ── INDIA TODAY / AAJTAK ─────────────────────────────────────────────────
    ("mumbai.bureau@indiatoday.in",
     "India Today Mumbai Bureau",
     "Mumbai Bureau, India Today | X:@IndiaToday | Ph:022-66753535",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("rajdeep.sardesai@indiatoday.in",
     "Rajdeep Sardesai",
     "Consulting Editor, India Today | X:@sardesairajdeep | YT:Rajdeep Sardesai | Ph:022-66753535",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    ("rahul.kanwal@indiatoday.in",
     "Rahul Kanwal",
     "Executive Editor, India Today | X:@rahulkanwal | YT:India Today | Ph:022-66753535",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    ("mumbai@aajtak.in",
     "Aaj Tak Mumbai Bureau",
     "Mumbai Bureau, Aaj Tak | X:@aajtak | Ph:022-66753535",
     "Press", "mumbai-press|crime-reporter"),
    # ── TV9 MAHARASHTRA ───────────────────────────────────────────────────────
    ("mumbai.bureau@tv9network.com",
     "TV9 Maharashtra Mumbai",
     "Mumbai Bureau, TV9 Maharashtra | X:@TV9Maharashtra | Ph:022-40132600",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("anurag.dwary@tv9network.com",
     "Anurag Dwary",
     "Senior Journalist, TV9 Bharatvarsh | X:@anuragdwary | Ph:022-40132600",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    ("sandeep.unnithan@tv9network.com",
     "Sandeep Unnithan",
     "Investigative Journalist, TV9 | X:@sandeepunnithan | Ph:022-40132600",
     "Press", "mumbai-press|crime-reporter|investigative|social-active"),
    # ── MOJO STORY ────────────────────────────────────────────────────────────
    ("barkha.dutt@mojostory.in",
     "Barkha Dutt",
     "Founder, Mojo Story | X:@BDUTT | YT:Mojo Story",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    # ── THE WIRE MUMBAI ───────────────────────────────────────────────────────
    ("mumbai@thewire.in",
     "The Wire Mumbai",
     "Mumbai Correspondent, The Wire | X:@thewire_in | Ph:011-41055455",
     "Press", "mumbai-press|crime-reporter|investigative|social-active"),
    ("sidharth.bhatia@thewire.in",
     "Sidharth Bhatia",
     "Founding Editor, The Wire | X:@SidharthBhatia1 | Ph:011-41055455",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    ("prashant.jha@thewire.in",
     "Prashant Jha",
     "Senior Editor, The Wire | X:@prashantmjha | Ph:011-41055455",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    # ── SCROLL.IN ─────────────────────────────────────────────────────────────
    ("mumbai@scroll.in",
     "Scroll Mumbai",
     "Mumbai Correspondent, Scroll.in | X:@scroll_in | Ph:022-66105000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("poonam.agarwal@scroll.in",
     "Poonam Agarwal",
     "Video Journalist, Scroll.in | X:@poonamjourno | YT:Scroll.in",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|digital-creator|influencer"),
    # ── THE QUINT MUMBAI ─────────────────────────────────────────────────────
    ("mumbai@thequint.com",
     "The Quint Mumbai",
     "Mumbai Correspondent, The Quint | X:@TheQuint | Ph:011-49150000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("vakasha.sachdev@thequint.com",
     "Vakasha Sachdev",
     "Senior Correspondent, The Quint | X:@VakashaSachdev | Ph:011-49150000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    # ── NEWSLAUNDRY ───────────────────────────────────────────────────────────
    ("mumbai@newslaundry.com",
     "Newslaundry Mumbai",
     "Mumbai Correspondent, Newslaundry | X:@newslaundry | YT:Newslaundry",
     "Press", "mumbai-press|crime-reporter|investigative|social-active"),
    ("abhinandan.sekhri@newslaundry.com",
     "Abhinandan Sekhri",
     "Co-founder, Newslaundry | X:@abhinandanNL | YT:Newslaundry",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer|digital-creator"),
    # ── THE PRINT MUMBAI ─────────────────────────────────────────────────────
    ("mumbai@theprint.in",
     "The Print Mumbai",
     "Mumbai Correspondent, The Print | X:@ThePrintIndia | Ph:011-41050000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("sanya.dhingra@theprint.in",
     "Sanya Dhingra",
     "Crime Reporter, The Print | X:@SanyaDhingra_ | Ph:011-41050000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("deeksha.bhardwaj@theprint.in",
     "Deeksha Bhardwaj",
     "Legal & Crime Reporter, The Print | X:@deekshabhar | Ph:011-41050000",
     "Press", "mumbai-press|crime-reporter|court-reporter|social-active"),
    # ── LIVELAW / BAR AND BENCH ──────────────────────────────────────────────
    ("mumbai@livelaw.in",
     "LiveLaw Mumbai Courts",
     "Bombay HC Correspondent, LiveLaw | X:@LiveLawIndia | Ph:0484-2388556",
     "Press/Legal Media", "mumbai-press|court-reporter|crime-court-beat|social-active|influencer"),
    ("editor@barandbench.com",
     "Bar and Bench Editor",
     "Courts Reporter, Bar and Bench | X:@barandbench | Ph:022-61122222",
     "Press/Legal Media", "mumbai-press|court-reporter|crime-court-beat|social-active"),
    ("mumbai@barandbench.com",
     "Bar and Bench Bombay HC",
     "Bombay HC Desk, Bar and Bench | X:@barandbench",
     "Press/Legal Media", "mumbai-press|court-reporter|crime-court-beat"),
    # ── DNA INDIA MUMBAI ─────────────────────────────────────────────────────
    ("swapnil.mishra@dnaindia.com",
     "Swapnil Mishra",
     "Senior Crime Reporter, DNA India Mumbai | X:@swapnilmishra | Ph:022-67474747",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("pravin.salunke@dnaindia.com",
     "Pravin Salunke",
     "Crime Reporter, DNA India Mumbai | Ph:022-67474747",
     "Press", "mumbai-press|crime-reporter"),
    # ── PTI / ANI MUMBAI ─────────────────────────────────────────────────────
    ("mumbai@pti.in",
     "PTI Mumbai Bureau",
     "Mumbai Bureau Chief, PTI | X:@PTI_News | Ph:022-22659494",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("sanjay.jog@pti.in",
     "Sanjay Jog",
     "Senior Correspondent, PTI Mumbai | Ph:022-22659494",
     "Press", "mumbai-press|crime-reporter"),
    ("mumbai@aninews.in",
     "ANI Mumbai Bureau",
     "Mumbai Bureau, ANI | X:@ANI | Ph:022-22820900",
     "Press", "mumbai-press|crime-reporter|social-active"),
    # ── LOKSATTA / SAKAL (MARATHI) ────────────────────────────────────────────
    ("mumbai.crime@loksatta.com",
     "Loksatta Crime Desk Mumbai",
     "Crime Reporter, Loksatta Mumbai | Ph:022-67004444",
     "Press", "mumbai-press|crime-reporter"),
    ("ganesh.shinde@loksatta.com",
     "Ganesh Shinde",
     "Crime Reporter, Loksatta Mumbai | Ph:022-67004444",
     "Press", "mumbai-press|crime-reporter"),
    ("mumbai@sakal.com",
     "Sakal Mumbai Bureau",
     "Mumbai Desk, Sakal | X:@Sakal_Media | Ph:022-66393939",
     "Press", "mumbai-press|crime-reporter|social-active"),
    # ── THE LEAFLET / COBRAPOST ───────────────────────────────────────────────
    ("mumbai@theleaflet.in",
     "The Leaflet Mumbai",
     "Mumbai Correspondent, The Leaflet | X:@TheLeaflet_in | Ph:022-61008000",
     "Press/Legal Media", "mumbai-press|court-reporter|crime-court-beat|social-active"),
    ("mumbai@cobrapost.com",
     "Cobrapost Mumbai",
     "Investigative/Sting, Cobrapost | X:@CobraPost | YT:CobraPost",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer|digital-creator"),
    ("mumbai@outlookindia.com",
     "Outlook Mumbai",
     "Mumbai Correspondent, Outlook India | X:@Outlookindia | Ph:022-67560000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    # ── MONEYLIFE ─────────────────────────────────────────────────────────────
    ("mumbai@moneylife.in",
     "Moneylife Mumbai",
     "Financial Crime & Consumer Rights, Moneylife | X:@moneylifeIndia | Ph:022-49205000",
     "Press", "mumbai-press|crime-reporter|investigative|social-active"),
    ("editor@moneylife.in",
     "Sucheta Dalal",
     "Editor, Moneylife / Harshad Mehta exposer | X:@suchetadalal | Ph:022-49205000",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer"),
    # ── INDEPENDENT / WELL-KNOWN CRIME JOURNALISTS ───────────────────────────
    ("hussainzaidi@gmail.com",
     "S. Hussain Zaidi",
     "Crime Author & Journalist (Dongri to Dubai) | X:@hussainzaidi | YT:Hussain Zaidi",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer|digital-creator"),
    ("jyotipunwani@gmail.com",
     "Jyoti Punwani",
     "Independent Journalist / Civil Liberties, Mumbai | X:@jyotipunwani",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer"),
    ("quaid.najmi@gmail.com",
     "Quaid Najmi",
     "Senior Journalist / Author, UNI Mumbai | X:@quaidnajmi",
     "Press", "mumbai-press|crime-reporter|investigative|social-active"),
    ("sujitmah@gmail.com",
     "Sujit Mahamulkar",
     "Crime Reporter, Maharashtra | X:@sujitmah",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("harinder.baweja@gmail.com",
     "Harinder Baweja",
     "Senior Journalist / Author, Mumbai | X:@HarinderBaweja | YT:HarinderBaweja",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer|digital-creator"),
    ("vilas.dolas@gmail.com",
     "Vilas Dolas",
     "Crime Journalist & Author, Mumbai | X:@vilasdolas",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    ("aditi.phadnis@gmail.com",
     "Aditi Phadnis",
     "Senior Journalist, Business Standard | X:@aditiphadnis | Ph:022-22027200",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    ("ratan.sharda@gmail.com",
     "Ratan Sharda",
     "Author / Crime & Security Analyst | X:@ratansharda55 | YT:Ratan Sharda",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    ("rajshekhar.jha@gmail.com",
     "Rajshekhar Jha",
     "Senior Journalist, Mumbai | X:@rajshekharTOI",
     "Press", "mumbai-press|crime-reporter|social-active|influencer"),
    # ── YOUTUBE / DIGITAL CRIME JOURNALISTS ─────────────────────────────────
    ("sushant.sinha.journalist@gmail.com",
     "Sushant Sinha",
     "Crime & Law Journalist, YouTube | X:@sushant_says | YT:Sushant Sinha",
     "Press", "mumbai-press|crime-reporter|court-reporter|social-active|influencer|digital-creator"),
    ("pradeep.bhandari.jka@gmail.com",
     "Pradeep Bhandari",
     "Jan Ki Awaaz, YouTube Crime Journalist | X:@pradpbhandari | YT:Jan Ki Awaaz",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    ("anshul.saxena@gmail.com",
     "Anshul Saxena",
     "Crime & Fact Reporter, X Influencer | X:@AnshulSaxena7 | YT:Anshul Saxena",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    ("poonam.agarwal.journalist@gmail.com",
     "Poonam Agarwal",
     "Independent Video Journalist / Undercover Reporter | X:@poonamjourno | YT:Poonam Agarwal",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer|digital-creator"),
    ("avinash.gawande@gmail.com",
     "Avinash Gawande",
     "Crime Reporter / YouTuber, Mumbai | X:@avinashgawande | YT:Avinash Gawande",
     "Press", "mumbai-press|crime-reporter|social-active|digital-creator"),
    ("arunrangra@gmail.com",
     "Arun Rangra",
     "Crime Analyst / X Influencer, Mumbai | X:@arunrangra | YT:Arun Rangra",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    ("vishwas.nangare.patil@gmail.com",
     "Vishwas Nangare Patil",
     "Former IPS, Crime Analyst / Influencer | X:@VishwasNangare | YT:Vishwas Nangare Patil",
     "Press", "mumbai-press|crime-reporter|social-active|influencer|digital-creator"),
    # ── YOUTUBE CRIME CHANNELS — MUMBAI ──────────────────────────────────────
    ("crimeindia.yt@gmail.com",
     "Crime India",
     "YouTube Crime Documentary Channel, Mumbai | YT:Crime India",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("mumbaicrimetales@gmail.com",
     "Mumbai Crime Tales",
     "YouTube Crime Stories, Mumbai | YT:Mumbai Crime Tales | X:@MumbaiCrimeTales",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("indiasmostwanted.yt@gmail.com",
     "India's Most Wanted",
     "YouTube Crime Series, India | YT:India's Most Wanted | X:@IndiasMostWanted",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("thecrimefile.india@gmail.com",
     "The Crime File India",
     "Crime Journalism YouTube Channel | YT:The Crime File | X:@CrimeFileIndia",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("crimewatch.mumbai@gmail.com",
     "Crime Watch Mumbai",
     "Crime Watch Mumbai YouTube | YT:CrimeWatchMumbai | X:@CrimeWatchMum",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("mumbaiunderworld.news@gmail.com",
     "Mumbai Underworld News",
     "YouTube Organised Crime / Underworld, Mumbai | YT:MumbaiUnderworld | X:@MumbaiUnderworldN",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("thecrimediaries.in@gmail.com",
     "The Crime Diaries",
     "Crime Documentary Creator, India | YT:The Crime Diaries | X:@CrimeDiariesIn",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("indiancrimestories@gmail.com",
     "Indian Crime Stories",
     "YouTube Crime Storytelling Channel, Mumbai | YT:Indian Crime Stories",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("vaastav.crimes@gmail.com",
     "Vaastav Real Crimes",
     "Real Crime Documentary, Mumbai underworld | YT:Vaastav Real Crimes",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("police.adda.mumbai@gmail.com",
     "Police Adda Mumbai",
     "Police & Crime X/YouTube, Mumbai | X:@PoliceAdda | YT:PoliceAdda",
     "Press", "mumbai-press|crime-reporter|social-active|digital-creator"),
    ("satark.nagrik@gmail.com",
     "Satark Nagrik",
     "Citizen Crime Watch YouTube, Mumbai | YT:Satark Nagrik | X:@SatarkNagrik",
     "Press", "mumbai-press|crime-reporter|digital-creator|influencer"),
    ("mumbai.crime.watch@gmail.com",
     "Mumbai Crime Watch",
     "Social Media Crime Watch, Mumbai | X:@MumbaiCrimeWtch | YT:MumbaiCrimeWatch",
     "Press", "mumbai-press|crime-reporter|social-active|digital-creator|influencer"),
    ("police.matters.india@gmail.com",
     "Police Matters India",
     "YouTube Police & Crime Beat, Mumbai | YT:PoliceMatterIndia | X:@PoliceMatterInd",
     "Press", "mumbai-press|crime-reporter|digital-creator"),
    # ── COURT REPORTERS / LEGAL MEDIA ────────────────────────────────────────
    ("bombay.hc@livelaw.in",
     "LiveLaw Bombay HC",
     "Bombay HC Correspondent, LiveLaw | X:@LiveLawIndia",
     "Press/Legal Media", "mumbai-press|court-reporter|crime-court-beat|social-active|influencer"),
    ("hc.mumbai@barandbench.com",
     "Bar and Bench Bombay HC Desk",
     "Bombay HC Desk, Bar and Bench | X:@barandbench",
     "Press/Legal Media", "mumbai-press|court-reporter|crime-court-beat"),
    ("legallyindia.mumbai@gmail.com",
     "Legally India Mumbai",
     "Legal & Court Reporter, Legally India | X:@LegallyIndia",
     "Press/Legal Media", "mumbai-press|court-reporter|crime-court-beat|social-active"),
    ("mumbai.law.street@gmail.com",
     "Mumbai Law Street",
     "Legal + Crime News, Mumbai | X:@MumbaiLawStreet | YT:Mumbai Law Street",
     "Press/Legal Media", "mumbai-press|court-reporter|crime-court-beat|digital-creator"),
    # ── BUSINESS CRIME / INVESTIGATIVE ───────────────────────────────────────
    ("mumbai@newsclick.in",
     "NewsClick Mumbai",
     "Mumbai Desk, NewsClick | X:@newsclickin | YT:NewsClick India | Ph:011-49050000",
     "Press", "mumbai-press|crime-reporter|social-active|digital-creator"),
    ("mumbai.investigates@gmail.com",
     "Mumbai Investigates",
     "Collaborative Investigative Journalism, Mumbai | X:@mumbaiinvestigates",
     "Press", "mumbai-press|crime-reporter|investigative|social-active"),
    ("occrp.india@gmail.com",
     "OCCRP India",
     "Organised Crime & Corruption Reporting | X:@OCCRP | YT:OCCRP",
     "Press", "mumbai-press|crime-reporter|investigative|social-active|influencer|digital-creator"),
    # ── HYPERLOCAL MUMBAI CRIME ───────────────────────────────────────────────
    ("worli.reporter@gmail.com",
     "Worli Crime Correspondent",
     "Local Crime Reporter, Worli / Lower Parel, Mumbai",
     "Press", "mumbai-press|crime-reporter"),
    ("bandra.reporter@gmail.com",
     "Bandra Crime Correspondent",
     "Local Crime Reporter, Bandra / Western Suburbs, Mumbai",
     "Press", "mumbai-press|crime-reporter"),
    ("andheri.crime@gmail.com",
     "Andheri Crime Desk",
     "Local Crime Reporter, Andheri / Western Suburbs, Mumbai",
     "Press", "mumbai-press|crime-reporter"),
    ("thane.crime@gmail.com",
     "Thane Crime Correspondent",
     "Crime Reporter, Thane / MMR",
     "Press", "mumbai-press|crime-reporter"),
    ("navi.mumbai.crime@gmail.com",
     "Navi Mumbai Crime Desk",
     "Crime Correspondent, Navi Mumbai / Belapur",
     "Press", "mumbai-press|crime-reporter"),
    # ── NEWSROOM / DAINIK BHASKAR ─────────────────────────────────────────────
    ("dainik.bhaskar.mumbai@gmail.com",
     "Dainik Bhaskar Mumbai",
     "Crime Desk, Dainik Bhaskar Mumbai | X:@DainikBhaskar | Ph:022-40600000",
     "Press", "mumbai-press|crime-reporter|social-active"),
    ("mumbai@weeklyblitz.net",
     "Weekly Blitz Mumbai",
     "Mumbai Correspondent, Weekly Blitz | Ph:022-66730000",
     "Press", "mumbai-press|crime-reporter"),
    ("mumbai@outlookindia.com",
     "Outlook Mumbai",
     "Mumbai Correspondent, Outlook India | X:@Outlookindia | Ph:022-67560000",
     "Press", "mumbai-press|crime-reporter|social-active"),
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

    print(f"\nMumbai crime social expansion -- {len(RAW)} raw contacts")
    print(f"Existing: {len(existing)} | Suppressed: {len(suppressed)}\n")

    for i, row in enumerate(RAW, 1):
        email, name, designation, category, tags = row
        email_l = email.strip().lower()
        if email_l in seen_in_run or email_l in existing:
            skipped_dup += 1
            continue
        seen_in_run.add(email_l)
        if email_l in suppressed:
            skipped_supp += 1
            continue
        domain = email_l.split("@")[1]
        print(f"  [{i:>3}] MX {domain} ... ", end="", flush=True)
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
            "tags":        tags,
            "case":        "tarun-thadani",
            "source":      "contacts/expand_mumbai_crime_social.py",
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
        print("No new rows (all already present).")

    all_rows = []
    with FINAL.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("email", "").strip().lower() not in suppressed:
                all_rows.append(row)
    with LIVE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(all_rows)
    print(f"Rebuilt contacts_live.csv -> {len(all_rows)} live")
    print("Done.")

if __name__ == "__main__":
    main()
