from uuid import UUID

from bucket_list.application.dtos import VisitOutput
from bucket_list.application.queries._helpers import visit_to_output
from bucket_list.domain.repositories import VisitRepository


class ListVisits:
    def __init__(self, repo: VisitRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: UUID) -> list[VisitOutput]:
        visits = await self._repo.list_by_user(user_id)
        return [visit_to_output(v) for v in visits]
