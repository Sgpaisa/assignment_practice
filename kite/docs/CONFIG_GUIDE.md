# 🔧 Configuration Guide - Change Settings Easily

## Quick Reference

### Most Important Setting: Circuit %

```python
# In config/settings.py
UPPER_CIRCUIT_PERCENT = 20    # ← CHANGE THIS!
LOWER_CIRCUIT_PERCENT = 20    # ← AND THIS!
```

This is the **key setting** - everything else is optional.

---

## All Configuration Options

### Stock Selection

```python
# Trade a single stock
STOCK_TO_TRADE = "HDFCBANK"

# Or trade multiple stocks at once
MULTIPLE_STOCKS = ["HDFCBANK", "INFY", "TCS"]

# Or auto-detect all NSE 200 stocks hitting circuit
AUTO_DETECT_CIRCUIT_STOCKS = True
```

### Circuit Breaker (THE KEY SETTING!)

```python
# Example: 20% circuit
# - Stock up 20% → SELL signal
# - Stock down 20% → BUY signal

UPPER_CIRCUIT_PERCENT = 20
LOWER_CIRCUIT_PERCENT = 20

# Recommendations:
# - Aggressive trader: 5-10%
# - Moderate trader: 15-20%
# - Conservative trader: 25-30%
```

### Position Management

```python
QUANTITY_PER_TRADE = 1      # Shares per trade (start with 1!)

STOP_LOSS_PERCENT = 2       # Exit if price drops by this %
TAKE_PROFIT_PERCENT = 5     # Exit if price rises by this %

# Example:
# - Buy at ₹100
# - Stop loss at ₹98 (down 2%)
# - Take profit at ₹105 (up 5%)
```

### Risk Management

```python
MAX_DAILY_LOSS = 100        # Stop trading if loss exceeds this (₹)

MAX_TRADES_PER_DAY = 10     # Maximum trades per day

MAX_OPEN_POSITIONS = 2      # Max simultaneous positions
```

### Trading Hours

```python
# Only trade between these times (IST - Indian Standard Time)
TRADING_START_HOUR = 9
TRADING_START_MINUTE = 15    # 9:15 AM

TRADING_END_HOUR = 12
TRADING_END_MINUTE = 15      # 12:15 PM (first 3 hours)

# Auto-close all positions at market close
AUTO_CLOSE_AT_MARKET_CLOSE = True
MARKET_CLOSE_HOUR = 15
MARKET_CLOSE_MINUTE = 30     # 3:30 PM
```

### Monitoring & Refresh

```python
PRICE_CHECK_INTERVAL = 5    # Check prices every X seconds

LOG_EVERY_X_CHECKS = 5      # Print status every X checks
```

### Debug & Test Mode

```python
DEBUG_MODE = True           # Print detailed logs

TEST_MODE = False           # TEST = simulate, FALSE = real trading!

VERBOSE = True              # Print all details

LOG_FILE = "trading_bot.log"
LOG_LEVEL = "INFO"          # DEBUG, INFO, WARNING, ERROR
```

---

## Preset Configurations

### Conservative (Low Risk)

```python
from config.settings import ConservativeConfig

# Uses:
# - Circuit: 10%
# - Quantity: 1
# - Stop Loss: 1%
# - Take Profit: 3%
# - Max Trades: 5/day
```

### Moderate (Medium Risk)

```python
from config.settings import ModerateConfig

# Uses:
# - Circuit: 15%
# - Quantity: 2
# - Stop Loss: 2%
# - Take Profit: 5%
```

### Aggressive (High Risk)

```python
from config.settings import AggressiveConfig

# Uses:
# - Circuit: 20%
# - Quantity: 5
# - Stop Loss: 3%
# - Take Profit: 10%
# - Max Trades: 15/day
```

---

## How to Change Settings

### Method 1: Edit config/settings.py

Open `config/settings.py` and change the values directly:

```python
STOCK_TO_TRADE = "INFY"                    # Changed
UPPER_CIRCUIT_PERCENT = 15                 # Changed
QUANTITY_PER_TRADE = 2                     # Changed
```

