from uuid import UUID

from resume.domain.exceptions import ResumeNotFound
from resume.domain.repositories import ResumeRepository


class DeleteResume:
    def __init__(self, repo: ResumeRepository) -> None:
        self._repo = repo

    async def execute(self, resume_id: UUID) -> None:
        resume = await self._repo.get_by_id(resume_id)
        if resume is None:
            raise ResumeNotFound(resume_id)
        await self._repo.delete(resume_id)
