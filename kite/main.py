"""
MAIN TRADING BOT - Easy to Use
Change the settings below and run this file to start trading
"""

import logging
import sys
sys.path.insert(0, '.')

from config.settings import TradingConfig
from config.nse200_stocks import get_all_stocks, get_all_sectors
from core.kite_client import KiteClient
from strategies.circuit_breaker_strategy import CircuitBreakerStrategy
from utils.logger import setup_logger
from authenticators.token_manager import TokenManager


def print_menu():
    """Print main menu"""
    print("\n" + "="*70)
    print("CIRCUIT BREAKER TRADING BOT - SELECT MODE")
    print("="*70)
    print("""
1. Monitor SINGLE stock for circuit breaker
2. Monitor MULTIPLE stocks for circuit breaker  
3. AUTO-DETECT and trade circuit stocks (NSE 200)
4. View NSE 200 stocks
5. Exit
    """)
    print("="*70)


def print_stocks():
    """Print available stocks"""
    print("\n" + "="*70)
    print("NSE 200 STOCKS - BY SECTOR")
    print("="*70)
    
    from config.nse200_stocks import NSE_200_STOCKS
    
    for sector, stocks in NSE_200_STOCKS.items():
        print(f"\n{sector}:")
        for symbol, name in stocks.items():
            print(f"  {symbol:<15} - {name}")
    
    print("\n" + "="*70 + "\n")


def mode_single_stock():
    """Mode 1: Monitor single stock"""
    print("\n" + "="*70)
    print("MODE 1: MONITOR SINGLE STOCK")
    print("="*70)
    
    # Get stock symbol
    symbol = input("Enter stock symbol (e.g., HDFCBANK): ").upper().strip()
    
    all_stocks = get_all_stocks()
    if symbol not in all_stocks:
        print(f"❌ Invalid stock: {symbol}")
        print(f"List of stocks: {', '.join(list(all_stocks.keys())[:10])}...")
        return
    
    # Get circuit percentage
    circuit_pct = input("Enter circuit % (default 20): ").strip()
    if circuit_pct:
        try:
            TradingConfig.UPPER_CIRCUIT_PERCENT = float(circuit_pct)
            TradingConfig.LOWER_CIRCUIT_PERCENT = float(circuit_pct)
        except:
            print("Invalid percentage, using default 20%")
    
    # Get quantity
    qty = input("Enter quantity per trade (default 1): ").strip()
    if qty:
        try:
            TradingConfig.QUANTITY_PER_TRADE = int(qty)
        except:
            print("Invalid quantity, using default 1")
    
    # Test mode?
    test = input("Test mode (Y/N, default N): ").lower().strip()
    if test == 'y':
        TradingConfig.TEST_MODE = True
        print("✓ Running in TEST MODE (no real trades)")
    
    print(f"\n✓ Stock: {symbol}")
    print(f"✓ Circuit Level: {TradingConfig.UPPER_CIRCUIT_PERCENT}%")
    print(f"✓ Quantity: {TradingConfig.QUANTITY_PER_TRADE}")
    print(f"✓ Test Mode: {TradingConfig.TEST_MODE}\n")
    
    # Get credentials
    api_key, access_token = TokenManager.load_credentials_from_env()
    if not api_key or not access_token:
        print("❌ Missing credentials in .env file")
        TokenManager.print_setup_instructions()
        return
    
    # Setup logging
    logger = setup_logger('kite-bot', TradingConfig.LOG_FILE, logging.INFO)
    
    # Start trading
    try:
        kite = KiteClient(api_key, access_token)
        
        if not kite.is_connected():
            print("❌ Cannot connect to Kite API")
            return
        
        print("✓ Connected to Kite API")
        
        strategy = CircuitBreakerStrategy(kite, TradingConfig)
        strategy.monitor_single_stock(symbol)
    
    except Exception as e:
        print(f"❌ Error: {e}")


