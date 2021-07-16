from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api.env import Site
from src.api.objects.guild import Guild
from src.api.utils.auth import verify


router = APIRouter()

templates = Jinja2Templates("src/web/templates")

@router.get("/")
async def get_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {
        "request": request,
        "site": Site,
    })

@router.get("/guilds")
async def get_guilds(request: Request) -> HTMLResponse:
    user = await verify(request)

    guilds = await request.state.db.get_guilds(int(user))

    return templates.TemplateResponse("guilds.html", {
        "request": request,
        "site": Site,
        "guilds": [Guild(g["icon_url"], g["title"], g["id"]) for g in guilds],
    })

@router.get("/guilds/{guild_id}/config")
async def get_guild_config(guild_id: str, request: Request) -> HTMLResponse:
    await verify(request, guild_id)

    guild = await request.state.db.get_guild(int(guild_id))

    return templates.TemplateResponse("config.html", {
        "request": request,
        "site": Site,
        "guild": Guild(guild["icon_url"], guild["title"], guild_id),
    })
