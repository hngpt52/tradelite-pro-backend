import redis
from app.core.config import settings

# Create Redis client
redis_client = redis.from_url(settings.REDIS_URL)

def get_redis_client():
    """
    Returns the Redis client instance
    """
    return redis_client
