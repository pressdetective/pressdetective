"""
Apply Olympio/Proton confirmed-dead bounces (14 June 2026) to the contacts DB.
MUST be run while checked out on the `contacts` branch.

- Appends 128 confirmed-dead addresses to contacts/suppression_list.csv
- Removes them from contacts/contacts_live.csv
- Writes audit of removed rows to contacts/removed_olympio_14june.csv

Does NOT touch the 36 policy-blocked govt addresses or 22 transient outlets.
"""
import csv, json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent.parent.parent.parent
SUP  = json.loads((ROOT / "clients/olympio-almeida/olympio_appeal/suppress_14june.json").read_text())
DATE = "2026-06-14"
SOURCE = "olympio_proton_bounce"

CONTACTS = ROOT / "contacts"
sup_csv  = CONTACTS / "suppression_list.csv"
live_csv = CONTACTS / "contacts_live.csv"

assert sup_csv.exists() and live_csv.exists(), "Run this ON the contacts branch (files missing)"

# 1) append to suppression_list.csv (dedup by email)
existing = {}
with sup_csv.open(encoding="utf-8-sig") as f:
    rd = csv.DictReader(f)
    sup_fields = rd.fieldnames
    for r in rd:
        existing[r["email"].strip().lower()] = r
added = 0
for email, reason in SUP.items():
    e = email.strip().lower()
    if e not in existing:
        existing[e] = {"email": e, "reason": reason, "date": DATE, "source": SOURCE}
        added += 1
with sup_csv.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=sup_fields, extrasaction="ignore")
    w.writeheader()
    for r in existing.values():
        w.writerow(r)
print(f"suppression_list.csv: +{added} new (total {len(existing)})")

# 2) remove from contacts_live.csv
supset = set(e.strip().lower() for e in SUP)
with live_csv.open(encoding="utf-8-sig") as f:
    rd = csv.DictReader(f)
    live_fields = rd.fieldnames
    rows = list(rd)
keep, removed = [], []
for r in rows:
    if r.get("email","").strip().lower() in supset:
        removed.append(r)
    else:
        keep.append(r)

with live_csv.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=live_fields, extrasaction="ignore")
    w.writeheader(); w.writerows(keep)

audit = CONTACTS / "removed_olympio_14june.csv"
with audit.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=live_fields, extrasaction="ignore")
    w.writeheader(); w.writerows(removed)

print(f"contacts_live.csv: {len(rows)} -> {len(keep)} (removed {len(removed)})")
print(f"Audit: removed_olympio_14june.csv ({len(removed)} rows)")
# how many suppressed addresses weren't in live (already absent / from institutional list only)
print(f"Suppressed not present in live: {len(supset) - len(removed)}")
cats = Counter(r.get("category","") for r in removed)
print("Removed by category:", dict(cats))
