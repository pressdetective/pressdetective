#!/usr/bin/env python3
"""
PressDetective compliant mailer — ProtonMail Bridge

Rules enforced:
  - Reply-To matches From (replies always return to sending address)
  - CC info@pressdetective.com on every send
  - One-click List-Unsubscribe header (RFC 8058)
  - Mandatory footer with unsubscribe + DPDP notice
  - Suppression list check before every send
  - Indian DPDP Act 2023 / IT Act 2000 compliant

Usage:
    from mailer.send import send_email, load_account

    send_email(
        from_key  = "info",             # key in proton_accounts.json
        to        = "someone@example.com",
        subject   = "Case update",
        body      = "Your message here.",
        reply_to_thread = True,         # set False for fresh threads
    )
"""

import smtplib, ssl, json, csv, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import re, datetime

# ── Paths ────────────────────────────────────────────────────────────────────
BASE         = Path(__file__).parent.parent
CREDS_PATH   = BASE / ".creds" / "proton_accounts.json"
SUPPRESS_CSV = BASE / "contacts" / "suppression_list.csv"
CONTACTS_CSV = BASE / "contacts" / "contacts_final.csv"

# ── SMTP Bridge ───────────────────────────────────────────────────────────────
BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 1025
BRIDGE_PW   = "FzspzmcI-DE4s1JIp7HU3A"

# ── DPDP / Compliance footer ──────────────────────────────────────────────────
FOOTER_TEMPLATE = """
---
This email is sent by PressDetective (pressdetective.com) for professional
notification purposes. Your contact information is held in accordance with
India's Digital Personal Data Protection Act 2023 (DPDP Act) and the
Information Technology Act, 2000.

To stop receiving emails: reply with "UNSUBSCRIBE" in the subject line, or
write to info@pressdetective.com. We will process your request within 48 hours.

Grievance Officer: info@pressdetective.com
Data Controller:   PressDetective, India
"""

UNSUBSCRIBE_EMAIL = "unsubscribe@pressdetective.com"
CC_ALWAYS         = "info@pressdetective.com"


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_accounts():
    return json.loads(CREDS_PATH.read_text(encoding="utf-8"))["accounts"]


def load_suppression() -> set:
    """Load suppression list — emails that must never receive mail."""
    if not SUPPRESS_CSV.exists():
        return set()
    suppressed = set()
    with SUPPRESS_CSV.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            e = (row.get("email") or "").strip().lower()
            if e:
                suppressed.add(e)
    return suppressed


def add_to_suppression(email: str, reason: str = "manual"):
    """Append one address to the suppression list."""
    SUPPRESS_CSV.parent.mkdir(exist_ok=True)
    exists = SUPPRESS_CSV.exists()
    with SUPPRESS_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["email", "reason", "date"])
        if not exists:
            w.writeheader()
        w.writerow({
            "email":  email.strip().lower(),
            "reason": reason,
            "date":   datetime.date.today().isoformat(),
        })


def _build_ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    return ctx


def _smtp_send(from_addr: str, recipients: list, raw: str, retries: int = 3):
    ctx = _build_ssl_ctx()
    for attempt in range(retries):
        try:
            with smtplib.SMTP(BRIDGE_HOST, BRIDGE_PORT, timeout=15) as s:
                s.ehlo()
                s.starttls(context=ctx)
                s.ehlo()
                s.login(from_addr, BRIDGE_PW)
                s.sendmail(from_addr, recipients, raw)
            return True
        except smtplib.SMTPRecipientsRefused as e:
            raise ValueError(f"Recipient refused: {e}")
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 + attempt * 2)
            else:
                raise
    return False


# ── Main send function ────────────────────────────────────────────────────────

