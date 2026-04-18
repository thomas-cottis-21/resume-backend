from __future__ import annotations

from uuid import UUID

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bucket_list.domain.entities import BucketListItem, BucketListStatus, Destination, DestinationCategory
from bucket_list.domain.repositories import BucketListItemRepository
from bucket_list.infrastructure.models import BucketListItemModel, BucketListStatusModel, DestinationModel


def _to_entity(m: BucketListItemModel) -> BucketListItem:
    destination = None
    if m.destination is not None:
        dest = m.destination
        category = None
        if dest.category is not None:
            category = DestinationCategory(
                id=dest.category.id,
                name=dest.category.name,
                sort_order=dest.category.sort_order,
            )
        destination = Destination(
            id=dest.id,
            name=dest.name,
            country=dest.country,
            continent=dest.continent,
            description=dest.description,
            cover_image_url=dest.cover_image_url,
            category_id=dest.category_id,
            created_at=dest.created_at,
            updated_at=dest.updated_at,
            category=category,
        )
    status = None
    if m.status is not None:
        status = BucketListStatus(id=m.status.id, name=m.status.name)

    return BucketListItem(
        id=m.id,
        user_id=m.user_id,
        destination_id=m.destination_id,
        status_id=m.status_id,
        notes=m.notes,
        created_at=m.created_at,
        updated_at=m.updated_at,
        destination=destination,
        status=status,
    )


_EAGER = [
    selectinload(BucketListItemModel.destination).selectinload(DestinationModel.category),
    selectinload(BucketListItemModel.status),
]


class SqlAlchemyBucketListItemRepository(BucketListItemRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, item_id: UUID) -> BucketListItem | None:
        result = await self._session.execute(
            select(BucketListItemModel)
            .options(*_EAGER)
            .where(BucketListItemModel.id == item_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_user_and_destination(
        self, user_id: UUID, destination_id: UUID
    ) -> BucketListItem | None:
        result = await self._session.execute(
            select(BucketListItemModel)
            .options(*_EAGER)
            .where(
                and_(
                    BucketListItemModel.user_id == user_id,
                    BucketListItemModel.destination_id == destination_id,
                )
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[BucketListItem]:
        result = await self._session.execute(
            select(BucketListItemModel)
            .options(*_EAGER)
            .where(BucketListItemModel.user_id == user_id)
            .order_by(BucketListItemModel.created_at.desc())
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, item: BucketListItem) -> None:
        existing = await self._session.get(BucketListItemModel, item.id)
        if existing:
            existing.status_id = item.status_id
            existing.notes = item.notes
            existing.updated_at = item.updated_at
        else:
            self._session.add(
                BucketListItemModel(
                    id=item.id,
                    user_id=item.user_id,
                    destination_id=item.destination_id,
                    status_id=item.status_id,
                    notes=item.notes,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                )
            )
        await self._session.flush()

    async def delete(self, item_id: UUID) -> None:
        await self._session.execute(
            delete(BucketListItemModel).where(BucketListItemModel.id == item_id)
        )
        await self._session.flush()
