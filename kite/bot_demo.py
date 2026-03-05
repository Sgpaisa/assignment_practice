#!/usr/bin/env python3
"""
AUTONOMOUS BOT - DEMO VERSION
Pre-configured for testing - no input needed
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

# ============================================================================
# CONFIGURATION - ADJUST THESE!
# ============================================================================
CIRCUIT_PERCENT = 15          # Trigger when stock moves 15%
QUANTITY_PER_TRADE = 5        # Buy/Sell 5 shares per stock
TEST_MODE = True              # True = simulate, False = real trading

# NSE 200 stocks (simplified list)
STOCKS = [
    "SBIN", "HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK", "IDFCBANK", "INDUSIND",
    "TCS", "INFY", "WIPRO", "TECHM", "LTIM", "HCLTECH", "MPHASIS",
    "RELIANCE", "BPCL", "HINDPETRO", "NTPC", "POWERGRID", "ONGC", "COALINDIA",
    "MARUTI", "TATAMOTORS", "BAJAJ-AUTO", "HEROMOTOCO", "EICHER",
    "TATASTEEL", "JSWSTEEL", "HINDALCO", "SHREECEM", "AMBUJACEMENT", "ULTRACEMCO",
    "NESTLEIND", "BRITANNIA", "HINDUNILVR", "ITC", "MARICO", "COLPAL", "GODREJCP",
    "DRREDDY", "SUNPHARMA", "CIPLA", "LUPIN", "DIVISLAB", "AUROPHARMA", "BIOCON",
    "ASIANPAINT", "DMART", "TITAN", "POLYCAB", "HAVELLS", "CROMPTON",
    "DLF", "OBEROIRLTY", "BHARTIARTL", "JIOTOWER", "ZEEL",
    "HDFC", "BAJAJFINSV", "SBICARD", "SBILIFE", "HDFCLIFE", "ICICIPRULI",
]

print("\n" + "="*70)
print("🤖 AUTONOMOUS CIRCUIT BREAKER TRADING BOT - DEMO")
print("="*70)
print(f"""
Configuration:
  • Circuit Threshold: {CIRCUIT_PERCENT}%
  • Quantity per Stock: {QUANTITY_PER_TRADE}
  • Test Mode: {'YES (Simulated)' if TEST_MODE else 'NO (Real Trading!)'}
  • Stocks to Monitor: {len(STOCKS)} NSE stocks
  
Bot will:
  1. Continuously scan all {len(STOCKS)} stocks
  2. Detect when ANY hits {CIRCUIT_PERCENT}% circuit
  3. Auto-{'simulate' if TEST_MODE else 'execute'} BUY/SELL orders
  
