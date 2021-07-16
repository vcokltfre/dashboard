from fastapi import FastAPI

from .routers import router


app = FastAPI(openapi_url=None)

app.include_router(router)
