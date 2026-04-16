from uuid import UUID

from resume.application.dtos import BulletOutput, WorkExperienceOutput
from resume.domain.repositories import WorkExperienceRepository


class ListWorkExperiences:
    def __init__(self, repo: WorkExperienceRepository) -> None:
        self._repo = repo

    async def execute(self, resume_id: UUID) -> list[WorkExperienceOutput]:
        experiences = await self._repo.list_by_resume(resume_id)
        return [
            WorkExperienceOutput(
                id=e.id,
                resume_id=e.resume_id,
                company=e.company,
                role=e.role,
                location=e.location,
                start_date=e.start_date,
                end_date=e.end_date,
                sort_order=e.sort_order,
                created_at=e.created_at,
                updated_at=e.updated_at,
                bullets=[
                    BulletOutput(
                        id=b.id,
                        experience_id=b.experience_id,
                        content=b.content,
                        sort_order=b.sort_order,
                    )
                    for b in e.bullets
                ],
            )
            for e in experiences
        ]
