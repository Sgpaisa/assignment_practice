"""
ZERODHA KITE CIRCUIT BREAKER TRADING BOT
SETUP VERIFICATION CHECKLIST & TROUBLESHOOTING
"""

# ============================================================================
# PRE-DEPLOYMENT CHECKLIST
# ============================================================================

CHECKLIST = """
📋 SETUP VERIFICATION CHECKLIST

SECTION 1: INSTALLATION ✓
☐ Python 3.7+ installed (Check: python --version)
☐ pip package manager working (Check: pip --version)
☐ kiteconnect library installed
☐ schedule library installed
☐ python-dotenv library installed

SECTION 2: ZERODHA SETUP ✓
☐ Zerodha account created (www.zerodha.com)
☐ API app created at (developers.kite.trade)
☐ API Key obtained
☐ Access Token generated
☐ App Secret saved securely
☐ Credentials stored in .env file (NEVER in code!)

SECTION 3: CONFIGURATION ✓
☐ .env file created with API credentials
☐ Stock symbols defined (e.g., INFY, TCS)
☐ Quantity per trade set (recommend starting with 1)
☐ Stop loss percentage defined (recommend 1-2%)
☐ Take profit percentage defined (recommend 3-5%)
☐ Trading window verified (9:15 AM - 12:15 PM IST)

SECTION 4: TESTING ✓
☐ Test connection to Kite API
☐ Fetch quotes for 1-2 stocks successfully
☐ Manually simulate circuit breaker detection
☐ Verify order placement on test account
☐ Check logging is working correctly
☐ Verify stop loss & take profit logic

SECTION 5: MONITORING SETUP ✓
☐ Logging file configured (circuit_trades.log)
☐ Email alerts configured (optional)
☐ Telegram alerts configured (optional)
☐ Dashboard/monitoring tool set up

SECTION 6: RISK MANAGEMENT ✓
☐ Max daily loss limit defined
☐ Max position size calculated
☐ Position sizing based on capital
☐ Emergency stop method planned
☐ Manual override procedure documented

SECTION 7: MARKET KNOWLEDGE ✓
☐ Understand what circuit breakers are
☐ Know which stocks hit circuits frequently
☐ Familiar with NSE trading hours
☐ Know holidays when market is closed
☐ Understand margin requirements for MIS

SECTION 8: FINAL VERIFICATION ✓
☐ Code reviewed for errors
☐ No hardcoded passwords in code
☐ Test run with small quantities (1 share)
☐ Monitor first day manually
☐ Keep emergency contact handy (Zerodha support)
☐ Backup of all configuration files

STATUS: [ ] Ready to deploy | [ ] Needs more work
"""

print(CHECKLIST)

# ============================================================================
# TROUBLESHOOTING GUIDE
# ============================================================================

