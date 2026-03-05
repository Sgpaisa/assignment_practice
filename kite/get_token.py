#!/usr/bin/env python3
"""
Zerodha Kite Access Token Generator
Automates the process of getting your access token - takes 2 minutes!
"""

from kiteconnect import KiteConnect
import webbrowser
import sys

def get_access_token():
    print("\n" + "="*70)
    print("ZERODHA KITE - ACCESS TOKEN GENERATOR")
    print("="*70)
    
    # Step 1: Get API Key
    print("\n" + "[STEP 1] Enter your API Key")
    print("         (From: https://developers.kite.trade/)")
    print("-" * 70)
    
    API_KEY = input("API Key: ").strip()
    
    if not API_KEY:
        print("[ERROR] API Key cannot be empty!")
        return False
    
    print(f"[OK] API Key: {API_KEY}")
    
    # Step 2: Initialize Kite
    print("\n[STEP 2] Initializing Kite API...")
    try:
        kite = KiteConnect(api_key=API_KEY)
        print("[OK] Kite initialized successfully")
    except Exception as e:
        print(f"[ERROR] Failed to initialize: {e}")
        return False
    
    # Step 3: Get login URL
    print("\n[STEP 3] Generating login URL...")
    login_url = kite.login_url()
    print(f"[OK] Login URL generated")
    print(f"\nURL: {login_url}")
    
    # Step 4: Ask to open in browser
    print("\n[STEP 4] Open login in browser?")
    open_browser = input("Open in browser now? (y/n): ").strip().lower()
    
    if open_browser == 'y':
        print("[OK] Opening Zerodha login page...")
        webbrowser.open(login_url)
        print("     Login in your browser using your Zerodha credentials")
    else:
        print("     Paste this URL in your browser manually:")
        print(f"     {login_url}")
    
    # Step 5: Get authorization code
    print("\n[STEP 5] Get authorization code from browser")
    print("-" * 70)
    print("After logging in, you'll be redirected to localhost")
    print("The URL will show: http://localhost:8080/?status=success&code=XXXXX")
    print("Copy the code part (XXXXX)")
    print("-" * 70)
    
    code = input("\nPaste the code here: ").strip()
    
    if not code:
        print("[ERROR] Code cannot be empty!")
        return False
    
    print(f"[OK] Code: {code}")
    
    # Step 6: Get app secret
    print("\n[STEP 6] Enter your App Secret")
    print("         (From: https://developers.kite.trade/ -> Your App -> Settings)")
    print("-" * 70)
    
    app_secret = input("App Secret: ").strip()
    
    if not app_secret:
        print("[ERROR] App Secret cannot be empty!")
        return False
    
    print(f"[OK] App Secret: {app_secret}")
    
    # Step 7: Request access token
    print("\n[STEP 7] Requesting access token...")
    print("-" * 70)
    
    try:
        data = kite.request_access_token(code=code, secret=app_secret)
        access_token = data['access_token']
        
        print("[OK] Access token generated successfully!")
        
        # Display results
        print("\n" + "="*70)
        print("SUCCESS! YOUR CREDENTIALS:")
        print("="*70)
        print(f"\nAPI_KEY:      {API_KEY}")
        print(f"ACCESS_TOKEN: {access_token}")
        print("\n" + "="*70)
        print("NEXT STEPS:")
        print("="*70)
        print("\n1. Create a file named '.env' in this folder:")
        print("   d:/visual studio/Module and packages/kite/.env")
        print("\n2. Add these lines to .env file:")
        print(f"   KITE_API_KEY={API_KEY}")
        print(f"   KITE_ACCESS_TOKEN={access_token}")
        print("\n3. Save the file")
        print("\n4. Run the trading bot:")
        print("   python QUICKSTART.py")
        print("\n" + "="*70)
        
        # Ask to save to file
        save_to_file = input("\nSave credentials to .env file automatically? (y/n): ").strip().lower()
        
        if save_to_file == 'y':
            try:
                with open('.env', 'w') as f:
                    f.write(f"KITE_API_KEY={API_KEY}\n")
                    f.write(f"KITE_ACCESS_TOKEN={access_token}\n")
                print("[OK] Credentials saved to .env file!")
                print("     You can now run: python QUICKSTART.py")
            except Exception as e:
                print(f"[ERROR] Could not save to file: {e}")
                print("        Create .env file manually")
        
        return True
    
    except Exception as e:
        print(f"\n[ERROR] Failed to get access token!")
        print(f"Error: {e}")
        print("\nCommon issues:")
        print("1. Code already used - Login again and get a new code")
        print("2. Code expired - Must use within 10 minutes of login")
        print("3. Wrong app secret - Check at developers.kite.trade")
        print("4. Wrong API key - Copy exact key from app settings")
        return False

if __name__ == "__main__":
    try:
        success = get_access_token()
        
        if success:
            print("\n[OK] All done! Your bot is ready to trade!")
            sys.exit(0)
        else:
            print("\n[ERROR] Failed to get access token. Please try again.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Process interrupted by user")
        sys.exit(1)
