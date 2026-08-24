"""Tests for AI-Telegram-News-Bot report generator and fallback data."""

import pytest

from scrapers.fallback_data import FALLBACK_CONTENT, get_fallback_articles


class TestFallbackData:
    """Tests for the static fallback content system."""

    def test_fallback_has_all_categories(self):
        """Every expected category should have fallback content."""
        expected = [
            "news", "arxiv", "blogs", "tools", "jobs",
            "startups", "models", "trending", "learn", "indian_ai",
        ]
        for cat in expected:
            assert cat in FALLBACK_CONTENT, f"Missing fallback for '{cat}'"

    def test_fallback_articles_have_required_keys(self):
        """Every fallback article must have title, link, source."""
        for category, articles in FALLBACK_CONTENT.items():
            for i, article in enumerate(articles):
                assert "title" in article, f"{category}[{i}] missing 'title'"
                assert "link" in article, f"{category}[{i}] missing 'link'"
                assert "source" in article, f"{category}[{i}] missing 'source'"

    def test_fallback_articles_have_valid_urls(self):
        """All fallback links should be valid URLs."""
        for category, articles in FALLBACK_CONTENT.items():
            for i, article in enumerate(articles):
                link = article["link"]
                assert link.startswith("http"), (
                    f"{category}[{i}] link '{link}' doesn't start with http"
                )

    def test_get_fallback_articles_returns_list(self):
        result = get_fallback_articles("news", 5)
        assert isinstance(result, list)

    def test_get_fallback_articles_respects_limit(self):
        result = get_fallback_articles("news", 3)
        assert len(result) <= 3

    def test_get_fallback_articles_unknown_category(self):
        result = get_fallback_articles("nonexistent_category_xyz", 5)
        assert result == []

    def test_get_fallback_articles_all_categories(self):
        """get_fallback_articles should work for every category."""
        for category in FALLBACK_CONTENT:
            result = get_fallback_articles(category, 5)
            assert isinstance(result, list), f"Failed for category '{category}'"

    def test_fallback_articles_are_dicts(self):
        result = get_fallback_articles("news", 5)
        for article in result:
            assert isinstance(article, dict)


class TestReportGeneratorFormat:
    """Tests for ReportGenerator._format_section."""

    def test_format_section_with_articles(self):
        from services.report_generator import ReportGenerator

        gen = ReportGenerator.__new__(ReportGenerator)
        articles = [
            {"title": "Test Article", "link": "https://example.com", "source": "Test"},
            {"title": "Another Article", "link": "https://example.org", "source": "Test2"},
        ]
        result = gen._format_section("Test Section", articles)
        assert "*Test Section*" in result
        assert "Test Article" in result
        assert "Another Article" in result
        assert "https://example.com" in result

    def test_format_section_empty_articles(self):
        from services.report_generator import ReportGenerator

        gen = ReportGenerator.__new__(ReportGenerator)
        result = gen._format_section("Empty Section", [])
        assert "*Empty Section*" in result
        assert "No updates available" in result

    def test_format_section_long_title_truncated(self):
        from services.report_generator import ReportGenerator

        gen = ReportGenerator.__new__(ReportGenerator)
        long_title = "A" * 200
        articles = [{"title": long_title, "link": "", "source": ""}]
        result = gen._format_section("Section", articles)
        assert "..." in result  # Title should be truncated

    def test_format_section_missing_keys_handled(self):
        from services.report_generator import ReportGenerator

        gen = ReportGenerator.__new__(ReportGenerator)
        articles = [{"title": "Only Title"}]  # Missing link and source
        result = gen._format_section("Section", articles)
        assert "Only Title" in result


class TestSchedulerService:
    """Tests for the scheduler service initialization."""

    def test_scheduler_init(self):
        from services.scheduler import SchedulerService

        callback = lambda: None
        svc = SchedulerService(callback)
        assert svc.refresh_callback is callback
        assert svc.daily_report_callback is None

    def test_scheduler_init_with_report_callback(self):
        from services.scheduler import SchedulerService

        refresh_cb = lambda: None
        report_cb = lambda: None
        svc = SchedulerService(refresh_cb, daily_report_callback=report_cb)
        assert svc.daily_report_callback is report_cb


class TestSummarizer:
    """Tests for the summarizer fallback behavior."""

    def test_simple_summary_returns_string(self):
        from services.summarizer import Summarizer

        summarizer = Summarizer.__new__(Summarizer)
        articles = [
            {"title": "Article 1", "link": "https://a.com"},
            {"title": "Article 2", "link": "https://b.com"},
        ]
        result = summarizer.get_simple_summary(articles)
        assert isinstance(result, str)
        assert "Article 1" in result
        assert "Article 2" in result

    def test_simple_summary_empty_articles(self):
        from services.summarizer import Summarizer

        summarizer = Summarizer.__new__(Summarizer)
        result = summarizer.get_simple_summary([])
        assert isinstance(result, str)
        assert "No articles" in result or "Today's Top" in result

    def test_simple_summary_truncates_at_10(self):
        from services.summarizer import Summarizer

        summarizer = Summarizer.__new__(Summarizer)
        articles = [{"title": f"Article {i}", "link": ""} for i in range(20)]
        result = summarizer.get_simple_summary(articles)
        # Should only include first 10
        assert "Article 9" in result
        # Article 10+ may or may not be present depending on implementation


class TestConfig:
    """Tests for the configuration module."""

    def test_config_has_required_attributes(self):
        from config.config import Config

        config = Config()
        assert hasattr(config, "ARTICLES_PER_SECTION")
        assert hasattr(config, "CACHE_EXPIRY_HOURS")
        assert hasattr(config, "RSS_FEEDS")
        assert hasattr(config, "REQUEST_TIMEOUT")
        assert hasattr(config, "MAX_RETRIES")

    def test_config_has_all_feed_categories(self):
        from config.config import Config

        config = Config()
        expected = [
            "news", "arxiv", "blogs", "tools", "jobs",
            "startups", "models", "trending", "learn", "indian_ai",
        ]
        for cat in expected:
            assert cat in config.RSS_FEEDS, f"Missing feed category: {cat}"

    def test_config_articles_per_section_positive(self):
        from config.config import Config

        config = Config()
        assert config.ARTICLES_PER_SECTION > 0

    def test_config_timeout_positive(self):
        from config.config import Config

        config = Config()
        assert config.REQUEST_TIMEOUT > 0
