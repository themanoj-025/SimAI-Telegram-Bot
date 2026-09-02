"""Tests for CacheManager — SQLite-based cache and dedup store."""

import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from utils.cache_manager import CacheManager

pytestmark = pytest.mark.integration



@pytest.fixture
def cache(tmp_path) -> None:
    """Create a CacheManager with a temporary SQLite database."""
    db_path = str(tmp_path / "test_cache.db")
    return CacheManager(db_path=db_path)


class TestCacheManagerInit:
    def test_creates_database_file(self, tmp_path) -> None:
        db_path = str(tmp_path / "new_cache.db")
        CacheManager(db_path=db_path)
        assert Path(db_path).exists()

    def test_creates_tables(self, cache) -> None:
        """Verify both cache and seen_items tables exist."""
        with sqlite3.connect(cache.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = {row[0] for row in cursor.fetchall()}
            assert "cache" in tables
            assert "seen_items" in tables


class TestUpdateAndGetCache:
    def test_update_and_get(self, cache) -> None:
        data = [{"title": "Article 1", "link": "https://example.com"}]
        cache.update_cache("news", data)
        result = cache.get_cached_data("news")
        assert result == data

    def test_get_missing_returns_none(self, cache) -> None:
        assert cache.get_cached_data("nonexistent") is None

    def test_cache_expiry(self, cache) -> None:
        """Data older than max_age_hours should not be returned."""
        data = [{"title": "Old article"}]
        cache.update_cache("old_category", data)

        # Manually backdate the timestamp
        with sqlite3.connect(cache.db_path) as conn:
            old_time = (datetime.now() - timedelta(hours=10)).isoformat()
            conn.execute(
                "UPDATE cache SET last_updated = ? WHERE category = ?",
                (old_time, "old_category"),
            )
            conn.commit()

        # Default max_age is 6 hours, so 10 hours old should expire
        assert cache.get_cached_data("old_category", max_age_hours=6) is None

    def test_cache_not_expired_within_window(self, cache) -> None:
        data = [{"title": "Fresh article"}]
        cache.update_cache("fresh_category", data)
        result = cache.get_cached_data("fresh_category", max_age_hours=6)
        assert result is not None

    def test_update_replaces_old_data(self, cache) -> None:
        cache.update_cache("cat", [{"v": 1}])
        cache.update_cache("cat", [{"v": 2}])
        result = cache.get_cached_data("cat")
        assert result == [{"v": 2}]

    def test_get_latest_cached_data(self, cache) -> None:
        cache.update_cache("cat", [{"v": 1}])
        time.sleep(0.01)
        cache.update_cache("cat", [{"v": 2}])
        result = cache.get_latest_cached_data("cat")
        assert result == [{"v": 2}]

    def test_get_latest_returns_none_for_missing(self, cache) -> None:
        assert cache.get_latest_cached_data("nope") is None


class TestDeduplication:
    def test_mark_and_check_seen(self, cache) -> None:
        assert cache.is_duplicate("cat", "item_1") is False
        cache.mark_as_seen("cat", "item_1")
        assert cache.is_duplicate("cat", "item_1") is True

    def test_different_categories_independent(self, cache) -> None:
        cache.mark_as_seen("cat_a", "item_1")
        assert cache.is_duplicate("cat_a", "item_1") is True
        assert cache.is_duplicate("cat_b", "item_1") is False

    def test_mark_as_seen_idempotent(self, cache) -> None:
        cache.mark_as_seen("cat", "item_1")
        cache.mark_as_seen("cat", "item_1")  # duplicate insert
        assert cache.is_duplicate("cat", "item_1") is True

    def test_clear_old_seen_items(self, cache) -> None:
        cache.mark_as_seen("cat", "old_item")
        # Backdate the item
        with sqlite3.connect(cache.db_path) as conn:
            old_time = (datetime.now() - timedelta(days=60)).isoformat()
            conn.execute(
                "UPDATE seen_items SET first_seen = ? WHERE item_id = ?",
                (old_time, "old_item"),
            )
            conn.commit()

        cache.clear_old_seen_items(days=30)
        assert cache.is_duplicate("cat", "old_item") is False

    def test_clear_preserves_recent_items(self, cache) -> None:
        cache.mark_as_seen("cat", "recent_item")
        cache.clear_old_seen_items(days=30)
        assert cache.is_duplicate("cat", "recent_item") is True


class TestEdgeCases:
    def test_empty_data(self, cache) -> None:
        cache.update_cache("empty", [])
        result = cache.get_cached_data("empty")
        assert result == []

    def test_none_category(self, cache) -> None:
        # Should not raise
        result = cache.get_cached_data(None)
        assert result is None

    def test_special_characters_in_data(self, cache) -> None:
        data = [{"title": "Unicode: 🎉🤖💡", "link": "https://example.com/Привет"}]
        cache.update_cache("unicode_cat", data)
        result = cache.get_cached_data("unicode_cat")
        assert result == data

    def test_large_data(self, cache) -> None:
        data = [{"id": i, "title": f"Article {i}"} for i in range(1000)]
        cache.update_cache("large", data)
        result = cache.get_cached_data("large")
        assert len(result) == 1000
