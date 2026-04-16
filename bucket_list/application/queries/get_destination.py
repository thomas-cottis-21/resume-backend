from uuid import UUID

from bucket_list.application.dtos import DestinationOutput
from bucket_list.application.queries._helpers import destination_to_output
from bucket_list.domain.exceptions import DestinationNotFound
from bucket_list.domain.repositories import DestinationRepository


class GetDestination:
    def __init__(self, repo: DestinationRepository) -> None:
        self._repo = repo

    async def execute(self, destination_id: UUID) -> DestinationOutput:
        destination = await self._repo.get_by_id(destination_id)
        if not destination:
            raise DestinationNotFound(destination_id)
        return destination_to_output(destination)
