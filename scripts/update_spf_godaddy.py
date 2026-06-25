#!/usr/bin/env python3
"""update_spf_godaddy.py -- Update pressdetective.com SPF record via GoDaddy API"""
import requests
import json
import sys
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

# GoDaddy API credentials
API_KEY = "hkTkhcctvrAs_3DNrnAQh5Cq4AtSbuzawBz"
API_SECRET = "DfdEZHLPvmah2Z612VfPtD"
DOMAIN = "pressdetective.com"

# GoDaddy API endpoint
BASE_URL = "https://api.godaddy.com/v1"
AUTH_HEADER = f"sso-key {API_KEY}:{API_SECRET}"

# New SPF record (Proton-only, strict fail)
NEW_SPF = "v=spf1 include:_spf.protonmail.ch -all"

print("=" * 70)
print("GoDaddy SPF Record Update — pressdetective.com")
print("=" * 70)

# Step 1: Get current TXT records
print("\n1. Fetching current TXT records...")
try:
    response = requests.get(
        f"{BASE_URL}/domains/{DOMAIN}/records/TXT",
        headers={"Authorization": AUTH_HEADER}
    )
    response.raise_for_status()
    records = response.json()
    print(f"   Found {len(records)} TXT record(s)")

    spf_record = None
    for rec in records:
        if rec['data'].startswith('v=spf1'):
            spf_record = rec
            print(f"   Current SPF: {rec['data']}")
            break

    if not spf_record:
        print("   WARNING: No existing SPF record found. Will create new one.")

except Exception as e:
    print(f"   ERROR fetching records: {e}")
    sys.exit(1)

# Step 2: Update/create SPF record
print("\n2. Updating SPF record...")
print(f"   New SPF: {NEW_SPF}")

try:
    update_data = [
        {
            "data": NEW_SPF,
            "name": "@",
            "ttl": 3600,
            "type": "TXT"
        }
    ]

    response = requests.put(
        f"{BASE_URL}/domains/{DOMAIN}/records/TXT/@",
        headers={"Authorization": AUTH_HEADER},
        json=update_data
    )
    response.raise_for_status()
    print("   [OK] SPF record updated successfully")

except Exception as e:
    print(f"   ERROR updating record: {e}")
    sys.exit(1)

# Step 3: Verify the change
print("\n3. Verifying change...")
try:
    response = requests.get(
        f"{BASE_URL}/domains/{DOMAIN}/records/TXT",
        headers={"Authorization": AUTH_HEADER}
    )
    response.raise_for_status()
    records = response.json()

    for rec in records:
        if rec['data'].startswith('v=spf1'):
            if rec['data'] == NEW_SPF:
                print(f"   [OK] Verified: {rec['data']}")
            else:
                print(f"   [!] Mismatch: {rec['data']}")
            break

except Exception as e:
    print(f"   ERROR verifying: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("[OK] SPF record update complete!")
print("=" * 70)
print("\nPropagation typically takes 5-15 minutes. Government gateways should")
print("now accept mail from pressdetective.com via Proton (protonmail.ch).")
print("\nNext: Send test email to police department to verify delivery.")
