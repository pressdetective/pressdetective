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

def run(silent=False):
    """
    Fetch Mailtrap hard bounces and suppress invalid addresses.
    Returns (new_suppressed, total_bounces).
    Call from any campaign script or triggered automatically via pre-push hook / scheduled task.
    """
    def out(msg):
        if not silent:
            print(msg)

    token = load_creds()
    if not token:
        out("[bounce-sync] no Mailtrap token -- skipping")
        return 0, 0

    try:
        bounces = fetch_bounces(token)
    except Exception as e:
        out(f"[bounce-sync] Mailtrap API error: {e}")
        return 0, 0

    genuine = [b for b in bounces if not is_policy_block(b)]
    existing = load_suppressed()
    new_bad = [b["email"].strip().lower() for b in genuine
               if b["email"].strip().lower() not in existing]

    if not new_bad:
        out(f"[bounce-sync] {len(bounces)} total, 0 new to suppress")
        return 0, len(bounces)

    bad_set = existing | set(new_bad)
    suppress_emails(new_bad)

    b1, a1 = remove_from_csv(LIVE, bad_set)
    snap = ROOT / "clients" / "olympio-almeida" / "olympio_appeal" / "contacts_live_snapshot.csv"
    remove_from_csv(snap, bad_set)

    out(f"[bounce-sync] suppressed {len(new_bad)} new | contacts_live: {b1}->{a1}")
    return len(new_bad), len(bounces)


def main():
    dry_run = "--dry-run" in sys.argv
    print(f"Mailtrap bounce sync {'(DRY RUN) ' if dry_run else ''}-- {datetime.date.today()}")

    if dry_run:
        token = load_creds()
        if not token:
            print("ERROR: no mailtrap token"); sys.exit(1)
        bounces = fetch_bounces(token)
        genuine = [b for b in bounces if not is_policy_block(b)]
        existing = load_suppressed()
        new_bad = [b["email"].strip().lower() for b in genuine if b["email"].strip().lower() not in existing]
        print(f"Would suppress {len(new_bad)} of {len(bounces)} bounces:")
        for e in new_bad:
            print(f"  {e}")
        return

    new_n, total = run(silent=False)
    if new_n == 0 and total == 0:
        print("ERROR: could not reach Mailtrap API")
        sys.exit(1)

if __name__ == "__main__":
    main()