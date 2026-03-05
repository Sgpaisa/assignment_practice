# ⚡ Zerodha Kite Circuit Breaker Trading Bot - NEW MODULAR VERSION

A clean, modular Python trading bot for Zerodha Kite that:
- ✅ Monitors stocks for circuit breaker levels
- ✅ Automatically places BUY/SELL orders
- ✅ Easy to configure and change percentages
- ✅ Supports single or multiple stocks
- ✅ Auto-detects circuit stocks from NSE 200
- ✅ Test mode for safe practice
- ✅ Fully modular and extensible

---

## 🚀 Quick Start (Choose One)

### 1️⃣ **Easiest - For Beginners**
```bash
python simple_setup.py
```
Interactive step-by-step setup!

### 2️⃣ **Recommended - Full Control**
```bash
python main.py
```
Menu-based with all options!

### 3️⃣ **For Advanced Users**
Edit `config/settings.py` and write custom scripts using the modular components.

---

## 📋 What This Bot Does

### Circuit Breaker Trading Strategy

```
🎯 WHEN STOCK DROPS BY X% (Lower Circuit)
└─ BUY Signal
   └─ Bot places BUY order
   └─ Wait for stock to bounce back
   └─ PROFIT!

🎯 WHEN STOCK RISES BY X% (Upper Circuit)
└─ SELL Signal
   └─ Bot places SELL order
   └─ Lock in profits
   └─ PROFIT!
```

---

## 📂 NEW MODULAR STRUCTURE

```
kite/
├── 🚀 main.py                    ← Start here (advanced)
├── 🚀 simple_setup.py            ← Start here (beginners)
├── requirements.txt               ← Dependencies
├── .env                          ← Your credentials (create this!)
│
├── config/                       ← 🔧 Change settings here
│   ├── settings.py              ← All configuration
│   └── nse200_stocks.py         ← List of NSE 200 stocks
│
├── core/                         ← Core trading logic
│   ├── kite_client.py           ← Zerodha API connection
│   ├── circuit_finder.py        ← Find circuit stocks
│   └── trader.py                ← Trading logic
│
├── strategies/                   ← Trading strategies
│   └── circuit_breaker_strategy.py
│
├── authenticators/               ← Authentication
│   └── token_manager.py
│
├── utils/                        ← Helper utilities
│   ├── logger.py                ← Logging setup
│   └── helpers.py               ← Helper functions
│
└── docs/                         ← 📚 Documentation
    ├── SETUP_GUIDE.md           ← Complete setup guide
    └── CONFIG_GUIDE.md          ← Configuration options
```

---

## 🔧 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create .env File

Create a file named `.env` in the kite folder:

```
KITE_API_KEY=your_api_key_here
KITE_ACCESS_TOKEN=your_access_token_here
```

Get credentials from: https://zerodha.com/developers/

### 3. Run the Bot

```bash
# Easy way:
python simple_setup.py

# Or:
python main.py
```

---

## 🎯 Key Features You Can Change

### Circuit Percentage (The Most Important!)

```python
# In config/settings.py or at runtime
UPPER_CIRCUIT_PERCENT = 20    # ← CHANGE THIS!
LOWER_CIRCUIT_PERCENT = 20    # ← AND THIS!
```python
API_KEY = "zudyrwgcegy6o0nw"       # From Step 1
ACCESS_TOKEN = "your_token_here"   # From Step 1
STOCK_TO_TRADE = "INFY"            # Your stock
UPPER_CIRCUIT_PERCENT = 20         # Sell threshold
LOWER_CIRCUIT_PERCENT = 20         # Buy threshold
QUANTITY_PER_TRADE = 1             # Shares per trade
```

### Step 3: Run Bot
```powershell
python bot.py
```

**That's it!** Watch the console for trading signals.

---

## 📝 WHAT TO EDIT & WHAT NOT TO

### ✅ EDIT THESE
- **config.py** - Change stock, percentages, quantity
- **.env** - Add your API credentials
- Nothing else!

### ❌ DON'T EDIT THESE
- bot.py - This is the main trading engine
- helpers/ scripts - Unless you know what you're doing
- docs/ - These are just reference

---

## 🔧 CONFIGURATION EXAMPLES

### Example 1: Trade RELIANCE with 10% threshold
```python
STOCK_TO_TRADE = "RELIANCE"
UPPER_CIRCUIT_PERCENT = 10
LOWER_CIRCUIT_PERCENT = 10
```

### Example 2: Conservative trading (small positions)
```python
QUANTITY_PER_TRADE = 1
STOP_LOSS_PERCENT = 1
TAKE_PROFIT_PERCENT = 3
```

### Example 3: Aggressive trading (larger positions)
```python
QUANTITY_PER_TRADE = 5
STOP_LOSS_PERCENT = 3
TAKE_PROFIT_PERCENT = 10
```

### Example 4: Test without real trades
```python
TEST_MODE = True  # Enable test mode
```

---

## 📊 REAL-TIME MONITORING

When bot runs, you'll see:

```
[RUNNING] Monitoring INFY for circuit breakers...
[RUNNING] Trading hours: 9:15 - 12:15
[RUNNING] Press Ctrl+C to stop

