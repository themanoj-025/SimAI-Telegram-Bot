import asyncio

import pytest

from scrapers.indian_news_scraper import IndianAINewsScraper

pytestmark = pytest.mark.integration


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
