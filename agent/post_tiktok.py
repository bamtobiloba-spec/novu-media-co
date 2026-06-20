"""
Novu Media Co. — TikTok Auto-Poster
Posts videos to TikTok via the Content Publishing API.

SETUP REQUIRED (one-time):
1. Go to https://developers.tiktok.com/ → Create an app
2. Add "Content Posting API" product
3. Enable scope: video.publish
4. Complete OAuth 2.0 flow to get your ACCESS TOKEN
5. Fill in the config below or use environment variables

TikTok API Notes:
- Videos must be .mp4, max 4GB, 3 seconds to 10 minutes
- The API uses a 2-step process: Initialize Upload → Upload File → Publish
- Direct post (auto-publish without TikTok review) requires approval from TikTok

Usage:
    python post_tiktok.py --video path/to/video.mp4 --caption "Your caption #hashtag"
    python post_tiktok.py --today   # Auto-post today's content
    python post_tiktok.py --info    # Test your credentials
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
TIKTOK_ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN", "YOUR_TIKTOK_ACCESS_TOKEN")
TIKTOK_OPEN_ID      = os.environ.get("TIKTOK_OPEN_ID", "YOUR_TIKTOK_OPEN_ID")  # Your TikTok user ID

BASE_URL = "https://open.tiktokapis.com/v2"

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def load_env():
    """Load .env file if present."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


def check_config():
    """Verify credentials are set."""
    global TIKTOK_ACCESS_TOKEN, TIKTOK_OPEN_ID
    load_env()
    TIKTOK_ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN", TIKTOK_ACCESS_TOKEN)
    TIKTOK_OPEN_ID      = os.environ.get("TIKTOK_OPEN_ID", TIKTOK_OPEN_ID)

    if "YOUR_" in TIKTOK_ACCESS_TOKEN:
        print("\n❌ ERROR: TikTok API credentials not configured.")
        print("\nTo set up:")
        print("1. Go to https://developers.tiktok.com/ → Create an app")
        print("2. Add 'Content Posting API' to your app")
        print("3. Enable scope: video.publish")
        print("4. Complete OAuth flow to get your access token")
        print("5. Your OPEN_ID is returned in the OAuth response")
        print("\nThen set environment variables:")
        print("   set TIKTOK_ACCESS_TOKEN=your_token")
        print("   set TIKTOK_OPEN_ID=your_open_id")
        print("\nOr create agent/.env file with those two values.")
        print("\nAlternative: TikTok Creator Studio at https://creatormarketplace.tiktok.com")
        print("allows scheduling posts without the API.")
        sys.exit(1)


