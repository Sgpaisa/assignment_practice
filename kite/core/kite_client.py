"""
Kite API Client Wrapper
Handles all communication with Zerodha Kite API
"""

import logging
from kiteconnect import KiteConnect

logger = logging.getLogger(__name__)


class KiteClient:
    """Wrapper around KiteConnect for easier use"""
    
    def __init__(self, api_key: str, access_token: str):
        """
        Initialize Kite client
        
        Args:
            api_key: Your Kite API key
            access_token: Your access token from login
        """
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)
        self.api_key = api_key
        self.access_token = access_token
        logger.info("KiteClient initialized successfully")
    
    def get_quote(self, symbol: str):
        """Get stock quote (LTP and previous close)"""
        try:
            # Format symbol for Kite API
            formatted_symbol = f"{symbol}:NSE" if ":NSE" not in symbol else symbol
            
            data = self.kite.quote([formatted_symbol])
            if 'data' in data and formatted_symbol in data['data']:
                return data['data'][formatted_symbol]
            else:
                logger.warning(f"No quote data found for {symbol}")
                return None
        except Exception as e:
            logger.error(f"Error getting quote for {symbol}: {e}")
            return None
    
    def get_quote_multiple(self, symbols: list):
        """Get quotes for multiple stocks"""
        try:
            # Format all symbols for Kite API
            formatted_symbols = [f"{s}:NSE" if ":NSE" not in s else s for s in symbols]
            
            data = self.kite.quote(formatted_symbols)
            return data.get('data', {})
        except Exception as e:
            logger.error(f"Error getting quotes: {e}")
            return {}
    
    def place_order(self, symbol: str, quantity: int, side: str, price: float = None, order_type: str = "MARKET"):
        """
        Place an order
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            side: BUY or SELL
            price: Order price (for limit orders)
            order_type: MARKET, LIMIT
            
        Returns:
            Order ID if successful, None otherwise
        """
        try:
            # Format symbol for Kite API
            formatted_symbol = f"{symbol}:NSE" if ":NSE" not in symbol else symbol
            
            order_id = self.kite.place_order(
                tradingsymbol=formatted_symbol,
                exchange="NSE",
                quantity=quantity,
                side=side,
                order_type=order_type,
                price=price if price else None,
                product="MIS"  # Margin Intraday Square-off
            )
            logger.info(f"Order placed: {side} {quantity} {symbol} - Order ID: {order_id}")
            return order_id
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
    
    def get_positions(self):
        """Get all open positions"""
        try:
            positions = self.kite.positions()
            return positions.get('net', [])
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return []
    
    def get_orders(self):
        """Get all orders"""
        try:
            return self.kite.orders()
        except Exception as e:
            logger.error(f"Error getting orders: {e}")
            return []
    
    def cancel_order(self, order_id: str):
        """Cancel an order"""
        try:
            self.kite.cancel_order(order_id=order_id, variety="regular")
            logger.info(f"Order cancelled: {order_id}")
            return True
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return False
    
    def get_holdings(self):
        """Get all holdings (stocks you own)"""
        try:
            return self.kite.holdings()
        except Exception as e:
            logger.error(f"Error getting holdings: {e}")
            return []
    
    def is_connected(self):
        """Check if connection is active"""
        try:
            # Try to get a simple quote to verify connection
            self.get_quote("HDFCBANK")
            return True
        except Exception:
            return False
