# Novu Media Co. — Social Media Agent

Automated content generation and posting for Instagram and TikTok.

---

## What's in this folder

| File | What it does |
|------|--------------|
| `content_agent.py` | Generates daily captions, hashtags, video scripts based on the 30-day plan |
| `post_instagram.py` | Posts images and Reels to Instagram via Meta Graph API |
| `post_tiktok.py` | Posts videos to TikTok via Content Publishing API |
| `.env` | Your API credentials (create this — see setup below) |

---

## Quick Start

### 1. Generate today's content brief
```
python content_agent.py --save
```
Saves a brief to: `../daily_briefs/`

### 2. See all 30 days
```
python content_agent.py --day 5
```
Replace `5` with any day number (1–30).

---

## Setting Up Auto-Posting

### Instagram Setup
1. Go to **https://developers.facebook.com/** → Create App
2. Add **Instagram Graph API** product
3. Connect your Instagram Business Account to a Facebook Page
4. Generate a **long-lived User Access Token** with permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
5. Find your **Instagram Account ID**:
   - Go to Instagram → Settings → About → Account ID
   - Or use: `https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_TOKEN`

### TikTok Setup
1. Go to **https://developers.tiktok.com/** → Create App
2. Add **Content Posting API** product
3. Enable scope: `video.publish`
4. Complete OAuth 2.0 flow to get your Access Token and Open ID

### Create your .env file
Create a file called `.env` in this folder with:
```
INSTAGRAM_ACCOUNT_ID=123456789012345
META_ACCESS_TOKEN=EAAxxxxxxxxxx...
TIKTOK_ACCESS_TOKEN=act.xxxxxxxx...
TIKTOK_OPEN_ID=xxxxxxxxxxxxxxxx
```

### Test your credentials
```
python post_instagram.py --info
python post_tiktok.py --info
```

---

## Auto-Posting Commands

### Post today's content automatically
```
python post_instagram.py --today
python post_tiktok.py --today
```

### Post a specific image to Instagram
```
python post_instagram.py --image path/to/photo.jpg --caption "Your caption here"
```

### Post a specific video to TikTok
```
python post_tiktok.py --video path/to/video.mp4 --caption "Your caption #hashtag"
```

---

## Media File Naming Convention

Name your media files to match the day number so the agent finds them automatically:
```
media/day01_intro_video.mp4
media/day02_carousel_cover.jpg
media/day03_reel.mp4
...
```

---

## Scheduled Agent

The **daily agent** runs automatically every morning at 8:00 AM.
It generates today's brief and attempts to auto-post if media files are ready.

You can also run it manually from the Claude Scheduled Tasks sidebar.

---

## 30-Day Plan Summary

| Week | Theme | Days |
|------|-------|------|
| Week 1 | Launch & Introduce | 1–7 |
| Week 2 | Educate & Build Trust | 8–14 |
| Week 3 | Social Proof & Engagement | 15–21 |
| Week 4 | Convert & Close | 22–30 |

Launch date: **June 16, 2026**
