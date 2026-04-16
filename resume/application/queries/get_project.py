from uuid import UUID

from resume.application.dtos import ProjectOutput, TechnologyOutput
from resume.domain.exceptions import ProjectNotFound
from resume.domain.repositories import ProjectRepository


class GetProject:
    def __init__(self, repo: ProjectRepository) -> None:
        self._repo = repo

    async def execute(self, project_id: UUID) -> ProjectOutput:
        project = await self._repo.get_by_id(project_id)
        if project is None:
            raise ProjectNotFound(project_id)
        return ProjectOutput(
            id=project.id,
            resume_id=project.resume_id,
            name=project.name,
            description=project.description,
            github_url=project.github_url,
            live_url=project.live_url,
            sort_order=project.sort_order,
            created_at=project.created_at,
            updated_at=project.updated_at,
            technologies=[
                TechnologyOutput(id=t.id, name=t.name) for t in project.technologies
            ],
        )
