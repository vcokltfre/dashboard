from asyncpg import Pool, Record, create_pool
from loguru import logger

from src.api.env import Database as DB, Auth


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

    async def create_guild(self, id: int, icon_url: str, name: str) -> None:
        await self._pool.execute(
            "INSERT INTO Guilds VALUES ($1, $2, $3, $4);", id, icon_url, name, ""
        )

    async def set_config(self, guild: int, value: str) -> None:
        await self._pool.execute(
            "UPDATE Guilds SET config = $1 WHERE id = $2;",
            value,
            guild,
        )

    async def get_guild(self, guild: int) -> Record:
        return await self._pool.fetchrow("SELECT * FROM Guilds WHERE id = $1;", guild)

    async def get_guilds(self, user_id: int) -> list:
        if str(user_id) in Auth.admins:
            return await self._pool.fetch("SELECT * FROM Guilds;")
        guilds = await self._pool.fetch("SELECT * FROM GuildAccess WHERE member_id = $1;", user_id)
        return await self._pool.fetch("SELECT * FROM Guilds WHERE id = any($1::bigint[]);", [g["member_id"] for g in guilds])

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
