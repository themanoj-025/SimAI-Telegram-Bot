"""Tests for fallback data provider."""


from scrapers.fallback_data import FALLBACK_ARTICLES, get_fallback_articles


class TestFallbackData:
    """Tests for get_fallback_articles."""

    def test_returns_list(self) -> None:
        articles = get_fallback_articles()
        assert isinstance(articles, list)

    def test_has_required_fields(self) -> None:
        articles = get_fallback_articles()
        for article in articles[:5]:
            assert "title" in article
            assert "link" in article

    def test_fallback_articles_not_empty(self) -> None:
        assert len(FALLBACK_ARTICLES) > 0

    def test_returns_subset(self) -> None:
        articles = get_fallback_articles(limit=3)
        assert len(articles) == 3
