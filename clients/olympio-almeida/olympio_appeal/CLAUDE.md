# Olympio Almeida appeal — project context (for Claude Code)

This folder was migrated from a Cowork session. The goal that couldn't be finished there: **actually send the appeal email**, because Cowork's sandbox had no network route to the mail server. Claude Code runs on the user's own machine, so it can reach both Proton Bridge (localhost) and ZeptoMail (internet) — finish the job here.

## The matter
Senior-citizen residents of **La Masseria, Survey No. 197/A, Siolim, Goa** vs. the **"Sunday Racquet and Social Club"** — outdoor padel courts at House No. 47/3, Gaunsawaddo, Sodiem, Siolim, ~30–40 ft from the homes. Issues: noise pollution (68–75 dB(A) vs. 55 dB(A) residential limit), commercial use in a residential zone, **encroachment on Olympio Almeida's land**, and a documented 2008 Panchayat licence-revocation for unauthorised construction on the same plot (Sy. No. 197/7), originally on Olympio Almeida's complaint. Complaint filed with GSPCB on 9 March 2026; no response. Appeals are sent in Olympio Almeida's name from `olympio.almeida@pressdetective.com`.

## What's in this folder
- `1_Updated_Master_Complaint.docx` — strengthened GSPCB complaint
- `2_Formal_Appeal_Escalation.docx` — appeal to GSPCB Chairman + North Goa Collector
- `3_GSPCB_Followup_Reminder.docx` — reminder letter
- `4_Public_Open_Letter.docx` — open letter for press/supporters
- `5_Simple_Appeal_from_Olympio_Almeida.docx` / `.pdf` — the plain appeal that gets emailed
- `Evidence_Packet_FULL.pdf` — 26-page compiled evidence bundle (attach to sends)
- `Distribution_Recipients.csv` / `BCC_institutional_list.txt` — 156 institutional emails (govt, police, press, panchayat, NGOs)
- `Supporters_Outreach.csv` / `BCC_supporters_list.txt` — 13 named activists/NGOs (verified public emails)
- `send_via_zeptomail.py` — mass send via ZeptoMail SMTP (recommended; works from anywhere with internet)
- `send_appeal.py` — mass send via local Proton Bridge (127.0.0.1:1025)
- `send_outreach.py` — personalised one-to-one send to the 13 named supporters (Proton Bridge)
- `EMAIL_ready_to_send.md` — the subject + body, for manual sending

## How to send (pick one)

### Option 1 — ZeptoMail (internet SMTP)
```
export ZEPTO_TOKEN="<your ZeptoMail Send Mail token>"   # PowerShell: $env:ZEPTO_TOKEN="..."
python3 send_via_zeptomail.py --dry-run
python3 send_via_zeptomail.py
```
Login `emailapikey` @ `smtp.zeptomail.in:587`, From `olympio.almeida@pressdetective.com`. ZeptoMail is transactional — if it throttles the 156-way blast, lower `BATCH_SIZE` or split with `--start/--limit`.

### Option 2 — Proton Bridge (local)
With Proton Mail Bridge running:
```
python3 send_appeal.py --dry-run      # mass appeal, BCC batches of 40
python3 send_appeal.py                # prompts for Bridge password
python3 send_outreach.py              # personalised notes to the 13 named supporters
```
Bridge SMTP: `127.0.0.1:1025`, user `olympio.almeida@pressdetective.com`, STARTTLS.

## Before sending
- Fill the date and a mobile number in `5_Simple_Appeal_from_Olympio_Almeida.docx`/PDF.
- Send the press/activist list via `send_outreach.py` (personalised), NOT in the mass BCC.
- Free Proton caps ~100 recipients/day; ZeptoMail may flag bulk cold mail. Batch accordingly.
- Rotate any token/password that was shared in chat once sending is done.

## Note on credentials
No secrets are stored in these files. The ZeptoMail token is read from `ZEPTO_TOKEN`; the Proton password is prompted at runtime.
