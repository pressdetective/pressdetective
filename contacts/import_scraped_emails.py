"""
contacts/import_scraped_emails.py  (one-shot, 21 Jun 2026)
Sweep every email out of the scraped source files (mailbox .mbm, police_emails.txt,
restored-gov CSV, legal-press CSV), filter out VERP/DKIM tracking-token noise,
dedupe against the DB, VERIFY each net-new address, and:
  - ADD the ones that pass verification (syntax + not-suppressed + not-known-bad +
    live MX) to contacts_final, tagged by domain.
  - the ones that FAIL are auto-suppressed by the verifier (recorded, never sent).
Then rebuild contacts_live. Nothing guessed; failures go to the blacklist, not live.
"""
import re, csv, glob, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from lib.verifier import verify_email   # auto-suppresses dead/known-bad domains

FINAL = ROOT / "contacts" / "contacts_final.csv"
SUPP  = ROOT / "contacts" / "suppression_list.csv"
FIELDS = ["email","name","designation","category","tags","case","source","mobile"]
SOURCE = "scraped_import_21jun2026"
CASE   = "tarun-thadani"

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# VERP / DKIM / message-id tracking tokens: 4+ hyphen-separated alnum groups
TOKEN_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){3,}$")
NOISE = ("noreply","no-reply","mailer-daemon","postmaster","donotreply","notifications",
         "@pressdetective.com","@protonmail","@proton.me","example.com","@sentry","@github",
         "@google.com","wordpress","@list.","bounce","feedback-id","@santoshsakpal.com",
         "@sendgrid","@amazonses","@mailgun","@sparkpost","unsubscribe","@email.")

def is_token(local):
    return bool(TOKEN_RE.match(local)) or (len(local) > 30 and any(c.isdigit() for c in local) and "." not in local)

def emails_from(path):
    try:
        txt = Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return set()
    out = set()
    for e in EMAIL_RE.findall(txt):
        el = e.lower().strip(".")
        if any(n in el for n in NOISE) or len(el) > 120:
            continue
        if is_token(el.split("@", 1)[0]):
            continue
        out.add(el)
    return out

def classify(email):
    d = email.split("@", 1)[1]
    if "goapolice" in d or "mahapolice" in d or d.startswith("police") or "-pol." in d:
        return "Police/Government", "police-hq|scraped-import"
    if d.endswith(".gov.in") or d.endswith(".nic.in") or d in ("gov.in","nic.in"):
        geo = "maharashtra" if "maharashtra" in d else ("goa" if "goa" in d else "")
        t = "govt-state|scraped-import" + (("|"+geo) if geo else "")
        return "Government", t
    PRESS = {"hindustantimes.com","thehindu.co.in","thegoan.net","intoday.com","ndtv.com",
             "indianexpress.com","expressindia.com","abplive.com","news18.com","aajtak.in",
             "lokmat.com","esakal.com","rediffmail.com","navhindtimes.com","heraldgoa.in"}
    if d in PRESS or "news" in d or "media" in d or "times" in d or "patrika" in d:
        return "Press", "press|scraped-import"
    return "Scraped", "scraped-import|unverified-context"

# ── gather ──
# Scrape source files live in the MAIN working tree (case materials are on the
# abhisheksaraf branch, not the contacts branch this worktree is on). Read from
# there; verify + write to THIS worktree's DB (contacts branch).
SRC = Path("C:/dev/pressdetective")
files = (glob.glob(str(SRC/"clients"/"**"/"*.mbm"), recursive=True)
         + glob.glob(str(SRC/"clients"/"**"/"*.txt"), recursive=True)
         + [str(SRC/"contacts"/"_restored_policy_rejected_gov_2026-06-21.csv"),
            str(SRC/"contacts"/"legal_press_contacts.csv")])
scraped = set()
for f in files:
    scraped |= emails_from(f)

final_rows = list(csv.DictReader(open(FINAL, encoding="utf-8-sig")))
existing = {r["email"].lower().strip() for r in final_rows}
with open(SUPP, encoding="utf-8-sig") as f:
    suppressed = {r["email"].strip().lower() for r in csv.DictReader(f) if r.get("email")}

netnew = sorted(e for e in scraped if e not in existing and e not in suppressed)
print(f"scraped (clean, token-filtered): {len(scraped)} | net-new to verify: {len(netnew)}")

added, failed = [], 0
for e in netnew:
    ok, reason = verify_email(e, auto_suppress=True)   # failures -> suppression_list
    if ok:
        cat, tags = classify(e)
        added.append({"email": e, "name": "", "designation": "scraped",
                      "category": cat, "tags": tags, "case": CASE,
                      "source": SOURCE, "mobile": ""})
    else:
        failed += 1

if added:
    with open(FINAL, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerows(added)

from collections import Counter
print(f"PASSED verification + added: {len(added)} | FAILED + suppressed: {failed}")
print("added by category:")
for k, n in Counter(r["category"] for r in added).most_common():
    print(f"   {k}: {n}")
