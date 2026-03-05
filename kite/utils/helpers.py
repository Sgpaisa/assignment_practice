"""Helper utilities for trading"""

from config.nse200_stocks import get_all_stocks


def is_valid_stock(symbol: str) -> bool:
    """Check if stock symbol is in NSE 200"""
    return symbol.upper() in get_all_stocks()


def format_price(price: float) -> str:
    """Format price for display"""
    return f"₹{price:.2f}"


def format_change(change_percent: float) -> str:
    """Format change percentage"""
    symbol = "+" if change_percent >= 0 else ""
    return f"{symbol}{change_percent:.2f}%"
