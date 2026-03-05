# Zerodha Kite Circuit Breaker Trading Bot - Setup Guide

## Overview
This trading bot automatically places BUY/SELL orders when stocks hit upper or lower circuit breakers within the first 3 hours of trading (9:15 AM - 12:15 PM IST).

---

## Installation & Setup

### 1. Install Required Libraries
```bash
pip install kiteconnect schedule
```

### 2. Get Kite API Credentials

#### Step 1: Create API App
- Go to https://developers.kite.trade/
- Sign in with your Zerodha account
- Click "Create App"
- Fill in app details:
  - **App Name**: Any name (e.g., "CircuitTrader")
  - **Redirect URL**: http://localhost:8080/ (or your preferred URL)
  - **Required Scopes**: Select "full_access"

#### Step 2: Get API Key
- Your **API Key** will be displayed on the app page

#### Step 3: Generate Access Token
```python
from kiteconnect import KiteConnect

kite = KiteConnect(api_key="YOUR_API_KEY")
# Open this URL in browser and login
print(kite.login_url())
```

- After login, you'll be redirected with a code like: `code=XXXXX`
- Use this code to get access token:

```python
data = kite.request_access_token(code="code_from_redirect", secret="YOUR_APP_SECRET")
access_token = data['access_token']
```

---

## Configuration

Edit the `zerodha_circuit_trader.py` file:

### Basic Settings
```python
# Your Kite credentials
API_KEY = "your_kite_api_key"
ACCESS_TOKEN = "your_kite_access_token"

# Stocks to monitor (NSE symbols)
stocks_to_monitor = [
    'INFY',      # Infosys
    'TCS',       # TCS
    'RELIANCE',  # Reliance
    'HDFC',      # HDFC Bank
    'BAJAJFINSV' # Bajaj Finance
]
```

### Trading Parameters
```python
self.upper_circuit = 20          # Upper circuit %
self.lower_circuit = 20          # Lower circuit %
self.quantity_per_trade = 1      # Shares per trade
self.stop_loss_percent = 2       # SL in %
self.take_profit_percent = 5     # TP in %
```

### Trading Window
- **Start**: 9:15 AM IST (Market Open)
- **End**: 12:15 PM IST (First 3 hours)
- **Weekdays Only**: Monday to Friday

---

## How It Works

### Trading Logic

1. **Upper Circuit Hit** (20% gain)
   - Stock is overvalued
   - Action: **SELL** (Short position)
   - Stop Loss: +2% (exit if price goes up more)
   - Take Profit: -5% (exit when it drops 5%)

2. **Lower Circuit Hit** (20% loss)
   - Stock is undervalued
   - Action: **BUY** (Long position)
   - Stop Loss: -2% (exit if price drops more)
   - Take Profit: +5% (exit when it rises 5%)

### Monitoring
- Checks for circuit levels every 2 minutes
- Monitors positions every 1 minute
- Closes all positions at market close (3:30 PM)

---

## Running the Bot

### Method 1: Direct Execution
```bash
python zerodha_circuit_trader.py
```

### Method 2: Background Execution (Windows)
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python zerodha_circuit_trader.py"
```

### Method 3: Task Scheduler (Windows)
1. Create batch file `run_trader.bat`:
```batch
@echo off
cd D:\visual studio\Module and packages\kite
python zerodha_circuit_trader.py
pause
```

2. Schedule in Task Scheduler:
   - Time Trigger: 9:00 AM IST (daily)
   - Action: Run `run_trader.bat`

---

## Logging & Monitoring

All activities are logged in `circuit_trader.log`:

```
2024-01-15 09:16:23,456 - INFO - CircuitTrader initialized
2024-01-15 09:20:45,789 - WARNING - INFY hit UPPER CIRCUIT. LTP: 1650.50
2024-01-15 09:21:12,345 - INFO - Order placed: {'order_id': '123456', ...}
```

### Key Metrics
```python
trader = CircuitTrader(API_KEY, ACCESS_TOKEN)

# Get order history
orders = trader.get_order_history()

# Get portfolio summary
summary = trader.get_portfolio_summary()
```

---

## Risk Management

### 1. Position Size
Adjust quantity to manage risk:
```python
trader.quantity_per_trade = 1  # Start small
```

### 2. Stop Loss & Take Profit
```python
trader.stop_loss_percent = 2      # 2% SL
trader.take_profit_percent = 5    # 5% TP
```

### 3. Capital Requirements
- Zerodha MIS (Intraday): 4x margin
- Margin for 1 share: Depends on stock price
- Recommendation: Start with 1-5 shares per trade

### 4. Maximum Losses Per Day
Consider setting a maximum daily loss:
```python
max_daily_loss = 50  # Stop trading after losing Rs. 50
total_loss = sum([pos['loss'] for pos in self.positions])
```

---

## Common Issues & Solutions

### Issue 1: "Access Denied" Error
**Solution**: Recheck API Key and Access Token

### Issue 2: "Insufficient Funds" Error
**Solution**: Ensure sufficient margin in account (4x for MIS)

### Issue 3: "Order Rejected" Error
**Solution**: 
- Check market hours (9:15 AM - 3:30 PM IST)
- Verify symbol names (use NSE symbols)
- Check circuit breaker levels haven't triggered a halt

### Issue 4: Bot Not Starting
**Solution**:
- Verify Python installation: `python --version`
- Install dependencies: `pip install kiteconnect schedule`
- Check file permissions and path

---

## Important Notes ⚠️

1. **Live Trading**: This code executes REAL trades with REAL money. Test thoroughly first.

2. **Market Risk**: Circuit breakers indicate extreme volatility. Losses can exceed expectations.

3. **Slippage**: Actual execution price may differ from LTP due to order queue.

4. **Weekend/Holidays**: Bot skips non-trading days automatically.

5. **Connection Loss**: Bot crashes if internet disconnects. Add reconnection logic for production.

6. **Tax Implications**: Keep records for capital gains tax (intraday trades are short-term).

---

## Advanced Features (Optional)

### Add Email Alerts
```python
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    # Send via SMTP
```

### Add WebSocket for Real-time Ticks
```python
from kiteconnect import WebSocket

def on_ticks(ws, ticks):
    for tick in ticks:
        # Process in real-time
        pass

kws = WebSocket(api_key, access_token=access_token)
kws.on_ticks = on_ticks
kws.connect()
```

### Database Logging
```python
import sqlite3
conn = sqlite3.connect('trades.db')
# Log all trades to database
```

---

## Support Resources

- **Kite API Docs**: https://kite.trade/docs/connect/v3/
- **Zerodha Support**: https://support.zerodha.com/
- **Python Kiteconnect**: https://github.com/zerodhatech/pykiteconnect

---

## Disclaimer

⚠️ **IMPORTANT**: This bot is provided as-is for educational purposes. 

- Trading involves substantial risk of loss
- Circuit breaker trades are highly volatile
- Always test with small quantities first
- Keep manual override ability
- Monitor bot activity regularly
- Consult a financial advisor before deploying

---

## Version History

- **v1.0** (2024): Initial release
  - Circuit breaker detection
  - Auto buy/sell on circuit hits
  - Position monitoring with SL/TP
  - Logging and order tracking
