"""Tests for the FastAPI health server."""

import time
from unittest.mock import patch

from fastapi.testclient import TestClient

import health_server
from health_server import app, set_readiness


class TestHealthServer:
    """Tests for the health endpoints (liveness / readiness / info)."""

    def test_liveness_returns_ok(self) -> None:
        client = TestClient(app)
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_liveness_endpoint_in_result(self) -> None:
        client = TestClient(app)
        resp = client.get("/health")
        assert "status" in resp.json()

    def test_readiness_not_ready_by_default(self) -> None:
        set_readiness(bot_connected=False, scheduler_running=False)
        client = TestClient(app)
        resp = client.get("/health/ready")
        assert resp.status_code == 503
        body = resp.json()
        assert body["status"] == "not_ready"
        assert body["bot_connected"] is False

    def test_readiness_ready_when_bot_connected(self) -> None:
        set_readiness(bot_connected=True, scheduler_running=True)
        try:
            client = TestClient(app)
            resp = client.get("/health/ready")
            assert resp.status_code == 200
            body = resp.json()
            assert body["status"] == "ready"
            assert body["bot_connected"] is True
        finally:
            set_readiness(bot_connected=False, scheduler_running=False)

    def test_root_lists_endpoints(self) -> None:
        client = TestClient(app)
        resp = client.get("/")
        assert resp.status_code == 200
        body = resp.json()
        assert body["health"] == "/health"
        assert body["readiness"] == "/health/ready"

    def test_metrics_endpoint_exists(self) -> None:
        client = TestClient(app)
        resp = client.get("/metrics")
        # 200 with prometheus_client installed, plain-text either way
        assert resp.status_code == 200

    def test_readiness_uptime_is_number(self) -> None:
        with patch.object(health_server, "_readiness", {"bot_connected": False, "scheduler_running": False, "started_at": time.time() - 10}):
            client = TestClient(app)
            resp = client.get("/health/ready")
            assert resp.status_code == 503
            assert isinstance(resp.json()["uptime_seconds"], float)
