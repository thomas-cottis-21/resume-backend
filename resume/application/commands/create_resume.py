from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from resume.application.dtos import ResumeOutput
from resume.domain.entities import Resume
from resume.domain.repositories import ResumeRepository


@dataclass
class CreateResumeInput:
    user_id: UUID
    tagline: str | None = None


class CreateResume:
    def __init__(self, repo: ResumeRepository) -> None:
        self._repo = repo

    async def execute(self, input: CreateResumeInput) -> ResumeOutput:
        now = datetime.now(tz=timezone.utc)
        resume = Resume(
            id=uuid4(),
            user_id=input.user_id,
            tagline=input.tagline,
            title=None,
            is_active=False,
            created_at=now,
            updated_at=now,
        )
        await self._repo.save(resume)
        return ResumeOutput(
            id=resume.id,
            user_id=resume.user_id,
            tagline=resume.tagline,
            title=resume.title,
            is_active=resume.is_active,
            created_at=resume.created_at,
            updated_at=resume.updated_at,
        )
