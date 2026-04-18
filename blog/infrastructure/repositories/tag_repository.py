from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from blog.domain.entities import Tag
from blog.domain.repositories import TagRepository
from blog.infrastructure.models import TagModel


class SqlAlchemyTagRepository(TagRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, tag_id: UUID) -> Tag | None:
        model = await self._session.get(TagModel, tag_id)
        return _to_entity(model) if model else None

    async def list_all(self) -> list[Tag]:
        result = await self._session.execute(select(TagModel).order_by(TagModel.name))
        return [_to_entity(m) for m in result.scalars().all()]


def _to_entity(m: TagModel) -> Tag:
    return Tag(id=m.id, name=m.name, slug=m.slug, created_at=m.created_at)
