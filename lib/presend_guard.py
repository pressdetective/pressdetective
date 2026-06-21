#!/usr/bin/env python3
"""
lib/presend_guard.py -- deliverability + compliance guard for scripts that send
via smtplib directly (i.e. bypass lib/mailer).  Import it once near the top and
EVERY send through that process is filtered before the envelope leaves:

  1. No-contact list   -- the complainant (Abhishek Saraf) is never emailed.
  2. Suppression list  -- contacts/suppression_list.csv (bounces + unsubscribes).
  3. Live verification -- syntax + MX/A DNS (system, then Google 8.8.8.8).

Recipients failing any check are stripped from the envelope, so dead /
suppressed / forbidden addresses can never bounce (protecting sender
reputation) or be contacted.  Patching SMTP.sendmail also covers
SMTP.send_message, which calls sendmail internally.

Usage (robust to current working directory):
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    import lib.presend_guard   # noqa: F401
"""
import csv
import smtplib
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SUPPRESSION_CSV = _ROOT / "contacts" / "suppression_list.csv"

# Never email the complainant -- counsel advised no direct contact (it can work
# against the case).  See memory: feedback_no_contact_saraf.
NO_CONTACT = {"abhishek_saraf78@yahoo.com"}


def _load_suppressed():
    s = set()
    if _SUPPRESSION_CSV.exists():
        try:
            with open(_SUPPRESSION_CSV, encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    if row.get("email"):
                        s.add(row["email"].strip().lower())
        except Exception:
            pass
    return s


# Loaded once per process (campaign run); cheap and avoids re-reading per send.
_SUPPRESSED = _load_suppressed()

# Pull verifier helpers (syntax + DNS) if available; degrade gracefully if not.
try:
    from lib.verifier import _syntax_ok as _verify_syntax, _has_mx as _verify_mx
    _VERIFY = True
except Exception:
    _VERIFY = False


def _check(addr):
    """Return None if the address is OK to send, else a short drop-reason."""
    low = addr.strip().lower()
    if low in NO_CONTACT:
        return "no-contact"
    if _VERIFY and not _verify_syntax(low):
        return "bad-syntax"
    if low in _SUPPRESSED:
        return "suppressed"
    if _VERIFY:
        domain = low.split("@", 1)[1] if "@" in low else ""
        if not domain or not _verify_mx(domain):
            return f"dead-domain:{domain}"
    return None


def _filter(to_addrs):
    kept, dropped = [], []
    for r in to_addrs:
        why = _check(r)
        (dropped if why else kept).append((r, why) if why else r)
    return kept, dropped


_orig_sendmail = smtplib.SMTP.sendmail


def _guarded_sendmail(self, from_addr, to_addrs, msg, *args, **kwargs):
    if isinstance(to_addrs, str):
        to_addrs = [to_addrs]
    to_addrs = list(to_addrs)
    kept, dropped = _filter(to_addrs)
    for addr, why in dropped:
        print(f"[presend-guard] dropped {addr} ({why})")
    if not kept:
        print("[presend-guard] no valid recipients remain -- skipping send")
        return {}
    return _orig_sendmail(self, from_addr, kept, msg, *args, **kwargs)


# Install once (idempotent -- re-import won't double-wrap).
if getattr(smtplib.SMTP.sendmail, "__name__", "") != "_guarded_sendmail":
    smtplib.SMTP.sendmail = _guarded_sendmail
