import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    ARTICLES_PER_SECTION = 5
    CACHE_EXPIRY_HOURS = 6

    RSS_FEEDS = {
        "news": [
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://venturebeat.com/category/ai/feed/",
            "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
            "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
            "https://www.wired.com/feed/tag/ai/latest/rss",
            "https://www.marktechpost.com/feed/",
            "https://syncedreview.com/feed/",
            "https://towardsdatascience.com/feed",
        ],
        "arxiv": [
            "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=15",
            "http://export.arxiv.org/api/query?search_query=cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=15",
            "http://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=15",
            "http://export.arxiv.org/api/query?search_query=cat:cs.CV&sortBy=submittedDate&sortOrder=descending&max_results=15",
        ],
        "blogs": [
            "https://openai.com/blog/rss.xml",
            "https://blogs.nvidia.com/feed/",
            "https://huggingface.co/blog/rss.xml",
            "https://deepmind.com/blog/feed/rss/",
            "https://ai.meta.com/blog/rss/",
            "https://mistral.ai/news/rss.xml",
            "https://www.anthropic.com/rss.xml",
        ],
        "tools": [
            "https://www.producthunt.com/feed?category=ai-tools",
            "https://futurepedia.io/rss",
            "https://www.toolify.ai/rss",
        ],
        "jobs": [
            "https://ai-jobs.net/rss/",
            "https://remoteok.com/remote-ai-jobs.rss",
            "https://weworkremotely.com/categories/remote-ai-jobs.rss",
        ],
        "startups": [
            "https://techcrunch.com/category/startups/feed/",
            "https://venturebeat.com/category/ai/feed/",
            "https://inc42.com/tag/artificial-intelligence/feed/",
        ],
        "models": [
            "https://huggingface.co/blog/rss.xml",
            "https://openai.com/blog/rss.xml",
            "https://deepmind.com/blog/feed/rss/",
        ],
        "trending": [
            "https://www.reddit.com/r/MachineLearning/.rss",
            "https://www.reddit.com/r/LocalLLaMA/.rss",
            "https://www.reddit.com/r/OpenAI/.rss",
        ],
        "learn": [
            "https://towardsdatascience.com/feed",
            "https://machinelearningmastery.com/feed/",
            "https://www.deeplearning.ai/the-batch/rss",
        ],
        "indian_ai": [
            "https://analyticsindiamag.com/feed/",
            "https://inc42.com/tag/artificial-intelligence/feed/",
            "https://yourstory.com/feed/tag/ai",
        ],
        "indian_ai_sources": {
            "government": [
                "https://indiaai.gov.in/news",
                "https://indiaai.gov.in/news/all",
                "https://indiaai.gov.in/article",
                "https://indiaai.gov.in/use-cases",
                "https://indiaai.gov.in/resources",
            ],
            "analytics_india": [
                "https://analyticsindiamag.com/category/artificial-intelligence/",
                "https://analyticsindiamag.com/category/machine-learning/",
                "https://analyticsindiamag.com/latest-news/",
                "https://analyticsindiamag.com/tag/india/",
            ],
            "economic_times": [
                "https://ai.economictimes.com/news",
                "https://ai.economictimes.com/news/artificial-intelligence",
                "https://enterpriseai.economictimes.indiatimes.com/news",
                "https://economictimes.indiatimes.com/topic/artificial-intelligence",
            ],
            "indian_express": [
                "https://indianexpress.com/section/technology/artificial-intelligence/",
                "https://indianexpress.com/section/technology/",
            ],
            "inc42": [
                "https://inc42.com/category/artificial-intelligence/",
                "https://inc42.com/tag/ai/",
                "https://inc42.com/tag/machine-learning/",
            ],
            "tech_media": [
                "https://www.gadgets360.com/ai",
                "https://www.gadgets360.com/topics/artificial-intelligence",
                "https://timesofindia.indiatimes.com/topic/artificial-intelligence",
                "https://timesofindia.indiatimes.com/tech",
                "https://www.ndtv.com/ai",
                "https://www.ndtv.com/topic/artificial-intelligence",
                "https://www.hindustantimes.com/topic/artificial-intelligence",
            ],
            "rss_feeds": [
                "https://news.google.com/search?q=artificial+intelligence+india",
                "https://www.bing.com/news/search?q=artificial+intelligence+india",
                "https://blog.feedspot.com/artificial_intelligence_blogs_india/",
            ],
            "company_blogs": [
                "https://www.tcs.com/what-we-do/artificial-intelligence",
                "https://www.infosys.com/services/data-ai",
                "https://www.wipro.com/ai",
                "https://www.hcltech.com/ai",
                "https://yellow.ai/blog",
                "https://uniphore.com/blog",
                "https://madstreetden.com/blog",
            ],
            "research": [
                "https://arxiv.org/search/?query=india+ai",
                "https://paperswithcode.com/search?q=india",
                "https://openreview.net",
            ],
        },
        "youtube": [
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCNJ1Ymd5yFuUPtn21xtRbbw",  # AI Explained
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCuK2Mf5As9OKfWU7XV6yzCg",  # Matt Wolfe
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCRJFAp0rewx8kzdhEqDHIlA",  # The AI Advantage
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCqcbQf6yw5KzRoDDcZ_wBSw",  # Wes Roth
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCSPkiRjFYpz-8DY-aF_1wRg",  # The AI Grid
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCawZsQWqfGSbCI5yjkdVkTA",  # Matthew Berman
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCYwLV1gDwzGbg7jXQ52bVnQ",  # World of AI
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg",  # Two Minute Papers
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCHmD-oSpV0sNfAUnpYpj8KA",  # Yannic Kilcher
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCcIXc5mJsHVYTZR1maL5l9w",  # DeepLearningAI
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCJIfeSCssxSC_Dhc5s7woww",  # Lex Fridman
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCQALLeQPoZdZC4JNUboVEUg",  # Sentdex
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCjWY5hREA6FFYrthD0rZNIw",  # Krish Naik
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCCWi3hpnq_Pe03nGxuS7isg",  # CampusX
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC1emV4A8liRs9p80CY8ElUQ",  # freeCodeCamp
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC5_6ZD6s8klmMu9TXEB_1IA",  # CodeEmporium
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC1_uAIS3r8Vu6JjXWvastJg",  # 3Blue1Brown
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCtYLUTtgS3k1Fg4y5tAhLbw",  # StatQuest
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCoxcjq-8xIDTYp3uz647V5A",  # Computerphile
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCuQprr9BORdW-vsHPZ796ZA",  # Jordan Harrod
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCsQoiOrh7jzKmE8NBofhTnQ",  # Varun Mayya
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCantI2XfGkxpvW85HYHE_XA",  # AI with Aakash
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCCsk2ye5FnRHanZlvr9mLww",  # The Indian AI Guy
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC-zVytOQB62OwMhKRi0TDvg",  # AI Anytime
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC13t24sAldkSIUwEJOBqWDw",  # AI Seekh Lo
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCTmFBhuhMibVoSfYom1uXEg",  # Codebasics
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCjzgvNs18uEX02kX-GSNYDQ",  # Data Science Lovers
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCnz-ZXXER4jOvuED5trXfEA",  # TechTFQ
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC1CgfNVk8NFzJJ1exEmPiCw",  # WsCube Tech
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCBvJMMD6JL4-9ry4LLXmqBg",  # iNeuron
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCH6gDteHtH4hg3o2343iObA",  # Analytics Vidhya
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCZJlMUYdbtzQ8tVfLvK1KvQ",  # Coding Ninjas India
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCxTFPM1NYtPVk1jBwUMJcnw",  # Decoding YT
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCR9j1jqqB5Rse69wjUnbYwA",  # All About AI
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCoM9lSqWLBEmhpPW1M83E6A",  # Futurepedia
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC5-m30sIN3k2-P0b6LC4Ekw",  # AI Search
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCzlV2ZyfPk7_JvAqUtZvMtg",  # AI Revolution News
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCyO-iNwDISfxBraxafH5ang",  # AI Uncovered
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCO4UnRJVugVyqeNtcUNJyXw",  # AI Today
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC1Id0Y6UzOeihraDf4lEARg",  # AI Insights
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCKelCK4ZaO6HeEI1KQjqzWA",  # AI Daily Brief
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC7yXYQfdJht-grQEsLxl9Jw",  # AI News Hub
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCY-9845u5E5mfkVX6W3hYJA",  # AI Tech Report
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCJjXHWGv5Q5Xwg7n5JRl_Ow",  # AI Breakdown
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCFH-_AqcoUOVSrL_ikqNRtA",  # AI Focus
        ],
    }

    GITHUB_TRENDING_URL = "https://github.com/trending/python?since=daily"

    REQUEST_TIMEOUT = 60
    MAX_RETRIES = 3

    LOG_LEVEL = "INFO"
    LOG_FILE = "ai_daily_bot.log"
    REPORT_TIME = datetime.now().replace(
        hour=9, minute=0, second=0, microsecond=0
    )  # Default report time