def headers():
    return {
        "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }


# ─── POSTING FUNCTIONS ────────────────────────────────────────────────────────
def get_creator_info():
    """Fetch user info to verify credentials (works with sandbox user.info.basic scope)."""
    check_config()

    # Try user info endpoint first (works in sandbox with user.info.basic scope)
    fields = "open_id,display_name,avatar_url"
    url = f"{BASE_URL}/user/info/?fields={fields}"
    response = requests.get(url, headers=headers())
    data = response.json()

    if data.get("error", {}).get("code") == "ok":
        info = data.get("data", {}).get("user", {})
        print("\n✅ Connected to TikTok!")
        print(f"   Display name: {info.get('display_name', 'N/A')}")
        print(f"   Open ID:      {info.get('open_id', 'N/A')}")
        return info

    error_msg = data.get("error", {}).get("message", "Unknown")
    error_code = data.get("error", {}).get("code", "Unknown")
    print(f"\n❌ TikTok API Error [{error_code}]: {error_msg}")
    return None


def initialize_upload(video_path, chunk_size=None):
    """Step 1: Tell TikTok we want to upload a video. Get upload URL."""
    check_config()
    video_size = os.path.getsize(video_path)
    video_size_mb = video_size / (1024 * 1024)
    print(f"📹 Video size: {video_size_mb:.1f} MB")

    # For files under 64MB, use PULL_FROM_URL or FILE_UPLOAD
    # We'll use FILE_UPLOAD for local files
    url = f"{BASE_URL}/post/publish/video/init/"
    payload = {
        "post_info": {
            "title": "",         # Will be set in publish step
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": video_size,      # Single chunk for simplicity
            "total_chunk_count": 1
        }
    }

    response = requests.post(url, headers=headers(), json=payload)
    data = response.json()

    if data.get("error", {}).get("code") != "ok":
        raise Exception(f"Upload init failed: {data.get('error', {}).get('message')}")

    upload_url    = data["data"]["upload_url"]
    publish_id    = data["data"]["publish_id"]
    print(f"✅ Upload initialized. Publish ID: {publish_id}")
    return upload_url, publish_id


def upload_video_chunk(upload_url, video_path):
    """Step 2: Upload the video file."""
    video_size = os.path.getsize(video_path)
    print(f"⬆️  Uploading video...")

    with open(video_path, "rb") as f:
        video_data = f.read()

    upload_headers = {
        "Content-Type": "video/mp4",
        "Content-Range": f"bytes 0-{video_size - 1}/{video_size}",
        "Content-Length": str(video_size)
    }
    response = requests.put(upload_url, headers=upload_headers, data=video_data)

    if response.status_code not in (200, 201, 206):
        raise Exception(f"Upload failed: {response.status_code} {response.text}")

    print("✅ Video uploaded successfully")
    return True


def check_publish_status(publish_id, max_wait=300):
    """Step 3: Poll until video is processed and published."""
    print("⏳ Waiting for TikTok to process video...")
    url = f"{BASE_URL}/post/publish/status/fetch/"
    payload = {"publish_id": publish_id}

    for attempt in range(max_wait // 5):
        time.sleep(5)
        response = requests.post(url, headers=headers(), json=payload)
        data = response.json()

        status = data.get("data", {}).get("status", "UNKNOWN")
        print(f"   Status: {status} (attempt {attempt + 1})")

        if status == "PUBLISH_COMPLETE":
            print("🎉 Video published to TikTok!")
            return True
        elif status in ("FAILED", "SPAM_RISK_TOO_MANY_POSTS"):
            raise Exception(f"Publishing failed: {status}")

    raise Exception(f"Timed out after {max_wait} seconds")


def post_video(video_path, caption, privacy="PUBLIC_TO_EVERYONE"):
    """Full pipeline: initialize → upload → verify → publish."""
    check_config()

    if not os.path.isfile(video_path):
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)

    ext = Path(video_path).suffix.lower()
    if ext not in (".mp4", ".mov", ".webm"):
        print(f"❌ Unsupported format: {ext}. Use .mp4, .mov, or .webm")
        sys.exit(1)

    print(f"\n🎵 Posting video to TikTok...")
    print(f"   File: {Path(video_path).name}")
    print(f"   Caption: {caption[:50]}...")

    # Initialize upload
    upload_url, publish_id = initialize_upload(video_path)

    # Upload the video file
    upload_video_chunk(upload_url, video_path)

    # Poll for completion
    check_publish_status(publish_id)

    print(f"\n✅ TikTok post complete!")
    print(f"   Caption: {caption[:60]}...")
    print(f"   View at: https://www.tiktok.com/@novumediaco")
    return publish_id


def post_today_brief():
    """Auto-generate and post today's content from the 30-day plan."""
    agent_dir = Path(__file__).parent
    sys.path.insert(0, str(agent_dir))

    try:
        from content_agent import get_day_number, generate_brief
    except ImportError:
        print("❌ content_agent.py not found. Make sure it's in the same folder.")
        sys.exit(1)

    day = get_day_number()
    brief = generate_brief(day)

    if not brief:
        print(f"❌ No content found for day {day}")
        sys.exit(1)

    if "TikTok" not in brief["platforms"]:
        print(f"ℹ️  Day {day} is Instagram-only content. No TikTok post today.")
        return

    print(f"\n📋 Today is Day {day}: {brief['title']}")
    caption = brief["caption"] + "\n\n" + " ".join(brief.get("hashtags", []))

    # Look for today's video in media folder
    media_dir = agent_dir.parent / "media"
    video_files = list(media_dir.glob(f"day{day:02d}_*.mp4")) + list(media_dir.glob(f"day{day:02d}_*.mov"))

    if video_files:
        print(f"📹 Found video: {video_files[0].name}")
        post_video(str(video_files[0]), caption)
    else:
        print(f"\n⚠️  No video found for Day {day} in: {media_dir}")
        print(f"   Expected: day{day:02d}_*.mp4 or day{day:02d}_*.mov")
        print(f"\n   Caption ready to post manually:")
        print("-" * 50)
        print(caption)
        print("-" * 50)
        if brief.get("video_script"):
            print(f"\n🎬 Script for today's video:")
            print(brief["video_script"])


# ─── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Novu Media Co. TikTok Poster")
    parser.add_argument("--video",   help="Path to video file (.mp4 or .mov)")
    parser.add_argument("--caption", help="Post caption + hashtags")
    parser.add_argument("--today",   action="store_true", help="Auto-post today's content brief")
    parser.add_argument("--info",    action="store_true", help="Show account info (test credentials)")
    args = parser.parse_args()

    if args.info:
        check_config()
        get_creator_info()
    elif args.today:
        post_today_brief()
    elif args.video:
        if not args.caption:
            print("❌ Please provide --caption")
            sys.exit(1)
        check_config()
        post_video(args.video, args.caption)
    else:
        parser.print_help()
