#!/usr/bin/env python3
import imaplib, ssl, email
from email.header import decode_header
from pathlib import Path

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

_, msg_data = m.fetch(b'103', '(RFC822)')
msg = email.message_from_bytes(msg_data[0][1])

out_dir = Path('C:/dev/pressdetective/clients/tarun-thadani')

for part in msg.walk():
    fn = part.get_filename()
    if fn:
        fn = dec(fn)
        payload = part.get_payload(decode=True)
        if payload:
            out_path = out_dir / fn
            out_path.write_bytes(payload)
            print(f'Saved: {out_path} ({len(payload)} bytes)')
            # Also print text content if it's a .txt
            if fn.endswith('.txt'):
                text = payload.decode('utf-8', errors='replace')
                print()
                print('--- FILE CONTENT ---')
                print(text[:3000])
    else:
        ct = part.get_content_type()
        if ct == 'text/html':
            payload = part.get_payload(decode=True)
            if payload:
                text = payload.decode('utf-8', errors='replace').strip()
                if text and len(text) > 20:
                    print(f'HTML body: {text[:300]}')

m.logout()
