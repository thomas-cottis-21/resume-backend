from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from resume.domain.entities import ResumeLink
from resume.infrastructure.models import ResumeLinkModel


class SqlAlchemyResumeLinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_resume(self, resume_id: UUID) -> list[ResumeLink]:
        result = await self._session.execute(
            select(ResumeLinkModel)
            .where(ResumeLinkModel.resume_id == resume_id)
            .order_by(ResumeLinkModel.sort_order)
        )
        return [_to_entity(m) for m in result.scalars().all()]


def _to_entity(m: ResumeLinkModel) -> ResumeLink:
    return ResumeLink(
        id=m.id,
        resume_id=m.resume_id,
        label=m.label,
        url=m.url,
        sort_order=m.sort_order,
    )
