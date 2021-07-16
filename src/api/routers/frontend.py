from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api.env import Site
from src.api.objects.guild import Guild


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
    return templates.TemplateResponse("guilds.html", {
        "request": request,
        "site": Site,
        "guilds": [],
    })

@router.get("/guilds/{guild_id}/config")
async def get_guild_config(guild_id: str, request: Request) -> HTMLResponse:
    return templates.TemplateResponse("config.html", {
        "request": request,
        "site": Site,
        "guild": Guild("", "", "123"),
    })
