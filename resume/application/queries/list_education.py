from uuid import UUID

from resume.application.dtos import EducationOutput
from resume.domain.repositories import EducationRepository


class ListEducation:
    def __init__(self, repo: EducationRepository) -> None:
        self._repo = repo

    async def execute(self, resume_id: UUID) -> list[EducationOutput]:
        entries = await self._repo.list_by_resume(resume_id)
        return [
            EducationOutput(
                id=e.id,
                resume_id=e.resume_id,
                institution=e.institution,
                degree=e.degree,
                start_year=e.start_year,
                end_year=e.end_year,
                sort_order=e.sort_order,
                created_at=e.created_at,
            )
            for e in entries
        ]
