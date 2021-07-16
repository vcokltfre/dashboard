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

        with open("src/api/data/init.sql") as f:
            await self._pool.execute(f.read())

    async def set_config(self, guild: int, value: str) -> None:
        await self._pool.execute(
            "INSERT INTO Guilds VALUES ($1, $2) ON CONFLICT (id) DO UPDATE SET config = $2;",
            guild,
            value,
        )

    async def get_config(self, guild: int) -> str:
        data = await self._pool.fetchrow("SELECT (config) FROM Guilds WHERE id = $1;", guild)

        if data:
            return data["config"]
        return ""

    async def grant_user(self, guild: int, user: int) -> None:
        await self._pool.execute("INSERT INTO GuildAccess VALUES ($1, $2) ON CONFLICT DO NOTHING;", guild, user)

    async def delete_user(self, guild: int, user: int) -> None:
        await self._pool.execute("DELETE FROM GuildAccess WHERE guild_id = $1 AND member_id = $2;", guild, user)

    async def auth_user(self, guild: int, user: int) -> bool:
        return bool(
            await self._pool.fetchrow("SELECT * FROM GuildAccess WHERE guild_id = $1 AND member_id = $2;", guild, user)
        )