def mode_multiple_stocks():
    """Mode 2: Monitor multiple stocks"""
    print("\n" + "="*70)
    print("MODE 2: MONITOR MULTIPLE STOCKS")
    print("="*70)
    
    stocks_input = input("Enter stock symbols (comma-separated, e.g., HDFCBANK,INFY,TCS): ").upper().strip()
    symbols = [s.strip() for s in stocks_input.split(',')]
    
    # Validate stocks
    all_stocks = get_all_stocks()
    invalid = [s for s in symbols if s not in all_stocks]
    
    if invalid:
        print(f"❌ Invalid stocks: {', '.join(invalid)}")
        return
    
    # Get circuit percentage
    circuit_pct = input("Enter circuit % (default 20): ").strip()
    if circuit_pct:
        try:
            TradingConfig.UPPER_CIRCUIT_PERCENT = float(circuit_pct)
            TradingConfig.LOWER_CIRCUIT_PERCENT = float(circuit_pct)
        except:
            print("Invalid percentage, using default 20%")
    
    # Get quantity
    qty = input("Enter quantity per trade (default 1): ").strip()
    if qty:
        try:
            TradingConfig.QUANTITY_PER_TRADE = int(qty)
        except:
            print("Invalid quantity, using default 1")
    
    # Test mode?
    test = input("Test mode (Y/N, default N): ").lower().strip()
    if test == 'y':
        TradingConfig.TEST_MODE = True
    
    print(f"\n✓ Stocks: {', '.join(symbols)}")
    print(f"✓ Circuit Level: {TradingConfig.UPPER_CIRCUIT_PERCENT}%")
    print(f"✓ Quantity: {TradingConfig.QUANTITY_PER_TRADE}")
    print(f"✓ Test Mode: {TradingConfig.TEST_MODE}\n")
    
    # Get credentials
    api_key, access_token = TokenManager.load_credentials_from_env()
    if not api_key or not access_token:
        print("❌ Missing credentials in .env file")
        TokenManager.print_setup_instructions()
        return
    
    # Setup logging
    logger = setup_logger('kite-bot', TradingConfig.LOG_FILE, logging.INFO)
    
    # Start trading
    try:
        kite = KiteClient(api_key, access_token)
        if not kite.is_connected():
            print("❌ Cannot connect to Kite API")
            return
        
        print("✓ Connected to Kite API\n")
        
        strategy = CircuitBreakerStrategy(kite, TradingConfig)
        strategy.monitor_multiple_stocks(symbols)
    
    except Exception as e:
        print(f"❌ Error: {e}")


def mode_auto_detect():
    """Mode 3: Auto-detect circuit stocks"""
    print("\n" + "="*70)
    print("MODE 3: AUTO-DETECT CIRCUIT STOCKS (NSE 200)")
    print("="*70)
    
    # Get circuit percentage
    circuit_pct = input("Enter circuit % (default 20): ").strip()
    if circuit_pct:
        try:
            TradingConfig.UPPER_CIRCUIT_PERCENT = float(circuit_pct)
            TradingConfig.LOWER_CIRCUIT_PERCENT = float(circuit_pct)
        except:
            print("Invalid percentage, using default 20%")
    
    # Get quantity
    qty = input("Enter quantity per trade (default 1): ").strip()
    if qty:
        try:
            TradingConfig.QUANTITY_PER_TRADE = int(qty)
        except:
            print("Invalid quantity, using default 1")
    
    # Test mode?
    test = input("Test mode (Y/N, default N): ").lower().strip()
    if test == 'y':
        TradingConfig.TEST_MODE = True
    
    print(f"\n✓ Circuit Level: {TradingConfig.UPPER_CIRCUIT_PERCENT}%")
    print(f"✓ Quantity: {TradingConfig.QUANTITY_PER_TRADE}")
    print(f"✓ Test Mode: {TradingConfig.TEST_MODE}")
    print(f"✓ Will auto-detect and trade {len(get_all_stocks())} NSE 200 stocks\n")
    
    # Get credentials
    api_key, access_token = TokenManager.load_credentials_from_env()
    if not api_key or not access_token:
        print("❌ Missing credentials in .env file")
        TokenManager.print_setup_instructions()
        return
    
    # Setup logging
    logger = setup_logger('kite-bot', TradingConfig.LOG_FILE, logging.INFO)
    
    # Start trading
    try:
        kite = KiteClient(api_key, access_token)
        if not kite.is_connected():
            print("❌ Cannot connect to Kite API")
            return
        
        print("✓ Connected to Kite API\n")
        
        strategy = CircuitBreakerStrategy(kite, TradingConfig)
        strategy.auto_detect_and_trade()
    
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main menu"""
    print("\n🚀 ZERODHA KITE CIRCUIT BREAKER TRADING BOT")
    print("="*70)
    
    while True:
        print_menu()
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            mode_single_stock()
        elif choice == '2':
            mode_multiple_stocks()
        elif choice == '3':
            mode_auto_detect()
        elif choice == '4':
            print_stocks()
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main()
