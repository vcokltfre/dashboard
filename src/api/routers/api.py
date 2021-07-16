from hmac import compare_digest
from secrets import token_hex

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from starlette_discord import DiscordOAuthClient

from src.api.env import Auth, Discord, Site
from src.api.models import SetConfig
from src.api.utils.auth import verify


router = APIRouter(prefix="/api")

oauth = DiscordOAuthClient(
    Discord.client_id,
    Discord.client_secret,
    Site.link + "/api/callback",
)

async def verify_internal(request: Request) -> None:
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(401)

    if not compare_digest(token, Auth.internal):
        raise HTTPException(401)

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
    try:
        await verify_internal(request)
    except Exception:
        await verify(request, guild_id)

    config = await request.state.db.get_config(int(guild_id))

    return {
        "value": config,
    }

@router.post("/guilds/{guild_id}/config")
async def set_guild_config(guild_id: str, config: SetConfig, request: Request) -> None:
    await verify(request, guild_id)

    await request.state.db.set_config(int(guild_id), config.value)

@router.post("/guilds/{guild_id}")
async def create_guild(guild_id: str, icon_url: str, name: str, request: Request) -> None:
    await verify_internal(request)

    await request.state.db.create_guild(int(guild_id), icon_url, name)

@router.post("/guilds/{guild_id}/access/{user_id}")
async def grant_guild_access(guild_id: int, user_id: int, request: Request) -> None:
    await verify_internal(request)

    await request.state.db.grant_user(guild_id, user_id)

@router.delete("/guilds/{guild_id}/access/{user_id}")
async def delete_guild_access(guild_id: int, user_id: int, request: Request) -> None:
    await verify_internal(request)

    await request.state.db.delete_user(guild_id, user_id)

@router.get("/guilds")
async def get_guilds(request: Request) -> list:
    await verify_internal(request)