TROUBLESHOOTING = {
    "Authentication Issues": {
        "Access Denied / Invalid Access Token": {
            "cause": "Access token expired or incorrect",
            "solution": [
                "1. Regenerate access token from developers.kite.trade",
                "2. Update .env file with new token",
                "3. Restart the bot",
                "4. Check token hasn't been used elsewhere"
            ]
        },
        "Invalid API Key": {
            "cause": "API key is incorrect or app is disabled",
            "solution": [
                "1. Verify API key from app settings",
                "2. Ensure app status is 'active'",
                "3. Copy exact key (no extra spaces)",
                "4. Update .env file and restart"
            ]
        }
    },
    
    "Trading Issues": {
        "Insufficient Margin": {
            "cause": "Account doesn't have 4x margin for MIS orders",
            "solution": [
                "1. Add funds to your Zerodha account",
                "2. Reduce quantity per trade",
                "3. Use NRML product instead of MIS (3x margin)",
                "4. Close existing positions to free margin"
            ]
        },
        "Order Rejected": {
            "cause": "Multiple reasons - invalid symbol, circuit limits, etc",
            "solution": [
                "1. Verify stock symbol is correct (e.g., 'INFY' not 'INFOSYS')",
                "2. Check stock hasn't actually hit circuit (trading halted)",
                "3. Ensure price is within acceptable range",
                "4. Check order quantity is valid",
                "5. Verify NSE symbol format (use official NSE list)"
            ]
        },
        "Orders Not Executing": {
            "cause": "Market closed, circuit breaker not hit, or network issue",
            "solution": [
                "1. Check if market is open (9:15 AM - 3:30 PM IST, weekdays only)",
                "2. Verify stock symbol and LTP in Zerodha app",
                "3. Check internet connection stability",
                "4. Monitor circuit_trades.log for errors",
                "5. Add debugging to print all prices checked"
            ]
        }
    },
    
    "Technical Issues": {
        "'ModuleNotFoundError: No module named 'kiteconnect'": {
            "cause": "kiteconnect library not installed",
            "solution": [
                "Run: pip install kiteconnect",
                "Verify with: python -c 'import kiteconnect; print(kiteconnect.__version__)'",
                "If still fails, try: pip install --upgrade kiteconnect"
            ]
        },
        "'Connection Error' / 'Timeout'": {
            "cause": "Network issue or Zerodha API down",
            "solution": [
                "1. Check internet connection",
                "2. Try pinging google.com",
                "3. Restart bot and try again",
                "4. Check Zerodha status page (status.kite.trade)",
                "5. Add reconnection logic to bot",
                "6. Consider using VPS for 24/7 connectivity"
            ]
        },
        "Bot Crashes/Exits Unexpectedly": {
            "cause": "Unhandled exception in code",
            "solution": [
                "1. Check logs in circuit_trades.log",
                "2. Add try-except blocks for each operation",
                "3. Add more detailed logging",
                "4. Check available system memory/disk space",
                "5. Run bot in background with process manager (PM2, systemd)",
                "6. Add graceful shutdown handlers"
            ]
        }
    },
    
    "Performance Issues": {
        "High Latency / Slow Orders": {
            "cause": "Network lag or exchange overload",
            "solution": [
                "1. Use VPS close to NSE server location",
                "2. Check internet speed (recommend >10 Mbps)",
                "3. Use 1-minute order placement instead of immediate",
                "4. Consider using WebSocket for real-time prices"
            ]
        },
        "High Slippage (Order price vs LTP)": {
            "cause": "Order placed at worse price due to queue",
            "solution": [
                "1. Use slightly better price than LTP",
                "2. Use market orders instead of limit (but riskier)",
                "3. Monitor order in real-time and cancel if not filled",
                "4. Test with small quantities first",
                "5. Increase price slightly above current LTP"
            ]
        }
    },
    
    "Logic Issues": {
        "Bot Not Detecting Circuit Breaker": {
            "cause": "Calculation error or threshold mismatch",
            "solution": [
                "1. Verify circuit threshold is 20% (CIRCUIT = 20)",
                "2. Print actual prices and calculations",
                "3. Check your calculation: upper = close * 1.20",
                "4. Ensure you're checking 'close' not 'open' price",
                "5. Add debug logging to print all detected circuits",
                "6. Manually check if stock hit circuit in Zerodha app"
            ]
        },
        "Bot Trading During Wrong Hours": {
            "cause": "Time zone issue or trading window check error",
            "solution": [
                "1. Verify server time is IST (Indian Standard Time)",
                "2. Check: python -c 'from datetime import datetime; print(datetime.now())'",
                "3. Set system timezone to IST if needed",
                "4. Add logging for current time check",
                "5. Hardcode market hours if time zone is issue"
            ]
        },
        "Repeated Orders For Same Stock": {
            "cause": "Position tracking not working correctly",
            "solution": [
                "1. Add position check before placing order",
                "2. Use dict to store active positions",
                "3. Check if stock already in positions before trading",
                "4. Add logic to skip if position already open",
                "5. Log all position changes for debugging"
            ]
        }
    }
}

print("\n" + "="*70)
print("TROUBLESHOOTING GUIDE")
print("="*70)

for category, issues in TROUBLESHOOTING.items():
    print(f"\n🔴 {category}")
    print("-" * 70)
    for issue, details in issues.items():
        print(f"\n  ❌ {issue}")
        print(f"  → Cause: {details['cause']}")
        print(f"  → Solutions:")
        for solution in details['solution']:
            print(f"      {solution}")

# ============================================================================
# QUICK DEBUG SCRIPT
# ============================================================================

