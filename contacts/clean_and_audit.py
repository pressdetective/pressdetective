#!/usr/bin/env python3
"""
clean_and_audit.py
One-shot cleanup + verification + full audit of the PressDetective contacts DB.

CLEAN:
  1. Normalise every row: lowercase+strip email, strip all fields,
     normalise tags (lowercase, '|'-sep, dedupe within row, drop empties).
  2. Collapse duplicate emails (case-insensitive), unioning tags + keeping
     the most complete name/designation/category/mobile.
  3. Quarantine syntactically-invalid emails to contacts_invalid.csv.

VERIFY:
  4. Live MX/A check on every unique domain (public resolvers 8.8.8.8/1.1.1.1,
     retry once). Dead domains -> suppression_list (reason=dead_domain).
  5. Rebuild contacts_live.csv = final  minus  (suppressed ∪ invalid).
  6. Integrity asserts: 0 dup, 0 suppressed-in-live, 0 bad-syntax-in-live.

AUDIT:
  7. Full summary: totals, by category / case / geography / source,
     suppression breakdown, phone coverage, top tags. Writes tag_summary.csv.
"""

import csv, re, sys, socket
from pathlib import Path
from collections import Counter, OrderedDict, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import dns.resolver
except ImportError:
    print("pip install dnspython"); sys.exit(1)

BASE   = Path(__file__).parent.parent / "contacts"
FINAL  = BASE / "contacts_final.csv"
LIVE   = BASE / "contacts_live.csv"
SUPP   = BASE / "suppression_list.csv"
INVALID= BASE / "contacts_invalid.csv"
TAGSUM = BASE / "tag_summary.csv"
HEADER = ["email","name","designation","category","tags","case","source","mobile"]
EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

_r = dns.resolver.Resolver()
_r.nameservers = ['8.8.8.8','1.1.1.1','8.8.4.4']
_r.timeout = 5; _r.lifetime = 8
_mx = {}

def domain_alive(d):
    if d in _mx: return _mx[d]
    for attempt in range(2):
        try: _r.resolve(d,'MX'); _mx[d]=True; return True
        except Exception:
            try: _r.resolve(d,'A'); _mx[d]=True; return True
            except Exception:
                if attempt==0: continue
                _mx[d]=False; return False

def norm_tags(s):
    parts = re.split(r'[|,;]', s or '')
    out, seen = [], set()
    for t in parts:
        t = t.strip().lower().replace(' ', '-')
        if t and t not in seen:
            seen.add(t); out.append(t)
    return '|'.join(out)

def load_supp():
    recs = OrderedDict()
    if SUPP.exists():
        for r in csv.DictReader(SUPP.open(encoding='utf-8-sig')):
            e=(r.get('email','') or '').strip().lower()
            if e: recs[e]=r
    return recs

