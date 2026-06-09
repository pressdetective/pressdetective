#!/usr/bin/env python3
"""
monitor.py — Check pressdetective.com; alert info@pressdetective.com on failure/recovery.

Send chain: Proton Bridge -> ZeptoMail (first available wins).
In GitHub Actions (no Bridge): ZeptoMail is used automatically via ZEPTO_TOKEN.

Usage:
    python scripts/monitor.py              # single check
    python scripts/monitor.py --loop 600  # check every 600s

Env vars (all optional -- creds file used if not set):
    BRIDGE_PASS_INFO   Proton Bridge password for info@
    ZEPTO_TOKEN        ZeptoMail token (fallback when Bridge unavailable)
    SITE_URL           URL to check (default: https://pressdetective.com)
    ALERT_TO           Alert recipient (default: info@pressdetective.com)
    PREV_STATUS        "up" or "down" -- previous check result (for recovery alerts)
    TIMEOUT            HTTP timeout seconds (default: 15)
"""
import os, sys, time, socket, argparse, urllib.request, urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.mailer import send_mail, build_msg

SITE_URL = os.environ.get("SITE_URL",  "https://pressdetective.com")
ALERT_TO = os.environ.get("ALERT_TO",  "info@pressdetective.com")
TIMEOUT  = int(os.environ.get("TIMEOUT", "15"))


def check_site():
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


def alert(subject, body):
    msg = build_msg(from_addr="info@pressdetective.com", to=ALERT_TO,
                    subject=subject, body=body, cc="")
    if not send_mail(msg, account="info", providers=["bridge", "zepto"]):
        print("[monitor] WARNING: could not send alert -- all providers failed")


def run_once(prev_status):
    ok, code, ms, err = check_site()
    if ok:
        print(f"[monitor] OK  {SITE_URL}  HTTP {code}  {ms}ms")
        if prev_status == "down":
            alert("[RECOVERED] pressdetective.com is back up",
                  f"Site: {SITE_URL}\nStatus: HTTP {code}\nLatency: {ms}ms\n\nThe site has recovered.")
        return "up"
    else:
        status_str = f"HTTP {code}" if code else "unreachable"
        print(f"[monitor] DOWN  {SITE_URL}  {status_str}  {ms}ms  {err}", file=sys.stderr)
        if prev_status != "down":
            alert("[DOWN] pressdetective.com is not responding",
                  f"Site: {SITE_URL}\nStatus: {status_str}\nLatency: {ms}ms\nError: {err}\n\n"
                  f"Check: https://github.com/pressdetective/pressdetective/actions")
        return "down"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loop", type=int, default=0, metavar="SECS",
                    help="repeat every N seconds (0 = run once)")
    args = ap.parse_args()
    prev = os.environ.get("PREV_STATUS", "up")
    if args.loop:
        print(f"[monitor] Polling {SITE_URL} every {args.loop}s")
        while True:
            prev = run_once(prev)
            time.sleep(args.loop)
    else:
        sys.exit(0 if run_once(prev) == "up" else 1)


if __name__ == "__main__":
    main()
