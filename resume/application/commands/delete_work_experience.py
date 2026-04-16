from uuid import UUID

from resume.domain.exceptions import WorkExperienceNotFound
from resume.domain.repositories import WorkExperienceRepository


class DeleteWorkExperience:
    def __init__(self, repo: WorkExperienceRepository) -> None:
        self._repo = repo

    async def execute(self, experience_id: UUID) -> None:
        exp = await self._repo.get_by_id(experience_id)
        if exp is None:
            raise WorkExperienceNotFound(experience_id)
        await self._repo.delete(experience_id)
