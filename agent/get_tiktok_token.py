#!/usr/bin/env python3
"""
TikTok OAuth Token Exchange Script
Run this from your terminal: python get_tiktok_token.py

After running, it will create/update the .env file with your TikTok credentials.
"""

import urllib.request
import urllib.parse
import json
import os

# ── Sandbox credentials ──────────────────────────────────────────────────────
CLIENT_KEY    = "sbawma7wku9xpvc1g0"
CLIENT_SECRET = "6WTGAYaVoKKdpdwvW4SEnGcuesiEo93K"
REDIRECT_URI  = "https://novumediaco.ca"

# ── Paste the code from the URL here ─────────────────────────────────────────
# After visiting the OAuth URL and authorizing, copy the ?code=XXXX value here
CODE = input("Paste the TikTok authorization code from the URL: ").strip()

print("\nExchanging code for access token...")

data = urllib.parse.urlencode({
    "client_key":    CLIENT_KEY,
    "client_secret": CLIENT_SECRET,
    "code":          CODE,
    "grant_type":    "authorization_code",
    "redirect_uri":  REDIRECT_URI,
}).encode()

req = urllib.request.Request(
    "https://open.tiktokapis.com/v2/oauth/token/",
    data=data,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
except Exception as e:
    print(f"❌ Request failed: {e}")
    exit(1)

print("Response:", json.dumps(result, indent=2))

if "access_token" not in result:
    print("❌ No access token in response. Check if code expired and re-authorize.")
    exit(1)

access_token = result["access_token"]
open_id      = result["open_id"]

print(f"\n✅ Access token: {access_token[:30]}...")
print(f"✅ Open ID:      {open_id}")

# ── Write .env file ───────────────────────────────────────────────────────────
env_path = os.path.join(os.path.dirname(__file__), ".env")
env_content = f"""# TikTok credentials (Sandbox)
TIKTOK_ACCESS_TOKEN={access_token}
TIKTOK_OPEN_ID={open_id}

# Meta/Instagram credentials (add after Meta setup)
INSTAGRAM_ACCOUNT_ID=
META_ACCESS_TOKEN=
"""

with open(env_path, "w") as f:
    f.write(env_content)

print(f"\n✅ .env file written to: {env_path}")
print("\nYou can now run: python post_tiktok.py --info")
