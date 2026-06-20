"""
Novu Media Co. — Social Media Content Agent
Generates daily captions, hashtags, and post briefs based on the 30-day plan.
Run: python content_agent.py [--day N]
"""

import json
import os
import sys
import argparse
from datetime import datetime, date

# ─── LAUNCH DATE ─────────────────────────────────────────────────────────────
# Set this to the date you want Day 1 to be (YYYY, M, D)
LAUNCH_DATE = date(2026, 6, 16)

# ─── 30-DAY CONTENT PLAN ─────────────────────────────────────────────────────
THIRTY_DAY_PLAN = {
    1:  {
        "week": "WEEK 1: LAUNCH & INTRODUCE",
        "platforms": ["Instagram", "TikTok"],
        "format": "Intro Video",
        "title": "We just launched! Here's what Novu Media Co. does",
        "caption": (
            "🚀 We're LIVE.\n\n"
            "Novu Media Co. is a Canadian digital marketing agency helping small businesses "
            "grow online through social media, paid ads, content creation, and brand strategy.\n\n"
            "Whether you're a local business trying to get noticed or an e-commerce brand "
            "ready to scale — we build the strategy, create the content, and run the campaigns. 🎯\n\n"
            "Visit us → novumediaco.ca\n\n"
            "#NovuMediaCo #DigitalMarketing #MarketingAgency #SocialMediaMarketing "
            "#CanadianMarketing #BusinessGrowth #ContentStrategy #BrandStrategy"
        ),
        "video_script": (
            "HOOK: 'We just launched a digital marketing agency in Canada — and here's exactly what we do.'\n"
            "BODY: Introduce Novu Media Co., show website, explain 6 services in 30 seconds.\n"
            "CTA: 'Check the link in our bio — we're taking on new clients this month.'"
        ),
        "notes": "Film a talking-head intro video. Show your website on screen. Keep it under 60 seconds."
    },
    2:  {
        "week": "WEEK 1: LAUNCH & INTRODUCE",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "5 signs your business needs a social media agency",
        "caption": (
            "📊 5 signs your business NEEDS a social media agency:\n\n"
            "1️⃣ You're posting but getting zero engagement\n"
            "2️⃣ You don't have time to stay consistent\n"
            "3️⃣ You have no idea what's actually working\n"
            "4️⃣ Your competitors are growing faster than you\n"
            "5️⃣ You've tried everything and nothing sticks\n\n"
            "Sound familiar? Save this post 👆 and DM us — let's fix it.\n\n"
            "#SocialMediaAgency #DigitalMarketing #SmallBusiness #InstagramGrowth "
            "#MarketingTips #NovuMediaCo #BusinessOwner #SocialMediaStrategy"
        ),
        "video_script": None,
        "notes": "Create a 5-slide carousel. Slide 1: hook. Slides 2-6: one sign per slide. Final slide: CTA."
    },
    3:  {
        "week": "WEEK 1: LAUNCH & INTRODUCE",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "The #1 mistake small businesses make on Instagram",
        "caption": (
            "❌ The #1 Instagram mistake killing small businesses — and it's NOT what you think.\n\n"
            "Most businesses post content... and wait. 🫠\n\n"
            "That's the mistake.\n\n"
            "Instagram is NOT a billboard. It's a CONVERSATION.\n\n"
            "Here's what actually works:\n"
            "✅ Reply to every comment within the first hour\n"
            "✅ Engage with your ideal clients BEFORE you post\n"
            "✅ Use stories to drive people back to your feed\n\n"
            "The algorithm rewards accounts that ENGAGE — not just post.\n\n"
            "Follow us for more tips that actually work. 🚀\n\n"
            "#InstagramTips #SocialMediaMarketing #InstagramAlgorithm #DigitalMarketing "
            "#NovuMediaCo #MarketingAgency #ContentCreator #BusinessGrowth"
        ),
        "video_script": (
            "HOOK: 'The #1 Instagram mistake killing small businesses — and it's not what you think.'\n"
            "BODY: 'Most businesses post and wait. Instagram is a conversation, not a billboard. "
            "Reply to comments within 1 hour, engage with your ideal clients before posting, "
            "use stories to drive back to feed.'\n"
            "CTA: 'Follow for more marketing tips that actually work.'"
        ),
        "notes": "Hook must be the first 3 seconds. Use text on screen. Fast-paced cuts. 30-45 seconds max."
    },
    4:  {
        "week": "WEEK 1: LAUNCH & INTRODUCE",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "What we do at Novu Media Co. — our 6 services",
        "caption": (
            "🛠 What exactly does Novu Media Co. do?\n\n"
            "We're a full-service digital marketing agency offering:\n\n"
            "📱 Social Media Management\n"
            "🎬 Content Creation\n"
            "💰 Paid Advertising (Meta + Google)\n"
            "🏆 Brand Strategy\n"
            "⭐ Reputation Management\n"
            "📧 Email & Lead Generation\n\n"
            "Whether you need one service or all six — we've got you. 💪\n\n"
            "Visit novumediaco.ca to see our packages.\n\n"
            "#MarketingAgency #DigitalMarketing #SocialMediaManagement #PaidAds "
            "#BrandStrategy #ContentCreation #NovuMediaCo #CanadaMarketing"
        ),
        "video_script": None,
        "notes": "One service per slide. Use icons and brand colors (cyan/black). Last slide: website URL."
    },
    5:  {
        "week": "WEEK 1: LAUNCH & INTRODUCE",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "How we grew a client's Instagram from 0 to 5K in 30 days",
        "caption": (
            "📈 We grew a client's Instagram from 0 to 5,000 followers in 30 days. Here's how:\n\n"
            "Step 1 → Identified their ideal customer avatar\n"
            "Step 2 → Rebuilt content strategy around 3 pillars\n"
            "Step 3 → Posted 5× per week with optimized captions + trending audio\n"
            "Step 4 → Engaged 30 min/day with target audience\n\n"
            "Result? 5K followers. 3× website traffic. 4 new client inquiries. ✅\n\n"
            "Want the same results for your business?\n"
            "Book a free strategy call → novumediaco.ca\n\n"
            "#InstagramGrowth #SocialMediaResults #MarketingAgency #NovuMediaCo "
            "#SmallBusinessMarketing #ContentStrategy #InstagramMarketing #GrowthHacking"
        ),
        "video_script": (
            "HOOK: 'We took this client from 0 to 5,000 Instagram followers in 30 days. Here's exactly how.'\n"
            "BODY: Walk through the 4 steps with text on screen.\n"
            "CTA: 'Want the same results? DM us or visit novumediaco.ca'"
        ),
        "notes": "Use before/after screenshots if available. Keep under 60 seconds."
    },
    6:  {
        "week": "WEEK 1: LAUNCH & INTRODUCE",
        "platforms": ["Instagram"],
        "format": "Story",
        "title": "Poll + Q&A: What's your biggest social media struggle?",
        "caption": "Stories don't use captions — use interactive stickers.",
        "video_script": None,
        "notes": (
            "Post 3 stories:\n"
            "1. Poll: 'What's your biggest social media struggle?' — options: 'Getting engagement' vs 'Growing followers'\n"
            "2. Q&A sticker: 'Ask us anything about social media'\n"
            "3. Swipe-up/link sticker pointing to novumediaco.ca"
        )
    },
    7:  {
        "week": "WEEK 1: LAUNCH & INTRODUCE",
        "platforms": ["TikTok"],
        "format": "TikTok",
        "title": "POV: It's Monday morning at a digital marketing agency",
        "caption": (
            "POV: Monday morning at a digital marketing agency 🖥️☕\n\n"
            "This is what it actually looks like running Novu Media Co. 👀\n\n"
            "#AgencyLife #MarketingAgency #BehindTheScenes #DigitalMarketing "
            "#NovuMediaCo #ContentCreator #BusinessOwner #DayInTheLife"
        ),
        "video_script": (
            "HOOK: 'POV: It's Monday morning at a digital marketing agency'\n"
            "BODY: Fast montage — morning coffee, opening laptop, reviewing analytics, "
            "creating content, team calls, responding to clients.\n"
            "AUDIO: Use a trending 'morning routine' or 'day in my life' audio.\n"
            "CTA: 'Follow to see behind the scenes of building an agency'"
        ),
        "notes": "Film throughout the day. Quick cuts. Use trending audio. Keep it real and relatable."
    },
    8:  {
        "week": "WEEK 2: EDUCATE & BUILD TRUST",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "3 Instagram Reels hooks that stop the scroll",
        "caption": (
            "🎣 3 Instagram Reels hooks that STOP the scroll:\n\n"
            "1️⃣ 'The #1 mistake [your audience] makes is...'\n"
            "2️⃣ 'Nobody is talking about this but...'\n"
            "3️⃣ 'I went from [X] to [Y] in [timeframe]. Here's how.'\n\n"
            "Save this for your next Reel 👆\n\n"
            "The hook is everything. If you lose them in the first 3 seconds, you've lost them forever.\n\n"
            "#InstagramReels #ContentCreator #ReelsTips #SocialMediaMarketing "
            "#NovuMediaCo #InstagramGrowth #DigitalMarketing #ContentStrategy"
        ),
        "video_script": (
            "HOOK: '3 Instagram Reels hooks that will stop people mid-scroll'\n"
            "BODY: Show each hook as text on screen with example. Fast pace.\n"
            "CTA: 'Save this and use it for your next Reel.'"
        ),
        "notes": "Show the hooks as text overlays. Use your own brand as an example for hook #3."
    },
    9:  {
        "week": "WEEK 2: EDUCATE & BUILD TRUST",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "The Instagram algorithm explained in 5 slides",
        "caption": (
            "🤖 The Instagram algorithm — explained simply:\n\n"
            "Swipe to understand exactly how it works in 2024 👉\n\n"
            "The algorithm isn't your enemy. Once you understand it, it becomes your biggest asset.\n\n"
            "Save this post so you can refer back to it 📌\n\n"
            "Questions? Drop them in the comments 👇\n\n"
            "#InstagramAlgorithm #InstagramTips #SocialMediaMarketing #NovuMediaCo "
            "#DigitalMarketing #InstagramGrowth #ContentStrategy #MarketingTips"
        ),
        "video_script": None,
        "notes": (
            "5 slides:\n"
            "1. 'The algorithm rewards [X]'\n"
            "2. 'Watch time matters most'\n"
            "3. 'Shares > Likes'\n"
            "4. 'Saves signal quality'\n"
            "5. 'Consistency beats virality'"
        )
    },
    10: {
        "week": "WEEK 2: EDUCATE & BUILD TRUST",
        "platforms": ["TikTok"],
        "format": "TikTok",
        "title": "Paid ads vs organic: which is right for your business?",
        "caption": (
            "Paid ads vs organic social media — which one wins? 🥊\n\n"
            "Short answer: BOTH. But here's when to use each...\n\n"
            "Organic = long-term trust and authority\n"
            "Paid ads = fast traffic and targeted leads\n\n"
            "The smartest businesses use both. Start organic, add paid once you have proof of concept.\n\n"
            "#PaidAds #OrganicMarketing #FacebookAds #DigitalMarketing #NovuMediaCo "
            "#MarketingStrategy #MetaAds #SmallBusinessMarketing"
        ),
        "video_script": (
            "HOOK: 'Paid ads vs organic — which one should YOUR business be using?'\n"
            "BODY: Compare both. Organic: slower, builds trust, free. Paid: fast, targeted, costs money.\n"
            "ANSWER: 'Start organic. Add paid when you have a proven offer.'\n"
            "CTA: 'Comment PAID or ORGANIC — which one are you using?'"
        ),
        "notes": "Encourage comments to boost engagement signal."
    },
    11: {
        "week": "WEEK 2: EDUCATE & BUILD TRUST",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "How to write captions that convert",
        "caption": (
            "✍️ How to write Instagram captions that actually convert:\n\n"
            "1. Start with a HOOK (make them stop scrolling)\n"
            "2. Tell a story or share a lesson\n"
            "3. Add value before the ask\n"
            "4. End with ONE clear CTA\n"
            "5. Use line breaks — walls of text get ignored\n\n"
            "Swipe to see before/after examples 👉\n\n"
            "Save this for your next post 📌\n\n"
            "#InstagramCaptions #CopywritingTips #SocialMediaMarketing #NovuMediaCo "
            "#ContentCreator #InstagramTips #DigitalMarketing #MarketingAgency"
        ),
        "video_script": None,
        "notes": "Show a 'bad caption' vs 'good caption' side-by-side on slide 3. Use real examples."
    },
    12: {
        "week": "WEEK 2: EDUCATE & BUILD TRUST",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "Ride a viral trend + marketing tip overlay",
        "caption": (
            "Marketing tip you didn't ask for but definitely needed 👀\n\n"
            "The businesses that WIN on social media aren't always the ones with the best product.\n"
            "They're the ones who show up CONSISTENTLY and tell the best story.\n\n"
            "Start today. Post anyway. Improve as you go. 🚀\n\n"
            "#MarketingTips #SocialMediaMarketing #NovuMediaCo #DigitalMarketing "
            "#BusinessOwner #ContentCreator #Entrepreneurship #GrowthMindset"
        ),
        "video_script": (
            "HOOK: Use a currently trending audio/sound on TikTok/Reels\n"
            "OVERLAY: Add text tip over the trending format\n"
            "TIP TO SHOW: 'Consistency beats talent on social media. Every. Single. Time.'\n"
            "CTA: 'Follow for daily marketing tips'"
        ),
        "notes": "Check TikTok Discover and Instagram Reels trending audio this week. Adapt format to the trend."
    },
    13: {
        "week": "WEEK 2: EDUCATE & BUILD TRUST",
        "platforms": ["Instagram"],
        "format": "Story",
        "title": "Client testimonial + book a free consultation CTA",
        "caption": "Stories don't use captions — use text overlays and stickers.",
        "video_script": None,
        "notes": (
            "Post 2-3 stories:\n"
            "1. Screenshot of a client testimonial (DM, Google review, or email)\n"
            "2. Text: 'This could be you. Book a FREE strategy call this week.'\n"
            "3. Link sticker → novumediaco.ca/contact"
        )
    },
    14: {
        "week": "WEEK 2: EDUCATE & BUILD TRUST",
        "platforms": ["TikTok"],
        "format": "TikTok",
        "title": "Things I wish I knew before starting a marketing agency",
        "caption": (
            "Things I wish I knew before starting a marketing agency 😅\n\n"
            "Nobody tells you this stuff...\n\n"
            "1. Clients need education, not just results\n"
            "2. Systems save you before talent does\n"
            "3. Your niche is your superpower\n"
            "4. Content IS your best salesperson\n"
            "5. Patience is the real strategy\n\n"
            "What would YOU add to this list? Drop it below 👇\n\n"
            "#AgencyLife #MarketingAgency #Entrepreneurship #BusinessLessons "
            "#NovuMediaCo #StartupLife #DigitalMarketing #BusinessTips"
        ),
        "video_script": (
            "HOOK: 'Things I wish I knew before starting a marketing agency — nobody talks about this'\n"
            "BODY: Talking head. Be genuine and personal. Share 4-5 real lessons.\n"
            "CTA: 'What would you add? Comment below — I read every reply.'"
        ),
        "notes": "Be authentic and vulnerable. This type of content builds the most trust."
    },
    15: {
        "week": "WEEK 3: SOCIAL PROOF & ENGAGEMENT",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "We increased this client's sales by 40% — mini case study",
        "caption": (
            "📈 Real results. Real client.\n\n"
            "In 60 days we helped a [client type] business:\n"
            "✅ Increase sales by 40%\n"
            "✅ Grow Instagram followers by 312%\n"
            "✅ Cut cost-per-lead by 60% with paid ads\n\n"
            "The strategy? A combination of organic content + targeted Meta ads + email nurture.\n\n"
            "Want us to do the same for your business?\n"
            "Book a free call → novumediaco.ca\n\n"
            "#MarketingResults #ClientWin #SocialMediaAgency #NovuMediaCo "
            "#PaidAds #InstagramMarketing #LeadGeneration #SmallBusinessMarketing"
        ),
        "video_script": (
            "HOOK: 'We increased this client's sales by 40% in 60 days. Here's the exact strategy.'\n"
            "BODY: Walk through the 3-part strategy: content + paid ads + email.\n"
            "SHOW: Numbers and results as text overlays.\n"
            "CTA: 'DM us or visit novumediaco.ca — we have 2 spots open this month.'"
        ),
        "notes": "Use anonymized client data if needed. Numbers are key — be specific."
    },
    16: {
        "week": "WEEK 3: SOCIAL PROOF & ENGAGEMENT",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "5 content ideas for [niche] businesses",
        "caption": (
            "🎯 5 content ideas for [YOUR NICHE] businesses that actually get engagement:\n\n"
            "(Replace [YOUR NICHE] with your client's industry)\n\n"
            "1️⃣ Behind-the-scenes process video\n"
            "2️⃣ 'Did you know?' fact about your industry\n"
            "3️⃣ Customer transformation story\n"
            "4️⃣ Myth vs. reality about your product/service\n"
            "5️⃣ 'A day in the life' of your business\n\n"
            "Save this 📌 and use one this week!\n\n"
            "#ContentIdeas #SocialMediaMarketing #ContentStrategy #NovuMediaCo "
            "#InstagramContent #DigitalMarketing #ContentCreator #MarketingTips"
        ),
        "video_script": None,
        "notes": "Customize the niche to a specific industry you serve (e.g., restaurants, fitness, real estate)."
    },
    17: {
        "week": "WEEK 3: SOCIAL PROOF & ENGAGEMENT",
        "platforms": ["TikTok"],
        "format": "TikTok",
        "title": "Stitch/Duet — react to a marketing mistake video",
        "caption": (
            "Reacting to this marketing advice so you don't fall for it 👀\n\n"
            "Not all social media advice is created equal. Here's what actually works in 2024:\n\n"
            "❌ 'Post every day no matter what' → ✅ Post consistently with QUALITY\n"
            "❌ 'Buy followers' → ✅ Earn engaged followers who actually buy\n"
            "❌ 'Just go viral' → ✅ Build trust first, reach second\n\n"
            "#MarketingMistakes #SocialMediaTips #NovuMediaCo #DigitalMarketing "
            "#TikTokMarketing #ContentCreator #BusinessTips #MarketingAdvice"
        ),
        "video_script": (
            "FORMAT: Stitch or duet a popular video with bad marketing advice\n"
            "HOOK: 'I need to address this because too many businesses are falling for it'\n"
            "BODY: Correct 3 specific mistakes from the original video\n"
            "CTA: 'Follow so you don't make these mistakes'"
        ),
        "notes": "Search TikTok for marketing advice videos with high engagement to stitch/duet."
    },
    18: {
        "week": "WEEK 3: SOCIAL PROOF & ENGAGEMENT",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "How much should you spend on social media marketing?",
        "caption": (
            "💰 How much should a small business spend on social media marketing?\n\n"
            "Honest answer — it depends. But here's a framework:\n\n"
            "📌 Startup (under $5K/mo revenue): Focus on organic. Budget $0–500/mo\n"
            "📌 Growing ($5K–20K/mo): Mix organic + ads. Budget $500–1,500/mo\n"
            "📌 Scaling ($20K+ /mo): Go full paid. Budget 10–15% of revenue\n\n"
            "The ROI of good marketing always outweighs the cost.\n\n"
            "Swipe to see the breakdown 👉\n\n"
            "#MarketingBudget #DigitalMarketing #SmallBusinessMarketing #NovuMediaCo "
            "#MarketingROI #BusinessOwner #PaidAds #MarketingTips"
        ),
        "video_script": None,
        "notes": "Include a simple chart/table in the carousel showing budget vs business stage."
    },
    19: {
        "week": "WEEK 3: SOCIAL PROOF & ENGAGEMENT",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "Before & after: client account transformation",
        "caption": (
            "Before → After. The power of a proper social media strategy. 📱✨\n\n"
            "Left: Inconsistent posting, low engagement, zero strategy\n"
            "Right: 3+ months with Novu Media Co. 🚀\n\n"
            "The difference isn't luck. It's:\n"
            "✅ A content strategy built around your audience\n"
            "✅ Consistent, high-quality creative\n"
            "✅ Data-driven decisions, not guesses\n\n"
            "Ready for your transformation? → novumediaco.ca\n\n"
            "#BeforeAndAfter #SocialMediaTransformation #MarketingAgency #NovuMediaCo "
            "#InstagramGrowth #ContentStrategy #DigitalMarketing #ClientResults"
        ),
        "video_script": (
            "HOOK: 'Before vs after — what 3 months of proper social media management looks like'\n"
            "SHOW: Side-by-side screenshot comparison of client profile\n"
            "BODY: Walk through the 3 key changes made\n"
            "CTA: 'Book a free call to get your transformation started → link in bio'"
        ),
        "notes": "Get client permission before showing their account. Blur brand names if needed."
    },
    20: {
        "week": "WEEK 3: SOCIAL PROOF & ENGAGEMENT",
        "platforms": ["Instagram"],
        "format": "Story",
        "title": "Open Q&A: ask us anything about your social media",
        "caption": "Stories don't use captions.",
        "video_script": None,
        "notes": (
            "Post 3 stories:\n"
            "1. 'Ask us ANYTHING about your social media strategy 👇' — Q&A sticker\n"
            "2. Answer 3-5 questions you receive (reshare each question with your answer)\n"
            "3. Final story: 'Want a personalized strategy? Book a free call → novumediaco.ca'"
        )
    },
    21: {
        "week": "WEEK 3: SOCIAL PROOF & ENGAGEMENT",
        "platforms": ["TikTok"],
        "format": "TikTok",
        "title": "A week in our agency — montage",
        "caption": (
            "A week at Novu Media Co. 🎬✨\n\n"
            "Strategy calls. Content shoots. Analytics. Client wins. Repeat.\n\n"
            "This is the reality of running a digital marketing agency in Canada. 🇨🇦\n\n"
            "What does your week look like? Tell us below 👇\n\n"
            "#AgencyLife #MarketingAgency #BehindTheScenes #NovuMediaCo "
            "#DigitalMarketing #ContentCreator #Entrepreneur #WeekInMyLife"
        ),
        "video_script": (
            "FORMAT: Fast-cut montage of the full week\n"
            "CLIPS TO COLLECT: Morning work setup, Zoom call screenshots, "
            "content creation, analytics dashboard, team moments, client messages\n"
            "AUDIO: Trending energetic track\n"
            "TEXT OVERLAYS: Day labels (Monday, Tuesday etc.) with quick captions"
        ),
        "notes": "Film short clips throughout the week (Monday–Friday). 15–30 second final video."
    },
    22: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "Our process: how we onboard a new client in 7 days",
        "caption": (
            "🗓 How we onboard a new client at Novu Media Co. — in 7 days:\n\n"
            "Day 1: Discovery call + goal setting\n"
            "Day 2: Brand audit + competitor research\n"
            "Day 3: Strategy presentation\n"
            "Day 4: Content calendar built\n"
            "Day 5: Creative assets designed\n"
            "Day 6: Approval + final tweaks\n"
            "Day 7: GO LIVE 🚀\n\n"
            "No fluff. No waiting. Just results.\n\n"
            "Interested? Book your free call → novumediaco.ca\n\n"
            "#ClientOnboarding #MarketingAgency #NovuMediaCo #DigitalMarketing "
            "#AgencyProcess #SocialMediaMarketing #BusinessGrowth #MarketingStrategy"
        ),
        "video_script": (
            "HOOK: 'Here's exactly how we take a new client from 0 to launched in 7 days'\n"
            "BODY: Walk through each day with text overlay timeline\n"
            "CTA: 'Ready to get started? We have spots open this month — link in bio'"
        ),
        "notes": "Use a timeline graphic or text overlays counting Day 1 through Day 7."
    },
    23: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "Pricing breakdown: what you get with each package",
        "caption": (
            "💸 What does working with a marketing agency actually cost?\n\n"
            "At Novu Media Co., we believe in total transparency. Here's a breakdown:\n\n"
            "🥉 Starter — $499/mo\n"
            "🥈 Growth — $899/mo (most popular)\n"
            "🥇 Premium — $1,499/mo\n\n"
            "Swipe to see exactly what's included in each package 👉\n\n"
            "All prices in CAD. Custom packages available.\n\n"
            "Questions? DM us or visit novumediaco.ca\n\n"
            "#MarketingPricing #SocialMediaAgency #NovuMediaCo #DigitalMarketing "
            "#MarketingPackages #SmallBusinessMarketing #AgencyPricing #BusinessGrowth"
        ),
        "video_script": None,
        "notes": "Use the pricing from your website: Starter $499 / Growth $899 / Premium $1,499 CAD/mo."
    },
    24: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["TikTok"],
        "format": "TikTok",
        "title": "Is a marketing agency worth it for small businesses?",
        "caption": (
            "Is hiring a marketing agency WORTH IT for small businesses? Honest answer. 👇\n\n"
            "The real question isn't 'can I afford an agency?'\n"
            "It's 'can I afford NOT to have one?'\n\n"
            "If your competitors are growing and you're not — that gap costs you more every month.\n\n"
            "A good agency:\n"
            "✅ Saves you 20+ hours/week\n"
            "✅ Brings expertise you'd spend years building\n"
            "✅ Pays for itself in new leads and sales\n\n"
            "#MarketingAgency #SmallBusiness #DigitalMarketing #NovuMediaCo "
            "#BusinessGrowth #SocialMediaMarketing #ROI #Entrepreneurship"
        ),
        "video_script": (
            "HOOK: 'Is hiring a marketing agency actually worth it for small businesses? Honest answer.'\n"
            "BODY: Address the 3 biggest objections — cost, trust, results.\n"
            "FLIP: Reframe each as 'the cost of NOT doing it'\n"
            "CTA: 'Book a free call at novumediaco.ca — no pressure, just a real plan'"
        ),
        "notes": "Address objections directly. Be honest. This builds trust more than any sales pitch."
    },
    25: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "Client spotlight — feature a client's success story",
        "caption": (
            "⭐ Client Spotlight\n\n"
            "[Client type / first name] came to us with a problem:\n"
            "❌ [Their challenge before]\n\n"
            "After [X] months with Novu Media Co.:\n"
            "✅ [Result 1]\n"
            "✅ [Result 2]\n"
            "✅ [Result 3]\n\n"
            "\"[Client quote / testimonial here]\"\n"
            "— [Client name or initials]\n\n"
            "This could be your story. Let's build it together. 🚀\n"
            "novumediaco.ca\n\n"
            "#ClientSpotlight #MarketingResults #NovuMediaCo #SocialMediaAgency "
            "#DigitalMarketing #ClientSuccess #TestimonialTuesday #BusinessGrowth"
        ),
        "video_script": None,
        "notes": "Replace all [brackets] with real client info. Get written permission before posting."
    },
    26: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "We have 2 spots open this month — how to apply",
        "caption": (
            "🔥 We only work with a limited number of clients each month.\n\n"
            "Right now, we have 2 spots open for June.\n\n"
            "Here's who we're looking for:\n"
            "✅ Business owner ready to invest in growth\n"
            "✅ Clear offer or service to promote\n"
            "✅ Willing to show up consistently\n\n"
            "Here's how to apply:\n"
            "1️⃣ Visit novumediaco.ca\n"
            "2️⃣ Click 'Book a Free Strategy Call'\n"
            "3️⃣ We'll review your business and get back to you within 24 hours\n\n"
            "Don't wait — these spots fill fast. 🚀\n\n"
            "#MarketingAgency #NovuMediaCo #DigitalMarketing #LimitedSpots "
            "#SocialMediaAgency #BusinessGrowth #MarketingStrategy #ClientApplication"
        ),
        "video_script": (
            "HOOK: 'We only take on 5 new clients per month — and we have 2 spots left.'\n"
            "BODY: Who it's for. What they get. The 3-step application process.\n"
            "CTA: 'Visit novumediaco.ca before these spots are gone — link in bio.'"
        ),
        "notes": "Scarcity drives action. Update the number of spots each month. Be honest."
    },
    27: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["Instagram"],
        "format": "Story",
        "title": "Link to contact page + testimonial screenshots",
        "caption": "Stories don't use captions.",
        "video_script": None,
        "notes": (
            "Post 3 stories:\n"
            "1. Testimonial screenshot with text: 'Real client. Real results.'\n"
            "2. 'Ready to grow your business on social media?'\n"
            "3. Link sticker → novumediaco.ca/contact with text 'Book your FREE strategy call'"
        )
    },
    28: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["TikTok"],
        "format": "TikTok",
        "title": "30 days on TikTok — here's what we learned",
        "caption": (
            "We've been on TikTok for 30 days. Here's everything we learned 👇\n\n"
            "🎯 What worked: [your actual top performing content type]\n"
            "❌ What flopped: [your actual low performers]\n"
            "😲 Most surprising: [genuine insight from your data]\n"
            "📈 Best result: [your actual best metric]\n\n"
            "The TikTok algorithm rewards authenticity over production quality. Every time.\n\n"
            "What's been working on YOUR TikTok? Tell us below 👇\n\n"
            "#TikTokMarketing #TikTokGrowth #NovuMediaCo #ContentCreator "
            "#SocialMediaMarketing #TikTokTips #DigitalMarketing #30DayChallenge"
        ),
        "video_script": (
            "HOOK: '30 days on TikTok as a marketing agency — here's what actually happened'\n"
            "BODY: Pull your REAL analytics. Show the screen. Be transparent about what worked and what didn't.\n"
            "DATA POINTS: Top video views, follower count, engagement rate\n"
            "CTA: 'Follow along for month 2 — we're just getting started'"
        ),
        "notes": "Use your REAL analytics for this. Transparency and authenticity = highest engagement."
    },
    29: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["Instagram"],
        "format": "Carousel",
        "title": "Month 1 recap: stats, wins, and lessons",
        "caption": (
            "📊 Month 1 wrapped. Here's what happened:\n\n"
            "📈 [X] Instagram followers gained\n"
            "📱 [X] TikTok followers gained\n"
            "👁 [X] total impressions\n"
            "💬 [X] DMs and inquiries\n"
            "🤝 [X] new clients signed\n\n"
            "Biggest lesson: [your real #1 takeaway]\n\n"
            "Month 2 starts now. Follow along 🚀\n\n"
            "#MonthlyRecap #SocialMediaGrowth #NovuMediaCo #DigitalMarketing "
            "#AgencyLife #ContentCreator #TransparentMarketing #BusinessUpdate"
        ),
        "video_script": None,
        "notes": "Replace all stats with your REAL numbers from Instagram + TikTok analytics."
    },
    30: {
        "week": "WEEK 4: CONVERT & CLOSE",
        "platforms": ["Instagram", "TikTok"],
        "format": "Reel / TikTok",
        "title": "If you're a business owner who wants to grow on social media, watch this",
        "caption": (
            "If you're a business owner struggling with social media — this is for you. 👇\n\n"
            "You don't need to go viral.\n"
            "You don't need a huge following.\n"
            "You don't need to post every single day.\n\n"
            "You need:\n"
            "✅ A clear message that speaks to the RIGHT people\n"
            "✅ Consistent content that builds trust over time\n"
            "✅ A strategy — not guesswork\n\n"
            "That's exactly what we do at Novu Media Co.\n\n"
            "Book a free 30-minute strategy call → novumediaco.ca\n"
            "No pressure. No sales pitch. Just a real plan for your business.\n\n"
            "#BusinessOwner #SocialMediaMarketing #NovuMediaCo #DigitalMarketing "
            "#MarketingAgency #SmallBusiness #BusinessGrowth #SocialMediaStrategy"
        ),
        "video_script": (
            "HOOK: 'If you're a business owner who wants to grow on social media — stop and watch this'\n"
            "BODY: Debunk the 3 myths about social media growth. Then present the real solution.\n"
            "BUILD-UP: 'You don't need X, Y, or Z. You need strategy + consistency + the right message.'\n"
            "CTA: 'Book a free strategy call at novumediaco.ca. Link in bio. Let's build your plan.'"
        ),
        "notes": "This is your closing video. Make it emotionally resonant. Speak directly to pain points."
    }
}

