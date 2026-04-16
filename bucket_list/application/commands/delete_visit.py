from uuid import UUID

from bucket_list.domain.exceptions import VisitNotFound
from bucket_list.domain.repositories import VisitRepository


class DeleteVisit:
    def __init__(self, repo: VisitRepository) -> None:
        self._repo = repo

    async def execute(self, visit_id: UUID) -> None:
        visit = await self._repo.get_by_id(visit_id)
        if not visit:
            raise VisitNotFound(visit_id)
        await self._repo.delete(visit_id)
