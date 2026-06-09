#!/usr/bin/env python3
"""
Build contacts_tagged.csv from all sources:
  - contacts_master.csv (3,188 existing)
  - Mumbai police hierarchy (user-provided official emails)
  - Mumbai courts (agent research)
  - Mumbai administration/land records
Adds: name, designation, category, tags, priority_rank
Deduplicates by email, sorts by priority then category then email.
"""

import csv, re
from pathlib import Path

BASE = Path(__file__).parent

# ── TAG PRIORITY ORDER (lower number = higher priority / appears first) ──────
TAG_PRIORITY = {
    'top-priority':     1,
    'police-hq':        2,
    'court-high':       2,
    'police-zone':      3,
    'police-special':   3,
    'anti-corruption':  3,
    'economic-fraud':   3,
    'cyber-crime':      3,
    'anti-extortion':   3,
    'crime-branch':     3,
    'court-lower':      4,
    'court-sessions':   4,
    'court-family':     4,
    'govt-admin':       5,
    'land-records':     5,
    'police-station':   6,
    'press':            6,
    'govt-state':       6,
    'ngo-civic':        7,
    'goa':              7,
    'individual':       8,
    'corporate':        8,
    'dgp-desk':         9,
    'unverified':       9,
    'general':         10,
}

def priority_score(tags_str):
    if not tags_str:
        return 10
    return min(TAG_PRIORITY.get(t, 10) for t in tags_str.split('|'))


