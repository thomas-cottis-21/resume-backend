from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from resume.domain.entities import Project, Technology
from resume.domain.repositories import ProjectRepository
from resume.infrastructure.models import ProjectModel, ProjectTechnologyModel, TechnologyModel


def _to_entity(m: ProjectModel) -> Project:
    technologies = [
        Technology(id=UUID(pt.technology.id), name=pt.technology.name)
        for pt in sorted(m.project_technologies, key=lambda pt: pt.sort_order)
        if pt.technology is not None
    ]
    return Project(
        id=UUID(m.id),
        resume_id=UUID(m.resume_id),
        name=m.name,
        description=m.description,
        github_url=m.github_url,
        live_url=m.live_url,
        sort_order=m.sort_order,
        created_at=m.created_at,
        updated_at=m.updated_at,
        technologies=technologies,
    )


class SqlAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, project_id: UUID) -> Project | None:
        result = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.project_technologies).selectinload(
                    ProjectTechnologyModel.technology
                )
            )
            .where(ProjectModel.id == str(project_id))
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_by_resume(self, resume_id: UUID) -> list[Project]:
        result = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.project_technologies).selectinload(
                    ProjectTechnologyModel.technology
                )
            )
            .where(ProjectModel.resume_id == str(resume_id))
            .order_by(ProjectModel.sort_order)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, project: Project) -> None:
        existing = await self._session.get(ProjectModel, str(project.id))
        if existing:
            existing.name = project.name
            existing.description = project.description
            existing.github_url = project.github_url
            existing.live_url = project.live_url
            existing.sort_order = project.sort_order
            existing.updated_at = project.updated_at
        else:
            self._session.add(
                ProjectModel(
                    id=str(project.id),
                    resume_id=str(project.resume_id),
                    name=project.name,
                    description=project.description,
                    github_url=project.github_url,
                    live_url=project.live_url,
                    sort_order=project.sort_order,
                    created_at=project.created_at,
                    updated_at=project.updated_at,
                )
            )
        await self._session.flush()

    async def save_technologies(
        self, project_id: UUID, technology_ids: list[tuple[UUID, int]]
    ) -> None:
        await self._session.execute(
            delete(ProjectTechnologyModel).where(
                ProjectTechnologyModel.project_id == str(project_id)
            )
        )
        for tech_id, sort_order in technology_ids:
            self._session.add(
                ProjectTechnologyModel(
                    project_id=str(project_id),
                    technology_id=str(tech_id),
                    sort_order=sort_order,
                )
            )
        await self._session.flush()

    async def delete(self, project_id: UUID) -> None:
        await self._session.execute(
            delete(ProjectModel).where(ProjectModel.id == str(project_id))
        )
        await self._session.flush()

    async def update_sort_orders(self, items: list[tuple[UUID, int]]) -> None:
        for project_id, sort_order in items:
            await self._session.execute(
                update(ProjectModel)
                .where(ProjectModel.id == str(project_id))
                .values(sort_order=sort_order)
            )
        await self._session.flush()
