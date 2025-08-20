import json
import functools
from redis.asyncio import Redis


def redis_cache(ttl: int = 60):
    """
    Decorator for caching FastAPI responses in Redis.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, redis: Redis, **kwargs):
            # Make a unique cache key based on function + args
            key_parts = [func.__name__] + list(args) + [f"{k}={v}" for k, v in kwargs.items()]
            cache_key = "cache:" + ":".join(map(str, key_parts))

            # Try to get from Redis
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)

            # Call original function
            result = await func(*args, redis=redis, **kwargs)

            # Save to Redis with TTL
            await redis.set(cache_key, json.dumps(result), ex=ttl)

            return result
        return wrapper
    return decorator
