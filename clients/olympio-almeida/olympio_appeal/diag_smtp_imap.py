"""
DIAGNOSTIC — Proton SMTP + IMAP for olympio.almeida@pressdetective.com
Tests:
  1. SMTP auth (does login succeed?)
  2. Sends ONE test email TO info@pressdetective.com (not BCC)
  3. Reads Bridge IMAP sent folder to list the 10 most recent sent items
     and confirm CC shows up in headers

    python clients/olympio-almeida/olympio_appeal/diag_smtp_imap.py
"""

# --- blacklist/no-contact/DNS guard: filters EVERY smtplib send (see lib/presend_guard) ---
import sys as _sys, pathlib as _pathlib
for _anc in _pathlib.Path(__file__).resolve().parents:
    if (_anc / "lib" / "presend_guard.py").exists():
        _sys.path.insert(0, str(_anc)); break
import lib.presend_guard  # noqa: F401
import json, smtplib, ssl, imaplib, email as emaillib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import datetime

ROOT  = Path(__file__).parent.parent.parent.parent
CREDS = json.loads((ROOT / ".creds" / "proton_accounts.json").read_text(encoding="utf-8-sig"))

FROM_ADDR = "olympio.almeida@pressdetective.com"
FROM_NAME = "Olympio Almeida"
TOKEN     = CREDS["accounts"]["olympio"]["token"]
BRIDGE_PW = CREDS["accounts"]["olympio"]["bridge_password"]
CC_INFO   = "info@pressdetective.com"

print("="*60)
print("STEP 1 — SMTP AUTH TEST")
print("="*60)
ctx = ssl.create_default_context()
try:
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=20) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.login(FROM_ADDR, TOKEN)
        print(f"  PASS — logged in as {FROM_ADDR}")
except Exception as e:
    print(f"  FAIL — {e}")
    print("  >>> TOKEN may be expired/wrong. Check .creds/proton_accounts.json")

print()
print("="*60)
print("STEP 2 — SEND TEST EMAIL TO info@pressdetective.com (TO field, not BCC)")
print("="*60)
m = MIMEMultipart("alternative")
m["Subject"] = f"[DIAG TEST] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} — SMTP working"
m["From"]    = f"{FROM_NAME} <{FROM_ADDR}>"
m["To"]      = CC_INFO        # <-- TO the info address directly
m["Cc"]      = CC_INFO        # <-- also CC (same, to confirm CC header is preserved)
body = (
    "This is an automated diagnostic test from PressDetective.\n"
    "If you see this in info@pressdetective.com, SMTP is working.\n"
    "Check the To: and Cc: headers on this message to confirm they are visible.\n"
    f"\nSent: {datetime.datetime.now().isoformat()}\n"
)
m.attach(MIMEText(body, "plain", "utf-8"))
rcpts = [CC_INFO, FROM_ADDR]
try:
    ctx2 = ssl.create_default_context()
    with smtplib.SMTP("smtp.protonmail.ch", 587, timeout=20) as s:
        s.ehlo(); s.starttls(context=ctx2); s.login(FROM_ADDR, TOKEN)
        s.sendmail(FROM_ADDR, rcpts, m.as_bytes())
    print(f"  PASS — test email submitted to Proton SMTP")
    print(f"  TO:  {CC_INFO}")
    print(f"  CC:  {CC_INFO}")
    print(f"  (check info@pressdetective.com inbox — should arrive within 60 seconds)")
except Exception as e:
    print(f"  FAIL — {e}")

print()
print("="*60)
print("STEP 3 — READ BRIDGE IMAP SENT FOLDER (10 most recent)")
print("="*60)
try:
    ctx3 = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx3.check_hostname = False; ctx3.verify_mode = ssl.CERT_NONE
    with imaplib.IMAP4("127.0.0.1", 1143) as M:
        M.starttls(ssl_context=ctx3)
        M.login(FROM_ADDR, BRIDGE_PW)
        # List folders to find Sent
        _, lst = M.list()
        folders = [l.decode() for l in lst]
        sent_folder = None
        for f in folders:
            if "Sent" in f or "sent" in f:
                sent_folder = f.split('"')[-2] if '"' in f else f.split()[-1]
                break
        if not sent_folder:
            print("  Could not find Sent folder. Folders available:")
            for f in folders: print(f"    {f}")
        else:
            print(f"  Sent folder: {sent_folder}")
            M.select(f'"{sent_folder}"', readonly=True)
            _, data = M.search(None, "ALL")
            ids = data[0].split()
            recent = ids[-10:] if len(ids) >= 10 else ids
            print(f"  Total in Sent: {len(ids)}  | Showing last {len(recent)}")
            print()
            for uid in reversed(recent):
                _, msg_data = M.fetch(uid, "(BODY[HEADER.FIELDS (DATE SUBJECT TO CC BCC)])")
                raw = msg_data[0][1].decode("utf-8", errors="replace")
                # parse subject, to, cc
                parsed = emaillib.message_from_string(raw)
                subj = (parsed.get("Subject","(none)") or "(none)")[:60]
                to_  = (parsed.get("To","") or "")[:80]
                cc_  = (parsed.get("Cc","") or "")[:80]
                bcc_ = (parsed.get("Bcc","") or "(stripped by Proton — normal)")[:80]
                date_= (parsed.get("Date","") or "")[:40]
                print(f"  [{uid.decode()}] {date_}")
                print(f"    Subject: {subj}")
                print(f"    To:      {to_}")
                print(f"    Cc:      {cc_}")
                print(f"    Bcc:     {bcc_}")
                print()
except Exception as e:
    print(f"  IMAP FAIL — {e}")
    print("  (Proton Bridge must be running on 127.0.0.1:1143)")

print("="*60)
print("NOTES:")
print("  - BCC recipients are ALWAYS stripped from Sent copies by Proton (by design).")
print("    This is why the sent folder shows no BCC list — it is normal.")
print("  - To: and Cc: should be visible in the sent copy header.")
print("  - If SMTP fails, the token in .creds/proton_accounts.json is wrong/expired.")
print("="*60)
