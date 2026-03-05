#!/usr/bin/env python3
"""
KITE ACCESS TOKEN GENERATOR
Step-by-step guide to get your access token
"""

import webbrowser
from kiteconnect import KiteConnect
import os

# Your API key (from .env)
API_KEY = "zudyrwgcegy6o0nw"
APP_SECRET = "p9ru97bcm6jc9r3ycz4ok4unizyysv1z"  # From .env

print("\n" + "="*70)
print("🔐 KITE ACCESS TOKEN GENERATOR")
print("="*70)

print("""
This script will help you get a fresh ACCESS TOKEN.

STEPS:
1. Click the login URL below
2. Login with your Zerodha account
3. You'll see a redirect - COPY the 'request_token' from URL
4. Paste it here
5. We'll generate your access token!

Let's start:
""")

# Step 1: Generate login URL
kite = KiteConnect(api_key=API_KEY)
login_url = kite.login_url()

print(f"📱 LOGIN URL:\n{login_url}\n")

# Open browser automatically
try:
    webbrowser.open(login_url)
    print("✓ Browser opened automatically!")
except:
    print("Note: Couldn't auto-open browser. Copy the URL above and open manually.")

print("\n" + "-"*70)
print("STEP 1: Login and Get Request Token")
print("-"*70)

print("""
After you login and get redirected:
The URL will look like: https://127.0.0.1:8080/?request_token=XXXXX

COPY the request_token value (the XXXXX part after =)
""")

request_token = input("Paste your request_token here: ").strip()

if not request_token:
    print("❌ No token provided")
    exit()

print(f"✓ Got request token: {request_token[:20]}...")

print("\n" + "-"*70)
print("STEP 2: Generating Access Token...")
print("-"*70)

try:
    # Request access token using request token
    data = kite.request_access_token(
        code=request_token,
        secret=APP_SECRET
    )
    
    access_token = data['access_token']
    
    print(f"\n✓ SUCCESS! Access Token Generated:")
    print(f"\n{access_token}\n")
    
    print("="*70)
    print("📝 COPY THIS AND PASTE IN .env FILE:")
    print("="*70)
    print(f"\nKITE_ACCESS_TOKEN={access_token}\n")
    
    print("="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("""
1. Open: d:\\visual studio\\Module and packages\\kite\\.env
2. Find line: KITE_ACCESS_TOKEN=
3. Paste your token:
   KITE_ACCESS_TOKEN=""" + access_token + """
4. Save the file
5. Run the bot:
   python bot_demo.py

Done! 🎉
""")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("  1. Make sure you copied the request_token correctly")
    print("  2. Request tokens expire quickly, get a fresh one")
    print("  3. Check your API key is correct in .env")
    print("  4. Make sure APP_SECRET matches your Zerodha app")