DEBUG_SCRIPT = """
# DEBUG SCRIPT - Run this to test bot setup
# Save as debug_test.py and run: python debug_test.py

#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from datetime import datetime, time

print("DEBUG TEST - Circuit Trading Bot")
print("="*50)

# Test 1: Check Python version
import sys
print(f"✓ Python Version: {sys.version}")

# Test 2: Check environment variables
load_dotenv()
api_key = os.getenv('KITE_API_KEY')
access_token = os.getenv('KITE_ACCESS_TOKEN')

if api_key and access_token:
    print(f"✓ API credentials loaded")
else:
    print(f"✗ ERROR: .env file not configured")
    exit(1)

# Test 3: Check libraries
try:
    import kiteconnect
    print(f"✓ kiteconnect library found: v{kiteconnect.__version__}")
except:
    print(f"✗ ERROR: kiteconnect not installed")
    exit(1)

try:
    import schedule
    print(f"✓ schedule library found")
except:
    print(f"✗ ERROR: schedule not installed")
    exit(1)

# Test 4: Test Kite API connection
from kiteconnect import KiteConnect

try:
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    
    # Try to get profile
    profile = kite.profile()
    print(f"✓ Connected to Zerodha Kite API")
    print(f"  User ID: {profile['user_id']}")
    print(f"  Email: {profile['email']}")
    
except Exception as e:
    print(f"✗ ERROR: Could not connect to Kite API")
    print(f"  Details: {e}")
    exit(1)

# Test 5: Test fetching quote
try:
    quote = kite.quote(symbols=['INFY'])
    infy_price = quote['data']['INFY']['last_price']
    print(f"✓ Fetched INFY price: Rs. {infy_price}")
except Exception as e:
    print(f"✗ ERROR: Could not fetch quote")
    print(f"  Details: {e}")
    exit(1)

# Test 6: Check market hours
now = datetime.now()
market_open = time(9, 15)
market_close = time(15, 30)
is_weekday = now.weekday() < 5

print(f"\\n✓ Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"✓ Is weekday: {is_weekday}")
print(f"✓ Is within market hours: {market_open <= now.time() <= market_close}")

# Test 7: Test circuit calculation
prev_close = 1500
ltp = 1200  # Lower circuit
upper = prev_close * 1.20
lower = prev_close * 0.80

print(f"\\n✓ Circuit Breaker Test:")
print(f"  Previous Close: {prev_close}")
print(f"  Upper Circuit: {upper}")
lower_circuit = ltp <= lower * 1.02
print(f"  Lower Circuit Hit: {lower_circuit}")

print(f"\\n✅ All tests passed! Bot is ready to run.")
"""

print("\n" + "="*70)
print("DEBUG SCRIPT")
print("="*70)
print(DEBUG_SCRIPT)

# ============================================================================
# EMERGENCY CONTACTS
# ============================================================================

print("""
🚨 EMERGENCY CONTACTS

Zerodha Support:
  - Website: support.zerodha.com
  - Email: support@zerodha.com
  - Phone: 1800-114-414-414 (Toll Free)
  - WhatsApp: +91 9108900600

For Trading Issues:
  - Check order status in Zerodha app immediately
  - Contact support if order not executed after 5 minutes
  - Document all issues with screenshots

For API/Technical Issues:
  - Check Kite status page: https://status.kite.trade
  - Visit developers forum: https://forum.kite.trade
  - Check GitHub issues: https://github.com/zerodhatech/pykiteconnect

For Losses/Complaints:
  - File complaint via Zerodha email within 24 hours
  - Document order details and execution price
  - Keep all logs for reference
""")

# ============================================================================
# FINAL NOTES
# ============================================================================

print("""
⚠️  IMPORTANT NOTES

1. TRADING RISK:
   - Circuit breaker trades are HIGHLY VOLATILE
   - You can lose more than expected
   - Only trade with money you can afford to lose

2. TESTING:
   - Always test with 1 share first
   - Monitor manually for first week
   - Double-check calculations and thresholds

3. SAFETY:
   - Never leave bot running unattended for full day
   - Check logs at least twice during trading hours
   - Have manual override procedure ready
   - Keep sufficient margin buffer (2x recommended position)

4. PERFORMANCE:
   - Track all trades in spreadsheet
   - Calculate win rate monthly
   - Adjust strategy based on results
   - Don't increase quantities until profitable

5. DISCLAIMER:
   - This bot is for educational purposes
   - Use at your own risk
   - Not responsible for losses
   - Consult financial advisor before deploying

Good luck! 📈
""")
