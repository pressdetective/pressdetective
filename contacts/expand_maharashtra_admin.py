#!/usr/bin/env python3
"""
expand_maharashtra_admin.py
36 Maharashtra District Collectors / District Magistrates — official office
emails + office phone numbers, copied verbatim 2026-06-13 from the Election
Commission directory ceoelection.maharashtra.gov.in/Downloads/AC2019/ContactCollector.pdf

The Collector is the District Magistrate (law & order, externment, preventive
detention, NSA) — part of the district crime/governance network. Names in the
PDF are 2019 incumbents; role/office emails persist, so contacts use the OFFICE
designation, not the (stale) individual name.

Sangli's listed address (collectorsangli@nic.com) is an obvious PDF typo for
nic.in — SKIPPED rather than guessed, to protect deliverability.
"""

import csv, socket, subprocess
from pathlib import Path

ROOT      = Path(__file__).parent.parent
FINAL_CSV = ROOT / "contacts" / "contacts_final.csv"
LIVE_CSV  = ROOT / "contacts" / "contacts_live.csv"
SUPP_CSV  = ROOT / "contacts" / "suppression_list.csv"
HEADER    = ["email","name","designation","category","tags","case","source","mobile"]
SRC       = "official_pdf:ceoelection_collectors"

TRUSTED = {"maharashtra.gov.in","nic.in","gov.in","gmail.com","rediffmail.com"}

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

# (district, email, phone with STD)
COLLECTORS = [
    ("Mumbai City",      "mahbom@nic.in",                              "022-22662440"),
    ("Mumbai Suburban",  "collectormsd@gmail.com",                     "022-26514742"),
    ("Palghar",          "collectorpalghar@gmail.com",                 "02525-253111"),
    ("Raigad",           "collector_raigad@maharashtra.gov.in",        "02141-222001"),
    ("Ratnagiri",        "mahrat@nic.in",                              "02352-222301"),
    ("Sindhudurg",       "collector_sindhudurg@maharashtra.gov.in",    "02362-228844"),
    ("Thane",            "collector_thane@maharashtra.gov.in",         "022-25344041"),
    ("Kolhapur",         "mahkolcol@nic.in",                           "0231-2654811"),
    ("Pune",             "mahpun@nic.in",                              "020-26114949"),
    ("Satara",           "mahsat@nic.in",                              "02162-232750"),
    ("Solapur",          "mahsho@nic.in",                              "0217-2731000"),
    ("Ahmednagar",       "mahahm@nic.in",                              "0241-2345001"),
    ("Dhule",            "mahdhu@nic.in",                              "02562-288701"),
    ("Jalgaon",          "ddcjalgaon@rediffmail.com",                  "0257-2220400"),
    ("Nandurbar",        "collectornandurbar@gmail.com",               "02564-221001"),
    ("Nashik",           "collector_nashik@maharashtra.gov.in",        "0253-2578500"),
    ("Chh. Sambhajinagar (Aurangabad)","abdcoll@gmail.com",            "0240-2331200"),
    ("Beed",             "mahbee@nic.in",                              "02442-222201"),
    ("Hingoli",          "hincollector@gmail.com",                     "02456-221701"),
    ("Jalna",            "collector_jalna@maharashtra.gov.in",         "02482-224700"),
    ("Latur",            "mahlat@nic.in",                              "02382-224001"),
    ("Nanded",           "collectornanded1@gmail.com",                 "02462-237101"),
    ("Dharashiv (Osmanabad)","collectorosmanabad@gmail.com",           "02472-224501"),
    ("Parbhani",         "pbncollector@rediffmail.com",                "02452-223555"),
    ("Akola",            "mahako@nic.in",                              "0724-2424442"),
    ("Amravati",         "collector_amravati@maharashtra.gov.in",      "0721-2662522"),
    ("Buldhana",         "collectorbul@gmail.com",                     "07262-242307"),
    ("Washim",           "coll_washim@rediffmail.com",                 "07252-233400"),
    ("Yavatmal",         "coll_yavatmal@rediffmail.com",               "07232-242501"),
    ("Bhandara",         "collectorbhandara@gmail.com",                "07184-254777"),
    ("Chandrapur",       "collector_chandrapur@maharashtra.gov.in",    "07172-255300"),
    ("Gadchiroli",       "mahgad@nic.in",                              "07132-222001"),
    ("Gondia",           "collector_gondia@maharashtra.gov.in",        "07182-236149"),
    ("Nagpur",           "collector_nagpur@maharashtra.gov.in",        "0712-2564973"),
    ("Wardha",           "mahwar@nic.in",                              "07152-240102"),
    # Sangli intentionally skipped (collectorsangli@nic.com = PDF typo)
]

CITY = {"mumbai city","thane","pune","nagpur","nashik","chh. sambhajinagar (aurangabad)","solapur","amravati","kolhapur"}

RAW = []
for dist, email, phone in COLLECTORS:
    region = dist.lower().split(" (")[0].replace("chh. sambhajinagar","aurangabad").replace("dharashiv","osmanabad").replace("mumbai city","mumbai").strip()
    tags = ["collector","district-magistrate","law-and-order","govt-state","maharashtra", region.replace(" ","-")]
    RAW.append((email, f"Collector & District Magistrate, {dist}",
                f"Collector / DM, {dist}", "Government",
                "|".join(dict.fromkeys(tags)), "general", SRC, phone))

def load_set(path):
    s = set()
    if path.exists():
        for r in csv.DictReader(path.open(encoding="utf-8-sig")):
            e=(r.get("email","") or "").strip().lower()
            if e: s.add(e)
    return s

def main():
    existing = load_set(FINAL_CSV); suppressed = load_set(SUPP_CSV)
    print(f"Existing {len(existing)} | Suppressed {len(suppressed)} | Candidates {len(RAW)}\n")
    seen = set(existing); added, dup, mx, supp = [], 0, 0, 0
    for row in RAW:
        e = row[0].strip().lower()
        if e in suppressed: supp += 1; continue
        if e in seen: dup += 1; continue
        if not email_ok(e): print(f"  BAD-MX  {e}"); mx += 1; continue
        seen.add(e); added.append(row); print(f"  OK      {e}")
    print(f"\nAdded {len(added)} | Dups {dup} | Bad-MX {mx} | Suppressed {supp}")
    if not added: return
    with FINAL_CSV.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for row in added:
            r=list(row)+[""]*(8-len(row)); w.writerow(r[:8])
    sup_now = load_set(SUPP_CSV)
    allrows = list(csv.DictReader(FINAL_CSV.open(encoding="utf-8-sig")))
    fn = list(allrows[0].keys())
    live = [r for r in allrows if (r.get("email","") or "").strip().lower() not in sup_now]
    with LIVE_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fn, extrasaction="ignore"); w.writeheader(); w.writerows(live)
    print(f"\ncontacts_final.csv: {len(allrows)} | contacts_live.csv: {len(live)}")

if __name__ == "__main__":
    main()
