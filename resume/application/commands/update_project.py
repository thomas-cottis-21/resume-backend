from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from resume.application.dtos import ProjectOutput, TechnologyOutput
from resume.domain.exceptions import ProjectNotFound
from resume.domain.repositories import ProjectRepository


@dataclass
class UpdateProjectInput:
    project_id: UUID
    name: str
    description: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    sort_order: int = 0
    technology_ids: list[tuple[UUID, int]] = field(default_factory=list)
    """List of (technology_id, sort_order) tuples."""


class UpdateProject:
    def __init__(self, repo: ProjectRepository) -> None:
        self._repo = repo

    async def execute(self, input: UpdateProjectInput) -> ProjectOutput:
        project = await self._repo.get_by_id(input.project_id)
        if project is None:
            raise ProjectNotFound(input.project_id)
        project.name = input.name
        project.description = input.description
        project.github_url = input.github_url
        project.live_url = input.live_url
        project.sort_order = input.sort_order
        project.updated_at = datetime.now(tz=timezone.utc)
        await self._repo.save(project)
        await self._repo.save_technologies(project.id, input.technology_ids)
        refreshed = await self._repo.get_by_id(project.id)
        assert refreshed is not None
        return ProjectOutput(
            id=refreshed.id,
            resume_id=refreshed.resume_id,
            name=refreshed.name,
            description=refreshed.description,
            github_url=refreshed.github_url,
            live_url=refreshed.live_url,
            sort_order=refreshed.sort_order,
            created_at=refreshed.created_at,
            updated_at=refreshed.updated_at,
            technologies=[
                TechnologyOutput(id=t.id, name=t.name) for t in refreshed.technologies
            ],
        )
