#!/usr/bin/env python3
"""
scripts/clean_proton_bounces.py
--------------------------------
Scan every PressDetective Proton mailbox (via Proton Bridge IMAP) for delivery-
failure / postmaster notices (DSNs / bounces), blacklist the addresses that are
genuinely DEAD, and move ALL the bounce/postmaster notices to Trash so the inbox
stays clean.

Why this exists: SMTP "OK" != delivered. Hard bounces (user unknown, 5.1.x) come
back as mailer-daemon notices. Those dead recipients must be suppressed so the
verifier (lib/verifier.py) never mails them again -- and the notices are clutter.

CLASSIFICATION (evidence-based -- never blacklist on a guess):
  * dead    5.1.x / 5.2.x / "user unknown" / "does not exist"  -> BLACKLIST + trash
  * policy  5.7.x / "access denied" / "blocked" / "spam"       -> trash, KEEP address
            (address is valid; this is OUR sender reputation -- not the contact's fault)
  * temp    4.x.x / "try again" / "deferred" / "quota"         -> trash, KEEP address
  * unknown no parseable code/reason                            -> trash, KEEP address

Handles all three real formats seen in these mailboxes:
  * Proton/Postfix text bounce   "<addr>: host ... said:\n 550-5.1.1 ..." (multi-line)
  * Google structured DSN        message/delivery-status part (Final-Recipient/Status)
  * Google HTML-only DSN         delivery-status embedded as TEXT inside text/html

SAFE BY DEFAULT:
  * Default mode is read-only --scan: reports, changes NOTHING.
  * --apply blacklists DEAD addresses + MOVES every notice to Trash
    (recoverable ~30 days; never permanently expunged).
  * Never blacklists our own @pressdetective.com or Proton infra (@*.protonmail.ch).

Usage:
    python scripts/clean_proton_bounces.py                 # scan all (read-only)
    python scripts/clean_proton_bounces.py --apply         # blacklist + clean inbox
    python scripts/clean_proton_bounces.py --account santosh --verbose
    python scripts/clean_proton_bounces.py --folders INBOX,Spam,Archive
"""
import sys, re, csv, ssl, html, imaplib, email, email.policy, datetime, argparse, collections
from email.header import decode_header, make_header
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from lib.mailer import (bridge_password, account_address,
                        BRIDGE_IMAP_HOST, BRIDGE_IMAP_PORT)

SUPP = ROOT / "contacts" / "suppression_list.csv"
LIVE = ROOT / "contacts" / "contacts_live.csv"
SNAP = ROOT / "clients" / "olympio-almeida" / "olympio_appeal" / "contacts_live_snapshot.csv"

ALL_ACCOUNTS    = ["info", "santosh", "olympio", "sujata"]
DEFAULT_FOLDERS = ["INBOX", "Spam"]
OWN_DOMAINS     = {"pressdetective.com"}

DAEMON_HINTS  = ("mailer-daemon", "mailerdaemon", "mail-daemon", "postmaster",
                 "mail delivery", "maildelivery", "mdaemon", "mail delivery system",
                 "mail delivery subsystem", "mail administrator")
SUBJECT_HINTS = ("undelivered mail", "undeliverable", "mail delivery failed",
                 "delivery status notification", "returned mail", "failure notice",
                 "delivery has failed", "could not be delivered", "delivery failure",
                 "returned to sender", "delivery incomplete", "message not delivered",
                 "delivery delayed", "warning: message", "mail system error",
                 "address not found", "not delivered to")
DELAY_HINTS   = ("delay", "warning", "still trying", "not yet")

EMAIL    = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
EMAIL_RE = re.compile(EMAIL)
FULLCODE_RE = re.compile(r"\b([245])\.(\d{1,3})\.(\d{1,3})\b")
BARECODE_RE = re.compile(r"\b(4\d\d|5\d\d)\b")
# Postfix/Proton failed-recipient line: "<addr>: ..." or "<addr> (..."
FAILLINE_RE = re.compile(r"<(" + EMAIL + r")>\s*[:(]")
# Google prose: "wasn't delivered to <addr> because ..."
PROSE_RE = re.compile(r"(?i)(?:delivered to|deliver to|reach)\s+<?(" + EMAIL + r")>?")
# Where the returned ORIGINAL message starts -- never parse recipients past here.
ORIG_BOUNDARY_RE = re.compile(
    r"(content-type:\s*message/rfc822"
    r"|content-type:\s*text/rfc822-headers"
    r"|-{2,}\s*original message"
    r"|-{2,}\s*forwarded message"
    r"|this is a copy of (?:the|your) message"
    r"|below this line is a copy)", re.I)