def main():
    rows = list(csv.DictReader(FINAL.open(encoding='utf-8-sig')))
    print(f"Loaded {len(rows)} rows from contacts_final.csv\n")

    # ── 1+2 normalise + dedupe ────────────────────────────────────────────
    merged = OrderedDict(); invalid=[]; dup=0
    for r in rows:
        e = (r.get('email','') or '').strip().lower()
        row = {k:(r.get(k,'') or '').strip() for k in HEADER}
        row['email']=e; row['tags']=norm_tags(row['tags'])
        if not e: continue
        if not EMAIL_RE.match(e):
            invalid.append(row); continue
        if e in merged:
            dup += 1
            m=merged[e]
            for fld in ('name','designation','category','mobile'):
                if len(row[fld])>len(m[fld]): m[fld]=row[fld]
            m['tags']=norm_tags(m['tags']+'|'+row['tags'])
            if (m['case'] or 'general').lower()=='general' and row['case'] and row['case'].lower()!='general':
                m['case']=row['case']
            srcs=[s for s in (m['source'].split(',')+[row['source']]) if s.strip()]
            m['source']=','.join(OrderedDict.fromkeys(srcs))
        else:
            merged[e]=row
    print(f"  normalised tags + fields | duplicates collapsed: {dup} | invalid syntax: {len(invalid)}")

    out=list(merged.values())
    FINAL.write_text('', encoding='utf-8')  # truncate then write
    with FINAL.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=HEADER,extrasaction='ignore'); w.writeheader(); w.writerows(out)
    if invalid:
        with INVALID.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=HEADER,extrasaction='ignore'); w.writeheader(); w.writerows(invalid)
        print(f"  quarantined {len(invalid)} invalid -> contacts_invalid.csv")

    # ── 4 DNS verify ──────────────────────────────────────────────────────
    domains=sorted({r['email'].split('@')[1] for r in out if '@' in r['email']})
    print(f"\nVerifying {len(domains)} unique domains (public DNS, parallel)...")
    dead=set(); done=0
    with ThreadPoolExecutor(max_workers=25) as pool:
        fut={pool.submit(domain_alive,d):d for d in domains}
        for f in as_completed(fut):
            d=fut[f]; done+=1
            if not f.result(): dead.add(d)
            if done%150==0: print(f"  {done}/{len(domains)} checked, {len(dead)} dead")
    print(f"  dead domains: {len(dead)}")

    supp=load_supp()
    import datetime
    today=datetime.date.today().isoformat()
    newdead=0
    for r in out:
        d=r['email'].split('@')[1] if '@' in r['email'] else ''
        if d in dead and r['email'] not in supp:
            supp[r['email']]={'email':r['email'],'reason':'dead_domain','date':today,'source':'clean_and_audit'}
            newdead+=1
    if newdead:
        with SUPP.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['email','reason','date','source'],extrasaction='ignore')
            w.writeheader()
            for e,rec in sorted(supp.items()):
                rec['email']=e; w.writerow(rec)
        print(f"  +{newdead} dead-domain emails suppressed")

    # ── 5 rebuild live ────────────────────────────────────────────────────
    supp_set=set(supp.keys())
    live=[r for r in out if r['email'] not in supp_set]
    with LIVE.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=HEADER,extrasaction='ignore'); w.writeheader(); w.writerows(live)

    # ── 6 integrity ───────────────────────────────────────────────────────
    dups=[e for e,c in Counter(r['email'] for r in live).items() if c>1]
    leak=[r['email'] for r in live if r['email'] in supp_set]
    bad =[r['email'] for r in live if not EMAIL_RE.match(r['email'])]
    print(f"\nINTEGRITY  dup-in-live={len(dups)}  suppressed-in-live={len(leak)}  bad-syntax-in-live={len(bad)}")

    # ── 7 audit summary ───────────────────────────────────────────────────
    def geo(r):
        b=(r['tags']+' '+r['category']+' '+r['designation']+' '+r['source']).lower()
        if 'goa' in b: return 'Goa'
        if any(x in b for x in ['mumbai','bombay','mahapolice','maharashtra','thane','pune','nagpur','nashik']): return 'Maharashtra/Mumbai'
        if any(x in b for x in ['reuters','bloomberg','bbc','guardian','nyt','wsj','ap ','apnews','international']): return 'International'
        return 'National/Other'

    crime_tags={'crime-journalist','crime-reporter','crime-court-beat','crime-beat','court-reporter',
        'legal-reporter','investigative','police','mumbai-police','crime-branch','eow','acb','cyber-crime',
        'ats-maharashtra','criminal-lawyer','senior-advocate','human-rights-lawyer','judge','hc-judge',
        'sessions-judge','sessions-court','taluka-court','court','district-police','public-prosecutor',
        'collector','district-magistrate','mla','mp','politician','bar-association','legal-activist','civic-activist'}

    print("\n"+"="*60)
    print("FULL DATABASE SUMMARY")
    print("="*60)
    print(f"Total unique contacts (final) : {len(out)}")
    print(f"Verified send-ready (live)    : {len(live)}")
    print(f"Suppressed (blacklist)        : {len(supp_set)}")
    print(f"Invalid (quarantined)         : {len(invalid)}")
    print(f"Live with phone/WhatsApp      : {sum(1 for r in live if r['mobile'])}")
    crime_live=sum(1 for r in live if set(r['tags'].split('|'))&crime_tags)
    print(f"Live crime-network tagged     : {crime_live}")

    def dist(rowset,key,n=12,fn=None):
        c=Counter()
        for r in rowset:
            v=fn(r) if fn else (r.get(key,'') or 'unknown')
            c[v]+=1
        return c.most_common(n)

    print("\nLIVE by category:")
    for k,v in dist(live,'category',12): print(f"  {k:<30} {v}")
    print("\nLIVE by geography:")
    for k,v in dist(live,None,5,geo): print(f"  {k:<30} {v}")
    print("\nLIVE by case:")
    for k,v in dist(live,'case',10): print(f"  {(k or 'general'):<30} {v}")

    tagc=Counter()
    for r in live:
        for t in r['tags'].split('|'):
            if t: tagc[t]+=1
    print("\nLIVE top 20 tags:")
    for k,v in tagc.most_common(20): print(f"  {k:<28} {v}")
    with TAGSUM.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['tag','count'])
        for k,v in tagc.most_common(): w.writerow([k,v])

    print("\nSUPPRESSION by reason:")
    for k,v in Counter((r.get('reason','?') or '?').split(':')[0] for r in supp.values()).most_common(10):
        print(f"  {k:<28} {v}")
    print("\nSUPPRESSION by source:")
    for k,v in Counter(r.get('source','?') or '?' for r in supp.values()).most_common(10):
        print(f"  {k:<28} {v}")

if __name__=='__main__':
    main()