# ─── HASHTAG SETS ─────────────────────────────────────────────────────────────
INSTAGRAM_HASHTAGS = [
    "#NovuMediaCo", "#DigitalMarketing", "#SocialMediaMarketing",
    "#MarketingAgency", "#ContentStrategy", "#InstagramGrowth",
    "#CanadianMarketing", "#SmallBusinessMarketing", "#BusinessGrowth"
]

TIKTOK_HASHTAGS = [
    "#NovuMediaCo", "#DigitalMarketing", "#MarketingAgency",
    "#TikTokMarketing", "#BusinessTips", "#SocialMediaTips"
]

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def get_day_number(launch_date=LAUNCH_DATE):
    """Calculate which day of the plan we're on."""
    today = date.today()
    delta = (today - launch_date).days + 1
    return max(1, min(delta, 30))


def generate_brief(day_num):
    """Generate a full content brief for the given day."""
    if day_num not in THIRTY_DAY_PLAN:
        return None

    plan = THIRTY_DAY_PLAN[day_num]
    today_str = date.today().strftime("%B %d, %Y")

    brief = {
        "date": today_str,
        "day": day_num,
        "week_theme": plan["week"],
        "platforms": plan["platforms"],
        "format": plan["format"],
        "title": plan["title"],
        "caption": plan["caption"],
        "hashtags": INSTAGRAM_HASHTAGS if "Instagram" in plan["platforms"] else TIKTOK_HASHTAGS,
        "video_script": plan.get("video_script"),
        "production_notes": plan.get("notes", ""),
    }
    return brief


