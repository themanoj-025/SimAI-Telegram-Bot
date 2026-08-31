"""Tests for AI feature scrapers — compare, roadmap, leaderboard (no network)."""

import pytest

from scrapers.ai_features_scraper import (
    AICompareScraper,
    AILeaderboardScraper,
    AIRoadmapScraper,
)


class TestAICompareScraper:
    def setup_method(self) -> None:
        self.scraper = AICompareScraper()

    def test_compare_two_models(self) -> None:
        result = self.scraper.compare("GPT-4o vs Claude")
        assert "GPT-4o" in result
        assert "Claude" in result
        assert "Comparison" in result or "Comparison" in result.lower() or "vs" in result.lower()

    def test_compare_three_models(self) -> None:
        result = self.scraper.compare("GPT-4o vs Claude vs Gemini")
        assert "GPT-4o" in result
        assert "Claude" in result
        assert "Gemini" in result

    def test_compare_unknown_model_shows_help(self) -> None:
        result = self.scraper.compare("TotallyFakeModel")
        assert "No recognized" in result or "Supported" in result

    def test_compare_single_model_card(self) -> None:
        result = self.scraper.compare("GPT-4o")
        assert "GPT-4o" in result
        assert "OpenAI" in result

    def test_compare_case_insensitive(self) -> None:
        result = self.scraper.compare("gpt-4o vs CLAUDE")
        assert "GPT-4o" in result or "gpt-4o" in result.lower()
        assert "Claude" in result

    def test_compare_alias_resolution(self) -> None:
        result = self.scraper.compare("chatgpt vs gemini")
        assert "OpenAI" in result or "GPT" in result
        assert "Google" in result or "Gemini" in result

    def test_compare_model_with_extra_text(self) -> None:
        result = self.scraper.compare("Compare GPT-4o and Claude for coding")
        assert "GPT-4o" in result
        assert "Claude" in result

    def test_compare_deduplicates(self) -> None:
        result = self.scraper.compare("GPT-4o and GPT-4o")
        # Should only show GPT-4o once in the comparison
        assert result.count("GPT-4o") <= 3  # name + provider + maybe once more


class TestAIRoadmapScraper:
    def setup_method(self) -> None:
        self.scraper = AIRoadmapScraper()

    def test_ai_engineer_roadmap(self) -> None:
        result = self.scraper.get_roadmap("ai engineer")
        assert "AI Engineer" in result or "ai engineer" in result.lower()
        assert "Python" in result or "python" in result.lower()

    def test_machine_learning_roadmap(self) -> None:
        result = self.scraper.get_roadmap("machine learning")
        assert "Machine Learning" in result or "machine learning" in result.lower()

    def test_llm_engineer_roadmap(self) -> None:
        result = self.scraper.get_roadmap("llm engineer")
        assert "LLM" in result or "llm" in result.lower()

    def test_unknown_role_falls_back_to_default(self) -> None:
        result = self.scraper.get_roadmap("quantum wizard")
        assert "Python" in result or "python" in result.lower()

    def test_empty_role_uses_default(self) -> None:
        result = self.scraper.get_roadmap("")
        assert len(result) > 0

    def test_roadmap_has_steps(self) -> None:
        result = self.scraper.get_roadmap("ai engineer")
        # Roadmaps should have numbered steps
        assert "1." in result
        assert "2." in result


class TestAILeaderboardScraper:
    def setup_method(self) -> None:
        self.scraper = AILeaderboardScraper()

    @pytest.mark.asyncio
    async def test_leaderboard_returns_data(self) -> None:
        result = await self.scraper.get_leaderboard()
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_leaderboard_has_top_models(self) -> None:
        result = await self.scraper.get_leaderboard()
        # Should mention some well-known models
        result_lower = result.lower()
        assert any(
            name in result_lower
            for name in ["gpt", "claude", "gemini", "llama", "deepseek"]
        )

    @pytest.mark.asyncio
    async def test_leaderboard_with_filter(self) -> None:
        result = await self.scraper.get_leaderboard("openai")
        assert len(result) > 0
