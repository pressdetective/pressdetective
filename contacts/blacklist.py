#!/usr/bin/env python3
"""
Blacklist / suppression list manager for PressDetective.

Maintains contacts/suppression_list.csv.
Sources of suppression:
  - ZeptoMail bounce exports (CSV or pasted list)
  - Manual unsubscribe requests
  - SMTP "user not found" confirmed bounces
  - Dead domains (no MX)

Usage:
    # Add one address manually
    python -m contacts.blacklist add someone@example.com "manual"

    # Import a ZeptoMail bounce CSV export
    python -m contacts.blacklist import zepto_bounces.csv

    # Show stats
    python -m contacts.blacklist stats

    # Clean contacts_final.csv against the blacklist
    python -m contacts.blacklist clean
"""

import csv, sys, re, datetime
from pathlib import Path
from collections import Counter

BASE          = Path(__file__).parent.parent
SUPPRESS_CSV  = BASE / "contacts" / "suppression_list.csv"
CONTACTS_CSV  = BASE / "contacts" / "contacts_final.csv"
LIVE_CSV      = BASE / "contacts" / "contacts_live.csv"

FIELDNAMES = ["email", "reason", "date", "source"]
EMAIL_RE   = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")


# ── Core helpers ──────────────────────────────────────────────────────────────

def load_suppression() -> dict:
    """Returns {email: {reason, date, source}}"""
    if not SUPPRESS_CSV.exists():
        return {}
    with SUPPRESS_CSV.open(encoding="utf-8-sig") as f:
        return {
            row["email"].strip().lower(): row
            for row in csv.DictReader(f)
            if row.get("email")
        }


def save_suppression(records: dict):
    SUPPRESS_CSV.parent.mkdir(exist_ok=True)
    with SUPPRESS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        w.writeheader()
        for email, row in sorted(records.items()):
            row["email"] = email
            w.writerow(row)


def add_to_blacklist(email: str, reason: str = "manual", source: str = ""):
    email = email.strip().lower()
    if not EMAIL_RE.match(email):
        print(f"  [SKIP] invalid email: {email}")
        return False
    records = load_suppression()
    if email in records:
        print(f"  [EXISTS] {email} already suppressed")
        return False
    records[email] = {
        "email":  email,
        "reason": reason,
        "date":   datetime.date.today().isoformat(),
        "source": source,
    }
    save_suppression(records)
    print(f"  [ADDED] {email}  ({reason})")
    return True


def bulk_add(emails: list[str], reason: str, source: str = "") -> int:
    records = load_suppression()
    added = 0
    today = datetime.date.today().isoformat()
    for email in emails:
        email = email.strip().lower()
        if not email or not EMAIL_RE.match(email):
            continue
        if email not in records:
            records[email] = {"email": email, "reason": reason,
                              "date": today, "source": source}
            added += 1
    save_suppression(records)
    return added


# ── Import from ZeptoMail bounce CSV ─────────────────────────────────────────

