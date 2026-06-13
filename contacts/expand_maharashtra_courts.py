#!/usr/bin/env python3
"""
expand_maharashtra_courts.py
Maharashtra district & sessions courts crime-court network — every email
copied verbatim 2026-06-13 from the official eCourts district sites
(<district>.dcourts.gov.in/contact-us/). Domains are all official judiciary:
  @mhstate.nic.in  @nic.in  @aij.gov.in  @bhc.gov.in
  @indianjudiciary.gov.in  @indiancourts.nic.in  @gov.in
plus a few official gmail/rediffmail desks (family/legal-aid/labour courts).

Sessions courts try criminal cases — core crime-court-beat contacts.
No guessed addresses; districts whose taluka tables were JS-paginated were
captured at main-court level only (Akola, Dhule, Sangli, Latur, Beed,
Chandrapur, Amravati, Ahmednagar, Raigad, Ratnagiri, Sindhudurg, Jalna,
Parbhani, Nandurbar, Gadchiroli). Not fetched (site refused): Hingoli,
Dharashiv/Osmanabad, Palghar, Buldhana — add later, don't guess.
"""

import csv, socket, subprocess
from pathlib import Path

ROOT      = Path(__file__).parent.parent
FINAL_CSV = ROOT / "contacts" / "contacts_final.csv"
LIVE_CSV  = ROOT / "contacts" / "contacts_live.csv"
SUPP_CSV  = ROOT / "contacts" / "suppression_list.csv"
HEADER    = ["email","name","designation","category","tags","case","source","mobile"]
SRC       = "official:ecourts.gov.in"

TRUSTED = {"mhstate.nic.in","nic.in","aij.gov.in","bhc.gov.in",
           "indianjudiciary.gov.in","indiancourts.nic.in","gov.in",
           "gmail.com","rediffmail.com"}

def email_ok(email):
    d = email.split("@")[1].lower()
    if any(d == t or d.endswith("."+t) for t in TRUSTED): return True
    try:
        out = subprocess.run(["nslookup","-type=MX",d], capture_output=True, text=True, timeout=6)
        if "mail exchanger" in out.stdout.lower(): return True
    except Exception: pass
    try:
        socket.setdefaulttimeout(4); socket.gethostbyname(d); return True
    except Exception: return False

