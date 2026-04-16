from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from resume.application.dtos import ProjectOutput, TechnologyOutput
from resume.domain.entities import Project, Technology
from resume.domain.repositories import ProjectRepository


@dataclass
class AddProjectInput:
    resume_id: UUID
    name: str
    description: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    sort_order: int = 0
    technology_ids: list[tuple[UUID, int]] = field(default_factory=list)
    """List of (technology_id, sort_order) tuples."""


class AddProject:
    def __init__(self, repo: ProjectRepository) -> None:
        self._repo = repo

    async def execute(self, input: AddProjectInput) -> ProjectOutput:
        now = datetime.now(tz=timezone.utc)
        project = Project(
            id=uuid4(),
            resume_id=input.resume_id,
            name=input.name,
            description=input.description,
            github_url=input.github_url,
            live_url=input.live_url,
            sort_order=input.sort_order,
            created_at=now,
            updated_at=now,
        )
        await self._repo.save(project)
        if input.technology_ids:
            await self._repo.save_technologies(project.id, input.technology_ids)
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
            technologies=[],
        )