def import_bounce_csv(path: Path) -> tuple[int, int]:
    """
    Parse any ZeptoMail bounce export CSV.
    Columns vary; we scan every cell for email addresses.
    Also categorises reasons: user_not_found, domain_not_found, spam, etc.
    Returns (added, skipped).
    """
    emails_reasons = []
    with path.open(encoding="utf-8-sig", errors="replace") as f:
        try:
            dialect = csv.Sniffer().sniff(f.read(4096)); f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)
        except Exception:
            f.seek(0)
            reader = csv.DictReader(f)

        for row in reader:
            row_lower = {k.lower(): v for k, v in row.items() if k}
            email = ""
            for col in ("email", "recipient", "address", "to", "email address"):
                if col in row_lower and EMAIL_RE.match((row_lower[col] or "").strip()):
                    email = row_lower[col].strip().lower()
                    break
            if not email:
                # scan all cells
                for v in row.values():
                    m = EMAIL_RE.search(v or "")
                    if m:
                        email = m.group(0).lower()
                        break
            if not email:
                continue

            # Determine reason from bounce category/description columns
            reason_raw = (
                row_lower.get("bounce type") or
                row_lower.get("bounce_type") or
                row_lower.get("category") or
                row_lower.get("reason") or
                row_lower.get("description") or
                ""
            ).lower()

            if "user not found" in reason_raw or "550" in reason_raw or "does not exist" in reason_raw:
                reason = "user_not_found"
            elif "domain" in reason_raw and ("not found" in reason_raw or "invalid" in reason_raw):
                reason = "domain_not_found"
            elif "spam" in reason_raw:
                reason = "spam_rejection"
            elif "policy" in reason_raw or "blocked" in reason_raw:
                reason = "policy_failure"
            elif "host" in reason_raw and "reachable" not in reason_raw:
                reason = "host_not_reachable"
            else:
                reason = "bounce_" + reason_raw[:30].replace(" ", "_") if reason_raw else "bounce"

            emails_reasons.append((email, reason))

    if not emails_reasons:
        print(f"  No emails found in {path.name}")
        return 0, 0

    records = load_suppression()
    added, skipped = 0, 0
    today = datetime.date.today().isoformat()
    for email, reason in emails_reasons:
        if email in records:
            skipped += 1
        else:
            records[email] = {"email": email, "reason": reason,
                              "date": today, "source": path.name}
            added += 1
    save_suppression(records)
    print(f"  Imported: {added} added, {skipped} already suppressed  (from {path.name})")
    return added, skipped


# ── Clean contacts against blacklist ─────────────────────────────────────────

def clean_contacts(dry_run: bool = False) -> tuple[int, int]:
    """
    Remove suppressed addresses from contacts_final.csv → contacts_live.csv.
    Returns (kept, removed).
    """
    if not CONTACTS_CSV.exists():
        print(f"  {CONTACTS_CSV} not found"); return 0, 0

    suppressed = load_suppression()
    rows       = list(csv.DictReader(CONTACTS_CSV.open(encoding="utf-8-sig")))
    kept, removed = [], []

    for row in rows:
        if row["email"].strip().lower() in suppressed:
            removed.append(row)
        else:
            kept.append(row)

    if not dry_run:
        fieldnames = list(rows[0].keys()) if rows else []
        with LIVE_CSV.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            w.writeheader()
            w.writerows(kept)

    action = "Would remove" if dry_run else "Removed"
    print(f"  {action}: {len(removed)}  |  Live contacts: {len(kept)}")

    if removed:
        by_reason = Counter(
            suppressed[r["email"].lower()]["reason"] for r in removed
        )
        print("  Breakdown:")
        for reason, cnt in by_reason.most_common():
            print(f"    {reason:<35} {cnt}")

    return len(kept), len(removed)


# ── Stats ─────────────────────────────────────────────────────────────────────

def show_stats():
    records = load_suppression()
    if not records:
        print("Suppression list is empty.")
        return
    by_reason = Counter(r["reason"] for r in records.values())
    print(f"\nSuppression list: {len(records)} addresses\n")
    print(f"{'Reason':<35} {'Count':>6}")
    print("-" * 43)
    for reason, cnt in by_reason.most_common():
        print(f"  {reason:<33} {cnt:>6}")

    if CONTACTS_CSV.exists():
        rows = list(csv.DictReader(CONTACTS_CSV.open(encoding="utf-8-sig")))
        blocked = sum(1 for r in rows if r["email"].lower() in records)
        print(f"\nOf {len(rows)} contacts in contacts_final.csv: {blocked} are suppressed")
        print(f"Send-ready: {len(rows) - blocked}")


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"

    if cmd == "add":
        email  = sys.argv[2] if len(sys.argv) > 2 else ""
        reason = sys.argv[3] if len(sys.argv) > 3 else "manual"
        if email:
            add_to_blacklist(email, reason)
        else:
            print("Usage: blacklist add <email> [reason]")

    elif cmd == "import":
        path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        if path and path.exists():
            import_bounce_csv(path)
        else:
            print("Usage: blacklist import <bounce_export.csv>")

    elif cmd == "clean":
        dry = "--dry" in sys.argv
        clean_contacts(dry_run=dry)

    elif cmd == "stats":
        show_stats()

    else:
        print(__doc__)
