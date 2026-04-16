from uuid import UUID

from resume.domain.exceptions import ProjectNotFound
from resume.domain.repositories import ProjectRepository


class DeleteProject:
    def __init__(self, repo: ProjectRepository) -> None:
        self._repo = repo

    async def execute(self, project_id: UUID) -> None:
        project = await self._repo.get_by_id(project_id)
        if project is None:
            raise ProjectNotFound(project_id)
        await self._repo.delete(project_id)
