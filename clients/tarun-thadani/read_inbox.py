#!/usr/bin/env python3
"""Read info@pressdetective.com inbox and show today's summary + any replies."""
import imaplib, ssl, email, textwrap
from email.header import decode_header
from email.utils import parsedate_to_datetime

ADDR  = 'info@pressdetective.com'
TOKEN = 'FzspzmcI-DE4s1JIp7HU3A'

def dec(h):
    parts = decode_header(h or '')
    return ''.join(
        p.decode(enc or 'utf-8', errors='replace') if isinstance(p, bytes) else p
        for p, enc in parts
    ).strip()

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get('Content-Disposition', ''))
            if ct == 'text/plain' and 'attachment' not in cd:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    return payload.decode(charset, errors='replace')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or 'utf-8'
            return payload.decode(charset, errors='replace')
    return ''

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
m = imaplib.IMAP4('127.0.0.1', 1143)
m.starttls(ssl_context=ctx)
m.login(ADDR, TOKEN)
m.select('INBOX')

_, data = m.search(None, 'ALL')
all_ids = data[0].split()

print(f'Total inbox: {len(all_ids)} messages\n')
print('-'*70)
print('TODAY\'S MESSAGES (9 Jun 2026) — NON-BROADCAST')
print('-'*70)

today_replies = []
broadcast_count = 0

for uid in reversed(all_ids):
    _, msg_data = m.fetch(uid, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    frm  = dec(msg.get('From', ''))
    subj = dec(msg.get('Subject', ''))
    date = msg.get('Date', '')

    # Filter for today
    if '09 Jun 2026' not in date and '9 Jun 2026' not in date:
        continue

    # Skip broadcast CC copies (from sujata to info@)
    if 'sujata.shirasi@pressdetective' in frm.lower():
        broadcast_count += 1
        continue

    today_replies.append((uid.decode(), date, frm, subj, msg))

print(f'Broadcast CC copies received today: {broadcast_count}')
print(f'Other messages today: {len(today_replies)}\n')

for uid, date, frm, subj, msg in today_replies:
    print(f'--- Message #{uid} -------------------------------------------')
    print(f'From : {frm}')
    print(f'Date : {date}')
    print(f'Subj : {subj}')
    body = get_body(msg).strip()
    if body:
        print('Body:')
        for line in body.splitlines()[:40]:
            print(f'  {line}')
        if len(body.splitlines()) > 40:
            print(f'  ... [{len(body.splitlines())-40} more lines]')
    print()

# Also show the very latest message in full regardless
print('-'*70)
print('LATEST MESSAGE (most recent, full read)')
print('-'*70)
_, msg_data = m.fetch(all_ids[-1], '(RFC822)')
msg = email.message_from_bytes(msg_data[0][1])
print(f'From : {dec(msg.get("From",""))}')
print(f'Date : {msg.get("Date","")}')
print(f'Subj : {dec(msg.get("Subject",""))}')
body = get_body(msg).strip()
if body:
    print('Body:')
    for line in body.splitlines()[:60]:
        print(f'  {line}')

m.logout()
