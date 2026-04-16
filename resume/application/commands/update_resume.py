from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from resume.application.dtos import ResumeOutput
from resume.domain.exceptions import ResumeNotFound
from resume.domain.repositories import ResumeRepository


@dataclass
class UpdateResumeInput:
    resume_id: UUID
    tagline: str | None


class UpdateResume:
    def __init__(self, repo: ResumeRepository) -> None:
        self._repo = repo

    async def execute(self, input: UpdateResumeInput) -> ResumeOutput:
        resume = await self._repo.get_by_id(input.resume_id)
        if resume is None:
            raise ResumeNotFound(input.resume_id)
        resume.tagline = input.tagline
        resume.updated_at = datetime.now(tz=timezone.utc)
        await self._repo.save(resume)
        return ResumeOutput(
            id=resume.id,
            user_id=resume.user_id,
            tagline=resume.tagline,
            is_active=resume.is_active,
            created_at=resume.created_at,
            updated_at=resume.updated_at,
        )
