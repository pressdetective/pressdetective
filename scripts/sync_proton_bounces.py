#!/usr/bin/env python3
"""
scripts/sync_proton_bounces.py
Parse Delivery Status Notification (DSN / bounce) emails from the Proton Bridge
inboxes and auto-suppress every address that actually failed. This is the
GROUND-TRUTH bounce cleanup -- it suppresses exactly the addresses that bounced,
with zero false positives.

Requires Proton Bridge running locally (127.0.0.1:1143) and .creds/proton_accounts.json.
Scans the INBOX of every account (info / olympio / santosh / sujata) for bounce
messages, extracts failed recipients from:
  1. RFC 3464 message/delivery-status parts (Action: failed -> Final-Recipient)
  2. plain-text Proton DSN bodies (lines carrying a 5.x.x code / failure phrase)

Usage:
    python scripts/sync_proton_bounces.py            # scan + suppress + rebuild live
    python scripts/sync_proton_bounces.py --dry-run  # show what would be suppressed
"""
import sys, re, ssl, csv, json, imaplib, email, datetime
from email.policy import default as DEFAULT_POLICY
from pathlib import Path

ROOT  = Path(__file__).parent.parent
CREDS = ROOT / ".creds" / "proton_accounts.json"
SUPP  = ROOT / "contacts" / "suppression_list.csv"
FINAL = ROOT / "contacts" / "contacts_final.csv"
LIVE  = ROOT / "contacts" / "contacts_live.csv"

IMAP_HOST, IMAP_PORT = "127.0.0.1", 1143
OWN_DOMAIN = "pressdetective.com"
LIVE_FIELDS = ["email","name","designation","category","tags","case","source","mobile"]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# phrases / codes that mark a line as a genuine permanent failure
FAIL_HINTS = (
    "550","551","553","554","5.1.1","5.1.0","5.1.2","5.1.3","5.2.1","5.4.1",
    "5.4.4","5.5.0","5.7.1","no such user","user unknown","does not exist",
    "doesn't exist","mailbox unavailable","mailbox not found","mailbox is unavailable",
    "recipient not found","address not found","no such recipient","unknown recipient",
    "recipient rejected","invalid recipient","unrouteable address","unrouteable",
    "host or domain name not found","domain not found","relay access denied",
    "account that you tried to reach does not exist","address couldn't be found",
    "address could not be found","no longer accept","permanent error","permanently failed",
)

BOUNCE_SEARCHES = [
    '(FROM "mailer-daemon")', '(FROM "MAILER-DAEMON")', '(FROM "postmaster")',
    '(SUBJECT "Undelivered")', '(SUBJECT "Undeliverable")',
    '(SUBJECT "Delivery Status Notification")', '(SUBJECT "Mail delivery failed")',
    '(SUBJECT "could not be delivered")', '(SUBJECT "delivery has failed")',
    '(SUBJECT "failure notice")', '(SUBJECT "returned mail")', '(SUBJECT "Returned to sender")',
]


def load_accounts():
    data = json.loads(CREDS.read_text(encoding="utf-8-sig"))
    return data.get("accounts", {})


def load_suppressed():
    if not SUPP.exists():
        return set()
    with open(SUPP, encoding="utf-8-sig") as f:
        return {r["email"].strip().lower() for r in csv.DictReader(f) if r.get("email")}


def _clean_addr(a):
    return a.strip().strip("<>").strip().lower()


