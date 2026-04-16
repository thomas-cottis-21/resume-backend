from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from resume.application.dtos import EducationOutput
from resume.domain.entities import Education
from resume.domain.repositories import EducationRepository


@dataclass
class AddEducationInput:
    resume_id: UUID
    institution: str
    degree: str
    start_year: int
    end_year: int | None = None
    sort_order: int = 0


class AddEducation:
    def __init__(self, repo: EducationRepository) -> None:
        self._repo = repo

    async def execute(self, input: AddEducationInput) -> EducationOutput:
        now = datetime.now(tz=timezone.utc)
        entry = Education(
            id=uuid4(),
            resume_id=input.resume_id,
            institution=input.institution,
            degree=input.degree,
            start_year=input.start_year,
            end_year=input.end_year,
            sort_order=input.sort_order,
            created_at=now,
        )
        await self._repo.save(entry)
        return EducationOutput(
            id=entry.id,
            resume_id=entry.resume_id,
            institution=entry.institution,
            degree=entry.degree,
            start_year=entry.start_year,
            end_year=entry.end_year,
            sort_order=entry.sort_order,
            created_at=entry.created_at,
        )
