#!/usr/bin/env python3
"""
STANDALONE AUTONOMOUS BOT - No complex imports
Self-contained circuit breaker trader
"""

import os
import logging
import time
from datetime import datetime
from dotenv import load_dotenv
from kiteconnect import KiteConnect

# Load environment
load_dotenv()
API_KEY = os.getenv('KITE_API_KEY')
ACCESS_TOKEN = os.getenv('KITE_ACCESS_TOKEN')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# NSE 200 stocks
STOCKS = [
    "SBIN", "HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK",
    "TCS", "INFY", "WIPRO", "TECHM", "HCLTECH",
    "RELIANCE", "BPCL", "ONGC", "NTPC", "POWERGRID",
    "MARUTI", "TATAMOTORS", "BAJAJ-AUTO", "HEROMOTOCO", "EICHER",
    "TATASTEEL", "JSWSTEEL", "HINDALCO", "SHREECEM",
    "NESTLE IND", "BRITANNIA", "HINDUNILVR", "ITC", "MARICO",
    "DRREDDY", "SUNPHARMA", "CIPLA", "LUPIN", "DIVISLAB",
    "ASIANPAINT", "DMART", "TITAN", "POLYCAB", "HAVELLS",
    "DLF", "OBEROIRLTY", "BHARTIARTL", "JIOTOWER",
    "HDFC", "BAJAJFINSV", "Sбиcard", "SBILIFE", "HDFCLIFE",
]

print("\n" + "="*70)
print("🤖 AUTONOMOUS CIRCUIT BREAKER TRADING BOT - STANDALONE")
print("="*70)
print(f"✓ Config loaded: API={API_KEY[:10]}..." if API_KEY else "❌ No API key!")
print()

# Get inputs
while True:
    try:
        circuit_pct = float(input("Enter circuit % (5-30): "))
        if 5 <= circuit_pct <= 30:
            break
    except:
        pass
    print("❌ Please enter 5-30")

print(f"✓ Circuit: {circuit_pct}%\n")

while True:
    try:
        qty = int(input("Enter quantity (1-100): "))
        if 1 <= qty <= 100:
            break
    except:
        pass
    print("❌ Please enter 1-100")

print(f"✓ Quantity: {qty}\n")

test_mode = input("Test mode? (Y/N, default Y): ").lower() != 'n'
print(f"✓ Mode: {'TEST' if test_mode else 'REAL'}\n")

# Connect
print("Connecting to Kite...")
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

try:
    quote = kite.quote(["HDFCBANK:NSE"])
    print("✓ Connected!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit()

# Run bot
print("\n" + "="*70)
print("🤖 BOT RUNNING - Scanning NSE 200...")
print(f"📊 Circuit Threshold: {circuit_pct}%")
print(f"⚡ Quantity per Stock: {qty}")
print(f"🔒 Mode: {'TEST (Simulated)' if test_mode else 'REAL TRADING'}")
print("⏸️  Press Ctrl+C to STOP")
print("="*70 + "\n")

check_count = 0
try:
    while True:
        check_count += 1
        if check_count % 6 == 0:  # Every 30 seconds  
            timestamp = datetime.now().strftime('%H:%M:%S')
            logger.info(f"[{timestamp}] Scanning {len(STOCKS)} stocks...")
        
        # Get quotes
        try:
            formatted = [f"{s.strip()}:NSE" for s in STOCKS if s.strip()]
            data = kite.quote(formatted)
            
            if 'data' not in data:
                logger.warning("No data in response")
                time.sleep(5)
                continue
            
            # Check for circuits
            for idx, stock in enumerate(STOCKS):
                stock_clean = stock.strip()
                sym = f"{stock_clean}:NSE"
                
                if sym not in data['data']:
                    continue
                
                quote = data['data'][sym]
                ltp = quote.get('last_price', 0)
                prev_close = quote.get('ohlc', {}).get('close', ltp)
                
                if prev_close > 0:
                    change = ((ltp - prev_close) / prev_close) * 100
                    
                    if abs(change) >= circuit_pct:
                        signal = "UPPER" if change >= circuit_pct else "LOWER"
                        action = "SELL" if change >= circuit_pct else "BUY"
                        logger.info(f"🔔 {stock_clean}: {signal} CIRCUIT ({change:+.2f}%) → {action} {qty}")
                        
                        if not test_mode:
                            try:
                                kite.place_order(
                                    tradingsymbol=sym,
                                    exchange="NSE",
                                    quantity=qty,
                                    side=action,
                                    order_type="MARKET",
                                    product="MIS"
                                )
                                logger.info(f"✓ Order placed: {action} {qty} {stock_clean}")
                            except Exception as e:
                                logger.error(f"Order failed: {e}")
        
        except Exception as e:
            logger.error(f"Scan error: {e}")
        
        time.sleep(5)

except KeyboardInterrupt:
    print("\n\n✓ Bot stopped")

