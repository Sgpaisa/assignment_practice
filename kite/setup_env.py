#!/usr/bin/env python3
"""
Quick Setup Script - Create .env file with your credentials
Run this ONCE to store credentials permanently
"""

import os
import sys

def setup_env_file():
    """Create .env file with user inputs"""
    
    print("\n" + "="*70)
    print("ZERODHA KITE - CREDENTIAL SETUP")
    print("="*70)
    print("\nThis script will create .env file with your credentials")
    print("You only need to do this ONCE\n")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("[CANCELLED] Keeping existing .env file")
            return False
    
    # Get API Key
    print("\n[STEP 1] Enter your API Key")
    print("         (From: https://developers.kite.trade/)")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("[ERROR] API Key cannot be empty!")
        return False
    
    # Get Access Token
    print("\n[STEP 2] Enter your Access Token")
    print("         (Generate using: python get_token.py)")
    access_token = input("Access Token: ").strip()
    
    if not access_token:
        print("[ERROR] Access Token cannot be empty!")
        return False
    
    # Optional: Get App Secret (for token refresh)
    print("\n[STEP 3] (Optional) Enter your App Secret")
    print("         (Leave blank if not needed - for auto-refresh feature)")
    print("         (From: https://developers.kite.trade/ -> Your App -> Settings)")
    app_secret = input("App Secret (optional): ").strip()
    
    # Create .env file content
    env_content = f"""# Zerodha Kite API Credentials
# DO NOT SHARE THIS FILE!
# Add to .gitignore if using Git

KITE_API_KEY={api_key}
KITE_ACCESS_TOKEN={access_token}
"""
    
    if app_secret:
        env_content += f"KITE_APP_SECRET={app_secret}\n"
    
    # Write to file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n" + "="*70)
        print("SUCCESS! .env file created")
        print("="*70)
        print("\nCredentials stored in: .env")
        print("API Key:     ", api_key[:20] + "...")
        print("Access Token:", access_token[:20] + "...")
        
        if app_secret:
            print("App Secret:  ", app_secret[:20] + "...")
        
        print("\n✅ You can now run the bot without entering credentials!")
        print("\nTo start trading:")
        print("  python QUICKSTART.py")
        
        return True
    
    except Exception as e:
        print(f"\n[ERROR] Could not create .env file: {e}")
        return False


def main():
    """Main setup function"""
    try:
        if setup_env_file():
            print("\n[OK] Setup complete! Your bot is ready to use.")
            return True
        else:
            print("\n[CANCELLED] Setup failed. Please try again.")
            return False
    
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Setup interrupted by user")
        return False
    
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
