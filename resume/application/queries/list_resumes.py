from uuid import UUID

from resume.application.dtos import ResumeOutput
from resume.domain.entities import Resume
from resume.domain.repositories import ResumeRepository


def _to_output(r: Resume) -> ResumeOutput:
    return ResumeOutput(
        id=r.id,
        user_id=r.user_id,
        tagline=r.tagline,
        is_active=r.is_active,
        created_at=r.created_at,
        updated_at=r.updated_at,
    )


class ListResumes:
    def __init__(self, repo: ResumeRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: UUID) -> list[ResumeOutput]:
        resumes = await self._repo.list_by_user(user_id)
        return [_to_output(r) for r in resumes]
