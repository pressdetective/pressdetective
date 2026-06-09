#!/usr/bin/env python3
import imaplib, ssl, email
from email.header import decode_header

import json, pathlib
_creds = json.loads((pathlib.Path(__file__).parents[2] / '.creds/proton_accounts.json').read_text())
ADDR  = _creds['accounts']['info']['address']
TOKEN = _creds['accounts']['info']['bridge_password']

def dec(h):
    parts = decode_header(h or '')
    return ''.join(
        p.decode(enc or 'utf-8') if isinstance(p, bytes) else p
        for p, enc in parts
    )

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

m = imaplib.IMAP4('127.0.0.1', 1143)
m.starttls(ssl_context=ctx)
typ, greeting = m.login(ADDR, TOKEN)
print(f'Login: {typ} {greeting}')

# List folders
_, folders = m.list()
print('Folders:')
for f in folders:
    print(' ', f.decode())

# Inbox
m.select('INBOX')
_, data = m.search(None, 'ALL')
ids = data[0].split()
print(f'\nInbox: {len(ids)} messages total')

recent = ids[-20:] if len(ids) >= 20 else ids
print(f'Last {len(recent)} messages:\n')
for uid in reversed(recent):
    _, msg_data = m.fetch(uid, '(RFC822.HEADER)')
    msg = email.message_from_bytes(msg_data[0][1])
    uid_str = uid.decode()
    date    = msg.get('Date', '')[:25]
    frm     = dec(msg.get('From', ''))[:50]
    subj    = dec(msg.get('Subject', ''))[:110]
    print(f'[{uid_str:>5}] {date}')
    print(f'  From: {frm}')
    print(f'  Subj: {subj}')
    print()

m.logout()
