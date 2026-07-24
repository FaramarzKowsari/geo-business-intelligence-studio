from __future__ import annotations

import asyncio
import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class CacheLookup(Generic[T]):
    value: T | None
    age_seconds: float | None
    is_fresh: bool


@dataclass(slots=True)
class _CacheEntry(Generic[T]):
    value: T
    stored_at: float
    expires_at: float
    stale_until: float


class AsyncTTLCache(Generic[T]):
    """Small process-local cache with optional stale-if-error retention."""

    def __init__(self, max_entries: int = 512) -> None:
        self.max_entries = max_entries
        self._entries: dict[str, _CacheEntry[T]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str, *, allow_stale: bool = False) -> CacheLookup[T]:
        now = time.monotonic()
        async with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return CacheLookup(None, None, False)
            if now > entry.stale_until:
                self._entries.pop(key, None)
                return CacheLookup(None, None, False)
            is_fresh = now <= entry.expires_at
            if not is_fresh and not allow_stale:
                return CacheLookup(None, now - entry.stored_at, False)
            return CacheLookup(entry.value, now - entry.stored_at, is_fresh)

    async def set(
        self,
        key: str,
        value: T,
        *,
        ttl_seconds: float,
        stale_ttl_seconds: float = 0,
    ) -> None:
        now = time.monotonic()
        async with self._lock:
            if len(self._entries) >= self.max_entries and key not in self._entries:
                oldest_key = min(self._entries, key=lambda item: self._entries[item].stored_at)
                self._entries.pop(oldest_key, None)
            self._entries[key] = _CacheEntry(
                value=value,
                stored_at=now,
                expires_at=now + max(ttl_seconds, 0),
                stale_until=now + max(ttl_seconds + stale_ttl_seconds, ttl_seconds),
            )

    async def clear(self) -> None:
        async with self._lock:
            self._entries.clear()

    async def size(self) -> int:
        async with self._lock:
            return len(self._entries)


class AsyncRequestCoalescer(Generic[T]):
    """Lets concurrent identical requests share one upstream operation."""

    def __init__(self) -> None:
        self._inflight: dict[str, asyncio.Task[T]] = {}
        self._lock = asyncio.Lock()

    async def run(self, key: str, factory: Callable[[], Awaitable[T]]) -> T:
        async with self._lock:
            task = self._inflight.get(key)
            if task is None:
                task = asyncio.create_task(factory())
                self._inflight[key] = task
        try:
            return await asyncio.shield(task)
        finally:
            if task.done():
                async with self._lock:
                    if self._inflight.get(key) is task:
                        self._inflight.pop(key, None)


class AsyncRateGate:
    """Serializes upstream requests and enforces a minimum start interval."""

    def __init__(self, minimum_interval_seconds: float) -> None:
        self.minimum_interval_seconds = max(minimum_interval_seconds, 0)
        self._last_started = 0.0
        self._lock = asyncio.Lock()

    async def wait(self) -> None:
        async with self._lock:
            now = time.monotonic()
            remaining = self.minimum_interval_seconds - (now - self._last_started)
            if remaining > 0:
                await asyncio.sleep(remaining)
            self._last_started = time.monotonic()


class SlidingWindowLimiter:
    """Process-local client limiter for public endpoints."""

    def __init__(self) -> None:
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def allow(
        self,
        key: str,
        *,
        max_requests: int,
        window_seconds: float,
    ) -> tuple[bool, int]:
        now = time.monotonic()
        cutoff = now - window_seconds
        async with self._lock:
            events = self._events[key]
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= max_requests:
                retry_after = max(1, int(events[0] + window_seconds - now) + 1)
                return False, retry_after
            events.append(now)
            return True, 0
