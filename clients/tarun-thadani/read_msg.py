#!/usr/bin/env python3
import imaplib, ssl, email
from email.header import decode_header

ADDR  = 'info@pressdetective.com'
TOKEN = 'FzspzmcI-DE4s1JIp7HU3A'

def dec(h):
    parts = decode_header(h or '')
    return ''.join(
        p.decode(enc or 'utf-8', errors='replace') if isinstance(p, bytes) else p
        for p, enc in parts
    ).strip()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
m = imaplib.IMAP4('127.0.0.1', 1143)
m.starttls(ssl_context=ctx)
m.login(ADDR, TOKEN)
m.select('INBOX')

# Read message 103 (Tony Mony - Document from TT)
for uid in [b'103', b'22']:
    _, msg_data = m.fetch(uid, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    print(f'=== MSG {uid.decode()} ===')
    print(f'From: {dec(msg.get("From",""))}')
    print(f'Date: {msg.get("Date","")}')
    print(f'Subj: {dec(msg.get("Subject",""))}')
    print(f'Content-Type: {msg.get_content_type()}')
    print()
    if msg.is_multipart():
        for i, part in enumerate(msg.walk()):
            ct = part.get_content_type()
            cd = str(part.get('Content-Disposition', ''))
            fn = part.get_filename()
            print(f'  Part {i}: {ct} | disp={cd[:40]} | filename={fn}')
            if ct == 'text/plain' and 'attachment' not in cd:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    text = payload.decode(charset, errors='replace').strip()
                    print(f'  Body text ({len(text)} chars): {text[:500]}')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or 'utf-8'
            text = payload.decode(charset, errors='replace').strip()
            print(f'Body ({len(text)} chars): {text[:500]}')
    print()

m.logout()