[14:30:20] INFY
  LTP: Rs. 1650.50 | Change: +2.3%
  Bid: Rs. 1650.20 | Ask: Rs. 1650.80
  Upper Circuit: Rs. 1800.00
  Lower Circuit: Rs. 1200.00

[14:35:45] INFY
  LTP: Rs. 1800.50 | Change: +20.1%

[WARNING] **UPPER CIRCUIT HIT**
[ORDER PLACED] SELL 1 @ Rs. 1800
```

---

## 🆘 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "API credentials not configured" | Edit config.py with API_KEY & ACCESS_TOKEN |
| "Could not fetch data for INFY" | Check stock symbol, market hours, internet |
| No orders placed | Check TEST_MODE = False, within trading hours |
| "Invalid API Key" | Run helpers/get_token.py to regenerate |
| Log file errors | Check trading_bot.log for detailed errors |

---

## 📁 FILE GUIDE

### Core Files (Essential)
| File | Purpose | Edit? |
|------|---------|-------|
| **bot.py** | Main trading bot | ❌ No |
| **config.py** | Configuration settings | ✅ YES! |
| **.env** | API credentials | ✅ YES (once) |
| **helpers/get_token.py** | Get access token | ❌ No |

### Reference Files (Optional Reading)
| File | Contains |
|------|----------|
| QUICK_START.md | Quick setup guide |
| docs/GET_ACCESS_TOKEN.md | Token generation details |
| docs/TOKEN_STORAGE_SOLUTIONS.md | Credential storage options |
| README_SETUP.md | Full setup instructions |
| CHECKLIST_TROUBLESHOOTING.py | Common issues & fixes |

### Legacy Files (Can Ignore)
- QUICKSTART.py - Old version
- zerodha_circuit_trader.py - Old full-featured bot
- kite.ipynb - Educational notebook
- CONFIG_TEMPLATES.md - Reference configs

---

## 💡 KEY CONCEPTS

### Circuit Breaker
When a stock price moves 20% (by default and by law in India):
- **UP 20%** = Upper circuit (too expensive) → **SELL**
- **DOWN 20%** = Lower circuit (bargain) → **BUY**

### Your Settings
```python
UPPER_CIRCUIT_PERCENT = 20  # Sell when up 20%
LOWER_CIRCUIT_PERCENT = 20  # Buy when down 20%
QUANTITY_PER_TRADE = 1      # Buy/sell 1 share
STOP_LOSS_PERCENT = 2       # Close trade if -2%
TAKE_PROFIT_PERCENT = 5     # Close trade if +5%
```

### How Bot Works
1. Checks stock price every 30 seconds
2. Calculates circuit levels
3. If circuit hit → Places order automatically
4. Monitors position with stop loss & take profit
5. Closes position at market close (3:30 PM)

---

## 🎯 COMMON CHANGES

### Change Stock
```python
# In config.py, line where it says:
STOCK_TO_TRADE = "INFY"

# Change to:
STOCK_TO_TRADE = "TCS"  # or any NSE symbol
```

### Change Percentages
```python
# Default (20% - official circuit):
UPPER_CIRCUIT_PERCENT = 20
LOWER_CIRCUIT_PERCENT = 20

# More trading (5% - very sensitive):
UPPER_CIRCUIT_PERCENT = 5
LOWER_CIRCUIT_PERCENT = 5

# Less trading (50% - very conservative):
UPPER_CIRCUIT_PERCENT = 50
LOWER_CIRCUIT_PERCENT = 50
```

### Change Position Size
```python
# Small (1 share)
QUANTITY_PER_TRADE = 1

# Medium (5 shares)
QUANTITY_PER_TRADE = 5

# Large (10 shares)
QUANTITY_PER_TRADE = 10
```

### Test Mode (No Real Trades)
```python
# Testing - shows what would happen:
TEST_MODE = True

