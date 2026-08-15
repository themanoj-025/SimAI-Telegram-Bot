import asyncio
import os
import sys

# Ensure the repository root is importable regardless of where this script
# is invoked from (repo root or a subdirectory such as scripts/).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.github_scraper import GitHubScraper
from scrapers.news_scraper import NewsScraper, YouTubeScraper
from services.report_generator import ReportGenerator


def safe_console_text(text: str) -> str:
    return text.encode("ascii", errors="replace").decode("ascii")


async def test_scrapers():
    print("Starting Async Scrapers Verification...")

    report_gen = ReportGenerator()

    try:
        print("\n--- Testing NewsScraper ---")
        news_scraper = NewsScraper()
        articles = await news_scraper.fetch_news(limit=3)
        print(f"FETCHED {len(articles)} news articles.")
        for article in articles:
            print(
                f"  * {safe_console_text(article.title[:50])}... ({safe_console_text(article.source)})"
            )

        print("\n--- Testing YouTubeScraper ---")
        yt_scraper = YouTubeScraper()
        videos = await yt_scraper.fetch_youtube(limit=3)
        print(f"FETCHED {len(videos)} YouTube videos.")
        for video in videos:
            print(
                f"  * {safe_console_text(video.title[:50])}... ({safe_console_text(video.source)})"
            )

        print("\n--- Testing GitHubScraper ---")
        gh_scraper = GitHubScraper()
        repos = await gh_scraper.fetch_trending(limit=3)
        print(f"FETCHED {len(repos)} trending repos.")
        for repo in repos:
            print(
                f"  * {safe_console_text(repo['title'][:50])}... ({safe_console_text(repo['source'])})"
            )

        print("\n--- Testing Full Report Generation ---")
        report = await report_gen.generate_report("all")
        print(f"FULL report generated ({len(report)} chars).")
        print("Summary of first 500 chars:")
        print(safe_console_text(report[:500]) + "...")

    except Exception as e:
        print(f"ERROR: Verification failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await report_gen.cleanup()


if __name__ == "__main__":
    asyncio.run(test_scrapers())
