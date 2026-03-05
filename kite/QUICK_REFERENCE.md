# 🎯 QUICK NAVIGATION GUIDE - Your New Bot Structure

## 🚀 WHERE TO START

### Option 1: I'm a Beginner
```bash
python simple_setup.py
```
→ Interactive wizard guides you through everything!

### Option 2: I Want Full Control
```bash
python main.py
```
→ Menu system with all options (single/multiple/auto-detect)

### Option 3: I Want to See Stocks First
```bash
python main.py
# Select option 4: View NSE 200 stocks
```
→ Browse available stocks by sector

---

## 🔧 WHERE TO CHANGE SETTINGS

### The Only File You Need to Edit
**File:** `config/settings.py`

```python
# Key settings to change:
STOCK_TO_TRADE = "HDFCBANK"         # Which stock?
UPPER_CIRCUIT_PERCENT = 20          # When to sell? (20%)
LOWER_CIRCUIT_PERCENT = 20          # When to buy? (20%)
QUANTITY_PER_TRADE = 1              # How many shares?

# Optional settings:
STOP_LOSS_PERCENT = 2               # Exit if down 2%
TAKE_PROFIT_PERCENT = 5             # Exit if up 5%
TEST_MODE = False                   # True = simulate, False = real
```

---

## 📂 WHAT EACH FOLDER DOES

| Folder | What's Inside | What It Does |
|--------|---------------|--------------|
| `config/` | settings.py, nse200_stocks.py | ⚙️ All configuration in one place |
| `core/` | kite_client.py, circuit_finder.py, trader.py | 💻 Core trading logic |
| `strategies/` | circuit_breaker_strategy.py | 🎯 Trading strategy |
| `authenticators/` | token_manager.py | 🔐 Handle authentication |
| `utils/` | logger.py, helpers.py | 🛠️ Helper utilities |
| `docs/` | SETUP_GUIDE.md, CONFIG_GUIDE.md | 📚 Complete documentation |

---

## 🎯 COMMON TASKS

### Task 1: Change Which Stock to Trade
Edit `config/settings.py`:
```python
STOCK_TO_TRADE = "INFY"  # Changed from HDFCBANK
```

### Task 2: Change Circuit Percentage
Edit `config/settings.py`:
```python
UPPER_CIRCUIT_PERCENT = 15    # Changed from 20
LOWER_CIRCUIT_PERCENT = 15    # More aggressive!
```

Or at runtime when running `main.py` - just enter the percentage.

### Task 3: Trade More Shares
Edit `config/settings.py`:
```python
QUANTITY_PER_TRADE = 5    # Changed from 1
```

### Task 4: Test Before Trading Real Money
Edit `config/settings.py`:
```python
TEST_MODE = True    # Simulate trades without risk!
```

### Task 5: Find All Available Stocks
```bash
python main.py
# Select option 4: View NSE 200 stocks
```

### Task 6: Trade Multiple Stocks
```bash
python main.py
# Select option 2: Monitor multiple stocks
# Enter: HDFCBANK,INFY,TCS
```

### Task 7: Auto-Detect Circuit Stocks
```bash
python main.py
# Select option 3: Auto-detect from all NSE 200
```

---

## 📖 DOCUMENTATION

### Quick Start
Read: `docs/SETUP_GUIDE.md`
- Installation steps
- How to get credentials
- First-time setup

### Configuration Reference
Read: `docs/CONFIG_GUIDE.md`
- All available settings
- What each setting does
- Configuration examples

### Troubleshooting
Read: `docs/SETUP_GUIDE.md` (Troubleshooting section)
- Common problems & solutions
- How to debug

---

## ⚠️ MUST KNOW

1. **Create .env file first**
   ```
   KITE_API_KEY=your_key
   KITE_ACCESS_TOKEN=your_token
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Use TEST_MODE first**
   ```python
   TEST_MODE = True  # In config/settings.py
   ```

4. **Start with 1 share**
   ```python
   QUANTITY_PER_TRADE = 1  # In config/settings.py
   ```

---

## 🏗️ ARCHITECTURE (Why It's Better)

### Before (Chaotic)
- Multiple trading files (bot.py, zerodha_circuit_trader.py, QUICKSTART.py)
- Configuration mixed in different places
- Hard to find what to edit
- Confusing structure

### After (Clean Modular)
✅ **One entry point** - main.py or simple_setup.py  
✅ **One config file** - config/settings.py only  
✅ **Organized code** - each piece has a purpose  
✅ **Easy to extend** - add new strategies without touching old code  
✅ **Easy to maintain** - clear folder organization  
✅ **Production ready** - proper logging, error handling, documentation  

---

## 🚀 YOUR FIRST TRADE (5 STEPS)

### Step 1: Install
```bash
pip install -r requirements.txt
```

### Step 2: Setup Credentials
Create `.env` file:
```
KITE_API_KEY=your_key
KITE_ACCESS_TOKEN=your_token
```

### Step 3: Configure
Edit `config/settings.py`:
```python
STOCK_TO_TRADE = "HDFCBANK"
UPPER_CIRCUIT_PERCENT = 20
TEST_MODE = True  # Test first!
```

### Step 4: Run
```bash
python simple_setup.py
```
Or:
```bash
python main.py
```

### Step 5: Watch
Follow the prompts and watch the trading signals!

---

## 💡 PRO TIPS

1. **Review logs** to understand what's happening
   - File: `trading_bot.log`
   - Shows all orders, prices, decisions

2. **Document your changes**  
   - Write down what circuit % works best
   - Track your profits/losses

3. **Test different percentages**
   - 5-10%: Very aggressive
   - 15-20%: Moderate (recommended)
   - 25-30%: Conservative

4. **Start small**
   - 1 share at a time
   - Increase after you're confident

5. **Use test mode**
   - Practice without risk
   - Verify settings work

---

## 📞 QUICK REFERENCE

| What to do | Where to look |
|-----------|----------|
| Run the bot | `python main.py` or `python simple_setup.py` |
| Change stock | `config/settings.py` - STOCK_TO_TRADE |
| Change circuit % | `config/settings.py` - UPPER/LOWER_CIRCUIT_PERCENT |
| Change quantity | `config/settings.py` - QUANTITY_PER_TRADE |
| View all stocks | `python main.py` → option 4 |
| Read setup guide | `docs/SETUP_GUIDE.md` |
| Read config guide | `docs/CONFIG_GUIDE.md` |
| Check logs | `trading_bot.log` |
| Get credentials | https://zerodha.com/developers/ |

---

## ✨ YOU'RE ALL SET!

Your kite folder is now:
- ✅ Organized and easy to navigate
- ✅ Simple to configure (one file to edit)
- ✅ Well documented
- ✅ Production ready
- ✅ Easy to modify and extend

**Next step:** Run `python simple_setup.py` and follow the prompts!

Good luck! 🚀
