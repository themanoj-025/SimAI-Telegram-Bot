import asyncio
import os
import sys

# Ensure the repository root is importable regardless of where this script
# is invoked from (repo root or a subdirectory such as tests/).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.indian_news_scraper import IndianAINewsScraper


async def test_indian_scraper() -> None:
    scraper = IndianAINewsScraper()
    print("Fetching Indian AI news...")
    news = await scraper.fetch_indian_ai_news(limit=10)
    print(f"\nFound {len(news)} articles:")
    for i, article in enumerate(news, 1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Link: {article['link']}")
        print("-" * 30)


if __name__ == "__main__":
    asyncio.run(test_indian_scraper())
