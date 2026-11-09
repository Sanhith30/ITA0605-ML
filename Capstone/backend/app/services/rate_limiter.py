"""
Simple in-memory rate limiter: max 30 requests per minute per IP.
Uses a sliding window of timestamps stored per IP address.
"""
import time
from collections import defaultdict, deque
from fastapi import Request, HTTPException, status

RATE_LIMIT = 30         # requests
WINDOW_SECONDS = 60     # per minute

# ip -> deque of UNIX timestamps for recent requests
_request_log: dict[str, deque] = defaultdict(deque)


def get_client_ip(request: Request) -> str:
    """Extract client IP, respecting X-Forwarded-For when present."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def enforce_rate_limit(request: Request) -> None:
    """
    Call at the start of a route handler to enforce rate limiting.
    Raises HTTP 429 if the client has exceeded RATE_LIMIT requests
    within WINDOW_SECONDS.
    """
    ip = get_client_ip(request)
    now = time.monotonic()
    window_start = now - WINDOW_SECONDS

    timestamps = _request_log[ip]

    # Drop entries outside the sliding window
    while timestamps and timestamps[0] < window_start:
        timestamps.popleft()

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: max {RATE_LIMIT} requests per {WINDOW_SECONDS}s.",
        )

    timestamps.append(now)
