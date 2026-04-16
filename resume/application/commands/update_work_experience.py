from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from resume.application.dtos import BulletOutput, WorkExperienceOutput
from resume.domain.entities import WorkExperienceBullet
from resume.domain.exceptions import WorkExperienceNotFound
from resume.domain.repositories import WorkExperienceRepository


@dataclass
class BulletInput:
    content: str
    sort_order: int


@dataclass
class UpdateWorkExperienceInput:
    experience_id: UUID
    company: str
    role: str
    start_date: date
    location: str | None = None
    end_date: date | None = None
    sort_order: int = 0
    bullets: list[BulletInput] = field(default_factory=list)


class UpdateWorkExperience:
    def __init__(self, repo: WorkExperienceRepository) -> None:
        self._repo = repo

    async def execute(self, input: UpdateWorkExperienceInput) -> WorkExperienceOutput:
        exp = await self._repo.get_by_id(input.experience_id)
        if exp is None:
            raise WorkExperienceNotFound(input.experience_id)
        exp.company = input.company
        exp.role = input.role
        exp.location = input.location
        exp.start_date = input.start_date
        exp.end_date = input.end_date
        exp.sort_order = input.sort_order
        exp.updated_at = datetime.now(tz=timezone.utc)
        new_bullets = [
            WorkExperienceBullet(
                id=uuid4(),
                experience_id=exp.id,
                content=b.content,
                sort_order=b.sort_order,
            )
            for b in input.bullets
        ]
        await self._repo.save(exp)
        await self._repo.save_bullets(exp.id, new_bullets)
        return WorkExperienceOutput(
            id=exp.id,
            resume_id=exp.resume_id,
            company=exp.company,
            role=exp.role,
            location=exp.location,
            start_date=exp.start_date,
            end_date=exp.end_date,
            sort_order=exp.sort_order,
            created_at=exp.created_at,
            updated_at=exp.updated_at,
            bullets=[
                BulletOutput(
                    id=b.id,
                    experience_id=b.experience_id,
                    content=b.content,
                    sort_order=b.sort_order,
                )
                for b in new_bullets
            ],
        )
