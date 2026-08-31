"""Tests for fallback_data — static fallback content provider."""


from scrapers.fallback_data import FALLBACK_CONTENT, get_fallback_articles


class TestGetFallbackArticles:
    def test_returns_known_category(self) -> None:
        articles = get_fallback_articles("news")
        assert len(articles) > 0
        assert all(isinstance(a, dict) for a in articles)

    def test_articles_have_required_keys(self) -> None:
        for category in FALLBACK_CONTENT:
            articles = get_fallback_articles(category)
            for article in articles:
                assert "title" in article
                assert "link" in article
                assert "source" in article

    def test_limit_works(self) -> None:
        articles = get_fallback_articles("news", limit=2)
        assert len(articles) == 2

    def test_limit_larger_than_available(self) -> None:
        articles = get_fallback_articles("news", limit=100)
        assert len(articles) == len(FALLBACK_CONTENT.get("news", []))

    def test_unknown_category_returns_empty(self) -> None:
        articles = get_fallback_articles("nonexistent_category")
        assert articles == []

    def test_limit_zero_returns_empty(self) -> None:
        articles = get_fallback_articles("news", limit=0)
        assert articles == []

    def test_all_categories_have_content(self) -> None:
        expected_categories = [
            "news", "arxiv", "blogs", "tools", "jobs",
            "startups", "models", "trending", "learn",
            "indian_ai", "github",
        ]
        for cat in expected_categories:
            articles = get_fallback_articles(cat)
            assert len(articles) > 0, f"Category '{cat}' has no fallback content"

    def test_links_are_valid_urls(self) -> None:
        articles = get_fallback_articles("news")
        for article in articles:
            assert article["link"].startswith("https://")

    def test_articles_are_dicts(self) -> None:
        for cat, articles in FALLBACK_CONTENT.items():
            for article in articles:
                assert isinstance(article, dict)
                assert isinstance(article["title"], str)
                assert isinstance(article["link"], str)
                assert isinstance(article["source"], str)
