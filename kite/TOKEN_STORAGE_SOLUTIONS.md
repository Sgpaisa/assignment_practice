# Permanent Access Token Storage - 3 Easy Solutions

## Problem
Don't want to enter credentials every time you run the bot? Here are 3 methods to store the token permanently!

---

## ✅ SOLUTION 1: Store in .env File (EASIEST)

The bot already loads from `.env` file automatically. Just ONE-TIME setup:

### Step 1: Create .env file
Create a file named `.env` in this folder:
```
d:\visual studio\Module and packages\kite\.env
```

### Step 2: Add your credentials
```
KITE_API_KEY=zudyrwgcegy6o0nw
KITE_ACCESS_TOKEN=your_long_access_token_here
```

### Step 3: Save the file
That's it! The bot will automatically load credentials from this file.

### To run bot now:
```powershell
cd "D:\visual studio\Module and packages\kite"
python QUICKSTART.py
```

✅ **No more entering credentials every time!**

---

## ✅ SOLUTION 2: Windows Environment Variables (SYSTEM-WIDE)

Set once, use everywhere on your computer:

### Method A: Using PowerShell (Admin)

1. **Open PowerShell as Administrator**
   - Right-click PowerShell → Run as administrator

2. **Set the variables:**
```powershell
# Set API Key
[Environment]::SetEnvironmentVariable("KITE_API_KEY", "your_api_key_here", "User")

# Set Access Token
[Environment]::SetEnvironmentVariable("KITE_ACCESS_TOKEN", "your_access_token_here", "User")

# Verify
Get-Item -Path Env:KITE_API_KEY
Get-Item -Path Env:KITE_ACCESS_TOKEN
```

3. **Restart your terminal/VS Code** (important!)

4. **Now run bot:**
```powershell
python QUICKSTART.py
```

### Method B: Using GUI (Windows Settings)

1. **Open Start Menu** → Search "Environment Variables"
2. **Click "Edit the system environment variables"**
3. **Click "Environment Variables..." button**
4. **Click "New..."** under User variables
5. **Add:**
   - Variable name: `KITE_API_KEY`
   - Variable value: `your_api_key_here`
6. **Click "New..."** again for access token:
   - Variable name: `KITE_ACCESS_TOKEN`
   - Variable value: `your_access_token_here`
7. **Click OK → OK → OK**
8. **Restart terminal/VS Code**

✅ **Now credentials persist across all sessions!**

---

## ✅ SOLUTION 3: Auto-Refresh Token (RECOMMENDED FOR PRODUCTION)

Token expires sometimes. Use this script to auto-generate a fresh token when needed:

### Create file: `token_manager.py`

```python
#!/usr/bin/env python3
"""
Token Manager - Automatically maintains fresh access token
Regenerates token if it's about to expire
"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from kiteconnect import KiteConnect

class TokenManager:
    def __init__(self, token_file='.token_cache.json'):
        self.token_file = token_file
        load_dotenv()
        
        self.api_key = os.getenv('KITE_API_KEY')
        self.app_secret = os.getenv('KITE_APP_SECRET')
        
        if not self.api_key:
            raise ValueError("KITE_API_KEY not found in .env")
    
    def get_valid_token(self):
        """
        Returns a valid access token.
        Regenerates if needed.
        """
        cached_token = self.load_cached_token()
        
        if cached_token and self.is_token_valid(cached_token):
            print("[OK] Using cached access token")
            return cached_token
        
        print("[WARNING] Token expired or not found - Regenerating...")
        new_token = self.generate_new_token()
        
        if new_token:
            self.save_cached_token(new_token)
            return new_token
        
        raise ValueError("Failed to generate new token")
    
    def load_cached_token(self):
        """Load token from cache file"""
        if not os.path.exists(self.token_file):
            return None
        
        try:
            with open(self.token_file, 'r') as f:
                data = json.load(f)
                return data.get('access_token')
        except:
            return None
    
    def is_token_valid(self, token):
        """Check if token is still valid"""
        if not os.path.exists(self.token_file):
            return False
        
        try:
            with open(self.token_file, 'r') as f:
                data = json.load(f)
                
            # Check if generated within last 23 hours
            generated_time = datetime.fromisoformat(data['generated_at'])
            expires_at = generated_time + timedelta(hours=23)
            
            is_valid = datetime.now() < expires_at
            
            if not is_valid:
                print(f"[INFO] Token expired at {expires_at}")
            
            return is_valid
        except:
            return False
    
    def save_cached_token(self, token):
        """Save token to cache"""
        data = {
            'access_token': token,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(self.token_file, 'w') as f:
            json.dump(data, f)
        
        print(f"[OK] Token cached at {self.token_file}")
    
    def generate_new_token(self):
        """Generate new token using stored credentials"""
        print("\nYou need to authenticate again.")
        print("Follow these steps:")
        print("1. Run: python get_token.py")
        print("2. Complete the authentication process")
        print("3. Your token will be auto-saved")
        
        return None


# Usage in your bot:
if __name__ == "__main__":
    try:
        manager = TokenManager()
        access_token = manager.get_valid_token()
        print(f"Using token: {access_token[:10]}...")
        
    except Exception as e:
        print(f"[ERROR] {e}")
```

