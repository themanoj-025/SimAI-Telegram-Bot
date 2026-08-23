import asyncio
import random

import feedparser
import httpx
from bs4 import BeautifulSoup

from scrapers.async_base_scraper import AsyncBaseScraper
from scrapers.fallback_data import get_fallback_articles
from utils.logger import setup_logger

logger = setup_logger(__name__)


class IndianAINewsScraper(AsyncBaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.rss_feeds = self.config.RSS_FEEDS.get("indian_ai", [])
        self.sources = self.config.RSS_FEEDS.get("indian_ai_sources", {})
        self.browser_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def fetch_url_with_headers(self, url: str) -> str | None:
        """Fetch URL with browser-like headers to avoid 403s."""
        async with httpx.AsyncClient(
            headers=self.browser_headers, follow_redirects=True, verify=False
        ) as client:
            try:
                response = await client.get(url, timeout=15)
                logger.info(f"Fetched {url} - Status: {response.status_code}")
                response.raise_for_status()
                return response.text
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                logger.error(f"Error fetching {url}: {e}")
                return None

    async def _fetch_rss(self, url: str, limit: int) -> list[dict]:
        """Fetch and parse RSS feed."""
        content = await self.fetch_url_with_headers(url)
        if not content:
            return []

        try:
            feed = feedparser.parse(content)
            source_name = feed.feed.get("title", "Indian AI News")
            articles = []
            for entry in feed.entries[:limit]:
                # Heuristic: Filter for India related keywords if it's a general feed
                title = entry.get("title", "No Title")
                articles.append(
                    {
                        "title": title,
                        "link": entry.get("link", ""),
                        "source": source_name,
                        "published": entry.get("published", ""),
                    }
                )
            logger.info(f"Fetched {len(articles)} articles from RSS: {url}")
            return articles
        except (ValueError, KeyError, AttributeError) as e:
            logger.error(f"Error parsing RSS {url}: {e}")
            return []

    async def _fetch_html_articles(self, url: str, source_name: str, limit: int) -> list[dict]:
        """Generic HTML article extractor for news pages."""
        content = await self.fetch_url_with_headers(url)
        if not content:
            return []

        articles = []
        try:
            soup = BeautifulSoup(content, "html.parser")
            # Improved heuristic: look for <h2>, <h3>, or <a> with significant text
            # We look for links within heading tags which are common for article titles
            for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
                link = heading.find("a", href=True)
                if not link:
                    # Maybe the heading is inside a link
                    link = (
                        heading.parent
                        if heading.parent.name == "a" and heading.parent.has_attr("href")
                        else None
                    )

                if link:
                    title = link.get_text().strip()
                    href = link["href"]

                    if not href.startswith("http"):
                        # Handle relative links
                        from urllib.parse import urljoin

                        href = urljoin(url, href)

                    if len(title) > 25 and href not in [a["link"] for a in articles]:
                        articles.append(
                            {
                                "title": title,
                                "link": href,
                                "source": source_name,
                                "published": "",
                            }
                        )

                if len(articles) >= limit:
                    break

            # Fallback to searching all links with a certain class or pattern if needed
            if not articles:
                links = soup.find_all("a", href=True)
                for link in links:
                    title = link.get_text().strip()
                    href = link["href"]
                    if len(title) > 40 and "http" in href:
                        if href not in [a["link"] for a in articles]:
                            articles.append(
                                {
                                    "title": title,
                                    "link": href,
                                    "source": source_name,
                                    "published": "",
                                }
                            )
                    if len(articles) >= limit:
                        break

            logger.info(f"Fetched {len(articles)} articles from HTML: {url}")
        except (ValueError, KeyError, AttributeError) as e:
            logger.error(f"Error parsing HTML {url}: {e}")

        return articles

    async def fetch_indian_ai_news(self, limit: int = 5) -> list[dict]:
        """Main method to fetch Indian AI news from all sources."""
        all_articles = []

        # 1. Fetch from RSS feeds
        rss_tasks = [self._fetch_rss(url, 3) for url in self.rss_feeds]

        # 2. Fetch from a subset of HTML sources to maintain speed
        # We'll pick one from each category if available
        html_tasks = []
        for category, urls in self.sources.items():
            if urls:
                # Pick a random URL from the category to ensure variety
                target_url = random.choice(urls)
                source_name = category.replace("_", " ").title()
                html_tasks.append(self._fetch_html_articles(target_url, source_name, 3))

        # Combine all tasks
        all_tasks = rss_tasks + html_tasks
        results = await asyncio.gather(*all_tasks, return_exceptions=True)

        for res in results:
            if isinstance(res, list):
                all_articles.extend(res)
            elif isinstance(res, Exception):
                logger.error(f"Scraper task failed: {res}")

        # Deduplicate and limit
        seen = set()
        unique_articles = []
        for article in all_articles:
            if article["link"] not in seen and article["title"] not in seen:
                seen.add(article["link"])
                seen.add(article["title"])
                unique_articles.append(article)

        # Shuffle slightly to show variety
        random.shuffle(unique_articles)

        result = unique_articles[:limit]
        if result:
            return result

        logger.warning("Indian AI scraper returned 0 live results - using fallback content.")
        return get_fallback_articles("indian_ai", limit)
