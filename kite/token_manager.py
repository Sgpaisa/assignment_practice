#!/usr/bin/env python3
"""
Token Manager - Automatically maintains fresh access token
Regenerates token if it's about to expire (keeps bot running 24/7)
"""

import os
import json
import webbrowser
from datetime import datetime, timedelta
from dotenv import load_dotenv
from kiteconnect import KiteConnect

class TokenManager:
    """Manages Kite API access tokens with auto-refresh capability"""
    
    def __init__(self, token_cache_file='.token_cache.json'):
        """Initialize token manager"""
        self.token_cache_file = token_cache_file
        load_dotenv()
        
        self.api_key = os.getenv('KITE_API_KEY')
        self.app_secret = os.getenv('KITE_APP_SECRET')
        
        if not self.api_key:
            raise ValueError("[ERROR] KITE_API_KEY not found in .env file")
    
    def get_valid_token(self):
        """
        Get a valid access token
        Returns cached token if valid, otherwise regenerates
        """
        # Try to get cached token
        cached_token = self.load_cached_token()
        
        if cached_token and self.is_token_valid(cached_token):
            remaining = self.get_token_remaining_time()
            print(f"[OK] Using cached token - expires in {remaining}")
            return cached_token
        
        # Token expired or not found
        print("[WARNING] Access token expired or not found")
        print("[INFO] Regenerating access token...")
        
        new_token = self.regenerate_token()
        
        if new_token:
            self.save_cached_token(new_token)
            return new_token
        
        raise ValueError("[ERROR] Failed to regenerate access token")
    
    def load_cached_token(self):
        """Load token from cache file"""
        if not os.path.exists(self.token_cache_file):
            return None
        
        try:
            with open(self.token_cache_file, 'r') as f:
                data = json.load(f)
                return data.get('access_token')
        except Exception as e:
            print(f"[WARNING] Error reading token cache: {e}")
            return None
    
    def is_token_valid(self, token):
        """Check if cached token is still valid (less than 24 hours old)"""
        if not token or not os.path.exists(self.token_cache_file):
            return False
        
        try:
            with open(self.token_cache_file, 'r') as f:
                data = json.load(f)
            
            # Token is valid for 24 hours, regenerate after 23 hours to be safe
            generated_time = datetime.fromisoformat(data['generated_at'])
            expires_at = generated_time + timedelta(hours=23)
            
            is_valid = datetime.now() < expires_at
            
            if not is_valid:
                print(f"[INFO] Token expired at {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return is_valid
        except Exception as e:
            print(f"[WARNING] Error checking token validity: {e}")
            return False
    
    def get_token_remaining_time(self):
        """Get remaining time before token expires"""
        if not os.path.exists(self.token_cache_file):
            return "Unknown"
        
        try:
            with open(self.token_cache_file, 'r') as f:
                data = json.load(f)
            
            generated_time = datetime.fromisoformat(data['generated_at'])
            expires_at = generated_time + timedelta(hours=23)
            remaining = expires_at - datetime.now()
            
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            
            return f"{hours}h {minutes}m"
        except:
            return "Unknown"
    
    def save_cached_token(self, token):
        """Save token to cache file for future use"""
        data = {
            'access_token': token,
            'generated_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        try:
            with open(self.token_cache_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"[OK] Token cached successfully")
        except Exception as e:
            print(f"[WARNING] Could not save token cache: {e}")
    
    def regenerate_token(self):
        """
        Regenerate access token using API key and app secret
        Returns new access token or None if failed
        """
        print("\n" + "="*70)
        print("TOKEN REGENERATION REQUIRED")
        print("="*70)
        
        # Check if app secret is configured
        if not self.app_secret:
            print("[ERROR] KITE_APP_SECRET not found in .env file")
            print("\nAdd this to your .env file:")
            print("KITE_APP_SECRET=your_app_secret_from_developers_kite_trade")
            return None
        
        # Initialize Kite
        kite = KiteConnect(api_key=self.api_key)
        login_url = kite.login_url()
        
        print("\n[STEP 1] Opening Zerodha login...")
        print(f"URL: {login_url}\n")
        
        # Try to open in browser
        try:
            webbrowser.open(login_url)
            print("[OK] Login page opened in browser")
        except:
            print("[WARNING] Could not open browser - please open manually")
        
        # Get authorization code
        print("\n[STEP 2] Login with your Zerodha credentials")
        print("         After login, copy the code from the URL")
        
        code = input("\nPaste authorization code here: ").strip()
        
        if not code:
            print("[ERROR] Code cannot be empty")
            return None
        
        # Request access token
        print("\n[STEP 3] Generating access token...")
        
        try:
            data = kite.request_access_token(code=code, secret=self.app_secret)
            access_token = data['access_token']
            
            print("[OK] Access token generated successfully!")
            
            # Update .env with new token
            self.update_env_file(access_token)
            
            return access_token
        
        except Exception as e:
            print(f"[ERROR] Failed to get access token: {e}")
            print("\nPossible issues:")
            print("- Code already used (login again to get new code)")
            print("- Code expired (must use within 10 minutes)")
            print("- Wrong app secret (check developers.kite.trade)")
            return None
    
    def update_env_file(self, new_token):
        """Update .env file with new access token"""
        try:
            # Read current .env
            env_content = ""
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    env_content = f.read()
            
            # Update or add KITE_ACCESS_TOKEN
            lines = env_content.split('\n')
            updated = False
            
            new_lines = []
            for line in lines:
                if line.startswith('KITE_ACCESS_TOKEN='):
                    new_lines.append(f'KITE_ACCESS_TOKEN={new_token}')
                    updated = True
                elif line.strip():
                    new_lines.append(line)
            
            if not updated:
                new_lines.append(f'KITE_ACCESS_TOKEN={new_token}')
            
            # Write back
            with open('.env', 'w') as f:
                f.write('\n'.join(new_lines) + '\n')
            
            print("[OK] Updated .env file with new token")
        
        except Exception as e:
            print(f"[WARNING] Could not update .env file: {e}")
            print("         You'll need to update manually")


def main():
    """Test the token manager"""
    print("\n" + "="*70)
    print("TOKEN MANAGER - ZERODHA KITE")
    print("="*70 + "\n")
    
    try:
        manager = TokenManager()
        print(f"[OK] API Key: {manager.api_key[:10]}...")
        
        # Get valid token
        token = manager.get_valid_token()
        
        print(f"\n[OK] Current Access Token: {token[:20]}...")
        print("\nYou can now use this token in your bot!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False
    
    return True


if __name__ == "__main__":
    import sys
    
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Process interrupted")
        sys.exit(1)
