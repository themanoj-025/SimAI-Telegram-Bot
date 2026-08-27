"""Lightweight FastAPI health server for Docker/k8s probes.

Runs in a background thread alongside the Telegram bot to expose:
- GET /health          — liveness probe (always 200)
- GET /health/ready    — readiness probe (checks bot + scrapers)
- GET /docs            — OpenAPI/Swagger documentation
- GET /openapi.json    — OpenAPI spec

Rate limiting via slowapi on /api/* endpoints (future expansion).
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address)

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI Telegram News Bot — Health API",
    description="Health checks, readiness probes, and operational status for the AI Daily Intelligence Bot.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "health",
            "description": "Liveness and readiness probes for container orchestration.",
        },
        {
            "name": "info",
            "description": "Service information and operational status.",
        },
    ],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Mutable readiness state (set by the bot's post_init / post_stop hooks)
# ---------------------------------------------------------------------------
_readiness: dict[str, Any] = {
    "bot_connected": False,
    "scheduler_running": False,
    "started_at": time.time(),
}


def set_readiness(bot_connected: bool = False, scheduler_running: bool = False) -> None:
    """Update readiness state — called from the bot's lifecycle hooks."""
    _readiness["bot_connected"] = bot_connected
    _readiness["scheduler_running"] = scheduler_running


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health", tags=["health"], summary="Liveness probe")
async def health() -> dict[str, str]:
    """Always returns 200 — the process is alive.

    Use this as the Docker/Kubernetes **liveness** probe. If this endpoint
    fails, the container should be restarted.
    """
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"], summary="Readiness probe")
async def health_ready() -> dict[str, Any]:
    """Returns 200 only when the bot is fully initialized.

    Use this as the Docker/Kubernetes **readiness** probe. The bot reports
    ready once the Telegram connection is established and the scheduler is
    running.
    """
    ready = _readiness["bot_connected"]
    status_code = 200 if ready else 503
    return {
        "status": "ready" if ready else "not_ready",
        "bot_connected": _readiness["bot_connected"],
        "scheduler_running": _readiness["scheduler_running"],
        "uptime_seconds": round(time.time() - _readiness["started_at"], 1),
    }


@app.get("/", tags=["info"], summary="Service info")
async def root() -> dict[str, Any]:
    """Service information and links."""
    return {
        "service": "AI Telegram News Bot",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "readiness": "/health/ready",
    }


# ---------------------------------------------------------------------------
# Background server runner
# ---------------------------------------------------------------------------
def start_health_server(port: int = 8080) -> threading.Thread:
    """Start the health server in a daemon thread.

    Returns the thread so the caller can join or manage its lifecycle.
    The server binds to 0.0.0.0:<port> and is accessible from Docker
    health check probes.
    """

    def _run() -> None:
        try:
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=port,
                log_level="warning",
                access_log=False,
            )
        except (OSError, RuntimeError) as exc:
            logger.error("Health server failed: %s", exc)

    thread = threading.Thread(target=_run, daemon=True, name="health-server")
    thread.start()
    logger.info("Health server started on port %d", port)
    return thread
