from fastapi import APIRouter

from .api import router as api_router
from .frontend import router as frontend_router


router = APIRouter()

router.include_router(api_router)
router.include_router(frontend_router)


__all__ = ("router",)