def save_brief(brief, output_dir=None):
    """Save the brief as a text file."""
    if output_dir is None:
        # Default to the Media Expert folder
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "daily_briefs"
        )
    os.makedirs(output_dir, exist_ok=True)

    filename = f"Day_{brief['day']:02d}_{date.today().strftime('%Y-%m-%d')}_brief.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"NOVU MEDIA CO. — DAILY CONTENT BRIEF\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Date:     {brief['date']}\n")
        f.write(f"Day:      {brief['day']} / 30\n")
        f.write(f"Theme:    {brief['week_theme']}\n")
        f.write(f"Platform: {', '.join(brief['platforms'])}\n")
        f.write(f"Format:   {brief['format']}\n\n")
        f.write("-" * 60 + "\n")
        f.write(f"📌 TITLE / TOPIC\n{brief['title']}\n\n")
        f.write("-" * 60 + "\n")
        f.write(f"✍️ CAPTION\n\n{brief['caption']}\n\n")
        f.write("-" * 60 + "\n")
        f.write(f"#️⃣ HASHTAGS\n{' '.join(brief['hashtags'])}\n\n")
        if brief.get("video_script"):
            f.write("-" * 60 + "\n")
            f.write(f"🎬 VIDEO SCRIPT\n\n{brief['video_script']}\n\n")
        f.write("-" * 60 + "\n")
        f.write(f"📋 PRODUCTION NOTES\n{brief['production_notes']}\n\n")
        f.write("=" * 60 + "\n")
        f.write("Generated by Novu Media Co. Content Agent\n")

    return filepath


