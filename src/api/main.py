from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import router
from .utils.database import Database
from .utils.redis import RedisCache


app = FastAPI(openapi_url=None)

app.mount("/static", StaticFiles(directory="src/web/static"), "static")
app.include_router(router)

db = Database()
rd = RedisCache()

@app.on_event("startup")
async def on_startup() -> None:
    await db.ainit()
    await rd.ainit()
