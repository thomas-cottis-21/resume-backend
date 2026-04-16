from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from bucket_list.application.dtos import DestinationOutput
from bucket_list.application.queries._helpers import destination_to_output
from bucket_list.domain.exceptions import DestinationNotFound
from bucket_list.domain.repositories import DestinationRepository


@dataclass
class UpdateDestinationInput:
    destination_id: UUID
    name: str
    country: str
    continent: str
    description: str | None = None
    cover_image_url: str | None = None
    category_id: UUID | None = None


class UpdateDestination:
    def __init__(self, repo: DestinationRepository) -> None:
        self._repo = repo

    async def execute(self, input: UpdateDestinationInput) -> DestinationOutput:
        destination = await self._repo.get_by_id(input.destination_id)
        if not destination:
            raise DestinationNotFound(input.destination_id)

        destination.name = input.name
        destination.country = input.country
        destination.continent = input.continent
        destination.description = input.description
        destination.cover_image_url = input.cover_image_url
        destination.category_id = input.category_id
        destination.updated_at = datetime.now(tz=timezone.utc)

        await self._repo.save(destination)
        loaded = await self._repo.get_by_id(destination.id)
        return destination_to_output(loaded)  # type: ignore[arg-type]
