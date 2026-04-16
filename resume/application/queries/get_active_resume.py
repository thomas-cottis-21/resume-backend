from uuid import UUID

from resume.application.dtos import ResumeOutput
from resume.domain.exceptions import NoActiveResume
from resume.domain.repositories import ResumeRepository


class GetActiveResume:
    def __init__(self, repo: ResumeRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: UUID) -> ResumeOutput:
        resume = await self._repo.get_active_for_user(user_id)
        if resume is None:
            raise NoActiveResume(user_id)
        return ResumeOutput(
            id=resume.id,
            user_id=resume.user_id,
            tagline=resume.tagline,
            is_active=resume.is_active,
            created_at=resume.created_at,
            updated_at=resume.updated_at,
        )
