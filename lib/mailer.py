#!/usr/bin/env python3
"""
lib/mailer.py — Unified PressDetective mailer + inbox reader.

Send chain (automatic fallback):
  1. Proton Bridge   127.0.0.1:1025  STARTTLS  (bridge_password from creds)
  2. Proton remote   smtp.protonmail.ch:587  STARTTLS  (token from creds)
  3. ZeptoMail       smtp.zeptomail.in:587   STARTTLS  (ZEPTO_TOKEN env var)

Read (IMAP via Proton Bridge, local only):
  Bridge IMAP: 127.0.0.1:1143  STARTTLS

Credentials file: .creds/proton_accounts.json
Env var overrides:
  BRIDGE_PASS_<ACCOUNT>   e.g. BRIDGE_PASS_INFO, BRIDGE_PASS_SUJATA
  PROTON_TOKEN_<ACCOUNT>  e.g. PROTON_TOKEN_INFO, PROTON_TOKEN_SUJATA
  ZEPTO_TOKEN             ZeptoMail send-mail token

Usage:
    from lib.mailer import send_mail, read_inbox, build_msg

    msg = build_msg(
        from_addr="info@pressdetective.com",
        to="client@example.com",
        subject="Your report",
        body="Please find attached...",
        cc="info@pressdetective.com",
    )
    send_mail(msg, account="info")          # auto-fallback chain

    # Read last 10 unseen messages in info@ inbox
    emails = read_inbox(account="info", limit=10, unseen_only=True)
    for e in emails:
        print(e["subject"], e["from"], e["date"])
"""

import os, json, ssl, smtplib, imaplib, email, email.policy
from email.message import EmailMessage
from pathlib import Path

# ── Paths & constants ─────────────────────────────────────────────────────────
ROOT       = Path(__file__).parent.parent
CREDS_FILE = ROOT / ".creds" / "proton_accounts.json"

BRIDGE_SMTP_HOST = "127.0.0.1"
BRIDGE_SMTP_PORT = 1025
BRIDGE_IMAP_HOST = "127.0.0.1"
BRIDGE_IMAP_PORT = 1143

PROTON_SMTP_HOST = "smtp.protonmail.ch"
PROTON_SMTP_PORT = 587

ZEPTO_SMTP_HOST  = "smtp.zeptomail.in"
ZEPTO_SMTP_PORT  = 587
ZEPTO_SMTP_USER  = "emailapikey"

CC_ALWAYS = "info@pressdetective.com"   # CC on every outbound message


# ── Credentials ───────────────────────────────────────────────────────────────
def _load_creds():
    if not CREDS_FILE.exists():
        return {}
    with open(CREDS_FILE, encoding="utf-8") as f:
        return json.load(f).get("accounts", {})


def _get(account: str, field: str, env_override: str = "") -> str:
    if env_override:
        val = os.environ.get(env_override, "")
        if val:
            return val
    creds = _load_creds()
    return creds.get(account, {}).get(field, "")


def bridge_password(account: str) -> str:
    return _get(account, "bridge_password", f"BRIDGE_PASS_{account.upper()}")


def proton_token(account: str) -> str:
    return _get(account, "token", f"PROTON_TOKEN_{account.upper()}")


def zepto_token() -> str:
    return os.environ.get("ZEPTO_TOKEN", "")


def account_address(account: str) -> str:
    creds = _load_creds()
    return creds.get(account, {}).get("address", account)


# ── Message builder ───────────────────────────────────────────────────────────
def build_msg(
    from_addr: str,
    to: str,
    subject: str,
    body: str,
    cc: str = CC_ALWAYS,
    attachments: list = None,   # list of file paths
) -> EmailMessage:
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


# ── SMTP senders ──────────────────────────────────────────────────────────────
def _starttls_ctx():
    ctx = ssl.create_default_context()
    return ctx


def _starttls_ctx_no_verify():
    """For Proton Bridge which uses a self-signed cert."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    return ctx


def _send_bridge(msg: EmailMessage, account: str) -> bool:
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


def _send_proton_remote(msg: EmailMessage, account: str) -> bool:
    token = proton_token(account)
    if not token or token == "FILL_IN":
        return False
    addr = account_address(account)
    try:
        ctx = _starttls_ctx()
        with smtplib.SMTP(PROTON_SMTP_HOST, PROTON_SMTP_PORT, timeout=15) as s:
            s.ehlo()
            s.starttls(context=ctx)
            s.login(addr, token)
            s.send_message(msg)
        print(f"[mailer] sent via Proton remote ({addr})")
        return True
    except Exception as e:
        print(f"[mailer] Proton remote failed: {e}")
        return False


def _send_zepto(msg: EmailMessage) -> bool:
    token = zepto_token()
    if not token:
        return False
    from_addr = msg["From"]
    try:
        ctx = _starttls_ctx()
        with smtplib.SMTP(ZEPTO_SMTP_HOST, ZEPTO_SMTP_PORT, timeout=15) as s:
            s.ehlo()
            s.starttls(context=ctx)
            s.login(ZEPTO_SMTP_USER, token)
            s.send_message(msg)
        print(f"[mailer] sent via ZeptoMail ({from_addr})")
        return True
    except Exception as e:
        print(f"[mailer] ZeptoMail failed: {e}")
        return False


def send_mail(msg: EmailMessage, account: str = "info", providers: list = None) -> bool:
    """
    Send msg through the first available provider.
    providers defaults to ["bridge", "proton", "zepto"].
    Returns True if sent, False if all providers failed.
    """
    chain = providers or ["bridge", "proton", "zepto"]
    for p in chain:
        if p == "bridge"  and _send_bridge(msg, account):        return True
        if p == "proton"  and _send_proton_remote(msg, account): return True
        if p == "zepto"   and _send_zepto(msg):                  return True
    print("[mailer] ERROR: all providers failed — message not sent")
    return False


# ── IMAP reader (Proton Bridge) ───────────────────────────────────────────────
def read_inbox(account: str = "info", limit: int = 10, unseen_only: bool = False,
               mailbox: str = "INBOX") -> list:
    """
    Read messages from account's inbox via Proton Bridge IMAP.
    Returns list of dicts: {uid, subject, from, date, body, seen}.
    Requires Proton Bridge running locally.
    """
    pw   = bridge_password(account)
    addr = account_address(account)
    if not pw:
        raise ValueError(f"No bridge_password for account '{account}'")

    ctx = _starttls_ctx_no_verify()
    with imaplib.IMAP4(BRIDGE_IMAP_HOST, BRIDGE_IMAP_PORT) as M:
        M.starttls(ssl_context=ctx)
        M.login(addr, pw)
        M.select(mailbox, readonly=True)

        criteria = "UNSEEN" if unseen_only else "ALL"
        _, data   = M.search(None, criteria)
        uids      = data[0].split()
        uids      = uids[-limit:] if limit else uids   # most recent N

        results = []
        for uid in reversed(uids):
            _, raw = M.fetch(uid, "(RFC822)")
            msg    = email.message_from_bytes(raw[0][1], policy=email.policy.default)
            body   = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_content()
                        break
            else:
                body = msg.get_content()
            results.append({
                "uid":     uid.decode(),
                "subject": msg["subject"] or "",
                "from":    msg["from"] or "",
                "date":    msg["date"] or "",
                "body":    body.strip(),
                "seen":    "\\Seen" in (msg.get("flags", "")),
            })
        return results
