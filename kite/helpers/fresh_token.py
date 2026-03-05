#!/usr/bin/env python3
"""
ZERODHA ACCESS TOKEN GENERATOR - OAuth Flow
This uses the official Zerodha OAuth flow to get a fresh token
"""

import os
import sys
import json
import webbrowser
from urllib.parse import parse_qs, urlparse
from datetime import datetime
from dotenv import load_dotenv

try:
    from kiteconnect import KiteConnect
    import requests
except ImportError:
    print("[ERROR] Missing required packages")
    print("Run: pip install kiteconnect requests")
    sys.exit(1)

load_dotenv()

API_KEY = os.getenv('KITE_API_KEY')
API_SECRET = os.getenv('KITE_APP_SECRET')

print("\n" + "="*70)
print("ZERODHA - FRESH ACCESS TOKEN GENERATOR")
print("="*70 + "\n")

if not API_KEY or not API_SECRET:
    print("[ERROR] API_KEY or APP_SECRET not in .env")
    sys.exit(1)

print(f"[OK] Using API Key: {API_KEY}\n")

kite = KiteConnect(api_key=API_KEY)
login_url = kite.login_url()

print("[STEP 1] Opening Zerodha login in browser...")
print(f"URL: {login_url}\n")

try:
    webbrowser.open(login_url)
except:
    print("Browser didn't open. Copy-paste this URL manually:")
    print(login_url)

print("[STEP 2] Log in with your Zerodha credentials\n")

print("[STEP 3] After login, copy the redirect URL from your browser\n")

redirect_url = input("Paste the redirect URL here: ").strip()

if not redirect_url:
    print("[ERROR] No URL provided")
    sys.exit(1)

try:
    parsed = parse_qs(urlparse(redirect_url).query)
    request_token = parsed.get('request_token', [None])[0]
    
    if not request_token:
        print("[ERROR] Could not extract request_token")
        print("Make sure you pasted the full redirect URL")
        sys.exit(1)
    
    print(f"\n[OK] Request token: {request_token}\n")
    
    print("[STEP 4] Generating access token...\n")
    
    session = kite.generate_session(request_token, api_secret=API_SECRET)
    
    access_token = session['access_token']
    user_id = session.get('user_id', 'N/A')
    
    print(f"[SUCCESS] Access token generated!")
    print(f"  User ID: {user_id}")
    print(f"  Token: {access_token}\n")
    
    # Save to .env
    env_path = ".env"
    with open(env_path, 'r') as f:
        content = f.read()
    
    old_line = f"KITE_ACCESS_TOKEN=.*"
    new_line = f"KITE_ACCESS_TOKEN={access_token}"
    
    import re
    content = re.sub(old_line, new_line, content)
    
    with open(env_path, 'w') as f:
        f.write(content)
    
    print(f"[OK] Updated .env file\n")
    
    # Test connection
    print("[STEP 5] Testing connection...")
    kite.set_access_token(access_token)
    
    try:
        quote = kite.quote("NSE:HDFCBANK")["NSE:HDFCBANK"]
        ltp = quote['last_price']
        print(f"[OK] Connected! HDFCBANK LTP: Rs. {ltp:.2f}\n")
        
        print("="*70)
        print("YOU'RE READY TO TRADE!")
        print("="*70)
        print("\nRun: python bot.py\n")
        
    except Exception as e:
        print(f"[WARNING] Could not fetch data: {e}")
        print("But token should be valid. Try running bot.py anyway\n")
    
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nTroubleshooting:")
    print("  1. Make sure you pasted the FULL redirect URL")
    print("  2. Check your API_KEY and API_SECRET in .env")
    print("  3. Try again\n")
    sys.exit(1)
