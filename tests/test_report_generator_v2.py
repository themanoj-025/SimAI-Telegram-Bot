"""Tests for report generator service."""


from services.report_generator import ReportGenerator


class TestReportGenerator:
    """Tests for ReportGenerator."""

    def test_init(self) -> None:
        gen = ReportGenerator()
        assert gen is not None

    def test_generate_daily_summary(self) -> None:
        gen = ReportGenerator()
        articles = [
            {"title": "AI Breakthrough", "source": "TechCrunch", "link": "http://example.com"},
            {"title": "New Model", "source": "MIT News", "link": "http://example.com/2"},
        ]
        result = gen.generate_daily_summary(articles)
        assert result is not None
        assert "AI Breakthrough" in result

    def test_empty_articles(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_daily_summary([])
        assert result is not None
