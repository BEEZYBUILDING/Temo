import redis
from django.conf import settings

redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

def is_rate_limited(key, max_requests, window_seconds):
    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, window_seconds)
    return current > max_requests