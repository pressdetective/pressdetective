#!/usr/bin/env python3
"""
scripts/apply_suppression.py
CSV hygiene -- no network, no creds. Safe to run anywhere (CI, pre-push hook):
  1. De-duplicate contacts_final.csv by email (keep first occurrence)
  2. Rebuild contacts_live.csv = contacts_final - suppression_list
So contacts_live can NEVER contain a suppressed or duplicate address.

Usage:  python scripts/apply_suppression.py
"""
import csv
from pathlib import Path

ROOT  = Path(__file__).parent.parent
FINAL = ROOT / "contacts" / "contacts_final.csv"
SUPP  = ROOT / "contacts" / "suppression_list.csv"
LIVE  = ROOT / "contacts" / "contacts_live.csv"
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]


def _load(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    final = _load(FINAL)
    supp  = {r["email"].strip().lower() for r in _load(SUPP) if r.get("email")}

    seen, deduped, dups = set(), [], 0
    for r in final:
        e = (r.get("email") or "").strip().lower()
        if not e:
            continue
        if e in seen:
            dups += 1
            continue
        seen.add(e)
        deduped.append(r)

    if dups:
        with open(FINAL, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
            w.writeheader(); w.writerows(deduped)

    live = [r for r in deduped if (r.get("email") or "").strip().lower() not in supp]
    with open(LIVE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader(); w.writerows(live)

    print(f"[apply-suppression] final={len(deduped)} (removed {dups} dup) "
          f"| suppressed={len(supp)} | live={len(live)}")
    return len(deduped), len(supp), len(live)


if __name__ == "__main__":
    main()
