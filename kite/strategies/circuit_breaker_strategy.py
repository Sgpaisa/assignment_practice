"""
Circuit Breaker Trading Strategy
Main trading strategy that monitors stocks and trades when they hit circuit levels
"""

import logging
import time
from datetime import datetime
from typing import List

from config.settings import TradingConfig
from core.kite_client import KiteClient
from core.circuit_finder import CircuitFinder
from core.trader import CircuitTrader

logger = logging.getLogger(__name__)


class CircuitBreakerStrategy:
    """
    Strategy that:
    1. Monitors stocks for circuit breaker hits
    2. Places BUY on lower circuit
    3. Places SELL on upper circuit
    """
    
    def __init__(self, kite_client: KiteClient, config: TradingConfig = None):
        """
        Initialize strategy
        
        Args:
            kite_client: KiteClient instance
            config: TradingConfig instance
        """
        self.config = config or TradingConfig()
        self.kite_client = kite_client
        self.trader = CircuitTrader(kite_client, config)
        self.circuit_finder = CircuitFinder(kite_client, config.UPPER_CIRCUIT_PERCENT)
        self.is_running = False
        
        logger.info("CircuitBreakerStrategy initialized")
    
    def monitor_single_stock(self, symbol: str):
        """
        Monitor a single stock for circuit breaker
        
        Args:
            symbol: Stock symbol to monitor
        """
        logger.info(f"🚀 Starting to monitor {symbol}")
        logger.info(f"Circuit Level: {self.config.UPPER_CIRCUIT_PERCENT}%")
        self.config.print_config()
        
        self.is_running = True
        check_count = 0
        
        try:
            while self.is_running:
                # Check if market is closed
                if self.trader.is_market_close_time():
                    logger.info("Market closed. Exiting...")
                    self.trader.close_all_positions()
                    break
                
                # Get current quote
                quote = self.kite_client.get_quote(symbol)
                
                if not quote:
                    logger.warning(f"Could not fetch quote for {symbol}")
                    time.sleep(self.config.PRICE_CHECK_INTERVAL)
                    continue
                
                ltp = quote.get('last_price', 0)
                previous_close = quote.get('ohlc', {}).get('close', ltp)
                
                # Check circuit breaker
                circuit_info = self.trader.get_circuit_levels(ltp, previous_close)
                change = circuit_info['change_percent']
                
                check_count += 1
                if check_count % self.config.LOG_EVERY_X_CHECKS == 0:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] {symbol}: LTP ₹{ltp:.2f} | Change: {change:+.2f}%")
                
                # Upper circuit hit - SELL signal
                if circuit_info['hit_upper_circuit']:
                    logger.warning(f"⚠️ UPPER CIRCUIT HIT: {symbol} ({change:+.2f}%)")
                    self.trader.place_sell_order(symbol)
                
                # Lower circuit hit - BUY signal
                elif circuit_info['hit_lower_circuit']:
                    logger.warning(f"⚠️ LOWER CIRCUIT HIT: {symbol} ({change:+.2f}%)")
                    self.trader.place_buy_order(symbol)
                
                time.sleep(self.config.PRICE_CHECK_INTERVAL)
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self.stop()
        except Exception as e:
            logger.error(f"Error in monitoring: {e}")
    
    def monitor_multiple_stocks(self, symbols: List[str]):
        """
        Monitor multiple stocks for circuit breaker
        
        Args:
            symbols: List of stock symbols to monitor
        """
        logger.info(f"🚀 Starting to monitor {len(symbols)} stocks")
        logger.info(f"Circuit Level: {self.config.UPPER_CIRCUIT_PERCENT}%")
        self.config.print_config()
        
        self.is_running = True
        check_count = 0
        
        try:
            while self.is_running:
                # Check if market is closed
                if self.trader.is_market_close_time():
                    logger.info("Market closed. Exiting...")
                    self.trader.close_all_positions()
                    break
                
                # Get quotes for all stocks
                quotes = self.kite_client.get_quote_multiple(symbols)
                
                check_count += 1
                if check_count % self.config.LOG_EVERY_X_CHECKS == 0:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"\n[{timestamp}] Checking {len(symbols)} stocks...")
                
                for symbol in symbols:
                    if symbol not in quotes:
                        continue
                    
                    quote = quotes[symbol]
                    ltp = quote.get('last_price', 0)
                    previous_close = quote.get('ohlc', {}).get('close', ltp)
                    
                    circuit_info = self.trader.get_circuit_levels(ltp, previous_close)
                    change = circuit_info['change_percent']
                    
                    if check_count % self.config.LOG_EVERY_X_CHECKS == 0:
                        symbol_display = f"{symbol:<12}"
                        change_display = f"{change:+7.2f}%"
                        print(f"  {symbol_display} LTP: ₹{ltp:>8.2f} | {change_display}")
                    
                    # Upper circuit hit
                    if circuit_info['hit_upper_circuit']:
                        logger.warning(f"⚠️ UPPER: {symbol} ({change:+.2f}%)")
                        self.trader.place_sell_order(symbol)
                    
                    # Lower circuit hit
                    elif circuit_info['hit_lower_circuit']:
                        logger.warning(f"⚠️ LOWER: {symbol} ({change:+.2f}%)")
                        self.trader.place_buy_order(symbol)
                
                time.sleep(self.config.PRICE_CHECK_INTERVAL)
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self.stop()
        except Exception as e:
            logger.error(f"Error in monitoring: {e}")
    
    def auto_detect_and_trade(self):
        """
        Auto-detect stocks hitting circuit and trade them
        Scans NSE 200 continuously - FULLY AUTONOMOUS!
        """
        logger.info("🚀 Starting autonomous circuit trading - scanning NSE 200")
        logger.info(f"Circuit Level: {self.config.UPPER_CIRCUIT_PERCENT}%")
        logger.info(f"Quantity per trade: {self.config.QUANTITY_PER_TRADE}")
        self.config.print_config()
        
        self.is_running = True
        check_count = 0
        
        try:
            while self.is_running:
                if self.trader.is_market_close_time():
                    logger.info("Market closed. Exiting...")
                    self.trader.close_all_positions()
                    break
                
                # Find circuit stocks
                circuit_stocks = self.circuit_finder.find_circuit_stocks()
                
                if circuit_stocks:
                    self.circuit_finder.print_circuit_summary()
                    
                    # Trade on circuit signals - FULLY AUTONOMOUS!
                    buy_stocks = self.circuit_finder.get_circuit_stocks_to_buy()
                    sell_stocks = self.circuit_finder.get_circuit_stocks_to_sell()
                    
                    # AUTO-TRADE without asking
                    for symbol in buy_stocks:
                        logger.info(f"🔔 AUTO-BUYING: {symbol} hit lower circuit!")
                        self.trader.place_buy_order(symbol)
                    
                    for symbol in sell_stocks:
                        logger.info(f"🔔 AUTO-SELLING: {symbol} hit upper circuit!")
                        self.trader.place_sell_order(symbol)
                
                check_count += 1
                if check_count % 3 == 0:  # Log every 3 scans
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    logger.info(f"[{timestamp}] Scanning NSE 200 stocks... {len(circuit_stocks) if circuit_stocks else 0} at circuit")
                
                time.sleep(self.config.PRICE_CHECK_INTERVAL * 2)  # Scan every 10 seconds
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self.stop()
        except Exception as e:
            logger.error(f"Error in auto-detect: {e}")
            import traceback
            traceback.print_exc()
    
    def stop(self):
        """Stop trading"""
        logger.info("Stopping trading...")
        self.is_running = False
        self.trader.close_all_positions()
        self.trader.print_status()
