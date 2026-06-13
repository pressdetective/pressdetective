#!/usr/bin/env python3
"""
lib/verifier.py -- Pre-send email verification for PressDetective.

Checks (in order):
  1. Syntax  -- basic email format
  2. Suppression list  -- contacts/suppression_list.csv
  3. DNS check  -- system DNS first, then Google 8.8.8.8 fallback.
                   Domain is only marked dead if BOTH resolvers fail.

Usage:
    from lib.verifier import verify_email, filter_recipients, batch_verify_csv

    ok, reason = verify_email("editor@thehindu.com")
    clean = filter_recipients(["a@b.com", "bad@dead.domain"])
    batch_verify_csv("contacts/contacts_live.csv", "contacts/contacts_live.csv")
"""

import re, csv, socket, time, concurrent.futures
from pathlib import Path

try:
    import dns.resolver as _dns_resolver
    _DNS_AVAILABLE = True
except ImportError:
    _DNS_AVAILABLE = False

ROOT             = Path(__file__).parent.parent
SUPPRESSION_CSV  = ROOT / "contacts" / "suppression_list.csv"
LIVE_CSV         = ROOT / "contacts" / "contacts_live.csv"

_EMAIL_RE  = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_mx_cache  = {}   # domain -> bool

# ---------------------------------------------------------------------------
# Core checks
# ---------------------------------------------------------------------------

def _syntax_ok(email: str) -> bool:
    return bool(_EMAIL_RE.match(email.strip()))


def _load_suppressed() -> set:
    if not SUPPRESSION_CSV.exists():
        return set()
    with open(SUPPRESSION_CSV, encoding="utf-8-sig") as f:
        return {row["email"].strip().lower() for row in csv.DictReader(f) if row.get("email")}


def _resolve_system(domain: str) -> bool:
    """Try system DNS resolver."""
    try:
        socket.getaddrinfo(domain, None, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_CANONNAME)
        return True
    except (socket.gaierror, OSError):
        return False


def _resolve_google(domain: str) -> bool:
    """Try Google public DNS (8.8.8.8) via dnspython."""
    if not _DNS_AVAILABLE:
        return False
    try:
        r = _dns_resolver.Resolver(configure=False)
        r.nameservers = ["8.8.8.8", "8.8.4.4"]
        r.timeout = 5
        r.lifetime = 5
        r.resolve(domain, "A")
        return True
    except Exception:
        try:
            r.resolve(domain, "MX")
            return True
        except Exception:
            return False


def _has_mx(domain: str) -> bool:
    """
    Returns True if domain resolves via system DNS OR Google 8.8.8.8.
    A domain is only marked dead if BOTH resolvers fail -- this prevents
    local DNS congestion or geo-filtering from causing false suppressions.
    """
    if domain in _mx_cache:
        return _mx_cache[domain]
    # Try system resolver up to 2 times
    for _ in range(2):
        if _resolve_system(domain):
            _mx_cache[domain] = True
            return True
        time.sleep(0.2)
    # System failed -- try Google public DNS before marking dead
    if _resolve_google(domain):
        _mx_cache[domain] = True
        return True
    _mx_cache[domain] = False
    return False


def _suppress(email: str, reason: str):
    """Append one entry to suppression_list.csv."""
    import datetime
    SUPPRESSION_CSV.parent.mkdir(parents=True, exist_ok=True)
    exists = SUPPRESSION_CSV.exists()
    with open(SUPPRESSION_CSV, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["email", "reason", "date", "source"])
        w.writerow([email.lower(), reason, datetime.date.today().isoformat(), "verifier"])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def verify_email(email: str, auto_suppress: bool = True):
    """
    Returns (True, "ok") or (False, reason_string).
    If auto_suppress=True, confirmed-dead domains are written to suppression_list.csv.
    """
    email = email.strip().lower()

    if not _syntax_ok(email):
        return False, "invalid_syntax"

    if email in _load_suppressed():
        return False, "suppressed"

    domain = email.split("@", 1)[1]
    if not _has_mx(domain):
        if auto_suppress:
            _suppress(email, f"dead_domain:{domain}")
        return False, f"dead_domain:{domain}"

    return True, "ok"


def filter_recipients(addresses, auto_suppress: bool = True):
    """
    Given a list of email strings, return only those that pass verification.
    Logs each rejection.
    """
    clean = []
    for addr in addresses:
        ok, reason = verify_email(addr, auto_suppress=auto_suppress)
        if ok:
            clean.append(addr)
        else:
            print(f"[verifier] SKIP {addr} -- {reason}")
    return clean


def batch_verify_csv(input_csv=None, output_csv=None, workers=10, verbose=False):
    """
    Verify every email in input_csv.
    Writes passing rows back to output_csv (in-place by default).
    Confirmed-dead domains are written to suppression_list.csv.
    Returns (total, passed, failed) counts.

    workers=10: Conservative default.  Each domain checked via system DNS
    first, then Google 8.8.8.8 fallback, so false positives are minimal.
    """
    src = Path(input_csv or LIVE_CSV)
    dst = Path(output_csv or src)

    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    if not rows:
        return 0, 0, 0

    emails  = [r["email"].strip() for r in rows]
    domains = list({e.split("@", 1)[1] for e in emails if "@" in e})

    print(f"[verifier] Checking {len(domains)} unique domains ({len(emails)} addresses)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(_has_mx, domains))   # populates _mx_cache

    passed, failed_rows = [], []
    for row in rows:
        email = row["email"].strip().lower()
        ok, reason = verify_email(email, auto_suppress=True)
        if ok:
            passed.append(row)
        else:
            failed_rows.append((email, reason))
            if verbose:
                print(f"  FAIL  {email}  {reason}")

    with open(dst, "w", encoding="utf-8", newline="", errors="replace") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(passed)

    total  = len(rows)
    n_pass = len(passed)
    n_fail = total - n_pass
    print(f"[verifier] Done: {total} total | {n_pass} pass | {n_fail} fail")
    return total, n_pass, n_fail


if __name__ == "__main__":
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else str(LIVE_CSV)
    batch_verify_csv(csv_path, verbose=True)