#!/usr/bin/env python3
"""
scripts/sync_postmark_bounces.py
Pull hard bounces + spam complaints from the Postmark Bounces API and suppress them.
Cloud-safe -- needs only POSTMARK_TOKEN (env var, or .creds/proton_accounts.json).
Used by the deliverability.yml GitHub Action and the pre-push hook.

Usage:
    POSTMARK_TOKEN=xxxx python scripts/sync_postmark_bounces.py [--dry-run]
"""
import os, sys, csv, json, datetime, urllib.request
from pathlib import Path

ROOT  = Path(__file__).parent.parent
CREDS = ROOT / ".creds" / "proton_accounts.json"
SUPP  = ROOT / "contacts" / "suppression_list.csv"
FINAL = ROOT / "contacts" / "contacts_final.csv"
LIVE  = ROOT / "contacts" / "contacts_live.csv"
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]

API = "https://api.postmarkapp.com/bounces"
# Postmark bounce types that mean "never send here again"
SUPPRESS_TYPES = {"HardBounce", "SpamComplaint", "BadEmailAddress",
                  "ManuallyDeactivated", "SpamNotification", "Blocked"}


def _token():
    t = os.environ.get("POSTMARK_TOKEN", "")
    if t:
        return t
    if CREDS.exists():
        return json.loads(CREDS.read_text(encoding="utf-8-sig")).get("smtp_postmark", {}).get("token", "")
    return ""


def _fetch_all(tok):
    out, offset, count = [], 0, 500
    while True:
        req = urllib.request.Request(
            f"{API}?count={count}&offset={offset}",
            headers={"Accept": "application/json", "X-Postmark-Server-Token": tok})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        batch = data.get("Bounces", [])
        out.extend(batch)
        offset += count
        if offset >= data.get("TotalCount", 0) or not batch:
            break
    return out


def _load_suppressed():
    if not SUPP.exists():
        return set()
    with open(SUPP, encoding="utf-8-sig") as f:
        return {r["email"].strip().lower() for r in csv.DictReader(f) if r.get("email")}


def _rebuild_live():
    if not FINAL.exists():
        return 0
    final = list(csv.DictReader(open(FINAL, encoding="utf-8-sig")))
    supp  = _load_suppressed()
    live  = [r for r in final if (r.get("email") or "").strip().lower() not in supp]
    with open(LIVE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader(); w.writerows(live)
    return len(live)


def run(silent=False, dry_run=False):
    def out(m):
        if not silent: print(m)
    tok = _token()
    if not tok:
        out("[postmark-bounce] no token -- skipping"); return 0, 0
    try:
        bounces = _fetch_all(tok)
    except Exception as e:
        out(f"[postmark-bounce] API error: {e}"); return 0, 0

    bad = {b["Email"].strip().lower() for b in bounces
           if b.get("Type") in SUPPRESS_TYPES and b.get("Email")}
    existing = _load_suppressed()
    new = sorted(b for b in bad if b not in existing)

    if dry_run:
        out(f"[postmark-bounce] DRY: would suppress {len(new)} of {len(bounces)} bounces")
        for e in new:
            out(f"  {e}")
        return 0, len(bounces)

    if new:
        today = datetime.date.today().isoformat()
        with open(SUPP, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            for e in new:
                w.writerow([e, "postmark_hard_bounce", today, "postmark_api"])
        n = _rebuild_live()
        out(f"[postmark-bounce] suppressed {len(new)} new | contacts_live now {n}")
    else:
        out(f"[postmark-bounce] {len(bounces)} bounces, 0 new to suppress")
    return len(new), len(bounces)


if __name__ == "__main__":
    run(silent=False, dry_run="--dry-run" in sys.argv)
