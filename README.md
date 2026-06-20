# Novu Media Co.

Canadian digital marketing agency helping small businesses grow through social media.

**Website:** [novumediaco.ca](https://novumediaco.ca)

---

## What's in this repo

| Folder / File | Description |
|---|---|
| `agent/` | Social media automation scripts |
| `agent/post_tiktok.py` | Auto-post videos to TikTok via API |
| `agent/post_instagram.py` | Auto-post to Instagram via Meta API |
| `agent/content_agent.py` | 30-day content plan generator |
| `agent/get_tiktok_token.py` | TikTok OAuth token exchange helper |
| `daily_briefs/` | Auto-generated daily content briefs |
| `index.html` | Main website |
| `services.html` | Services page |
| `pricing.html` | Pricing page |
| `about.html` | About page |
| `contact.html` | Contact page |

---

## Setup

### TikTok Auto-Posting

1. Run OAuth flow: `python agent/get_tiktok_token.py`
2. Follow the prompts — creates `agent/.env` with your token
3. Test: `python agent/post_tiktok.py --info`
4. Post a video: `python agent/post_tiktok.py --video path/to/video.mp4 --caption "Your caption #hashtags"`

### Requirements

```bash
pip install requests
```

---

## Content Strategy

30-day content plan across TikTok and Instagram covering:
- Educational tips
- Behind-the-scenes
- Promotional content
- Client success stories

---

*Built by Toby Bamigboye — Novu Media Co.*
