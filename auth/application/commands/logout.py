from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from auth.domain.repositories import RefreshTokenRepository
from auth.infrastructure.security import hash_token


@dataclass
class LogoutInput:
    raw_refresh_token: str


class Logout:
    def __init__(self, refresh_token_repo: RefreshTokenRepository) -> None:
        self._refresh_token_repo = refresh_token_repo

    async def execute(self, input: LogoutInput) -> None:
        token_hash = hash_token(input.raw_refresh_token)
        existing = await self._refresh_token_repo.get_by_hash(token_hash)
        if existing:
            await self._refresh_token_repo.revoke(
                existing.id, datetime.now(tz=timezone.utc)
            )
