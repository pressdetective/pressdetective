#!/usr/bin/env python3
"""
patch_and_send.py
  1. Fills date + mobile/email into the appeal PDF
  2. Sends to all 156 Goa contacts via ZeptoMail (batches of 40)
  3. Emails a full report to REPORT_TO when done

Usage:
    $env:ZEPTO_TOKEN = "..."          # PowerShell
    python patch_and_send.py          # live run
    python patch_and_send.py --dry    # preview only
"""
import smtplib, ssl, os, sys, time, argparse
from io import BytesIO
from email.message import EmailMessage

import pypdf
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import white

# ── Config ────────────────────────────────────────────────────
HERE        = os.path.dirname(os.path.abspath(__file__))
SMTP_HOST   = "smtp.zeptomail.in"
SMTP_PORT   = 587
SMTP_USER   = "emailapikey"
FROM_ADDR   = "olympio.almeida@pressdetective.com"
REPORT_TO   = "gavora@gmail.com"
BATCH_SIZE  = 40
PAUSE_SECS  = 20

MOBILE      = "+91 98221 68112"
EMAIL_SHOWN = "olympio.almeida@pressdetective.com"
DATE_STR    = "9 June 2026"

PAGE_W, PAGE_H = 595.303937, 841.889764

SUBJECT = (
    'Appeal to look into encroachment, illegal construction and noise '
    'nuisance - "Sunday Racquet and Social Club", Sodiem, Siolim'
)

BODY = """\
Respected Sir / Madam,

I, Olympio Almeida, a resident of Sodiem, Siolim, Bardez - Goa, am writing to \
appeal to all the authorities concerned to kindly look into a serious and continuing \
matter at Survey No. 197 / House No. 47/3, Gaunsawaddo, Sodiem, Siolim.

A commercial sporting business - outdoor padel courts operating as the \
"Sunday Racquet and Social Club" - is being run in the middle of a residential area, \
immediately next to family homes. It has also ENCROACHED UPON MY LAND. It is causing \
daily distress to residents, several of whom are senior citizens, and it appears to be \
operating in violation of the law. In particular:

1. Encroachment on my property - the operators have encroached upon and occupied a \
portion of my land without any right, title or consent;
2. Loud and continuous noise - the sharp impact of paddle-ball play, amplified music \
and rowdy, late-night activity - from early morning until around midnight, well above \
the noise limits permitted for a residential area;
3. Commercial use of land in a residential zone, with no proper buffer from \
neighbouring homes; and
4. A documented history of unauthorised construction at this very plot - the Village \
Panchayat Siolim-Sodiem had earlier revoked the construction licence here for building \
"not as per the approved plan."

Despite complaints already made, the disturbance continues and no effective action \
appears to have been taken on the ground.

I therefore appeal to the authorities to kindly:

1. Carry out an inspection and a survey/demarcation of the premises, including during \
evening and night hours when the disturbance is at its worst;
2. Examine the legality of the construction and the commercial operation on this \
residential plot, and have the encroachment on my land surveyed, removed and my \
property restored to me;
3. Take appropriate action under the noise-pollution, public-nuisance, planning and \
panchayat laws; and
4. Direct that the disturbance be stopped, so that residents - especially the elderly \
and unwell - can live in peace.

The attached appeal and evidence compilation set out the facts, the measured noise \
levels and the relevant records. I shall be happy to provide any further information \
required, and to assist any inspection.

I earnestly request your kind and prompt intervention.

Yours faithfully,
Olympio Almeida
Sodiem, Siolim, Bardez - Goa
olympio.almeida@pressdetective.com  |  Mobile: +91 98221 68112
"""


# ── PDF patching ──────────────────────────────────────────────
def _overlay(page_num):
    buf = BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    if page_num == 0:
        # Cover "__________ 2026" (x=105.4 y=687.6) and write date
        c.setFillColor(white)
        c.rect(104.0, 684.5, 140.0, 13.5, fill=1, stroke=0)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 11)
        c.drawString(105.4, 687.6, DATE_STR)
    elif page_num == 1:
        # Cover mobile blank (x=117.4) and email blank (x=303.5) at y=431.5
        c.setFillColor(white)
        c.rect(116.0, 429.0, 152.0, 13.5, fill=1, stroke=0)  # mobile blank
        c.rect(302.0, 429.0, 210.0, 13.5, fill=1, stroke=0)  # email blank
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 11)
        c.drawString(117.4, 431.5, MOBILE)
        c.drawString(303.5, 431.5, EMAIL_SHOWN)
    c.showPage()
    c.save()
    buf.seek(0)
    return pypdf.PdfReader(buf)


def patch_pdf(src, dst):
    reader = pypdf.PdfReader(src)
    writer = pypdf.PdfWriter()
    for i, page in enumerate(reader.pages):
        page.merge_page(_overlay(i).pages[0])
        writer.add_page(page)
    with open(dst, "wb") as f:
        writer.write(f)
    print(f"  PDF saved: {os.path.basename(dst)}")


# ── Recipients ────────────────────────────────────────────────
def load_recipients():
    path = os.path.join(HERE, "BCC_institutional_list.txt")
    seen, out = set(), []
    for e in open(path, encoding="utf-8").read().replace("\n", ",").split(","):
        e = e.strip()
        if e and "@" in e and e.lower() not in seen:
            seen.add(e.lower())
            out.append(e)
    return out