DEAD_PHRASES   = ("user unknown", "does not exist", "doesn't exist", "no such user",
                  "no such recipient", "recipient not found", "address not found",
                  "mailbox not found", "invalid recipient", "recipient address rejected",
                  "mailbox unavailable", "mailbox does not exist", "user not found",
                  "unknown user", "no mailbox", "account disabled", "account is disabled",
                  "address rejected", "not a valid", "no such address", "unrouteable address",
                  "recipient rejected", "user doesn't exist", "user does not exist")
POLICY_PHRASES = ("access denied", "blocked", "spam", "reputation", "policy", "blacklist",
                  "blocklist", "not authorized", "quarantine", "rejected by", "5.7.",
                  "due to suspected", "message rejected", "content rejected", "banned")
TEMP_PHRASES   = ("temporar", "try again", "deferred", "delay", "over quota", "quota",
                  "mailbox full", "is full", "limit exceeded", "inode", "greylist",
                  "rate limit", "throttl", "timed out", "connection timed out",
                  "resources temporarily", "4.2.2")

RANK = {"dead": 3, "policy": 2, "temp": 1, "unknown": 0}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def dec(s):
    try:
        return str(make_header(decode_header(s or "")))
    except Exception:
        return s or ""


def is_own(addr):
    return "@" in addr and addr.rsplit("@", 1)[-1].lower() in OWN_DOMAINS


def is_internal(addr):
    if "@" not in addr:
        return True
    lp, dom = addr.split("@", 1)
    dom, lp = dom.lower(), lp.lower()
    if dom == "protonmail.ch" or dom.endswith(".protonmail.ch"):
        return True
    return lp in ("mailer-daemon", "postmaster") or lp.startswith("mailer-daemon")


def grp(pattern, text):
    m = re.search(pattern, text or "", re.I)
    return m.group(1).strip() if m else ""


def classify(text, default="unknown"):
    """Return dead | policy | temp | unknown from an SMTP diagnostic window."""
    t = (text or "").lower()
    codes = FULLCODE_RE.findall(text or "")                 # list of (cls, sub, det)
    if any(c == "4" for c, _, _ in codes):
        return "temp"
    if any(w in t for w in TEMP_PHRASES):
        return "temp"
    for c, s, d in codes:                                   # enhanced status codes
        if c == "5" and s == "1":
            return "dead"                                   # 5.1.x bad address (definitive)
        if c == "5" and s == "2":
            return "dead" if d == "1" else "temp"           # 5.2.1 disabled=dead; 5.2.2 full=transient
        if c == "5" and s == "7":
            return "policy"                                 # 5.7.x policy / reputation
        if c == "5" and s == "4":
            return "temp"                                   # 5.4.x routing/network
    if any(w in t for w in DEAD_PHRASES):
        return "dead"
    if "relay" in t and ("denied" in t or "disallow" in t or "not permitted" in t):
        return "policy"                                     # relay refusal != dead mailbox
    if any(w in t for w in POLICY_PHRASES):
        return "policy"
    if re.search(r"\b(550|551|553)\b", t):                  # bare permanent codes
        return "dead"
    if re.search(r"\b(554)\b", t):
        return "dead" if any(w in t for w in DEAD_PHRASES) else "policy"
    if re.search(r"\b(421|450|451|452)\b", t):
        return "temp"
    return default


def get_report_text(msg):
    """Human-readable report text (plain + html-stripped), original message cut off."""
    plain, htmls = [], []
    for part in msg.walk():
        ct = part.get_content_type()
        if ct == "text/plain":
            try:
                plain.append(part.get_content())
            except Exception:
                plain.append((part.get_payload(decode=True) or b"").decode("utf-8", "replace"))
        elif ct == "text/html":
            try:
                raw = part.get_content()
            except Exception:
                raw = (part.get_payload(decode=True) or b"").decode("utf-8", "replace")
            raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
            raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
            raw = re.sub(r"(?i)</(p|div|tr|li|h[1-6])>", "\n", raw)
            raw = re.sub(r"<[^>]+>", " ", raw)
            htmls.append(re.sub(r"[ \t]+", " ", html.unescape(raw)))
    text = "\n".join(plain + htmls)
    cut = ORIG_BOUNDARY_RE.search(text)
    return text[:cut.start()] if cut else text


