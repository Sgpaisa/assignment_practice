"""
AUTONOMOUS CIRCUIT BREAKER BOT - FULLY AUTOMATED
Just set 2 parameters: circuit % and quantity
Then it auto-trades any NSE 200 stock hitting the circuit!
"""

import sys
import os
sys.path.insert(0, '.')

from config.settings import TradingConfig
from authenticators.token_manager import TokenManager
import logging


def autonomous_bot_setup():
    """
    Minimal setup - only ask for circuit % and quantity
    Then run fully autonomous trading
    """
    print("\n" + "="*70)
    print("🤖 AUTONOMOUS CIRCUIT BREAKER TRADING BOT")
    print("="*70)
    print("""
Your bot will:
1. Scan ALL 200 NSE stocks continuously
2. Detect when ANY stock hits your circuit % threshold
3. AUTO-TRADE immediately (no asking)
4. Execute the quantity you specify
5. Repeat until market close

You only need to set:
  • Circuit %: 5-30% (how much stock must move to trigger trade)
  • Quantity: shares per trade
  
That's it! 🚀
    """)
    
    # Step 1: Check credentials
    print("\n" + "-"*70)
    print("STEP 1: CHECK CREDENTIALS")
    print("-"*70)
    
    api_key, access_token = TokenManager.load_credentials_from_env()
    
    if not api_key or not access_token:
        print("❌ Missing credentials in .env file\n")
        print("Create a .env file with:")
        print("  KITE_API_KEY=your_key_here")
        print("  KITE_ACCESS_TOKEN=your_token_here")
        print("\nGet credentials from: https://zerodha.com/developers/")
        return
    
    print("✓ Credentials loaded from .env")
    
    # Step 2: Ask for circuit percentage
    print("\n" + "-"*70)
    print("STEP 2: CIRCUIT PERCENTAGE THRESHOLD")
    print("-"*70)
    print("""
Choose when to trigger trades:
  • 5-10%:   VERY AGGRESSIVE (many trades, higher risk)
  • 15-20%:  MODERATE       (balanced, recommended)
  • 25-30%:  CONSERVATIVE   (fewer trades, lower risk)

Example: 20% means:
  - Stock up 20% → AUTO SELL ✓
  - Stock down 20% → AUTO BUY ✓
    """)
    
    while True:
        try:
            circuit_pct = float(input("Enter circuit % (5-30): ").strip())
            if 5 <= circuit_pct <= 30:
                break
            else:
                print("❌ Please enter a value between 5 and 30")
        except:
            print("❌ Invalid input. Enter a number like 15 or 20")
    
    print(f"✓ Circuit threshold: {circuit_pct}%")
    
    # Step 3: Ask for quantity
    print("\n" + "-"*70)
    print("STEP 3: QUANTITY PER TRADE")
    print("-"*70)
    print("""
How many shares to trade for EACH stock that hits circuit?

Recommendation:
  • Conservative: 1-2 shares
  • Moderate:     2-5 shares
  • Aggressive:   5-10 shares

⚠️ You'll trade with MULTIPLE STOCKS in parallel!
If 10 stocks hit circuit, you'll execute qty on each = 10x total quantity
    """)
    
    while True:
        try:
            qty = int(input("Enter quantity per stock (1-100): ").strip())
            if 1 <= qty <= 100:
                break
            else:
                print("❌ Please enter a value between 1 and 100")
        except:
            print("❌ Invalid input. Enter a number like 1, 2, or 5")
    
    print(f"✓ Quantity per stock: {qty}")
    
    # Step 4: Test mode?
    print("\n" + "-"*70)
    print("STEP 4: TEST OR REAL TRADING?")
    print("-"*70)
    print("""
TEST MODE: Simulates trades without real money (recommended first time)
REAL MODE: Executes actual trades with your Zerodha account
    """)
    
    test = input("Use TEST mode first? (Y/N): ").lower().strip()
    test_mode = test == 'y'
    
    if test_mode:
        print("✓ TEST MODE ENABLED - No real orders will be placed")
    else:
        confirm = input("\n⚠️ REAL TRADING - Are you sure? (Y/N): ").lower().strip()
        if confirm != 'y':
            print("❌ Cancelled")
            return
        print("✓ REAL TRADING MODE - Orders will be placed!")
    
    # Step 5: Summary
    print("\n" + "="*70)
    print("BOT CONFIGURATION SUMMARY")
    print("="*70)
    print(f"Circuit Threshold:    {circuit_pct}%")
    print(f"Quantity per Stock:   {qty} shares")
    print(f"Stocks to Monitor:    ALL 200 NSE stocks")
    print(f"Mode:                 {'🧪 TEST (Simulated)' if test_mode else '💰 REAL TRADING'}")
    print(f"Trading Hours:        9:15 AM - 3:30 PM IST")
    print("="*70)
    
    confirm = input("\n✓ START AUTONOMOUS BOT? (Y/N): ").lower().strip()
    
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Update configuration
    TradingConfig.UPPER_CIRCUIT_PERCENT = circuit_pct
    TradingConfig.LOWER_CIRCUIT_PERCENT = circuit_pct
    TradingConfig.QUANTITY_PER_TRADE = qty
    TradingConfig.TEST_MODE = test_mode
    TradingConfig.AUTO_DETECT_CIRCUIT_STOCKS = True  # Enable auto-detect
    
    # Step 6: Connect and run
    print("\n⏳ Connecting to Zerodha Kite API...")
    
    from core.kite_client import KiteClient
    from strategies.circuit_breaker_strategy import CircuitBreakerStrategy
    from utils.logger import setup_logger
    
    try:
        # Setup logging
        logger = setup_logger('kite-bot', TradingConfig.LOG_FILE, logging.INFO)
        
        # Connect to Kite
        kite = KiteClient(api_key, access_token)
        
        print("⏳ Testing connection...")
        if not kite.is_connected():
            print("❌ Cannot connect to Kite API")
            print("\nTroubleshooting:")
            print("- Check if credentials are correct")
            print("- Check internet connection")
            print("- Make sure market is open (9:15 AM - 3:30 PM IST)")
            return
        
        print("✓ Connected to Zerodha Kite API!")
        
        print("\n" + "="*70)
        print("🤖 BOT STARTING - AUTONOMOUS MODE")
        print("="*70)
        print(f"\n📊 Monitoring ALL 200 NSE stocks for {circuit_pct}% circuit breaker")
        print(f"⚡ Will auto-execute {qty} shares when ANY stock hits circuit")
        print(f"🔒 Mode: {('TEST - No real trades' if test_mode else 'REAL TRADING - Live orders')}")
        print(f"📁 Logs saved to: trading_bot.log")
        print("\n⏸️  Press Ctrl+C to STOP\n")
        
        # Run autonomous bot
        strategy = CircuitBreakerStrategy(kite, TradingConfig)
        strategy.auto_detect_and_trade()
    
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
        print("Summary saved to trading_bot.log")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    autonomous_bot_setup()

