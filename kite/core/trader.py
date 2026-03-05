"""
Circuit Breaker Trading Bot
Main trading logic - handles placing orders when circuit breakers are hit
"""

import logging
from datetime import datetime, time as dt_time
from typing import Dict
from config.settings import TradingConfig

logger = logging.getLogger(__name__)


class CircuitTrader:
    """Main trading bot - places trades when circuit breaker is hit"""
    
    def __init__(self, kite_client, config: TradingConfig = None):
        """
        Initialize trader
        
        Args:
            kite_client: KiteClient instance
            config: TradingConfig instance (uses default if None)
        """
        self.kite_client = kite_client
        self.config = config or TradingConfig()
        
        # Trading state
        self.positions = {}  # Current open positions
        self.trades_today = 0
        self.daily_loss = 0
        self.trade_log = []
        
        logger.info("CircuitTrader initialized")
    
    def is_trading_hours(self) -> bool:
        """Check if current time is within trading window"""
        current_time = datetime.now().time()
        is_weekday = datetime.now().weekday() < 5  # Mon-Fri
        
        start_time = dt_time(self.config.TRADING_START_HOUR, self.config.TRADING_START_MINUTE)
        end_time = dt_time(self.config.TRADING_END_HOUR, self.config.TRADING_END_MINUTE)
        
        return is_weekday and start_time <= current_time <= end_time
    
    def is_market_close_time(self) -> bool:
        """Check if it's market close time"""
        current_time = datetime.now().time()
        close_time = dt_time(self.config.MARKET_CLOSE_HOUR, self.config.MARKET_CLOSE_MINUTE)
        return current_time >= close_time
    
    def get_circuit_levels(self, ltp: float, previous_close: float) -> Dict:
        """Calculate if stock hit circuit breaker"""
        change_percent = ((ltp - previous_close) / previous_close) * 100
        
        return {
            'change_percent': change_percent,
            'hit_upper_circuit': change_percent >= self.config.UPPER_CIRCUIT_PERCENT,
            'hit_lower_circuit': change_percent <= -self.config.LOWER_CIRCUIT_PERCENT,
            'upper_level': previous_close * (1 + self.config.UPPER_CIRCUIT_PERCENT / 100),
            'lower_level': previous_close * (1 - self.config.LOWER_CIRCUIT_PERCENT / 100),
        }
    
    def check_trade_limits(self) -> bool:
        """Check if we can place more trades (within limits)"""
        if self.trades_today >= self.config.MAX_TRADES_PER_DAY:
            logger.warning(f"Max trades reached ({self.config.MAX_TRADES_PER_DAY})")
            return False
        
        if self.daily_loss >= self.config.MAX_DAILY_LOSS:
            logger.warning(f"Max daily loss reached ({self.config.MAX_DAILY_LOSS})")
            return False
        
        if len(self.positions) >= self.config.MAX_OPEN_POSITIONS:
            logger.warning(f"Max open positions reached ({self.config.MAX_OPEN_POSITIONS})")
            return False
        
        return True
    
    def place_buy_order(self, symbol: str) -> bool:
        """Place a BUY order"""
        if not self.is_trading_hours():
            logger.warning(f"Outside trading hours")
            return False
        
        if not self.check_trade_limits():
            return False
        
        if self.config.TEST_MODE:
            logger.info(f"[TEST] Would BUY {self.config.QUANTITY_PER_TRADE} shares of {symbol}")
            return True
        
        order_id = self.kite_client.place_order(
            symbol=symbol,
            quantity=self.config.QUANTITY_PER_TRADE,
            side="BUY"
        )
        
        if order_id:
            self.positions[symbol] = {
                'symbol': symbol,
                'side': 'BUY',
                'quantity': self.config.QUANTITY_PER_TRADE,
                'order_id': order_id,
                'timestamp': datetime.now(),
            }
            self.trades_today += 1
            logger.info(f"✓ BUY order placed for {symbol}")
            return True
        
        return False
    
    def place_sell_order(self, symbol: str) -> bool:
        """Place a SELL order"""
        if not self.is_trading_hours():
            logger.warning(f"Outside trading hours")
            return False
        
        if self.config.TEST_MODE:
            logger.info(f"[TEST] Would SELL {self.config.QUANTITY_PER_TRADE} shares of {symbol}")
            return True
        
        order_id = self.kite_client.place_order(
            symbol=symbol,
            quantity=self.config.QUANTITY_PER_TRADE,
            side="SELL"
        )
        
        if order_id:
            self.trades_today += 1
            logger.info(f"✓ SELL order placed for {symbol}")
            return True
        
        return False
    
    def close_all_positions(self):
        """Close all open positions (usually at market close)"""
        for symbol in list(self.positions.keys()):
            logger.info(f"Closing position in {symbol}")
            self.place_sell_order(symbol)
            del self.positions[symbol]
    
    def print_status(self):
        """Print current trading status"""
        print("\n" + "="*60)
        print(f"TRADING STATUS - {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        print(f"Trades Today: {self.trades_today}/{self.config.MAX_TRADES_PER_DAY}")
        print(f"Daily Loss: ₹{self.daily_loss}/{self.config.MAX_DAILY_LOSS}")
        print(f"Open Positions: {len(self.positions)}/{self.config.MAX_OPEN_POSITIONS}")
        
        if self.positions:
            print("\nOpen Positions:")
            for symbol, pos in self.positions.items():
                print(f"  - {symbol}: {pos['side']} {pos['quantity']} shares")
        
        print("="*60 + "\n")
