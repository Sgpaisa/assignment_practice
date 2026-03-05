"""Direct API test - bypass our wrapper"""

from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('KITE_API_KEY')
access_token = os.getenv('KITE_ACCESS_TOKEN')

print(f"API Key: {api_key[:10]}...")
print(f"Access Token: {access_token[:10]}...")

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

print("\nTesting KiteConnect.quote() directly...")
print("Trying: kite.quote(['HDFCBANK:NSE'])")

try:
    result = kite.quote(['HDFCBANK:NSE'])
    print(f"✓ Success! Got: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"   Type: {type(e)}")
