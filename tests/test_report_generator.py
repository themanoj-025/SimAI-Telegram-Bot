"""Tests for ReportGenerator formatting and Article class."""


from scrapers.news_scraper import Article
from services.report_generator import ReportGenerator


class TestArticleClass:
    def test_init(self):
        a = Article(title="Test", link="https://example.com", source="TestSrc")
        assert a.title == "Test"
        assert a.link == "https://example.com"
        assert a.source == "TestSrc"
        assert a.published == ""

    def test_init_with_published(self):
        a = Article(title="T", link="L", source="S", published="2024-01-01")
        assert a.published == "2024-01-01"

    def test_to_dict(self):
        a = Article(title="Title", link="https://x.com", source="Src", published="2024")
        d = a.to_dict()
        assert d == {
            "title": "Title",
            "link": "https://x.com",
            "source": "Src",
            "published": "2024",
        }

    def test_to_dict_default_published(self):
        a = Article(title="T", link="L", source="S")
        d = a.to_dict()
        assert d["published"] == ""


class TestFormatSection:
    def setup_method(self):
        self.gen = ReportGenerator()

    def test_empty_articles(self):
        result = self.gen._format_section("Test Section", [])
        assert "*Test Section*" in result
        assert "No updates available" in result

    def test_with_dict_articles(self):
        articles = [
            {"title": "Article 1", "link": "https://a.com", "source": "Source A"},
            {"title": "Article 2", "link": "https://b.com", "source": "Source B"},
        ]
        result = self.gen._format_section("My Section", articles)
        assert "*My Section*" in result
        assert "Article 1" in result
        assert "Article 2" in result
        assert "https://a.com" in result
        assert "Source A" in result

    def test_with_article_objects(self):
        articles = [
            Article(title="Obj Article", link="https://c.com", source="Source C"),
        ]
        result = self.gen._format_section("Obj Section", articles)
        assert "Obj Article" in result
        assert "https://c.com" in result

    def test_long_title_truncated(self):
        long_title = "A" * 200
        articles = [{"title": long_title, "link": "https://x.com", "source": "S"}]
        result = self.gen._format_section("Section", articles)
        # Title should be truncated at 150 chars + "..."
        assert "..." in result
        assert long_title not in result  # Full title should not appear

    def test_missing_link_and_source(self):
        articles = [{"title": "No extras"}]
        result = self.gen._format_section("Section", articles)
        assert "No extras" in result
        assert "Link:" not in result
        assert "Source:" not in result

    def test_numbered_items(self):
        articles = [
            {"title": f"Art {i}", "link": "", "source": ""}
            for i in range(5)
        ]
        result = self.gen._format_section("Section", articles)
        assert "1." in result
        assert "5." in result
