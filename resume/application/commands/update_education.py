from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from resume.application.dtos import EducationOutput
from resume.domain.exceptions import EducationNotFound
from resume.domain.repositories import EducationRepository


@dataclass
class UpdateEducationInput:
    education_id: UUID
    institution: str
    degree: str
    start_year: int
    end_year: int | None = None
    sort_order: int = 0


class UpdateEducation:
    def __init__(self, repo: EducationRepository) -> None:
        self._repo = repo

    async def execute(self, input: UpdateEducationInput) -> EducationOutput:
        entry = await self._repo.get_by_id(input.education_id)
        if entry is None:
            raise EducationNotFound(input.education_id)
        entry.institution = input.institution
        entry.degree = input.degree
        entry.start_year = input.start_year
        entry.end_year = input.end_year
        entry.sort_order = input.sort_order
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
