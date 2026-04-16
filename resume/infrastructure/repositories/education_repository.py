from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from resume.domain.entities import Education
from resume.domain.repositories import EducationRepository
from resume.infrastructure.models import EducationModel


def _to_entity(m: EducationModel) -> Education:
    return Education(
        id=UUID(m.id),
        resume_id=UUID(m.resume_id),
        institution=m.institution,
        degree=m.degree,
        start_year=m.start_year,
        end_year=m.end_year,
        sort_order=m.sort_order,
        created_at=m.created_at,
    )


class SqlAlchemyEducationRepository(EducationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, education_id: UUID) -> Education | None:
        result = await self._session.execute(
            select(EducationModel).where(EducationModel.id == str(education_id))
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_by_resume(self, resume_id: UUID) -> list[Education]:
        result = await self._session.execute(
            select(EducationModel)
            .where(EducationModel.resume_id == str(resume_id))
            .order_by(EducationModel.sort_order)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, education: Education) -> None:
        existing = await self._session.get(EducationModel, str(education.id))
        if existing:
            existing.institution = education.institution
            existing.degree = education.degree
            existing.start_year = education.start_year
            existing.end_year = education.end_year
            existing.sort_order = education.sort_order
        else:
            self._session.add(
                EducationModel(
                    id=str(education.id),
                    resume_id=str(education.resume_id),
                    institution=education.institution,
                    degree=education.degree,
                    start_year=education.start_year,
                    end_year=education.end_year,
                    sort_order=education.sort_order,
                    created_at=education.created_at,
                )
            )
        await self._session.flush()

    async def delete(self, education_id: UUID) -> None:
        await self._session.execute(
            delete(EducationModel).where(EducationModel.id == str(education_id))
        )
        await self._session.flush()
