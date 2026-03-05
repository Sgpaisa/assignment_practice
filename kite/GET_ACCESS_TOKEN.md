# How to Get KITE_ACCESS_TOKEN - Step by Step Guide

## 📋 Complete Process (5 Minutes)

### STEP 1: Create Zerodha App
1. Go to: **https://developers.kite.trade/**
2. Sign in with your **Zerodha account credentials**
   - Username: Your Zerodha client ID
   - Password: Your Zerodha account password
3. Click **"Create App"** (or use existing app if you have one)

### STEP 2: Fill App Details
Enter the following information:

```
App Name:     CircuitTrader (or any name you want)
Redirect URL: http://localhost:8080/
Purpose:      Kite API trading bot
Scopes:       Select "full_access" (top checkbox)
```

✅ **Click "Create App"**

### STEP 3: Get API Key
After creating the app:
1. You'll see your **API Key** on the app page
2. **Copy this key** and save it safely
3. It looks like: `zudyrwgcegy6o0nw` (random letters/numbers)

### STEP 4: Generate Access Token (THE MAIN PART!)

Now you need to get the **Access Token**. Follow these steps:

#### Option A: Using Browser (Easiest - 2 minutes)

**Run this Python code in your terminal:**

```powershell
cd "D:\visual studio\Module and packages\kite"
python
```

Then paste this code in Python:

```python
from kiteconnect import KiteConnect

API_KEY = "YOUR_API_KEY_HERE"  # Replace with your API Key from Step 3
kite = KiteConnect(api_key=API_KEY)

# Print the login URL
print(kite.login_url())
```

**Output will be like:**
```
https://kite.zerodha.com/connect/login?api_key=zudyrwgcegy6o0nw&v=3
```

#### COPY THIS URL and open it in your browser!

---

### STEP 5: Login in Browser

1. **Paste the URL** in your browser address bar
2. **Sign in** with your Zerodha credentials again
   - Client ID
   - Password
   - OTP from your phone
3. **You'll see a success message** with a code in the URL

The URL will change to something like:
```
http://localhost:8080/?status=success&code=ABCD1234EFGH5678
```

✅ **Copy the CODE** from the URL (the long random string after `code=`)

---

### STEP 6: Get ACCESS_TOKEN using the Code

Still in Python, run this:

```python
# Get your Access Token
code = "YOUR_CODE_HERE"  # Replace with the code from Step 5
secret = "YOUR_APP_SECRET_HERE"  # From app settings at developers.kite.trade

try:
    data = kite.request_access_token(code=code, secret=secret)
    access_token = data['access_token']
    print(f"Your Access Token: {access_token}")
    
except Exception as e:
    print(f"Error: {e}")
    print("Check your code and secret are correct")
```

✅ **You got your ACCESS_TOKEN!**

---

### STEP 7: Save in .env File

Create a file named `.env` in the kite folder:

```
D:\visual studio\Module and packages\kite\.env
```

Add this content:

```
KITE_API_KEY=zudyrwgcegy6o0nw
KITE_ACCESS_TOKEN=your_long_access_token_here
```

**Replace the values with YOUR actual credentials!**

---

## 🔍 Where to Find App Secret?

1. Go to: https://developers.kite.trade/
2. Click on your app name
3. Scroll down - you'll see **"App Secret"** (looks like: `abcdef123456`)
4. Copy it for Step 6

---

## ⚡ Quick Reference Command

Run this full Python script to automate the process:

```python
#!/usr/bin/env python3
from kiteconnect import KiteConnect

print("="*60)
print("ZERODHA KITE ACCESS TOKEN GENERATOR")
print("="*60)

# Step 1: Get API Key
API_KEY = input("\nEnter your API Key: ").strip()

# Step 2: Create Kite connection
kite = KiteConnect(api_key=API_KEY)

# Step 3: Get login URL
login_url = kite.login_url()
print(f"\n[1] Open this URL in browser:\n{login_url}")

# Step 4: User logs in and gets code
input("\n[2] Press ENTER after you've logged in and copied the code from URL...")
code = input("[3] Paste the code from URL here: ").strip()

# Step 5: Get app secret
app_secret = input("[4] Enter your App Secret: ").strip()

# Step 6: Get access token
try:
    data = kite.request_access_token(code=code, secret=app_secret)
    access_token = data['access_token']
    
    print("\n" + "="*60)
    print("[SUCCESS] Got your Access Token!")
    print("="*60)
    print(f"\nAPI_KEY: {API_KEY}")
    print(f"ACCESS_TOKEN: {access_token}")
    print("\nAdd these to your .env file:")
    print(f"KITE_API_KEY={API_KEY}")
    print(f"KITE_ACCESS_TOKEN={access_token}")
    
except Exception as e:
    print(f"\n[ERROR] Failed to get access token: {e}")
    print("Possible reasons:")
    print("- Code already used (generate new login)")
    print("- Wrong app secret")
    print("- Code expired (take less than 10 mins)")
```

Save this as `get_token.py` and run:
```powershell
python get_token.py
```

---

## 🚨 Common Errors & Solutions

| Error | Solution |
|-------|----------|
| "Invalid code" | Code expired or already used. Login again |
| "Invalid API Key" | Check API key spelling, copy from app settings |
| "Invalid secret" | App Secret from app page at developers.kite.trade |
| "Connection refused" | Make sure kiteconnect is installed |
| "Empty access token" | Code or secret is wrong |

---

## 🔐 Security Tips

✅ **DO:**
- Keep API Key & Access Token SECRET
- Store in `.env` file (never in GitHub)
- Regenerate tokens monthly
- Use separate Zerodha account for bots

❌ **DON'T:**
- Share tokens with anyone
- Hardcode in your code
- Post in forums/Discord
- Use production account for testing

---

## ✅ Verification

After getting the token, verify it works:

```python
from kiteconnect import KiteConnect

kite = KiteConnect(api_key="YOUR_API_KEY")
kite.set_access_token("YOUR_ACCESS_TOKEN")

# Try to get your profile
try:
    profile = kite.profile()
    print(f"Success! Logged in as: {profile['email']}")
except:
    print("Token invalid - regenerate it")
```

---

## 📞 Still Have Issues?

**Zerodha Support:**
- Website: https://support.zerodha.com/
- Live Chat: Available on Zerodha website
- Email: support@zerodha.com
- Phone: 1800-114-414-414

**API Documentation:**
- Kite API Docs: https://kite.trade/docs/connect/v3/
- Forum: https://forum.kite.trade/

---

## Summary

```
1. Go to developers.kite.trade
2. Create app → Get API Key
3. Run KiteConnect to get login URL
4. Login in browser → Copy code from URL
5. Use code + app secret to get ACCESS_TOKEN
6. Save both in .env file
7. DONE! 🎉
```

Your bot is now ready to trade!

