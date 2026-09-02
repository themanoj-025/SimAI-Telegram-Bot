import pytest

from services.summarizer import Summarizer
        import asyncio
pytestmark = pytest.mark.integration

"""Tests for summarizer service."""




class TestSummarizer:
    """Tests for Summarizer."""

    def test_simple_summary_no_model(self) -> None:
        summarizer = Summarizer()
        # Force no model
        summarizer.model = None
        articles = [
            {"title": "AI Breakthrough", "link": "http://example.com/1"},
            {"title": "New Model Released", "link": "http://example.com/2"},
        ]
        result = summarizer.get_simple_summary(articles)
        assert "AI Breakthrough" in result
        assert "New Model Released" in result

    def test_simple_summary_empty_articles(self) -> None:
        summarizer = Summarizer()
        summarizer.model = None
        result = summarizer.get_simple_summary([])
        assert "Top AI Stories" in result

    def test_summarize_no_articles(self) -> None:
        summarizer = Summarizer()
        summarizer.model = None
        result = asyncio.run(summarizer.summarize_articles([]))
        assert "No articles" in result
