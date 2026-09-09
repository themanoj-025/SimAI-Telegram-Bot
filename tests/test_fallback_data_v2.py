"""Tests for fallback data provider."""

from scrapers.fallback_data import FALLBACK_CONTENT, get_fallback_articles


class TestFallbackData:
    """Tests for get_fallback_articles."""

    def test_returns_list(self) -> None:
        articles = get_fallback_articles("news")
        assert isinstance(articles, list)

    def test_has_required_fields(self) -> None:
        articles = get_fallback_articles("news")
        for article in articles[:5]:
            assert "title" in article
            assert "link" in article

    def test_fallback_articles_not_empty(self) -> None:
        assert len(FALLBACK_CONTENT) > 0

    def test_returns_subset(self) -> None:
        articles = get_fallback_articles("news", limit=3)
        assert len(articles) == 3

    def test_unknown_category_returns_empty(self) -> None:
        assert get_fallback_articles("nonexistent_category_xyz") == []
