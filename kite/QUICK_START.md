# 🚀 ZERODHA KITE TRADING BOT - QUICK START GUIDE

## ⚡ 30 SECOND SETUP

### 1. Edit `config.py`
```python
API_KEY = "your_api_key_here"
ACCESS_TOKEN = "your_access_token_here"
STOCK_TO_TRADE = "INFY"  # Change to your stock
UPPER_CIRCUIT_PERCENT = 20
LOWER_CIRCUIT_PERCENT = 20
QUANTITY_PER_TRADE = 1
```

### 2. Run the bot
```powershell
cd "D:\visual studio\Module and packages\kite"
python bot.py
```

### 3. Watch the console for signals!

---

## 📁 SIMPLIFIED FILE STRUCTURE

```
kite/
├── bot.py                    ← THE MAIN BOT (Run this!)
├── config.py                 ← EDIT THIS to change settings
├── .env                      ← Your credentials (create this)
├── trading_bot.log           ← Generated trade logs
├── QUICK_START.md            ← This file
├── helpers/
│   ├── get_token.py         ← Get access token
│   └── setup_env.py         ← Create .env file
└── docs/
    ├── GET_ACCESS_TOKEN.md
    ├── TOKEN_STORAGE_SOLUTIONS.md
    └── others...
```

---

## 🎯 COMMON CONFIGURATIONS

### Conservative Trader (Low Risk)
```python
UPPER_CIRCUIT_PERCENT = 10
LOWER_CIRCUIT_PERCENT = 10
QUANTITY_PER_TRADE = 1
STOP_LOSS_PERCENT = 1
TAKE_PROFIT_PERCENT = 3
```

### Moderate Trader (Medium Risk)
```python
UPPER_CIRCUIT_PERCENT = 15
LOWER_CIRCUIT_PERCENT = 15
QUANTITY_PER_TRADE = 2
STOP_LOSS_PERCENT = 2
TAKE_PROFIT_PERCENT = 5
```

### Aggressive Trader (High Risk)
```python
UPPER_CIRCUIT_PERCENT = 20
LOWER_CIRCUIT_PERCENT = 20
QUANTITY_PER_TRADE = 5
STOP_LOSS_PERCENT = 3
TAKE_PROFIT_PERCENT = 10
```

---

## 🧪 TESTING MODE (NO REAL TRADES)

To test without placing real orders:

```python
# In config.py
TEST_MODE = True
```

Now run:
```powershell
python bot.py
```

Bot will show what trades WOULD happen without actually placing them.

---

## ✅ STEP-BY-STEP SETUP

### Step 1: Get Your Credentials

**Option A: Generate New Token (5 min)**
```powershell
python helpers/get_token.py
```

**Option B: Already have token? Use it directly**

### Step 2: Configure `config.py`

```python
# Your login credentials
API_KEY = "zudyrwgcegy6o0nw"  # From developers.kite.trade
ACCESS_TOKEN = "abcdef123456..."  # From get_token.py

# Which stock to trade
STOCK_TO_TRADE = "INFY"  # Change to your stock

# When to buy/sell
UPPER_CIRCUIT_PERCENT = 20  # Sell when up 20%
LOWER_CIRCUIT_PERCENT = 20  # Buy when down 20%

# Position size
QUANTITY_PER_TRADE = 1  # 1 share per trade

# Risk management
STOP_LOSS_PERCENT = 2  # Exit if loses 2%
TAKE_PROFIT_PERCENT = 5  # Exit if gains 5%
```

### Step 3: Run Bot

```powershell
cd "D:\visual studio\Module and packages\kite"
python bot.py
```

### Step 4: Watch Console for Signals

When circuit is hit, you'll see:
```
[WARNING] UPPER CIRCUIT HIT for INFY!
          Stock price: Rs. 1650.50
[ORDER PLACED] SELL 1 @ Rs. 1650
```

Or:
```
[WARNING] LOWER CIRCUIT HIT for INFY!
          Stock price: Rs. 1200.50
[ORDER PLACED] BUY 1 @ Rs. 1200
```

---

## 🔍 CHANGING PERCENTAGES

### Example 1: Lower percentage = More trading
```python
# More sensitive (trades at smaller moves)
UPPER_CIRCUIT_PERCENT = 5
LOWER_CIRCUIT_PERCENT = 5
```

### Example 2: Only want 1 stock
```python
STOCK_TO_TRADE = "TCS"  # Just change this
```

### Example 3: Risk management
```python
QUANTITY_PER_TRADE = 2  # Bigger positions
STOP_LOSS_PERCENT = 1   # Tighter SL
TAKE_PROFIT_PERCENT = 3  # Take profits faster
```

---

## 📊 WHAT YOU'LL SEE

### Normal Operation
```
[14:30:20] INFY
  LTP: Rs. 1650.50 | Change: +2.3%
  Bid: Rs. 1650.20 | Ask: Rs. 1650.80
  Upper Circuit: Rs. 1800.00
  Lower Circuit: Rs. 1200.00
```

