from uuid import UUID

from resume.application.dtos import EducationOutput
from resume.domain.exceptions import EducationNotFound
from resume.domain.repositories import EducationRepository


class GetEducationEntry:
    def __init__(self, repo: EducationRepository) -> None:
        self._repo = repo

    async def execute(self, education_id: UUID) -> EducationOutput:
        entry = await self._repo.get_by_id(education_id)
        if entry is None:
            raise EducationNotFound(education_id)
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
