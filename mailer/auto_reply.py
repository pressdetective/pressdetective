#!/usr/bin/env python3
"""
Auto-reply engine for PressDetective inboxes.

- Polls all 4 accounts for new messages from a given sender
- Replies from the SAME account the message landed in (Reply-To rule)
- Handles ZeptoMail unblock replies, unsubscribe requests, bounce webhooks

Usage:
    python -m mailer.auto_reply --watch zeptomail.com
    python -m mailer.auto_reply --once  zeptomail.com
"""

import argparse, time, re, sys
from pathlib import Path
from .inbox import read_inbox, read_all_inboxes
from .send  import send_email, process_unsubscribe

# Track processed Message-IDs to avoid double replies
PROCESSED_FILE = Path(__file__).parent.parent / "contacts" / ".processed_msg_ids.txt"


def _load_processed() -> set:
    if PROCESSED_FILE.exists():
        return set(PROCESSED_FILE.read_text(encoding="utf-8").splitlines())
    return set()


def _mark_processed(msg_id: str):
    PROCESSED_FILE.parent.mkdir(exist_ok=True)
    with PROCESSED_FILE.open("a", encoding="utf-8") as f:
        f.write(msg_id.strip() + "\n")


# ── Reply templates ───────────────────────────────────────────────────────────

def build_zepto_gdpr_reply(original_body: str) -> str:
    return """\
Dear ZeptoMail Support Team,

Thank you for your response. We want to provide full transparency on the steps we have taken and the nature of our contacts.

NATURE OF OUR CONTACT LIST
---------------------------
All contacts in our list are professionals — journalists, editors, lawyers, government officials, and civil society organisations — who are part of our legitimate professional network. These are not purchased lists or unknown recipients. They are contacts we have worked with, corresponded with, or engaged over the course of our case work. Many of these contacts date back several years, and over that time, some institutional email addresses become inactive when individuals change roles or organisations. This was the source of the "User not found" bounces — not spam, not harvested lists.

NEW COMPLIANCE MEASURES NOW IN PLACE
--------------------------------------
We have implemented the following safeguards, effective immediately:

1. DPDP Act 2023 Compliance (India)
   - Every outbound email now carries a mandatory unsubscribe footer with a one-click reply mechanism
   - List-Unsubscribe and List-Unsubscribe-Post headers (RFC 8058) are set on every message
   - A suppression list is maintained at contacts/suppression_list.csv; every send is checked against it
   - Unsubscribe requests are processed within 48 hours: address removed from suppression list + contacts list
   - Grievance Officer contact (info@pressdetective.com) is disclosed in every email footer

2. Email Cleaning Pipeline
   - DNS / MX record verification run on all 3,238 contacts — 68 dead-domain addresses removed
   - All ZeptoMail "User not found" bounces are being appended to our suppression blacklist
   - All "Host not reachable" bounces are similarly being suppressed
   - Going forward: no address is added to the active list without DNS verification

3. Send Volume Controls
   - Future campaigns will be sent in small batches (max 200/day) to monitor bounce rate in real time
   - Any domain with a bounce rate above 5% is immediately added to the suppression list

4. Dedicated Transactional Use Only
   - We confirm that our ZeptoMail usage is strictly transactional: case notifications and legal intelligence reports to named, known contacts
   - We are not running broadcast marketing campaigns

CURRENT STATE
--------------
Our active contact list has been reduced from 3,238 to 3,170 after DNS cleaning, and we are continuing to remove bounced addresses as they are identified. We expect the final verified list to be significantly smaller and entirely bounce-free.

We respectfully request reinstatement of our account. We are committed to maintaining a clean sender reputation and are happy to provide any additional information or documentation you require.

Thank you for your patience and support.

Warm regards,
PressDetective
info@pressdetective.com
Grievance Officer: info@pressdetective.com
"""


