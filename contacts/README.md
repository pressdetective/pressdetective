# PressDetective — Master Contact List
**Updated: 2026-06-09 — Deep cleaned & DNS verified**

## Primary file: `contacts_clean.csv`
DNS-verified, fully tagged, named, sorted. **Use this for all outreach.**

Columns: `email | name | designation | category | tags | case | source`

---

## Total: 3,170 verified email addresses
*(3,238 raw → 68 removed: 3 bad syntax, 65 dead domains)*

### Removed (see `contacts_removed.csv`)
- `dyaigo&m.dgoffice@mahapolice.gov.in` — `&` character invalid in email local-part
- `bhc.gov.in/familycourtlatur@gmail.com` — URL fragment corrupted into email field
- `6258322/625562mtiladmin@de16.vsnl.net.in` — fax number prepended to address
- 7x `@dnaindia.net` — DNA India moved to dnaindia.com, old .net domain dead
- 2x `@gmail.in` — typo for gmail.com
- 53 other dead/expired domains (see clean_report.txt)

---

## By tag (for quick batch selection)

| Tag | Count | Use for |
|---|---|---|
| `top-priority` | 69 | CP/DGP/ADG/Collector level — always include |
| `police-hq` | 1,131 | IGs, DIGs, AIGs, DGP office staff |
| `police-zone` | 88 | All DCP zones + all ACPs |
| `police-station` | 97 | All 88 Mumbai PS + Goa stations |
| `police-special` | 21 | EOW, ACB, Cyber, Crime Branch |
| `anti-corruption` | 9 | ACB Maharashtra |
| `economic-fraud` | 5 | EOW — corporate/financial fraud |
| `cyber-crime` | 8 | Cyber PS all regions + IG |
| `anti-extortion` | 2 | Crime Branch / AEC command |
| `crime-branch` | 3 | Crime Branch Mumbai chain |
| `court-high` | 11 | Bombay High Court |
| `court-lower` | 47 | CMM/Magistrate courts (17 Mumbai courts) |
| `court-sessions` | 3 | City Civil & Sessions Court |
| `court-family` | 1 | Family Court Mumbai BKC |
| `press` | 1,439 | Journalists + media |
| `govt-state` | 861 | Maharashtra state govt officials |
| `govt-admin` | 27 | District admin (Collectors) |
| `land-records` | 27 | Land records, encroachment officers |
| `ngo-civic` | 14 | NGOs and civil society |
| `goa` | 167 | Goa-specific (Olympio Almeida case) |
| `dgp-desk` | 70 | DGP admin desks (Desk 1-44) |
| `individual` | 2 | Named supporters |
| `general` | 7 | Unclassified |

---

## Quick-send reference

| Outreach type | Filter tag | Key addresses |
|---|---|---|
| Cyber crime | `cyber-crime` | `cyberpst-mum@mahapolice.gov.in`, `ig.cbr-mah@gov.in` |
| Economic fraud | `economic-fraud` | `adg.eowms@mahapolice.gov.in` |
| Corruption/bribery | `anti-corruption` | `acbwebmail@mahapolice.gov.in`, `addlcpacbmumbai@mahapolice.gov.in` |
| Extortion | `anti-extortion` | `cp.mumbai.jtcp.crime@mahapolice.gov.in`, `dcpdet1.mum@mahapolice.gov.in` |
| Land grabbing | `land-records` | `collector.mumbaicity@maharashtra.gov.in`, `collector.mumbaisuburb@maharashtra.gov.in` |
| Press outreach | `press` | 1,439 journalists (India-wide + Goa) |
| High Court | `court-high` | `hcbom.mah@nic.in`, `regos-bhc@nic.in` |
| Magistrate court | `court-lower` | 47 CMM/MM courts |
| Top decision-makers | `top-priority` | 69 addresses — CP, DGP, ADGs, Collectors |

---

## Files
| File | Description |
|---|---|
| `contacts_clean.csv` | **USE THIS** — 3,170 DNS-verified, tagged, sorted |
| `contacts_removed.csv` | 68 removed entries with rejection reasons |
| `clean_report.txt` | Full DNS verification report |
| `tag_summary.csv` | Tag legend with counts |
| `contacts_tagged.csv` | Pre-clean version (3,238, for reference) |
| `contacts_master.csv` | Original extraction (3,188, no tags) |
| `build_tagged.py` | Builds contacts_tagged.csv from all sources |
| `deep_clean.py` | DNS verification + cleaning script |
