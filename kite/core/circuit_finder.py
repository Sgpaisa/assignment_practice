"""
Circuit Breaker Finder
Auto-detect stocks that have hit circuit breaker levels
"""

import logging
from typing import List, Dict
from config.settings import TradingConfig
from config.nse200_stocks import get_all_stocks

logger = logging.getLogger(__name__)


class CircuitFinder:
    """Find stocks that have hit circuit breaker levels"""
    
    def __init__(self, kite_client, circuit_percent: float = 20):
        """
        Initialize circuit finder
        
        Args:
            kite_client: KiteClient instance
            circuit_percent: Circuit level percentage (e.g., 20 for 20%)
        """
        self.kite_client = kite_client
        self.circuit_percent = circuit_percent
        self.circuit_stocks = []
    
    def find_circuit_stocks(self, stocks_list: List[str] = None) -> Dict[str, Dict]:
        """
        Find all stocks in given list that have hit circuit breaker
        
        Args:
            stocks_list: List of stock symbols to check (default: NSE 200)
            
        Returns:
            Dict of stocks with their circuit info
        """
        if stocks_list is None:
            stocks_list = list(get_all_stocks().keys())
        
        logger.info(f"Scanning {len(stocks_list)} stocks for {self.circuit_percent}% circuit...")
        
        circuit_stocks = {}
        
        try:
            # Format symbols for Kite API
            formatted_symbols = [f"{s}:NSE" for s in stocks_list]
            
            # Get quotes for all stocks
            quotes = self.kite_client.get_quote_multiple(formatted_symbols)
            
            for idx, symbol in enumerate(stocks_list):
                formatted_sym = formatted_symbols[idx]
                
                if formatted_sym not in quotes:
                    continue
                
                quote = quotes[formatted_sym]
                if not quote:
                    continue
                
                # Calculate percentage change
                ltp = quote.get('last_price', 0)
                previous_close = quote.get('ohlc', {}).get('close', ltp)
                
                if previous_close > 0:
                    change_percent = ((ltp - previous_close) / previous_close) * 100
                    
                    # Check if stock hit upper or lower circuit
                    if abs(change_percent) >= self.circuit_percent:
                        circuit_stocks[symbol] = {
                            'symbol': symbol,
                            'ltp': ltp,
                            'previous_close': previous_close,
                            'change_percent': change_percent,
                            'is_upper_circuit': change_percent >= self.circuit_percent,
                            'is_lower_circuit': change_percent <= -self.circuit_percent,
                        }
                        
                        action = "UPPER" if change_percent >= self.circuit_percent else "LOWER"
                        logger.info(f"✓ {symbol}: {action} CIRCUIT ({change_percent:+.2f}%)")
        
        except Exception as e:
            logger.error(f"Error scanning for circuit stocks: {e}")
            import traceback
            traceback.print_exc()
        
        self.circuit_stocks = circuit_stocks
        return circuit_stocks
    
    def get_circuit_stocks_to_buy(self) -> Dict[str, Dict]:
        """Get stocks that hit lower circuit (buy signals)"""
        return {
            symbol: data for symbol, data in self.circuit_stocks.items()
            if data['is_lower_circuit']
        }
    
    def get_circuit_stocks_to_sell(self) -> Dict[str, Dict]:
        """Get stocks that hit upper circuit (sell signals)"""
        return {
            symbol: data for symbol, data in self.circuit_stocks.items()
            if data['is_upper_circuit']
        }
    
    def print_circuit_summary(self):
        """Print summary of found circuit stocks"""
        if not self.circuit_stocks:
            print("No circuit breaker stocks found.")
            return
        
        print("\n" + "="*70)
        print(f"CIRCUIT BREAKER STOCKS ({self.circuit_percent}%)")
        print("="*70)
        
        buy_signals = self.get_circuit_stocks_to_buy()
        sell_signals = self.get_circuit_stocks_to_sell()
        
        if buy_signals:
            print("\n📉 LOWER CIRCUIT (BUY SIGNAL):")
            for symbol, data in buy_signals.items():
                print(f"  {symbol}: {data['change_percent']:+.2f}% (LTP: {data['ltp']})")
        
        if sell_signals:
            print("\n📈 UPPER CIRCUIT (SELL SIGNAL):")
            for symbol, data in sell_signals.items():
                print(f"  {symbol}: {data['change_percent']:+.2f}% (LTP: {data['ltp']})")
        
        print("="*70 + "\n")