### Method 2: Change at Runtime

The config can be updated while the bot is running:

```python
from config.settings import TradingConfig

TradingConfig.update(
    STOCK_TO_TRADE="INFY",
    UPPER_CIRCUIT_PERCENT=15,
    QUANTITY_PER_TRADE=2
)
```

### Method 3: Interactive Menu

```bash
python main.py
# Select option 1, 2, or 3
# When prompted, enter the circuit percentage and quantity
```

---

## Understanding the Settings

### What Each Setting Does

| Setting | Default | Effect | Recommendation |
|---------|---------|--------|-----------------|
| CIRCUIT_PERCENT | 20% | How much stock must move to trigger trade | 10-20% |
| QUANTITY | 1 | Shares per trade | Start with 1 |
| STOP_LOSS | 2% | Exit if price goes against you | 1-3% |
| TAKE_PROFIT | 5% | Exit if profit reaches this | 3-10% |
| MAX_TRADES | 10 | Max trades per day | 5-20 |
| MAX_POSITIONS | 2 | Simultaneous trades | 2-5 |

---

## Examples

### Example 1: Conservative Trader

```python
# Risk: LOW
UPPER_CIRCUIT_PERCENT = 10      # Only trade at 10%
LOWER_CIRCUIT_PERCENT = 10
QUANTITY_PER_TRADE = 1          # 1 share
STOP_LOSS_PERCENT = 1           # Tight stop
TAKE_PROFIT_PERCENT = 3         # Quick profit
MAX_TRADES_PER_DAY = 5          # Few trades
MAX_OPEN_POSITIONS = 1          # One at a time
```

### Example 2: Aggressive Trader

```python
# Risk: HIGH
UPPER_CIRCUIT_PERCENT = 20      # Trade at 20%
LOWER_CIRCUIT_PERCENT = 20
QUANTITY_PER_TRADE = 5          # 5 shares
STOP_LOSS_PERCENT = 3           # Loose stop
TAKE_PROFIT_PERCENT = 10        # Bigger profit target
MAX_TRADES_PER_DAY = 20         # Many trades
MAX_OPEN_POSITIONS = 5          # Multiple at once
```

### Example 3: Balanced Trader

```python
# Risk: MEDIUM
UPPER_CIRCUIT_PERCENT = 15      # Trade at 15%
LOWER_CIRCUIT_PERCENT = 15
QUANTITY_PER_TRADE = 2          # 2 shares
STOP_LOSS_PERCENT = 2           # Moderate stop
TAKE_PROFIT_PERCENT = 5         # Reasonable profit
MAX_TRADES_PER_DAY = 10         # Regular trades
MAX_OPEN_POSITIONS = 3          # Few simultaneous
```

---

## Common Configuration Changes

### Want to trade more frequently?
```python
UPPER_CIRCUIT_PERCENT = 5       # Down from 20
LOWER_CIRCUIT_PERCENT = 5       # Down from 20
```

### Want safer trading with bigger stops?
```python
STOP_LOSS_PERCENT = 5           # Up from 2
TAKE_PROFIT_PERCENT = 10        # Up from 5
```

### Want to trade more shares?
```python
QUANTITY_PER_TRADE = 10         # Up from 1
MAX_OPEN_POSITIONS = 5          # Up from 2
```

### Want to test before going live?
```python
TEST_MODE = True                # Simulate first!
```

---

## Credentials (.env File)

Create a `.env` file with:

```
KITE_API_KEY=your_key_here
KITE_ACCESS_TOKEN=your_token_here
```

**Never share or commit this file!**

---

## Important Tips

1. **Start with TEST_MODE = True** before trading real money
2. **Start with small QUANTITY** (like 1) before increasing
3. **Monitor the logs** to see what's happening
4. **Document your changes** for learning
5. **Test different percentages** to find your sweet spot

---

**Remember: Conservative settings = Fewer but safer trades**
**Aggressive settings = More trades but higher risk**
