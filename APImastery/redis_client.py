import os
from redis import Redis

# Use environment variables to configure Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 1))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD
)

def check_redis_connection():
    """ check the connection"""
    try:
        redis_client.ping()
        print("Redis connection is healthy!")
    except Exception as e:
        print(f"Redis connection failed: {e}")
