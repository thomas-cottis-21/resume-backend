from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from auth.domain.entities import RefreshToken, User
from auth.domain.repositories import RefreshTokenRepository, UserRepository
from auth.infrastructure.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
)
from core.config import Settings
from core.exceptions import ConflictError


@dataclass
class RegisterUserInput:
    email: str
    password: str
    display_name: str


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterUser:
    def __init__(
        self,
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository,
        settings: Settings,
    ) -> None:
        self._user_repo = user_repo
        self._refresh_token_repo = refresh_token_repo
        self._settings = settings

    async def execute(self, input: RegisterUserInput) -> TokenPair:
        if await self._user_repo.get_by_email(input.email):
            raise ConflictError(f"Email {input.email!r} is already registered")

        now = datetime.now(tz=timezone.utc)
        user = User(
            id=uuid4(),
            email=input.email,
            password_hash=hash_password(input.password),
            display_name=input.display_name,
            bio=None,
            avatar_url=None,
            roles=["USER"],
            created_at=now,
            updated_at=now,
        )
        await self._user_repo.save(user)

        return await _issue_token_pair(
            user, self._refresh_token_repo, self._settings
        )


async def _issue_token_pair(
    user: User,
    refresh_token_repo: RefreshTokenRepository,
    settings: Settings,
) -> TokenPair:
    now = datetime.now(tz=timezone.utc)
    raw_refresh, token_hash = generate_refresh_token()
    refresh_token = RefreshToken(
        id=uuid4(),
        user_id=user.id,
        token_hash=token_hash,
        expires_at=now + timedelta(days=settings.refresh_token_expire_days),
        revoked_at=None,
        created_at=now,
    )
    await refresh_token_repo.save(refresh_token)
    access_token = create_access_token(user.id, user.roles, settings)
    return TokenPair(access_token=access_token, refresh_token=raw_refresh)
