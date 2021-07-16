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
        "guilds": []
    })
