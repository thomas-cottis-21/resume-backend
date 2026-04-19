from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.entities import User
from auth.domain.repositories import UserRepository
from auth.infrastructure.models import RoleModel, UserModel, UserRoleModel


def _to_entity(m: UserModel) -> User:
    return User(
        id=m.id,
        email=m.email,
        password_hash=m.password_hash,
        display_name=m.display_name,
        bio=m.bio,
        avatar_url=m.avatar_url,
        roles=[r.name for r in m.roles],
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        model = await self._session.get(UserModel, user_id)
        return _to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def save(self, user: User) -> None:
        existing = await self._session.get(UserModel, user.id)
        if existing:
            existing.email = user.email
            existing.password_hash = user.password_hash
            existing.display_name = user.display_name
            existing.bio = user.bio
            existing.avatar_url = user.avatar_url
            existing.updated_at = user.updated_at
        else:
            self._session.add(
                UserModel(
                    id=user.id,
                    email=user.email,
                    password_hash=user.password_hash,
                    display_name=user.display_name,
                    bio=user.bio,
                    avatar_url=user.avatar_url,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )
            )
            await self._session.flush()
            for role_name in user.roles:
                role = (await self._session.execute(
                    select(RoleModel).where(RoleModel.name == role_name)
                )).scalar_one_or_none()
                if role:
                    self._session.add(UserRoleModel(user_id=user.id, role_id=role.id))
        await self._session.flush()
