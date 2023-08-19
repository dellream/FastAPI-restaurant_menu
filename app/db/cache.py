import redis

from app.config import REDIS_HOST, REDIS_PORT


class CacheRepository:
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST,
                                        port=REDIS_PORT, db=0)


