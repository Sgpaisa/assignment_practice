#!/usr/bin/env python3
"""
ZERODHA KITE - SIMPLIFIED TRADING BOT
Easy to understand, easy to configure
For testing with ONE stock at a time

STEPS:
1. Edit config.py to set your stock and percentages
2. Run this file: python bot.py
3. Watch the console to see prices and signals
"""

import os
import logging
from datetime import datetime, time as dt_time
from dotenv import load_dotenv
from kiteconnect import KiteConnect

# Load configuration
from config import (
    API_KEY, ACCESS_TOKEN, STOCK_TO_TRADE,
    UPPER_CIRCUIT_PERCENT, LOWER_CIRCUIT_PERCENT,
    QUANTITY_PER_TRADE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT,
    TRADING_START_HOUR, TRADING_START_MINUTE,
    TRADING_END_HOUR, TRADING_END_MINUTE,
    DEBUG_MODE, TEST_MODE, LOG_FILE
)

# ============================================================================
# SETUP LOGGING
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# TRADING BOT CLASS
# ============================================================================
class SimpleTradingBot:
    """
    Simple bot that trades ONE stock at a time
    Easy to understand and configure
    """
    
    def __init__(self):
        """Initialize the bot"""
        logger.info("="*70)
        logger.info("ZERODHA KITE TRADING BOT - STARTING")
        logger.info("="*70)
        
        # Load credentials
        load_dotenv()
        api_key = API_KEY or os.getenv('KITE_API_KEY')
        access_token = ACCESS_TOKEN or os.getenv('KITE_ACCESS_TOKEN')
        
        if not api_key or not access_token:
            logger.error("[FATAL] API credentials not configured!")
            logger.error("        Edit config.py with your API_KEY and ACCESS_TOKEN")
            raise ValueError("Missing API credentials")
        
        # Connect to Kite
        try:
            self.kite = KiteConnect(api_key=api_key)
            self.kite.set_access_token(access_token)
            logger.info(f"[OK] Connected to Zerodha Kite API")
        except Exception as e:
            logger.error(f"[ERROR] Failed to connect to Kite: {e}")
            raise
        
        # Trading parameters
        self.stock = STOCK_TO_TRADE
        self.upper_circuit = UPPER_CIRCUIT_PERCENT
        self.lower_circuit = LOWER_CIRCUIT_PERCENT
        self.quantity = QUANTITY_PER_TRADE
        self.sl_percent = STOP_LOSS_PERCENT
        self.tp_percent = TAKE_PROFIT_PERCENT
        
        # State
        self.position = None
        self.check_count = 0
        
        logger.info(f"\n[CONFIG] Stock: {self.stock}")
        logger.info(f"[CONFIG] Quantity: {self.quantity} shares")
        logger.info(f"[CONFIG] Upper Circuit: {self.upper_circuit}%")
        logger.info(f"[CONFIG] Lower Circuit: {self.lower_circuit}%")
        logger.info(f"[CONFIG] Stop Loss: {self.sl_percent}%")
        logger.info(f"[CONFIG] Take Profit: {self.tp_percent}%")
        
        if TEST_MODE:
            logger.warning("\n[WARNING] TEST MODE ENABLED - No real trades will be placed")
        
        logger.info("="*70 + "\n")
    
    def is_trading_time(self):
        """Check if current time is within trading window"""
        now = datetime.now()
        current_time = now.time()
        is_weekday = now.weekday() < 5  # Monday to Friday
        
        trading_start = dt_time(TRADING_START_HOUR, TRADING_START_MINUTE)
        trading_end = dt_time(TRADING_END_HOUR, TRADING_END_MINUTE)
        
        within_hours = trading_start <= current_time <= trading_end
        
        return is_weekday and within_hours
    
    def get_stock_data(self):
        """
        Fetch current stock price data
        Returns: dict with price, previous close, and circuit levels
        """
        try:
            # Get quote using NSE format
            quote = self.kite.quote(f"NSE:{self.stock}")[f"NSE:{self.stock}"]
            
            ltp = quote['last_price']
            prev_close = quote['ohlc']['close']
            
            # Calculate circuit levels
            upper_level = prev_close * (1 + self.upper_circuit / 100)
            lower_level = prev_close * (1 - self.lower_circuit / 100)
            
            # Calculate change percentage
            change_pct = ((ltp - prev_close) / prev_close) * 100
            
            return {
                'ltp': ltp,
                'prev_close': prev_close,
                'upper_circuit': upper_level,
                'lower_circuit': lower_level,
                'change_pct': change_pct,
                'bid': quote['bid'],
                'ask': quote['ask']
            }
        
        except Exception as e:
            logger.error(f"[ERROR] Could not fetch data for {self.stock}: {e}")
            return None
    
    def check_circuit_status(self, data):
        """
        Check if stock hit circuit breaker
        Returns: 'UPPER', 'LOWER', or 'NONE'
        """
        if not data:
            return 'NONE'
        
        ltp = data['ltp']
        upper = data['upper_circuit']
        lower = data['lower_circuit']
        
        # Check upper circuit (95% threshold to catch near-circuit)
        if ltp >= upper * 0.95:
            return 'UPPER'
        
        # Check lower circuit
        if ltp <= lower * 1.05:
            return 'LOWER'
        
        return 'NONE'
    
    def place_order(self, symbol, order_type, price):
        """
        Place buy or sell order
        order_type: 'BUY' or 'SELL'
        """
        if TEST_MODE:
            logger.warning(f"[TEST] Would place {order_type} order for {symbol} at Rs. {price:.2f}")
            return f"TEST_ORDER_{order_type}"
        
        try:
            order_id = self.kite.place_order(
                variety='regular',
                exchange='NSE',
                tradingsymbol=f"NSE:{self.stock}",
                transaction_type=order_type,
                quantity=self.quantity,
                price=int(price),
                order_type='limit',
                product='MIS'  # Intraday
            )
            
            logger.info(f"\n[ORDER PLACED] {order_type} {self.quantity} @ Rs. {price:.2f}")
            logger.info(f"               Order ID: {order_id}\n")
            
            return order_id
        
        except Exception as e:
            logger.error(f"[ERROR] Failed to place order: {e}")
            return None
    
    def check_and_trade(self):
        """
        Main trading logic
        Checks price and executes trades
        """
        # Check if within trading hours
        if not self.is_trading_time():
            return
        
        # Get current data
        data = self.get_stock_data()
        if not data:
            return
        
        self.check_count += 1
        
        # Print prices periodically (to reduce console spam)
        if self.check_count % 5 == 0:
            self._print_prices(data)
        
        # Check circuit status
        circuit_status = self.check_circuit_status(data)
        
        if circuit_status == 'UPPER':
            self._handle_upper_circuit(data)
        
        elif circuit_status == 'LOWER':
            self._handle_lower_circuit(data)
    
    def _print_prices(self, data):
        """Print current stock prices"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {self.stock}")
        print(f"  LTP: Rs. {data['ltp']:.2f} | Change: {data['change_pct']:+.1f}%")
        print(f"  Bid: Rs. {data['bid']:.2f} | Ask: Rs. {data['ask']:.2f}")
        print(f"  Upper Circuit: Rs. {data['upper_circuit']:.2f}")
        print(f"  Lower Circuit: Rs. {data['lower_circuit']:.2f}")
        
        if self.position:
            print(f"  [POSITION OPEN] {self.position['type']} @ Rs. {self.position['entry']:.2f}")
    
    def _handle_upper_circuit(self, data):
        """Handle upper circuit hit - SELL signal"""
        ltp = data['ltp']
        
        logger.warning(f"\n{'*'*70}")
        logger.warning(f"UPPER CIRCUIT HIT for {self.stock}!")
        logger.warning(f"Stock price: Rs. {ltp:.2f}")
        logger.warning(f"Circuit level: Rs. {data['upper_circuit']:.2f}")
        logger.warning(f"{'*'*70}\n")
        
        # Place sell order
        order_id = self.place_order(self.stock, 'SELL', int(ltp))
        
        if order_id:
            self.position = {
                'type': 'SHORT',
                'entry': ltp,
                'order_id': order_id,
                'stop_loss': ltp * (1 + self.sl_percent / 100),
                'take_profit': ltp * (1 - self.tp_percent / 100)
            }
            
            logger.info(f"Position: SHORT at Rs. {ltp:.2f}")
            logger.info(f"Stop Loss: Rs. {self.position['stop_loss']:.2f}")
            logger.info(f"Take Profit: Rs. {self.position['take_profit']:.2f}\n")
    
    def _handle_lower_circuit(self, data):
        """Handle lower circuit hit - BUY signal"""
        ltp = data['ltp']
        
        logger.warning(f"\n{'*'*70}")
        logger.warning(f"LOWER CIRCUIT HIT for {self.stock}!")
        logger.warning(f"Stock price: Rs. {ltp:.2f}")
        logger.warning(f"Circuit level: Rs. {data['lower_circuit']:.2f}")
        logger.warning(f"{'*'*70}\n")
        
        # Place buy order
        order_id = self.place_order(self.stock, 'BUY', int(ltp))
        
        if order_id:
            self.position = {
                'type': 'LONG',
                'entry': ltp,
                'order_id': order_id,
                'stop_loss': ltp * (1 - self.sl_percent / 100),
                'take_profit': ltp * (1 + self.tp_percent / 100)
            }
            
            logger.info(f"Position: LONG at Rs. {ltp:.2f}")
            logger.info(f"Stop Loss: Rs. {self.position['stop_loss']:.2f}")
            logger.info(f"Take Profit: Rs. {self.position['take_profit']:.2f}\n")
    
    def run(self):
        """Main loop - runs continuously"""
        logger.info(f"[RUNNING] Monitoring {self.stock} for circuit breakers...")
        logger.info(f"[RUNNING] Trading hours: {TRADING_START_HOUR}:{TRADING_START_MINUTE:02d} - {TRADING_END_HOUR}:{TRADING_END_MINUTE:02d}")
        logger.info(f"[RUNNING] Press Ctrl+C to stop\n")
        
        import time
        import schedule
        
        # Check every 30 seconds
        schedule.every(30).seconds.do(self.check_and_trade)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("\n\n[STOPPED] Bot stopped by user")
            logger.info("="*70)


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    try:
        bot = SimpleTradingBot()
        bot.run()
    
    except ValueError as e:
        logger.error(f"\n[FATAL] {e}")
    
    except Exception as e:
        logger.error(f"\n[FATAL] Unexpected error: {e}")
