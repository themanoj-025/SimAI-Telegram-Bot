# syntax=docker/dockerfile:1
# ═══════════════════════════════════════════════════════════════════════
# AI Telegram News Bot — python-telegram-bot polling worker
#
# The bot runs long-polling against Telegram (no inbound HTTP port) and
# maintains a local SQLite cache (bot_cache.db) plus a log file, so the
# container needs a writable data volume mounted at /app/data.
#
# Usage:
#   docker build -t ai-news-bot .
#   docker compose up -d
# ═══════════════════════════════════════════════════════════════════════

# ── Base stage ─────────────────────────────────────────────────────────
FROM python:3.13-slim AS base

LABEL org.opencontainers.image.title="AI Daily Telegram News Bot"
LABEL org.opencontainers.image.description="AI-powered daily intelligence Telegram bot with 2-hour auto-refresh"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="AI-Daily"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# tini: proper PID-1 signal handling so SIGTERM reaches the bot process
RUN apt-get update && apt-get install -y --no-install-recommends \
        tini \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Deps stage ─────────────────────────────────────────────────────────
FROM base AS deps

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Runtime stage ──────────────────────────────────────────────────────
FROM deps AS prod

# Non-root runtime user
RUN useradd --create-home --uid 10001 botuser && \
    mkdir -p /app/data /app/logs && \
    chown -R botuser:botuser /app

COPY config/ ./config/
COPY scrapers/ ./scrapers/
COPY services/ ./services/
COPY utils/ ./utils/
COPY run_bot.py ./
COPY get_chat_id.py ./

USER botuser

# Data lives on a named volume so the SQLite cache survives restarts.
# The bot also writes ai_daily_bot.log — point LOG_FILE at /app/logs via
# the compose env override or a bind mount if persistence is wanted.
VOLUME ["/app/data"]

# No EXPOSE — this is an outbound-only polling worker.
# Liveness probe: verifies the run_bot.py process is actually alive by
# scanning /proc cmdlines (no extra packages needed on Debian slim).
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import glob; \
        alive = any('run_bot.py' in open(f, 'rb').read().decode(errors='ignore') \
                    for f in glob.glob('/proc/[0-9]*/cmdline')); \
        exit(0 if alive else 1)" || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "run_bot.py"]

# ── Dev stage ──────────────────────────────────────────────────────────
FROM deps AS dev

RUN useradd --create-home --uid 10001 botuser && \
    mkdir -p /app/data /app/logs && \
    chown -R botuser:botuser /app

# Dev tooling: pytest + test deps for running the test suite in-container
RUN pip install --no-cache-dir pytest pytest-asyncio pytest-cov flake8

COPY config/ ./config/
COPY scrapers/ ./scrapers/
COPY services/ ./services/
COPY utils/ ./utils/
COPY run_bot.py ./

USER botuser

CMD ["python", "run_bot.py"]
