from bs4 import BeautifulSoup

from scrapers.async_base_scraper import AsyncBaseScraper
from scrapers.fallback_data import get_fallback_articles
from utils.logger import setup_logger

logger = setup_logger(__name__)


class GitHubScraper(AsyncBaseScraper):
    def __init__(self):
        super().__init__()
        self.trending_url = "https://github.com/trending?since=weekly"

    async def fetch_trending(self, limit: int = 5) -> list[dict]:
        html = await self.fetch_url(self.trending_url, timeout=10)
        articles = self._parse_trending_html(html, limit) if html else []
        if articles:
            return articles

        logger.warning("GitHub scraper returned 0 live results - using fallback content.")
        return get_fallback_articles("github", limit)

    def _parse_trending_html(self, html: str, limit: int) -> list[dict]:
        articles = []
        soup = BeautifulSoup(html, "html.parser")
        repositories = soup.select(
            "article.Box-row, article.box-row, article.Box, article.box-border"
        )

        for repo in repositories:
            try:
                title_elem = repo.select_one("h2 a")
                if not title_elem:
                    continue

                full_name = title_elem.get("href", "").strip("/")
                title = " ".join(title_elem.get_text(" ", strip=True).split())

                description_elem = repo.select_one("p")
                description = (
                    " ".join(description_elem.get_text(" ", strip=True).split())
                    if description_elem
                    else ""
                )

                stars_elem = repo.select_one("a[href$='/stargazers']")
                stars = stars_elem.get_text(" ", strip=True) if stars_elem else ""

                articles.append(
                    {
                        "title": f"{title} {description}".strip(),
                        "link": f"https://github.com/{full_name}",
                        "source": f"GitHub {stars}".strip(),
                        "published": "",
                    }
                )
            except Exception as e:
                logger.warning(f"Error parsing GitHub repo: {e}")

            if len(articles) >= limit:
                break

        return articles[:limit]
