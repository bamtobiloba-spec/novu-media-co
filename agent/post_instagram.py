"""
Novu Media Co. — Instagram Auto-Poster
Posts images and videos to Instagram via Meta Graph API.

SETUP REQUIRED (one-time):
1. Go to https://developers.facebook.com/ and create an app
2. Add "Instagram Graph API" product to your app
3. Connect your Instagram Business Account to a Facebook Page
4. Generate a long-lived User Access Token with these permissions:
   - instagram_basic
   - instagram_content_publish
   - pages_read_engagement
5. Find your Instagram Business Account ID (Settings → About → Account ID)
6. Fill in the config below or set environment variables

Usage:
    python post_instagram.py --image path/to/image.jpg --caption "Your caption"
    python post_instagram.py --video path/to/video.mp4 --caption "Your Reel caption"
    python post_instagram.py --today   # Auto-post today's content brief
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
# Option 1: Fill these in directly
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", "YOUR_INSTAGRAM_ACCOUNT_ID")
META_ACCESS_TOKEN     = os.environ.get("META_ACCESS_TOKEN", "YOUR_META_ACCESS_TOKEN")

# Option 2: Set these as environment variables (recommended for security):
#   set INSTAGRAM_ACCOUNT_ID=123456789
#   set META_ACCESS_TOKEN=EAAxxxx...
#
# Or create a .env file in this folder:
#   INSTAGRAM_ACCOUNT_ID=123456789
#   META_ACCESS_TOKEN=EAAxxxx...

BASE_URL = "https://graph.facebook.com/v18.0"

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
    global INSTAGRAM_ACCOUNT_ID, META_ACCESS_TOKEN
    load_env()
    INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", INSTAGRAM_ACCOUNT_ID)
    META_ACCESS_TOKEN     = os.environ.get("META_ACCESS_TOKEN", META_ACCESS_TOKEN)

    if "YOUR_" in INSTAGRAM_ACCOUNT_ID or "YOUR_" in META_ACCESS_TOKEN:
        print("\n❌ ERROR: Meta API credentials not configured.")
        print("\nTo set up:")
        print("1. Go to https://developers.facebook.com/ → Create App")
        print("2. Add 'Instagram Graph API' product")
        print("3. Connect Instagram Business Account to Facebook Page")
        print("4. Generate access token with instagram_content_publish permission")
        print("5. Find your Instagram Account ID (Settings → About → Account ID)")
        print("\nThen set environment variables:")
        print("   set INSTAGRAM_ACCOUNT_ID=your_account_id")
        print("   set META_ACCESS_TOKEN=your_token")
        print("\nOr create agent/.env file with those two values.")
        sys.exit(1)


def upload_image_to_hosting(image_path):
    """
    Instagram requires a PUBLIC URL for images — local files won't work directly.
    This function uploads to a temporary hosting service (file.io) for demo purposes.

    For production: use your own server, AWS S3, or Cloudinary.
    """
    print(f"📤 Uploading image to temporary host...")
    with open(image_path, "rb") as f:
        response = requests.post(
            "https://file.io",
            files={"file": f},
            data={"expires": "1d"}
        )
    if response.status_code == 200:
        url = response.json().get("link")
        print(f"✅ Image hosted at: {url}")
        return url
    else:
        raise Exception(f"Failed to upload image: {response.text}")


# ─── POSTING FUNCTIONS ────────────────────────────────────────────────────────
def create_image_container(image_url, caption):
    """Step 1: Create a media container for an image post."""
    url = f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media"
    params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": META_ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    data = response.json()

    if "id" not in data:
        raise Exception(f"Failed to create container: {data}")

    container_id = data["id"]
    print(f"✅ Media container created: {container_id}")
    return container_id


def create_video_container(video_url, caption, is_reel=True):
    """Step 1: Create a media container for a video / Reel."""
    url = f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media"
    params = {
        "video_url": video_url,
        "caption": caption,
        "media_type": "REELS" if is_reel else "VIDEO",
        "share_to_feed": "true",
        "access_token": META_ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    data = response.json()

    if "id" not in data:
        raise Exception(f"Failed to create video container: {data}")

    container_id = data["id"]
    print(f"✅ Video container created: {container_id}")
    return container_id


def wait_for_container(container_id, max_wait=120):
    """Poll until video container is ready (videos take time to process)."""
    print("⏳ Waiting for media to process...")
    url = f"{BASE_URL}/{container_id}"
    params = {"fields": "status_code,status", "access_token": META_ACCESS_TOKEN}

    for attempt in range(max_wait // 5):
        time.sleep(5)
        response = requests.get(url, params=params)
        data = response.json()
        status = data.get("status_code", data.get("status", "UNKNOWN"))

        if status == "FINISHED":
            print("✅ Media processed successfully")
            return True
        elif status in ("ERROR", "EXPIRED"):
            raise Exception(f"Media processing failed: {data}")

        print(f"   Status: {status} (attempt {attempt + 1})")

    raise Exception(f"Timed out waiting for container {container_id}")


def publish_container(container_id):
    """Step 2: Publish the container to Instagram."""
    url = f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    params = {
        "creation_id": container_id,
        "access_token": META_ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    data = response.json()

    if "id" not in data:
        raise Exception(f"Failed to publish: {data}")

    post_id = data["id"]
    print(f"🎉 Published! Post ID: {post_id}")
    print(f"   View at: https://www.instagram.com/p/{post_id}/")
    return post_id


def post_image(image_path_or_url, caption):
    """Post a single image to Instagram."""
    check_config()
    print(f"\n📸 Posting image to Instagram...")

    # If it's a local file, upload it to get a public URL
    if os.path.isfile(image_path_or_url):
        image_url = upload_image_to_hosting(image_path_or_url)
    else:
        image_url = image_path_or_url  # Already a public URL

    container_id = create_image_container(image_url, caption)
    post_id = publish_container(container_id)
    return post_id


def post_reel(video_path_or_url, caption):
    """Post a Reel to Instagram."""
    check_config()
    print(f"\n🎬 Posting Reel to Instagram...")

    if os.path.isfile(video_path_or_url):
        print("⚠️  For videos, you need a PUBLIC URL. Please host your video on:")
        print("   - Your web server (novumediaco.ca/videos/)")
        print("   - AWS S3 / Google Cloud Storage")
        print("   - Cloudinary (free tier available)")
        print(f"\n   Local path provided: {video_path_or_url}")
        sys.exit(1)

    container_id = create_video_container(video_path_or_url, caption)
    wait_for_container(container_id)
    post_id = publish_container(container_id)
    return post_id


def post_today_brief():
    """Auto-generate and post today's content from the 30-day plan."""
    # Import the content agent
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

    if "Instagram" not in brief["platforms"]:
        print(f"ℹ️  Day {day} is TikTok-only content. No Instagram post today.")
        return

    print(f"\n📋 Today is Day {day}: {brief['title']}")
    caption = brief["caption"] + "\n\n" + " ".join(brief["hashtags"])

    # Look for today's image/video in the media folder
    media_dir = agent_dir.parent / "media"
    image_files = list(media_dir.glob(f"day{day:02d}_*.jpg")) + list(media_dir.glob(f"day{day:02d}_*.png"))
    video_files = list(media_dir.glob(f"day{day:02d}_*.mp4"))

    if video_files:
        print(f"📹 Found video: {video_files[0].name}")
        print("ℹ️  To post a Reel, provide the public URL of this video.")
        print(f"   Upload it to your server and run:")
        print(f"   python post_instagram.py --video https://novumediaco.ca/videos/{video_files[0].name} --caption [auto]")
    elif image_files:
        print(f"🖼️  Found image: {image_files[0].name}")
        post_image(str(image_files[0]), caption)
    else:
        print(f"\n⚠️  No media found for Day {day} in: {media_dir}")
        print(f"   Expected: day{day:02d}_*.jpg, day{day:02d}_*.png, or day{day:02d}_*.mp4")
        print(f"\n   Caption is ready to post manually:")
        print("-" * 50)
        print(caption)
        print("-" * 50)


