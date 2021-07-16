from fastapi import Request
from fastapi.exceptions import HTTPException

from src.api.env import Auth

from .database import Database
from .redis import RedisCache


async def verify(request: Request, guild: str = None) -> None:
    db: Database = request.state.db
    redis: RedisCache = request.state.rd

    token = request.cookies.get("confd_api_key")

    if not token:
        raise HTTPException(401)

    user = await redis.get_session(token)

    if not user:
        raise HTTPException(401)

    if not guild:
        return user

    if not await db.get_guild(int(guild)):
        raise HTTPException(404)

    if user in Auth.admins:
        return

    if not await db.auth_user(int(user), int(guild)):
        raise HTTPException(403)
