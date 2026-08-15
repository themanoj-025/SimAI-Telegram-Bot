import asyncio
import random

import feedparser

from scrapers.async_base_scraper import AsyncBaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)

STATIC_AI_TWEETS = [
    {
        "title": "OpenAI continues shipping multimodal improvements across its flagship models.",
        "link": "https://openai.com/news/",
        "source": "X (@OpenAI)",
        "published": "",
    },
    {
        "title": "Google DeepMind keeps pushing speed and reasoning with Gemini model updates.",
        "link": "https://deepmind.google/technologies/gemini/",
        "source": "X (@GoogleDeepMind)",
        "published": "",
    },
    {
        "title": "Anthropic remains strong on coding and long-context assistant use cases.",
        "link": "https://www.anthropic.com/news",
        "source": "X (@AnthropicAI)",
        "published": "",
    },
    {
        "title": "DeepSeek shows how competitive open models can be on cost and reasoning quality.",
        "link": "https://www.deepseek.com/",
        "source": "X (@deepseek_ai)",
        "published": "",
    },
    {
        "title": "Meta's Llama family remains a major open-weight option for self-hosted AI stacks.",
        "link": "https://www.llama.com/",
        "source": "X (@MetaAI)",
        "published": "",
    },
    {
        "title": "Hugging Face continues to grow the open model and app ecosystem at high speed.",
        "link": "https://huggingface.co/models",
        "source": "X (@huggingface)",
        "published": "",
    },
    {
        "title": "AI agents keep gaining attention as teams connect LLMs with tools and workflows.",
        "link": "https://github.com/microsoft/autogen",
        "source": "X (@LangChainAI)",
        "published": "",
    },
    {
        "title": "Demand for AI compute remains strong as model training and inference scale up.",
        "link": "https://nvidianews.nvidia.com/",
        "source": "X (@NVIDIAAI)",
        "published": "",
    },
]


class TwitterScraper(AsyncBaseScraper):
    def __init__(self):
        super().__init__()
        self.rsshub_instances = [
            "https://rsshub.app",
            "https://hub.slarker.me",
            "https://rss.fatpandadev.com",
        ]
        self.accounts = [
            "sama",
            "OpenAI",
            "AndrewYNg",
            "karpathy",
            "GoogleAI",
            "demishassabis",
            "AnthropicAI",
            "DeepMind",
            "huggingface",
            "NVIDIAAI",
            "ylecun",
            "lexfridman",
            "rowancheung",
            "VaibhavSisinty",
            "waitin4agi",
            "OfficialINDIAai",
        ]

    async def fetch_tweets(self, limit: int = 10) -> list[dict]:
        logger.info(f"Fetching latest AI tweets (limit: {limit})")
        all_tweets = []
        sampled_accounts = random.sample(self.accounts, min(len(self.accounts), 8))

        async def fetch_account_tweets(account: str) -> list[dict]:
            for rsshub in random.sample(self.rsshub_instances, len(self.rsshub_instances)):
                rss_url = f"{rsshub}/twitter/user/{account}"
                try:
                    content = await self.fetch_url(rss_url, timeout=5)
                    if not content:
                        continue

                    feed = feedparser.parse(content)
                    items = []
                    for entry in feed.entries[:2]:
                        items.append(
                            {
                                "title": entry.get("title", ""),
                                "link": entry.get("link", f"https://x.com/{account}"),
                                "source": f"X (@{account})",
                                "published": entry.get("published", ""),
                            }
                        )
                    return items
                except Exception:
                    continue
            return []

        results = await asyncio.gather(
            *[fetch_account_tweets(account) for account in sampled_accounts]
        )
        for result in results:
            all_tweets.extend(result)

        all_tweets = [tweet for tweet in all_tweets if tweet.get("title", "").strip()]
        if len(all_tweets) < 3:
            logger.warning(
                "Live tweet fetch yielded insufficient results. Using curated static fallback."
            )
            all_tweets = STATIC_AI_TWEETS.copy()

        random.shuffle(all_tweets)
        return all_tweets[:limit]