# (email, court name, district, is_main_sessions, phone)
COURTS = [
    # ── Main District & Sessions Courts (try criminal/sessions cases) ──
    ("mahpundc@mhstate.nic.in","District & Sessions Court, Pune","pune",True,"020-25534799"),
    ("mahnagdc@mhstate.nic.in","District & Sessions Court, Nagpur","nagpur",True,"0712-2531989"),
    ("mahthadc@mhstate.nic.in","District & Sessions Court, Thane","thane",True,"022-25474574"),
    ("mahnasdc@mhstate.nic.in","District & Sessions Court, Nashik","nashik",True,""),
    ("mahaurdc@mhstate.nic.in","District & Sessions Court, Chh. Sambhajinagar (Aurangabad)","aurangabad",True,""),
    ("mahkoldc@mhstate.nic.in","District & Sessions Court, Kolhapur","kolhapur",True,""),
    ("mahshodc@mhstate.nic.in","District & Sessions Court, Solapur","solapur",True,""),
    ("mahamrdc@mhstate.nic.in","District & Sessions Court, Amravati","amravati",True,""),
    ("mahahmdc@nic.in","District & Sessions Court, Ahmednagar","ahmednagar",True,""),
    ("mahjagdc@nic.in","District & Sessions Court, Jalgaon","jalgaon",True,""),
    ("mahnandc@mhstate.nic.in","District & Sessions Court, Nanded","nanded",True,""),
    ("mahsandc@mhstate.nic.in","District & Sessions Court, Sangli","sangli",True,""),
    ("mahsatdc@mhstate.nic.in","District & Sessions Court, Satara","satara",True,""),
    ("mahlatdc@mhstate.nic.in","District & Sessions Court, Latur","latur",True,""),
    ("mahbeedc@mhstate.nic.in","District & Sessions Court, Beed","beed",True,""),
    ("mahchadc@mhstate.nic.in","District & Sessions Court, Chandrapur","chandrapur",True,""),
    ("mahakodc@mhstate.nic.in","District & Sessions Court, Akola","akola",True,""),
    ("mahdhudc@mhstate.nic.in","District & Sessions Court, Dhule","dhule",True,""),
    ("mahyavdc@mhstate.nic.in","District & Sessions Court, Yavatmal","yavatmal",True,""),
    ("mahwardc@mhstate.nic.in","District & Sessions Court, Wardha","wardha",True,""),
    ("mahgondc@mhstate.nic.in","District & Sessions Court, Gondia","gondia",True,""),
    ("mahbhadc@mhstate.nic.in","District & Sessions Court, Bhandara","bhandara",True,""),
    ("mahraidc@mhstate.nic.in","District & Sessions Court, Raigad-Alibag","raigad",True,""),
    ("mahratdc@mhstate.nic.in","District & Sessions Court, Ratnagiri","ratnagiri",True,""),
    ("mahsindc@nic.in","District & Sessions Court, Sindhudurg","sindhudurg",True,""),
    ("mahjaldc@mhstate.nic.in","District & Sessions Court, Jalna","jalna",True,""),
    ("mahpardc@mhstate.nic.in","District & Sessions Court, Parbhani","parbhani",True,""),
    ("mahdhunansc@indianjudiciary.gov.in","District & Sessions Court, Nandurbar","nandurbar",True,""),
    ("mahgaddc@mhstate.nic.in","District & Sessions Court, Gadchiroli","gadchiroli",True,""),
    ("dj.gondia-mah@aij.gov.in","District Judge, Gondia","gondia",True,""),
    ("mahakowassc@aij.gov.in","District & Sessions Court, Washim","washim",True,""),

    # ── Thane taluka court complexes ──
    ("mahthnnavmumsc@aij.gov.in","Belapur Taluka Court (Navi Mumbai)","thane",False,""),
    ("mahthnbhisc@aij.gov.in","Bhiwandi Taluka Court","thane",False,""),
    ("mahthnkalsc@aij.gov.in","Kalyan Taluka Court","thane",False,""),
    ("mahthnpalsc@aij.gov.in","Palghar Taluka Court","thane",False,""),
    ("mahthnvassc@aij.gov.in","Vasai Taluka Court","thane",False,""),
    ("mahthndahsc@aij.gov.in","Dahanu Taluka Court","thane",False,""),
    ("mahthjaw@aij.gov.in","Jawhar Taluka Court","thane",False,""),
    ("mahthnmurbad@aij.gov.in","Murbad Taluka Court","thane",False,""),
    ("mahthnshasc@aij.gov.in","Shahapur Taluka Court","thane",False,""),
    ("mahthnulhsc@aij.gov.in","Ulhasnagar Taluka Court","thane",False,""),
    ("mahthnwadsc@aij.gov.in","Wada Taluka Court","thane",False,""),
    ("mahthnmira@aij.gov.in","Mira Bhayandar Taluka Court","thane",False,""),
    ("mahthnkalrc@aij.gov.in","Kalyan Railway Taluka Court","thane",False,""),
    ("mahthnvirsc@aij.gov.in","Virar Railway Taluka Court","thane",False,""),
    ("mahthnamb@aij.gov.in","Chikhloli Ambarnath Taluka Court","thane",False,""),

    # ── Nashik district courts ──
    ("mah-nascjm@bhc.gov.in","Chief Judicial Magistrate, Nashik","nashik",False,""),
    ("mah-nassd@bhc.gov.in","Civil Court Senior Division, Nashik","nashik",False,""),
    ("dlsa-nashik@bhc.gov.in","District Legal Services Authority, Nashik","nashik",False,""),
    ("mahnasmalrdsc@aij.gov.in","District Court-1, Malegaon","nashik",False,""),
    ("mah-nasmalsd@bhc.gov.in","Civil Court Sr Div, Malegaon","nashik",False,""),
    ("jdmalegaon@bhc.gov.in","Civil Court Jr Div, Malegaon","nashik",False,""),
    ("mahnasniprdsc@aij.gov.in","District Court-1, Niphad","nashik",False,""),
    ("srdivniphad@bhc.gov.in","Civil Court Sr Div, Niphad","nashik",False,""),
    ("mah-nasnipjd@bhc.gov.in","Civil Court Jr Div, Niphad","nashik",False,""),
    ("mah-naspim@bhc.gov.in","Civil Court Jr Div, Pimpalgaon","nashik",False,""),
    ("mah-nasdin@bhc.gov.in","Civil Court Jr Div, Dindori","nashik",False,""),
    ("addldjyeola@bhc.gov.in","District Court-1, Yeola","nashik",False,""),
    ("mahnasyeordsc@aij.gov.in","Civil Court Jr Div, Yeola","nashik",False,""),
    ("mahnaschardsc@aij.gov.in","Civil Court Jr Div, Chandwad","nashik",False,""),
    ("mahnasnanrdsc@aij.gov.in","Civil Court Jr Div, Nandgaon","nashik",False,""),
    ("srdivsinnar@bhc.gov.in","Civil Court Sr Div, Sinnar","nashik",False,""),
    ("mahnassinrdsc@aij.gov.in","Civil Court Jr Div, Sinnar","nashik",False,""),
    ("srdivigatpuri@bhc.gov.in","Civil Court Sr Div, Igatpuri","nashik",False,""),
    ("mahnasigardsc@aij.gov.in","Civil Court Jr Div, Igatpuri","nashik",False,""),
    ("mahnaskalrdsc@aij.gov.in","Civil Court Jr Div, Kalwan","nashik",False,""),
    ("mahnassatrdsc@aij.gov.in","Civil Court Jr Div, Satana","nashik",False,""),
    ("mahnasmanrdsc@aij.gov.in","Civil Court Jr Div, Manmad City","nashik",False,""),
    ("mah-nasmanrly@bhc.gov.in","JMFC, Manmad Railway","nashik",False,""),
    ("mahnasnasrdsc@aij.gov.in","Civil Court Jr Div, Nashik Road","nashik",False,""),
    ("mah-nasmv@bhc.gov.in","JMFC Motor Vehicle Court, Nashik","nashik",False,""),

    # ── Aurangabad / Satara / Dhule MACT ──
    ("mact-aurangabad@indiancourts.nic.in","MACT, Aurangabad","aurangabad",False,""),
    ("mact-aur.vaijapur@indiancourts.nic.in","MACT, Vaijapur","aurangabad",False,""),
    ("mact-satara@indiancourts.nic.in","MACT, Satara","satara",False,""),
    ("mact-satara.karad@indiancourts.nic.in","MACT, Karad","satara",False,""),
    ("mact-satara.vaduj@indiancourts.nic.in","MACT, Vaduj","satara",False,""),
    ("mact-dhule@indiancourts.nic.in","MACT, Dhule","dhule",False,""),

    # ── Solapur district courts ──
    ("mah-solcjsd@bhc.gov.in","Civil Court Sr Div, Solapur","solapur",False,""),
    ("mah-solcjm@bhc.gov.in","Chief Judicial Magistrate, Solapur","solapur",False,""),
    ("mahsolpansc@aij.gov.in","Addl District & Sessions Court, Pandharpur","solapur",False,""),
    ("mah-solpancjsd@bhc.gov.in","Civil Court Sr Div, Pandharpur","solapur",False,""),
    ("mah-solpancjjd@bhc.gov.in","Civil Court Jr Div, Pandharpur","solapur",False,""),
    ("mah-solpanjmfc@bhc.gov.in","JMFC, Pandharpur","solapur",False,""),
    ("mahsolmalsc@aij.gov.in","Addl District & Sessions Court, Malshiras","solapur",False,""),
    ("mah-solmalcjsd@bhc.gov.in","Civil Court Sr Div, Malshiras","solapur",False,""),
    ("mah-solmalcjjd@bhc.gov.in","Civil Court Jr Div, Malshiras","solapur",False,""),
    ("mah-solbaradj@bhc.gov.in","Addl District & Sessions Court, Barshi","solapur",False,""),
    ("mahsolbarsc@aij.gov.in","Civil Court Sr Div, Barshi","solapur",False,""),
    ("mah-solbarcjjd@bhc.gov.in","Civil Court Jr Div, Barshi","solapur",False,""),
    ("mah-solbarjmfc@bhc.gov.in","JMFC, Barshi","solapur",False,""),
    ("mahsolakksc@aij.gov.in","Civil & Criminal Court, Akkalkot","solapur",False,""),
    ("mahsolmohsc@aij.gov.in","Civil & Criminal Court, Mohol","solapur",False,""),
    ("cjsd-madha@bhc.gov.in","Civil Court Sr Div, Madha","solapur",False,""),
    ("mahsolmadsc@aij.gov.in","Civil & Criminal Court, Madha","solapur",False,""),
    ("cjsd-karmala@bhc.gov.in","Civil Court Sr Div, Karmala","solapur",False,""),
    ("mahsolkarsc@aij.gov.in","Civil & Criminal Court, Karmala","solapur",False,""),
    ("mahsolsansc@aij.gov.in","Civil & Criminal Court, Sangola","solapur",False,""),
    ("mahsolmansc@aij.gov.in","Civil & Criminal Court, Mangalwedha","solapur",False,""),

    # ── Jalgaon district courts ──
    ("mahjalamasc@aij.gov.in","Court, Amalner","jalgaon",False,""),
    ("mahjalbhasc@aij.gov.in","Court, Bhadgaon","jalgaon",False,""),
    ("mahjalbhusc@aij.gov.in","Court, Bhusawal","jalgaon",False,""),
    ("mahjalbodjd@bhc.gov.in","Court, Bodwad","jalgaon",False,""),
    ("mahjalchasc@indianjudiciary.gov.in","Court, Chalisgaon","jalgaon",False,""),
    ("mahjalchosc@aij.gov.in","Court, Chopda","jalgaon",False,""),
    ("mahjaldhasc@indianjudiciary.gov.in","Court, Dharangaon","jalgaon",False,""),
    ("mahjalerasc@aij.gov.in","Court, Erandol","jalgaon",False,""),
    ("mahjaljamsc@aij.gov.in","Court, Jamner","jalgaon",False,""),
    ("mahjalmuksc@aij.gov.in","Court, Muktainagar","jalgaon",False,""),
    ("mahjalpacsc@aij.gov.in","Court, Pachora","jalgaon",False,""),
    ("mahjalparsc@aij.gov.in","Court, Parola","jalgaon",False,""),
    ("mahjalbhurly@bhc.gov.in","Court, Bhusawal Railway","jalgaon",False,""),
    ("mahjalravsc@aij.gov.in","Court, Raver","jalgaon",False,""),
    ("mahjalyawsc@indianjudiciary.gov.in","Court, Yawal","jalgaon",False,""),

    # ── Nanded district courts ──
    ("nancjsd@bhc.gov.in","Civil Judge Sr Div, Nanded","nanded",False,""),
    ("legalaidnanded@gmail.com","District Legal Service Authority, Nanded","nanded",False,""),
    ("mahnanbilsc@indianjudiciary.gov.in","District Judge-1, Biloli","nanded",False,""),
    ("nanbilcjsd@bhc.gov.in","CJSD, Biloli","nanded",False,""),
    ("nanbilcjjd@bhc.gov.in","Jt CJJD, Biloli","nanded",False,""),
    ("mahnankansc@indianjudiciary.gov.in","District Judge-1, Kandhar","nanded",False,""),
    ("nankancjsd@bhc.gov.in","CJSD, Kandhar","nanded",False,""),
    ("nankancjjd@bhc.gov.in","Jt CJJD, Kandhar","nanded",False,""),
    ("mahnanbhosc@indianjudiciary.gov.in","District Judge-1, Bhokar","nanded",False,""),
    ("nanbhocjsd@bhc.gov.in","CJSD, Bhokar","nanded",False,""),
    ("nanbhocjjd@bhc.gov.in","CJJD, Bhokar","nanded",False,""),
    ("mahnankinsc@aij.gov.in","Court, Kinwat","nanded",False,""),
    ("mahnanhimsc@aij.gov.in","Court, Himayatnagar","nanded",False,""),
    ("mahnanhadsc@indianjudiciary.gov.in","Court, Hadgaon","nanded",False,""),
    ("cjjd-umri@aij.gov.in","Court, Umri","nanded",False,""),
    ("mahnanmuksc@indianjudiciary.gov.in","District Judge-1, Mukhed","nanded",False,""),
    ("nanmkdcjsd@bhc.gov.in","CJSD, Mukhed","nanded",False,""),
    ("nanmkdcjjd@bhc.gov.in","CJJD, Mukhed","nanded",False,""),
    ("mahnandegsc@aij.gov.in","Court, Degloor","nanded",False,""),
    ("mahnannaisc@aij.gov.in","Court, Naigaon","nanded",False,""),
    ("mahnandhasc@aij.gov.in","Court, Dharmabad","nanded",False,""),
    ("nanmahrsc@aij.gov.in","Court, Mahur","nanded",False,""),
    ("nanardsc@aij.gov.in","Court, Ardhapur","nanded",False,""),
    ("nanmudsc@aij.gov.in","Court, Mudkhed","nanded",False,""),
    ("familycourtnanded@gmail.com","Family Court, Nanded","nanded",False,""),

    # ── Yavatmal district courts ──
    ("mahyatdarsc@indianjudiciary.gov.in","Addl Sessions Court, Darwha","yavatmal",False,""),
    ("mahyatpussc@indianjudiciary.gov.in","Addl Sessions Court, Pusad","yavatmal",False,""),
    ("mahyatpansc@aij.gov.in","Addl Sessions Court, Kelapur","yavatmal",False,""),
    ("ytlzariascjjd@bhc.gov.in","Civil & Criminal Court, Zari-Jamni","yavatmal",False,""),
    ("mahyatarnsc@indianjudiciary.gov.in","Civil & Criminal Court, Arni","yavatmal",False,""),
    ("mahyatbabsc@indianjudiciary.gov.in","Civil & Criminal Court, Babhulgaon","yavatmal",False,""),
    ("mahyatdigsc@indianjudiciary.gov.in","Civil & Criminal Court, Digras","yavatmal",False,""),
    ("mahyatghasc@indianjudiciary.gov.in","Civil & Criminal Court, Ghatanji","yavatmal",False,""),
    ("mahyatkalsc@indianjudiciary.gov.in","Civil Court, Kalamb","yavatmal",False,""),
    ("mahyatmahsc@indianjudiciary.gov.in","Civil & Criminal Court, Mahagaon","yavatmal",False,""),
    ("mahyatmarsc@indianjudiciary.gov.in","Civil Court, Maregaon","yavatmal",False,""),
    ("mahyatnersc@indianjudiciary.gov.in","Civil & Criminal Court, Ner","yavatmal",False,""),
    ("ytlralascjjd@bhc.gov.in","Civil & Criminal Court, Ralegaon","yavatmal",False,""),
    ("mahyatumasc@indianjudiciary.gov.in","Civil Court, Umarkhed","yavatmal",False,""),
    ("mahyatwansc@indianjudiciary.gov.in","Civil & Criminal Court, Wani","yavatmal",False,""),
    ("fcyavatmal@bhc.gov.in","Family Court, Yavatmal","yavatmal",False,""),

    # ── Wardha district courts ──
    ("mact-wardha@indiancourts.nic.in","MACT, Wardha","wardha",False,""),
    ("mahwarhinsc@indianjudiciary.gov.in","Taluka Court, Hinganghat","wardha",False,""),
    ("mahwarpulsc@indianjudiciary.gov.in","Taluka Court, Pulgaon","wardha",False,""),
    ("mahwararvsc@indianjudiciary.gov.in","Taluka Court, Arvi","wardha",False,""),
    ("mahwarkarsc@indianjudiciary.gov.in","Taluka Court, Karanja (Gh)","wardha",False,""),
    ("mahwarashsc@indianjudiciary.gov.in","Taluka Court, Ashti","wardha",False,""),
    ("mahwarselsc@indianjudiciary.gov.in","Taluka Court, Seloo","wardha",False,""),
    ("mahwarsamsc@indianjudiciary.gov.in","Taluka Court, Samudrapur","wardha",False,""),
    ("mahwarlc@indianjudiciary.gov.in","Labour Court, Wardha","wardha",False,""),

    # ── Gondia district courts ──
    ("gonamgaonsc-mh@indiancourts.nic.in","Civil Court, Amgaon","gondia",False,""),
    ("gonarjunisc-mh@indiancourts.nic.in","Civil Court, Arjuni Morgaon","gondia",False,""),
    ("gondeorisc-mh@indiancourts.nic.in","Civil Court, Deori","gondia",False,""),
    ("gonsadaksc-mh@indiancourts.nic.in","Civil Court, Sadak Arjuni","gondia",False,""),

    # ── Bhandara district courts ──
    ("bhandara-dlsa.mh@bhc.gov.in","District Legal Service Authority, Bhandara","bhandara",False,""),
    ("cjjdmohadi@bhc.gov.in","CJJD, Mohadi","bhandara",False,""),
    ("cjjdpauni@bhc.gov.in","CJJD, Pauni","bhandara",False,""),
    ("cjjdlakhani@bhc.gov.in","CJJD, Lakhani","bhandara",False,""),
    ("cjjdlakhandur@bhc.gov.in","CJJD, Lakhandur","bhandara",False,""),

    # ── Washim district courts ──
    ("mact-washim@indiancourts.nic.in","MACT, Washim","washim",False,""),
    ("mactwas.mangrulpir@indiancourts.nic.in","ADJ Court, Mangrulpir","washim",False,""),
    ("mahakomansc@aij.gov.in","Civil Court Sr Div, Mangrulpir","washim",False,""),
    ("mahakokarsc@aij.gov.in","Civil Court Jr Div, Karanja","washim",False,""),
    ("mahakorissc@aij.gov.in","Civil Court Jr Div, Risod","washim",False,""),
    ("mahakomalsc@indianjudiciary.gov.in","Civil Court Jr Div, Malegaon (Washim)","washim",False,""),
]

