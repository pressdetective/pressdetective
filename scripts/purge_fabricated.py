#!/usr/bin/env python3
"""
scripts/purge_fabricated.py
One-shot proactive cleanup (run 21 Jun 2026) -- complements the ground-truth
Proton DSN bounce sync by suppressing addresses that WILL bounce before they do:

  A. KNOWN_BAD_DOMAINS  -- confirmed always-bouncing / dead domains (Times Group
     infra, DNA print). Pattern-guessed reporter addresses on these never deliver.
  B. FABRICATED_SOURCES -- bulk-expansion sources confirmed/flagged as fabricated
     (expand_goa_press = confirmed; mumbai_expansion_2026 = research-flagged:
     DNA dead, names not in mastheads). Only the generated firstname.lastname
     addresses are suppressed; real role addresses (info@/editor@/desk@) are kept.

Rows are SUPPRESSED (added to suppression_list, removed from contacts_live) but
LEFT in contacts_final -- so it's fully reversible. Real harvested (.mbm) and
verified-research contacts are never touched.
"""
import csv, re, datetime
from pathlib import Path

ROOT  = Path(__file__).parent.parent
FINAL = ROOT / "contacts" / "contacts_final.csv"
SUPP  = ROOT / "contacts" / "suppression_list.csv"
LIVE  = ROOT / "contacts" / "contacts_live.csv"
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]

KNOWN_BAD_DOMAINS = {"timesgroup.com","timesofindia.com","timesinternet.in","dnaindia.com"}
FABRICATED_SOURCES = {"contacts/expand_goa_press.py", "mumbai_expansion_2026"}

ROLE = {"info","editor","news","desk","contact","mail","admin","office","crime","city",
        "web","webeditor","online","advt","advertising","circulation","marketing","sales",
        "grievance","letters","feedback","editorial","reception","support","general","press",
        "media","reporter","newsdesk","help","hello","enquiry","enquiries","secretary","chief",
        "bureau"}


def is_generated_name(localpart):
    parts = re.split(r"[._]", localpart.lower())
    return (len(parts) >= 2
            and all(re.fullmatch(r"[a-z]+[0-9]*", p) for p in parts)
            and not any(p in ROLE for p in parts))


def load(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    final = load(FINAL)
    supp_rows = load(SUPP)
    suppressed = {r["email"].strip().lower() for r in supp_rows if r.get("email")}

    to_suppress = {}   # email -> reason
    for r in final:
        e = (r.get("email") or "").strip().lower()
        if not e or e in suppressed:
            continue
        domain = e.split("@", 1)[1] if "@" in e else ""
        local  = e.split("@", 1)[0]
        if domain in KNOWN_BAD_DOMAINS:
            to_suppress[e] = f"known_bad_domain:{domain}"
        elif r.get("source", "") in FABRICATED_SOURCES and is_generated_name(local):
            to_suppress[e] = "fabricated_bulk_source"

    if not to_suppress:
        print("[purge] nothing to suppress")
        return

    today = datetime.date.today().isoformat()
    with open(SUPP, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for e, reason in sorted(to_suppress.items()):
            w.writerow([e, reason, today, "purge_fabricated_21jun"])

    # rebuild live
    suppressed |= set(to_suppress)
    live = [r for r in final if (r.get("email") or "").strip().lower() not in suppressed]
    with open(LIVE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader(); w.writerows(live)

    from collections import Counter
    by_reason = Counter(v.split(":")[0] for v in to_suppress.values())
    print(f"[purge] suppressed {len(to_suppress)} rows:")
    for k, n in by_reason.most_common():
        print(f"   {k}: {n}")
    print(f"[purge] contacts_live now {len(live)}")


if __name__ == "__main__":
    main()
