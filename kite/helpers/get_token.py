#!/usr/bin/env python3
"""
GET ZERODHA KITE ACCESS TOKEN
Run this script to authenticate and get your access token
"""

import os
import sys
import webbrowser
from urllib.parse import parse_qs, urlparse
from dotenv import load_dotenv

try:
    from kiteconnect import KiteConnect
except ImportError:
    print("[ERROR] kiteconnect not installed")
    print("Run: pip install kiteconnect")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Get credentials from .env
API_KEY = os.getenv('KITE_API_KEY')
API_SECRET = os.getenv('KITE_APP_SECRET')

print("\n" + "="*70)
print("ZERODHA KITE - GET ACCESS TOKEN")
print("="*70 + "\n")

if not API_KEY or not API_SECRET:
    print("[ERROR] API_KEY or APP_SECRET not configured in .env file")
    sys.exit(1)

print(f"[OK] API_KEY found: {API_KEY[:10]}...{API_KEY[-5:]}")
print(f"[OK] APP_SECRET found: {API_SECRET[:10]}...{API_SECRET[-5:]}\n")

# Initialize KiteConnect
kite = KiteConnect(api_key=API_KEY)

# Generate login URL
login_url = kite.login_url()

print("[STEP 1] Opening Zerodha login page in your browser...")
print(f"           {login_url}\n")

try:
    webbrowser.open(login_url)
    print("[OK] Browser opened. Please log in with your Zerodha credentials.\n")
except:
    print("[WARNING] Could not open browser automatically")
    print("[ACTION] Please manually visit this URL:")
    print(f"         {login_url}\n")

# Get authorization code
print("[STEP 2] After login, you'll be redirected to a URL")
print("         Copy the full redirect URL and paste it here:\n")

redirect_url = input("Paste the redirect URL: ").strip()

if not redirect_url:
    print("[ERROR] No URL provided")
    sys.exit(1)

try:
    # Parse the redirect URL to get the authorization code
    parsed = parse_qs(urlparse(redirect_url).query)
    request_token = parsed.get('request_token', [None])[0]
    
    if not request_token:
        print("[ERROR] Could not extract request_token from URL")
        print("        Make sure you copied the full redirect URL")
        sys.exit(1)
    
    print(f"\n[OK] Request token found: {request_token}\n")
    
    # Generate access token
    print("[STEP 3] Generating access token...")
    session = kite.generate_session(request_token, api_secret=API_SECRET)
    
    access_token = session['access_token']
    user_id = session.get('user_id', 'N/A')
    
    print(f"[OK] Access token generated successfully!\n")
    print(f"     User ID: {user_id}")
    print(f"     Access Token: {access_token}\n")
    
    # Update .env file
    print("[STEP 4] Updating .env file...")
    
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Replace the access token
    content = content.replace(
        'KITE_ACCESS_TOKEN=your_access_token_here',
        f'KITE_ACCESS_TOKEN={access_token}'
    )
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"[OK] .env file updated\n")
    
    print("="*70)
    print("SUCCESS! You can now run the trading bot:")
    print("="*70)
    print("\ncd 'd:\\visual studio\\Module and packages\\kite'")
    print("python bot.py\n")
    print("OR test with:")
    print("python helpers/test_order.py\n")
    
except Exception as e:
    print(f"[ERROR] Failed to generate access token: {e}")
    print("\nTroubleshooting:")
    print("  1. Make sure you copied the FULL redirect URL")
    print("  2. Check that your API_KEY and API_SECRET are correct")
    print("  3. Try again\n")
    sys.exit(1)
