import asyncio

import pytest

from scrapers.twitter_scraper import TwitterScraper

pytestmark = pytest.mark.integration


async def test_twitter_scraper() -> None:
    print("Testing TwitterScraper...")
    scraper = TwitterScraper()
    tweets = await scraper.fetch_tweets(limit=5)

    if tweets:
        print(f"Successfully fetched {len(tweets)} tweets:")
        for i, tweet in enumerate(tweets, 1):
            print(f"{i}. {tweet['title'][:50]}... from {tweet['source']}")
            print(f"   Link: {tweet['link']}")
    else:
        print("Failed to fetch any tweets.")


if __name__ == "__main__":
    asyncio.run(test_twitter_scraper())
