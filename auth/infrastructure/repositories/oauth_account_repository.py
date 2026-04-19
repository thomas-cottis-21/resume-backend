from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.entities import OAuthAccount
from auth.domain.repositories import OAuthAccountRepository
from auth.infrastructure.models import OAuthAccountModel


def _to_entity(m: OAuthAccountModel) -> OAuthAccount:
    return OAuthAccount(
        id=m.id,
        user_id=m.user_id,
        provider=m.provider,
        provider_user_id=m.provider_user_id,
        provider_email=m.provider_email,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


class SqlAlchemyOAuthAccountRepository(OAuthAccountRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_provider(self, provider: str, provider_user_id: str) -> OAuthAccount | None:
        result = await self._session.execute(
            select(OAuthAccountModel).where(
                OAuthAccountModel.provider == provider,
                OAuthAccountModel.provider_user_id == provider_user_id,
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def save(self, account: OAuthAccount) -> None:
        existing = await self._session.get(OAuthAccountModel, account.id)
        if existing:
            existing.provider_email = account.provider_email
            existing.updated_at = account.updated_at
        else:
            self._session.add(
                OAuthAccountModel(
                    id=account.id,
                    user_id=account.user_id,
                    provider=account.provider,
                    provider_user_id=account.provider_user_id,
                    provider_email=account.provider_email,
                    created_at=account.created_at,
                    updated_at=account.updated_at,
                )
            )
        await self._session.flush()
