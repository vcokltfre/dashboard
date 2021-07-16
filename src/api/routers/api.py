from secrets import token_hex

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from starlette_discord import DiscordOAuthClient

from src.api.env import Discord, Site


router = APIRouter(prefix="/api")

oauth = DiscordOAuthClient(
    Discord.client_id,
    Discord.client_secret,
    Site.link + "/api/callback",
)

@router.get("/login")
async def login() -> None:
    return oauth.redirect()

@router.get("/callback")
async def callback(code: str, request: Request) -> None:
    try:
        user = await oauth.login(code)
    except OAuth2Error:
        return "Invalid code."

    token = token_hex(32)
    await request.state.rd.set_session(token, user["id"])

    response = RedirectResponse("/guilds")
    response.set_cookie("confd_api_key", token, max_age=86400)

    return response
