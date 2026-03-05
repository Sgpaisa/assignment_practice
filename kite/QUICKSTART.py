"""
QUICK START GUIDE - Zerodha Kite Circuit Trading Bot
Complete setup in 10 minutes
"""

# ============================================================================
# STEP 1: INSTALL DEPENDENCIES (Copy-Paste in PowerShell)
# ============================================================================
# 
# 
# 
# pip install kiteconnect schedule python-dotenv

# ============================================================================
# STEP 2: CREATE .env FILE with your credentials
# ============================================================================

# Create a file named .env in the same directory:
"""
KITE_API_KEY=your_api_key_here
KITE_ACCESS_TOKEN=your_access_token_here
"""

# ============================================================================
# STEP 3: GET YOUR API CREDENTIALS
# ============================================================================

# 1. Go to: https://developers.kite.trade/
# 2. Sign in with Zerodha account
# 3. Click "Create App"
# 4. Enter details:
#    - App Name: CircuitTrader
#    - Redirect URL: http://localhost:8080/
#    - Scopes: full_access
# 5. Copy API Key to .env file
# 
# 6. To get Access Token, run this Python code:
# from kiteconnect import KiteConnect
# api_key = "YOUR_API_KEY"
# kite = KiteConnect(api_key=api_key)
# print(kite.login_url())

# ============================================================================
# STEP 4: RUN THE BOT
# ============================================================================

import os
import logging
import schedule
import time
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from datetime import datetime, time as dt_time

# Load credentials from .env
load_dotenv()
API_KEY = os.getenv('KITE_API_KEY')
ACCESS_TOKEN = os.getenv('KITE_ACCESS_TOKEN')

if not API_KEY or not ACCESS_TOKEN:
    print("[ERROR] Set KITE_API_KEY and KITE_ACCESS_TOKEN in .env file")
    exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('circuit_trades.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CircuitBot:
    def __init__(self):
        self.kite = KiteConnect(api_key=API_KEY)
        self.kite.set_access_token(ACCESS_TOKEN)
        self.trading_active = True
        self.positions = {}
        logger.info("[OK] Connected to Zerodha Kite API")
    
    def is_trading_time(self):
        """Check if within 9:15 AM - 12:15 PM IST"""
        now = datetime.now().time()
        return (dt_time(9, 15) <= now <= dt_time(14, 15)) and datetime.now().weekday() < 5
    
    def check_circuit(self, symbol):
        """Check if stock hit circuit breaker"""
        try:
            data = self.kite.quote(symbols=[symbol])['data'][symbol]
            ltp = data['last_price']
            prev_close = data['ohlc']['close']
            
            # Calculate circuit levels (20%)
            upper = prev_close * 1.20
            lower = prev_close * 0.80
            
            change = ((ltp - prev_close) / prev_close) * 100
            
            return {
                'ltp': ltp,
                'prev_close': prev_close,
                'upper': upper,
                'lower': lower,
                'change': change,
                'upper_circuit': ltp >= upper * 0.98,
                'lower_circuit': ltp <= lower * 1.02
            }
        except Exception as e:
            logger.error(f"Error checking {symbol}: {e}")
            return None
    
    def place_order(self, symbol, buy_sell, price):
        """Place buy/sell order"""
        try:
            order_id = self.kite.place_order(
                variety='regular',
                exchange='NSE',
                tradingsymbol=symbol,
                transaction_type=buy_sell,
                quantity=1,
                price=int(price),
                order_type='limit',
                product='MIS'
            )
            
            logger.info(f"[OK] {buy_sell} {symbol} at Rs. {price:.2f} | Order ID: {order_id}")
            
            self.positions[symbol] = {
                'type': buy_sell,
                'entry': price,
                'order_id': order_id
            }
            
            return order_id
        
        except Exception as e:
            logger.error(f"[FAIL] Order failed for {symbol}: {e}")
            return None
    
    def run(self, symbols):
        """Main trading loop"""
        logger.info(f"Starting bot for: {symbols}")
        
        def check_all():
            if not self.is_trading_time():
                return
            
            for symbol in symbols:
                data = self.check_circuit(symbol)
                if not data:
                    continue
                
                if data['lower_circuit']:
                    logger.warning(f"[BUY SIGNAL] {symbol} hit LOWER CIRCUIT! Buying...")
                    self.place_order(symbol, 'BUY', data['ltp'])
                
                elif data['upper_circuit']:
                    logger.warning(f"[SELL SIGNAL] {symbol} hit UPPER CIRCUIT! Selling...")
                    self.place_order(symbol, 'SELL', data['ltp'])
        
        # Check every 2 minutes
        schedule.every(2).minutes.do(check_all)
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(1)

# ============================================================================
# STEP 5: RUN IT!
# ============================================================================

if __name__ == "__main__":
    bot = CircuitBot()
    
    # Stocks to monitor
    STOCKS = ['INFY', 'TCS', 'RELIANCE', 'HDFC', 'BAJAJFINSV']
    
    try:
        bot.run(STOCKS)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

# ============================================================================
# STEP 6: RUN THE BOT (In PowerShell)
# ============================================================================

# cd D:\visual studio\Module and packages\kite
# python main.py

# ============================================================================
# MONITORING & LOGS
# ============================================================================

# Watch logs real-time:
# Get-Content circuit_trades.log -Wait

# ============================================================================
# TIPS FOR SUCCESS
# ============================================================================

# 1. Start SMALL - Use 1 share per trade
# 2. Monitor GainLoss - Check circuit_trades.log daily
# 3. Scale UP - After profitable 10-15 trades
# 4. Adjust SL/TP - If losing too much
# 5. Holiday SKIP - Don't run on market holidays
# 6. Internet RELIABLE - Use stable connection
# 7. Code CAREFUL - Never lose credentials

# ============================================================================
# SUPPORT & HELP
# ============================================================================

# API Issues: https://support.zerodha.com/
# Kite Docs: https://kite.trade/docs/connect/v3/
# Order Status: Check in Zerodha Kite web/app

print("""
[OK] Circuit Trading Bot - Quick Start Complete!

Next Steps:
1. Create .env file with API credentials
2. Run: python main.py
3. Monitor trades in terminal
4. Check circuit_trades.log for details

Good luck with trading!
""")
