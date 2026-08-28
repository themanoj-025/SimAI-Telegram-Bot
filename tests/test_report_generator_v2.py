"""Tests for report generator service."""

import pytest
from unittest.mock import MagicMock

from services.report_generator import ReportGenerator


class TestReportGenerator:
    """Tests for ReportGenerator."""

    def test_init(self):
        gen = ReportGenerator()
        assert gen is not None

    def test_generate_daily_summary(self):
        gen = ReportGenerator()
        articles = [
            {"title": "AI Breakthrough", "source": "TechCrunch", "link": "http://example.com"},
            {"title": "New Model", "source": "MIT News", "link": "http://example.com/2"},
        ]
        result = gen.generate_daily_summary(articles)
        assert result is not None
        assert "AI Breakthrough" in result

    def test_empty_articles(self):
        gen = ReportGenerator()
        result = gen.generate_daily_summary([])
        assert result is not None
