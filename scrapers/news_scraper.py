import asyncio
import random

import feedparser

from scrapers.async_base_scraper import AsyncBaseScraper
from scrapers.fallback_data import get_fallback_articles
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Article:
    def __init__(self, title: str, link: str, source: str, published: str = "") -> None:
        self.title = title
        self.link = link
        self.source = source
        self.published = published

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "link": self.link,
            "source": self.source,
            "published": self.published,
        }


class NewsScraper(AsyncBaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.feeds = self.config.RSS_FEEDS.get("news", [])

    async def fetch_news(self, limit: int = 5) -> list[Article]:
        articles = []

        async def fetch_feed(url) -> None:
            try:
                content = await self.fetch_url(url)
                if not content:
                    return []
                feed = feedparser.parse(content)
                source_name = feed.feed.get("title", "Unknown")
                res = []
                for entry in feed.entries[:limit]:
                    res.append(
                        Article(
                            title=entry.get("title", "No Title"),
                            link=entry.get("link", ""),
                            source=source_name,
                            published=entry.get("published", ""),
                        )
                    )
                return res
            except Exception as e:
                logger.error(f"Error fetching news from {url}: {e}")
                return []

        results = await asyncio.gather(*[fetch_feed(url) for url in self.feeds])
        for res in results:
            articles.extend(res)

        seen = set()
        unique_articles = []
        for article in articles:
            if article.title not in seen:
                seen.add(article.title)
                unique_articles.append(article)

        result = unique_articles[:limit]
        if result:
            return result

        logger.warning("News scraper returned 0 live results - using fallback content.")
        return self._build_fallback_articles("news", limit)

    def _build_fallback_articles(self, category: str, limit: int) -> list[Article]:
        return [
            Article(
                title=item["title"],
                link=item["link"],
                source=item["source"],
                published=item.get("published", ""),
            )
            for item in get_fallback_articles(category, limit)
        ]


class ArxivScraper(AsyncBaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.feeds = self.config.RSS_FEEDS.get("arxiv", [])

    async def fetch_papers(self, limit: int = 5) -> list[Article]:
        articles = []
        for feed_url in self.feeds:
            try:
                content = await self.fetch_url(feed_url)
                if not content:
                    continue
                feed = feedparser.parse(content)
                for entry in feed.entries[:limit]:
                    title = entry.get("title", "No Title").replace("\n", " ").strip()
                    summary = entry.get("summary", "")[:150].replace("\n", " ").strip()
                    articles.append(
                        Article(
                            title=f"{title}\n{summary}...",
                            link=entry.get("link", ""),
                            source="arXiv",
                            published=entry.get("published", ""),
                        )
                    )
            except Exception as e:
                logger.error(f"Error fetching arXiv papers from {feed_url}: {e}")

        result = articles[:limit]
        if result:
            return result

        logger.warning("arXiv scraper returned 0 live results - using fallback content.")
        return [
            Article(
                title=item["title"],
                link=item["link"],
                source=item["source"],
                published=item.get("published", ""),
            )
            for item in get_fallback_articles("arxiv", limit)
        ]


class BlogScraper(AsyncBaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.feeds = self.config.RSS_FEEDS.get("blogs", [])

    async def fetch_blogs(self, limit: int = 5) -> list[Article]:
        articles = []
        for feed_url in self.feeds:
            try:
                content = await self.fetch_url(feed_url)
                if not content:
                    continue
                feed = feedparser.parse(content)
                source_name = feed.feed.get("title", "Unknown")
                for entry in feed.entries[:limit]:
                    articles.append(
                        Article(
                            title=entry.get("title", "No Title"),
                            link=entry.get("link", ""),
                            source=source_name,
                            published=entry.get("published", ""),
                        )
                    )
            except Exception as e:
                logger.error(f"Error fetching blogs from {feed_url}: {e}")

        result = articles[:limit]
        if result:
            return result

        logger.warning("Blog scraper returned 0 live results - using fallback content.")
        return [
            Article(
                title=item["title"],
                link=item["link"],
                source=item["source"],
                published=item.get("published", ""),
            )
            for item in get_fallback_articles("blogs", limit)
        ]


class YouTubeScraper(AsyncBaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.feeds = self.config.RSS_FEEDS.get("youtube", [])

    async def fetch_youtube(self, limit: int = 5) -> list[Article]:
        articles = []
        feeds_shuffled = self.feeds.copy()
        random.shuffle(feeds_shuffled)

        async def fetch_yt_feed(url) -> None:
            try:
                content = await self.fetch_url(url, timeout=5)
                if not content:
                    return []
                feed = feedparser.parse(content)
                source_name = feed.feed.get("title", "YouTube")
                res = []
                for entry in feed.entries[:2]:
                    res.append(
                        Article(
                            title=entry.get("title", "No Title"),
                            link=entry.get("link", ""),
                            source=source_name,
                            published=entry.get("published", ""),
                        )
                    )
                return res
            except Exception as e:
                logger.debug(f"YouTube feed skipped ({url}): {e}")
                return []

        results = await asyncio.gather(
            *[fetch_yt_feed(url) for url in feeds_shuffled[:10]]
        )  # Fetch top 10 feeds in parallel
        for res in results:
            articles.extend(res)

        try:
            articles.sort(key=lambda x: x.published, reverse=True)
        except Exception:
            pass

        result = articles[:limit]
        if not result:
            logger.warning("YouTube scraper returned 0 results - using fallback links.")
            fallback = [
                Article(
                    "AI Explained - Latest AI News & Analysis",
                    "https://www.youtube.com/@aiexplained-official",
                    "YouTube",
                ),
                Article(
                    "Matt Wolfe - AI Tools & Updates",
                    "https://www.youtube.com/@mreflow",
                    "YouTube",
                ),
                Article(
                    "Yannic Kilcher - AI Research Papers",
                    "https://www.youtube.com/@YannicKilcher",
                    "YouTube",
                ),
                Article(
                    "Two Minute Papers - AI Research Highlights",
                    "https://www.youtube.com/@TwoMinutePapers",
                    "YouTube",
                ),
                Article(
                    "Lex Fridman - AI & Technology Conversations",
                    "https://www.youtube.com/@lexfridman",
                    "YouTube",
                ),
            ]
            return fallback[:limit]

        return result


class TutorialScraper(AsyncBaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.feeds = self.config.RSS_FEEDS.get("tutorials", [])

    async def fetch_tutorials(self, limit: int = 5) -> list[Article]:
        articles = []
        for url in self.feeds:
            content = await self.fetch_url(url)
            if not content:
                continue
            feed = feedparser.parse(content)
            for entry in feed.entries[:limit]:
                articles.append(
                    Article(
                        entry.get("title"),
                        entry.get("link"),
                        feed.feed.get("title", "Unknown"),
                    )
                )

        result = articles[:limit]
        if result:
            return result

        logger.warning("Tutorial scraper returned 0 live results - using fallback content.")
        return [
            Article(
                title=item["title"],
                link=item["link"],
                source=item["source"],
                published=item.get("published", ""),
            )
            for item in get_fallback_articles("learn", limit)
        ]
