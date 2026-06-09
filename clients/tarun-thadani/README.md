# Tarun Thadani — Defence Project (Press Detective)

Migration package for **Claude Code**. Unzip, then open the folder in Claude Code:
```
cd tarun-thadani-defence
claude
```
Claude Code will read `CLAUDE.md` automatically for project context and guardrails.

## Folder structure
```
tarun-thadani-defence/
├── CLAUDE.md              # Project context, case facts, guardrails (read first)
├── README.md             # This file
├── case_summary.md       # Facts, timeline, parties, key documents
├── deliverables/         # Final .docx drafts (Revision, Quashing, Plan of Action, Change.org)
├── scripts/              # Node generators to rebuild/edit each .docx
└── source_materials/     # Original case files (complaints, notices, photos, judgments)
```

## Requirements to rebuild docs
- Node.js + `npm install docx` (inside `scripts/`)
- Run `node gen_*.js` to regenerate the corresponding deliverable.

## Status
- 4 deliverables drafted. Placeholders ([brackets]) still need confirming from certified copies.
- All drafts require sign-off by Adv. Sujata Shirasi before any filing/publishing.