CITY_TAGS = {"mumbai","pune","thane","nagpur","nashik","aurangabad","solapur",
             "kolhapur","amravati"}

RAW = []
for email, name, dist, is_main, phone in COURTS:
    tags = ["court","judiciary","crime-court-beat","govt-state","maharashtra", dist]
    if is_main:
        tags += ["sessions-court","district-court","top-priority"]
    else:
        tags += ["taluka-court"]
    if dist in CITY_TAGS:
        tags.append(dist)
    RAW.append((email, name, name, "Court/Judiciary",
                "|".join(dict.fromkeys(tags)), "general", SRC, phone))

def load_set(path):
    s = set()
    if path.exists():
        for r in csv.DictReader(path.open(encoding="utf-8-sig")):
            e = (r.get("email","") or "").strip().lower()
            if e: s.add(e)
    return s

def main():
    existing = load_set(FINAL_CSV); suppressed = load_set(SUPP_CSV)
    print(f"Existing {len(existing)} | Suppressed {len(suppressed)} | Candidates {len(RAW)}\n")
    seen_now = set(existing)
    added, dup, mx, supp, selfdup = [], 0, 0, 0, 0
    for row in RAW:
        e = row[0].strip().lower()
        if e in suppressed: supp += 1; continue
        if e in seen_now:   dup += 1; continue
        if not email_ok(e): print(f"  BAD-MX  {e}"); mx += 1; continue
        seen_now.add(e); added.append(row)
    print(f"Added {len(added)} | Dups {dup} | Bad-MX {mx} | Suppressed {supp}")
    if not added: print("Nothing to add."); return

    with FINAL_CSV.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for row in added:
            r = list(row)+[""]*(8-len(row)); w.writerow(r[:8])

    sup_now = load_set(SUPP_CSV)
    allrows = list(csv.DictReader(FINAL_CSV.open(encoding="utf-8-sig")))
    fn = list(allrows[0].keys())
    live = [r for r in allrows if (r.get("email","") or "").strip().lower() not in sup_now]
    with LIVE_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fn, extrasaction="ignore"); w.writeheader(); w.writerows(live)
    print(f"\ncontacts_final.csv: {len(allrows)} | contacts_live.csv: {len(live)}")

if __name__ == "__main__":
    main()
