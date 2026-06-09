#!/usr/bin/env python3
"""
check_inbox.py — Read the PressDetective Proton Bridge inbox.

Requires Proton Bridge running locally (127.0.0.1:1143).

Usage:
    python scripts/check_inbox.py                      # info@ last 10 messages
    python scripts/check_inbox.py --account olympio    # olympio@ inbox
    python scripts/check_inbox.py --unseen             # unseen only
    python scripts/check_inbox.py --limit 20           # last 20 messages
    python scripts/check_inbox.py --mailbox Sent       # different mailbox
"""
import sys, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.mailer import read_inbox

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--account",  default="info",    help="account key (info/olympio/santosh/sujata)")
    ap.add_argument("--limit",    type=int, default=10)
    ap.add_argument("--unseen",   action="store_true")
    ap.add_argument("--mailbox",  default="INBOX")
    args = ap.parse_args()

    print(f"Reading {args.account}@ — {args.mailbox} ({'unseen' if args.unseen else 'all'}, last {args.limit})\n")

    msgs = read_inbox(account=args.account, limit=args.limit,
                      unseen_only=args.unseen, mailbox=args.mailbox)

    if not msgs:
        print("(no messages)")
        return

    for i, m in enumerate(msgs, 1):
        print(f"{'─'*60}")
        print(f"#{i}  {m['date']}")
        print(f"From:    {m['from']}")
        print(f"Subject: {m['subject']}")
        print(f"Body:\n{m['body'][:500]}{'...' if len(m['body']) > 500 else ''}")
    print(f"{'─'*60}")
    print(f"\n{len(msgs)} message(s) shown.")

if __name__ == "__main__":
    main()
