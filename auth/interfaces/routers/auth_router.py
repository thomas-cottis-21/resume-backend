from fastapi import APIRouter, Cookie, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.commands.login_user import LoginUser, LoginUserInput
from auth.application.commands.logout import Logout, LogoutInput
from auth.application.commands.refresh_token import RefreshAccessToken, RefreshTokenInput
from auth.application.commands.register_user import RegisterUser, RegisterUserInput
from auth.domain.entities import User
from auth.infrastructure.repositories.refresh_token_repository import SqlAlchemyRefreshTokenRepository
from auth.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from auth.interfaces.dependencies import get_current_user
from auth.interfaces.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from core.config import settings
from core.database.session import get_db_session
from core.exceptions import AuthenticationError

router = APIRouter(tags=["auth"])

_REFRESH_COOKIE = "refresh_token"
_COOKIE_MAX_AGE = settings.refresh_token_expire_days * 24 * 60 * 60


def _set_refresh_cookie(response: Response, raw_token: str) -> None:
    response.set_cookie(
        key=_REFRESH_COOKIE,
        value=raw_token,
        max_age=_COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=False,  # set True in production (HTTPS)
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    user_repo = SqlAlchemyUserRepository(db)
    refresh_token_repo = SqlAlchemyRefreshTokenRepository(db)
    result = await RegisterUser(user_repo, refresh_token_repo, settings).execute(
        RegisterUserInput(email=body.email, password=body.password, display_name=body.display_name)
    )
    _set_refresh_cookie(response, result.refresh_token)
    return TokenResponse(access_token=result.access_token)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    user_repo = SqlAlchemyUserRepository(db)
    refresh_token_repo = SqlAlchemyRefreshTokenRepository(db)
    result = await LoginUser(user_repo, refresh_token_repo, settings).execute(
        LoginUserInput(email=body.email, password=body.password)
    )
    _set_refresh_cookie(response, result.refresh_token)
    return TokenResponse(access_token=result.access_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    response: Response,
    raw_refresh_token: str | None = Cookie(default=None, alias=_REFRESH_COOKIE),
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    if not raw_refresh_token:
        raise AuthenticationError("Missing refresh token")
    user_repo = SqlAlchemyUserRepository(db)
    refresh_token_repo = SqlAlchemyRefreshTokenRepository(db)
    result = await RefreshAccessToken(user_repo, refresh_token_repo, settings).execute(
        RefreshTokenInput(raw_refresh_token=raw_refresh_token)
    )
    _set_refresh_cookie(response, result.refresh_token)
    return TokenResponse(access_token=result.access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    response: Response,
    raw_refresh_token: str | None = Cookie(default=None, alias=_REFRESH_COOKIE),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    if raw_refresh_token:
        refresh_token_repo = SqlAlchemyRefreshTokenRepository(db)
        await Logout(refresh_token_repo).execute(LogoutInput(raw_refresh_token=raw_refresh_token))
    response.delete_cookie(_REFRESH_COOKIE)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        bio=current_user.bio,
        avatar_url=current_user.avatar_url,
        roles=current_user.roles,
    )
