#!/usr/bin/env python3
"""
lib/mailer.py -- PressDetective mailer via Proton Mail only.

Send chain (automatic fallback):
  1. Proton Bridge    127.0.0.1:1025          STARTTLS  (bridge_password from creds)
  2. Proton remote    smtp.protonmail.ch:587   STARTTLS  (token from creds)

Read (IMAP via Proton Bridge, local only):
  Bridge IMAP: 127.0.0.1:1143  STARTTLS

Credentials file: .creds/proton_accounts.json
Env var overrides:
  BRIDGE_PASS_<ACCOUNT>   e.g. BRIDGE_PASS_INFO
  PROTON_TOKEN_<ACCOUNT>  e.g. PROTON_TOKEN_INFO

Usage:
    from lib.mailer import send_mail, read_inbox, build_msg

    msg = build_msg(
        from_addr="info@pressdetective.com",
        to="client@example.com",
        subject="Your report",
        body="Please find attached...",
        cc="info@pressdetective.com",
    )
    send_mail(msg, account="info")          # auto-fallback to Bridge → Proton remote

    emails = read_inbox(account="info", limit=10, unseen_only=True)
    for e in emails:
        print(e["subject"], e["from"], e["date"])
"""

import os, json, ssl, smtplib, imaplib, email, email.policy
from email.message import EmailMessage
from pathlib import Path

ROOT       = Path(__file__).parent.parent
CREDS_FILE = ROOT / ".creds" / "proton_accounts.json"

BRIDGE_SMTP_HOST    = "127.0.0.1"
BRIDGE_SMTP_PORT    = 1025
BRIDGE_IMAP_HOST    = "127.0.0.1"
BRIDGE_IMAP_PORT    = 1143

PROTON_SMTP_HOST    = "smtp.protonmail.ch"
PROTON_SMTP_PORT    = 587

CC_ALWAYS = "info@pressdetective.com"

# ---------------------------------------------------------------------------
# Do-not-send list (temporary).  Any account name OR From address listed here
# is BLOCKED from sending -- send_mail() refuses and returns False.
# Reason: Adv. Sujata Shirasi is on vacation (set 2026-06-21); all outreach
# must go from Santosh Sakpal (account="santosh", santosh@pressdetective.com).
# To re-enable her when she returns: remove both entries below.
# ---------------------------------------------------------------------------
BLOCKED_SENDERS = {"sujata", "sujata.shirasi@pressdetective.com"}


def _is_blocked_sender(msg, account):
    """True if this send is from a blocked account name OR a blocked From address."""
    if account and account.strip().lower() in BLOCKED_SENDERS:
        return True
    from_hdr = (msg.get("From", "") or "").lower()
    return any(b in from_hdr for b in BLOCKED_SENDERS if "@" in b)


def _load_creds():
    if not CREDS_FILE.exists():
        return {}
    with open(CREDS_FILE, encoding="utf-8") as f:
        return json.load(f).get("accounts", {})


def _get(account, field, env_override=""):
    if env_override:
        val = os.environ.get(env_override, "")
        if val:
            return val
    creds = _load_creds()
    return creds.get(account, {}).get(field, "")


def bridge_password(account):
    return _get(account, "bridge_password", f"BRIDGE_PASS_{account.upper()}")


def proton_token(account):
    return _get(account, "token", f"PROTON_TOKEN_{account.upper()}")


def account_address(account):
    creds = _load_creds()
    return creds.get(account, {}).get("address", account)


def build_msg(from_addr, to, subject, body, cc=CC_ALWAYS, attachments=None):
    msg = EmailMessage()
    msg["From"]    = from_addr
    msg["To"]      = to
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc
    msg.set_content(body)
    for path in (attachments or []):
        p = Path(path)
        with open(p, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="octet-stream",
                               filename=p.name)
    return msg


def _starttls_ctx():
    return ssl.create_default_context()


def _starttls_ctx_no_verify():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    return ctx


def _send_bridge(msg, account):
    pw = bridge_password(account)
    if not pw:
        return False
    addr = account_address(account)
    try:
        with smtplib.SMTP(BRIDGE_SMTP_HOST, BRIDGE_SMTP_PORT, timeout=10) as s:
            s.ehlo()
            s.starttls(context=_starttls_ctx_no_verify())
            s.login(addr, pw)
            s.send_message(msg)
        print(f"[mailer] sent via Bridge ({addr})")
        return True
    except Exception as e:
        print(f"[mailer] Bridge failed: {e}")
        return False


