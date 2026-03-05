# Configuration Templates for Circuit Trading Bot

## Template 1: Conservative Trading (Low Risk)
```python
# For beginners - very safe
UPPER_CIRCUIT_THRESHOLD = 20
LOWER_CIRCUIT_THRESHOLD = 20
QUANTITY_PER_TRADE = 1
STOP_LOSS_PERCENT = 1.5  # Very tight SL
TAKE_PROFIT_PERCENT = 3  # Conservative TP
MAX_DAILY_LOSS = 100
MAX_POSITIONS = 2
```

## Template 2: Moderate Trading (Medium Risk)
```python
# For experienced traders
UPPER_CIRCUIT_THRESHOLD = 20
LOWER_CIRCUIT_THRESHOLD = 20
QUANTITY_PER_TRADE = 2
STOP_LOSS_PERCENT = 2
TAKE_PROFIT_PERCENT = 5
MAX_DAILY_LOSS = 500
MAX_POSITIONS = 5
```

## Template 3: Aggressive Trading (High Risk)
```python
# For risk takers - use with caution!
UPPER_CIRCUIT_THRESHOLD = 20
LOWER_CIRCUIT_THRESHOLD = 20
QUANTITY_PER_TRADE = 5
STOP_LOSS_PERCENT = 3
TAKE_PROFIT_PERCENT = 8
MAX_DAILY_LOSS = 1000
MAX_POSITIONS = 10
```

## Template 4: Day Trade Scalper (Very Active)
```python
# For active traders - trades multiple times
UPPER_CIRCUIT_THRESHOLD = 15  # Lower threshold
LOWER_CIRCUIT_THRESHOLD = 15
QUANTITY_PER_TRADE = 1
STOP_LOSS_PERCENT = 0.5  # Scalper SL
TAKE_PROFIT_PERCENT = 1.5  # Quick profits
REENTRY_ENABLED = True
MAX_REENTRIES = 3
```

---

## Stock Selection by Risk Profile

### High Probability Stocks (Liquid, Volatile)
- INFY (Infosys) - Tech sensitive
- TCS (Tata Consultancy) - Volatile
- RELIANCE - High volume
- HDFC Bank - Banking sector
- BAJAJFINSV - Finance sector

### Medium Probability Stocks
- WIPRO
- LT
- MARUTI
- HDFCBANK
- ICICIBANK

### Lower Probability (Less Volatile)
- SBIN
- PNB
- SUNPHARMA
- ASIANPAINT
- BPCL

---

## Position Sizing Based on Capital

### For Rs. 50,000 Capital
```python
QUANTITY_PER_TRADE = 1
MAX_DAILY_LOSS = 50  # 0.1% risk
RISK_PER_TRADE = 10  # Rs. 10 loss limit
```

### For Rs. 1,00,000 Capital
```python
QUANTITY_PER_TRADE = 2
MAX_DAILY_LOSS = 100  # 0.1% risk
RISK_PER_TRADE = 20  # Rs. 20 loss limit
```

### For Rs. 5,00,000 Capital
```python
QUANTITY_PER_TRADE = 5
MAX_DAILY_LOSS = 500  # 0.1% risk
RISK_PER_TRADE = 100  # Rs. 100 loss limit
```

---

## .env File Template

```bash
# .env
KITE_API_KEY=your_api_key_here
KITE_ACCESS_TOKEN=your_access_token_here
KITE_APP_SECRET=your_app_secret
ZERODHA_USER_ID=your_zerodha_userid
LOG_LEVEL=INFO
LOG_FILE=circuit_trades.log
TELEGRAM_BOT_TOKEN=optional_for_alerts
TELEGRAM_CHAT_ID=optional_for_alerts
```

---

## Performance Tracking Template

Track your trading performance with this structure:

```python
PERFORMANCE_METRICS = {
    'total_trades': 0,
    'winning_trades': 0,
    'losing_trades': 0,
    'win_rate': 0,
    'total_profit': 0,
    'total_loss': 0,
    'net_profit': 0,
    'best_trade': 0,
    'worst_trade': 0,
    'avg_profit_per_trade': 0,
    'risk_reward_ratio': 0,
    'profit_factor': 0,  # gross_profit / gross_loss
}
```

---

## Market Hours Configuration

