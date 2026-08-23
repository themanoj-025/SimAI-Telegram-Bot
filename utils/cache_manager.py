import json
import os
import sqlite3
from datetime import datetime, timedelta

from utils.logger import setup_logger

logger = setup_logger(__name__)


class CacheManager:
    def __init__(self, db_path=None) -> None:
        if db_path is None:
            db_path = os.getenv("DATABASE_PATH", "bot_cache.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cache (
                        category TEXT,
                        data TEXT,
                        last_updated TIMESTAMP
                    )
                """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS seen_items (
                        category TEXT,
                        item_id TEXT,
                        first_seen TIMESTAMP,
                        PRIMARY KEY (category, item_id)
                    )
                """
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error initializing SQLite cache database: {e}")

    def get_cached_data(self, category, max_age_hours=6) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT data, last_updated FROM cache WHERE category = ?",
                    (category,),
                )
                row = cursor.fetchone()

                if row:
                    data_str, last_updated_str = row
                    last_updated = datetime.fromisoformat(last_updated_str)
                    if datetime.now() - last_updated < timedelta(hours=max_age_hours):
                        return json.loads(data_str)
            return None
        except (sqlite3.Error, json.JSONDecodeError) as e:
            logger.error(f"Error reading from cache: {e}")
            return None

    def get_latest_cached_data(self, category) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT data FROM cache WHERE category = ? ORDER BY last_updated DESC LIMIT 1",
                    (category,),
                )
                row = cursor.fetchone()
                return json.loads(row[0]) if row else None
        except (sqlite3.Error, json.JSONDecodeError) as e:
            logger.error(f"Error fetching latest cached data: {e}")
            return None

    def update_cache(self, category, data) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cache WHERE category = ?", (category,))
                cursor.execute(
                    "INSERT INTO cache (category, data, last_updated) VALUES (?, ?, ?)",
                    (category, json.dumps(data), datetime.now().isoformat()),
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error updating cache: {e}")

    def is_duplicate(self, category, item_id) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT 1 FROM seen_items WHERE category = ? AND item_id = ?",
                    (category, item_id),
                )
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Error checking duplicate: {e}")
            return False

    def mark_as_seen(self, category, item_id) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO seen_items (category, item_id, first_seen) VALUES (?, ?, ?)",
                    (category, item_id, datetime.now().isoformat()),
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error marking item as seen: {e}")

    def clear_old_seen_items(self, days=30) -> None:
        try:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM seen_items WHERE first_seen < ?", (cutoff,))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error clearing old seen items: {e}")
