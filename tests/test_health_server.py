"""Tests for health check server."""

import pytest
from unittest.mock import MagicMock, patch

from health_server import HealthServer


class TestHealthServer:
    """Tests for HealthServer."""

    def test_init(self):
        server = HealthServer()
        assert server is not None

    def test_health_endpoint_returns_ok(self):
        server = HealthServer()
        # The health endpoint should return a status dict
        result = server.get_health()
        assert "status" in result