# ── ALL NEW MUMBAI CONTACTS ──────────────────────────────────────────────────
# Columns: email, name, designation, category, tags, case
NEW_MUMBAI = [

    # ── Commissioner's Office ──────────────────────────────────────────────
    ("cp.mumbai@mahapolice.gov.in",             "Commissioner of Police Mumbai",            "Commissioner of Police, Brihan Mumbai",                                        "Mumbai Police HQ",             "top-priority|police-hq"),
    ("cp.mumbai.jtcp.crime@mahapolice.gov.in",  "Jt. CP Crime Branch Mumbai",               "Joint Commissioner of Police (Crime), Mumbai",                                  "Mumbai Police - Crime Branch",  "top-priority|police-hq|crime-branch|anti-extortion"),
    ("dcpdet1.mum@mahapolice.gov.in",           "DCP Detection-1 Mumbai",                   "Deputy Commissioner of Police, Detection-1 (Anti-Extortion Cell supervisor)",    "Mumbai Police - Crime Branch",  "police-zone|crime-branch|anti-extortion"),

    # ── DGP Office Senior Officers ─────────────────────────────────────────
    ("dgpms.mumbai@mahapolice.gov.in",          "Director General of Police Maharashtra",    "Director General of Police, Maharashtra State",                                 "Maharashtra DGP",              "top-priority|police-hq"),
    ("adg.lo@mahapolice.gov.in",                "ADG (Law & Order) Mumbai",                 "Additional Director General of Police, Law & Order, Mumbai",                    "Maharashtra DGP",              "top-priority|police-hq"),
    ("adg.establishment@mahapolice.gov.in",     "ADG Establishment Mumbai",                 "Additional Director General of Police, Establishment, Mumbai",                  "Maharashtra DGP",              "police-hq"),
    ("adg.pc@mahapolice.gov.in",                "ADG (Planning & Coordination) Mumbai",     "Additional Director General of Police, Planning & Coordination, Mumbai",         "Maharashtra DGP",              "police-hq"),
    ("adg.admn@mahapolice.gov.in",              "ADG Administration Mumbai",                "Additional Director General of Police, Administration, Mumbai",                  "Maharashtra DGP",              "police-hq"),
    ("adg.sops.mahpol@nic.in",                  "ADG Special Operations Mumbai",            "Additional Director General of Police, Special Operations, Mumbai",              "Maharashtra DGP",              "top-priority|police-hq"),
    ("adg.policy@mahapolice.gov.in",            "ADG Policy Mumbai",                        "Additional Director General of Police, Policy, Mumbai",                         "Maharashtra DGP",              "police-hq"),
    ("adg.pcr.mumbai@mahapolice.gov.in",        "ADG (PCR) Mumbai",                         "Additional Director General of Police, PCR, Mumbai",                            "Maharashtra DGP",              "police-hq"),
    ("adg.eowms@mahapolice.gov.in",             "ADG Economic Offences Wing Mumbai",        "Additional Director General of Police, Economic Offences Wing (EOW)",            "Mumbai Police - EOW",          "top-priority|police-hq|police-special|economic-fraud"),
    ("adgp.trg@mahapolice.gov.in",              "ADGP Training Mumbai",                     "Additional Director General of Police, Training (Personal)",                    "Maharashtra DGP - Training",   "police-hq"),
    ("trg.directorate@mahapolice.gov.in",       "Training Branch Directorate",              "Training Branch, Maharashtra Police Directorate",                               "Maharashtra DGP - Training",   "police-hq"),
    ("adg.trg.office@mahapolice.gov.in",        "ADG Training Office Mumbai",               "ADG Training Office (All Staff), Maharashtra Police",                           "Maharashtra DGP - Training",   "police-hq"),
    ("ig.establishment@mahapolice.gov.in",      "IG Establishment Mumbai",                  "Inspector General, Establishment, Mumbai",                                      "Maharashtra DGP",              "police-hq"),
    ("ig.lo@mahapolice.gov.in",                 "IG (Law & Order) Mumbai",                  "Inspector General, Law & Order, Mumbai",                                        "Maharashtra DGP",              "police-hq"),
    ("ig.admin@mahapolice.gov.in",              "IG Administration Mumbai",                 "Inspector General, Administration, Mumbai",                                     "Maharashtra DGP",              "police-hq"),
    ("ig.training@mahapolice.gov.in",           "IG Training Mumbai",                       "Inspector General, Training, Mumbai",                                           "Maharashtra DGP",              "police-hq"),
    ("ig.paw@mahapolice.gov.in",                "IG (PAW) Mumbai",                          "Inspector General, PAW, Mumbai",                                                "Maharashtra DGP",              "police-hq"),
    ("ig.cbr-mah@gov.in",                       "IG Cyber Security Maharashtra",            "Inspector General, Cyber Bureau, Maharashtra",                                  "Maharashtra DGP - Cyber",      "top-priority|police-hq|cyber-crime"),
    ("dig.pcr.mumbai@mahapolice.gov.in",        "DIG (PCR) Mumbai",                         "Deputy Inspector General, PCR, Mumbai",                                         "Maharashtra DGP",              "police-hq"),
    ("aiglo.dgoffice@mahapolice.gov.in",        "AIG (L&O) DGP Office",                     "Assistant Inspector General, Law & Order, DGP Office",                          "Maharashtra DGP",              "police-hq"),
    ("aigamdmn.dgoffice@mahapolice.gov.in",     "AIG Administration DGP Office",            "Assistant Inspector General, Administration, DGP Office",                       "Maharashtra DGP",              "police-hq"),
    ("aigpestt.dgoffice@mahapolice.gov.in",     "AIG Establishment DGP Office",             "Assistant Inspector General, Establishment, DGP Office",                        "Maharashtra DGP",              "police-hq"),
    ("aig.pc@mahapolice.gov.in",                "AIG (Planning & Coordination)",            "Assistant Inspector General, Planning & Coordination",                          "Maharashtra DGP",              "police-hq"),
    ("aigpolicy.dgoffice@mahapolice.gov.in",    "AIG Policy DGP Office",                    "Assistant Inspector General, Policy, DGP Office",                               "Maharashtra DGP",              "police-hq"),
    ("aig.dakshata@mahapolice.gov.in",          "AIG Dakshata Mumbai",                      "Assistant Inspector General, Dakshata, Mumbai",                                 "Maharashtra DGP",              "police-hq"),
    ("sp.dgcontrolroom@mahapolice.gov.in",      "SP DGP Control Room",                      "Superintendent of Police, DG Control Room, Mumbai",                             "Maharashtra DGP",              "police-hq"),
    ("la.dgpoffice@mahapolice.gov.in",          "Legal Advisor DGP Office",                 "Legal Advisor, DGP Office, Mumbai",                                             "Maharashtra DGP",              "police-hq"),
    ("lo.dgpoffice@mahapolice.gov.in",          "Law Officer DGP Office",                   "Law Officer, DGP Office, Mumbai",                                               "Maharashtra DGP",              "police-hq"),
    ("mpd.dakshata@mahapolice.gov.in",          "Dakshata Office Maharashtra Police",       "Dakshata Office, Maharashtra Police",                                           "Maharashtra DGP",              "police-hq"),
    ("compcell.dgoffice@mahapolice.gov.in",     "Computer Cell DGP Office",                 "Computer Cell, DGP Office, Mumbai",                                             "Maharashtra DGP",              "police-hq"),

    # ── DGP Office AIG/Dy-AIG Level ───────────────────────────────────────
    ("srdyaigpen.dgoffice@mahapolice.gov.in",   "Sr Dy AIG Pension",                        "Senior Deputy AIG, Pension, DGP Office",                                        "Maharashtra DGP - Desk",       "dgp-desk|police-hq"),
    ("srdyaigest1.dgoffice@mahapolice.gov.in",  "Sr Dy AIG Establishment-1",               "Senior Deputy AIG, Establishment-1, DGP Office",                               "Maharashtra DGP - Desk",       "dgp-desk|police-hq"),
    ("dyaigcrime.dgoffice@mahapolice.gov.in",   "Dy AIG Crime DGP Office",                 "Deputy AIG, Crime, DGP Office",                                                 "Maharashtra DGP - Desk",       "dgp-desk|police-hq"),
    ("dyaigsb.dgoffice@mahapolice.gov.in",      "Dy AIG SB DGP Office",                    "Deputy AIG, Special Branch, DGP Office",                                        "Maharashtra DGP - Desk",       "dgp-desk|police-hq"),
    ("dyaigde.dgoffice@mahapolice.gov.in",      "Dy AIG DE DGP Office",                    "Deputy AIG, DE, DGP Office",                                                    "Maharashtra DGP - Desk",       "dgp-desk|police-hq"),
    ("dyaigconfi.dgoffice@mahapolice.gov.in",   "Dy AIG Confidential DGP Office",          "Deputy AIG, Confidential, DGP Office",                                          "Maharashtra DGP - Desk",       "dgp-desk|police-hq"),
    ("dyaigacc.dgoffice@mahapolice.gov.in",     "Dy AIG Accounts DGP Office",              "Deputy AIG, Accounts, DGP Office",                                              "Maharashtra DGP - Desk",       "dgp-desk|police-hq"),

    # ── DGP Office Desks 1-44 ─────────────────────────────────────────────
    ("desk1.dgoffice@mahapolice.gov.in",        "DGP Office Desk 1",    "Desk 1, DGP Office Mumbai",    "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk1a.dgoffice@mahapolice.gov.in",       "DGP Office Desk 1A",   "Desk 1A, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk2.dgoffice@mahapolice.gov.in",        "DGP Office Desk 2",    "Desk 2, DGP Office Mumbai",    "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk2a.dgoffice@mahapolice.gov.in",       "DGP Office Desk 2A",   "Desk 2A, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk3.dgoffice@mahapolice.gov.in",        "DGP Office Desk 3",    "Desk 3, DGP Office Mumbai",    "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk3a.dgoffice@mahapolice.gov.in",       "DGP Office Desk 3A",   "Desk 3A, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk4.dgoffice@mahapolice.gov.in",        "DGP Office Desk 4",    "Desk 4, DGP Office Mumbai",    "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk5.dgoffice@mahapolice.gov.in",        "DGP Office Desk 5",    "Desk 5, DGP Office Mumbai",    "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk5a.dgoffice@mahapolice.gov.in",       "DGP Office Desk 5A",   "Desk 5A, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk6.dgoffice@mahapolice.gov.in",        "DGP Office Desk 6",    "Desk 6, DGP Office Mumbai",    "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk8.dgoffice@mahapolice.gov.in",        "DGP Office Desk 8",    "Desk 8, DGP Office Mumbai",    "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk8a.dgoffice@mahapolice.gov.in",       "DGP Office Desk 8A",   "Desk 8A, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk9.dgoffice@mahapolice.gov.in",        "DGP Office Desk 9",    "Desk 9, DGP Office Mumbai",    "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk10.dgoffice@mahapolice.gov.in",       "DGP Office Desk 10",   "Desk 10, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk11.dgoffice@mahapolice.gov.in",       "DGP Office Desk 11",   "Desk 11, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk11a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 11A",  "Desk 11A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk12.dgoffice@mahapolice.gov.in",       "DGP Office Desk 12",   "Desk 12, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk13.dgoffice@mahapolice.gov.in",       "DGP Office Desk 13",   "Desk 13, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk14.dgoffice@mahapolice.gov.in",       "DGP Office Desk 14",   "Desk 14, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk14a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 14A",  "Desk 14A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk15.dgoffice@mahapolice.gov.in",       "DGP Office Desk 15",   "Desk 15, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk16.dgoffice@mahapolice.gov.in",       "DGP Office Desk 16",   "Desk 16, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk16a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 16A",  "Desk 16A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk16b.dgoffice@mahapolice.gov.in",      "DGP Office Desk 16B",  "Desk 16B, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk.17dgoffice@mahapolice.gov.in",       "DGP Office Desk 17",   "Desk 17, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk17a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 17A",  "Desk 17A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk18.dgoffice@mahapolice.gov.in",       "DGP Office Desk 18",   "Desk 18, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk19.dgoffice@mahapolice.gov.in",       "DGP Office Desk 19",   "Desk 19, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk20.dgoffice@mahapolice.gov.in",       "DGP Office Desk 20",   "Desk 20, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk20a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 20A",  "Desk 20A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk21.dgoffice@mahapolice.gov.in",       "DGP Office Desk 21",   "Desk 21, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk21a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 21A",  "Desk 21A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk22.dgoffice@mahapolice.gov.in",       "DGP Office Desk 22",   "Desk 22, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk23a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 23",   "Desk 23, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk24.dgoffice@mahapolice.gov.in",       "DGP Office Desk 24",   "Desk 24, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk25.dgoffice@mahapolice.gov.in",       "DGP Office Desk 25",   "Desk 25, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk26a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 26A",  "Desk 26A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk26b.dgoffice@mahapolice.gov.in",      "DGP Office Desk 26B",  "Desk 26B, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk27a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 27A",  "Desk 27A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk27b.dgoffice@mahapolice.gov.in",      "DGP Office Desk 27B",  "Desk 27B, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk28.dgoffice@mahapolice.gov.in",       "DGP Office Desk 28",   "Desk 28, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk28a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 28A",  "Desk 28A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk29.dgoffice@mahapolice.gov.in",       "DGP Office Desk 29",   "Desk 29, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk30.dgoffice@mahapolice.gov.in",       "DGP Office Desk 30",   "Desk 30, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk31.dgoffice@mahapolice.gov.in",       "DGP Office Desk 31",   "Desk 31, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk32.dgoffice@mahapolice.gov.in",       "DGP Office Desk 32",   "Desk 32, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk33.dgoffice@mahapolice.gov.in",       "DGP Office Desk 33",   "Desk 33, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk34.dgoffice@mahapolice.gov.in",       "DGP Office Desk 34",   "Desk 34, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk35.dgoffice@mahapolice.gov.in",       "DGP Office Desk 35",   "Desk 35, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk36.dgoffice@mahapolice.gov.in",       "DGP Office Desk 36",   "Desk 36, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk36a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 36A",  "Desk 36A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk38.dgoffice@mahapolice.gov.in",       "DGP Office Desk 38",   "Desk 38, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk39.dgoffice@mahapolice.gov.in",       "DGP Office Desk 39",   "Desk 39, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk40.dgoffice@mahapolice.gov.in",       "DGP Office Desk 40",   "Desk 40, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk41.dgoffice@mahapolice.gov.in",       "DGP Office Desk 41",   "Desk 41, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk42a.dgoffice@mahapolice.gov.in",      "DGP Office Desk 42A",  "Desk 42A, DGP Office Mumbai",  "Maharashtra DGP - Desk",  "dgp-desk"),
    ("desk44.dgoffice@mahapolice.gov.in",       "DGP Office Desk 44",   "Desk 44, DGP Office Mumbai",   "Maharashtra DGP - Desk",  "dgp-desk"),

    # ── Mumbai Police DCP Zones ───────────────────────────────────────────
    ("cp.mum.dcp.hq1@mahapolice.gov.in",        "DCP Administrative HQ-1 Mumbai",           "Deputy Commissioner of Police, Administrative Desk HQ-1",                       "Mumbai Police - DCP Admin",    "police-zone"),
    ("cp.mum.dcp.hq2@mahapolice.gov.in",        "DCP Administrative HQ-2 Mumbai",           "Deputy Commissioner of Police, Administrative Desk HQ-2",                       "Mumbai Police - DCP Admin",    "police-zone"),
    ("dcpzone1-mum@mahapolice.gov.in",          "DCP Zone I (South Mumbai)",                "Deputy Commissioner of Police, Zone I – South Mumbai",                          "Mumbai Police - DCP Zone",     "top-priority|police-zone"),
    ("dcpzone2-mum@mahapolice.gov.in",          "DCP Zone II (South-Central Mumbai)",       "Deputy Commissioner of Police, Zone II – South-Central",                        "Mumbai Police - DCP Zone",     "top-priority|police-zone"),
    ("dcpzone3-mum@mahapolice.gov.in",          "DCP Zone III (Byculla/Central Mumbai)",    "Deputy Commissioner of Police, Zone III – Byculla/Central",                    "Mumbai Police - DCP Zone",     "top-priority|police-zone"),
    ("dcpzone4-mum@mahapolice.gov.in",          "DCP Zone IV (Matunga/Sion Mumbai)",        "Deputy Commissioner of Police, Zone IV – Matunga/Sion",                        "Mumbai Police - DCP Zone",     "top-priority|police-zone"),
    ("dcpzone5-mum@mahapolice.gov.in",          "DCP Zone V (Worli/Dadar Mumbai)",          "Deputy Commissioner of Police, Zone V – Worli/Dadar",                          "Mumbai Police - DCP Zone",     "top-priority|police-zone"),
    ("dcpzone6-mum@mahapolice.gov.in",          "DCP Zone VI (Chembur/East Mumbai)",        "Deputy Commissioner of Police, Zone VI – Chembur/East",                        "Mumbai Police - DCP Zone",     "top-priority|police-zone"),
    ("dcpzone7-mum@mahapolice.gov.in",          "DCP Zone VII (Mulund/North-East Mumbai)",  "Deputy Commissioner of Police, Zone VII – Mulund/North-East",                  "Mumbai Police - DCP Zone",     "top-priority|police-zone"),
    ("dcpzone8-mum@mahapolice.gov.in",          "DCP Zone VIII (Bandra/BKC Mumbai)",        "Deputy Commissioner of Police, Zone VIII – Bandra/BKC",                        "Mumbai Police - DCP Zone",     "top-priority|police-zone"),
    ("dcpzone12-mum@mahapolice.gov.in",         "DCP Zone XII (Dahisar/North Mumbai)",      "Deputy Commissioner of Police, Zone XII – Dahisar/North",                      "Mumbai Police - DCP Zone",     "top-priority|police-zone"),

    # ── ACB Maharashtra ───────────────────────────────────────────────────
    ("acbwebmail@mahapolice.gov.in",            "ACB Maharashtra HQ",                       "Anti-Corruption Bureau Maharashtra — General Intake (DG: Shri Sanjeev Kumar Singhal IPS)",  "Mumbai Police - ACB",  "top-priority|police-special|anti-corruption"),
    ("addlcpacbmumbai@mahapolice.gov.in",       "Additional CP ACB Mumbai Range",           "Additional Commissioner of Police, ACB Mumbai (Shri Sandip Diwan / Shri Rajendra G. Sangale / Shri Anil T. Gheradikar)",  "Mumbai Police - ACB",  "top-priority|police-special|anti-corruption"),

    # ── Cyber Crime ───────────────────────────────────────────────────────
    ("cyberpst-mum@mahapolice.gov.in",          "Cyber Police Station Mumbai",              "Cyber Crime Police Station, Mumbai (ACP Irfan Sheikh)",                         "Mumbai Police - Cyber Crime",  "top-priority|police-special|cyber-crime"),
    ("ps.centralcyber.mum@mahapolice.gov.in",   "Cyber PS Mumbai Central Region",          "Cyber Police Station, Mumbai Central Region",                                   "Mumbai Police - Cyber Crime",  "police-special|cyber-crime"),
    ("ps.eastcyber.mum@mahapolice.gov.in",      "Cyber PS Mumbai East Region",             "Cyber Police Station, Mumbai East Region",                                      "Mumbai Police - Cyber Crime",  "police-special|cyber-crime"),
    ("ps.northcyber.mum@mahapolice.gov.in",     "Cyber PS Mumbai North Region",            "Cyber Police Station, Mumbai North Region",                                     "Mumbai Police - Cyber Crime",  "police-special|cyber-crime"),
    ("ps.southcyber.mum@mahapolice.gov.in",     "Cyber PS Mumbai South Region",            "Cyber Police Station, Mumbai South Region",                                     "Mumbai Police - Cyber Crime",  "police-special|cyber-crime"),

    # ── CID Maharashtra ───────────────────────────────────────────────────
    ("computer.cid@mahapolice.gov.in",          "CID Maharashtra State HQ",                "CID Maharashtra (ADGP Sunil Ramanand), State HQ Pune",                          "Maharashtra CID",              "top-priority|police-hq"),

    # ── Mumbai Police ACP Divisions ───────────────────────────────────────
    ("acpcolaba.mum@mahapolice.gov.in",         "ACP Colaba Division",          "Assistant Commissioner of Police, Colaba Division",        "Mumbai Police - ACP", "police-zone"),
    ("acpam.mum@mahapolice.gov.in",             "ACP Azad Maidan Division",     "Assistant Commissioner of Police, Azad Maidan Division",   "Mumbai Police - ACP", "police-zone"),
    ("acpdongri.mum@mahapolice.gov.in",         "ACP Dongri Division",          "Assistant Commissioner of Police, Dongri Division",        "Mumbai Police - ACP", "police-zone"),
    ("acppyd.mum@mahapolice.gov.in",            "ACP Pydhonie Division",        "Assistant Commissioner of Police, Pydhonie Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpgirgaon.mum@mahapolice.gov.in",        "ACP Girgaon Division",         "Assistant Commissioner of Police, Girgaon Division",       "Mumbai Police - ACP", "police-zone"),
    ("acpgamdevi.mum@mahapolice.gov.in",        "ACP Gamdevi Division",         "Assistant Commissioner of Police, Gamdevi Division",       "Mumbai Police - ACP", "police-zone"),
    ("acpyg.mum@mahapolice.gov.in",             "ACP Yellow Gate Division",     "Assistant Commissioner of Police, Yellow Gate Division",   "Mumbai Police - ACP", "police-zone"),
    ("acpwadala.mum@mahapolice.gov.in",         "ACP Wadala Division",          "Assistant Commissioner of Police, Wadala Division",        "Mumbai Police - ACP", "police-zone"),
    ("acptardeo.mum@mahapolice.gov.in",         "ACP Tardeo Division",          "Assistant Commissioner of Police, Tardeo Division",        "Mumbai Police - ACP", "police-zone"),
    ("acpagripada.mum@mahapolice.gov.in",       "ACP Agripada Division",        "Assistant Commissioner of Police, Agripada Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpworli.mum@mahapolice.gov.in",          "ACP Worli Division",           "Assistant Commissioner of Police, Worli Division",         "Mumbai Police - ACP", "police-zone"),
    ("acpbhoiwada.mum@mahapolice.gov.in",       "ACP Bhoiwada Division",        "Assistant Commissioner of Police, Bhoiwada Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpmatunga.mum@mahapolice.gov.in",        "ACP Matunga Division",         "Assistant Commissioner of Police, Matunga Division",       "Mumbai Police - ACP", "police-zone"),
    ("acpsion.mum@mahapolice.gov.in",           "ACP Sion Division",            "Assistant Commissioner of Police, Sion Division",          "Mumbai Police - ACP", "police-zone"),
    ("acpdadar.mum@mahapolice.gov.in",          "ACP Dadar Division",           "Assistant Commissioner of Police, Dadar Division",         "Mumbai Police - ACP", "police-zone"),
    ("acpmahim.mum@mahapolice.gov.in",          "ACP Mahim Division",           "Assistant Commissioner of Police, Mahim Division",         "Mumbai Police - ACP", "police-zone"),
    ("acpkurla.mum@mahapolice.gov.in",          "ACP Kurla Division",           "Assistant Commissioner of Police, Kurla Division",         "Mumbai Police - ACP", "police-zone"),
    ("acpnehrunagar.mum@mahapolice.gov.in",     "ACP Nehru Nagar Division",     "Assistant Commissioner of Police, Nehru Nagar Division",   "Mumbai Police - ACP", "police-zone"),
    ("acpchembur.mum@mahapolice.gov.in",        "ACP Chembur Division",         "Assistant Commissioner of Police, Chembur Division",       "Mumbai Police - ACP", "police-zone"),
    ("acptrombay.mum@mahapolice.gov.in",        "ACP Trombay Division",         "Assistant Commissioner of Police, Trombay Division",       "Mumbai Police - ACP", "police-zone"),
    ("acpdeonar.mum@mahapolice.gov.in",         "ACP Deonar Division",          "Assistant Commissioner of Police, Deonar Division",        "Mumbai Police - ACP", "police-zone"),
    ("acpghatkopar.mum@mahapolice.gov.in",      "ACP Ghatkopar Division",       "Assistant Commissioner of Police, Ghatkopar Division",     "Mumbai Police - ACP", "police-zone"),
    ("acpvikhroli.mum@mahapolice.gov.in",       "ACP Vikhroli Division",        "Assistant Commissioner of Police, Vikhroli Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpbhandup.mum@mahapolice.gov.in",        "ACP Bhandup Division",         "Assistant Commissioner of Police, Bhandup Division",       "Mumbai Police - ACP", "police-zone"),
    ("acpmulund.mum@mahapolice.gov.in",         "ACP Mulund Division",          "Assistant Commissioner of Police, Mulund Division",        "Mumbai Police - ACP", "police-zone"),
    ("acpvakola.mum@mahapolice.gov.in",         "ACP Vakola Division",          "Assistant Commissioner of Police, Vakola Division",        "Mumbai Police - ACP", "police-zone"),
    ("acpkherwadi.mum@mahapolice.gov.in",       "ACP Kherwadi Division",        "Assistant Commissioner of Police, Kherwadi Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpairport.mum@mahapolice.gov.in",        "ACP Airport Division",         "Assistant Commissioner of Police, Airport Division",       "Mumbai Police - ACP", "police-zone"),
    ("acpbandra.mum@mahapolice.gov.in",         "ACP Bandra Division",          "Assistant Commissioner of Police, Bandra Division",        "Mumbai Police - ACP", "police-zone"),
    ("acposhiwara.mum@mahapolice.gov.in",       "ACP Oshiwara Division",        "Assistant Commissioner of Police, Oshiwara Division",      "Mumbai Police - ACP", "police-zone"),
    ("acp.santacruzdiv@mahapolice.gov.in",      "ACP Santacruz Division",       "Assistant Commissioner of Police, Santacruz Division",     "Mumbai Police - ACP", "police-zone"),
    ("acpdnnagar.mum@mahapolice.gov.in",        "ACP D.N. Nagar Division",      "Assistant Commissioner of Police, D.N. Nagar Division",    "Mumbai Police - ACP", "police-zone"),
    ("acpmeghwadi.mum@mahapolice.gov.in",       "ACP Meghwadi Division",        "Assistant Commissioner of Police, Meghwadi Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpsakinaka.mum@mahapolice.gov.in",       "ACP Sakinaka Division",        "Assistant Commissioner of Police, Sakinaka Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpandheri.mum@mahapolice.gov.in",        "ACP Andheri Division",         "Assistant Commissioner of Police, Andheri Division",       "Mumbai Police - ACP", "police-zone"),
    ("acpgoregaon.mum@mahapolice.gov.in",       "ACP Goregaon Division",        "Assistant Commissioner of Police, Goregaon Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpmalad.mum@mahapolice.gov.in",          "ACP Malad/Malvani Division",   "Assistant Commissioner of Police, Malad/Malvani Division", "Mumbai Police - ACP", "police-zone"),
    ("acpborivali.mum@mahapolice.gov.in",       "ACP Borivali Division",        "Assistant Commissioner of Police, Borivali Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpdindoshi.mum@mahapolice.gov.in",       "ACP Dindoshi Division",        "Assistant Commissioner of Police, Dindoshi Division",      "Mumbai Police - ACP", "police-zone"),
    ("acpsamtanagar.mum@mahapolice.gov.in",     "ACP Samata Nagar Division",    "Assistant Commissioner of Police, Samata Nagar Division",  "Mumbai Police - ACP", "police-zone"),
    ("acpdahisar.mum@mahapolice.gov.in",        "ACP Dahisar Division",         "Assistant Commissioner of Police, Dahisar Division",       "Mumbai Police - ACP", "police-zone"),
    ("cyberpst-mum@mahapolice.gov.in",          "ACP Cyber Division",           "ACP Cyber Division, Mumbai (Irfan Sheikh)",                "Mumbai Police - ACP", "police-zone|police-special|cyber-crime"),

    # ── Mumbai Police Stations ────────────────────────────────────────────
    ("ps.aareysub.mum@mahapolice.gov.in",       "Aarey Sub-Division PS",        "Aarey Sub-Division Police Station",        "Mumbai Police Station", "police-station"),
    ("ps.nmjoshimarg.mum@mahapolice.gov.in",    "N.M. Joshi Marg PS",           "N.M. Joshi Marg Police Station",           "Mumbai Police Station", "police-station"),
    ("ps.shivajinagar.mum@mahapolice.gov.in",   "Shivaji Nagar PS",             "Shivaji Nagar Police Station",             "Mumbai Police Station", "police-station"),
    ("ps.agripada.mum@mahapolice.gov.in",       "Agripada PS",                  "Agripada Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.ltmarg.mum@mahapolice.gov.in",         "L.T. Marg PS",                 "L.T. Marg Police Station",                 "Mumbai Police Station", "police-station"),
    ("ps.airport.mum@mahapolice.gov.in",        "Airport PS",                   "Airport Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.amboli.mum@mahapolice.gov.in",         "Amboli PS",                    "Amboli Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.andheri.mum@mahapolice.gov.in",        "Andheri PS",                   "Andheri Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.antophill.mum@mahapolice.gov.in",      "Antop Hill PS",                "Antop Hill Police Station",                "Mumbai Police Station", "police-station"),
    ("ps.azadmaidan.mum@mahapolice.gov.in",     "Azad Maidan PS",               "Azad Maidan Police Station",               "Mumbai Police Station", "police-station"),
    ("ps.bkc.mum@mahapolice.gov.in",            "BKC PS",                       "BKC Police Station",                       "Mumbai Police Station", "police-station"),
    ("ps.bandra.mum@mahapolice.gov.in",         "Bandra PS",                    "Bandra Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.bangurnagar.mum@mahapolice.gov.in",    "Bangur Nagar PS",              "Bangur Nagar Police Station",              "Mumbai Police Station", "police-station"),
    ("ps.bhandup.mum@mahapolice.gov.in",        "Bhandup PS",                   "Bhandup Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.bhoiwada.mum@mahapolice.gov.in",       "Bhoiwada PS",                  "Bhoiwada Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.dharavi.mum@mahapolice.gov.in",        "Dharavi PS",                   "Dharavi Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.borivali.mum@mahapolice.gov.in",       "Borivali PS",                  "Borivali Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.charkop.mum@mahapolice.gov.in",        "Charkop PS",                   "Charkop Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.chembur.mum@mahapolice.gov.in",        "Chembur PS",                   "Chembur Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.chunabhatti.mum@mahapolice.gov.in",    "Chunabhatti PS",               "Chunabhatti Police Station",               "Mumbai Police Station", "police-station"),
    ("ps.byculla.mum@mahapolice.gov.in",        "Byculla PS",                   "Byculla Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.colaba.mum@mahapolice.gov.in",         "Colaba PS",                    "Colaba Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.cuffeparade.mum@mahapolice.gov.in",    "Cuffe Parade PS",              "Cuffe Parade Police Station",              "Mumbai Police Station", "police-station"),
    ("ps.dbmarg.mum@mahapolice.gov.in",         "Dr. D.B. Marg PS",             "Dr. D.B. Marg Police Station",             "Mumbai Police Station", "police-station"),
    ("ps.dnnagar.mum@mahapolice.gov.in",        "D.N. Nagar PS",                "D.N. Nagar Police Station",                "Mumbai Police Station", "police-station"),
    ("ps.dadar.mum@mahapolice.gov.in",          "Dadar PS",                     "Dadar Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.dahisar.mum@mahapolice.gov.in",        "Dahisar PS",                   "Dahisar Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.deonar.mum@mahapolice.gov.in",         "Deonar PS",                    "Deonar Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.dindoshi.mum@mahapolice.gov.in",       "Dindoshi PS",                  "Dindoshi Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.dongri.mum@mahapolice.gov.in",         "Dongri PS",                    "Dongri Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.gamdevi.mum@mahapolice.gov.in",        "Gamdevi PS",                   "Gamdevi Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.ghatkopar.mum@mahapolice.gov.in",      "Ghatkopar PS",                 "Ghatkopar Police Station",                 "Mumbai Police Station", "police-station"),
    ("ps.gorai.mum@mahapolice.gov.in",          "Gorai PS",                     "Gorai Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.goregaon.mum@mahapolice.gov.in",       "Goregaon PS",                  "Goregaon Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.govandi.mum@mahapolice.gov.in",        "Govandi PS",                   "Govandi Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.jogeshwari.mum@mahapolice.gov.in",     "Jogeshwari PS",                "Jogeshwari Police Station",                "Mumbai Police Station", "police-station"),
    ("ps.juhu.mum@mahapolice.gov.in",           "Juhu PS",                      "Juhu Police Station",                      "Mumbai Police Station", "police-station"),
    ("ps.kalachowki.mum@mahapolice.gov.in",     "Kalachowki PS",                "Kalachowki Police Station",                "Mumbai Police Station", "police-station"),
    ("ps.kandivali.mum@mahapolice.gov.in",      "Kandivali PS",                 "Kandivali Police Station",                 "Mumbai Police Station", "police-station"),
    ("ps.kanjurmarg.mum@mahapolice.gov.in",     "Kanjurmarg PS",                "Kanjurmarg Police Station",                "Mumbai Police Station", "police-station"),
    ("ps.kasturba.mum@mahapolice.gov.in",       "Kasturba Marg PS",             "Kasturba Marg Police Station",             "Mumbai Police Station", "police-station"),
    ("ps.khar.mum@mahapolice.gov.in",           "Khar PS",                      "Khar Police Station",                      "Mumbai Police Station", "police-station"),
    ("ps.kherwadi.mum@mahapolice.gov.in",       "Kherwadi PS",                  "Kherwadi Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.kurar.mum@mahapolice.gov.in",          "Kurar PS",                     "Kurar Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.kurla.mum@mahapolice.gov.in",          "Kurla PS",                     "Kurla Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.mhb.mum@mahapolice.gov.in",            "MHB Colony PS",                "MHB Colony Police Station",                "Mumbai Police Station", "police-station"),
    ("ps.mra.mum@mahapolice.gov.in",            "MRA Marg PS",                  "MRA Marg Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.mahim.mum@mahapolice.gov.in",          "Mahim PS",                     "Mahim Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.malad.mum@mahapolice.gov.in",          "Malad PS",                     "Malad Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.malabarhill.mum@mahapolice.gov.in",    "Malabar Hill PS",              "Malabar Hill Police Station",              "Mumbai Police Station", "police-station"),
    ("ps.malvani.mum@mahapolice.gov.in",        "Malvani PS",                   "Malvani Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.mankhurd.mum@mahapolice.gov.in",       "Mankhurd PS",                  "Mankhurd Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.marinedrive.mum@mahapolice.gov.in",    "Marine Drive PS",              "Marine Drive Police Station",              "Mumbai Police Station", "police-station"),
    ("ps.matunga.mum@mahapolice.gov.in",        "Matunga PS",                   "Matunga Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.meghwadi.mum@mahapolice.gov.in",       "Meghwadi PS",                  "Meghwadi Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.mulund.mum@mahapolice.gov.in",         "Mulund PS",                    "Mulund Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.mumbaisagari.mum@mahapolice.gov.in",   "Mumbai Sagari-1 PS",           "Mumbai Sagari-1 (Marine) Police Station",  "Mumbai Police Station", "police-station"),
    ("ps.sagari2.mum@mahapolice.gov.in",        "Mumbai Sagari-2 PS",           "Mumbai Sagari-2 (Marine) Police Station",  "Mumbai Police Station", "police-station"),
    ("ps.nagpada.mum@mahapolice.gov.in",        "Nagpada PS",                   "Nagpada Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.navghar.mum@mahapolice.gov.in",        "Navghar PS",                   "Navghar Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.nehrunagar.mum@mahapolice.gov.in",     "Nehru Nagar PS",               "Nehru Nagar Police Station",               "Mumbai Police Station", "police-station"),
    ("ps.nirmalnagar.mum@mahapolice.gov.in",    "Nirmal Nagar PS",              "Nirmal Nagar Police Station",              "Mumbai Police Station", "police-station"),
    ("ps.oshiwara.mum@mahapolice.gov.in",       "Oshiwara PS",                  "Oshiwara Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.pantnagar.mum@mahapolice.gov.in",      "Pantnagar PS",                 "Pantnagar Police Station",                 "Mumbai Police Station", "police-station"),
    ("ps.parksite.mum@mahapolice.gov.in",       "Parksite PS",                  "Parksite Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.powai.mum@mahapolice.gov.in",          "Powai PS",                     "Powai Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.paydhunie.mum@mahapolice.gov.in",      "Paydhuni PS",                  "Paydhuni Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.rcf.mum@mahapolice.gov.in",            "RCF PS",                       "RCF Police Station",                       "Mumbai Police Station", "police-station"),
    ("ps.sahar.mum@mahapolice.gov.in",          "Sahar PS",                     "Sahar Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.sakinaka.mum@mahapolice.gov.in",       "Sakinaka PS",                  "Sakinaka Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.samtanagar.mum@mahapolice.gov.in",     "Samata Nagar PS",              "Samata Nagar Police Station",              "Mumbai Police Station", "police-station"),
    ("ps.santacruz.mum@mahapolice.gov.in",      "Santacruz PS",                 "Santacruz Police Station",                 "Mumbai Police Station", "police-station"),
    ("ps.sewri.mum@mahapolice.gov.in",          "Sewri/Shivdi PS",              "Sewri/Shivdi Police Station",              "Mumbai Police Station", "police-station"),
    ("ps.shahunagar.mum@mahapolice.gov.in",     "Shahu Nagar PS",               "Shahu Nagar Police Station",               "Mumbai Police Station", "police-station"),
    ("ps.shivajipark.mum@mahapolice.gov.in",    "Shivaji Park PS",              "Shivaji Park Police Station",              "Mumbai Police Station", "police-station"),
    ("ps.jjmarg.mum@mahapolice.gov.in",         "Sir J.J. Marg PS",             "Sir J.J. Marg Police Station",             "Mumbai Police Station", "police-station"),
    ("ps.tardeo.mum@mahapolice.gov.in",         "Tardeo PS",                    "Tardeo Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.tilaknagar.mum@mahapolice.gov.in",     "Tilak Nagar PS",               "Tilak Nagar Police Station",               "Mumbai Police Station", "police-station"),
    ("ps.trombay.mum@mahapolice.gov.in",        "Trombay PS",                   "Trombay Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.vbnagar.mum@mahapolice.gov.in",        "Vinoba Bhave Nagar PS",        "Vinoba Bhave Nagar Police Station",        "Mumbai Police Station", "police-station"),
    ("ps.vproad.mum@mahapolice.gov.in",         "V.P. Road PS",                 "V.P. Road Police Station",                 "Mumbai Police Station", "police-station"),
    ("ps.vakola.mum@mahapolice.gov.in",         "Vakola PS",                    "Vakola Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.goregaoneatc.mum@mahapolice.gov.in",   "Vanrai (Goregaon East ATC) PS","Vanrai Police Station (Goregaon East ATC)","Mumbai Police Station", "police-station"),
    ("ps.versova.mum@mahapolice.gov.in",        "Versova PS",                   "Versova Police Station",                   "Mumbai Police Station", "police-station"),
    ("ps.vikhroli.mum@mahapolice.gov.in",       "Vikhroli PS",                  "Vikhroli Police Station",                  "Mumbai Police Station", "police-station"),
    ("ps.vileparle.mum@mahapolice.gov.in",      "Vile Parle PS",                "Vile Parle Police Station",                "Mumbai Police Station", "police-station"),
    ("ps.wadala.mum@mahapolice.gov.in",         "Wadala PS",                    "Wadala Police Station",                    "Mumbai Police Station", "police-station"),
    ("ps.wtt.mum@mahapolice.gov.in",            "Wadala Truck Terminal PS",     "Wadala Truck Terminal Police Station",      "Mumbai Police Station", "police-station"),
    ("ps.worli.mum@mahapolice.gov.in",          "Worli PS",                     "Worli Police Station",                     "Mumbai Police Station", "police-station"),
    ("ps.yellowgate.mum@mahapolice.gov.in",     "Yellow Gate PS",               "Yellow Gate Police Station",               "Mumbai Police Station", "police-station"),

    # ── Bombay High Court ─────────────────────────────────────────────────
    ("hcbom.mah@nic.in",                        "Registrar General BHC",                    "Registrar General, Bombay High Court",                                          "Bombay High Court",            "top-priority|court-high"),
    ("regos-bhc@nic.in",                        "Registrar Original Side BHC",              "Registrar, Original Side, Bombay High Court",                                   "Bombay High Court",            "court-high"),
    ("judlib-bhc@nic.in",                       "Judges Library BHC",                       "Judges Library, Bombay High Court",                                             "Bombay High Court",            "court-high"),
    ("protocol-bhc@nic.in",                     "Protocol Department BHC",                  "Protocol Department, Bombay High Court",                                        "Bombay High Court",            "court-high"),
    ("commfortakacc-bhc@nic.in",                "Commissioner for Accounts BHC",            "Commissioner for Taking Accounts, Bombay High Court",                           "Bombay High Court",            "court-high"),
    ("crcvr-bhc@nic.in",                        "Court Receiver BHC",                       "Court Receiver, Bombay High Court",                                             "Bombay High Court",            "court-high"),
    ("cr-bhc@nic.in",                           "Company Registrar BHC",                    "Company Registrar, Bombay High Court",                                          "Bombay High Court",            "court-high"),
    ("ir-bhc@nic.in",                           "Insolvency Registrar BHC",                 "Insolvency Registrar, Bombay High Court",                                       "Bombay High Court",            "court-high"),
    ("hcnag.mah@nic.in",                        "BHC Nagpur Bench",                         "Bombay High Court, Nagpur Bench",                                               "Bombay High Court",            "court-high"),
    ("hcaur.mah@nic.in",                        "BHC Aurangabad Bench",                     "Bombay High Court, Aurangabad Bench",                                           "Bombay High Court",            "court-high"),
    ("reg-high.goa@nic.in",                     "BHC Goa Bench Registrar",                  "Registrar, High Court of Bombay at Goa",                                        "Bombay High Court",            "court-high|goa"),

    # ── CMM / Magistrate Courts Mumbai ────────────────────────────────────
    ("cmm-mum.mh@bhc.gov.in",                   "CMM Esplanade Mumbai",                     "Chief Metropolitan Magistrate, Esplanade, Mumbai",                              "CMM Courts Mumbai",            "top-priority|court-lower"),
    ("registrar.esplan@bhc.gov.in",             "Registrar Esplanade Courts",               "Registrar, Esplanade Courts, Mumbai",                                           "CMM Courts Mumbai",            "court-lower"),
    ("acmmmaz-mum.mh@bhc.gov.in",               "ACJM Mazgaon Mumbai",                      "Additional Chief Judicial Magistrate, Mazgaon",                                 "CMM Courts Mumbai",            "court-lower"),
    ("acmmkurla.mum.mh@bhc.gov.in",             "ACJM Kurla Mumbai",                        "Additional Chief Judicial Magistrate, Kurla",                                   "CMM Courts Mumbai",            "court-lower"),
    ("acmmgir-mum.mh@bhc.gov.in",               "ACJM Girgaon Mumbai",                      "Additional Chief Judicial Magistrate, Girgaon",                                 "CMM Courts Mumbai",            "court-lower"),
    ("acmmdadar.mum.mh@bhc.gov.in",             "ACJM Dadar Mumbai",                        "Additional Chief Judicial Magistrate, Dadar",                                   "CMM Courts Mumbai",            "court-lower"),
    ("acmmvik-mum.mh@bhc.gov.in",               "ACJM Vikhroli Mumbai",                     "Additional Chief Judicial Magistrate, Vikhroli",                                "CMM Courts Mumbai",            "court-lower"),
    ("acmmbori-mum@bhc.gov.in",                 "ACJM Borivali Mumbai",                     "Additional Chief Judicial Magistrate, Borivali",                                "CMM Courts Mumbai",            "court-lower"),
    ("acmmban-mum.mh@bhc.gov.in",               "ACJM Bandra Mumbai",                       "Additional Chief Judicial Magistrate, Bandra",                                  "CMM Courts Mumbai",            "court-lower"),
    ("acmmandheri-mum@bhc.gov.in",              "ACJM Andheri Mumbai",                      "Additional Chief Judicial Magistrate, Andheri",                                 "CMM Courts Mumbai",            "court-lower"),
    ("acmmballard.mh@bhc.gov.in",               "ACJM Ballard Pier Mumbai",                 "Additional Chief Judicial Magistrate, Ballard Pier",                            "CMM Courts Mumbai",            "court-lower"),
    ("mmshw-mum.mh@bhc.gov.in",                 "JMFC Shindewadi Mumbai",                   "Judicial Magistrate First Class, Shindewadi",                                   "CMM Courts Mumbai",            "court-lower"),
    ("mmjuv-mum.mh@bhc.gov.in",                 "Juvenile Justice Board Mumbai",            "Juvenile Justice Board, Mumbai",                                                "CMM Courts Mumbai",            "court-lower"),
    ("mmmulund.mum.mh@bhc.gov.in",              "JMFC Mulund Mumbai",                       "Judicial Magistrate First Class, Mulund",                                       "CMM Courts Mumbai",            "court-lower"),
    ("mmcst.mum.mh@bhc.gov.in",                 "CST Railway Court Mumbai",                 "Judicial Magistrate First Class, C.S.T. Railway",                               "CMM Courts Mumbai",            "court-lower"),
    ("mmvp-mum.mh@bhc.gov.in",                  "JMFC Vile Parle Mumbai",                   "Judicial Magistrate First Class, Vile Parle",                                   "CMM Courts Mumbai",            "court-lower"),
    ("mmmct.mum.mh@bhc.gov.in",                 "Mumbai Central Railway Court",             "Judicial Magistrate First Class, Mumbai Central Railway",                       "CMM Courts Mumbai",            "court-lower"),

    # ── City Civil & Sessions Court ───────────────────────────────────────
    ("ctcourt-mum@nic.in",                      "Registrar City Civil & Sessions Court",    "Registrar, City Civil & Sessions Court, Fort, Mumbai",                          "Sessions Court Mumbai",        "top-priority|court-sessions"),
    ("ctcivilcourtdinsc@aij.gov.in",            "Additional Registrar City Civil Court Dindoshi", "Additional Registrar, City Civil Court, Dindoshi",                         "Sessions Court Mumbai",        "court-sessions"),
    ("ctcourt-mazgoan@bhc.gov.in",              "Asst. Registrar City Civil Court Mazgaon", "Assistant Registrar, City Civil Court, Mazgaon",                                "Sessions Court Mumbai",        "court-sessions"),

    # ── Family Court Mumbai ───────────────────────────────────────────────
    ("fc-bhc@nic.in",                           "Family Court Mumbai BKC",                  "Family Court, BKC, Bandra (East), Mumbai 400051",                               "Family Court Mumbai",          "court-family"),

    # ── Mumbai Administration — Collectors ───────────────────────────────
    ("collector.mumbaicity@maharashtra.gov.in", "Hon. Aanchal Goyal IAS",                   "Collector & District Magistrate, Mumbai City (South Mumbai)",                   "Mumbai Administration",        "top-priority|govt-admin|land-records"),
    ("collector.mumbaisuburb@maharashtra.gov.in","Shri Saurabh Katiyar",                    "District Collector & Magistrate, Mumbai Suburban (Bandra–Dahisar / Kurla–Mulund)","Mumbai Administration",        "top-priority|govt-admin|land-records"),

    # ── Mumbai Administration — Land Records ─────────────────────────────
    ("dycollcolaba@yahoo.in",                   "Shri Prashant Panvekar",                   "Deputy Collector (Encroachment & Removal), Colaba Branch",                      "Mumbai Administration - Land", "govt-admin|land-records"),
    ("dyencdharavi01@gmail.com",                "Shri Prashant Panvekar (Add. Charge)",     "Deputy Collector (Removal), Dharavi Division",                                  "Mumbai Administration - Land", "govt-admin|land-records"),
    ("cts.rev.mumbaicity@gmail.com",            "Shri Dhanajirao Kashinath Dhaygude",       "Superintendent, City Survey & Land Records, Mumbai City",                       "Mumbai Administration - Land", "govt-admin|land-records"),
    ("dslr.msd@gmail.com",                      "Shri Krishnat Kanse",                      "District Superintendent of Land Records, Mumbai Suburban",                      "Mumbai Administration - Land", "govt-admin|land-records"),
    ("dyslrmsd@gmail.com",                      "Shri Vikas Rane",                          "Deputy Superintendent of Land Records, Mumbai Suburban",                        "Mumbai Administration - Land", "govt-admin|land-records"),
    ("ctsovileparle@gmail.com",                 "Shri Dattatray Satpute",                   "City Survey Officer, Vile Parle Range",                                         "Mumbai Administration - Land", "govt-admin|land-records"),
    ("ctsogoregaon@gmail.com",                  "Shri Ranjit Deshmukh",                     "City Survey Officer, Goregaon Range",                                           "Mumbai Administration - Land", "govt-admin|land-records"),
    ("ctsochembur80@gmail.com",                 "Shri Milind Bhole",                        "City Survey Officer, Chembur Range",                                            "Mumbai Administration - Land", "govt-admin|land-records"),
    ("ctsoghatkopar@gmail.com",                 "Shri Sujit Jadhav",                        "City Survey Officer, Ghatkopar Range",                                          "Mumbai Administration - Land", "govt-admin|land-records"),

    # ── Maharashtra Home Department ───────────────────────────────────────
    ("sandeep.dhakane@nic.in",                  "Sandeep Dhakane",                          "Web Information Manager, Home Department, Mantralaya Mumbai",                   "Maharashtra Home Department",  "govt-state"),
]


