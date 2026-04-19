from uuid import UUID

from resume.application.dtos import ResumeOutput
from resume.domain.exceptions import ResumeNotFound
from resume.domain.repositories import ResumeRepository


class GetResumeById:
    def __init__(self, repo: ResumeRepository) -> None:
        self._repo = repo

    async def execute(self, resume_id: UUID) -> ResumeOutput:
        resume = await self._repo.get_by_id(resume_id)
        if resume is None:
            raise ResumeNotFound(resume_id)
        return ResumeOutput(
            id=resume.id,
            user_id=resume.user_id,
            tagline=resume.tagline,
            title=resume.title,
            is_active=resume.is_active,
            created_at=resume.created_at,
            updated_at=resume.updated_at,
        )