def extract_failures(msg):
    """Returns (looks_bounce, {email: {status, diag, kind}}) with kind in RANK."""
    frm  = dec(msg.get("From", "")).lower()
    subj = dec(msg.get("Subject", "")).lower()
    from_daemon  = any(h in frm for h in DAEMON_HINTS)
    subject_hint = any(h in subj for h in SUBJECT_HINTS)
    default_kind = "temp" if any(h in subj for h in DELAY_HINTS) else "unknown"

    failures, is_dsn = {}, False

    def add(addr, status, diag, kind):
        addr = (addr or "").strip().strip("<>.").lower()
        if not addr or "@" not in addr or is_own(addr) or is_internal(addr):
            return
        prev = failures.get(addr)
        if prev is None or RANK[kind] > RANK[prev["kind"]]:
            failures[addr] = {"status": status, "diag": (diag or "").strip()[:200], "kind": kind}

    # 1) structured message/delivery-status MIME parts
    for part in msg.walk():
        if part.get_content_type() == "message/delivery-status":
            is_dsn = True

    # 2) parse the report text (covers Postfix text, Google HTML-embedded, structured-as-text)
    report = get_report_text(msg)

    #   2a) RFC-3464 fields wherever they appear in the text
    for chunk in re.split(r"(?i)Final-Recipient:", report)[1:]:
        window = chunk[:500]
        addr = grp(r"^\s*[^;\n]*;\s*(" + EMAIL + r")", window)
        if not addr:
            continue
        is_dsn = True
        action = grp(r"Action:\s*(\w+)", window).lower()
        if action == "delivered":
            continue
        status = grp(r"Status:\s*([245]\.\d{1,3}\.\d{1,3})", window)
        diag   = grp(r"Diagnostic-Code:\s*(.+)", window)
        kind = classify(status + " " + diag, default=default_kind)
        if action == "delayed" and kind == "unknown":
            kind = "temp"
        add(addr, status, diag, kind)

    #   2b) Postfix "<addr>: ..." failure lines, with a TIGHTLY-bounded diagnostic window.
    #   The window ends at the earliest of: blank line (end of this recipient's block),
    #   next "<addr>:" line, start of the structured section, or a hard char cap --
    #   so one recipient's verdict never bleeds in from another's Status code.
    matches = list(FAILLINE_RE.finditer(report))
    for i, m in enumerate(matches):
        seg = report[m.start():]
        end = min(len(seg), 320)
        nb = re.search(r"\n[ \t]*\n", seg)
        if nb:
            end = min(end, nb.start())
        if i + 1 < len(matches):
            end = min(end, matches[i + 1].start() - m.start())
        fr = re.search(r"(?i)final-recipient:", seg)
        if fr:
            end = min(end, fr.start())
        window = seg[:end]
        add(m.group(1), grp(r"([245]\.\d{1,3}\.\d{1,3})", window), window[:200],
            classify(window, default=default_kind))

    #   2c) Google prose fallback ("wasn't delivered to <addr> ...")
    if not failures and (from_daemon or subject_hint):
        for m in PROSE_RE.finditer(report):
            window = report[m.start():m.start() + 600]
            add(m.group(1), grp(r"([245]\.\d{1,3}\.\d{1,3})", window), window[:200],
                classify(window, default=default_kind))

    looks_bounce = is_dsn or from_daemon or subject_hint
    return looks_bounce, failures


# --------------------------------------------------------------------------- #
# IMAP
# --------------------------------------------------------------------------- #
SEARCHES = [
    '(FROM "mailer-daemon")', '(FROM "postmaster")', '(FROM "mail delivery")',
    '(FROM "maildelivery")', '(HEADER Content-Type "delivery-status")',
    '(SUBJECT "undeliverable")', '(SUBJECT "undelivered")',
    '(SUBJECT "delivery status notification")', '(SUBJECT "mail delivery failed")',
    '(SUBJECT "failure notice")', '(SUBJECT "returned mail")',
    '(SUBJECT "could not be delivered")', '(SUBJECT "delivery has failed")',
    '(SUBJECT "message not delivered")', '(SUBJECT "returned to sender")',
    '(SUBJECT "address not found")',
]


