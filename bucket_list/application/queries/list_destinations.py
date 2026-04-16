from __future__ import annotations

from uuid import UUID

from bucket_list.application.dtos import DestinationOutput
from bucket_list.application.queries._helpers import destination_to_output
from bucket_list.domain.repositories import DestinationRepository


class ListDestinations:
    def __init__(self, repo: DestinationRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        category_id: UUID | None = None,
        country: str | None = None,
        continent: str | None = None,
    ) -> list[DestinationOutput]:
        destinations = await self._repo.list_all(
            category_id=category_id,
            country=country,
            continent=continent,
        )
        return [destination_to_output(d) for d in destinations]
