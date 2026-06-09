#!/usr/bin/env python3
"""
PressDetective IMAP inbox reader.

- Reads all 4 ProtonMail Bridge accounts
- Finds unread messages, shows bodies
- Returns structured data for auto-reply logic
- Marks messages as read after processing
"""

import imaplib, ssl, email, json
from email.header import decode_header
from pathlib import Path
from dataclasses import dataclass, field

CREDS_PATH  = Path(__file__).parent.parent / ".creds" / "proton_accounts.json"
BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 1143
BRIDGE_PW   = "FzspzmcI-DE4s1JIp7HU3A"


@dataclass
class Message:
    uid:        str
    inbox:      str          # which PD address received it
    from_addr:  str
    to_addr:    str
    subject:    str
    date:       str
    message_id: str
    body:       str
    raw:        bytes = field(repr=False, default=b"")


def _ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    return ctx


def _decode_header(h: str) -> str:
    parts = decode_header(h or "")
    return "".join(
        p.decode(enc or "utf-8", errors="replace") if isinstance(p, bytes) else p
        for p, enc in parts
    ).strip()


def _get_body(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in cd:
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(
                        part.get_content_charset() or "utf-8", errors="replace"
                    )
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(
                msg.get_content_charset() or "utf-8", errors="replace"
            )
    return ""


def read_inbox(
    account_key: str,
    unread_only: bool = True,
    search_from: str  = "",
    limit:       int  = 50,
    mark_read:   bool = False,
) -> list[Message]:
    """
    Fetch messages from one account's inbox.

    account_key : 'info' | 'sujata' | 'santosh' | 'olympio'
    unread_only : only UNSEEN messages
    search_from : filter by sender domain/address (e.g. 'zeptomail.com')
    limit       : max messages to return (most recent first)
    mark_read   : mark fetched messages as \\Seen
    """
    creds  = json.loads(CREDS_PATH.read_text(encoding="utf-8"))
    acc    = creds["accounts"][account_key]
    addr   = acc["address"]
    ctx    = _ssl_ctx()

    m = imaplib.IMAP4(BRIDGE_HOST, BRIDGE_PORT)
    m.starttls(ssl_context=ctx)
    m.login(addr, BRIDGE_PW)
    m.select("INBOX")

    if search_from:
        criteria = f'FROM "{search_from}"'
    elif unread_only:
        criteria = "UNSEEN"
    else:
        criteria = "ALL"

    _, data = m.search(None, criteria)
    ids = data[0].split()
    ids = ids[-limit:]  # most recent

    messages = []
    for uid in reversed(ids):
        _, msg_data = m.fetch(uid, "(RFC822)")
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        messages.append(Message(
            uid        = uid.decode(),
            inbox      = addr,
            from_addr  = _decode_header(msg.get("From", "")),
            to_addr    = _decode_header(msg.get("To", "")),
            subject    = _decode_header(msg.get("Subject", "")),
            date       = msg.get("Date", ""),
            message_id = msg.get("Message-ID", ""),
            body       = _get_body(msg),
            raw        = raw,
        ))

        if mark_read:
            m.store(uid, "+FLAGS", "\\Seen")

    m.logout()
    return messages


def read_all_inboxes(
    unread_only: bool = True,
    search_from: str  = "",
    limit:       int  = 20,
) -> dict[str, list[Message]]:
    """Read all 4 accounts. Returns {account_key: [Message, ...]}."""
    creds = json.loads(CREDS_PATH.read_text(encoding="utf-8"))
    result = {}
    for key in creds["accounts"]:
        try:
            result[key] = read_inbox(key, unread_only=unread_only,
                                     search_from=search_from, limit=limit)
        except Exception as e:
            print(f"  [inbox] {key}: {e}")
            result[key] = []
    return result


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sender_filter = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"Checking all inboxes{' for: ' + sender_filter if sender_filter else ''}\n")
    all_msgs = read_all_inboxes(unread_only=False, search_from=sender_filter)
    for key, msgs in all_msgs.items():
        print(f"  [{key}]  {len(msgs)} message(s)")
        for msg in msgs:
            print(f"    From   : {msg.from_addr}")
            print(f"    Subject: {msg.subject}")
            print(f"    Date   : {msg.date}")
            print(f"    Msg-ID : {msg.message_id}")
            if msg.body.strip():
                print("    Body   :")
                for line in msg.body.strip().splitlines()[:30]:
                    print(f"      {line}")
            print()
