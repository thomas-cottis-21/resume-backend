from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from auth.application.commands.register_user import TokenPair
from auth.domain.entities import RefreshToken
from auth.domain.repositories import RefreshTokenRepository, UserRepository
from auth.infrastructure.security import (
    create_access_token,
    generate_refresh_token,
    hash_token,
)
from core.config import Settings
from core.exceptions import AuthenticationError


@dataclass
class RefreshTokenInput:
    raw_refresh_token: str


class RefreshAccessToken:
    def __init__(
        self,
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository,
        settings: Settings,
    ) -> None:
        self._user_repo = user_repo
        self._refresh_token_repo = refresh_token_repo
        self._settings = settings

    async def execute(self, input: RefreshTokenInput) -> TokenPair:
        token_hash = hash_token(input.raw_refresh_token)
        existing = await self._refresh_token_repo.get_by_hash(token_hash)
        if not existing:
            raise AuthenticationError("Invalid or expired refresh token")

        now = datetime.now(tz=timezone.utc)

        # Rotate: revoke old, issue new
        await self._refresh_token_repo.revoke(existing.id, now)

        new_raw, new_hash = generate_refresh_token()
        new_token = RefreshToken(
            id=uuid4(),
            user_id=existing.user_id,
            token_hash=new_hash,
            expires_at=now + timedelta(days=self._settings.refresh_token_expire_days),
            revoked_at=None,
            created_at=now,
        )
        await self._refresh_token_repo.save(new_token)

        user = await self._user_repo.get_by_id(existing.user_id)
        if not user:
            raise AuthenticationError("User not found")

        access_token = create_access_token(user.id, user.roles, self._settings)
        return TokenPair(access_token=access_token, refresh_token=new_raw)
