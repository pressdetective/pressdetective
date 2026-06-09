#!/usr/bin/env python3
"""
lib/proton_smtp.py — shared Proton Mail SMTP helper for PressDetective send scripts.

Supports:
  - Remote Proton SMTP: smtp.protonmail.ch:587 (STARTTLS, token as password)
  - Local Proton Bridge: 127.0.0.1:1025 (STARTTLS, Bridge password prompted)

Accounts:
  olympio   olympio.almeida@pressdetective.com
  santosh   santosh@pressdetective.com
  info      info@pressdetective.com
  sujata    sujata.shirasi@pressdetective.com

Usage:
    from lib.proton_smtp import proton_send, load_account

    account = load_account("sujata")          # reads .creds/proton_accounts.json
    proton_send(msg, account)                 # remote SMTP (token auth)
    proton_send(msg, account, bridge=True)    # local Bridge (prompts password)
"""
import smtplib, ssl, json, os, getpass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE = os.path.join(ROOT, ".creds", "proton_accounts.json")

REMOTE_HOST = "smtp.protonmail.ch"
REMOTE_PORT = 587
BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 1025


def load_account(name: str) -> dict:
    """Load account config from .creds/proton_accounts.json by short name."""
    with open(CREDS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    accounts = data["accounts"]
    if name not in accounts:
        raise ValueError(f"Unknown account '{name}'. Known: {list(accounts)}")
    acc = accounts[name]
    if not acc.get("token") or acc["token"] == "FILL_IN":
        raise ValueError(f"Token for '{name}' not set in {CREDS_FILE}")
    return acc


def proton_send(msg, account: dict, bridge: bool = False):
    """
    Send an EmailMessage via Proton SMTP.
    bridge=False  → remote smtp.protonmail.ch:587 using account['token']
    bridge=True   → local Bridge 127.0.0.1:1025, prompts for Bridge password
    """
    address = account["address"]
    if bridge:
        host, port = BRIDGE_HOST, BRIDGE_PORT
        password = getpass.getpass(f"Proton Bridge password for {address}: ")
    else:
        host, port = REMOTE_HOST, REMOTE_PORT
        password = account["token"]

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port) as s:
        s.ehlo()
        s.starttls(context=context)
        s.login(address, password)
        s.send_message(msg)
