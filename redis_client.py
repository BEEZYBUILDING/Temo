#this file will create a reusabl Redis connetion
import redis
from decouple import config 

redis_client = redis.StrictRedis.from_url(
    config('REDIS_URL'),
    decode_responses=True #redis will return strings instead of bytes
)