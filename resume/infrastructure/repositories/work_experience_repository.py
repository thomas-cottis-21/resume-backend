from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from resume.domain.entities import WorkExperience, WorkExperienceBullet
from resume.domain.repositories import WorkExperienceRepository
from resume.infrastructure.models import WorkExperienceBulletModel, WorkExperienceModel


def _bullet_to_entity(m: WorkExperienceBulletModel) -> WorkExperienceBullet:
    return WorkExperienceBullet(
        id=m.id,
        experience_id=m.experience_id,
        content=m.content,
        sort_order=m.sort_order,
    )


def _to_entity(m: WorkExperienceModel) -> WorkExperience:
    return WorkExperience(
        id=m.id,
        resume_id=m.resume_id,
        company=m.company,
        role=m.role,
        location=m.location,
        start_date=m.start_date,
        end_date=m.end_date,
        sort_order=m.sort_order,
        created_at=m.created_at,
        updated_at=m.updated_at,
        bullets=[_bullet_to_entity(b) for b in m.bullets],
    )


class SqlAlchemyWorkExperienceRepository(WorkExperienceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, experience_id: UUID) -> WorkExperience | None:
        result = await self._session.execute(
            select(WorkExperienceModel)
            .options(selectinload(WorkExperienceModel.bullets))
            .where(WorkExperienceModel.id == experience_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_by_resume(self, resume_id: UUID) -> list[WorkExperience]:
        result = await self._session.execute(
            select(WorkExperienceModel)
            .options(selectinload(WorkExperienceModel.bullets))
            .where(WorkExperienceModel.resume_id == resume_id)
            .order_by(WorkExperienceModel.sort_order)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, experience: WorkExperience) -> None:
        existing = await self._session.get(WorkExperienceModel, experience.id)
        if existing:
            existing.company = experience.company
            existing.role = experience.role
            existing.location = experience.location
            existing.start_date = experience.start_date
            existing.end_date = experience.end_date
            existing.sort_order = experience.sort_order
            existing.updated_at = experience.updated_at
        else:
            self._session.add(
                WorkExperienceModel(
                    id=experience.id,
                    resume_id=experience.resume_id,
                    company=experience.company,
                    role=experience.role,
                    location=experience.location,
                    start_date=experience.start_date,
                    end_date=experience.end_date,
                    sort_order=experience.sort_order,
                    created_at=experience.created_at,
                    updated_at=experience.updated_at,
                )
            )
        await self._session.flush()

    async def save_bullets(
        self, experience_id: UUID, bullets: list[WorkExperienceBullet]
    ) -> None:
        await self._session.execute(
            delete(WorkExperienceBulletModel).where(
                WorkExperienceBulletModel.experience_id == experience_id
            )
        )
        for bullet in bullets:
            self._session.add(
                WorkExperienceBulletModel(
                    id=bullet.id,
                    experience_id=bullet.experience_id,
                    content=bullet.content,
                    sort_order=bullet.sort_order,
                )
            )
        await self._session.flush()

    async def delete(self, experience_id: UUID) -> None:
        await self._session.execute(
            delete(WorkExperienceModel).where(
                WorkExperienceModel.id == experience_id
            )
        )
        await self._session.flush()

    async def update_sort_orders(self, items: list[tuple[UUID, int]]) -> None:
        for exp_id, sort_order in items:
            await self._session.execute(
                update(WorkExperienceModel)
                .where(WorkExperienceModel.id == exp_id)
                .values(sort_order=sort_order)
            )
        await self._session.flush()