### Circuit Hit!
```
[14:35:45] INFY
  LTP: Rs. 1800.50 | Change: +20.1%
  
[WARNING] **UPPER CIRCUIT HIT**
          Stock price: Rs. 1800.50
          Circuit level: Rs. 1800.00

[ORDER PLACED] SELL 1 @ Rs. 1800
               Order ID: 123456789

[POSITION OPEN] SHORT @ Rs. 1800.00
                Stop Loss: Rs. 1836.00
                Take Profit: Rs. 1700.00
```

---

## 🆘 TROUBLESHOOTING

### "API credentials not configured!"
**Solution:** Edit `config.py` with your API_KEY and ACCESS_TOKEN

### "Could not fetch data for INFY"
**Solution:** 
- Check stock symbol is correct
- Market might be closed
- Check internet connection

### No orders are being placed
**Solution:**
- Check if within trading hours (9:15 AM - 12:15 PM)
- Check circuit actually hit (up/down 20%)
- Check TEST_MODE is False

### Orders place but bot stops
**Solution:**
- Check `trading_bot.log` file for errors
- Verify Kite connection is stable
- Check sufficient margin in account

---

## 📝 EDITING config.py EXAMPLES

### Test with TCS instead of INFY
```python
STOCK_TO_TRADE = "TCS"
```

### Buy/Sell at 10% instead of 20%
```python
UPPER_CIRCUIT_PERCENT = 10
LOWER_CIRCUIT_PERCENT = 10
```

### Trade 5 shares instead of 1
```python
QUANTITY_PER_TRADE = 5
```

### Tight stop loss (2% instead of 2%)
```python
STOP_LOSS_PERCENT = 1
```

### Fast profit taking
```python
TAKE_PROFIT_PERCENT = 3
```

---

## 🧠 HOW IT WORKS

```
START BOT
   ↓
Check time (9:15 AM - 12:15 PM)
   ↓
Get stock price from Zerodha
   ↓
Calculate circuit levels (±20%)
   ↓
IS PRICE UP 20%? 
   YES → Place SELL order
   NO → Check next condition
   ↓
IS PRICE DOWN 20%?
   YES → Place BUY order
   NO → Wait and check again in 30 seconds
   ↓
REPEAT
```

---

## 💡 KEY SETTINGS EXPLAINED

| Setting | What it does | Example |
|---------|------------|---------|
| STOCK_TO_TRADE | Which stock to monitor | "INFY" |
| UPPER_CIRCUIT_PERCENT | Sell when up by % | 20 = Sell when +20% |
| LOWER_CIRCUIT_PERCENT | Buy when down by % | 20 = Buy when -20% |
| QUANTITY_PER_TRADE | Shares per trade | 1, 2, 5, etc. |
| STOP_LOSS_PERCENT | Exit loss limit | 2 = Exit if -2% |
| TAKE_PROFIT_PERCENT | Exit profit target | 5 = Exit if +5% |
| TEST_MODE | Test without trades | True = Test, False = Live |

---

## 🎓 USEFUL STOCKS TO PRACTICE WITH

| Stock | Volatility | Frequency |
|-------|-----------|-----------|
| INFY | High | Often hits circuit |
| TCS | High | Often hits circuit |
| RELIANCE | High | Regular circuits |
| HDFC | Medium | Occasional circuits |
| BAJAJFINSV | High | Frequent circuits |

---

## ✅ CHECKLIST BEFORE RUNNING

- [ ] Edited `config.py` with API_KEY
- [ ] Edited `config.py` with ACCESS_TOKEN
- [ ] Set STOCK_TO_TRADE to your choice
- [ ] TEST_MODE = True (for first run)
- [ ] Verified credentials work (run `python bot.py`)
- [ ] Understand buying/selling logic
- [ ] Ready to place real trades (TEST_MODE = False)

---

## 🚀 NEXT STEPS

1. **Get credentials** (if not done): Run `python helpers/get_token.py`
2. **Edit config.py** with your settings
3. **Test in test mode**: Set `TEST_MODE = True`
4. **Run bot**: `python bot.py`
5. **Watch logs**: See what happens
6. **Go live**: Set `TEST_MODE = False`

---

## 📞 NEED HELP?

### Check these files:
- `docs/GET_ACCESS_TOKEN.md` - How to get token
- `docs/TOKEN_STORAGE_SOLUTIONS.md` - Where to store credentials
- `trading_bot.log` - Detailed logs of what bot is doing
- `helpers/` - Utility scripts

### Common Issues:
- Credentials not working? Run `python helpers/get_token.py`
- Don't understand config? Read the comments in `config.py`
- Bot not trading? Check `trading_bot.log` for errors
- Testing first? Set `TEST_MODE = True` in `config.py`

---

## 🎯 SIMPLEST POSSIBLE SETUP

1. Copy your API credentials
2. Edit top 2 lines of `config.py`
3. Run `python bot.py`
4. Done!

```powershell
# That's literally it:
python bot.py
```

---

**Good luck with trading! Remember: Start small, test thoroughly, scale gradually.** 🚀

