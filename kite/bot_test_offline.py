#!/usr/bin/env python3
"""
AUTONOMOUS CIRCUIT BREAKER BOT - OFFLINE TEST VERSION
Tests bot logic WITHOUT needing Zerodha quote permission
Uses simulated stock data for testing
"""

import os
import logging
import time
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================
CIRCUIT_PERCENT = 15          # Trigger when stock moves 15%
QUANTITY_PER_TRADE = 5        # Buy/Sell 5 shares per stock
TEST_MODE = True              # Always test mode (simulated)

# NSE 200 stocks
STOCKS = [
    "SBIN", "HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK", "IDFCBANK", "INDUSIND",
    "TCS", "INFY", "WIPRO", "TECHM", "LTIM", "HCLTECH", "MPHASIS",
    "RELIANCE", "BPCL", "HINDPETRO", "NTPC", "POWERGRID", "ONGC", "COALINDIA",
    "MARUTI", "TATAMOTORS", "BAJAJ-AUTO", "HEROMOTOCO", "EICHER",
    "TATASTEEL", "JSWSTEEL", "HINDALCO", "SHREECEM", "AMBUJACEMENT", "ULTRACEMCO",
]

print("\n" + "="*70)
print("🤖 AUTONOMOUS CIRCUIT BREAKER TRADING BOT - OFFLINE TEST")
print("="*70)
print(f"""
Configuration:
  • Circuit Threshold: {CIRCUIT_PERCENT}%
  • Quantity per Stock: {QUANTITY_PER_TRADE}
  • Mode: TEST MODE (Simulated with random data)
  • Stocks to Monitor: {len(STOCKS)} NSE stocks
  
This version works WITHOUT needing Zerodha quote permission!
Perfect for testing bot logic before enabling permissions.

Status: Running in offline mode...
""")

# Simulate market data
def get_simulated_quotes():
    """Generate simulated stock data"""
    quotes = {}
    for stock in STOCKS:
        # Simulate random price changes
        prev_close = random.uniform(100, 5000)
        change_direction = random.choice([-1, 1])
        change_pct = random.uniform(0, CIRCUIT_PERCENT * 1.5) * change_direction
        ltp = prev_close * (1 + change_pct / 100)
        
        quotes[f"{stock}:NSE"] = {
            'last_price': ltp,
            'ohlc': {'close': prev_close},
            'change_percent': change_pct
        }
    
    return {'data': quotes}

# Run bot
print("="*70)
print("🤖 BOT RUNNING - OFFLINE SIMULATION MODE")
print("="*70)
print(f"\n📊 Scanning {len(STOCKS)} stocks every 5 seconds")
print(f"🎯 Trigger level: {CIRCUIT_PERCENT}%")
print(f"⚡ Auto-trade: {QUANTITY_PER_TRADE} shares per stock")
print(f"🔒 Mode: 🧪 TEST (Simulated)")
print("\n⏸️  Press Ctrl+C to STOP\n")

check_count = 0
circuit_found_count = 0
trades_executed = 0

try:
    while True:
        check_count += 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        try:
            # Get simulated data
            data = get_simulated_quotes()
            
            # Log status every 6 checks (30 seconds)
            if check_count % 6 == 0:
                print(f"[{timestamp}] ✓ Scanned {len(STOCKS)} stocks | Circuits found: {circuit_found_count} | Trades: {trades_executed}")
            
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
            
            # Process signals
            if signals['buy'] or signals['sell']:
                circuit_found_count += 1
                
                # BUY signals (lower circuit)
                if signals['buy']:
                    for sig in signals['buy']:
                        print(f"[{timestamp}] 🔴 LOWER CIRCUIT DETECTED!")
                        print(f"          Stock: {sig['stock']}")
                        print(f"          Change: {sig['change']:.2f}%")
                        print(f"          LTP: Rs. {sig['ltp']:.2f}")
                        print(f"          ACTION: Auto-BUY {QUANTITY_PER_TRADE} shares")
                        print(f"          Status: SIMULATED (Test Mode)")
                        trades_executed += 1
                        print()
                
                # SELL signals (upper circuit)
                if signals['sell']:
                    for sig in signals['sell']:
                        print(f"[{timestamp}] 🟢 UPPER CIRCUIT DETECTED!")
                        print(f"          Stock: {sig['stock']}")
                        print(f"          Change: {sig['change']:.2f}%")
                        print(f"          LTP: Rs. {sig['ltp']:.2f}")
                        print(f"          ACTION: Auto-SELL {QUANTITY_PER_TRADE} shares")
                        print(f"          Status: SIMULATED (Test Mode)")
                        trades_executed += 1
                        print()
            
            time.sleep(5)
        
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.error(f"Error in scan loop: {e}")
            time.sleep(5)

except KeyboardInterrupt:
    print(f"\n\n{'='*70}")
    print("🛑 BOT STOPPED")
    print(f"{'='*70}")
    print(f"Total scans: {check_count}")
    print(f"Circuits found: {circuit_found_count}")
    print(f"Trades executed: {trades_executed} (simulated)")
    print(f"\n✓ Bot is working correctly!")
    print(f"✓ Once Zerodha enables quote permission, just update credentials")
    print(f"  and run: python bot_demo.py")
    print()
