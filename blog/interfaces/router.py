from fastapi import APIRouter

from blog.interfaces.routers.posts import router as posts_router

blog_router = APIRouter()

blog_router.include_router(posts_router)
