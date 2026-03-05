# How to Enable Quote Permissions in Zerodha

If you're getting "Insufficient permission for that call" error, you need to enable quote data permissions.

## Method 1: Zerodha Console (Recommended)

### Step 1: Go to Zerodha Console
- Open: https://console.zerodha.com/
- Login with your Zerodha trading account (same username/password as Kite)

### Step 2: Navigate to Apps
In the left sidebar, look for:
- **"Apps"** → **"My Apps"** 
- OR **"Integrations"** → **"Connected Apps"**

### Step 3: Find Your App
You should see your app listed with:
- **App Name**: Your circuit breaker bot or app name
- **API Key**: `zudyrwgcegy6o0nw` (the one you're using)

Click on it to open the app settings.

### Step 4: Enable Permissions
Look for a **"Permissions"**, **"Scopes"**, or **"Features"** tab.

Enable these permissions:
- ✅ **quote** - To get stock price quotes
- ✅ **order** - To place buy/sell orders  
- ✅ **portfolio** - To check account balance

Then click **"Save"** or **"Update"**

---

## Method 2: Kite App Settings

### Step 1: Open Kite
- Go to: https://kite.zerodha.com/
- OR open Kite mobile app
- Login if needed

### Step 2: Open Settings
- Click on your **Profile icon** (usually top-right corner with your name)
- Select **"Settings"**

### Step 3: Find API Section
- Look for **"API" section** or **"Connected Apps"**
- Click on your app

### Step 4: Check/Enable Permissions
- Make sure **Quote** or **Live Data** is enabled
- Click **"Save"** if you made changes

---

## Method 3: Account Permissions Page

Sometimes quote access is linked to account-level settings:

### Step 1: Zerodha Account Page
- Go to: https://account.zerodha.com/
- Login if needed

### Step 2: Look for API/Data Permissions
- Find **"API"** or **"Data Access"** section
- Check if **"Live data access"** is **"Enabled"**

### Step 3: Subscribe to Market Data (if needed)
- Some accounts require a subscription to live data
- Look for **"Market Data Subscription"** option
- Enable/Subscribe if available

---

## Common Issues & Solutions

### Issue: "Insufficient permission for that call"

**Cause 1: Quote permission not enabled**
- Solution: Follow steps above to enable quote permission

**Cause 2: Account restriction**
- Solution: Some demo/test accounts don't have quote access
- Try: Create a new app or check if your account is restricted

**Cause 3: Token expired**
- Solution: Regenerate access token (tokens expire in ~24 hours)
- Run: `python get_access_token.py`

**Cause 4: API Key mismatch**
- Check that you're using the correct API key
- Verify in .env file: `KITE_API_KEY=zudyrwgcegy6o0nw`

---

## Verification Steps

After enabling permissions, verify by running:

```powershell
cd "d:\visual studio\Module and packages\kite"
python -c "
from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

load_dotenv()
kite = KiteConnect(
    api_key=os.getenv('KITE_API_KEY'),
    access_token=os.getenv('KITE_ACCESS_TOKEN')
)

try:
    quote = kite.quote(['HDFCBANK:NSE'])
    print('SUCCESS! Quote access working!')
    print(f'Stock: {quote}')
except Exception as e:
    print(f'ERROR: {e}')
"
```

If you see "SUCCESS!", your permissions are enabled!

---

## Still Having Issues?

If permissions are enabled but still getting errors:

1. **Regenerate Access Token** (tokens expire in ~24 hours):
   ```powershell
   python get_access_token.py
   ```

2. **Restart the bot**:
   ```powershell
   python bot_demo.py
   ```

3. **Wait 5 minutes** - Sometimes permissions take a few minutes to apply

4. **Check Zerodha Support**:
   - Visit: https://support.zerodha.com/
   - Contact them with your API key if still having issues

---

## Contact Zerodha Support

If you can't find these settings, reach out to Zerodha:
- **Email**: support@zerodha.com
- **Support Portal**: https://support.zerodha.com/
- **Phone**: Check Zerodha website for support number

Tell them:
- You need to enable **"quote"** permission for your API app
- Provide your **API Key**: `zudyrwgcegy6o0nw`
