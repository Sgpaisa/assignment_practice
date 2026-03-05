"""NSE 200 Stocks List - Organized by Sector"""

NSE_200_STOCKS = {
    "BANKING": {
        "SBIN": "State Bank of India",
        "HDFCBANK": "HDFC Bank",
        "ICICIBANK": "ICICI Bank",
        "KOTAKBANK": "Kotak Mahindra Bank",
        "AXISBANK": "Axis Bank",
        "IDFCBANK": "IDFC Bank",
        "INDUSIND": "IndusInd Bank",
    },
    "IT": {
        "TCS": "Tata Consultancy Services",
        "INFY": "Infosys",
        "WIPRO": "Wipro",
        "TECHM": "Tech Mahindra",
        "LTIM": "LTI Mindtree",
        "HCLTECH": "HCL Technologies",
    },
    "PHARMA": {
        "DRREDDY": "Dr. Reddy's Laboratories",
        "SUNPHARMA": "Sun Pharmaceutical",
        "CIPLA": "Cipla",
        "LUPIN": "Lupin",
        "DIVISLAB": "Divi's Laboratories",
        "AUROPHARMA": "Aurobindo Pharma",
        "BIOCON": "Biocon",
    },
    "AUTO": {
        "MARUTI": "Maruti Suzuki",
        "TATAMOTORS": "Tata Motors",
        "BAJAJ-AUTO": "Bajaj Auto",
        "HEROMOTOCO": "Hero MotoCorp",
        "EICHER": "Eicher Motors",
    },
    "FINANCE": {
        "HDFC": "HDFC Corp",
        "BAJAJFINSV": "Bajaj Finserv",
        "SBICARD": "SBI Card",
        "SBILIFE": "SBI Life",
        "HDFCLIFE": "HDFC Life",
    },
    "ENERGY": {
        "RELIANCE": "Reliance Industries",
        "BPCL": "Bharat Petroleum",
        "ONGC": "Oil & Natural Gas",
        "NTPC": "NTPC",
        "POWERGRID": "Power Grid",
    },
    "METALS": {
        "TATASTEEL": "Tata Steel",
        "JSWSTEEL": "JSW Steel",
        "HINDALCO": "Hindalco",
        "SHREECEM": "Shree Cement",
    },
    "FMCG": {
        "NESTLEIND": "Nestle India",
        "BRITANNIA": "Britannia",
        "HINDUNILVR": "Hindustan Unilever",
        "ITC": "ITC",
    },
    "REALTY": {
        "DLF": "DLF",
        "OBEROIRLTY": "Oberoi Realty",
    },
    "TELECOM": {
        "BHARTIARTL": "Bharti Airtel",
        "JIOTOWER": "Jio Tower",
    },
}

def get_all_stocks():
    """Return flat list of all NSE 200 stocks"""
    all_stocks = {}
    for sector, stocks in NSE_200_STOCKS.items():
        all_stocks.update(stocks)
    return all_stocks

def get_stocks_by_sector(sector_name):
    """Get stocks from a specific sector"""
    return NSE_200_STOCKS.get(sector_name, {})

def get_all_sectors():
    """Get list of all sectors"""
    return list(NSE_200_STOCKS.keys())
