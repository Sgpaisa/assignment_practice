# Kite Trading Bot - Complete Setup & Usage Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start-5-minutes)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Using the Bot](#using-the-bot)
5. [Troubleshooting](#troubleshooting)
6. [Understanding Circuit Breakers](#understanding-circuit-breakers)

---

## 🚀 Quick Start (5 Minutes)

### For Complete Beginners:
```bash
python simple_setup.py
```
Just follow the prompts! This is the easiest way to get started.

### For Advanced Users:
```bash
python main.py
```
More control over settings and multiple trading options.

---

## 💾 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**If requirements.txt doesn't exist, install these packages:**
```bash
pip install kiteconnect python-dotenv
```

### 2. Set Up Credentials (.env file)

Create a `.env` file in the kite folder:

```env
KITE_API_KEY=your_api_key_here
KITE_ACCESS_TOKEN=your_access_token_here
```

**How to get API Key:**
1. Go to https://zerodha.com/developers/
2. Register / Login
3. Click "Create API Application"
4. Copy your API Key

**How to get Access Token:**
1. Go to https://kite.zerodha.com/connect/
2. Login with your Zerodha account
3. You'll be redirected with token in URL
4. Copy and paste the token

---

## ⚙️ Configuration

### Easy Way: Edit `config/settings.py`

```python
# STOCK SELECTION
STOCK_TO_TRADE = "HDFCBANK"  # Change this!

# CIRCUIT LEVEL (KEY SETTING)
UPPER_CIRCUIT_PERCENT = 20    # Stock up 20% → SELL signal
LOWER_CIRCUIT_PERCENT = 20    # Stock down 20% → BUY signal

# QUANTITY
QUANTITY_PER_TRADE = 1        # How many shares to buy/sell

# STOP LOSS & TAKE PROFIT
STOP_LOSS_PERCENT = 2         # Exit if down 2%
TAKE_PROFIT_PERCENT = 5       # Exit if up 5%

# TEST MODE
TEST_MODE = False             # True to simulate, False to trade real
```

### Preset Configurations

#### Conservative (Low Risk)
```python
from config.settings import ConservativeConfig
# Uses: 10% circuit, 1 share, 1% stop loss
```

#### Moderate (Medium Risk)
```python
from config.settings import ModerateConfig
# Uses: 15% circuit, 2 shares, 2% stop loss
```

#### Aggressive (High Risk)
```python
from config.settings import AggressiveConfig
# Uses: 20% circuit, 5 shares, 3% stop loss
```

---

## 🎯 Using the Bot

### Option 1: Single Stock Trading

```bash
python main.py
# Select option 1
# Enter: HDFCBANK
# Enter: 20 (for 20% circuit)
# Enter: 1 (for 1 share)
```

The bot will:
- Monitor HDFCBANK every 5 seconds
- Show price and percentage change
- **BUY when stock drops 20%** (lower circuit hit)
- **SELL when stock rises 20%** (upper circuit hit)

### Option 2: Multiple Stocks

```bash
python main.py
# Select option 2
# Enter: HDFCBANK,INFY,TCS (comma-separated)
# Configure circuit %, quantity, etc.
```

Monitor multiple stocks and trade all that hit circuit levels.

### Option 3: Auto-Detect from NSE 200

```bash
python main.py
# Select option 3
```

The bot will:
- Scan all 200 NSE stocks automatically
- Find stocks hitting circuit breaker
- Trade them automatically

### Option 4: Quick Setup (Easiest)

```bash
python simple_setup.py
```

Interactive step-by-step guide!

---

## 📊 Understanding Circuit Breakers

### What is a Circuit Breaker?

A **circuit breaker** is a trading halt triggered when a stock price moves too much (in either direction).

Example:
- A stock at ₹100 with 20% circuit breaker
- **Upper Circuit**: ₹120 (up 20%)
- **Lower Circuit**: ₹80 (down 20%)

### Trading Strategy

```
Stock Price Falls 20%
    ↓
LOWER CIRCUIT HIT
    ↓
BOT PLACES BUY ORDER
    ↓
Expected: Stock bounces back up
    ↓
PROFIT!

---

Stock Price Rises 20%
    ↓
UPPER CIRCUIT HIT
    ↓
BOT PLACES SELL ORDER
    ↓
Expected: Stock comes down / takes profit
    ↓
PROFIT!
```

### Changing the Percentage

The **percentage is the KEY setting**. Change it like this:

```python
# In config/settings.py
UPPER_CIRCUIT_PERCENT = 10    # More aggressive (trade at 10% instead of 20%)
LOWER_CIRCUIT_PERCENT = 10
```

Or at runtime:
```bash
python main.py
# When prompted: Enter 10
```

---

## 📂 Folder Structure (Fully Modular)

```
kite/
├── main.py                    ← START HERE (advanced)
├── simple_setup.py            ← START HERE (beginners)
├── .env                       ← Your credentials
├── requirements.txt           ← Dependencies
│
├── config/
│   ├── settings.py           ← All configuration (EDIT THIS!)
│   └── nse200_stocks.py      ← List of all NSE 200 stocks
│
├── core/
│   ├── kite_client.py        ← Zerodha API connection
│   ├── circuit_finder.py     ← Find circuit stocks
│   └── trader.py             ← Trading logic
│
├── strategies/
│   └── circuit_breaker_strategy.py  ← Main trading strategy
│
├── authenticators/
│   └── token_manager.py      ← Handle authentication
│
├── utils/
│   ├── logger.py             ← Logging
│   └── helpers.py            ← Helper functions
│
└── docs/
    └── README.md             ← This file!
```

---

## 🔧 Common Tasks

### Change Circuit Percentage

1. Edit `config/settings.py`:
```python
UPPER_CIRCUIT_PERCENT = 15    # Changed from 20 to 15
LOWER_CIRCUIT_PERCENT = 15
```

2. Or at runtime when prompted.

### Change Quantity Per Trade

Edit `config/settings.py`:
```python
QUANTITY_PER_TRADE = 5    # Trade 5 shares instead of 1
```

### Stop Loss & Take Profit

Edit `config/settings.py`:
```python
STOP_LOSS_PERCENT = 3        # Exit if down 3%
TAKE_PROFIT_PERCENT = 10     # Exit if up 10%
```

### Test Before Trading Real Money

```python
# In config/settings.py
TEST_MODE = True   # Simulate without real trades
```

Or select "Test mode" when prompted.

### View All NSE 200 Stocks

```bash
python main.py
# Select option 4
```

---

## 🎓 Example Walkthroughs

### Example 1: Trade HDFCBANK at 20% Circuit

```bash
$ python simple_setup.py

⚡ QUICK START - CIRCUIT BREAKER TRADING BOT SETUP
================================================================

This wizard will help you set up your trading bot in 3 steps:

STEP 1: ZERODHA CREDENTIALS
-------------------------------------------------
✓ Credentials found in .env file!

STEP 2: TRADING CONFIGURATION
-------------------------------------------------
Which stock do you want to trade?
Stock symbol: HDFCBANK
✓ Stock: HDFCBANK

At what percentage should we trigger trade?
Circuit percentage (default 20): 20
✓ Circuit level: 20%

How many quantity per trade?
Quantity (default 1): 1
✓ Quantity per trade: 1

Do you want to test (simulate) before trading real money?
Test mode? (Y/N): y
✓ Test Mode: True

STEP 3: READY TO START!
--------------------------------------------------
============================================================
CURRENT TRADING CONFIGURATION
============================================================
Stock to Trade: HDFCBANK
Circuit Breaker: 20%
Quantity per Trade: 1
Stop Loss: 2%
Take Profit: 5%
Trading Hours: 9:15 - 12:15
Test Mode: True
============================================================

Start trading with these settings? (Y/N): y

✓ Connected to Kite API!
✓ Starting to monitor HDFCBANK...

[09:15:23] HDFCBANK: LTP ₹1250.50 | Change: +0.15%
[09:16:23] HDFCBANK: LTP ₹1251.20 | Change: +0.25%
[09:17:23] HDFCBANK: LTP ₹1002.00 | Change: -19.98%  ← Almost hit!
[09:18:23] HDFCBANK: LTP ₹999.00 | Change: -20.05%   ← HIT LOWER CIRCUIT!
⚠️ LOWER CIRCUIT HIT: HDFCBANK (-20.05%)
[TEST] Would BUY 1 shares of HDFCBANK ✓
```

### Example 2: Trade Multiple Stocks

```bash
$ python main.py

🚀 ZERODHA KITE CIRCUIT BREAKER TRADING BOT
================================================================

CIRCUIT BREAKER TRADING BOT - SELECT MODE
================================================================

1. Monitor SINGLE stock for circuit breaker
2. Monitor MULTIPLE stocks for circuit breaker  
3. AUTO-DETECT and trade circuit stocks (NSE 200)
4. View NSE 200 stocks
5. Exit

================================================================

Select option (1-5): 2

MODE 2: MONITOR MULTIPLE STOCKS
================================================================

Enter stock symbols (comma-separated, e.g., HDFCBANK,INFY,TCS): HDFCBANK,INFY,RELIANCE

Enter circuit % (default 20): 15

Enter quantity per trade (default 1): 2

Test mode (Y/N, default N): n

✓ Stocks: HDFCBANK, INFY, RELIANCE
✓ Circuit Level: 15%
✓ Quantity: 2
✓ Test Mode: False

[09:16:45] Checking 3 stocks...
  HDFCBANK     LTP: ₹1250.50 | +0.15%
  INFY         LTP: ₹ 945.00 | -0.50%
  RELIANCE     LTP: ₹2895.00 | +1.20%

[09:17:45] Checking 3 stocks...
  HDFCBANK     LTP: ₹1248.00 | -0.10%
  INFY         LTP: ₹ 800.75 | -15.30% ← HIT LOWER CIRCUIT!
  RELIANCE     LTP: ₹2920.00 | +0.85%

⚠️ LOWER: INFY (-15.30%)
✓ BUY order placed for INFY
```

---

## 🐛 Troubleshooting

### ❌ "Cannot connect to Kite API"

**Solution:** Check your credentials in `.env` file
```env
KITE_API_KEY=your_actual_key_here
KITE_ACCESS_TOKEN=your_actual_token_here
```

### ❌ "No quote data found"

**Reasons:**
- Market is closed (closed on weekends)
- Stock symbol is wrong (use NSE format like HDFCBANK, not HDFC Bank)
- Network issue

**Solution:** Use `python main.py` → option 4 to see all valid stocks

### ❌ "ModuleNotFoundError: No module named 'kiteconnect'"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install kiteconnect python-dotenv
```

### ❌ "No permission to create trading_bot.log"

**Solution:** Run the script from the kite folder where `main.py` is located.

---

## 📈 How the Bot Works (Technical Details)

### 1. **Initialization**
- Loads credentials from `.env`
- Connects to Zerodha Kite API
- Sets up configuration

### 2. **Monitoring Loop** (Every 5 seconds by default)
```python
while trading_active:
    # Get current price
    quote = kite.get_quote(symbol)
    ltp = quote['last_price']
    
    # Calculate change from previous close
    change_percent = (ltp - previous_close) / previous_close * 100
    
    # Check circuit levels
    if change_percent >= 20:  # UPPER CIRCUIT
        place_sell_order()
    elif change_percent <= -20:  # LOWER CIRCUIT
        place_buy_order()
```

### 3. **Risk Management**
- Max trades per day: prevents over-trading
- Max open positions: doesn't open too many at once
- Stop loss: exits if price goes against you by X%
- Take profit: exits if profit reaches X%

---

## ⚠️ Important Warnings

1. **Start with TEST MODE** first!
   ```python
   TEST_MODE = True
   ```

2. **Start with small quantities**
   ```python
   QUANTITY_PER_TRADE = 1
   ```

3. **Understand the risks** - Circuit breaker trading can be risky!

4. **Monitor continuously** - Don't leave the bot unattended

5. **Check logs** - Review `trading_bot.log` for all activity

---

## 💡 Tips for Success

1. **Test different percentages** to find what works for your style
   - 5-10%: Very aggressive (more frequent trades, higher risk)
   - 15-20%: Moderate (standard approach)
   - 25%+: Conservative (fewer trades, lower risk)

2. **Trade during market hours only**
   - NSE Market: 9:15 AM - 3:30 PM IST (Monday-Friday)

3. **Monitor the logs** to understand what's happening

4. **Use test mode** the first time to build confidence

5. **Start small** - 1 share per trade until you're confident

---

## 📞 Support

For issues or questions:
1. Check `trading_bot.log` for errors
2. Review this README section by section
3. Verify your Zerodha credentials are correct
4. Make sure market is open (9:15 AM - 3:30 PM IST)

---

**Happy Trading! 🚀**