def connect(account):
    addr = account_address(account)
    pw   = bridge_password(account)
    if not pw:
        raise RuntimeError(f"no bridge password configured for account {account!r}")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    M = imaplib.IMAP4(BRIDGE_IMAP_HOST, BRIDGE_IMAP_PORT)
    M.starttls(ssl_context=ctx)
    M.login(addr, pw)
    return M, addr


def candidate_uids(M):
    uids = set()
    for crit in SEARCHES:
        try:
            typ, data = M.uid("SEARCH", None, crit)
            if typ == "OK" and data and data[0]:
                uids.update(data[0].split())
        except Exception:
            pass
    return sorted(uids, key=lambda b: int(b))


def move_to_trash(M, uid):
    try:
        typ, _ = M.uid("MOVE", uid, "Trash")
        if typ == "OK":
            return True
    except Exception:
        pass
    try:
        M.uid("COPY", uid, "Trash")
        M.uid("STORE", uid, "+FLAGS", r"(\Deleted)")
        M.expunge()
        return True
    except Exception as e:
        print(f"      ! could not move uid {uid.decode()}: {e}")
        return False


# --------------------------------------------------------------------------- #
# suppression list
# --------------------------------------------------------------------------- #
def load_suppressed():
    if not SUPP.exists():
        return set()
    with open(SUPP, encoding="utf-8-sig") as f:
        return {r["email"].strip().lower() for r in csv.DictReader(f) if r.get("email")}


