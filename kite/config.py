# ========================================================================
# ZERODHA KITE TRADING BOT - CONFIGURATION FILE
# Edit this file to customize your bot behavior
# ========================================================================

# ========================================================================
# STEP 1: API CREDENTIALS - Load from .env file
# ========================================================================
# Load environment variables from .env file
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file first

# Load credentials from environment variables (.env file)
API_KEY = os.getenv('KITE_API_KEY', '')
ACCESS_TOKEN = os.getenv('KITE_ACCESS_TOKEN', '')

# If not in .env, you can hardcode here (NOT RECOMMENDED - use .env instead):
# API_KEY = "your_api_key_here"
# ACCESS_TOKEN = "your_access_token_here"

# ========================================================================
# STEP 2: STOCK TO TRADE (Choose ONE from NSE 200)
# ========================================================================
# UNCOMMENT ONE stock below to select which NSE 200 stock to trade
# Just remove the # from one line and add # to others
# 
# BANKING SECTOR:
# STOCK_TO_TRADE = "SBIN"           # State Bank of India
STOCK_TO_TRADE = "HDFCBANK"       # HDFC Bank
# STOCK_TO_TRADE = "KOTAKBANK"      # Kotak Mahindra Bank
# STOCK_TO_TRADE = "AXISBANK"       # Axis Bank
# STOCK_TO_TRADE = "ICICIBANK"      # ICICI Bank
# STOCK_TO_TRADE = "IDFCBANK"       # IDFC Bank
# STOCK_TO_TRADE = "INDUSIND"       # IndusInd Bank
# STOCK_TO_TRADE = "RBL"            # RBL Bank
#
# IT SECTOR:
# STOCK_TO_TRADE = "INFY"           # Infosys
# STOCK_TO_TRADE = "TCS"            # Tata Consultancy Services
# STOCK_TO_TRADE = "WIPRO"          # Wipro
# STOCK_TO_TRADE = "TECHM"          # Tech Mahindra
# STOCK_TO_TRADE = "LTIM"           # LTI Mindtree
# STOCK_TO_TRADE = "HCLTECH"        # HCL Technologies
# STOCK_TO_TRADE = "MPHASIS"        # Mphasis
# STOCK_TO_TRADE = "OFSS"           # Oracle Financial Services
#
# PHARMA SECTOR:
# STOCK_TO_TRADE = "DRREDDY"        # Dr. Reddy's Laboratories
# STOCK_TO_TRADE = "SUNPHARMA"      # Sun Pharmaceutical
# STOCK_TO_TRADE = "CIPLA"          # Cipla
# STOCK_TO_TRADE = "LUPIN"          # Lupin
# STOCK_TO_TRADE = "DIVISLAB"       # Divi's Laboratories
# STOCK_TO_TRADE = "AUROPHARMA"     # Aurobindo Pharma
# STOCK_TO_TRADE = "BIOCON"         # Biocon
# STOCK_TO_TRADE = "PFIZER"         # Pfizer
#
# AUTO SECTOR:
# STOCK_TO_TRADE = "MARUTI"         # Maruti Suzuki
# STOCK_TO_TRADE = "TATAMOTORS"     # Tata Motors
# STOCK_TO_TRADE = "BAJAJ-AUTO"     # Bajaj Auto
# STOCK_TO_TRADE = "HEROMOTOCO"     # Hero MotoCorp
# STOCK_TO_TRADE = "EICHER"         # Eicher Motors
# STOCK_TO_TRADE = "SUMBEROTECH"    # Sumber Auto Tech
# STOCK_TO_TRADE = "JSWSTEEL"       # JSW Steel
# STOCK_TO_TRADE = "MOTHERSON"      # Motherson Sumi
#
# FINANCE & INSURANCE:
# STOCK_TO_TRADE = "HDFC"           # HDFC Corp
# STOCK_TO_TRADE = "BAJAJFINSV"     # Bajaj Finserv
# STOCK_TO_TRADE = "SBICARD"        # SBI Card
# STOCK_TO_TRADE = "SBILIFE"        # SBI Life
# STOCK_TO_TRADE = "HDFCLIFE"       # HDFC Life
# STOCK_TO_TRADE = "ICICIPRULI"     # ICICI Prudential
# STOCK_TO_TRADE = "SHRIRAMFIN"     # Shriram Finance
# STOCK_TO_TRADE = "MANAPPURAM"     # Manappuram Finance
#
# ENERGY & UTILITIES:
# STOCK_TO_TRADE = "RELIANCE"       # Reliance Industries
# STOCK_TO_TRADE = "BPCL"           # Bharat Petroleum
# STOCK_TO_TRADE = "HINDPETRO"      # Hindustan Petroleum
# STOCK_TO_TRADE = "NTPC"           # NTPC
# STOCK_TO_TRADE = "POWERGRID"      # Power Grid
# STOCK_TO_TRADE = "ONGC"           # Oil & Natural Gas
# STOCK_TO_TRADE = "COALINDIA"      # Coal India
# STOCK_TO_TRADE = "ADANIPOWER"     # Adani Power
#
# METAL & CEMENT:
# STOCK_TO_TRADE = "TATASTEEL"      # Tata Steel
# STOCK_TO_TRADE = "JSWSTEEL"       # JSW Steel
# STOCK_TO_TRADE = "HINDALCO"       # Hindalco
# STOCK_TO_TRADE = "SHREECEM"       # Shree Cement
# STOCK_TO_TRADE = "AMBUJACEMENT"   # Ambuja Cements
# STOCK_TO_TRADE = "ULTRACEMCO"     # UltraTech Cement
# STOCK_TO_TRADE = "RAMCOCEM"       # Ramco Cements
# STOCK_TO_TRADE = "GRASIM"         # Grasim Industries
#
# FAST MOVING CONSUMER GOODS (FMCG):
# STOCK_TO_TRADE = "NESTLEIND"      # Nestle India
# STOCK_TO_TRADE = "BRITANNIA"      # Britannia
# STOCK_TO_TRADE = "HINDUNILVR"     # Hindustan Unilever
# STOCK_TO_TRADE = "ITC"            # ITC
# STOCK_TO_TRADE = "MARICO"         # Marico
# STOCK_TO_TRADE = "COLPAL"         # Colgate-Palmolive
# STOCK_TO_TRADE = "GODREJCP"       # Godrej Consumer
# STOCK_TO_TRADE = "MOREPEN"        # Mohan Meakin
#
# INFRASTRUCTURE & REAL ESTATE:
# STOCK_TO_TRADE = "LT"             # Larsen & Toubro
# STOCK_TO_TRADE = "LTIM"           # LT Infotech Mindtree
# STOCK_TO_TRADE = "ADANIPORTS"     # Adani Ports
# STOCK_TO_TRADE = "DLF"            # DLF
# STOCK_TO_TRADE = "OBEROIRLTY"     # Oberoi Realty
# STOCK_TO_TRADE = "LODHA"          # Lodha Group
# STOCK_TO_TRADE = "INOXLEISURE"    # INOX Leisure
# STOCK_TO_TRADE = "PNC"            # P&C Housing
#
# TELECOM & MEDIA:
# STOCK_TO_TRADE = "BHARTIARTL"     # Bharti Airtel
# STOCK_TO_TRADE = "JIOTOWER"       # Jio Tower
# STOCK_TO_TRADE = "ZEEL"           # Zee Entertainment
# STOCK_TO_TRADE = "SONYLTD"        # Sony Electronics
# STOCK_TO_TRADE = "INDIAMART"      # IndiaMART
# STOCK_TO_TRADE = "NYKAA"          # Nykaa
# STOCK_TO_TRADE = "ZOMATO"         # Zomato
# STOCK_TO_TRADE = "PAYTM"          # Paytm
#
# FASHION & RETAIL:
# STOCK_TO_TRADE = "ASIANPAINT"     # Asian Paints
# STOCK_TO_TRADE = "DMART"          # Avenue Supermarts (Dmart)
# STOCK_TO_TRADE = "TITAN"          # Titan Company
# STOCK_TO_TRADE = "MCDOWELL-N"     # McDowell & Co
# STOCK_TO_TRADE = "PAGEIND"        # Page Industries
# STOCK_TO_TRADE = "POLYCAB"        # Polycab India
# STOCK_TO_TRADE = "HAVELLS"        # Havells India
# STOCK_TO_TRADE = "CROMPTON"       # Crompton Greaves
#
# DIVERSIFIED:
# STOCK_TO_TRADE = "BAJAJHLDNG"     # Bajaj Holdings
# STOCK_TO_TRADE = "M&M"            # Mahindra & Mahindra
# STOCK_TO_TRADE = "SUMITOMO"       # Sumitomo Rishi
# STOCK_TO_TRADE = "SIEMENS"        # Siemens
# STOCK_TO_TRADE = "KBL"            # Kalyani Steels
# STOCK_TO_TRADE = "AGRITECH"       # Agritech
# STOCK_TO_TRADE = "SUNTECH"        # Sunteck Industrial

