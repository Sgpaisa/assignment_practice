"""
Zerodha Kite Circuit Breaker Trading Bot
Author: Trading Bot
Description: Automatically places buy/sell orders when stocks hit upper/lower circuit breakers
             within the first 3 hours of trading (9:15 AM - 12:15 PM IST)
"""

import logging
from datetime import datetime, time
from typing import Dict, List, Tuple
import schedule
import time as time_module
from kiteconnect import KiteConnect

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('circuit_trader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CircuitTrader:
    """Trading bot that trades on circuit breaker levels"""
    
    def __init__(self, api_key: str, access_token: str):
        """
        Initialize Kite connection
        Args:
            api_key: Your Kite API key
            access_token: Your Kite access token (from redirect after login)
        """
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)
        self.api_key = api_key
        self.access_token = access_token
        
        # Trading parameters
        self.trading_start = time(9, 15)      # Market opening
        self.trading_end = time(12, 15)       # First 3 hours end
        self.market_close = time(15, 30)      # Market closing
        
        # Circuit breaker levels (percentage)
        self.upper_circuit = 20  # 20% up
        self.lower_circuit = 20  # 20% down
        
        # Risk management
        self.quantity_per_trade = 1
        self.stop_loss_percent = 2
        self.take_profit_percent = 5
        
        # Storage for active positions
        self.positions = {}
        self.order_log = []
        
        logger.info("CircuitTrader initialized")
    
    def is_within_trading_window(self) -> bool:
        """Check if current time is within first 3 hours of trading"""
        current_time = datetime.now().time()
        is_weekday = datetime.now().weekday() < 5  # Monday to Friday
        return is_weekday and self.trading_start <= current_time <= self.trading_end
    
    def get_circuit_levels(self, ltp: float, previous_close: float) -> Dict:
        """
        Calculate circuit breaker levels
        Args:
            ltp: Last Traded Price
            previous_close: Previous day closing price
        
        Returns:
            Dict with upper_circuit_price and lower_circuit_price
        """
        upper_level = previous_close * (1 + self.upper_circuit / 100)
        lower_level = previous_close * (1 - self.lower_circuit / 100)
        
        return {
            'upper_circuit_price': upper_level,
            'lower_circuit_price': lower_level,
            'previous_close': previous_close,
            'current_change_percent': ((ltp - previous_close) / previous_close) * 100
        }
    
    def get_instrument_data(self, symbol: str) -> Dict:
        """
        Get instrument data including LTP and previous close
        Args:
            symbol: Stock symbol (e.g., 'INFY', 'TCS')
        
        Returns:
            Dict with price data
        """
        try:
            # Get quote data
            data = self.kite.quote(symbols=[symbol])
            if symbol in data['data']:
                quote = data['data'][symbol]
                return {
                    'symbol': symbol,
                    'ltp': quote['last_price'],
                    'previous_close': quote['ohlc']['close'],
                    'bid': quote['bid'],
                    'ask': quote['ask'],
                    'volume': quote['volume'],
                    'open_interest': quote['oi']
                }
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
        
        return None
    
    def check_circuit_levels(self, symbol: str) -> Tuple[bool, str, float]:
        """
        Check if stock has hit circuit breaker levels
        Args:
            symbol: Stock symbol
        
        Returns:
            Tuple: (is_at_circuit, circuit_type, price)
                   circuit_type: 'UPPER', 'LOWER', or 'NONE'
        """
        data = self.get_instrument_data(symbol)
        
        if not data:
            return False, 'NONE', 0
        
        ltp = data['ltp']
        previous_close = data['previous_close']
        
        circuit_levels = self.get_circuit_levels(ltp, previous_close)
        
        # Check if at upper circuit (stock price is at or very close to upper level)
        if ltp >= circuit_levels['upper_circuit_price'] * 0.98:
            logger.warning(f"{symbol} hit UPPER CIRCUIT. LTP: {ltp}")
            return True, 'UPPER', ltp
        
        # Check if at lower circuit (stock price is at or very close to lower level)
        if ltp <= circuit_levels['lower_circuit_price'] * 1.02:
            logger.warning(f"{symbol} hit LOWER CIRCUIT. LTP: {ltp}")
            return True, 'LOWER', ltp
        
        return False, 'NONE', ltp
    
    def place_order(self, symbol: str, transaction_type: str, price: float, 
                   quantity: int = None) -> Dict:
        """
        Place order on Kite
        Args:
            symbol: Stock symbol
            transaction_type: 'BUY' or 'SELL'
            price: Order price
            quantity: Number of shares
        
        Returns:
            Dict with order details
        """
        if quantity is None:
            quantity = self.quantity_per_trade
        
        try:
            order_id = self.kite.place_order(
                variety=self.kite.VARIETY_REGULAR,
                exchange=self.kite.EXCHANGE_NSE,
                tradingsymbol=symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                price=price,
                order_type=self.kite.ORDER_TYPE_LIMIT,
                product=self.kite.PRODUCT_MIS  # Intraday
            )
            
            order_info = {
                'order_id': order_id,
                'symbol': symbol,
                'transaction_type': transaction_type,
                'quantity': quantity,
                'price': price,
                'timestamp': datetime.now(),
                'status': 'PLACED'
            }
            
            self.order_log.append(order_info)
            logger.info(f"Order placed: {order_info}")
            
            return order_info
        
        except Exception as e:
            logger.error(f"Error placing order for {symbol}: {e}")
            return None
    
    def execute_circuit_trade(self, symbol: str):
        """
        Execute trade when circuit is hit
        Args:
            symbol: Stock symbol
        """
        is_circuit, circuit_type, price = self.check_circuit_levels(symbol)
        
        if not is_circuit:
            return
        
        if not self.is_within_trading_window():
            logger.info(f"Outside trading window for {symbol}. Skipping trade.")
            return
        
        try:
            if circuit_type == 'UPPER':
                # Upper circuit hit - SELL (stock is overvalued)
                logger.info(f"Initiating SELL for {symbol} at upper circuit ({price})")
                order = self.place_order(symbol, 'SELL', price)
                
                if order:
                    self.positions[symbol] = {
                        'type': 'SHORT',
                        'entry_price': price,
                        'quantity': self.quantity_per_trade,
                        'stop_loss': price * (1 + self.stop_loss_percent / 100),
                        'take_profit': price * (1 - self.take_profit_percent / 100)
                    }
            
            elif circuit_type == 'LOWER':
                # Lower circuit hit - BUY (stock is undervalued)
                logger.info(f"Initiating BUY for {symbol} at lower circuit ({price})")
                order = self.place_order(symbol, 'BUY', price)
                
                if order:
                    self.positions[symbol] = {
                        'type': 'LONG',
                        'entry_price': price,
                        'quantity': self.quantity_per_trade,
                        'stop_loss': price * (1 - self.stop_loss_percent / 100),
                        'take_profit': price * (1 + self.take_profit_percent / 100)
                    }
        
        except Exception as e:
            logger.error(f"Error executing circuit trade for {symbol}: {e}")
    
    def monitor_positions(self):
        """Monitor active positions and exit based on SL/TP"""
        for symbol, position in list(self.positions.items()):
            try:
                data = self.get_instrument_data(symbol)
                if not data:
                    continue
                
                current_price = data['ltp']
                
                # Check stop loss
                if position['type'] == 'LONG':
                    if current_price <= position['stop_loss']:
                        logger.warning(f"Stop loss hit for {symbol}. Exiting LONG.")
                        self.place_order(symbol, 'SELL', current_price, position['quantity'])
                        del self.positions[symbol]
                    
                    elif current_price >= position['take_profit']:
                        logger.info(f"Take profit hit for {symbol}. Exiting LONG.")
                        self.place_order(symbol, 'SELL', current_price, position['quantity'])
                        del self.positions[symbol]
                
                elif position['type'] == 'SHORT':
                    if current_price >= position['stop_loss']:
                        logger.warning(f"Stop loss hit for {symbol}. Exiting SHORT.")
                        self.place_order(symbol, 'BUY', current_price, position['quantity'])
                        del self.positions[symbol]
                    
                    elif current_price <= position['take_profit']:
                        logger.info(f"Take profit hit for {symbol}. Exiting SHORT.")
                        self.place_order(symbol, 'BUY', current_price, position['quantity'])
                        del self.positions[symbol]
            
            except Exception as e:
                logger.error(f"Error monitoring position for {symbol}: {e}")
    
    def close_all_positions(self):
        """Close all open positions at market close"""
        for symbol in list(self.positions.keys()):
            try:
                data = self.get_instrument_data(symbol)
                position = self.positions[symbol]
                
                if position['type'] == 'LONG':
                    self.place_order(symbol, 'SELL', data['ltp'], position['quantity'])
                else:
                    self.place_order(symbol, 'BUY', data['ltp'], position['quantity'])
                
                del self.positions[symbol]
                logger.info(f"Closed position in {symbol}")
            
            except Exception as e:
                logger.error(f"Error closing position for {symbol}: {e}")
    
    def start_trading(self, symbols: List[str]):
        """
        Start automated trading
        Args:
            symbols: List of stock symbols to monitor (e.g., ['INFY', 'TCS', 'RELIANCE'])
        """
        logger.info(f"Starting trading bot for symbols: {symbols}")
        
        # Schedule trading job during market hours
        for symbol in symbols:
            # Check circuit every 2 minutes
            schedule.every(2).minutes.do(self.execute_circuit_trade, symbol=symbol)
        
        # Monitor positions every minute
        schedule.every(1).minutes.do(self.monitor_positions)
        
        # Close all positions at market close
        schedule.every().day.at("15:30").do(self.close_all_positions)
        
        # Keep scheduler running
        while True:
            schedule.run_pending()
            time_module.sleep(1)
    
    def get_order_history(self) -> List:
        """Return all executed orders"""
        return self.order_log
    
    def get_portfolio_summary(self) -> Dict:
        """Get summary of current positions"""
        return {
            'total_positions': len(self.positions),
            'positions': self.positions,
            'total_trades': len(self.order_log)
        }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def main():
    """
    Main function to run the trading bot
    """
    # Replace with your credentials
    API_KEY = "your_kite_api_key"
    ACCESS_TOKEN = "your_kite_access_token"
    
    # Initialize trader
    trader = CircuitTrader(api_key=API_KEY, access_token=ACCESS_TOKEN)
    
    # List of stocks to monitor (NSE symbols)
    stocks_to_monitor = [
        'INFY',      # Infosys
        'TCS',       # TCS
        'RELIANCE',  # Reliance
        'HDFC',      # HDFC Bank
        'BAJAJFINSV' # Bajaj Finance
    ]
    
    try:
        # Start trading
        trader.start_trading(symbols=stocks_to_monitor)
    
    except KeyboardInterrupt:
        logger.info("Trading bot stopped by user")
        # Close all positions before exit
        trader.close_all_positions()
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        trader.close_all_positions()


if __name__ == "__main__":
    main()
