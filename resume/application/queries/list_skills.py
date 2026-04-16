from resume.application.dtos import SkillOutput
from resume.domain.repositories import SkillRepository


class ListSkills:
    def __init__(self, repo: SkillRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[SkillOutput]:
        skills = await self._repo.list_all()
        return [
            SkillOutput(id=s.id, name=s.name, category_id=s.category_id)
            for s in skills
        ]