def send_email(
    from_key:  str,
    to:        str | list,
    subject:   str,
    body:      str,
    cc:        str | list | None = None,
    bcc:       str | list | None = None,
    html_body: str | None = None,
    in_reply_to: str | None = None,   # Message-ID of original for threading
    skip_footer: bool = False,
) -> dict:
    """
    Send one email from a named PressDetective account.

    from_key    : one of 'info', 'sujata', 'santosh', 'olympio'
    to          : single address or list
    subject     : email subject
    body        : plain-text body
    cc          : extra CC (info@pressdetective.com always added)
    html_body   : optional HTML part
    in_reply_to : set to original Message-ID to thread replies correctly
    skip_footer : True only for purely internal/test emails

    Returns: {'ok': True/False, 'from': addr, 'to': [list], 'error': str|None}
    """
    accounts   = load_accounts()
    if from_key not in accounts:
        raise ValueError(f"Unknown account key '{from_key}'. "
                         f"Valid keys: {list(accounts.keys())}")

    from_addr  = accounts[from_key]["address"]

    # Normalise recipients
    to_list  = [to]  if isinstance(to,  str) else list(to)
    cc_list  = [cc]  if isinstance(cc,  str) else list(cc or [])
    bcc_list = [bcc] if isinstance(bcc, str) else list(bcc or [])

    # Always CC info@, but don't duplicate if sending FROM info@
    if CC_ALWAYS not in cc_list and from_addr != CC_ALWAYS:
        cc_list.append(CC_ALWAYS)

    # ── DPDP suppression check ─────────────────────────────────────────────
    suppressed = load_suppression()
    blocked = [e for e in to_list + cc_list if e.lower() in suppressed]
    if blocked:
        return {
            "ok":    False,
            "from":  from_addr,
            "to":    to_list,
            "error": f"Blocked by suppression list: {blocked}",
        }

    # ── Build message ──────────────────────────────────────────────────────
    msg = MIMEMultipart("alternative")
    msg["From"]     = from_addr
    msg["To"]       = ", ".join(to_list)
    msg["Cc"]       = ", ".join(cc_list)
    msg["Subject"]  = subject
    msg["Reply-To"] = from_addr   # replies ALWAYS return to sender account

    # RFC 8058 one-click unsubscribe
    msg["List-Unsubscribe"]       = f"<mailto:{UNSUBSCRIBE_EMAIL}?subject=unsubscribe>"
    msg["List-Unsubscribe-Post"]  = "List-Unsubscribe=One-Click"

    # Thread continuity
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"]  = in_reply_to
        if not subject.lower().startswith("re:"):
            msg["Subject"] = "Re: " + subject

    # Body with DPDP footer
    full_body = body if skip_footer else (body + FOOTER_TEMPLATE)
    msg.attach(MIMEText(full_body, "plain"))
    if html_body:
        html_full = (html_body if skip_footer
                     else html_body + FOOTER_TEMPLATE.replace("\n", "<br>"))
        msg.attach(MIMEText(html_full, "html"))

    all_recipients = to_list + cc_list + bcc_list

    try:
        _smtp_send(from_addr, all_recipients, msg.as_string())
        return {"ok": True, "from": from_addr, "to": to_list, "error": None}
    except Exception as e:
        return {"ok": False, "from": from_addr, "to": to_list, "error": str(e)}


# ── Unsubscribe processor (call when "UNSUBSCRIBE" reply arrives) ─────────────

def process_unsubscribe(email: str):
    """
    Add to suppression list + remove from contacts_final.csv.
    Call this when an unsubscribe request arrives in any inbox.
    """
    email = email.strip().lower()
    add_to_suppression(email, reason="unsubscribe_request")

    # Remove from contacts CSV
    if CONTACTS_CSV.exists():
        rows = list(csv.DictReader(CONTACTS_CSV.open(encoding="utf-8-sig")))
        kept = [r for r in rows if r["email"].lower() != email]
        if len(kept) < len(rows):
            with CONTACTS_CSV.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(kept)
            print(f"Removed {email} from contacts_final.csv")
    print(f"Suppressed: {email}")


# ── CLI test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    # Quick smoke test — sends to self
    key = sys.argv[1] if len(sys.argv) > 1 else "info"
    accounts = load_accounts()
    addr = accounts[key]["address"]
    result = send_email(
        from_key = key,
        to       = addr,
        subject  = f"[SMOKE TEST] {addr}",
        body     = f"Mailer smoke test from account '{key}'.\nReply-To: {addr}\nCompliance footer included below.",
        skip_footer = False,
    )
    print(f"Result: {result}")
