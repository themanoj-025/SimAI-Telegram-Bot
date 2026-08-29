import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from config.config import Config

# Async-safe request ID via contextvars
try:
    import contextvars

    _request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
        "_request_id", default=""
    )
except ImportError:
    _request_id_var = cast(Any, None)


def set_request_id(request_id: str) -> None:
    """Set the current request ID for structured logging."""
    if _request_id_var is not None:
        _request_id_var.set(request_id)


def get_request_id() -> str:
    """Get the current request ID."""
    if _request_id_var is not None:
        return _request_id_var.get()
    return ""


class StructuredFormatter(logging.Formatter):
    """JSON structured log formatter for production log aggregation."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include request ID if available
        rid = get_request_id()
        if rid:
            log_entry["request_id"] = rid

        # Include extra fields
        for key in ("user_id", "chat_id", "category", "error"):
            val = getattr(record, key, None)
            if val is not None:
                log_entry[key] = val

        # Include exception info if present
        if record.exc_info and record.exc_info[1] is not None:
            log_entry["exception"] = {
                "type": type(record.exc_info[1]).__name__,
                "message": str(record.exc_info[1]),
            }

        return json.dumps(log_entry, ensure_ascii=False, default=str)


class ReadableFormatter(logging.Formatter):
    """Human-readable formatter for console output."""

    def format(self, record: logging.LogRecord) -> str:
        rid = get_request_id()
        prefix = f"[{rid}] " if rid else ""
        return f"{prefix}{recordasctime} - {record.name} - {record.levelname} - {record.getMessage()}"


def _ensure_utf8_console() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, OSError):
                pass


def setup_logger(name: str = "ai_daily_bot") -> logging.Logger:
    """Set up structured logging with JSON file output and readable console output."""
    _ensure_utf8_console()
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    if logger.handlers:
        return logger

    # Console handler — human-readable
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ReadableFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(console_handler)

    # File handler — structured JSON
    log_file = Path(Config.LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(StructuredFormatter())
    logger.addHandler(file_handler)

    return logger