# ========================================================================
# STEP 3: CIRCUIT BREAKER LEVELS (in percentage)
# ========================================================================
# When stock goes UP by this percentage -> SELL
UPPER_CIRCUIT_PERCENT = 20  # Standard: 20%, Conservative: 10%, Aggressive: 5%

# When stock goes DOWN by this percentage -> BUY
LOWER_CIRCUIT_PERCENT = 20  # Standard: 20%, Conservative: 10%, Aggressive: 5%

# ========================================================================
# STEP 4: POSITION MANAGEMENT
# ========================================================================
# How many shares to buy/sell per trade
QUANTITY_PER_TRADE = 1  # Start with 1, increase after testing

# Stop Loss (percentage below entry price)
STOP_LOSS_PERCENT = 2  # If price drops 2%, sell to limit losses

# Take Profit (percentage above entry price)
TAKE_PROFIT_PERCENT = 5  # If price rises 5%, sell to lock in profits

# ========================================================================
# STEP 5: RISK MANAGEMENT
# ========================================================================
# Maximum loss per day (in Rupees)
MAX_DAILY_LOSS = 100  # Stop trading if daily loss exceeds this

# Maximum number of trades per day
MAX_TRADES_PER_DAY = 10

# Maximum positions open at same time
MAX_OPEN_POSITIONS = 2

