from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from blog.domain.entities import PostStatus
from blog.domain.repositories import StatusRepository
from blog.infrastructure.models import PostStatusModel


class SqlAlchemyStatusRepository(StatusRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_statuses(self) -> list[PostStatus]:
        result = await self._session.execute(select(PostStatusModel))
        return [PostStatus(id=UUID(m.id), name=m.name) for m in result.scalars().all()]

    async def get_by_status_id(self, status_id: UUID) -> PostStatus | None:
        model = await self._session.get(PostStatusModel, str(status_id))
        return PostStatus(id=UUID(model.id), name=model.name) if model else None
