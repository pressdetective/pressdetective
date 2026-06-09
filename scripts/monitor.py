#!/usr/bin/env python3
"""
monitor.py — Check pressdetective.com is live and email info@ on failure/recovery.

Usage (local):
    python scripts/monitor.py

Usage (GitHub Actions / CI):
    PROTON_TOKEN=<sujata or info token> python scripts/monitor.py

Env vars:
    PROTON_TOKEN   Proton SMTP token for FROM_ADDR (required in CI)
    PROTON_ADDR    Sender address (default: info@pressdetective.com)
    SITE_URL       URL to check (default: https://pressdetective.com)
    ALERT_TO       Alert recipient (default: info@pressdetective.com)
    TIMEOUT        Request timeout seconds (default: 15)
"""
import os, sys, smtplib, ssl, urllib.request, urllib.error, socket, time
from email.message import EmailMessage

SITE_URL   = os.environ.get("SITE_URL",    "https://pressdetective.com")
ALERT_TO   = os.environ.get("ALERT_TO",   "info@pressdetective.com")
FROM_ADDR  = os.environ.get("PROTON_ADDR", "info@pressdetective.com")
TOKEN      = os.environ.get("PROTON_TOKEN", "")
TIMEOUT    = int(os.environ.get("TIMEOUT", "15"))

SMTP_HOST  = "smtp.protonmail.ch"
SMTP_PORT  = 587


def check_site():
    """Returns (ok: bool, status_code: int|None, latency_ms: int, error: str)."""
    t0 = time.monotonic()
    try:
        req = urllib.request.Request(SITE_URL, headers={"User-Agent": "PressDetective-Monitor/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            latency = int((time.monotonic() - t0) * 1000)
            return True, r.status, latency, ""
    except urllib.error.HTTPError as e:
        latency = int((time.monotonic() - t0) * 1000)
        return False, e.code, latency, str(e)
    except (urllib.error.URLError, socket.timeout, Exception) as e:
        latency = int((time.monotonic() - t0) * 1000)
        return False, None, latency, str(e)


def send_alert(subject, body):
    if not TOKEN:
        print(f"[monitor] No PROTON_TOKEN — cannot send alert email.\nSubject: {subject}\n{body}")
        return
    msg = EmailMessage()
    msg["From"]    = FROM_ADDR
    msg["To"]      = ALERT_TO
    msg["Subject"] = subject
    msg.set_content(body)
    ctx = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(FROM_ADDR, TOKEN)
        s.send_message(msg)
    print(f"[monitor] Alert sent to {ALERT_TO}: {subject}")


def main():
    ok, code, latency_ms, err = check_site()

    if ok:
        print(f"[monitor] OK  {SITE_URL}  HTTP {code}  {latency_ms}ms")
        # In CI, GitHub sets PREV_STATUS via cache — send recovery if previously down
        prev = os.environ.get("PREV_STATUS", "up")
        if prev == "down":
            send_alert(
                f"[RECOVERED] pressdetective.com is back up",
                f"Site: {SITE_URL}\nStatus: HTTP {code}\nLatency: {latency_ms}ms\n\nThe site has recovered and is responding normally."
            )
        sys.exit(0)
    else:
        status_str = f"HTTP {code}" if code else "unreachable"
        print(f"[monitor] DOWN  {SITE_URL}  {status_str}  {latency_ms}ms  error={err}", file=sys.stderr)
        send_alert(
            f"[DOWN] pressdetective.com is not responding",
            f"Site: {SITE_URL}\nStatus: {status_str}\nLatency: {latency_ms}ms\nError: {err}\n\nPlease check https://github.com/pressdetective/pressdetective/actions for details."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
