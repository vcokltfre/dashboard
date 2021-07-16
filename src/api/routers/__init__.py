from fastapi import APIRouter

from .frontend import router as frontend_router


router = APIRouter()

router.include_router(frontend_router)


__all__ = ("router",)
