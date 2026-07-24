import asyncio
import time

import pytest

from app.config import Settings
from app.models import Business, SearchRequest
from app.providers.base import BusinessProvider
from app.services import SearchService
from app.traffic import (
    AsyncRateGate,
    AsyncRequestCoalescer,
    AsyncTTLCache,
    SlidingWindowLimiter,
)


class CountingProvider(BusinessProvider):
    id = "sample"
    label = "Counting provider"

    def __init__(self) -> None:
        self.calls = 0

    async def search(self, request: SearchRequest) -> list[Business]:
        self.calls += 1
        await asyncio.sleep(0.01)
        return [Business(id="1", name="Cached Cafe", source="sample")]


@pytest.mark.asyncio
async def test_search_cache_avoids_repeated_provider_calls() -> None:
    provider = CountingProvider()
    service = SearchService({"sample": provider}, Settings(_env_file=None))
    request = SearchRequest(provider="sample", query="coffee", city="Amsterdam")

    first = await service.search(request)
    second = await service.search(request)

    assert first.meta.cache_hit is False
    assert second.meta.cache_hit is True
    assert provider.calls == 1


@pytest.mark.asyncio
async def test_identical_concurrent_requests_are_coalesced() -> None:
    calls = 0
    coalescer: AsyncRequestCoalescer[int] = AsyncRequestCoalescer()

    async def factory() -> int:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.02)
        return 42

    values = await asyncio.gather(*(coalescer.run("same", factory) for _ in range(5)))
    assert values == [42] * 5
    assert calls == 1


@pytest.mark.asyncio
async def test_ttl_cache_can_serve_stale_value() -> None:
    cache: AsyncTTLCache[str] = AsyncTTLCache()
    await cache.set("key", "value", ttl_seconds=0.01, stale_ttl_seconds=1)
    await asyncio.sleep(0.02)

    fresh = await cache.get("key")
    stale = await cache.get("key", allow_stale=True)

    assert fresh.value is None
    assert stale.value == "value"
    assert stale.is_fresh is False


@pytest.mark.asyncio
async def test_rate_gate_spaces_request_starts() -> None:
    gate = AsyncRateGate(0.02)
    started = time.monotonic()
    await gate.wait()
    await gate.wait()
    assert time.monotonic() - started >= 0.018


@pytest.mark.asyncio
async def test_client_limiter_returns_retry_after() -> None:
    limiter = SlidingWindowLimiter()
    assert (await limiter.allow("client", max_requests=2, window_seconds=60))[0]
    assert (await limiter.allow("client", max_requests=2, window_seconds=60))[0]
    allowed, retry_after = await limiter.allow("client", max_requests=2, window_seconds=60)
    assert allowed is False
    assert retry_after >= 1
