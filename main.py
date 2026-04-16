from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from blog.interfaces.router import blog_router
from bucket_list.interfaces.router import bucket_list_router_root
from core.config import settings
from resume.interfaces.router import resume_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Project Nomadica API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(resume_router, prefix="/api/v1")
    app.include_router(bucket_list_router_root, prefix="/api/v1")
    app.include_router(blog_router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
