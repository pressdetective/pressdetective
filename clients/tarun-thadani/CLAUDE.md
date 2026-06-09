# CLAUDE.md — Project Context

## Scope guardrail (IMPORTANT)
This project relates **only to Press Detective (pressdetective)**. Never confuse it with any other
site or matter. Any email/automation work uses **pressdetective** (incl. ZeptoMail = pressdetective).

## Matter
False criminal case against **Mr. Tarun Thadani**, founder of **Dharte (dharte.com)**.

- **FIR / C.R.:** No. 0654 of 2022, **Dadar Police Station**, Mumbai (registered ~12–13 Aug 2022)
- **Offences alleged:** Assault + ₹1 crore extortion — IPC s.384/385/387, 506 r/w 34 *(confirm exact sections from charge-sheet)*
- **Complainant / First Informant:** Mr. Abhishek Badriprasad Saraf (Esplanade House, Mumbai 400001)
- **Co-accused:** Mr. Ali Asgar Merchant
- **Incident:** Private event, restaurant in Worli, 02–03 June 2022
- **Tarun's role:** Sent invitations only; **NOT present** at the venue
- **Status:** Charge-sheeted; **discharge REFUSED by the Sessions Court on 31 March 2024**
- **Counsel / Advocate on Record:** Adv. Sujata Shirasi (+91 93216 13691)

## Core defence (one line)
Tarun was not present and did nothing beyond sending invitations; the ₹1 crore extortion allegation
was absent from the original 04.06.2022 complaint and was added ~2 months later; the FIR was
registered without examining any accused or verifying any evidence.

## Deliverables produced (in /deliverables)
1. `01_Criminal_Revision_Application_*` — s.397/401 CrPC, Bombay HC, vs the 31.03.2024 discharge refusal.
2. `02_Section_482_Quashing_Petition_*` — quash FIR/charge-sheet qua Tarun (alternative/parallel remedy).
3. `03_Plan_of_Action_*` — multi-track strategy (criminal, defamation, ACB, counter-action).
4. `04_ChangeOrg_Campaign_*` — ready-to-publish public petition package.

## Open items / placeholders to fill before filing
- Confirm which Sessions Court passed the 31.03.2024 order; the Sessions Case No.; accused number.
- Confirm exact IPC sections in the charge-sheet.
- Tarun's address/age; certified-copy dates; limitation/condonation.
- Revision vs s.482 are alternative remedies — counsel to choose lead remedy and disclose parallel filing.

## How to regenerate documents
Scripts in `/scripts` use the `docx` npm package (Node). From that folder:
```
npm install docx
node gen_revision.js   # -> 01_...docx
node gen_quash.js      # -> 02_...docx
node gen_poa.js        # -> 03_...docx  (Plan of Action)
node gen_changeorg.js  # -> 04_...docx
```
Edit the text inside each script, then re-run to rebuild the .docx.

## Legal/usage note
All documents are AI-generated **drafts for review by the Advocate on Record** — not legal advice,
not for filing as-is. The matter is sub judice; keep public statements measured and frame third-party
conduct as "alleged".
