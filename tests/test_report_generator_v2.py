import pytest

from services.report_generator import ReportGenerator

pytestmark = pytest.mark.integration

"""Tests for report generator service."""


class TestReportGenerator:
    """Tests for ReportGenerator."""

    def test_init(self) -> None:
        gen = ReportGenerator()
        assert gen is not None

    def test_format_section_with_articles(self) -> None:
        gen = ReportGenerator()
        articles = [
            {"title": "AI Breakthrough", "source": "TechCrunch", "link": "http://example.com"},
            {"title": "New Model", "source": "MIT News", "link": "http://example.com/2"},
        ]
        result = gen._format_section("News", articles)
        assert result is not None
        assert "AI Breakthrough" in result

    def test_format_section_empty_articles(self) -> None:
        gen = ReportGenerator()
        result = gen._format_section("News", [])
        assert result is not None
        assert "No updates available" in result