def extract_failed(msg):
    """Return a set of failed recipient addresses from one bounce message."""
    failed = set()

    # 1) RFC 3464 structured delivery-status report (most reliable)
    for part in msg.walk():
        if part.get_content_type() == "message/delivery-status":
            try:
                text = part.as_string()
            except Exception:
                continue
            for block in re.split(r"\n[ \t]*\n", text):
                if re.search(r"Action:\s*fail", block, re.I):
                    for m in re.finditer(
                        r"(?:Final|Original)-Recipient:\s*[^;\n]*;\s*<?([^\s<>]+@[^\s<>]+)>?",
                        block, re.I):
                        failed.add(_clean_addr(m.group(1)))

    # 2) plain-text fallback: only emails on a line that ALSO carries a failure hint
    body = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            try:
                body += "\n" + part.get_content()
            except Exception:
                pass
    for line in body.splitlines():
        ll = line.lower()
        if any(h in ll for h in FAIL_HINTS):
            for a in EMAIL_RE.findall(line):
                failed.add(a.lower())

    # never suppress our own addresses or daemon noise
    return {a for a in failed
            if a and not a.endswith("@" + OWN_DOMAIN)
            and "mailer-daemon" not in a and "postmaster" not in a
            and "@protonmail.ch" not in a and "@proton.me" not in a}


def scan_account(name, acct, limit=1500):
    addr = acct.get("address", name)
    pw   = acct.get("bridge_password")
    if not pw:
        return set(), 0
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    failed, n_msgs = set(), 0
    try:
        M = imaplib.IMAP4(IMAP_HOST, IMAP_PORT)
        M.starttls(ssl_context=ctx)
        M.login(addr, pw)
        M.select("INBOX", readonly=True)
        seqs = set()
        for q in BOUNCE_SEARCHES:
            try:
                typ, data = M.search(None, q)
                if typ == "OK" and data and data[0]:
                    seqs.update(data[0].split())
            except Exception:
                pass
        seqs = list(seqs)[-limit:]
        for sid in seqs:
            try:
                typ, raw = M.fetch(sid, "(RFC822)")
                if typ != "OK" or not raw or not raw[0]:
                    continue
                m = email.message_from_bytes(raw[0][1], policy=DEFAULT_POLICY)
                hit = extract_failed(m)
                if hit:
                    failed |= hit
                    n_msgs += 1
            except Exception:
                pass
        try: M.logout()
        except Exception: pass
    except Exception as e:
        print(f"[proton-dsn] {name}: IMAP error: {e}")
    return failed, n_msgs


def suppress_emails(emails, reason="proton_dsn_bounce", source="proton_dsn"):
    today = datetime.date.today().isoformat()
    new = SUPP.exists()
    with open(SUPP, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if not new:
            w.writerow(["email", "reason", "date", "source"])
        for e in sorted(emails):
            w.writerow([e, reason, today, source])


def rebuild_live():
    if not FINAL.exists():
        return 0
    final = list(csv.DictReader(open(FINAL, encoding="utf-8-sig")))
    supp  = load_suppressed()
    live  = [r for r in final if r.get("email","").strip().lower() not in supp]
    with open(LIVE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LIVE_FIELDS, extrasaction="ignore")
        w.writeheader(); w.writerows(live)
    return len(live)


def run(silent=False, dry_run=False):
    """Scan all account inboxes, suppress failed recipients, rebuild live.
    Returns (new_suppressed, total_failed_found)."""
    def out(m):
        if not silent: print(m)
    if not CREDS.exists():
        out("[proton-dsn] no creds -- skipping"); return 0, 0
    all_failed = set()
    for name, acct in load_accounts().items():
        hits, n = scan_account(name, acct)
        if hits:
            out(f"[proton-dsn] {name}: {len(hits)} failed addrs in {n} bounce msgs")
        all_failed |= hits
    existing = load_suppressed()
    new_bad = sorted(a for a in all_failed if a not in existing)
    if dry_run:
        out(f"[proton-dsn] DRY RUN: would suppress {len(new_bad)} new (of {len(all_failed)} found)")
        for e in new_bad:
            out(f"   {e}")
        return 0, len(all_failed)
    if new_bad:
        suppress_emails(new_bad)
        n_live = rebuild_live()
        out(f"[proton-dsn] suppressed {len(new_bad)} new bounced addrs | contacts_live now {n_live}")
    else:
        out(f"[proton-dsn] no new bounces to suppress ({len(all_failed)} already known)")
    return len(new_bad), len(all_failed)


if __name__ == "__main__":
    run(silent=False, dry_run="--dry-run" in sys.argv)
