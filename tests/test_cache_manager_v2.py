"""Tests for CacheManager with SQLite storage."""

import os
import tempfile

import pytest

from utils.cache_manager import CacheManager


@pytest.fixture
def cache_db():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_cache.db")
        cm = CacheManager(db_path=db_path)
        yield cm


class TestCacheManager:
    """Tests for CacheManager CRUD operations."""

    def test_init_creates_tables(self, cache_db):
        assert cache_db is not None

    def test_update_and_get(self, cache_db):
        cache_db.update_cache("news", [{"title": "AI Breakthrough"}])
        data = cache_db.get_cached_data("news")
        assert data is not None
        assert len(data) == 1
        assert data[0]["title"] == "AI Breakthrough"

    def test_get_expired_returns_none(self, cache_db):
        cache_db.update_cache("news", [{"title": "test"}])
        # max_age_hours=0 means everything is expired
        data = cache_db.get_cached_data("news", max_age_hours=0)
        assert data is None

    def test_get_nonexistent_returns_none(self, cache_db):
        data = cache_db.get_cached_data("nonexistent")
        assert data is None

    def test_get_latest_cached(self, cache_db):
        cache_db.update_cache("news", [{"v": 1}])
        cache_db.update_cache("news", [{"v": 2}])
        data = cache_db.get_latest_cached_data("news")
        assert data[0]["v"] == 2

    def test_is_duplicate(self, cache_db):
        assert cache_db.is_duplicate("news", "item1") is False
        cache_db.mark_as_seen("news", "item1")
        assert cache_db.is_duplicate("news", "item1") is True

    def test_mark_as_seen_idempotent(self, cache_db):
        cache_db.mark_as_seen("news", "item1")
        cache_db.mark_as_seen("news", "item1")  # Should not raise
        assert cache_db.is_duplicate("news", "item1") is True

    def test_clear_old_seen_items(self, cache_db):
        cache_db.mark_as_seen("news", "old_item")
        # Clear items older than 0 days (all items)
        cache_db.clear_old_seen_items(days=0)
        assert cache_db.is_duplicate("news", "old_item") is False

    def test_different_categories(self, cache_db):
        cache_db.update_cache("news", [{"type": "news"}])
        cache_db.update_cache("github", [{"type": "github"}])
        assert cache_db.get_cached_data("news") is not None
        assert cache_db.get_cached_data("github") is not None
        assert cache_db.get_cached_data("twitter") is None
