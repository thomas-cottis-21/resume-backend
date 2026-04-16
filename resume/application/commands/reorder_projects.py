from resume.application.dtos import ReorderItem
from resume.domain.repositories import ProjectRepository


class ReorderProjects:
    def __init__(self, repo: ProjectRepository) -> None:
        self._repo = repo

    async def execute(self, items: list[ReorderItem]) -> None:
        await self._repo.update_sort_orders(
            [(item.id, item.sort_order) for item in items]
        )