### Indian Stock Market (NSE/BSE)
```python
MARKET_OPEN = time(9, 15)      # 9:15 AM IST
TRADING_WINDOW_END = time(12, 15)  # 12:15 PM (first 3 hours)
MARKET_CLOSE = time(15, 30)    # 3:30 PM IST
EXTENDED_CLOSE = time(16, 0)   # 4:00 PM (extended margin)
HOLIDAYS = [
    # Add market holidays
    "2024-01-26",  # Republic Day
    "2024-03-25",  # Holi
    "2024-08-15",  # Independence Day
]
```

---

## Order Configuration

```python
ORDER_CONFIG = {
    'product': 'MIS',  # Intraday
    'variety': 'REGULAR',
    'order_type': 'LIMIT',
    'exchange': 'NSE',
    'validity': 'DAY',
    'price_offset': 0.5,  # Place order 0.5 away from LTP
    'Order_timetout': 60,  # Seconds
}
```

---

## Risk Management Rules

```python
RISK_MANAGEMENT = {
    'max_positions': 5,
    'max_loss_per_day': 500,
    'max_loss_per_trade': 50,
    'max_trades_per_day': 20,
    'min_profit_to_continue': 100,
    'stop_trading_at_loss': -500,
    'take_profit_at_gain': 1000,
}
```

---

## Notification Configuration (Optional)

```python
NOTIFICATIONS = {
    'email_enabled': False,
    'email_address': 'your_email@gmail.com',
    'telegram_enabled': False,
    'telegram_token': 'your_bot_token',
    'telegram_chat_id': 'your_chat_id',
    'sms_enabled': False,
    'sms_phone': '+91xxxxxxxxxx',
}
```

---

## Advanced Features Configuration

```python
ADVANCED_CONFIG = {
    'use_websocket': True,  # Real-time data
    'database_logging': True,
    'email_summary': True,
    'daily_summary_time': time(16, 0),  # After market close
    'auto_reentry': False,
    'pyramid_trading': False,
    'trailing_sl': False,
}
```

---

## Testing & Backtesting Template

```python
BACKTEST_CONFIG = {
    'start_date': '2024-01-01',
    'end_date': '2024-03-31',
    'initial_capital': 100000,
    'commission': 20,  # Rs. per trade
    'slippage': 1,  # 1 rupee
    'date_range': 'last_3_months',
}
```

---

## How to Use These Templates:

1. **Choose your risk profile** (Conservative/Moderate/Aggressive)
2. **Copy the corresponding template**
3. **Edit `zerodha_circuit_trader.py`** and update parameters
4. **Test with small quantities** first
5. **Monitor for 1-2 weeks** before scaling up
6. **Adjust based on results**

---

## Recommended Starting Point:

```python
# For beginners - SAFEST approach
STOCKS = ['INFY']  # Start with 1 stock
QUANTITY_PER_TRADE = 1
STOP_LOSS_PERCENT = 1.5
TAKE_PROFIT_PERCENT = 3
MAX_DAILY_LOSS = 100

# After 10+ profitable trades, increase to:
STOCKS = ['INFY', 'TCS']  # Add 2nd stock
QUANTITY_PER_TRADE = 1
STOP_LOSS_PERCENT = 2
TAKE_PROFIT_PERCENT = 5
MAX_DAILY_LOSS = 200

# After 30+ profitable trades:
STOCKS = ['INFY', 'TCS', 'RELIANCE']  # Add 3rd stock
QUANTITY_PER_TRADE = 2
# ... and so on
```

---

## Daily Checklist Before Running Bot:

- [ ] Check internet connection is stable
- [ ] Verify API credentials in .env
- [ ] Check market is open (weekday, 9:15-15:30)
- [ ] Verify sufficient margin in account
- [ ] Review yesterday's trades in log
- [ ] Check for holidays in market calendar
- [ ] Monitor first 30 minutes manually
- [ ] Set alerts for large losses
- [ ] Plan to close all positions at 3:25 PM

---

## Troubleshooting Guide:

| Problem | Solution |
|---------|----------|
| "Access Denied" | Regenerate access token |
| "Insufficient Margin" | Add funds to account |
| "Order Rejected" | Check stock name and circuit limits |
| "Connection Lost" | Reconnect internet, restart bot |
| "No trades executing" | Check if within trading window |
| "High slippage" | Use market orders or wait for better price |
| "Bot crashes" | Check logs and increase error handling |

