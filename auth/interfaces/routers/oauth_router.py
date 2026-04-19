from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.commands.oauth_callback import OAuthCallback, OAuthCallbackInput
from auth.infrastructure.repositories.oauth_account_repository import SqlAlchemyOAuthAccountRepository
from auth.infrastructure.repositories.refresh_token_repository import SqlAlchemyRefreshTokenRepository
from auth.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from auth.infrastructure.security import generate_oauth_state, verify_oauth_state
from auth.interfaces.routers.auth_router import _set_refresh_cookie
from core.config import settings
from core.database.session import get_db_session
from core.exceptions import AuthenticationError

router = APIRouter(tags=["auth"])


@router.get("/google/authorize")
async def google_authorize() -> RedirectResponse:
    state = generate_oauth_state(settings)
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account",
    }
    url = settings.google_auth_url + "?" + urlencode(params)
    response = RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        "oauth_state", state, max_age=600, httponly=True, samesite="lax"
    )
    return response


@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    code: str,
    state: str,
    db: AsyncSession = Depends(get_db_session),
) -> RedirectResponse:
    # Validate state
    cookie_state = request.cookies.get("oauth_state")
    if not cookie_state or cookie_state != state or not verify_oauth_state(state, settings):
        raise AuthenticationError("Invalid OAuth state")

    async with httpx.AsyncClient(timeout=10.0) as client:
        token_response = await client.post(
            settings.google_token_url,
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        token_response.raise_for_status()
        tokens = token_response.json()

        userinfo_response = await client.get(
            settings.google_userinfo_url,
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()

    if not userinfo.get("sub"):
        raise AuthenticationError("Invalid Google userinfo response")
    if not userinfo.get("email"):
        raise AuthenticationError("Google account must have an email address")

    user_repo = SqlAlchemyUserRepository(db)
    oauth_repo = SqlAlchemyOAuthAccountRepository(db)
    refresh_token_repo = SqlAlchemyRefreshTokenRepository(db)

    result = await OAuthCallback(user_repo, oauth_repo, refresh_token_repo, settings).execute(
        OAuthCallbackInput(
            provider="google",
            provider_user_id=userinfo["sub"],
            provider_email=userinfo.get("email"),
            display_name=userinfo.get("name", ""),
        )
    )

    redirect = RedirectResponse(
        url=f"{settings.oauth_success_redirect}#access_token={result.access_token}",
        status_code=status.HTTP_302_FOUND,
    )
    _set_refresh_cookie(redirect, result.refresh_token)
    redirect.delete_cookie("oauth_state")
    return redirect
