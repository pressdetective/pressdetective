#!/usr/bin/env python3
"""
Strip ZeptoMail bounce exports from contacts_final.csv.

Usage:
    python apply_bounces.py <bounce_export.csv>

The bounce CSV from ZeptoMail dashboard has at minimum an "email" column.
Columns vary by export format — we auto-detect the email column.

Reads:  contacts_final.csv  (3,170 contacts)
Writes: contacts_live.csv   (bounced addresses removed)
        contacts_bounced.csv (removed entries, for audit)
"""

import csv, sys, re
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

def extract_emails_from_csv(path: Path) -> set:
    """Extract all emails from any CSV — scans every cell, tolerant of column name variations."""
    found = set()
    with path.open(encoding='utf-8-sig', errors='replace') as f:
        try:
            dialect = csv.Sniffer().sniff(f.read(2048))
            f.seek(0)
            reader = csv.reader(f, dialect)
        except Exception:
            f.seek(0)
            reader = csv.reader(f)
        for row in reader:
            for cell in row:
                m = EMAIL_RE.search(cell)
                if m:
                    found.add(m.group(0).lower())
    return found


def main():
    if len(sys.argv) < 2:
        print("Usage: python apply_bounces.py <zepto_bounce_export.csv>")
        print("       (also accepts multiple files: python apply_bounces.py f1.csv f2.csv)")
        sys.exit(1)

    bounce_files = [Path(a) for a in sys.argv[1:]]
    for bf in bounce_files:
        if not bf.exists():
            print(f"ERROR: {bf} not found"); sys.exit(1)

    # Collect all bounced addresses
    bounced = set()
    for bf in bounce_files:
        extracted = extract_emails_from_csv(bf)
        print(f"  {bf.name}: {len(extracted)} emails extracted")
        bounced |= extracted
    print(f"\nTotal unique bounced addresses: {len(bounced)}")

    # Load contacts
    src = BASE / 'contacts_final.csv'
    if not src.exists():
        src = BASE / 'contacts_clean.csv'
    rows = list(csv.DictReader(src.open(encoding='utf-8-sig')))
    print(f"Input contacts: {len(rows)}")

    live, removed = [], []
    for row in rows:
        if row['email'].lower() in bounced:
            removed.append(row)
        else:
            live.append(row)

    fieldnames = list(rows[0].keys())

    out_live = BASE / 'contacts_live.csv'
    out_removed = BASE / 'contacts_bounced.csv'

    with out_live.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader()
        w.writerows(live)

    with out_removed.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader()
        w.writerows(removed)

    # Tag breakdown of what was removed
    tag_counts = Counter()
    for r in removed:
        for t in r.get('tags', '').split('|'):
            if t:
                tag_counts[t] += 1

    domain_counts = Counter(r['email'].split('@')[1] for r in removed)

    print(f"\n{'='*50}")
    print(f"Input:   {len(rows)}")
    print(f"Removed: {len(removed)}  ({100*len(removed)/len(rows):.1f}%)")
    print(f"Live:    {len(live)}")
    print(f"\nRemoved by tag:")
    for tag, cnt in tag_counts.most_common(15):
        print(f"  {tag:<25} {cnt}")
    print(f"\nTop removed domains:")
    for dom, cnt in domain_counts.most_common(20):
        print(f"  {dom}: {cnt}")
    print(f"\nLive contacts written to: contacts_live.csv")


if __name__ == '__main__':
    main()
