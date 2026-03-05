#!/usr/bin/env python3
"""
SIMPLEST TOKEN METHOD - Just paste your token!
"""

import os

print("\n" + "="*70)
print("MANUAL TOKEN INPUT - SIMPLEST METHOD")
print("="*70 + "\n")

print("STEP 1: Go to https://kite.zerodha.com/")
print("STEP 2: Log in with your credentials")
print("STEP 3: Open browser Developer Tools (F12)")
print("STEP 4: Go to Application → Cookies → kite.zerodha.com")
print("STEP 5: Find 'authorization' cookie")
print("STEP 6: Copy the VALUE (long string)\n")

token = input("Paste your access token: ").strip()

if token and len(token) > 30:
    env_file = ".env"
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    import re
    content = re.sub(
        r'KITE_ACCESS_TOKEN=.*',
        f'KITE_ACCESS_TOKEN={token}',
        content
    )
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"\n[OK] Token saved! Token: {token[:20]}...{token[-10:]}\n")
    
    # Test it
    print("Testing connection...")
    os.system("python helpers/test_order.py")
    
else:
    print("\n[ERROR] Token too short or invalid")
    print("        Token should be 40+ characters\n")
