#!/usr/bin/env python3
"""
🤖 AUTONOMOUS CIRCUIT BREAKER BOT - ROBUST VERSION
Fully automatic trading - just 2 inputs!
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '.')

def main():
    print("\n" + "="*70)
    print("🤖 AUTONOMOUS CIRCUIT BREAKER TRADING BOT")
    print("="*70)
    print("""
AUTO-TRADES NSE 200 STOCKS HITTING CIRCUIT BREAKERSOLELY!

Setup:
  1. Only 2 inputs needed
  2. Circuit % threshold (5-30)
  3. Quantity per stock
  4. Bot runs autonomously - no manual intervention!
    """)
    
    # ============================================================================
    # STEP 1: CHECK CREDENTIALS
    # ============================================================================
    print("\n" + "-"*70)
    print("STEP 1: CHECKING CREDENTIALS")
    print("-"*70)
    
    try:
        from authenticators.token_manager import TokenManager
        api_key, access_token = TokenManager.load_credentials_from_env()
        
        if not api_key or not access_token:
            print("❌ Missing credentials!\n")
            print("Create .env file with:")
            print("  KITE_API_KEY=your_key")
            print("  KITE_ACCESS_TOKEN=your_token")
            print("\nGet from: https://zerodha.com/developers/")
            return
        
        print("✓ Credentials loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return
    
    # ============================================================================
    # STEP 2: GET CIRCUIT PERCENTAGE
    # ============================================================================
    print("\n" + "-"*70)
    print("STEP 2: CIRCUIT PERCENTAGE THRESHOLD")
    print("-"*70)
    print("""
When should bot trade? (choose ONE):
  
  5-10%   → Very Aggressive (many trades)
  15%     → Recommended (balanced)
  20%     → Moderate (fewer trades)
  25-30%  → Conservative (rare trades)
    """)
    
    circuit_pct = None
    while circuit_pct is None:
        try:
            user_input = input("Enter circuit % (5-30): ").strip()
            if not user_input:
                print("❌ Please enter a value")
                continue
            
            pct = float(user_input)
            if 5 <= pct <= 30:
                circuit_pct = pct
                print(f"✓ Circuit threshold: {circuit_pct}%")
            else:
                print(f"❌ Must be between 5-30, got {pct}")
        except ValueError:
            print(f"❌ Invalid input: {user_input}. Enter a number like 15")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            return
    
    # ============================================================================
    # STEP 3: GET QUANTITY
    # ============================================================================
    print("\n" + "-"*70)
    print("STEP 3: QUANTITY PER STOCK")
    print("-"*70)
    print("""
How many shares to trade per stock?

Note: If 10 stocks hit circuit, you'll trade this qty on each!
  
  1-2    → Conservative (small positions)
  3-5    → Recommended (balanced)
  5-10   → Aggressive (larger positions)
    """)
    
    quantity = None
    while quantity is None:
        try:
            user_input = input("Enter quantity (1-100): ").strip()
            if not user_input:
                print("❌ Please enter a value")
                continue
            
            qty = int(user_input)
            if 1 <= qty <= 100:
                quantity = qty
                print(f"✓ Quantity per stock: {quantity} shares")
            else:
                print(f"❌ Must be between 1-100, got {qty}")
        except ValueError:
            print(f"❌ Invalid input: {user_input}. Enter a number like 5")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            return
    
    # ============================================================================
    # STEP 4: TEST OR LIVE?
    # ============================================================================
    print("\n" + "-"*70)
    print("STEP 4: TEST OR LIVE TRADING?")
    print("-"*70)
    print("""
TEST MODE: Simulates trades (safe, no real money)
LIVE MODE: Real trades with your Zerodha account
    """)
    
    test_mode = True  # Default to test
    user_input = input("Start in TEST mode? (Y/N, default=Y): ").strip().lower()
    
    if user_input == 'n':
        print("\n⚠️  WARNING: LIVE TRADING MODE")
        confirm = input("Are you SURE? Real money will be traded (Y/N): ").strip().lower()
        if confirm == 'y':
            test_mode = False
            print("✓ LIVE TRADING ENABLED")
        else:
            print("✓ Staying in TEST mode")
    else:
        print("✓ TEST mode enabled (no real trades)")
    
    # ============================================================================
    # STEP 5: SUMMARY & START
    # ============================================================================
    print("\n" + "="*70)
    print("CONFIGURATION SUMMARY")
    print("="*70)
    print(f"Circuit Threshold:      {circuit_pct}%")
    print(f"Quantity per Stock:     {quantity} shares")
    print(f"Stocks to Monitor:      ALL 200 NSE stocks")
    print(f"Mode:                   {'🧪 TEST (Simulated)' if test_mode else '💰 LIVE TRADING'}")
    print(f"Trading Hours:          9:15 AM - 3:30 PM IST")
    print("="*70)
    
    user_input = input("\n✓ START BOT NOW? (Y/N): ").strip().lower()
    
    if user_input != 'y':
        print("❌ Cancelled")
        return
    
    # ============================================================================
    # START BOT
    # ============================================================================
    print("\n⏳ Starting bot...")
    
    try:
        from config.settings import TradingConfig
        from core.kite_client import KiteClient
        from strategies.circuit_breaker_strategy import CircuitBreakerStrategy
        from utils.logger import setup_logger
        import logging
        
        # Configure
        TradingConfig.UPPER_CIRCUIT_PERCENT = circuit_pct
        TradingConfig.LOWER_CIRCUIT_PERCENT = circuit_pct
        TradingConfig.QUANTITY_PER_TRADE = quantity
        TradingConfig.TEST_MODE = test_mode
        TradingConfig.AUTO_DETECT_CIRCUIT_STOCKS = True
        
        # Setup logging
        logger = setup_logger('kite-bot', TradingConfig.LOG_FILE, logging.INFO)
        
        # Connect
        kite = KiteClient(api_key, access_token)
        
        print("⏳ Testing connection to Kite API...")
        if not kite.is_connected():
            print("❌ Cannot connect to Zerodha Kite API")
            print("\nCheck:")
            print("  - Credentials are correct")
            print("  - Internet connection works")
            print("  - Market is open (9:15 AM - 3:30 PM IST)")
            return
        
        print("✓ Connected to Zerodha Kite API!")
        
        print("\n" + "="*70)
        print("🤖 BOT STARTING - AUTONOMOUS MODE")
        print("="*70)
        print(f"\n📊 Scanning ALL 200 NSE stocks continuously")
        print(f"🎯 Trigger: {circuit_pct}% circuit breaker")
        print(f"⚡ Auto-trade: {quantity} shares per stock")
        print(f"🔒 Mode: {('TEST - Simulated' if test_mode else 'LIVE - Real Trading')}")
        print(f"📁 Log file: trading_bot.log")
        print("\n⏸️  Press Ctrl+C to STOP the bot\n")
        
        # Run bot
        strategy = CircuitBreakerStrategy(kite, TradingConfig)
        strategy.auto_detect_and_trade()
    
    except KeyboardInterrupt:
        print("\n\n✓ Bot stopped by user")
        print("✓ All trades logged to trading_bot.log")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
