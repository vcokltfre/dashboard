from hashlib import sha256

from aioredis import Redis, create_redis_pool
from loguru import logger

from src.api.env import Redis as RD, Auth


class RedisCache:
    _redis: Redis

    def __init__(self) -> None:
        self._redis = None

    @staticmethod
    def session_hash(token: str) -> None:
        return sha256(token + Auth.salt).hexdigest()

    async def ainit(self) -> None:
        logger.info("Connecting to Redis...")
        self._redis = await create_redis_pool(RD.uri)
        logger.info("Redis connected.")

    async def set_session(self, token: str, user: str) -> None:
        await self._redis.set(
            self.session_hash(token),
            user,
            expire=86400,
        )

    async def get_session(self, token: str) -> None:
        return await self._redis.get(self.session_hash(token), encoding="utf-8")
