# PressDetective — Master Contact List
**Updated: 2026-06-09**

## Primary file: `contacts_tagged.csv`
Fully tagged, named, and sorted. Use this for all outreach.

Columns: `email | name | designation | category | tags | case | source`

---

## Total: 3,238 unique verified email addresses

### By tag (for quick batch selection)

| Tag | Count | Use for |
|---|---|---|
| `top-priority` | 69 | Commissioners, DGP, ADG, Collectors — always include |
| `police-hq` | 1,144 | Police HQ officers (IG, DIG, AIG, desks) |
| `police-zone` | 88 | Zonal DCPs and all ACPs |
| `police-station` | 97 | All 88 Mumbai PS + Goa police stations |
| `police-special` | 21 | Specialized units (EOW, ACB, Cyber, Crime Branch) |
| `anti-corruption` | 9 | ACB Maharashtra — bribery / disproportionate assets |
| `economic-fraud` | 5 | EOW — corporate scams, money laundering |
| `cyber-crime` | 8 | Cyber Crime police — all 5 regional PS + IG |
| `anti-extortion` | 2 | Crime Branch / Anti-Extortion Cell command |
| `crime-branch` | 3 | Crime Branch Mumbai chain |
| `court-high` | 11 | Bombay High Court (registrar + benches) |
| `court-lower` | 47 | CMM / Magistrate courts (all 17 Mumbai courts) |
| `court-sessions` | 3 | City Civil & Sessions Court |
| `court-family` | 1 | Family Court Mumbai BKC |
| `press` | 1,489 | Journalists + media outlets |
| `govt-state` | 876 | State government — ministers, Maharashtra officials |
| `govt-admin` | 27 | District admin (Mumbai City + Suburban collectors) |
| `land-records` | 27 | Land records, encroachment, city survey officers |
| `ngo-civic` | 14 | NGOs and civil society |
| `goa` | 167 | Goa-specific (Olympio Almeida case) |
| `individual` | 2 | Named individual supporters |
| `dgp-desk` | 71 | DGP Office admin desks (Desk 1-44 + AIG/Dy-AIG) |
| `unverified` | 4 | Non-official domains — verify before bulk send |

### By case
| Case | Count |
|---|---|
| tarun-thadani | 3,031 |
| olympio-almeida | 157 |
| mumbai-contacts | 50 (net new) |

---

## Quick-send reference

### Cyber crime complaint
Filter: `cyber-crime`
Key: `cyberpst-mum@mahapolice.gov.in`, `ig.cbr-mah@gov.in`

### Economic fraud / corporate scam
Filter: `economic-fraud`
Key: `adg.eowms@mahapolice.gov.in`

### Corruption / bribery
Filter: `anti-corruption`
Key: `acbwebmail@mahapolice.gov.in`, `addlcpacbmumbai@mahapolice.gov.in`

### Extortion / Crime Branch
Filter: `anti-extortion`
Key: `cp.mumbai.jtcp.crime@mahapolice.gov.in`, `dcpdet1.mum@mahapolice.gov.in`

### Land grabbing / encroachment (Mumbai)
Filter: `land-records`
Key: `collector.mumbaicity@maharashtra.gov.in`, `collector.mumbaisuburb@maharashtra.gov.in`

### Press outreach
Filter: `press`
1,489 journalists + media outlets (India-wide + Goa-specific)

### High court filing / registry
Filter: `court-high`
Key: `hcbom.mah@nic.in`, `regos-bhc@nic.in`

### Magistrate court
Filter: `court-lower`
17 Mumbai courts — Esplanade, Dadar, Bandra, Andheri, Borivali, Kurla, etc.

---

## Source files
- `contacts_master.csv` — base 3,188 (pre-tagging, original extraction)
- `contacts_tagged.csv` — **use this** (3,238, fully tagged + sorted)
- `tag_summary.csv` — tag legend with counts
- `build_tagged.py` — script that built this; re-run to rebuild
