#!/usr/bin/env python3
"""Try different username/password combos against Bridge IMAP."""
import socket, ssl, time, base64

HOST = '127.0.0.1'
PORT = 1143

def try_auth(username, password, label=''):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((HOST, PORT))
        banner = s.recv(1024).decode(errors='replace').strip()

        # STARTTLS
        s.send(b'A001 STARTTLS\r\n')
        resp = s.recv(1024).decode(errors='replace').strip()

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ts = ctx.wrap_socket(s, server_hostname=HOST)

        # AUTH PLAIN two-step: send command, wait for +, then send credentials
        plain = base64.b64encode(b'\x00' + username.encode() + b'\x00' + password.encode()).decode()
        ts.send(b'A002 AUTHENTICATE PLAIN\r\n')
        time.sleep(0.5)
        challenge = ts.recv(4096).decode(errors='replace').strip()
        if not challenge.startswith('+'):
            ts.close()
            print(f'  [{label}] no challenge: {challenge[:60]}')
            return False
        ts.send((plain + '\r\n').encode())
        time.sleep(0.5)
        resp = ts.recv(4096).decode(errors='replace').strip()
        ts.close()

        ok = 'A002 OK' in resp
        status = 'OK' if ok else resp[:80]
        print(f'  [{label}] {status}')
        return ok
    except Exception as e:
        print(f'  [{label}] ERROR: {e}')
        return False

# The password as read from Bridge UI (ambiguous chars)
# Position 8 (Fzspzmcl): l vs 1
# Position 14 (DE4s1J): 1 vs l vs I
# Position 15 (Jlp): l vs 1 vs I

user = 'wheredemtamales@protonmail.com'
base_pw = 'Fzspzmcl-DE4s1Jlp7HU3A'

variants = {
    'orig-lowercase-l': 'Fzspzmcl-DE4s1Jlp7HU3A',
    'pos14-one-pos15-I': 'Fzspzmcl-DE4s11Jp7HU3A',
    'pos15-one':         'Fzspzmcl-DE4s1J1p7HU3A',
    'pos15-I':           'Fzspzmcl-DE4s1JIp7HU3A',
    'pos8-one':          'Fzspzmc1-DE4s1Jlp7HU3A',
    'pos8-one+pos15-I':  'Fzspzmc1-DE4s1JIp7HU3A',
}

print(f'Testing {user}\n')
for label, pw in variants.items():
    try_auth(user, pw, label)
    time.sleep(2)