# Live - actually places trades:
TEST_MODE = False
```

---

## ✅ SETUP CHECKLIST

- [ ] Read QUICK_START.md
- [ ] Run `python helpers/get_token.py` to get credentials
- [ ] Edit `config.py` with API_KEY and ACCESS_TOKEN
- [ ] Set STOCK_TO_TRADE to your choice
- [ ] Change percentages if needed
- [ ] Set TEST_MODE = True for first run
- [ ] Run `python bot.py`
- [ ] Watch console for output
- [ ] Check trading_bot.log for details
- [ ] Once confident, set TEST_MODE = False
- [ ] Run `python bot.py` to start trading

---

## 🚀 RUNNING THE BOT

### First Time (Test Mode)
```powershell
cd "D:\visual studio\Module and packages\kite"
# Make sure TEST_MODE = True in config.py
python bot.py
```

Watch for 5-10 minutes to see if it's working. Check logs.

### Live Trading
```powershell
# Change TEST_MODE = False in config.py
python bot.py
```

Monitor the first trades carefully.

### Stopping Bot
```
Press Ctrl+C in the terminal
```

---

## 📊 MONITORING

### Console Output
Shows real-time prices and signals

### Log File: `trading_bot.log`
```
2026-03-04 09:20:15,123 | INFO | [OK] Connected to Zerodha Kite API
2026-03-04 09:20:30,456 | INFO | [INFY] LTP: Rs. 1650.50 | Change: +2.3%
2026-03-04 09:35:45,789 | WARNING | UPPER CIRCUIT HIT for INFY!
2026-03-04 09:35:46,012 | INFO | [ORDER PLACED] SELL 1 @ Rs. 1800
```

Check this file if bot doesn't work as expected.

---

## 💰 CAPITAL REQUIREMENTS

- **Minimum**: ₹50,000 (for 4x MIS margin)
- **Per Trade**: 1 share * stock price * 4x margin
- **Example**: INFY @ ₹1650 = ₹6,600 margin needed

Start with 1 share until you're confident.

---

## 🔐 SECURITY

### Keep Safe
- API_KEY (never share)
- ACCESS_TOKEN (never share)
- .env file (never commit to git)

### Best Practices
- Store credentials in .env file only
- Add .env to .gitignore if using git
- Regenerate tokens monthly
- Use separate Zerodha account for bot

---

## 📚 LEARNING PATH

1. **Read**: QUICK_START.md (5 min)
2. **Setup**: Edit config.py (1 min)
3. **Test**: Run in TEST_MODE (5 min)
4. **Monitor**: Watch a test run (10 min)
5. **Go Live**: Change TEST_MODE = False
6. **Optimize**: Adjust settings based on results

---

## 🎓 UNDERSTANDING THE BOT

### What bot.py does:
1. Connects to Zerodha Kite API
2. Monitors your stock every 30 seconds
3. Checks if price hit circuit levels
4. Automatically places buy/sell orders
5. Monitors positions with SL/TP
6. Closes all positions at market close
7. Logs everything to trading_bot.log

### What config.py controls:
- Which stock to trade
- When to buy/sell (percentages)
- Position size (quantity)
- Risk limits (SL/TP)
- Test mode on/off

---

## ❓ FAQ

**Q: Do I need to monitor the bot?**
A: Not required, but recommended for first time. It runs automatically.

**Q: Can I trade multiple stocks?**
A: Currently designed for 1 stock. Edit bot.py for multiple stocks.

**Q: What if I lose internet connection?**
A: Bot will crash. Run it on VPS for 24/7 reliability.

**Q: Can I change settings while bot is running?**
A: No. Stop bot, edit config.py, restart bot.

**Q: How much will I earn?**
A: Depends on market volatility. Circuit breakers are rare (1-2/month).

**Q: Is this legal?**
A: Yes, algorithmic trading is legal in India.

---

## 🎯 NEXT STEPS

1. **Start Here**: Read QUICK_START.md
2. **Get Token**: Run `python helpers/get_token.py`
3. **Configure**: Edit config.py
4. **Test**: Run `python bot.py` with TEST_MODE = True
5. **Monitor**: Check trading_bot.log
6. **Go Live**: Set TEST_MODE = False and run

---

**Ready to start?** Run this command:

```powershell
cd "D:\visual studio\Module and packages\kite"
python bot.py
```

**Good luck!** 🚀 Remember: Start small, test thoroughly, scale gradually.