def get_account_info():
    """Fetch basic account info to verify credentials."""
    check_config()
    url = f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}"
    params = {
        "fields": "id,username,followers_count,media_count",
        "access_token": META_ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        print(f"❌ API Error: {data['error']['message']}")
        return

    print("\n✅ Connected to Instagram!")
    print(f"   Username:  @{data.get('username', 'N/A')}")
    print(f"   Followers: {data.get('followers_count', 'N/A'):,}")
    print(f"   Posts:     {data.get('media_count', 'N/A')}")


# ─── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Novu Media Co. Instagram Poster")
    parser.add_argument("--image",   help="Path or URL to image file")
    parser.add_argument("--video",   help="Public URL to video/Reel file")
    parser.add_argument("--caption", help="Post caption (use 'auto' to generate from 30-day plan)")
    parser.add_argument("--today",   action="store_true", help="Auto-post today's content brief")
    parser.add_argument("--info",    action="store_true", help="Show account info (test credentials)")
    args = parser.parse_args()

    if args.info:
        get_account_info()
    elif args.today:
        post_today_brief()
    elif args.image:
        if not args.caption:
            print("❌ Please provide --caption")
            sys.exit(1)
        check_config()
        post_image(args.image, args.caption)
    elif args.video:
        if not args.caption:
            print("❌ Please provide --caption")
            sys.exit(1)
        check_config()
        post_reel(args.video, args.caption)
    else:
        parser.print_help()
