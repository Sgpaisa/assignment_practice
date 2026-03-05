#!/usr/bin/env python3
"""
DIAGNOSTIC SCRIPT - Test API Connection & Place Test Order
Use this to verify your Zerodha credentials and test order placement
"""

import os
import sys
from dotenv import load_dotenv
from kiteconnect import KiteConnect

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    API_KEY, ACCESS_TOKEN, STOCK_TO_TRADE,
    QUANTITY_PER_TRADE

)

print("\n" + "="*70)
print("ZERODHA KITE - DIAGNOSTIC TEST")
print("="*70 + "\n")

# Load credentials
load_dotenv()
api_key = API_KEY or os.getenv('KITE_API_KEY')
access_token = ACCESS_TOKEN or os.getenv('KITE_ACCESS_TOKEN')

print("[STEP 1] Checking credentials...")
if api_key.startswith("your_") or access_token.startswith("your_"):
    print("[ERROR] Credentials are still PLACEHOLDER values!")
    print("        Edit .env file or config.py with real credentials")
    sys.exit(1)

if len(api_key) < 15 or len(access_token) < 15:
    print("[ERROR] Credentials appear to be INVALID or INCOMPLETE!")
    print(f"        API Key length: {len(api_key)} chars (should be 30+)")
    print(f"        Access Token length: {len(access_token)} chars (should be 50+)")
    print("\n[SOLUTION]")
    print("1. Go to: https://kite.trade/apps/mine")
    print("2. Log in with your Zerodha account")
    print("3. Copy the API Key")
    print("4. Run: python helpers/get_token.py")
    print("5. Add both to .env file")
    sys.exit(1)

print(f"API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'NOT SET'}")
print(f"Access Token: {access_token[:20]}...{access_token[-10:] if access_token else 'NOT SET'}")

if not api_key or not access_token:
    print("[ERROR] Credentials not configured!")
    print("        Edit .env file with KITE_API_KEY and KITE_ACCESS_TOKEN")
    sys.exit(1)

print("[OK] Credentials found\n")

# Connect to Kite
print("[STEP 2] Connecting to Zerodha Kite API...")
try:
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    print("[OK] Connected successfully\n")
except Exception as e:
    print(f"[ERROR] Failed to connect: {e}")
    sys.exit(1)

# Fetch stock data
print(f"[STEP 3] Fetching {STOCK_TO_TRADE} stock data...")
try:
    # Get quote using NSE format
    quote = kite.quote(f"NSE:{STOCK_TO_TRADE}")[f"NSE:{STOCK_TO_TRADE}"]
    
    ltp = quote['last_price']
    prev_close = quote['ohlc']['close']
    bid = quote['bid']
    ask = quote['ask']
    volume = quote['volume']
    
    change = ((ltp - prev_close) / prev_close) * 100
    
    print(f"[OK] Data retrieved:")
    print(f"     Stock: {STOCK_TO_TRADE}")
    print(f"     LTP: Rs. {ltp:.2f}")
    print(f"     Previous Close: Rs. {prev_close:.2f}")
    print(f"     Change: {change:.2f}%")
    print(f"     Bid: Rs. {bid:.2f}")
    print(f"     Ask: Rs. {ask:.2f}")
    print(f"     Volume: {volume}\n")
    
except Exception as e:
    print(f"[ERROR] Failed to fetch data: {e}")
    sys.exit(1)

# Test order placement
print("[STEP 4] Testing order placement...")
print(f"         (This will place a TEST order, NOT a real trade)\n")

confirm = input("Do you want to place a test BUY order? (yes/no): ").lower().strip()

if confirm == 'yes':
    try:
        print(f"\nPlacing BUY order for {QUANTITY_PER_TRADE} share(s) at Rs. {int(ltp)}...")
        
        order_id = kite.place_order(
            variety='regular',
            exchange='NSE',
            tradingsymbol=f"NSE:{STOCK_TO_TRADE}",
            transaction_type='BUY',
            quantity=QUANTITY_PER_TRADE,
            price=int(ltp),
            order_type='limit',
            product='MIS'  # Intraday
        )
        
        print(f"[OK] Order placed successfully!")
        print(f"     Order ID: {order_id}\n")
        print("[NEXT] Check your Zerodha app/website for the order\n")
        
        # Try to cancel it immediately
        try:
            print("Attempting to cancel the order...")
            kite.cancel_order(
                variety='regular',
                order_id=order_id
            )
            print(f"[OK] Order cancelled (test successful)\n")
        except Exception as e:
            print(f"[WARNING] Could not auto-cancel: {e}")
            print("          You may manually cancel it from Zerodha website\n")
        
    except Exception as e:
        print(f"[ERROR] Failed to place order: {e}\n")
        print("Possible reasons:")
        print("  - Market is closed")
        print("  - Invalid stock symbol")
        print("  - Insufficient funds/margin")
        print("  - API credentials expired\n")

print("="*70)
print("DIAGNOSTIC TEST COMPLETE")
print("="*70 + "\n")

print("TROUBLESHOOTING TIPS:")
print("  1. If connection fails: Check API_KEY and ACCESS_TOKEN in config.py")
print("  2. If data fetch fails: Check STOCK_TO_TRADE symbol (NSE format)")
print("  3. If order fails: Market may be closed or you lack funds/margin")
print("  4. Check trading_bot.log for detailed error messages")
print("  5. Verify market hours: 9:15 AM - 3:30 PM IST (Weekdays only)\n")
