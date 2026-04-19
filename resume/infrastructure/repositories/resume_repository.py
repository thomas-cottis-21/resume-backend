from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from resume.domain.entities import Resume
from resume.domain.repositories import ResumeRepository
from resume.infrastructure.models import ResumeModel


def _to_entity(m: ResumeModel) -> Resume:
    return Resume(
        id=m.id,
        user_id=m.user_id,
        tagline=m.tagline,
        title=m.title,
        is_active=m.is_active,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


class SqlAlchemyResumeRepository(ResumeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, resume_id: UUID) -> Resume | None:
        result = await self._session.execute(
            select(ResumeModel).where(ResumeModel.id == resume_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_active_for_user(self, user_id: UUID) -> Resume | None:
        result = await self._session.execute(
            select(ResumeModel).where(
                ResumeModel.user_id == user_id,
                ResumeModel.is_active.is_(True),
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[Resume]:
        result = await self._session.execute(
            select(ResumeModel)
            .where(ResumeModel.user_id == user_id)
            .order_by(ResumeModel.created_at.desc())
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, resume: Resume) -> None:
        existing = await self._session.get(ResumeModel, resume.id)
        if existing:
            existing.tagline = resume.tagline
            existing.title = resume.title
            existing.is_active = resume.is_active
            existing.updated_at = resume.updated_at
        else:
            self._session.add(
                ResumeModel(
                    id=resume.id,
                    user_id=resume.user_id,
                    tagline=resume.tagline,
                    title=resume.title,
                    is_active=resume.is_active,
                    created_at=resume.created_at,
                    updated_at=resume.updated_at,
                )
            )
        await self._session.flush()

    async def delete(self, resume_id: UUID) -> None:
        await self._session.execute(
            delete(ResumeModel).where(ResumeModel.id == resume_id)
        )
        await self._session.flush()

    async def deactivate_all_for_user(self, user_id: UUID) -> None:
        await self._session.execute(
            update(ResumeModel)
            .where(ResumeModel.user_id == user_id)
            .values(is_active=False)
        )
        await self._session.flush()
