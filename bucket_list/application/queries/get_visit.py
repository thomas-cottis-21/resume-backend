from uuid import UUID

from bucket_list.application.dtos import VisitOutput
from bucket_list.application.queries._helpers import visit_to_output
from bucket_list.domain.exceptions import VisitNotFound
from bucket_list.domain.repositories import VisitRepository


class GetVisit:
    def __init__(self, repo: VisitRepository) -> None:
        self._repo = repo

    async def execute(self, visit_id: UUID) -> VisitOutput:
        visit = await self._repo.get_by_id(visit_id)
        if not visit:
            raise VisitNotFound(visit_id)
        return visit_to_output(visit)
