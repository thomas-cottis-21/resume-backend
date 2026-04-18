from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from resume.domain.entities import ResumeSkillEntry, Skill, SkillCategory, Technology
from resume.domain.repositories import SkillRepository
from resume.infrastructure.models import (
    ResumeSkillModel,
    SkillCategoryModel,
    SkillModel,
    TechnologyModel,
)


class SqlAlchemySkillRepository(SkillRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Skill]:
        result = await self._session.execute(
            select(SkillModel).order_by(SkillModel.name)
        )
        return [
            Skill(id=m.id, name=m.name, category_id=m.category_id)
            for m in result.scalars().all()
        ]

    async def list_categories(self) -> list[SkillCategory]:
        result = await self._session.execute(
            select(SkillCategoryModel)
            .options(selectinload(SkillCategoryModel.skills))
            .order_by(SkillCategoryModel.sort_order)
        )
        categories = []
        for m in result.scalars().all():
            skills = [
                Skill(id=s.id, name=s.name, category_id=s.category_id)
                for s in sorted(m.skills, key=lambda s: s.name)
            ]
            categories.append(
                SkillCategory(
                    id=m.id,
                    name=m.name,
                    sort_order=m.sort_order,
                    skills=skills,
                )
            )
        return categories

    async def get_resume_skills(self, resume_id: UUID) -> list[ResumeSkillEntry]:
        result = await self._session.execute(
            select(ResumeSkillModel, SkillModel)
            .join(SkillModel, ResumeSkillModel.skill_id == SkillModel.id)
            .where(ResumeSkillModel.resume_id == resume_id)
            .order_by(ResumeSkillModel.sort_order)
        )
        return [
            ResumeSkillEntry(
                skill_id=rs.skill_id,
                sort_order=rs.sort_order,
                skill=Skill(id=skill.id, name=skill.name, category_id=skill.category_id),
            )
            for rs, skill in result.all()
        ]

    async def set_resume_skills(
        self, resume_id: UUID, entries: list[ResumeSkillEntry]
    ) -> None:
        await self._session.execute(
            delete(ResumeSkillModel).where(
                ResumeSkillModel.resume_id == resume_id
            )
        )
        for entry in entries:
            self._session.add(
                ResumeSkillModel(
                    resume_id=resume_id,
                    skill_id=entry.skill_id,
                    sort_order=entry.sort_order,
                )
            )
        await self._session.flush()

    async def list_technologies(self) -> list[Technology]:
        result = await self._session.execute(
            select(TechnologyModel).order_by(TechnologyModel.name)
        )
        return [Technology(id=m.id, name=m.name) for m in result.scalars().all()]
