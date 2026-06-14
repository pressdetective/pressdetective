"""
Verify pressdetective.com email-auth DNS is correct.
Run this AFTER removing the duplicate DMARC record. Exit 0 = fixed.
    python clients/olympio-almeida/olympio_appeal/verify_dmarc_fix.py
"""
import sys
try:
    import dns.resolver
except ImportError:
    print("pip install dnspython"); sys.exit(2)

DOMAIN = "pressdetective.com"
def q(name, rt):
    try:
        return [r.to_text().strip('"') for r in dns.resolver.resolve(name, rt)]
    except Exception:
        return []

ok = True

# 1) DMARC — must be exactly ONE v=DMARC1 record
dmarc = [x for x in q(f"_dmarc.{DOMAIN}", "TXT") if "DMARC1" in x.replace('" "','')]
# join split strings
dmarc_raw = q(f"_dmarc.{DOMAIN}", "TXT")
n_dmarc = sum(1 for x in dmarc_raw if x.replace('" "','').lstrip().startswith("v=DMARC1"))
print(f"DMARC records: {n_dmarc}")
for x in dmarc_raw: print(f"    {x}")
if n_dmarc == 1:
    print("  PASS — exactly one DMARC record")
else:
    print(f"  FAIL — must be exactly 1 (found {n_dmarc}). Delete the duplicate.")
    ok = False

# 2) SPF — single v=spf1 including Proton
spf = [x for x in q(DOMAIN, "TXT") if x.lstrip().startswith("v=spf1")]
print(f"\nSPF records: {len(spf)}")
for x in spf: print(f"    {x}")
if len(spf) == 1 and "_spf.protonmail.ch" in spf[0]:
    print("  PASS — single SPF, includes Proton")
else:
    print("  WARN — expected 1 SPF record including _spf.protonmail.ch")
    if len(spf) != 1: ok = False

# 3) DKIM — Proton selector present
dkim = q(f"protonmail._domainkey.{DOMAIN}", "CNAME") or q(f"protonmail._domainkey.{DOMAIN}", "TXT")
print(f"\nDKIM (protonmail selector): {dkim if dkim else '(none)'}")
if dkim and "proton" in dkim[0].lower():
    print("  PASS — Proton DKIM selector resolves")
else:
    print("  WARN — Proton DKIM selector not found")

print("\n" + ("="*50))
print("RESULT:", "ALL CLEAR — safe to re-send to government" if ok else "NOT FIXED YET — apply the DNS change first")
sys.exit(0 if ok else 1)
