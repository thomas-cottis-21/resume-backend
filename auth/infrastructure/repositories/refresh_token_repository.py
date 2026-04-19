from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.entities import RefreshToken
from auth.domain.repositories import RefreshTokenRepository
from auth.infrastructure.models import RefreshTokenModel


def _to_entity(m: RefreshTokenModel) -> RefreshToken:
    return RefreshToken(
        id=m.id,
        user_id=m.user_id,
        token_hash=m.token_hash,
        expires_at=m.expires_at,
        revoked_at=m.revoked_at,
        created_at=m.created_at,
    )


class SqlAlchemyRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        result = await self._session.execute(
            select(RefreshTokenModel).where(
                RefreshTokenModel.token_hash == token_hash,
                RefreshTokenModel.revoked_at.is_(None),
                RefreshTokenModel.expires_at > datetime.now(tz=timezone.utc),
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def save(self, token: RefreshToken) -> None:
        self._session.add(
            RefreshTokenModel(
                id=token.id,
                user_id=token.user_id,
                token_hash=token.token_hash,
                expires_at=token.expires_at,
                revoked_at=token.revoked_at,
                created_at=token.created_at,
            )
        )
        await self._session.flush()

    async def revoke(self, token_id: UUID, revoked_at: datetime) -> None:
        await self._session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == token_id)
            .values(revoked_at=revoked_at)
        )
        await self._session.flush()

    async def revoke_all_for_user(self, user_id: UUID, revoked_at: datetime) -> None:
        await self._session.execute(
            update(RefreshTokenModel)
            .where(
                RefreshTokenModel.user_id == user_id,
                RefreshTokenModel.revoked_at.is_(None),
            )
            .values(revoked_at=revoked_at)
        )
        await self._session.flush()
