from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from resume.application.dtos import BulletOutput, WorkExperienceOutput
from resume.domain.entities import WorkExperience, WorkExperienceBullet
from resume.domain.repositories import WorkExperienceRepository


@dataclass
class BulletInput:
    content: str
    sort_order: int


@dataclass
class AddWorkExperienceInput:
    resume_id: UUID
    company: str
    role: str
    start_date: date
    location: str | None = None
    end_date: date | None = None
    sort_order: int = 0
    bullets: list[BulletInput] = field(default_factory=list)


class AddWorkExperience:
    def __init__(self, repo: WorkExperienceRepository) -> None:
        self._repo = repo

    async def execute(self, input: AddWorkExperienceInput) -> WorkExperienceOutput:
        now = datetime.now(tz=timezone.utc)
        exp_id = uuid4()
        bullets = [
            WorkExperienceBullet(
                id=uuid4(),
                experience_id=exp_id,
                content=b.content,
                sort_order=b.sort_order,
            )
            for b in input.bullets
        ]
        experience = WorkExperience(
            id=exp_id,
            resume_id=input.resume_id,
            company=input.company,
            role=input.role,
            location=input.location,
            start_date=input.start_date,
            end_date=input.end_date,
            sort_order=input.sort_order,
            created_at=now,
            updated_at=now,
            bullets=bullets,
        )
        await self._repo.save(experience)
        await self._repo.save_bullets(exp_id, bullets)
        return WorkExperienceOutput(
            id=experience.id,
            resume_id=experience.resume_id,
            company=experience.company,
            role=experience.role,
            location=experience.location,
            start_date=experience.start_date,
            end_date=experience.end_date,
            sort_order=experience.sort_order,
            created_at=experience.created_at,
            updated_at=experience.updated_at,
            bullets=[
                BulletOutput(
                    id=b.id,
                    experience_id=b.experience_id,
                    content=b.content,
                    sort_order=b.sort_order,
                )
                for b in bullets
            ],
        )
