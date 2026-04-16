from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from resume.application.commands.add_work_experience import (
    AddWorkExperience,
    AddWorkExperienceInput,
    BulletInput,
)
from resume.application.commands.delete_work_experience import DeleteWorkExperience
from resume.application.commands.reorder_work_experiences import ReorderWorkExperiences
from resume.application.commands.update_work_experience import (
    UpdateWorkExperience,
    UpdateWorkExperienceInput,
    BulletInput as UpdateBulletInput,
)
from resume.application.dtos import ReorderItem
from resume.application.queries.get_work_experience import GetWorkExperience
from resume.application.queries.list_work_experiences import ListWorkExperiences
from core.exceptions import NotFoundError
from resume.interfaces.dependencies import (
    get_add_work_experience,
    get_delete_work_experience,
    get_list_work_experiences,
    get_reorder_work_experiences,
    get_update_work_experience,
    get_work_experience,
)
from resume.interfaces.mappers import work_experience_to_response
from resume.interfaces.schemas import (
    ReorderRequest,
    WorkExperienceCreateRequest,
    WorkExperienceResponse,
    WorkExperienceUpdateRequest,
)

router = APIRouter(prefix="/resumes/{resume_id}/work-experience", tags=["work-experience"])


@router.get("", response_model=list[WorkExperienceResponse])
async def list_work_experiences(
    resume_id: UUID,
    use_case: ListWorkExperiences = Depends(get_list_work_experiences),
) -> list[WorkExperienceResponse]:
    results = await use_case.execute(resume_id)
    return [work_experience_to_response(r) for r in results]


@router.post("", response_model=WorkExperienceResponse, status_code=status.HTTP_201_CREATED)
async def add_work_experience(
    resume_id: UUID,
    body: WorkExperienceCreateRequest,
    use_case: AddWorkExperience = Depends(get_add_work_experience),
) -> WorkExperienceResponse:
    result = await use_case.execute(
        AddWorkExperienceInput(
            resume_id=resume_id,
            company=body.company,
            role=body.role,
            location=body.location,
            start_date=body.start_date,
            end_date=body.end_date,
            sort_order=body.sort_order,
            bullets=[BulletInput(content=b.content, sort_order=b.sort_order) for b in body.bullets],
        )
    )
    return work_experience_to_response(result)


@router.post("/reorder", status_code=status.HTTP_204_NO_CONTENT)
async def reorder_work_experiences(
    resume_id: UUID,
    body: ReorderRequest,
    use_case: ReorderWorkExperiences = Depends(get_reorder_work_experiences),
) -> None:
    await use_case.execute([ReorderItem(id=item.id, sort_order=item.sort_order) for item in body.items])


@router.get("/{experience_id}", response_model=WorkExperienceResponse)
async def get_work_experience_route(
    resume_id: UUID,
    experience_id: UUID,
    use_case: GetWorkExperience = Depends(get_work_experience),
) -> WorkExperienceResponse:
    try:
        result = await use_case.execute(experience_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return work_experience_to_response(result)


@router.put("/{experience_id}", response_model=WorkExperienceResponse)
async def update_work_experience(
    resume_id: UUID,
    experience_id: UUID,
    body: WorkExperienceUpdateRequest,
    use_case: UpdateWorkExperience = Depends(get_update_work_experience),
) -> WorkExperienceResponse:
    try:
        result = await use_case.execute(
            UpdateWorkExperienceInput(
                experience_id=experience_id,
                company=body.company,
                role=body.role,
                location=body.location,
                start_date=body.start_date,
                end_date=body.end_date,
                sort_order=body.sort_order,
                bullets=[
                    UpdateBulletInput(content=b.content, sort_order=b.sort_order)
                    for b in body.bullets
                ],
            )
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return work_experience_to_response(result)


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_experience(
    resume_id: UUID,
    experience_id: UUID,
    use_case: DeleteWorkExperience = Depends(get_delete_work_experience),
) -> None:
    try:
        await use_case.execute(experience_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
