from uuid import UUID

from resume.application.dtos import ProjectOutput, TechnologyOutput
from resume.domain.repositories import ProjectRepository


class ListProjects:
    def __init__(self, repo: ProjectRepository) -> None:
        self._repo = repo

    async def execute(self, resume_id: UUID) -> list[ProjectOutput]:
        projects = await self._repo.list_by_resume(resume_id)
        return [
            ProjectOutput(
                id=p.id,
                resume_id=p.resume_id,
                name=p.name,
                description=p.description,
                github_url=p.github_url,
                live_url=p.live_url,
                sort_order=p.sort_order,
                created_at=p.created_at,
                updated_at=p.updated_at,
                technologies=[
                    TechnologyOutput(id=t.id, name=t.name) for t in p.technologies
                ],
            )
            for p in projects
        ]
