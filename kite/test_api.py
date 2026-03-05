"""Test the Kite API connection directly"""

import sys
sys.path.insert(0, '.')

from authenticators.token_manager import TokenManager
from core.kite_client import KiteClient

print("Testing Kite API Connection...")
print("="*70)

# Load credentials
api_key, access_token = TokenManager.load_credentials_from_env()

if not api_key or not access_token:
    print("❌ Missing credentials in .env")
    sys.exit(1)

print(f"✓ Credentials loaded")
print(f"  API Key: {api_key[:10]}...")
print(f"  Access Token: {access_token[:10]}...")

# Try to connect
print("\nConnecting to Zerodha Kite API...")

try:
    kite = KiteClient(api_key, access_token)
    print("✓ KiteClient created")
    
    # Test single quote
    print("\nTesting single stock quote...")
    quote = kite.get_quote("HDFCBANK")
    if quote:
        print(f"✓ Got HDFCBANK quote: LTP = {quote.get('last_price')}")
    else:
        print("❌ Failed to get HDFCBANK quote")
    
    # Test multiple quotes
    print("\nTesting multiple stock quotes...")
    quotes = kite.get_quote_multiple(["INFY", "TCS", "RELIANCE"])
    if quotes:
        print(f"✓ Got {len(quotes)} quotes")
        for sym, data in quotes.items():
            if data:
                print(f"  - {sym}: LTP = {data.get('last_price')}")
    else:
        print("❌ Failed to get multiple quotes")
    
    print("\n✓ API Connection Test PASSED!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
