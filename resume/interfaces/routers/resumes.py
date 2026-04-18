from uuid import UUID

from fastapi import APIRouter, Depends, status

from resume.application.commands.activate_resume import ActivateResume
from resume.application.commands.create_resume import CreateResume, CreateResumeInput
from resume.application.commands.delete_resume import DeleteResume
from resume.application.commands.update_resume import UpdateResume, UpdateResumeInput
from resume.application.queries.get_active_resume import GetActiveResume
from resume.application.queries.get_resume_by_id import GetResumeById
from resume.application.queries.list_resumes import ListResumes
from resume.interfaces.dependencies import (
    get_activate_resume,
    get_active_resume,
    get_create_resume,
    get_delete_resume,
    get_list_resumes,
    get_resume_by_id,
    get_update_resume,
)
from resume.interfaces.mappers import resume_to_response
from resume.interfaces.schemas import ResumeCreateRequest, ResumeResponse, ResumeUpdateRequest

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("", response_model=list[ResumeResponse])
async def list_resumes(
    user_id: UUID,
    use_case: ListResumes = Depends(get_list_resumes),
) -> list[ResumeResponse]:
    results = await use_case.execute(user_id)
    return [resume_to_response(r) for r in results]


@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    body: ResumeCreateRequest,
    use_case: CreateResume = Depends(get_create_resume),
) -> ResumeResponse:
    result = await use_case.execute(
        CreateResumeInput(user_id=body.user_id, tagline=body.tagline)
    )
    return resume_to_response(result)


@router.get("/active", response_model=ResumeResponse)
async def get_active_resume_route(
    user_id: UUID,
    use_case: GetActiveResume = Depends(get_active_resume),
) -> ResumeResponse:
    result = await use_case.execute(user_id)
    return resume_to_response(result)


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: UUID,
    use_case: GetResumeById = Depends(get_resume_by_id),
) -> ResumeResponse:
    result = await use_case.execute(resume_id)
    return resume_to_response(result)


@router.patch("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: UUID,
    body: ResumeUpdateRequest,
    use_case: UpdateResume = Depends(get_update_resume),
) -> ResumeResponse:
    result = await use_case.execute(UpdateResumeInput(resume_id=resume_id, tagline=body.tagline))
    return resume_to_response(result)


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: UUID,
    use_case: DeleteResume = Depends(get_delete_resume),
) -> None:
    await use_case.execute(resume_id)


@router.post("/{resume_id}/activate", response_model=ResumeResponse)
async def activate_resume(
    resume_id: UUID,
    use_case: ActivateResume = Depends(get_activate_resume),
) -> ResumeResponse:
    result = await use_case.execute(resume_id)
    return resume_to_response(result)
