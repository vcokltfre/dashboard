from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api.env import Site


router = APIRouter()

templates = Jinja2Templates("src/web/templates")

@router.get("/")
async def get_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {
        "request": request,
        "site": Site,
    })
