from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from bucket_list.application.dtos import DestinationOutput
from bucket_list.application.queries._helpers import destination_to_output
from bucket_list.domain.entities import Destination
from bucket_list.domain.repositories import DestinationRepository


@dataclass
class CreateDestinationInput:
    name: str
    country: str
    continent: str
    description: str | None = None
    cover_image_url: str | None = None
    category_id: UUID | None = None


class CreateDestination:
    def __init__(self, repo: DestinationRepository) -> None:
        self._repo = repo

    async def execute(self, input: CreateDestinationInput) -> DestinationOutput:
        now = datetime.now(tz=timezone.utc)
        destination = Destination(
            id=uuid4(),
            name=input.name,
            country=input.country,
            continent=input.continent,
            description=input.description,
            cover_image_url=input.cover_image_url,
            category_id=input.category_id,
            created_at=now,
            updated_at=now,
        )
        await self._repo.save(destination)
        loaded = await self._repo.get_by_id(destination.id)
        return destination_to_output(loaded)  # type: ignore[arg-type]