Status: Connecting...
""")

# Connect
try:
    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(ACCESS_TOKEN)
    
    # Test connection
    test_quote = kite.quote(["HDFCBANK:NSE"])
    print("✓ Connected to Zerodha Kite API!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nMake sure:")
    print("  1. .env has correct KITE_API_KEY and KITE_ACCESS_TOKEN")
    print("  2. Internet is working")
    print("  3. Market is open (9:15 AM - 3:30 PM IST)")
    exit()

# Run bot
print("\n" + "="*70)
print("🤖 BOT RUNNING - AUTONOMOUS MODE")
print("="*70)
print(f"\n📊 Scanning {len(STOCKS)} stocks every 5 seconds")
print(f"🎯 Trigger level: {CIRCUIT_PERCENT}%")
print(f"⚡ Auto-trade: {QUANTITY_PER_TRADE} shares per stock")
print(f"🔒 Mode: {'🧪 TEST (Simulated)' if TEST_MODE else '💰 REAL TRADING'}")
print("\n⏸️  Press Ctrl+C to STOP\n")

check_count = 0
circuit_found_count = 0

try:
    while True:
        check_count += 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        try:
            # Format all stocks for API
            formatted = [f"{s.strip()}:NSE" for s in STOCKS if s.strip()]
            
            # Get quotes
            data = kite.quote(formatted)
            
            if 'data' not in data:
                logger.warning(f"[{timestamp}] No data in response")
                time.sleep(5)
                continue
            
            # Log status every 6 checks (30 seconds)
            if check_count % 6 == 0:
                print(f"[{timestamp}] ✓ Scanned {len(STOCKS)} stocks | Found circuits: {circuit_found_count}")
            
            # Check each stock
            signals = {
                'buy': [],    # Lower circuit
                'sell': []    # Upper circuit
            }
            
            for stock in STOCKS:
                stock_clean = stock.strip()
                sym = f"{stock_clean}:NSE"
                
                if sym not in data['data']:
                    continue
                
                quote_data = data['data'][sym]
                ltp = quote_data.get('last_price', 0)
                prev_close = quote_data.get('ohlc', {}).get('close', ltp)
                
                if prev_close > 0:
                    change_pct = ((ltp - prev_close) / prev_close) * 100
                    
                    # Upper circuit - SELL
                    if change_pct >= CIRCUIT_PERCENT:
                        signals['sell'].append({
                            'stock': stock_clean,
                            'change': change_pct,
                            'ltp': ltp
                        })
                    
                    # Lower circuit - BUY
                    elif change_pct <= -CIRCUIT_PERCENT:
                        signals['buy'].append({
                            'stock': stock_clean,
                            'change': change_pct,
                            'ltp': ltp
                        })
            
            # Execute signals
            for signal in signals['buy']:
                circuit_found_count += 1
                stock = signal['stock']
                change = signal['change']
                ltp = signal['ltp']
                
                print(f"\n🔔 SIGNAL: {stock} HIT LOWER CIRCUIT!")
                print(f"   Change: {change:+.2f}% | LTP: ₹{ltp:.2f}")
                print(f"   Action: {'[TEST] Simulated BUY' if TEST_MODE else '✓ AUTO-BUY'} {QUANTITY_PER_TRADE} shares")
                
                if not TEST_MODE:
                    try:
                        order_id = kite.place_order(
                            tradingsymbol=f"{stock}:NSE",
                            exchange="NSE",
                            quantity=QUANTITY_PER_TRADE,
                            side="BUY",
                            order_type="MARKET",
                            product="MIS"
                        )
                        print(f"   ✓ Order placed! ID: {order_id}\n")
                    except Exception as e:
                        print(f"   ❌ Order failed: {e}\n")
            
            for signal in signals['sell']:
                circuit_found_count += 1
                stock = signal['stock']
                change = signal['change']
                ltp = signal['ltp']
                
                print(f"\n🔔 SIGNAL: {stock} HIT UPPER CIRCUIT!")
                print(f"   Change: {change:+.2f}% | LTP: ₹{ltp:.2f}")
                print(f"   Action: {'[TEST] Simulated SELL' if TEST_MODE else '✓ AUTO-SELL'} {QUANTITY_PER_TRADE} shares")
                
                if not TEST_MODE:
                    try:
                        order_id = kite.place_order(
                            tradingsymbol=f"{stock}:NSE",
                            exchange="NSE",
                            quantity=QUANTITY_PER_TRADE,
                            side="SELL",
                            order_type="MARKET",
                            product="MIS"
                        )
                        print(f"   ✓ Order placed! ID: {order_id}\n")
                    except Exception as e:
                        print(f"   ❌ Order failed: {e}\n")
        
        except Exception as e:
            logger.error(f"[{timestamp}] Scan error: {e}")
        
        time.sleep(5)

except KeyboardInterrupt:
    print(f"\n\n" + "="*70)
    print("✓ BOT STOPPED")
    print("="*70)
    print(f"Summary:")
    print(f"  • Total scans: {check_count}")
    print(f"  • Circuit signals found: {circuit_found_count}")
    print(f"  • Mode: {'TEST (Simulated)' if TEST_MODE else 'REAL TRADING'}")
    print(f"  • All activity logged to trading_bot.log")
    print("="*70 + "\n")

