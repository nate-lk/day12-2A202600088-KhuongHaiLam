import time
import logging
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

# Storage setup
_redis = None
_in_memory_fallback = {}

if settings.redis_url:
    try:
        import redis
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
        _redis.ping()
        logger.info("Rate Limiter: Connected to Redis")
    except Exception as e:
        logger.error(f"Rate Limiter: Failed to connect to Redis: {e}")
        _redis = None

def check_rate_limit(user_id: str):
    """
    Sliding window rate limiter using Redis (fallback to in-memory).
    """
    now = time.time()
    window_seconds = 60
    limit = settings.rate_limit_per_minute
    key = f"rate_limit:{user_id}"

    if _redis:
        try:
            # Clean old requests
            _redis.zremrangebyscore(key, 0, now - window_seconds)
            # Count current window
            current_count = _redis.zcard(key)
            
            if current_count >= limit:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded: {limit} req/min",
                    headers={"Retry-After": "60"},
                )
            
            # Add current request
            _redis.zadd(key, {str(now): now})
            _redis.expire(key, window_seconds + 5)
            return
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Redis rate limit error: {e}")
            # Fallback to in-memory logic below

    # In-memory fallback
    from collections import deque
    if key not in _in_memory_fallback:
        _in_memory_fallback[key] = deque()
    
    window = _in_memory_fallback[key]
    while window and window[0] < now - window_seconds:
        window.popleft()
    
    if len(window) >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {limit} req/min",
            headers={"Retry-After": "60"},
        )
    window.append(now)
