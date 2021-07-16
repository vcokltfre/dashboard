from aioredis import Redis, create_redis_pool
from loguru import logger

from src.api.env import Redis as RD


class RedisCache:
    _redis: Redis

    def __init__(self) -> None:
        self._redis = None

    async def ainit(self) -> None:
        logger.info("Connecting to Redis...")
        self._redis = await create_redis_pool(RD.uri)
        logger.info("Redis connected.")
