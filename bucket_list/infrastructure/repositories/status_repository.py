from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bucket_list.domain.entities import BucketListStatus, DestinationCategory
from bucket_list.domain.repositories import StatusRepository
from bucket_list.infrastructure.models import BucketListStatusModel, DestinationCategoryModel


class SqlAlchemyStatusRepository(StatusRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_statuses(self) -> list[BucketListStatus]:
        result = await self._session.execute(
            select(BucketListStatusModel).order_by(BucketListStatusModel.name)
        )
        return [
            BucketListStatus(id=m.id, name=m.name)
            for m in result.scalars().all()
        ]

    async def get_status_by_id(self, status_id: UUID) -> BucketListStatus | None:
        model = await self._session.get(BucketListStatusModel, status_id)
        return BucketListStatus(id=model.id, name=model.name) if model else None

    async def list_categories(self) -> list[DestinationCategory]:
        result = await self._session.execute(
            select(DestinationCategoryModel).order_by(DestinationCategoryModel.sort_order)
        )
        return [
            DestinationCategory(id=m.id, name=m.name, sort_order=m.sort_order)
            for m in result.scalars().all()
        ]
