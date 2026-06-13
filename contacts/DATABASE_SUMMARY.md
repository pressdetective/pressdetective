# PressDetective Contacts — Database Summary
**Generated: 2026-06-13** · branch `contacts` · all emails live-verified (MX/A + syntax + bounce-history)

## Headline

| Metric | Count |
|---|---|
| **Total unique contacts** (`contacts_final.csv`) | **4,787** |
| **Verified send-ready** (`contacts_live.csv`) | **3,036** |
| Suppressed (bounces / opt-outs / dead domains) | 1,834 |
| With real phone/WhatsApp number | 96 |
| Distinct tags in use | 169 |

**Integrity:** 0 duplicates · 0 suppressed addresses in live · 0 bad syntax. Ban-safe.

---

## By geography (live)

| Region | Count |
|---|---|
| National / pan-India | 1,645 |
| **Mumbai** | **951** |
| Maharashtra (other districts) | 220 |
| Goa | 215 |
| International | 5 |

Maharashtra district coverage: all 36 districts + 11 police commissionerates (SP/CP offices, sessions courts, collectors).

## By theme (live — contacts can carry multiple)

| Theme | Count |
|---|---|
| Press / Journalists | 1,553 |
| Govt / Administration | 1,070 |
| Police / Enforcement | 942 |
| Courts / Judiciary | 431 |
| Influencers / Social | 310 |
| Lawyers / Legal | 98 |
| Politicians | 87 |
| NGO / Activist | 45 |

## By category (live)

| Category | Count |
|---|---|
| Press | 1,415 |
| Police/Government | 741 |
| Government | 226 |
| Press/Media | 165 |
| Court/Judiciary | 151 |
| Press/Legal Media | 116 |
| Legal | 64 |
| Politician/MLA | 57 |
| Court | 21 |
| Politician/MP | 19 |

## By case (live)

`tarun-thadani` 2,011 · `general` 771 · `olympio-almeida` 204 · `mumbai-contacts` 50
*(case tags overlap — a contact can serve multiple campaigns)*

## Top 30 tags (live)

| Tag | # | Tag | # | Tag | # |
|---|--|---|--|---|--|
| govt-state | 1070 | times-of-india | 109 | police | 60 |
| press | 968 | legal-press | 105 | police-zone | 60 |
| police-hq | 899 | politician | 84 | national-media | 57 |
| mumbai-press | 625 | legal-reporter | 81 | mla | 57 |
| crime-court-beat | 428 | social-active | 80 | crime-beat | 54 |
| top-priority | 374 | investigative | 79 | digital-creator | 54 |
| crime-reporter | 334 | influencer | 76 | bribery-reporter | 54 |
| maharashtra | 220 | goa | 75 | hindustan-times | 50 |
| x-active | 184 | judiciary | 144 | court | 144 |
| taluka-court | 143 | goa-press | 138 | crime-journalist | 123 |

---

## Files

| File | Purpose |
|---|---|
| `contacts_live.csv` | **Send from this** — 3,036 verified, suppression applied |
| `contacts_final.csv` | Master (4,787, incl. suppressed) |
| `suppression_list.csv` | Blacklist (1,834) |
| `influencers_emailable.csv` | 325 verified-email creators (sortable subset of live) |
| `influencers_mumbai_reference.csv` | 29 crime/legal/political/activist creators for DM/team outreach (handles + followers, no emails — they aren't public) |
| `contacts_removed_full.csv` | Removed-with-reasons log |

## How to pull a segment (examples)

- **Mumbai crime press:** filter live where tags contain `mumbai-press` AND (`crime-reporter` OR `crime-journalist` OR `crime-court-beat`)
- **Maharashtra police (all districts):** tags contain `police` (943) — with WhatsApp numbers on the SP/CP rows
- **Courts:** tags contain `court` / `sessions-court` / `taluka-court` (431)
- **Lawyers:** tags contain `criminal-lawyer` / `senior-advocate` / `human-rights-lawyer`
- **Digital creators:** tags contain `influencer` / `youtuber` / `x-active` / `digital-creator` (310)
- **Top-priority decision-makers:** tag `top-priority` (374)

Run `python contacts/clean_and_audit.py` before any major campaign to re-verify.
