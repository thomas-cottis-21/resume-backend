from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bucket_list.domain.entities import Destination, DestinationCategory
from bucket_list.domain.repositories import DestinationRepository
from bucket_list.infrastructure.models import DestinationCategoryModel, DestinationModel


def _to_entity(m: DestinationModel) -> Destination:
    category = None
    if m.category is not None:
        category = DestinationCategory(
            id=m.category.id,
            name=m.category.name,
            sort_order=m.category.sort_order,
        )
    return Destination(
        id=m.id,
        name=m.name,
        country=m.country,
        continent=m.continent,
        description=m.description,
        cover_image_url=m.cover_image_url,
        category_id=m.category_id,
        created_at=m.created_at,
        updated_at=m.updated_at,
        category=category,
    )


class SqlAlchemyDestinationRepository(DestinationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, destination_id: UUID) -> Destination | None:
        result = await self._session.execute(
            select(DestinationModel)
            .options(selectinload(DestinationModel.category))
            .where(DestinationModel.id == destination_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_all(
        self,
        category_id: UUID | None = None,
        country: str | None = None,
        continent: str | None = None,
    ) -> list[Destination]:
        query = (
            select(DestinationModel)
            .options(selectinload(DestinationModel.category))
            .order_by(DestinationModel.country, DestinationModel.name)
        )
        if category_id is not None:
            query = query.where(DestinationModel.category_id == category_id)
        if country is not None:
            query = query.where(DestinationModel.country == country)
        if continent is not None:
            query = query.where(DestinationModel.continent == continent)

        result = await self._session.execute(query)
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, destination: Destination) -> None:
        existing = await self._session.get(DestinationModel, destination.id)
        if existing:
            existing.name = destination.name
            existing.country = destination.country
            existing.continent = destination.continent
            existing.description = destination.description
            existing.cover_image_url = destination.cover_image_url
            existing.category_id = destination.category_id
            existing.updated_at = destination.updated_at
        else:
            self._session.add(
                DestinationModel(
                    id=destination.id,
                    name=destination.name,
                    country=destination.country,
                    continent=destination.continent,
                    description=destination.description,
                    cover_image_url=destination.cover_image_url,
                    category_id=destination.category_id,
                    created_at=destination.created_at,
                    updated_at=destination.updated_at,
                )
            )
        await self._session.flush()

    async def delete(self, destination_id: UUID) -> None:
        await self._session.execute(
            delete(DestinationModel).where(DestinationModel.id == destination_id)
        )
        await self._session.flush()
