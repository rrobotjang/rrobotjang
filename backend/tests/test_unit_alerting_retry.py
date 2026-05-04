"""Tests for alerting retry behavior."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.services import alerting


@pytest.mark.asyncio
async def test_post_with_retry_retries_three_times_before_success(monkeypatch):
    """_post_with_retry should attempt up to three API calls before succeeding."""
    post_mock = AsyncMock(side_effect=[Exception("boom1"), Exception("boom2"), SimpleNamespace(status_code=200)])

    class DummyClient:
        """Minimal async client that exposes a mocked post method."""

        async def __aenter__(self):
            """Enter async context for the client mock."""
            return self

        async def __aexit__(self, exc_type, exc, tb):
            """Exit async context for the client mock."""
            return None

        post = post_mock

    monkeypatch.setattr(alerting.httpx, "AsyncClient", lambda timeout=5: DummyClient())

    ok = await alerting._post_with_retry("https://example.com", {"text": "x"}, {200}, retries=3)

    assert ok is True
    assert post_mock.await_count == 3


@pytest.mark.asyncio
async def test_post_with_retry_returns_false_after_three_failures(monkeypatch):
    """_post_with_retry should return False if all three attempts fail."""
    post_mock = AsyncMock(side_effect=[Exception("boom")] * 3)

    class DummyClient:
        """Minimal async client that exposes a mocked post method."""

        async def __aenter__(self):
            """Enter async context for the client mock."""
            return self

        async def __aexit__(self, exc_type, exc, tb):
            """Exit async context for the client mock."""
            return None

        post = post_mock

    monkeypatch.setattr(alerting.httpx, "AsyncClient", lambda timeout=5: DummyClient())

    ok = await alerting._post_with_retry("https://example.com", {"text": "x"}, {200}, retries=3)

    assert ok is False
    assert post_mock.await_count == 3
