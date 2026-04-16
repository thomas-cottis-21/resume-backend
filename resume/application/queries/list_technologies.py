from resume.application.dtos import TechnologyOutput
from resume.domain.repositories import SkillRepository


class ListTechnologies:
    def __init__(self, repo: SkillRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[TechnologyOutput]:
        technologies = await self._repo.list_technologies()
        return [TechnologyOutput(id=t.id, name=t.name) for t in technologies]