# ── AUTO-TAGGER for existing contacts ────────────────────────────────────────
def auto_tag(email, name, category, source, case):
    tags = set()
    e = email.lower()
    domain = e.split('@')[1] if '@' in e else ''
    cat = (category or '').lower()
    src = (source or '').lower()

    if case == 'olympio-almeida' or 'goa' in domain:
        tags.add('goa')

    if 'mahapolice.gov.in' in domain:
        tags.add('police-hq')  # default for mahapolice
        if re.match(r'^(dgpms|adg\.|adgp\.)', e):
            tags.add('top-priority')
        if re.match(r'^(ig\.|jcp|cp\.mumbai)', e):
            tags.add('top-priority')
        if re.search(r'^dcp', e) or 'jtcp' in e:
            tags.add('police-zone')
            tags.discard('police-hq')
            if 'det1' in e or 'crime' in e:
                tags.add('crime-branch')
        if re.match(r'^acp', e):
            tags.add('police-zone')
            tags.discard('police-hq')
        if re.match(r'^ps\.', e):
            tags.add('police-station')
            tags.discard('police-hq')
        if 'acb' in e or 'addlcpacb' in e:
            tags.add('police-special'); tags.add('anti-corruption')
        if 'cyber' in e:
            tags.add('police-special'); tags.add('cyber-crime')
        if 'eow' in e:
            tags.add('police-special'); tags.add('economic-fraud')
        if re.match(r'^(desk\d|desk\.|srdyaig|dyaig|aig[a-z])', e):
            tags.add('dgp-desk')
        if 'cbcid' in e or '.cid@' in e:
            tags.add('police-hq')

    if domain in ('bhc.gov.in',) or domain.endswith('bhc.gov.in'):
        if re.match(r'^(cmm|acmm|mm|registrar\.)', e):
            tags.add('court-lower')
        elif 'fc-bhc' in e:
            tags.add('court-family')
        else:
            tags.add('court-lower')

    if domain == 'nic.in':
        if re.match(r'^(hcbom|hcnag|hcaur|reg-high|regos|judlib|protocol|commfort|crcvr|cr-|ir-)', e):
            tags.add('court-high')
        elif re.match(r'^ctcourt', e):
            tags.add('court-sessions')
        elif 'fc-bhc' in e:
            tags.add('court-family')
        elif 'police' in e or any(x in e for x in ['acb', 'eow', 'cid', 'adg', 'ig.', 'sp.']):
            tags.add('police-hq')
        else:
            tags.add('govt-state')

    if 'maharashtra.gov.in' in domain:
        if 'collector' in e:
            tags.add('top-priority'); tags.add('govt-admin'); tags.add('land-records')
        else:
            tags.add('govt-state')

    if 'goapolice.gov.in' in domain:
        tags.add('police-hq'); tags.add('goa')

    if 'gspcb.in' in domain or 'goa@nic.in' in e:
        tags.add('govt-state'); tags.add('goa')

    if 'journalist' in src:
        tags.add('press')
    if 'police_emails' in src:
        tags.add('police-hq')

    if 'press' in cat or 'media' in cat or 'journalist' in cat:
        tags.add('press')
    if 'government' in cat or 'minister' in cat or 'elected' in cat:
        tags.add('govt-state')
    if 'ngo' in cat or 'civic' in cat:
        tags.add('ngo-civic')
    if 'regulator' in cat or 'environment' in cat:
        tags.add('ngo-civic'); tags.add('govt-state')
    if 'corporate' in cat:
        tags.add('corporate')
    if 'individual supporter' in cat:
        tags.add('individual'); tags.add('goa')
    if 'general' in cat:
        tags.add('police-hq')  # Santosh_all etc. are police/govt

    # Gmail/Yahoo addresses from land records: keep but mark
    if domain in ('gmail.com', 'yahoo.in', 'yahoo.co.in') and not tags:
        tags.add('unverified')

    return '|'.join(sorted(tags)) if tags else 'general'


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    out_fields = ['email', 'name', 'designation', 'category', 'tags', 'case', 'source']

    # Build lookup: email -> row dict
    contacts = {}  # email -> dict

    # 1. Load existing master CSV
    src = BASE / 'contacts_master.csv'
    existing = list(csv.DictReader(src.open(encoding='utf-8-sig')))
    print(f"Loaded {len(existing)} from contacts_master.csv")

    for row in existing:
        email = row['email'].strip().lower()
        if not email or email in contacts:
            continue
        tags = auto_tag(email, row.get('name',''), row.get('category',''), row.get('source',''), row.get('case',''))
        contacts[email] = {
            'email':       email,
            'name':        row.get('name', ''),
            'designation': '',
            'category':    row.get('category', ''),
            'tags':        tags,
            'case':        row.get('case', ''),
            'source':      row.get('source', ''),
        }

    # 2. Add new Mumbai contacts
    added = 0
    updated = 0
    for entry in NEW_MUMBAI:
        if len(entry) == 5:
            email_raw, name, designation, category, tags = entry
        else:
            continue
        email = email_raw.strip().lower()
        if not email:
            continue
        if email in contacts:
            # Upgrade: add name/designation/tags if missing
            if not contacts[email]['name']:
                contacts[email]['name'] = name
            if not contacts[email]['designation']:
                contacts[email]['designation'] = designation
            # Merge tags
            existing_tags = set(contacts[email]['tags'].split('|')) if contacts[email]['tags'] else set()
            new_tags = set(tags.split('|')) if tags else set()
            contacts[email]['tags'] = '|'.join(sorted(existing_tags | new_tags))
            updated += 1
        else:
            contacts[email] = {
                'email':       email,
                'name':        name,
                'designation': designation,
                'category':    category,
                'tags':        tags,
                'case':        'mumbai-contacts',
                'source':      'official-directories',
            }
            added += 1

    print(f"Added {added} new Mumbai contacts, updated {updated} existing")
    print(f"Total unique contacts: {len(contacts)}")

    # 3. Sort: priority_score ASC, then category, then email
    sorted_contacts = sorted(
        contacts.values(),
        key=lambda r: (priority_score(r['tags']), r['category'], r['email'])
    )

    # 4. Write output
    out = BASE / 'contacts_tagged.csv'
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(sorted_contacts)
    print(f"Written: {out}")

    # 5. Print breakdown
    from collections import Counter
    tag_counts = Counter()
    for r in sorted_contacts:
        for t in r['tags'].split('|'):
            tag_counts[t] += 1
    print("\nContacts by tag:")
    for tag, cnt in sorted(tag_counts.items(), key=lambda x: TAG_PRIORITY.get(x[0], 10)):
        print(f"  {tag:<25} {cnt}")

    # 6. Write tag summary CSV for quick reference
    tag_summary = BASE / 'tag_summary.csv'
    with tag_summary.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['tag', 'count', 'description'])
        tag_descriptions = {
            'top-priority':  'Commissioner / DGP / ADG / Collector level — always include',
            'police-hq':     'Police HQ officers (IG, DIG, AIG, desks)',
            'police-zone':   'Zonal DCPs and ACPs',
            'police-station':'Individual Mumbai police stations (88 stations)',
            'police-special':'Specialized units (EOW, ACB, Cyber, Crime Branch)',
            'anti-corruption':'Anti-Corruption Bureau (ACB) Maharashtra',
            'economic-fraud':'Economic Offences Wing (EOW)',
            'cyber-crime':   'Cyber Crime police department',
            'anti-extortion':'Crime Branch / Anti-Extortion Cell chain',
            'crime-branch':  'Crime Branch Mumbai',
            'court-high':    'Bombay High Court',
            'court-lower':   'CMM / Magistrate courts',
            'court-sessions':'City Civil & Sessions Court',
            'court-family':  'Family Court Mumbai',
            'press':         'Journalists and media outlets',
            'govt-state':    'State government officials',
            'govt-admin':    'District administration (collectors, etc.)',
            'land-records':  'Land records, encroachment, survey officers',
            'ngo-civic':     'NGOs and civil society organizations',
            'goa':           'Goa-specific contacts (Olympio Almeida case)',
            'individual':    'Named individuals / supporters',
            'corporate':     'Corporate / company contacts',
            'dgp-desk':      'DGP Office administrative desks (bulk mail)',
            'unverified':    'Non-official domains — verify before sending',
            'general':       'Unclassified contacts',
        }
        for tag, cnt in sorted(tag_counts.items(), key=lambda x: TAG_PRIORITY.get(x[0], 10)):
            w.writerow([tag, cnt, tag_descriptions.get(tag, '')])
    print(f"Tag summary: {tag_summary}")

if __name__ == '__main__':
    main()
