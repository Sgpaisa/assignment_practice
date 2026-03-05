#!/usr/bin/env python3
"""
SIMPLE TOKEN GENERATOR - No interactive input needed
Just follow the instructions and run once more
"""

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('KITE_API_KEY')
API_SECRET = os.getenv('KITE_APP_SECRET')

print("\n" + "="*70)
print("GET YOUR ZERODHA ACCESS TOKEN - SIMPLE METHOD")
print("="*70)

print("\n[METHOD 1] Copy from Browser (EASIEST)")
print("-" * 70)
print("1. Open: https://kite.zerodha.com/")
print("2. Log in with your Zerodha credentials")
print("3. Press F12 (Developer Tools)")
print("4. Go to 'Application' tab")
print("5. Click 'Cookies' → 'kite.zerodha.com'")
print("6. Find 'authorization' cookie")
print("7. Copy the value (long string)")
print("8. Run this command in PowerShell:\n")

print('   cd "D:\\visual studio\\Module and packages\\kite"')
print('   $token = Read-Host "Paste your access token"')
print('   (Get-Content ".env") -replace "KITE_ACCESS_TOKEN=.*", "KITE_ACCESS_TOKEN=$token" | Set-Content ".env"')
print('\n9. Then test with: python helpers/test_order.py\n')

print("-" * 70)
print("[METHOD 2] Through Zerodha API (More Complex)")
print("-" * 70)
print("1. Get token from: https://kite.trade/apps/mine")
print("2. Use postman or similar tool")
print("3. Then paste token in .env file\n")

print("="*70)
print("QUICK COPY-PASTE SOLUTION")
print("="*70)

# Token provided by user will go here
token = input("\nPaste your access token here: ").strip()

if token and len(token) > 30:
    env_file = ".env"
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'KITE_ACCESS_TOKEN=your_access_token_here',
        f'KITE_ACCESS_TOKEN={token}'
    )
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("\n[OK] Access token saved to .env!")
    print(f"     Token: {token[:20]}...{token[-10:]}\n")
    print("Next step: python helpers/test_order.py\n")
else:
    print("\n[ERROR] Invalid token or token too short")
    print("        Make sure you copied the FULL token\n")
