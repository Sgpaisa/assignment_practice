"""
Token Manager for Zerodha Kite
Handles access token generation and management
"""

import logging
import webbrowser
from dotenv import load_dotenv, set_key
import os

logger = logging.getLogger(__name__)


class TokenManager:
    """Manage Zerodha authentication tokens"""
    
    def __init__(self, api_key: str, api_secret: str = None):
        """
        Initialize token manager
        
        Args:
            api_key: Your Kite API key
            api_secret: Your API secret (optional, for automated token generation)
        """
        self.api_key = api_key
        self.api_secret = api_secret
    
    def get_login_url(self) -> str:
        """
        Get Zerodha login URL for manual authentication
        
        Returns:
            Login URL
        """
        return f"https://kite.zerodha.com/connect/open?api_key={self.api_key}"
    
    def open_login_page(self):
        """Open login page in browser"""
        url = self.get_login_url()
        logger.info(f"Opening login page: {url}")
        webbrowser.open(url)
    
    @staticmethod
    def save_token_to_env(access_token: str, api_key: str = None):
        """
        Save access token to .env file
        
        Args:
            access_token: Access token from authentication
            api_key: API key (optional)
        """
        load_dotenv()
        
        env_file = '.env'
        
        if access_token:
            set_key(env_file, 'KITE_ACCESS_TOKEN', access_token)
            logger.info("Access token saved to .env")
        
        if api_key:
            set_key(env_file, 'KITE_API_KEY', api_key)
            logger.info("API key saved to .env")
    
    @staticmethod
    def load_credentials_from_env():
        """Load credentials from environment"""
        load_dotenv()
        
        api_key = os.getenv('KITE_API_KEY')
        access_token = os.getenv('KITE_ACCESS_TOKEN')
        
        if not api_key or not access_token:
            logger.warning("Missing credentials in .env file")
            return None, None
        
        return api_key, access_token
    
    @staticmethod
    def print_setup_instructions():
        """Print setup instructions"""
        print("\n" + "="*70)
        print("ZERODHA KITE AUTHENTICATION SETUP")
        print("="*70)
        print("""
1. Get your API credentials from https://zerodha.com/developers/
2. Save them in .env file in the root kite folder:
   
   KITE_API_KEY=your_api_key_here
   KITE_ACCESS_TOKEN=your_access_token_here

3. To get an access token:
   - Go to: https://kite.zerodha.com/connect/open?api_key=YOUR_API_KEY
   - Login to your Zerodha account
   - Copy the token from the redirect URL
   - Paste it in the .env file

For automated token management, use:
   TokenManager.open_login_page()
        """)
        print("="*70 + "\n")
