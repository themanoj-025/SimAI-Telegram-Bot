import asyncio
from datetime import datetime

from config.config import Config
from scrapers.ai_features_scraper import (
    AICompareScraper,
    AILeaderboardScraper,
    AIRoadmapScraper,
)
from scrapers.extended_scrapers import (
    JobScraper,
    LearnScraper,
    ModelScraper,
    StartupScraper,
    ToolScraper,
    TrendingScraper,
)
from scrapers.github_scraper import GitHubScraper
from scrapers.indian_news_scraper import IndianAINewsScraper
from scrapers.news_scraper import ArxivScraper, BlogScraper, NewsScraper, YouTubeScraper
from scrapers.twitter_scraper import TwitterScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ReportGenerator:
    def __init__(self):
        self.config = Config()
        self.news_scraper = NewsScraper()
        self.arxiv_scraper = ArxivScraper()
        self.blog_scraper = BlogScraper()
        self.github_scraper = GitHubScraper()
        self.indian_scraper = IndianAINewsScraper()
        self.youtube_scraper = YouTubeScraper()
        self.tool_scraper = ToolScraper()
        self.job_scraper = JobScraper()
        self.startup_scraper = StartupScraper()
        self.model_scraper = ModelScraper()
        self.trending_scraper = TrendingScraper()
        self.learn_scraper = LearnScraper()
        self.twitter_scraper = TwitterScraper()
        self.compare_scraper = AICompareScraper()
        self.roadmap_scraper = AIRoadmapScraper()
        self.leaderboard_scraper = AILeaderboardScraper()

    async def cleanup(self):
        """Reserved for future async cleanup hooks."""
        return

    async def generate_report(self, category: str = "all", force_refresh: bool = False) -> str:
        logger.info(f"Generating report for category: {category} (Force: {force_refresh})")

        limit = self.config.ARTICLES_PER_SECTION
        date_str = datetime.now().strftime("%B %d, %Y")

        if category == "all":
            report = f"*AI Daily Brief*\n\n*Date:* {date_str}\n\n"
            tasks = [
                self.news_scraper.fetch_news(limit),
                self.arxiv_scraper.fetch_papers(limit),
                self.tool_scraper.fetch_tools(limit, force_refresh),
                self.github_scraper.fetch_trending(limit),
                self.startup_scraper.fetch_startups(limit, force_refresh),
                self.model_scraper.fetch_models(limit, force_refresh),
                self.indian_scraper.fetch_indian_ai_news(limit),
                self.youtube_scraper.fetch_youtube(limit),
            ]
            headers = [
                "News",
                "Research Papers",
                "Tools",
                "GitHub Trending",
                "Startups and Funding",
                "Model Releases",
                "Indian AI News",
                "YouTube",
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for header, result in zip(headers, results):
                if isinstance(result, Exception):
                    logger.error(f"Error fetching section {header}: {result}")
                    report += self._format_section(header, [])
                else:
                    report += self._format_section(header, result)

            return report

        category_map = {
            "news": ("Global AI News", lambda: self.news_scraper.fetch_news(limit)),
            "papers": (
                "Research Papers",
                lambda: self.arxiv_scraper.fetch_papers(limit),
            ),
            "blogs": ("AI Blogs", lambda: self.blog_scraper.fetch_blogs(limit)),
            "tools": (
                "AI Tool Discovery",
                lambda: self.tool_scraper.fetch_tools(limit, force_refresh),
            ),
            "jobs": (
                "AI Jobs",
                lambda: self.job_scraper.fetch_jobs(limit, force_refresh),
            ),
            "startups": (
                "AI Startups and Funding",
                lambda: self.startup_scraper.fetch_startups(limit, force_refresh),
            ),
            "models": (
                "AI Model Releases",
                lambda: self.model_scraper.fetch_models(limit, force_refresh),
            ),
            "trending": (
                "AI Community Trends",
                lambda: self.trending_scraper.fetch_trending(limit, force_refresh),
            ),
            "learn": (
                "AI Learning Resources",
                lambda: self.learn_scraper.fetch_learn(limit, force_refresh),
            ),
            "india": (
                "Indian AI News",
                lambda: self.indian_scraper.fetch_indian_ai_news(limit),
            ),
            "youtube": (
                "Latest AI YouTube News",
                lambda: self.youtube_scraper.fetch_youtube(limit),
            ),
            "twitter": (
                "Latest AI Posts from X",
                lambda: self.twitter_scraper.fetch_tweets(limit),
            ),
        }

        if category not in category_map:
            return "Invalid category selected."

        title, loader = category_map[category]
        return self._format_section(title, await loader())

    async def generate_compare(self, models_input: str) -> str:
        return self.compare_scraper.compare(models_input)

    async def generate_roadmap(self, role_input: str) -> str:
        return self.roadmap_scraper.get_roadmap(role_input)

    async def generate_leaderboard(self, filter_input: str = "") -> str:
        return await self.leaderboard_scraper.get_leaderboard(filter_input)

    def _format_section(self, title: str, articles: list) -> str:
        section = f"*{title}*\n"
        if not articles:
            return section + "- No updates available\n\n"

        for index, article in enumerate(articles, 1):
            title_text = (
                article.get("title", "No Title")
                if isinstance(article, dict)
                else getattr(article, "title", "No Title")
            )
            link = (
                article.get("link", "")
                if isinstance(article, dict)
                else getattr(article, "link", "")
            )
            source = (
                article.get("source", "")
                if isinstance(article, dict)
                else getattr(article, "source", "")
            )

            safe_title = title_text[:150] + "..." if len(title_text) > 150 else title_text
            section += f"{index}. {safe_title}\n"
            if link:
                section += f"   Link: {link}\n"
            if source:
                section += f"   Source: {source}\n"
            section += "\n"

        return section
