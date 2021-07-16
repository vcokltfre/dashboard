from secrets import token_hex

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from starlette_discord import DiscordOAuthClient

from src.api.env import Discord, Site
from src.api.models import SetConfig
from src.api.utils.database import Database
from src.api.utils.redis import RedisCache


router = APIRouter(prefix="/api")

oauth = DiscordOAuthClient(
    Discord.client_id,
    Discord.client_secret,
    Site.link + "/api/callback",
)

async def verify(request: Request, guild: str) -> None:
    db: Database = request.state.db
    redis: RedisCache = request.state.rd

    token = request.cookies.get("confd_api_key")

    if not token:
        raise HTTPException(401)

    user = await redis.get_session(token)

    if not user:
        raise HTTPException(401)

    if not await db.auth_user(int(user), int(guild)):
        raise HTTPException(403)

@router.get("/login")
async def login() -> None:
    return oauth.redirect()

@router.get("/callback")
async def callback(code: str, request: Request) -> RedirectResponse:
    try:
        user = await oauth.login(code)
    except OAuth2Error:
        return "Invalid code."

    token = token_hex(32)
    await request.state.rd.set_session(token, user["id"])

    response = RedirectResponse("/guilds")
    response.set_cookie("confd_api_key", token, max_age=86400)

    return response

@router.get("/guilds/{guild_id}/config")
async def get_guild_config(guild_id: str, request: Request) -> dict:
    await verify(request, guild_id)

    config = await request.state.db.get_config(int(guild_id))

    return {
        "value": config,
    }

@router.post("/guilds/{guild_id}/config")
async def set_guild_config(guild_id: str, config: SetConfig, request: Request) -> None:
    await verify(request, guild_id)

    await request.state.db.set_config(int(guild_id), config.value)
