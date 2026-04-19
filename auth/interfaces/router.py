from fastapi import APIRouter

from auth.interfaces.routers.auth_router import router as auth_router
from auth.interfaces.routers.oauth_router import router as oauth_router
router = APIRouter()
router.include_router(auth_router)
router.include_router(oauth_router, prefix="/oauth")
