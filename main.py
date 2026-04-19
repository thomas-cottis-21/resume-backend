from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from auth.interfaces.router import router as auth_router
from blog.interfaces.router import blog_router
from bucket_list.interfaces.router import bucket_list_router_root
from core.config import settings
from core.exceptions import AuthenticationError, ConflictError, NotFoundError, OwnershipError, ValidationError
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

    @app.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(ConflictError)
    async def conflict_handler(_: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(OwnershipError)
    async def ownership_handler(_: Request, exc: OwnershipError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    async def validation_handler(_: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)})

    @app.exception_handler(AuthenticationError)
    async def authentication_handler(_: Request, exc: AuthenticationError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})

    app.include_router(auth_router, prefix="/api/v1/auth")
    app.include_router(resume_router, prefix="/api/v1")
    app.include_router(bucket_list_router_root, prefix="/api/v1")
    app.include_router(blog_router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