def build_unsubscribe_reply(from_name: str) -> str:
    return f"""\
Dear {from_name or 'Colleague'},

We have received your unsubscribe request and have processed it immediately.

Your email address has been permanently removed from our contact list and added to our suppression list. You will not receive any further emails from PressDetective.

If you believe this was done in error or wish to re-subscribe in future, please write to info@pressdetective.com.

Thank you.

Warm regards,
PressDetective
info@pressdetective.com
"""


# ── Core processor ────────────────────────────────────────────────────────────

def process_message(account_key: str, msg) -> bool:
    """
    Inspect one message and take action.
    Returns True if a reply was sent.
    """
    processed = _load_processed()
    if msg.message_id in processed:
        return False

    from_lower   = msg.from_addr.lower()
    subj_lower   = msg.subject.lower()
    body_lower   = msg.body.lower()

    replied = False

    # ── ZeptoMail support reply ────────────────────────────────────────────
    if "zeptomail" in from_lower or "zoho" in from_lower:
        if any(kw in subj_lower or kw in body_lower
               for kw in ["blocked", "unusual", "bounce", "suspended", "reinstat"]):
            print(f"  [AUTO-REPLY] ZeptoMail message → replying from {msg.inbox}")
            result = send_email(
                from_key     = account_key,
                to           = _extract_email(msg.from_addr),
                subject      = msg.subject,
                body         = build_zepto_gdpr_reply(msg.body),
                in_reply_to  = msg.message_id,
            )
            if result["ok"]:
                print(f"  [SENT] Reply to ZeptoMail from {msg.inbox}")
                replied = True
            else:
                print(f"  [FAIL] {result['error']}")

    # ── Unsubscribe request ────────────────────────────────────────────────
    elif ("unsubscribe" in subj_lower
          or "remove me" in body_lower
          or "opt out" in body_lower
          or "opt-out" in body_lower):
        sender_email = _extract_email(msg.from_addr)
        print(f"  [UNSUB] Processing unsubscribe for {sender_email}")
        process_unsubscribe(sender_email)
        from_name = msg.from_addr.split("<")[0].strip().strip('"')
        result = send_email(
            from_key     = account_key,
            to           = sender_email,
            subject      = "Re: Unsubscribe request — confirmed",
            body         = build_unsubscribe_reply(from_name),
            in_reply_to  = msg.message_id,
            skip_footer  = True,
        )
        if result["ok"]:
            print(f"  [SENT] Unsubscribe confirmation to {sender_email}")
            replied = True

    if replied or msg.message_id:
        _mark_processed(msg.message_id)

    return replied


def _extract_email(header: str) -> str:
    m = re.search(r"<([^>]+)>", header)
    if m:
        return m.group(1).strip()
    return header.strip()


# ── Poll loop ─────────────────────────────────────────────────────────────────

def check_once(sender_filter: str = ""):
    """Check all inboxes once. Print summary."""
    print(f"Checking all inboxes{' (filter: ' + sender_filter + ')' if sender_filter else ''}...")
    all_msgs = read_all_inboxes(unread_only=False, search_from=sender_filter)
    total_acted = 0
    for key, msgs in all_msgs.items():
        for msg in msgs:
            acted = process_message(key, msg)
            if acted:
                total_acted += 1
    print(f"Done. {total_acted} auto-repl(ies) sent.")
    return total_acted


def watch(sender_filter: str = "", interval_s: int = 120):
    """Poll every interval_s seconds."""
    print(f"Watching all inboxes every {interval_s}s. Ctrl+C to stop.")
    while True:
        try:
            check_once(sender_filter)
        except KeyboardInterrupt:
            print("Stopped.")
            break
        except Exception as e:
            print(f"  [ERROR] {e}")
        time.sleep(interval_s)


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", metavar="SENDER", default="",
                        help="Watch inboxes and auto-reply to this sender domain")
    parser.add_argument("--once", metavar="SENDER", default="",
                        help="Check once for this sender and reply, then exit")
    parser.add_argument("--interval", type=int, default=120,
                        help="Poll interval in seconds (default 120)")
    args = parser.parse_args()

    if args.watch:
        watch(args.watch, args.interval)
    elif args.once:
        check_once(args.once)
    else:
        check_once()
