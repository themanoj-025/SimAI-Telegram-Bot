import logging
from pathlib import Path
from unittest.mock import patch

import pytest

from utils.logger import setup_logger

pytestmark = pytest.mark.unit

"""Tests for logger — setup_logger and _ensure_utf8_console."""




class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger = setup_logger("test_logger_returns")
        assert isinstance(logger, logging.Logger)

    def test_logger_name(self) -> None:
        logger = setup_logger("test_my_unique_name")
        assert logger.name == "test_my_unique_name"

    def test_default_name(self) -> None:
        logger = setup_logger()
        assert logger.name == "ai_daily_bot"

    def test_logger_has_handlers(self) -> None:
        logger = setup_logger("test_handlers_check")
        assert len(logger.handlers) >= 2  # console + file

    def test_logger_level_from_config(self) -> None:
        logger = setup_logger("test_level_check")
        # Config.LOG_LEVEL defaults to "INFO"
        assert logger.level == logging.INFO

    def test_repeated_setup_doesnt_duplicate_handlers(self) -> None:
        name = "test_no_duplicates"
        logger1 = setup_logger(name)
        handler_count_1 = len(logger1.handlers)
        logger2 = setup_logger(name)
        handler_count_2 = len(logger2.handlers)
        assert handler_count_1 == handler_count_2

    def test_creates_log_file(self, tmp_path) -> None:
        log_file = str(tmp_path / "test.log")
        with patch("utils.logger.Config") as mock_config:
            mock_config.LOG_LEVEL = "INFO"
            mock_config.LOG_FILE = log_file
            logger = setup_logger("test_file_creation")
            # The logger setup creates the file handler
            # Trigger a log message to ensure the handler writes
            logger.info("test message")

        assert Path(log_file).exists()

    def test_logger_can_log(self) -> None:
        logger = setup_logger("test_can_log")
        # Should not raise
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")


class TestEnsureUtf8Console:
    def test_no_crash(self) -> None:
        # Should not raise
        _ensure_utf8_console()
