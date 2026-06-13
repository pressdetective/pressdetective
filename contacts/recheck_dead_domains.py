#!/usr/bin/env python3
"""
recheck_dead_domains.py
The 2026-06-12 verify_all.py run executed during a DNS outage, so many
domains marked dead_domain are false positives (lookup timed out locally).

Now that internet is back:
1. Collect all suppression_list.csv entries with reason=dead_domain
2. Re-run MX/A lookup per domain (parallel, working DNS)
3. Remove suppressions whose domain now resolves
4. Rebuild contacts_live.csv from contacts_final.csv minus suppression

Genuinely dead domains stay suppressed.
"""

import csv, sys
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import dns.resolver
except ImportError:
    print("ERROR: pip install dnspython"); sys.exit(1)

BASE         = Path(__file__).parent.parent
FINAL_CSV    = BASE / "contacts" / "contacts_final.csv"
LIVE_CSV     = BASE / "contacts" / "contacts_live.csv"
SUPPRESS_CSV = BASE / "contacts" / "suppression_list.csv"

# Use public resolvers in case the router DNS is still flaky
resolver = dns.resolver.Resolver()
resolver.nameservers = ["8.8.8.8", "1.1.1.1"]
resolver.lifetime = 8


def domain_alive(domain: str) -> bool:
    try:
        resolver.resolve(domain, "MX")
        return True
    except Exception:
        pass
    try:
        resolver.resolve(domain, "A")
        return True
    except Exception:
        return False


def main():
    rows = list(csv.DictReader(SUPPRESS_CSV.open(encoding="utf-8-sig")))
    print(f"Suppression entries: {len(rows)}")

    dead = [r for r in rows if r.get("reason", "") == "dead_domain"]
    domains = sorted({r["email"].split("@")[1].lower() for r in dead if "@" in r["email"]})
    print(f"dead_domain entries: {len(dead)} across {len(domains)} unique domains")
    print("Re-checking with 8.8.8.8 / 1.1.1.1 ...\n")

    alive = set()
    checked = 0
    with ThreadPoolExecutor(max_workers=25) as pool:
        futures = {pool.submit(domain_alive, d): d for d in domains}
        for fut in as_completed(futures):
            d = futures[fut]
            checked += 1
            if fut.result():
                alive.add(d)
                print(f"  ALIVE   {d}")
            if checked % 50 == 0:
                print(f"  ... {checked}/{len(domains)} checked, {len(alive)} alive so far")

    print(f"\nDomains re-checked : {len(domains)}")
    print(f"Actually alive     : {len(alive)}")
    print(f"Confirmed dead     : {len(domains) - len(alive)}")

    # Drop suppressions whose domain is alive
    keep, recovered = [], []
    for r in rows:
        e = r.get("email", "").lower()
        if r.get("reason") == "dead_domain" and "@" in e and e.split("@")[1] in alive:
            recovered.append(e)
        else:
            keep.append(r)

    print(f"Suppressions recovered (removed): {len(recovered)}")
    print(f"Suppression list after          : {len(keep)}")

    with SUPPRESS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["email", "reason", "date", "source"], extrasaction="ignore")
        w.writeheader()
        w.writerows(keep)

    # Rebuild live
    suppressed = {r["email"].strip().lower() for r in keep}
    all_rows = list(csv.DictReader(FINAL_CSV.open(encoding="utf-8-sig")))
    fieldnames = list(all_rows[0].keys())
    live = [r for r in all_rows if r.get("email", "").strip().lower() not in suppressed]
    with LIVE_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(live)

    print(f"\ncontacts_final.csv : {len(all_rows)} rows")
    print(f"contacts_live.csv  : {len(live)} rows (rebuilt)")

    tag_cnt = Counter()
    for r in live:
        for t in (r.get("tags") or "").split("|"):
            if t.strip():
                tag_cnt[t.strip()] += 1
    print("\nTop tags in live list:")
    for t, c in tag_cnt.most_common(15):
        print(f"  {t:<30} {c}")


if __name__ == "__main__":
    main()
