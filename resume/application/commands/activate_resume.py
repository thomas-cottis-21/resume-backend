from uuid import UUID

from resume.application.dtos import ResumeOutput
from resume.domain.exceptions import ResumeNotFound
from resume.domain.repositories import ResumeRepository


class ActivateResume:
    def __init__(self, repo: ResumeRepository) -> None:
        self._repo = repo

    async def execute(self, resume_id: UUID) -> ResumeOutput:
        resume = await self._repo.get_by_id(resume_id)
        if resume is None:
            raise ResumeNotFound(resume_id)
        await self._repo.deactivate_all_for_user(resume.user_id)
        resume.is_active = True
        await self._repo.save(resume)
        return ResumeOutput(
            id=resume.id,
            user_id=resume.user_id,
            tagline=resume.tagline,
            is_active=resume.is_active,
            created_at=resume.created_at,
            updated_at=resume.updated_at,
        )
