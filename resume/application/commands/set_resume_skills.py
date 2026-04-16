from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from resume.domain.entities import ResumeSkillEntry
from resume.domain.repositories import SkillRepository


@dataclass
class SkillEntryInput:
    skill_id: UUID
    sort_order: int


class SetResumeSkills:
    def __init__(self, repo: SkillRepository) -> None:
        self._repo = repo

    async def execute(self, resume_id: UUID, entries: list[SkillEntryInput]) -> None:
        skill_entries = [
            ResumeSkillEntry(skill_id=e.skill_id, sort_order=e.sort_order)
            for e in entries
        ]
        await self._repo.set_resume_skills(resume_id, skill_entries)