def append_suppressions(rows):
    today = datetime.date.today().isoformat()
    with open(SUPP, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for email_addr, reason in rows:
            reason = re.sub(r"\s+", " ", str(reason)).strip()[:120]   # keep reason single-line
            w.writerow([email_addr.strip().lower(), reason, today, "proton_imap"])
    return len(rows)


def remove_from_csv(path, bad_set):
    if not path.exists():
        return 0, 0
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    if not rows:
        return 0, 0
    keep = [r for r in rows if r.get("email", "").strip().lower() not in bad_set]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(keep)
    return len(rows), len(keep)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def process_account(account, folders, apply, verbose, no_trash=False):
    res = {"account": account, "dead": {}, "policy": set(), "temp": set(),
           "unknown_msgs": 0, "trashed": 0, "notices": 0, "error": None}
    mutate = apply and not no_trash       # only select read-write when we will move messages
    try:
        M, addr = connect(account)
    except Exception as e:
        res["error"] = str(e)
        print(f"\n### {account:<8} — CONNECT FAILED: {e}")
        return res

    print(f"\n### {account:<8} <{addr}>")
    try:
        for folder in folders:
            try:
                typ, _ = M.select(f'"{folder}"', readonly=not mutate)
                if typ != "OK":
                    continue
            except Exception:
                continue
            uids = candidate_uids(M)
            if not uids:
                print(f"  {folder:<10} no candidate messages")
                continue
            to_trash, n_dead = [], 0
            for uid in uids:
                try:
                    typ, raw = M.uid("FETCH", uid, "(RFC822)")
                    if typ != "OK" or not raw or not raw[0]:
                        continue
                    msg = email.message_from_bytes(raw[0][1], policy=email.policy.default)
                except Exception:
                    continue
                looks_bounce, failures = extract_failures(msg)
                if not looks_bounce:
                    continue
                res["notices"] += 1
                to_trash.append(uid)
                dead = {a: i for a, i in failures.items() if i["kind"] == "dead"}
                if dead:
                    n_dead += 1
                    for a, i in dead.items():
                        res["dead"].setdefault(a, i["diag"] or i["status"] or "hard_bounce")
                    if verbose:
                        for a, i in dead.items():
                            print(f"      DEAD {a:<44} {i['status']:<8} {i['diag'][:48]}")
                res["policy"].update(a for a, i in failures.items() if i["kind"] == "policy")
                res["temp"].update(a for a, i in failures.items() if i["kind"] == "temp")
                if not failures:
                    res["unknown_msgs"] += 1
            print(f"  {folder:<10} {len(uids):>4} candidates | notices w/dead-addr: {n_dead}")
            if mutate and to_trash:
                moved = sum(move_to_trash(M, uid) for uid in to_trash)
                res["trashed"] += moved
                print(f"  {folder:<10} moved {moved}/{len(to_trash)} notice(s) to Trash")
    finally:
        try:
            M.logout()
        except Exception:
            pass
    return res


def main():
    ap = argparse.ArgumentParser(description="Clean Proton bounce/postmaster notices + blacklist dead addresses.")
    ap.add_argument("--apply", action="store_true", help="blacklist dead addrs + move notices to Trash")
    ap.add_argument("--no-trash", action="store_true", help="with --apply: blacklist only, do NOT move any mail")
    ap.add_argument("--account", help="single account; default: all")
    ap.add_argument("--folders", default=",".join(DEFAULT_FOLDERS))
    ap.add_argument("--verbose", action="store_true", help="print each dead recipient + diagnostic")
    args = ap.parse_args()

    accounts = [args.account] if args.account else ALL_ACCOUNTS
    folders  = [f.strip() for f in args.folders.split(",") if f.strip()]
    if not args.apply:
        mode = "SCAN (read-only — nothing changes)"
    elif args.no_trash:
        mode = "APPLY (blacklist only — no mail moved)"
    else:
        mode = "APPLY (blacklist + move notices to Trash)"

    print("=" * 72)
    print(f"Proton bounce cleanup — {datetime.date.today()} — {mode}")
    print(f"Accounts: {', '.join(accounts)}   Folders: {', '.join(folders)}")
    print("=" * 72)

    results = [process_account(a, folders, args.apply, args.verbose, args.no_trash) for a in accounts]

    dead, policy, temp = {}, set(), set()
    trashed = notices = unknown_msgs = 0
    for r in results:
        dead.update(r["dead"]); policy.update(r["policy"]); temp.update(r["temp"])
        trashed += r["trashed"]; notices += r["notices"]; unknown_msgs += r["unknown_msgs"]
    policy -= set(dead); temp -= set(dead) | policy        # a dead addr trumps weaker verdicts

    existing = load_suppressed()
    new_bad  = sorted(e for e in dead if e not in existing)
    dom_tally = collections.Counter(e.rsplit("@", 1)[-1] for e in dead).most_common(15)

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Bounce/postmaster notices found ........ {notices}")
    print(f"  DEAD addresses (blacklist) ............. {len(dead)}  ({len(new_bad)} new)")
    print(f"  Policy/reputation rejects (KEPT) ....... {len(policy)}")
    print(f"  Transient/delayed (KEPT) ............... {len(temp)}")
    print(f"  Notices with no parseable address ...... {unknown_msgs}")
    if dom_tally:
        print("\n  DEAD addresses by domain (this is WHY the inbox fills up):")
        for dom, n in dom_tally:
            print(f"    {n:>4}  @{dom}")
    if policy:
        print(f"\n  Policy/reputation rejects NOT blacklisted (valid addrs — fix sender rep, don't drop):")
        for e in sorted(policy)[:25]:
            print(f"    {e}")
        if len(policy) > 25:
            print(f"    ... +{len(policy) - 25} more")

    if not args.apply:
        if new_bad:
            print(f"\n  New DEAD addresses that WOULD be blacklisted ({len(new_bad)}):")
            for e in new_bad:
                print(f"    {e:<46} {str(dead[e])[:44]}")
        print("\n  [SCAN ONLY] Re-run with --apply to blacklist DEAD addrs and move all notices to Trash.")
        return

    if new_bad:
        append_suppressions([(e, f"proton_bounce:{(str(dead[e])[:38] or 'hard_bounce').strip()}") for e in new_bad])
        bad_set = set(dead) | existing
        b1, a1 = remove_from_csv(LIVE, bad_set)
        remove_from_csv(SNAP, bad_set)
        print(f"\n  Blacklisted {len(new_bad)} new DEAD address(es) -> suppression_list.csv")
        print(f"  contacts_live.csv pruned: {b1} -> {a1}")
    else:
        print("\n  No new dead addresses to blacklist (all already suppressed).")
    print(f"  Bounce/postmaster notices moved to Trash: {trashed}")
    print("\n  Done — inbox cleaned. (Trash auto-purges in ~30 days; recoverable until then.)")


if __name__ == "__main__":
    main()