# ========================================================================
# STEP 6: TRADING HOURS
# ========================================================================
# Only trade during first 3 hours of market (9:15 AM - 12:15 PM IST)
TRADING_START_HOUR = 9
TRADING_START_MINUTE = 15

TRADING_END_HOUR = 15
TRADING_END_MINUTE = 30

# Auto-close all positions at market close (3:30 PM)
AUTO_CLOSE_AT_MARKET_CLOSE = True
MARKET_CLOSE_HOUR = 15
MARKET_CLOSE_MINUTE = 30

# ========================================================================
# STEP 7: TESTING & DEBUGGING
# ========================================================================
# Print detailed logs
DEBUG_MODE = True

# Test mode: Shows what WOULD happen without actually trading
TEST_MODE = False  # Set to True to test without real trades

# Print prices every X checks
PRINT_EVERY_X_CHECKS = 5

# ========================================================================
# STEP 8: LOGGING
# ========================================================================
LOG_FILE = "trading_bot.log"
LOG_CONSOLE = True  # Print logs to console

# ========================================================================
# QUICK REFERENCE - COMMON CONFIGURATIONS
# ========================================================================

# CONSERVATIVE TRADER (Low Risk):
# UPPER_CIRCUIT_PERCENT = 10
# LOWER_CIRCUIT_PERCENT = 10
# QUANTITY_PER_TRADE = 1
# STOP_LOSS_PERCENT = 1
# TAKE_PROFIT_PERCENT = 3

# MODERATE TRADER (Medium Risk):
# UPPER_CIRCUIT_PERCENT = 15
# LOWER_CIRCUIT_PERCENT = 15
# QUANTITY_PER_TRADE = 2
# STOP_LOSS_PERCENT = 2
# TAKE_PROFIT_PERCENT = 5

# AGGRESSIVE TRADER (High Risk):
# UPPER_CIRCUIT_PERCENT = 20
# LOWER_CIRCUIT_PERCENT = 20
# QUANTITY_PER_TRADE = 5
# STOP_LOSS_PERCENT = 3
# TAKE_PROFIT_PERCENT = 10

# ========================================================================
# END OF CONFIGURATION
# ========================================================================
# After editing this file:
# 1. Change STOCK_TO_TRADE to your stock
# 2. Update API_KEY and ACCESS_TOKEN
# 3. Adjust percentage and quantity as needed
# 4. Run: python bot.py
# 5. Watch the logs to see if it's working
# ========================================================================
