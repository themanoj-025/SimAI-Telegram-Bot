import feedparser
import httpx

from scrapers.async_base_scraper import AsyncBaseScraper
from scrapers.fallback_data import get_fallback_articles
from utils.cache_manager import CacheManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ExtendedScraper(AsyncBaseScraper):
    def __init__(self):
        super().__init__()
        self.cache = CacheManager()

    async def fetch_category(
        self, category: str, limit: int = 5, force_refresh: bool = False
    ) -> list[dict]:
        """Fetch data for a specific category, using cache if fresh unless force_refresh is True."""
        if not force_refresh:
            cached_data = self.cache.get_cached_data(category)
            if cached_data:
                logger.info(f"Returning cached data for {category}")
                return cached_data

        logger.info(f"Fetching fresh data for {category} (Force: {force_refresh})")
        feeds = self.config.RSS_FEEDS.get(category, [])
        articles = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
            for url in feeds:
                try:
                    response = await client.get(url, timeout=10)
                    response.raise_for_status()
                    feed = feedparser.parse(response.content)
                    source_name = feed.feed.get("title", category.capitalize())

                    for entry in feed.entries[:limit]:
                        item = {
                            "title": entry.get("title", "No Title"),
                            "link": entry.get("link", ""),
                            "source": source_name,
                            "published": entry.get("published", ""),
                        }
                        articles.append(item)
                except Exception as e:
                    logger.error(f"Error fetching {category} from {url}: {e}")

        # Deduplicate
        seen = set()
        unique_articles = []
        for a in articles:
            if a["link"] not in seen:
                seen.add(a["link"])
                unique_articles.append(a)

        result = unique_articles[:limit]
        if result:
            self.cache.update_cache(category, result)
            return result

        stale_cache = self.cache.get_latest_cached_data(category)
        if stale_cache:
            logger.warning(
                f"Live fetch failed for {category}; returning cached fallback data."
            )
            return stale_cache[:limit]

        logger.warning(
            f"No live or cached data for {category}; using static fallback content."
        )
        return get_fallback_articles(category, limit)


class ToolScraper(ExtendedScraper):
    async def fetch_tools(self, limit: int = 5, force_refresh: bool = False):
        return await self.fetch_category("tools", limit, force_refresh)


class JobScraper(ExtendedScraper):
    async def fetch_jobs(self, limit: int = 5, force_refresh: bool = False):
        return await self.fetch_category("jobs", limit, force_refresh)


class StartupScraper(ExtendedScraper):
    async def fetch_startups(self, limit: int = 5, force_refresh: bool = False):
        return await self.fetch_category("startups", limit, force_refresh)


class ModelScraper(ExtendedScraper):
    async def fetch_models(self, limit: int = 5, force_refresh: bool = False):
        return await self.fetch_category("models", limit, force_refresh)


class DatasetScraper(ExtendedScraper):
    async def fetch_datasets(self, limit: int = 5, force_refresh: bool = False):
        return await self.fetch_category("datasets", limit, force_refresh)


class TrendingScraper(ExtendedScraper):
    async def fetch_trending(self, limit: int = 5, force_refresh: bool = False):
        return await self.fetch_category("trending", limit, force_refresh)


class LearnScraper(ExtendedScraper):
    async def fetch_learn(self, limit: int = 5, force_refresh: bool = False):
        return await self.fetch_category("learn", limit, force_refresh)


class ConferenceScraper(ExtendedScraper):
    async def fetch_conferences(self, limit: int = 5, force_refresh: bool = False):
        return await self.fetch_category("conferences", limit, force_refresh)
