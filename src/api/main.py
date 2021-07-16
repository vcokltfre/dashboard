from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import router


app = FastAPI(openapi_url=None)

app.mount("/static", StaticFiles(directory="src/web/static"), "static")

app.include_router(router)
