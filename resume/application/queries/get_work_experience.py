from uuid import UUID

from resume.application.dtos import BulletOutput, WorkExperienceOutput
from resume.domain.exceptions import WorkExperienceNotFound
from resume.domain.repositories import WorkExperienceRepository


class GetWorkExperience:
    def __init__(self, repo: WorkExperienceRepository) -> None:
        self._repo = repo

    async def execute(self, experience_id: UUID) -> WorkExperienceOutput:
        exp = await self._repo.get_by_id(experience_id)
        if exp is None:
            raise WorkExperienceNotFound(experience_id)
        return WorkExperienceOutput(
            id=exp.id,
            resume_id=exp.resume_id,
            company=exp.company,
            role=exp.role,
            location=exp.location,
            start_date=exp.start_date,
            end_date=exp.end_date,
            sort_order=exp.sort_order,
            created_at=exp.created_at,
            updated_at=exp.updated_at,
            bullets=[
                BulletOutput(
                    id=b.id,
                    experience_id=b.experience_id,
                    content=b.content,
                    sort_order=b.sort_order,
                )
                for b in exp.bullets
            ],
        )
