from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bucket_list.domain.entities import Destination, DestinationCategory, Visit
from bucket_list.domain.repositories import VisitRepository
from bucket_list.infrastructure.models import DestinationModel, VisitModel


def _to_entity(m: VisitModel) -> Visit:
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
    return Visit(
        id=m.id,
        user_id=m.user_id,
        destination_id=m.destination_id,
        visited_at=m.visited_at,
        notes=m.notes,
        created_at=m.created_at,
        destination=destination,
    )


_EAGER = [
    selectinload(VisitModel.destination).selectinload(DestinationModel.category),
]


class SqlAlchemyVisitRepository(VisitRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, visit_id: UUID) -> Visit | None:
        result = await self._session.execute(
            select(VisitModel)
            .options(*_EAGER)
            .where(VisitModel.id == visit_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[Visit]:
        result = await self._session.execute(
            select(VisitModel)
            .options(*_EAGER)
            .where(VisitModel.user_id == user_id)
            .order_by(VisitModel.visited_at.desc())
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, visit: Visit) -> None:
        existing = await self._session.get(VisitModel, visit.id)
        if not existing:
            self._session.add(
                VisitModel(
                    id=visit.id,
                    user_id=visit.user_id,
                    destination_id=visit.destination_id,
                    visited_at=visit.visited_at,
                    notes=visit.notes,
                    created_at=visit.created_at,
                )
            )
            await self._session.flush()

    async def delete(self, visit_id: UUID) -> None:
        await self._session.execute(
            delete(VisitModel).where(VisitModel.id == visit_id)
        )
        await self._session.flush()
