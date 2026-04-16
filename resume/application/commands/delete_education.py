from uuid import UUID

from resume.domain.exceptions import EducationNotFound
from resume.domain.repositories import EducationRepository


class DeleteEducation:
    def __init__(self, repo: EducationRepository) -> None:
        self._repo = repo

    async def execute(self, education_id: UUID) -> None:
        entry = await self._repo.get_by_id(education_id)
        if entry is None:
            raise EducationNotFound(education_id)
        await self._repo.delete(education_id)
