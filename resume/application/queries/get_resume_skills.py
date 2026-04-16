from uuid import UUID

from resume.application.dtos import ResumeSkillEntryOutput, SkillOutput
from resume.domain.repositories import SkillRepository


class GetResumeSkills:
    def __init__(self, repo: SkillRepository) -> None:
        self._repo = repo

    async def execute(self, resume_id: UUID) -> list[ResumeSkillEntryOutput]:
        entries = await self._repo.get_resume_skills(resume_id)
        return [
            ResumeSkillEntryOutput(
                skill_id=e.skill_id,
                sort_order=e.sort_order,
                skill=(
                    SkillOutput(
                        id=e.skill.id,
                        name=e.skill.name,
                        category_id=e.skill.category_id,
                    )
                    if e.skill
                    else None
                ),
            )
            for e in entries
        ]
