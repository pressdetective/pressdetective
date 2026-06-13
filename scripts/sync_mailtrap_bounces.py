#!/usr/bin/env python3
"""
scripts/sync_mailtrap_bounces.py
Run after any campaign to pull hard bounces from Mailtrap and auto-suppress.

Usage:
    python scripts/sync_mailtrap_bounces.py [--dry-run]
"""
import sys, csv, datetime, urllib.request, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

ROOT  = Path(__file__).parent.parent
SUPP  = ROOT / "contacts" / "suppression_list.csv"
LIVE  = ROOT / "contacts" / "contacts_live.csv"

def load_creds():
    creds_file = ROOT / ".creds" / "proton_accounts.json"
    if creds_file.exists():
        with open(creds_file, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("smtp_mailtrap", {}).get("token", "")
    return ""

def fetch_bounces(token):
    req = urllib.request.Request(
        "https://mailtrap.io/api/suppressions",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def is_policy_block(b):
    """Distinguish sender-reputation blocks (valid address) from invalid addresses."""
    esp = b.get("message_esp_response", "").lower()
    return "access denied" in esp and "5.4.1" in esp

def load_suppressed():
    if not SUPP.exists():
        return set()
    with open(SUPP, encoding="utf-8-sig") as f:
        return {row["email"].strip().lower() for row in csv.DictReader(f) if row.get("email")}

def suppress_emails(emails, reason="mailtrap_hard_bounce"):
    today = datetime.date.today().isoformat()
    with open(SUPP, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for email in emails:
            w.writerow([email, reason, today, "mailtrap_api"])

def remove_from_csv(path, bad_emails):
    if not path.exists():
        return 0, 0
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    before = len(rows)
    clean = [r for r in rows if r.get("email","").strip().lower() not in bad_emails]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(clean)
    return before, len(clean)

def main():
    dry_run = "--dry-run" in sys.argv
    print(f"Mailtrap bounce sync {'(DRY RUN) ' if dry_run else ''}-- {datetime.date.today()}")

    token = load_creds()
    if not token:
        print("ERROR: no mailtrap token in .creds/proton_accounts.json")
        sys.exit(1)

    bounces = fetch_bounces(token)
    print(f"Mailtrap suppressions: {len(bounces)} total")

    genuine = [b for b in bounces if not is_policy_block(b)]
    blocked = [b for b in bounces if is_policy_block(b)]
    print(f"  Invalid mailboxes:    {len(genuine)} (will suppress)")
    print(f"  Policy blocks (keep): {len(blocked)}")
    if blocked:
        for b in blocked:
            print(f"    KEEP {b['email']}  -- server blocked, address is valid")

    existing = load_suppressed()
    new_bad = [b["email"].strip().lower() for b in genuine
               if b["email"].strip().lower() not in existing]
    print(f"  New suppressions:     {len(new_bad)}")

    if not new_bad:
        print("Nothing new to suppress.")
        return

    if dry_run:
        print("DRY RUN -- would suppress:")
        for e in new_bad:
            print(f"  {e}")
        return

    bad_set = existing | set(new_bad)
    suppress_emails(new_bad)

    b1, a1 = remove_from_csv(LIVE, bad_set)
    print(f"contacts_live.csv:  {b1} -> {a1}  ({b1-a1} removed)")

    snap = ROOT / "clients" / "olympio-almeida" / "olympio_appeal" / "contacts_live_snapshot.csv"
    b2, a2 = remove_from_csv(snap, bad_set)
    if b2:
        print(f"olympio snapshot:   {b2} -> {a2}  ({b2-a2} removed)")

    print(f"\nDone. Run after every campaign to keep lists clean.")

if __name__ == "__main__":
    main()