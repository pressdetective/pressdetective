#!/usr/bin/env python3
"""
dedupe_contacts.py
Collapse duplicate email addresses in contacts_final.csv (case-insensitive).
When merging duplicates:
  - keep the longest non-empty name / designation / category / mobile
  - UNION all tags (pipe-separated) so no sorting/segment info is lost
  - keep the first non-'general' case, else 'general'
  - keep the first source, append others
Then rebuild contacts_live.csv = final minus suppression_list.csv.
"""

import csv
from pathlib import Path
from collections import OrderedDict

ROOT      = Path(__file__).parent.parent
FINAL_CSV = ROOT / "contacts" / "contacts_final.csv"
LIVE_CSV  = ROOT / "contacts" / "contacts_live.csv"
SUPP_CSV  = ROOT / "contacts" / "suppression_list.csv"
HEADER    = ["email","name","designation","category","tags","case","source","mobile"]


def longest(a, b):
    a, b = (a or "").strip(), (b or "").strip()
    return a if len(a) >= len(b) else b


def merge(dst, src):
    dst["name"]        = longest(dst["name"], src.get("name"))
    dst["designation"] = longest(dst["designation"], src.get("designation"))
    dst["category"]    = longest(dst["category"], src.get("category"))
    dst["mobile"]      = longest(dst.get("mobile",""), src.get("mobile"))
    # union tags
    tags = [t.strip() for t in (dst["tags"].split("|") + src.get("tags","").split("|")) if t.strip()]
    seen, uniq = set(), []
    for t in tags:
        if t.lower() not in seen:
            seen.add(t.lower()); uniq.append(t)
    dst["tags"] = "|".join(uniq)
    # case: prefer a specific (non-general) case
    if (dst.get("case","general") or "general").lower() == "general" and \
       (src.get("case","") or "").strip() and src["case"].lower() != "general":
        dst["case"] = src["case"]
    # source: keep union (comma)
    srcs = [s.strip() for s in (dst.get("source","").split(",") + [src.get("source","")]) if s.strip()]
    dst["source"] = ",".join(OrderedDict.fromkeys(srcs))
    return dst


def main():
    rows = list(csv.DictReader(FINAL_CSV.open(encoding="utf-8-sig")))
    print(f"contacts_final.csv input rows: {len(rows)}")

    merged = OrderedDict()  # email_lower -> row
    dup_count = 0
    for r in rows:
        e = r.get("email","").strip().lower()
        if not e:
            continue
        # normalise to full header
        row = {k: (r.get(k,"") or "").strip() for k in HEADER}
        row["email"] = e
        if e in merged:
            merge(merged[e], row)
            dup_count += 1
        else:
            merged[e] = row

    print(f"Duplicates collapsed: {dup_count}")
    print(f"Unique contacts     : {len(merged)}")

    out = list(merged.values())
    with FINAL_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, extrasaction="ignore")
        w.writeheader(); w.writerows(out)
    print(f"contacts_final.csv rewritten -> {len(out)} rows")

    # Rebuild live
    suppressed = set()
    if SUPP_CSV.exists():
        for r in csv.DictReader(SUPP_CSV.open(encoding="utf-8-sig")):
            e = r.get("email","").strip().lower()
            if e: suppressed.add(e)
    live = [r for r in out if r["email"] not in suppressed]
    with LIVE_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, extrasaction="ignore")
        w.writeheader(); w.writerows(live)
    print(f"contacts_live.csv rewritten -> {len(live)} rows (suppressed {len(out)-len(live)})")

    # integrity
    from collections import Counter
    dups = [e for e,c in Counter(r["email"] for r in live).items() if c>1]
    leaked = [r["email"] for r in live if r["email"] in suppressed]
    print(f"\nINTEGRITY: dup emails in live: {len(dups)} | suppressed leaked: {len(leaked)}")


if __name__ == "__main__":
    main()
