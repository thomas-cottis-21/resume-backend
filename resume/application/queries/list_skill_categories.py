from resume.application.dtos import SkillCategoryOutput, SkillOutput
from resume.domain.repositories import SkillRepository


class ListSkillCategories:
    def __init__(self, repo: SkillRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[SkillCategoryOutput]:
        categories = await self._repo.list_categories()
        return [
            SkillCategoryOutput(
                id=c.id,
                name=c.name,
                sort_order=c.sort_order,
                skills=[
                    SkillOutput(id=s.id, name=s.name, category_id=s.category_id)
                    for s in c.skills
                ],
            )
            for c in categories
        ]