def _send_proton_remote(msg, account):
    token = proton_token(account)
    if not token or token == "FILL_IN":
        return False
    addr = account_address(account)
    try:
        with smtplib.SMTP(PROTON_SMTP_HOST, PROTON_SMTP_PORT, timeout=15) as s:
            s.ehlo()
            s.starttls(context=_starttls_ctx())
            s.login(addr, token)
            s.send_message(msg)
        print(f"[mailer] sent via Proton remote ({addr})")
        return True
    except Exception as e:
        print(f"[mailer] Proton remote failed: {e}")
        return False


_send_counter = 0         # counts send_mail() calls this process (for monitoring)


def send_mail(msg, account="info", providers=None):
    """
    Send msg through the first available Proton provider (Bridge → remote).
    providers defaults to ["bridge", "proton"].
    Returns True if sent, False if all providers failed.
    """
    global _send_counter

    # Hard guard: refuse sends from any blocked sender (e.g. account on vacation).
    if _is_blocked_sender(msg, account):
        print(f"[mailer] BLOCKED: account={account!r} / From={msg.get('From','')!r} "
              f"is on the do-not-send list (Sujata on vacation). "
              f"Use account='santosh' (santosh@pressdetective.com) instead. Not sent.")
        return False

    _send_counter += 1

    chain = providers or ["bridge", "proton"]

    # Pre-send: verify recipient addresses
    try:
        from lib.verifier import filter_recipients
        import email as _em
        raw_to  = msg.get("To",  "") or ""
        raw_cc  = msg.get("Cc",  "") or ""
        all_rcpt = [a.strip() for a in (raw_to + "," + raw_cc).split(",") if a.strip()]
        clean    = filter_recipients(all_rcpt, auto_suppress=True)
        if not clean:
            print("[mailer] All recipients failed verification -- aborting send")
            return False
        # Rebuild To/Cc with only clean addresses
        clean_to = [a for a in clean if a.lower() in [x.lower() for x in raw_to.split(",") if x.strip()]]
        clean_cc = [a for a in clean if a not in clean_to]
        if clean_to:
            del msg["To"];  msg["To"]  = ", ".join(clean_to)
        if clean_cc:
            del msg["Cc"];  msg["Cc"]  = ", ".join(clean_cc)
        elif raw_cc:
            del msg["Cc"]
    except ImportError:
        pass   # verifier not available -- skip check

    # Deliverability: one-click List-Unsubscribe (RFC 8058) on every message.
    if "List-Unsubscribe" not in msg:
        msg["List-Unsubscribe"] = "<mailto:info@pressdetective.com?subject=unsubscribe>"
    if "List-Unsubscribe-Post" not in msg:
        msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"

    for p in chain:
        if p == "bridge" and _send_bridge(msg, account):        return True
        if p == "proton" and _send_proton_remote(msg, account): return True
    print("[mailer] ERROR: all Proton providers failed -- message not sent")
    return False


def read_inbox(account="info", limit=10, unseen_only=False, mailbox="INBOX"):
    """
    Read messages from account inbox via Proton Bridge IMAP.
    Returns list of dicts: {uid, subject, from, date, body, seen}.
    Requires Proton Bridge running locally.
    """
    pw   = bridge_password(account)
    addr = account_address(account)
    if not pw:
        raise ValueError(f"No bridge_password for account {account!r}")

    ctx = _starttls_ctx_no_verify()
    with imaplib.IMAP4(BRIDGE_IMAP_HOST, BRIDGE_IMAP_PORT) as M:
        M.starttls(ssl_context=ctx)
        M.login(addr, pw)
        M.select(mailbox, readonly=True)

        criteria = "UNSEEN" if unseen_only else "ALL"
        _, data   = M.search(None, criteria)
        uids      = data[0].split()
        uids      = uids[-limit:] if limit else uids

        results = []
        for uid in reversed(uids):
            _, raw = M.fetch(uid, "(RFC822)")
            parsed = email.message_from_bytes(raw[0][1], policy=email.policy.default)
            body   = ""
            if parsed.is_multipart():
                for part in parsed.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_content()
                        break
            else:
                body = parsed.get_content()
            results.append({
                "uid":     uid.decode(),
                "subject": parsed["subject"] or "",
                "from":    parsed["from"] or "",
                "date":    parsed["date"] or "",
                "body":    body.strip(),
                "seen":    "\\Seen" in (parsed.get("flags", "")),
            })
        return results