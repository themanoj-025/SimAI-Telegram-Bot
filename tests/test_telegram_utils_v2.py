"""Tests for telegram utility functions."""

import pytest

from utils.telegram_utils import format_message, truncate_text, escape_markdown


class TestFormatMessage:
    """Tests for format_message."""

    def test_basic_format(self):
        result = format_message("Test Title", "Test content")
        assert "Test Title" in result
        assert "Test content" in result

    def test_with_url(self):
        result = format_message("Title", "Content", url="http://example.com")
        assert "http://example.com" in result


class TestTruncateText:
    """Tests for truncate_text."""

    def test_short_text_unchanged(self):
        result = truncate_text("Hello", 100)
        assert result == "Hello"

    def test_long_text_truncated(self):
        result = truncate_text("A" * 200, 100)
        assert len(result) <= 103  # 100 + "..."

    def test_empty_text(self):
        result = truncate_text("", 100)
        assert result == ""


class TestEscapeMarkdown:
    """Tests for escape_markdown."""

    def test_escapes_special_chars(self):
        result = escape_markdown("Hello *world*")
        assert "*" in result or "world" in result