# ── SMTP helpers ──────────────────────────────────────────────
def smtp_connect(token):
    ctx = ssl.create_default_context()
    s = smtplib.SMTP_SSL(SMTP_HOST, 465, context=ctx, timeout=60)
    s.ehlo()
    s.login(SMTP_USER, token)
    return s


def appeal_msg(bcc, appeal_pdf, evidence_pdf):
    m = EmailMessage()
    m["From"]    = FROM_ADDR
    m["To"]      = FROM_ADDR
    m["Cc"]      = "info@pressdetective.com"
    m["Bcc"]     = ", ".join(bcc)
    m["Subject"] = SUBJECT
    m.set_content(BODY)
    for p in [appeal_pdf, evidence_pdf]:
        with open(p, "rb") as f:
            m.add_attachment(f.read(), maintype="application", subtype="pdf",
                             filename=os.path.basename(p))
    return m


def send_report(token, sent, errors, total, elapsed_s):
    lines = [
        "Olympio Almeida Appeal — Delivery Report",
        f"Date: {DATE_STR}",
        f"From: {FROM_ADDR}",
        f"Recipients: {total}  |  Sent: {sent}  |  Failed: {total - sent}",
        f"Time elapsed: {elapsed_s:.0f}s",
        f"Batch size: {BATCH_SIZE}  |  Pause between batches: {PAUSE_SECS}s",
        "",
        f"Subject: {SUBJECT}",
        "",
        "Attachments:",
        "  - 5_Simple_Appeal_from_Olympio_Almeida_FILLED.pdf",
        "  - Evidence_Packet_FULL.pdf",
        "",
    ]
    if errors:
        lines += ["Errors:", *errors, ""]
    else:
        lines.append("No errors.")
    body = "\n".join(lines)

    m = EmailMessage()
    m["From"]    = FROM_ADDR
    m["To"]      = REPORT_TO
    m["Cc"]      = "info@pressdetective.com"
    m["Subject"] = f"[PressDetective] Olympio appeal sent — {sent}/{total} delivered"
    m.set_content(body)

    with smtp_connect(token) as s:
        s.send_message(m)
    print(f"  Report sent -> {REPORT_TO}")


# ── Main ──────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry",   action="store_true", help="preview only, send nothing")
    ap.add_argument("--start", type=int, default=0, help="skip first N recipients (resume)")
    ap.add_argument("--limit", type=int, default=0, help="send at most N recipients")
    args = ap.parse_args()

    token = os.environ.get("ZEPTO_TOKEN", "")
    if not token and not args.dry:
        print("ERROR: set ZEPTO_TOKEN env var"); sys.exit(1)

    appeal_src = os.path.join(HERE, "5_Simple_Appeal_from_Olympio_Almeida.pdf")
    appeal_out = os.path.join(HERE, "5_Simple_Appeal_from_Olympio_Almeida_FILLED.pdf")
    evidence   = os.path.join(HERE, "Evidence_Packet_FULL.pdf")

    print("=== Step 1: Patch PDF ===")
    patch_pdf(appeal_src, appeal_out)

    print("\n=== Step 2: Recipients ===")
    all_recips = load_recipients()
    recips = all_recips[args.start:]
    if args.limit:
        recips = recips[:args.limit]
    if args.start or args.limit:
        print(f"  Resuming: skipping first {args.start}, sending {len(recips)} of {len(all_recips)}")
    batches = [recips[i:i+BATCH_SIZE] for i in range(0, len(recips), BATCH_SIZE)]
    print(f"  {len(recips)} recipients in {len(batches)} batches of {BATCH_SIZE}")
    for i, b in enumerate(batches, 1):
        print(f"  Batch {i}: {b[0]} ... {b[-1]}  ({len(b)} rcpts)")

    if args.dry:
        print("\nDRY RUN — nothing sent.")
        return

    print("\n=== Step 3: Send appeal ===")
    sent, errors, t0 = 0, [], time.time()

    for i, batch in enumerate(batches, 1):
        # Pre-build message before opening SMTP connection (avoid timeout while encoding PDFs)
        msg = appeal_msg(batch, appeal_out, evidence)
        ok = False
        for attempt in range(1, 4):
            try:
                with smtp_connect(token) as s:
                    s.send_message(msg)
                sent += len(batch)
                print(f"  [{i}/{len(batches)}] sent {sent}/{len(recips)}")
                ok = True
                break
            except Exception as e:
                print(f"  Attempt {attempt} failed: {e}")
                if attempt < 3:
                    time.sleep(10)
        if not ok:
            err = f"Batch {i}: all 3 attempts failed"
            errors.append(err)
            print(f"  ERROR: {err}")
        if i < len(batches):
            print(f"  Waiting {PAUSE_SECS}s ...")
            time.sleep(PAUSE_SECS)

    elapsed = time.time() - t0
    print(f"\nDone. {sent}/{len(recips)} sent in {elapsed:.0f}s. {len(errors)} error(s).")

    print("\n=== Step 4: Send report ===")
    send_report(token, sent, errors, len(recips), elapsed)


if __name__ == "__main__":
    main()
