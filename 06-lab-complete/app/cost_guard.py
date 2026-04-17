import time
import logging
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

# Pricing
PRICE_PER_1K_INPUT = 0.00015
PRICE_PER_1K_OUTPUT = 0.0006

# Storage
_redis = None
_in_memory_cost = 0.0
_in_memory_day = ""

if settings.redis_url:
    try:
        import redis
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
        _redis.ping()
        logger.info("Cost Guard: Connected to Redis")
    except Exception as e:
        logger.error(f"Cost Guard: Failed to connect to Redis: {e}")
        _redis = None

def check_and_record_cost(input_tokens: int, output_tokens: int):
    """
    Check if daily budget is exceeded and record new usage.
    """
    global _in_memory_cost, _in_memory_day
    
    today = time.strftime("%Y-%m-%d")
    cost = (input_tokens / 1000) * PRICE_PER_1K_INPUT + (output_tokens / 1000) * PRICE_PER_1K_OUTPUT
    limit = settings.daily_budget_usd

    if _redis:
        try:
            key = f"cost:{today}"
            current_cost = float(_redis.get(key) or 0)
            
            if current_cost >= limit:
                raise HTTPException(503, "Daily budget exhausted. Try tomorrow.")
            
            _redis.incrbyfloat(key, cost)
            _redis.expire(key, 86400 * 2)  # Keep for 2 days
            return
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Redis cost guard error: {e}")

    # Fallback to in-memory
    if today != _in_memory_day:
        _in_memory_cost = 0.0
        _in_memory_day = today
        
    if _in_memory_cost >= limit:
        raise HTTPException(503, "Daily budget exhausted. Try tomorrow.")
    
    _in_memory_cost += cost
