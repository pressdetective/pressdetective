#!/usr/bin/env python3
"""
monitor.py — Check pressdetective.com is live; alert info@pressdetective.com via Proton Bridge.

Keep Proton Bridge running locally before running this script.

Bridge settings:
    Host:     127.0.0.1
    Port:     1025
    User:     info@pressdetective.com
    Password: stored in .creds/proton_accounts.json (bridge_password for "info")
    TLS:      STARTTLS

Usage:
    python scripts/monitor.py              # single check
    python scripts/monitor.py --loop 600  # check every 600 seconds

Env var overrides:
    SITE_URL      URL to check          (default: https://pressdetective.com)
    ALERT_TO      Alert recipient       (default: info@pressdetective.com)
    BRIDGE_PASS   Bridge password       (overrides .creds file)
    TIMEOUT       HTTP timeout seconds  (default: 15)
"""
import os, sys, json, smtplib, ssl, urllib.request, urllib.error, socket, time, argparse

ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE = os.path.join(ROOT, ".creds", "proton_accounts.json")

SITE_URL   = os.environ.get("SITE_URL",  "https://pressdetective.com")
ALERT_TO   = os.environ.get("ALERT_TO",  "info@pressdetective.com")
FROM_ADDR  = "info@pressdetective.com"
TIMEOUT    = int(os.environ.get("TIMEOUT", "15"))

BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 1025


def load_bridge_password():
    override = os.environ.get("BRIDGE_PASS", "")
    if override:
        return override
    try:
        with open(CREDS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        pw = data["accounts"]["info"].get("bridge_password", "")
        if not pw:
            raise ValueError("bridge_password not set for 'info' in proton_accounts.json")
        return pw
    except FileNotFoundError:
        raise SystemExit(f"ERROR: {CREDS_FILE} not found. Create it or set BRIDGE_PASS env var.")


def check_site():
    """Returns (ok, status_code|None, latency_ms, error_str)."""
    t0 = time.monotonic()
    try:
        req = urllib.request.Request(SITE_URL, headers={"User-Agent": "PressDetective-Monitor/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            ms = int((time.monotonic() - t0) * 1000)
            return True, r.status, ms, ""
    except urllib.error.HTTPError as e:
        ms = int((time.monotonic() - t0) * 1000)
        return False, e.code, ms, str(e)
    except (urllib.error.URLError, socket.timeout, Exception) as e:
        ms = int((time.monotonic() - t0) * 1000)
        return False, None, ms, str(e)


def send_alert(subject, body, password):
    msg_obj = __import__("email.message", fromlist=["EmailMessage"]).EmailMessage()
    msg_obj["From"]    = FROM_ADDR
    msg_obj["To"]      = ALERT_TO
    msg_obj["Subject"] = subject
    msg_obj.set_content(body)
    ctx = ssl.create_default_context()
    with smtplib.SMTP(BRIDGE_HOST, BRIDGE_PORT) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.login(FROM_ADDR, password)
        s.send_message(msg_obj)
    print(f"[monitor] Alert sent → {ALERT_TO}: {subject}")


def run_once(password, prev_status):
    ok, code, ms, err = check_site()
    if ok:
        print(f"[monitor] OK  {SITE_URL}  HTTP {code}  {ms}ms")
        if prev_status == "down":
            send_alert(
                "[RECOVERED] pressdetective.com is back up",
                f"Site: {SITE_URL}\nStatus: HTTP {code}\nLatency: {ms}ms\n\nThe site has recovered and is responding normally."
                , password
            )
        return "up"
    else:
        status_str = f"HTTP {code}" if code else "unreachable"
        print(f"[monitor] DOWN  {SITE_URL}  {status_str}  {ms}ms  {err}", file=sys.stderr)
        if prev_status != "down":
            send_alert(
                "[DOWN] pressdetective.com is not responding",
                f"Site: {SITE_URL}\nStatus: {status_str}\nLatency: {ms}ms\nError: {err}\n\nPlease check https://pressdetective.com and your GitHub Pages settings."
                , password
            )
        return "down"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loop", type=int, default=0, metavar="SECS",
                    help="repeat check every N seconds (0 = single check)")
    args = ap.parse_args()

    password   = load_bridge_password()
    prev       = "up"

    if args.loop:
        print(f"[monitor] Polling {SITE_URL} every {args.loop}s via Bridge {BRIDGE_HOST}:{BRIDGE_PORT}")
        while True:
            prev = run_once(password, prev)
            time.sleep(args.loop)
    else:
        prev = run_once(password, prev)
        sys.exit(0 if prev == "up" else 1)


if __name__ == "__main__":
    main()
