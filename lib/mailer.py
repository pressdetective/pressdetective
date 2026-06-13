#!/usr/bin/env python3
"""
lib/mailer.py -- Unified PressDetective mailer + inbox reader.

Send chain (automatic fallback):
  1. Proton Bridge    127.0.0.1:1025          STARTTLS  (bridge_password from creds)
  2. Postmark         smtp.postmarkapp.com:587 STARTTLS  (token from creds smtp_postmark)
  3. Proton remote    smtp.protonmail.ch:587   STARTTLS  (token from creds)
  4. ZeptoMail        smtp.zeptomail.in:587    STARTTLS  (ZEPTO_TOKEN env var)

Read (IMAP via Proton Bridge, local only):
  Bridge IMAP: 127.0.0.1:1143  STARTTLS

Credentials file: .creds/proton_accounts.json
Env var overrides:
  BRIDGE_PASS_<ACCOUNT>   e.g. BRIDGE_PASS_INFO, BRIDGE_PASS_SUJATA
  PROTON_TOKEN_<ACCOUNT>  e.g. PROTON_TOKEN_INFO, PROTON_TOKEN_SUJATA
  POSTMARK_TOKEN          Postmark Server API token
  MAILTRAP_TOKEN          Mailtrap API token
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

POSTMARK_SMTP_HOST  = "smtp.postmarkapp.com"
POSTMARK_SMTP_PORT  = 587

ZEPTO_SMTP_HOST     = "smtp.zeptomail.in"
ZEPTO_SMTP_PORT     = 587
ZEPTO_SMTP_USER     = "emailapikey"

MAILTRAP_SMTP_HOST  = "live.smtp.mailtrap.io"
MAILTRAP_SMTP_PORT  = 587
MAILTRAP_SMTP_USER  = "api"

CC_ALWAYS = "info@pressdetective.com"


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


def postmark_token():
    env = os.environ.get("POSTMARK_TOKEN", "")
    if env:
        return env
    if CREDS_FILE.exists():
        with open(CREDS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("smtp_postmark", {}).get("token", "")
    return ""


def zepto_token():
    return os.environ.get("ZEPTO_TOKEN", "")




def mailtrap_token():
    env = os.environ.get('MAILTRAP_TOKEN', '')
    if env:
        return env
    if CREDS_FILE.exists():
        with open(CREDS_FILE, encoding='utf-8') as f:
            data = json.load(f)
        return data.get('smtp_mailtrap', {}).get('token', '')
    return ''


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


def _send_postmark(msg):
    token = postmark_token()
    if not token:
        return False
    from_addr = msg["From"]
    import copy
    msg = copy.copy(msg)
    if "X-PM-Message-Stream" not in msg:
        msg["X-PM-Message-Stream"] = "outbound"
    try:
        with smtplib.SMTP(POSTMARK_SMTP_HOST, POSTMARK_SMTP_PORT, timeout=15) as s:
            s.ehlo()
            s.starttls(context=_starttls_ctx())
            s.login(token, token)
            s.send_message(msg)
        print(f"[mailer] sent via Postmark ({from_addr})")
        return True
    except Exception as e:
        print(f"[mailer] Postmark failed: {e}")
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


def _send_zepto(msg):
    token = zepto_token()
    if not token:
        return False
    from_addr = msg["From"]
    try:
        with smtplib.SMTP(ZEPTO_SMTP_HOST, ZEPTO_SMTP_PORT, timeout=15) as s:
            s.ehlo()
            s.starttls(context=_starttls_ctx())
            s.login(ZEPTO_SMTP_USER, token)
            s.send_message(msg)
        print(f"[mailer] sent via ZeptoMail ({from_addr})")
        return True
    except Exception as e:
        print(f"[mailer] ZeptoMail failed: {e}")
        return False


def _send_mailtrap(msg):
    token = mailtrap_token()
    if not token:
        return False
    from_addr = msg["From"]
    try:
        with smtplib.SMTP(MAILTRAP_SMTP_HOST, MAILTRAP_SMTP_PORT, timeout=15) as s:
            s.ehlo()
            s.starttls(context=_starttls_ctx())
            s.login(MAILTRAP_SMTP_USER, token)
            s.send_message(msg)
        print(f"[mailer] sent via Mailtrap ({from_addr})")
        return True
    except Exception as e:
        print(f"[mailer] Mailtrap failed: {e}")
        return False


def send_mail(msg, account="info", providers=None):
    """
    Send msg through the first available provider.
    providers defaults to ["bridge", "postmark", "proton", "zepto"].
    Returns True if sent, False if all providers failed.
    """
    chain = providers or ["bridge", "postmark", "proton", "zepto"]
    for p in chain:
        if p == "bridge"   and _send_bridge(msg, account):        return True
        if p == "postmark" and _send_postmark(msg):               return True
        if p == "proton"   and _send_proton_remote(msg, account): return True
        if p == "zepto"    and _send_zepto(msg):                  return True
    print("[mailer] ERROR: all providers failed -- message not sent")
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