def print_brief(brief):
    """Print the brief to console."""
    print("\n" + "=" * 60)
    print("NOVU MEDIA CO. — DAILY CONTENT BRIEF")
    print("=" * 60)
    print(f"Date:     {brief['date']}")
    print(f"Day:      {brief['day']} / 30")
    print(f"Theme:    {brief['week_theme']}")
    print(f"Platform: {', '.join(brief['platforms'])}")
    print(f"Format:   {brief['format']}")
    print("\n📌 TITLE")
    print(brief['title'])
    print("\n✍️ CAPTION")
    print(brief['caption'])
    print("\n#️⃣ HASHTAGS")
    print(" ".join(brief['hashtags']))
    if brief.get("video_script"):
        print("\n🎬 VIDEO SCRIPT")
        print(brief['video_script'])
    print("\n📋 PRODUCTION NOTES")
    print(brief['production_notes'])
    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Novu Media Co. Content Agent")
    parser.add_argument("--day", type=int, help="Override the day number (1-30)")
    parser.add_argument("--save", action="store_true", help="Save brief to file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    day_num = args.day if args.day else get_day_number()
    brief = generate_brief(day_num)

    if not brief:
        print(f"No content found for day {day_num}")
        sys.exit(1)

    if args.json:
        print(json.dumps(brief, indent=2))
    else:
        print_brief(brief)

    if args.save:
        path = save_brief(brief)
        print(f"Brief saved to: {path}")
