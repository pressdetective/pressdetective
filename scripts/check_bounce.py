#!/usr/bin/env python3
"""check_bounce.py -- Check Proton Bridge IMAP for bounce DSNs from police test"""
import imaplib
import email
import json
from pathlib import Path
from email.parser import BytesParser

CREDS = json.loads(Path(r'C:\dev\pressdetective\.creds\proton_accounts.json').read_text(encoding='utf-8-sig'))
BRIDGE_HOST = CREDS['imap_bridge']['host']
BRIDGE_PORT = CREDS['imap_bridge']['port']
BRIDGE_PASS = CREDS['accounts']['santosh']['bridge_password']
FROM = CREDS['accounts']['santosh']['address']

print("=" * 70)
print("Checking Bridge IMAP for bounces...")
print("=" * 70)

try:
    imap = imaplib.IMAP4_SSL(BRIDGE_HOST, BRIDGE_PORT)
except:
    imap = imaplib.IMAP4(BRIDGE_HOST, BRIDGE_PORT)
    imap.starttls()

imap.login(FROM, BRIDGE_PASS)
print(f"[OK] Connected to Bridge at {BRIDGE_HOST}:{BRIDGE_PORT}")

# Check Inbox for recent bounce messages
imap.select('INBOX')
status, msg_ids = imap.search(None, 'ALL')
msg_ids = msg_ids[0].split()

print(f"\nInbox has {len(msg_ids)} messages. Checking last 20 for bounces...")

bounce_found = False
for msg_id in msg_ids[-20:]:
    status, msg_data = imap.fetch(msg_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])

    subj = msg.get('Subject', '')
    sender = msg.get('From', '')

    # Look for DSN or bounce-related subjects
    if 'dadar' in subj.lower() or 'fir 0654' in subj.lower():
        print(f"\n[FOUND TEST EMAIL]")
        print(f"  From: {sender}")
        print(f"  Subject: {subj}")
        print(f"  Content-Type: {msg.get_content_type()}")

        # Show body preview
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    print(f"  Body: {body[:200]}")
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            print(f"  Body: {body[:200]}")

    if 'mailer' in sender.lower() or 'postmaster' in sender.lower() or 'mail delivery' in subj.lower():
        bounce_found = True
        print(f"\n[BOUNCE DSN FOUND]")
        print(f"  From: {sender}")
        print(f"  Subject: {subj}")

        # Extract body for bounce code
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    # Look for 5.7.7, 5.1.1, etc
                    if '5.7.7' in body:
                        print(f"  CODE: 5.7.7 (POLICY REJECTION) - Gateway still blocking")
                    elif '5.1.1' in body:
                        print(f"  CODE: 5.1.1 (USER NOT FOUND) - Address doesn't exist")
                    elif '5.' in body:
                        codes = [w for w in body.split() if w.startswith('5.')]
                        if codes:
                            print(f"  CODE: {codes[0]}")
                    print(f"  Details: {body[:300]}")
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            if '5.7.7' in body:
                print(f"  CODE: 5.7.7 (POLICY REJECTION)")
            elif '5.1.1' in body:
                print(f"  CODE: 5.1.1 (USER NOT FOUND)")
            print(f"  Body: {body[:300]}")

if not bounce_found:
    print("\n[NO BOUNCES FOUND in recent messages]")
    print("This is GOOD -- it means the email was either:")
    print("  1. DELIVERED successfully (SPF/policy block is fixed!)")
    print("  2. Still in flight (check again in 1-2 minutes)")

imap.close()
imap.logout()

print("\n" + "=" * 70)
