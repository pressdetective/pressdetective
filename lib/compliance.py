#!/usr/bin/env python3
"""
lib/compliance.py -- GDPR / DPDP / deliverability compliance helpers.

  load_suppression_set()     → set of suppressed (lowercase) email addresses
  is_suppressed(addr, ...)   → bool
  filter_suppressed(rows, …) → rows with suppressed addresses removed
  add_unsubscribe_headers(msg) → sets RFC 8058 List-Unsubscribe headers
  FOOTER                     → standard unsubscribe + legal footer text
"""

import csv
from pathlib import Path

ROOT = Path(__file__).parent.parent

_PHYSICAL = "PressDetective | Mumbai, Maharashtra, India | info@pressdetective.com"

FOOTER = (
    "--------------------------------------------------------------\n"
    "UNSUBSCRIBE: Reply UNSUBSCRIBE or email info@pressdetective.com.\n"
    "Your address will be removed within 24 hours. Sent on public-interest\n"
    "journalism basis under Indian DPDP Act 2023 and GDPR Art. 6(1)(f).\n"
    f"{_PHYSICAL}\n"
    "--------------------------------------------------------------\n"
)


def load_suppression_set(path=None):
    """Return set of suppressed email addresses (lowercase)."""
    p = Path(path) if path else ROOT / "contacts" / "suppression_list.csv"
    suppressed = set()
    if not p.exists():
        return suppressed
    with open(p, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            e = row.get("email", "").strip().lower()
            if e:
                suppressed.add(e)
    return suppressed


def is_suppressed(addr, suppression_set=None):
    if suppression_set is None:
        suppression_set = load_suppression_set()
    return addr.strip().lower() in suppression_set


def filter_suppressed(rows, email_key=0, suppression_set=None):
    """Return rows (list of tuples or dicts) with suppressed addresses removed.

    email_key: int index for tuples, or string key for dicts.
    """
    if suppression_set is None:
        suppression_set = load_suppression_set()
    result, dropped = [], 0
    for row in rows:
        addr = (row[email_key] if not isinstance(row, dict)
                else row.get(email_key, "")).strip().lower()
        if addr in suppression_set:
            dropped += 1
        else:
            result.append(row)
    if dropped:
        print(f"[compliance] Suppressed {dropped} address(es) removed from send list")
    return result


def add_unsubscribe_headers(msg):
    """Add RFC 8058 one-click List-Unsubscribe headers (idempotent)."""
    if "List-Unsubscribe" not in msg:
        msg["List-Unsubscribe"] = "<mailto:info@pressdetective.com?subject=UNSUBSCRIBE>"
    if "List-Unsubscribe-Post" not in msg:
        msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    return msg
