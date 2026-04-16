from uuid import UUID

from bucket_list.domain.exceptions import DestinationNotFound
from bucket_list.domain.repositories import DestinationRepository


class DeleteDestination:
    def __init__(self, repo: DestinationRepository) -> None:
        self._repo = repo

    async def execute(self, destination_id: UUID) -> None:
        destination = await self._repo.get_by_id(destination_id)
        if not destination:
            raise DestinationNotFound(destination_id)
        await self._repo.delete(destination_id)
