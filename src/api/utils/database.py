from asyncpg import Pool, create_pool
from loguru import logger

from src.api.env import Database as DB


class Database:
    _pool: Pool

    def __init__(self) -> None:
        self._pool = None

    async def ainit(self) -> None:
        logger.info("Connecting to Postgres...")
        self._pool = await create_pool(DB.uri)
        logger.info("Postgers connected.")
