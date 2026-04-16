from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from bucket_list.application.dtos import VisitOutput
from bucket_list.application.queries._helpers import visit_to_output
from bucket_list.domain.entities import Visit
from bucket_list.domain.exceptions import DestinationNotFound
from bucket_list.domain.repositories import DestinationRepository, VisitRepository


@dataclass
class LogVisitInput:
    user_id: UUID
    destination_id: UUID
    visited_at: date
    notes: str | None = None


class LogVisit:
    def __init__(
        self,
        visit_repo: VisitRepository,
        destination_repo: DestinationRepository,
    ) -> None:
        self._visit_repo = visit_repo
        self._destination_repo = destination_repo

    async def execute(self, input: LogVisitInput) -> VisitOutput:
        destination = await self._destination_repo.get_by_id(input.destination_id)
        if not destination:
            raise DestinationNotFound(input.destination_id)

        visit = Visit(
            id=uuid4(),
            user_id=input.user_id,
            destination_id=input.destination_id,
            visited_at=input.visited_at,
            notes=input.notes,
            created_at=datetime.now(tz=timezone.utc),
        )
        await self._visit_repo.save(visit)
        loaded = await self._visit_repo.get_by_id(visit.id)
        return visit_to_output(loaded)  # type: ignore[arg-type]