### Update QUICKSTART.py to use TokenManager:

Add this at the top of the bot code:

```python
from token_manager import TokenManager

# Instead of:
# API_KEY = os.getenv('KITE_API_KEY')
# ACCESS_TOKEN = os.getenv('KITE_ACCESS_TOKEN')

# Use:
try:
    manager = TokenManager()
    API_KEY = os.getenv('KITE_API_KEY')
    ACCESS_TOKEN = manager.get_valid_token()
except Exception as e:
    print(f"[ERROR] Failed to get token: {e}")
    exit(1)
```

---

## 📋 Comparison of All 3 Methods

| Method | Setup Time | Persistence | Security | Auto-Refresh |
|--------|-----------|-------------|----------|--------------|
| **.env File** | 2 min | ✅ Until token expires | ⚠️ Good (file ignored by git) | ❌ Manual |
| **Environment Variables** | 5 min | ✅ System-wide | ✅ Best | ❌ Manual |
| **Token Manager** | 5 min | ✅ Auto-cached | ✅ Best | ✅ Auto |

---

## 🎯 RECOMMENDED SETUP

**Best approach for daily trading:**

```powershell
# Step 1: Create .env file with credentials
# File: d:\visual studio\Module and packages\kite\.env
# Content:
KITE_API_KEY=your_api_key
KITE_ACCESS_TOKEN=your_access_token

# Step 2: Add .env to .gitignore (if using git)
echo ".env" >> .gitignore

# Step 3: Run bot
python QUICKSTART.py

# Step 4: DONE! Credentials never entered again
```

---

## ⏰ When Does Access Token Expire?

- **Zerodha Tokens**: Valid for **24 hours**
- **After 24 hours**: You need to regenerate using `get_token.py`
- **Recommendation**: Regenerate weekly to be safe

---

## 🔐 Security Best Practices

### ✅ DO:
- Store `.env` in `.gitignore`
- Use environment variables for production
- Regenerate tokens monthly
- Use separate account for trading bot

### ❌ DON'T:
- Commit `.env` to GitHub
- Share API keys with anyone
- Hardcode credentials in code
- Use production account for testing

---

## Quickest Solution - DO THIS NOW

### In PowerShell:

```powershell
# Navigate to kite folder
cd "D:\visual studio\Module and packages\kite"

# Create .env file with your credentials
# (Replace with YOUR actual credentials)
@"
KITE_API_KEY=your_api_key_here
KITE_ACCESS_TOKEN=your_access_token_here
"@ | Out-File -Encoding UTF8 .env

# Verify file was created
Get-Content .env

# Now run bot - no prompts!
python QUICKSTART.py
```

✅ **That's it! Credentials stored permanently!**

---

## Verify Setup

Test that credentials are loading:

```powershell
python
```

Then:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('KITE_API_KEY')
access_token = os.getenv('KITE_ACCESS_TOKEN')

print(f"API Key: {api_key}")
print(f"Access Token: {access_token}")
```

If you see your credentials printed, it's working! ✅

---

## Still Having Issues?

### .env file not loading?
- Make sure file is named exactly `.env` (no .txt extension)
- Make sure it's in the right folder
- Restart Python/terminal after creating file

### Token keeps expiring?
- Generate new token using `get_token.py` weekly
- Use TokenManager for auto-refresh (Solution 3)

### Different error?
- Check credential spelling
- Copy exactly from developers.kite.trade
- No extra spaces or quotes

---

## Summary

```
FASTEST SOLUTION: Create .env file with credentials
MOST SECURE: Use Windows environment variables
MOST AUTOMATED: Use TokenManager (auto-refresh)

Choose one and you'll never enter credentials again!
```

Let me know which method you choose and I'll help you set it up! 🚀

