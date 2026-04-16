from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from resume.application.commands.add_education import AddEducation, AddEducationInput
from resume.application.commands.delete_education import DeleteEducation
from resume.application.commands.update_education import UpdateEducation, UpdateEducationInput
from resume.application.queries.get_education_entry import GetEducationEntry
from resume.application.queries.list_education import ListEducation
from core.exceptions import NotFoundError
from resume.interfaces.dependencies import (
    get_add_education,
    get_delete_education,
    get_education_entry,
    get_list_education,
    get_update_education,
)
from resume.interfaces.mappers import education_to_response
from resume.interfaces.schemas import (
    EducationCreateRequest,
    EducationResponse,
    EducationUpdateRequest,
)

router = APIRouter(prefix="/resumes/{resume_id}/education", tags=["education"])


@router.get("", response_model=list[EducationResponse])
async def list_education(
    resume_id: UUID,
    use_case: ListEducation = Depends(get_list_education),
) -> list[EducationResponse]:
    results = await use_case.execute(resume_id)
    return [education_to_response(r) for r in results]


@router.post("", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_education(
    resume_id: UUID,
    body: EducationCreateRequest,
    use_case: AddEducation = Depends(get_add_education),
) -> EducationResponse:
    result = await use_case.execute(
        AddEducationInput(
            resume_id=resume_id,
            institution=body.institution,
            degree=body.degree,
            start_year=body.start_year,
            end_year=body.end_year,
            sort_order=body.sort_order,
        )
    )
    return education_to_response(result)


@router.get("/{education_id}", response_model=EducationResponse)
async def get_education(
    resume_id: UUID,
    education_id: UUID,
    use_case: GetEducationEntry = Depends(get_education_entry),
) -> EducationResponse:
    try:
        result = await use_case.execute(education_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return education_to_response(result)


@router.put("/{education_id}", response_model=EducationResponse)
async def update_education(
    resume_id: UUID,
    education_id: UUID,
    body: EducationUpdateRequest,
    use_case: UpdateEducation = Depends(get_update_education),
) -> EducationResponse:
    try:
        result = await use_case.execute(
            UpdateEducationInput(
                education_id=education_id,
                institution=body.institution,
                degree=body.degree,
                start_year=body.start_year,
                end_year=body.end_year,
                sort_order=body.sort_order,
            )
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return education_to_response(result)


@router.delete("/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    resume_id: UUID,
    education_id: UUID,
    use_case: DeleteEducation = Depends(get_delete_education),
) -> None:
    try:
        await use_case.execute(education_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
