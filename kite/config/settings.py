"""
Trading Configuration Settings
Edit this file OR use environment variables to customize your trading
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TradingConfig:
    """Main configuration class for trading bot"""
    
    # =================================================================
    # CREDENTIALS (Load from .env file)
    # =================================================================
    API_KEY = os.getenv('KITE_API_KEY', '')
    ACCESS_TOKEN = os.getenv('KITE_ACCESS_TOKEN', '')
    
    # =================================================================
    # STOCK SELECTION
    # =================================================================
    # Single stock to trade (or use MULTIPLE_STOCKS for multiple)
    STOCK_TO_TRADE = "HDFCBANK"  # Change this to any NSE 200 stock
    
    # Trade multiple stocks (set to None to use STOCK_TO_TRADE instead)
    MULTIPLE_STOCKS = None  # Example: ["HDFCBANK", "INFY", "TCS"]
    
    # Auto-detect and trade stocks that hit circuit breaker
    AUTO_DETECT_CIRCUIT_STOCKS = False  # Set to True to auto-find circuit stocks
    
    # =================================================================
    # CIRCUIT BREAKER SETTINGS (These are the key parameters)
    # =================================================================
    # EASY TO CHANGE: Adjust these percentages as you want
    UPPER_CIRCUIT_PERCENT = 20  # Stock goes UP by X% -> SELL signal
    LOWER_CIRCUIT_PERCENT = 20  # Stock goes DOWN by X% -> BUY signal
    
    # Examples:
    # - For aggressive: set to 5-10%
    # - For moderate: set to 15-20%
    # - For conservative: set to 25-30%
    
    # =================================================================
    # POSITION MANAGEMENT
    # =================================================================
    QUANTITY_PER_TRADE = 1          # Number of shares per trade
    STOP_LOSS_PERCENT = 2           # Exit if price drops by this %
    TAKE_PROFIT_PERCENT = 5         # Exit if price rises by this %
    
    # =================================================================
    # RISK MANAGEMENT
    # =================================================================
    MAX_DAILY_LOSS = 100            # Stop trading if daily loss exceeds this
    MAX_TRADES_PER_DAY = 10         # Maximum trades in a day
    MAX_OPEN_POSITIONS = 2          # Max simultaneous positions
    
    # =================================================================
    # TRADING HOURS
    # =================================================================
    # Only trade during these hours (IST - Indian Standard Time)
    TRADING_START_HOUR = 9
    TRADING_START_MINUTE = 15       # Market opens at 9:15 AM
    
    TRADING_END_HOUR = 12
    TRADING_END_MINUTE = 15         # Trade until 12:15 PM (first 3 hours)
    
    # Auto-close all positions at market close
    AUTO_CLOSE_AT_MARKET_CLOSE = True
    MARKET_CLOSE_HOUR = 15
    MARKET_CLOSE_MINUTE = 30        # Market closes at 3:30 PM
    
    # =================================================================
    # MONITORING & REFRESH SETTINGS
    # =================================================================
    PRICE_CHECK_INTERVAL = 5        # Check prices every X seconds
    LOG_EVERY_X_CHECKS = 5          # Log status every X checks
    
    # =================================================================
    # DEBUG & TEST MODE
    # =================================================================
    DEBUG_MODE = True               # Print detailed logs
    TEST_MODE = False               # True = simulate without trading, False = real trading
    VERBOSE = True                  # Print all details
    
    # =================================================================
    # LOGGING
    # =================================================================
    LOG_FILE = "trading_bot.log"
    LOG_LEVEL = "INFO"              # DEBUG, INFO, WARNING, ERROR
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("\n" + "="*60)
        print("CURRENT TRADING CONFIGURATION")
        print("="*60)
        print(f"Stock to Trade: {cls.STOCK_TO_TRADE}")
        print(f"Circuit Breaker: {cls.UPPER_CIRCUIT_PERCENT}%")
        print(f"Quantity per Trade: {cls.QUANTITY_PER_TRADE}")
        print(f"Stop Loss: {cls.STOP_LOSS_PERCENT}%")
        print(f"Take Profit: {cls.TAKE_PROFIT_PERCENT}%")
        print(f"Trading Hours: {cls.TRADING_START_HOUR}:{cls.TRADING_START_MINUTE:02d} - {cls.TRADING_END_HOUR}:{cls.TRADING_END_MINUTE:02d}")
        print(f"Test Mode: {cls.TEST_MODE}")
        print("="*60 + "\n")
    
    @classmethod
    def update(cls, **kwargs):
        """Dynamically update configuration"""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
            else:
                raise ValueError(f"Unknown setting: {key}")


# Preset configurations for different trading styles
class ConservativeConfig(TradingConfig):
    """Low-risk trading configuration"""
    UPPER_CIRCUIT_PERCENT = 10
    LOWER_CIRCUIT_PERCENT = 10
    QUANTITY_PER_TRADE = 1
    STOP_LOSS_PERCENT = 1
    TAKE_PROFIT_PERCENT = 3
    MAX_TRADES_PER_DAY = 5


class ModerateConfig(TradingConfig):
    """Medium-risk trading configuration"""
    UPPER_CIRCUIT_PERCENT = 15
    LOWER_CIRCUIT_PERCENT = 15
    QUANTITY_PER_TRADE = 2
    STOP_LOSS_PERCENT = 2
    TAKE_PROFIT_PERCENT = 5


class AggressiveConfig(TradingConfig):
    """High-risk trading configuration"""
    UPPER_CIRCUIT_PERCENT = 20
    LOWER_CIRCUIT_PERCENT = 20
    QUANTITY_PER_TRADE = 5
    STOP_LOSS_PERCENT = 3
    TAKE_PROFIT_PERCENT = 10
    MAX_TRADES_PER_DAY = 15
