from uuid import UUID

from fastapi import APIRouter, Depends, status

from resume.application.commands.set_resume_skills import SetResumeSkills, SkillEntryInput
from resume.application.queries.get_resume_skills import GetResumeSkills
from resume.application.queries.list_skill_categories import ListSkillCategories
from resume.application.queries.list_skills import ListSkills
from resume.application.queries.list_technologies import ListTechnologies
from resume.interfaces.dependencies import (
    get_resume_skills as get_resume_skills_use_case,
    get_list_skill_categories,
    get_list_skills,
    get_list_technologies,
    get_set_resume_skills,
)
from resume.interfaces.mappers import resume_skill_entry_to_response, skill_category_to_response
from resume.interfaces.schemas import (
    ResumeSkillEntryResponse,
    SetResumeSkillsRequest,
    SkillCategoryResponse,
    SkillResponse,
    TechnologyResponse,
)

router = APIRouter(tags=["skills"])


@router.get("/skill-categories", response_model=list[SkillCategoryResponse])
async def list_skill_categories(
    use_case: ListSkillCategories = Depends(get_list_skill_categories),
) -> list[SkillCategoryResponse]:
    results = await use_case.execute()
    return [skill_category_to_response(r) for r in results]


@router.get("/skills", response_model=list[SkillResponse])
async def list_skills(
    use_case: ListSkills = Depends(get_list_skills),
) -> list[SkillResponse]:
    results = await use_case.execute()
    return [SkillResponse(id=s.id, name=s.name, category_id=s.category_id) for s in results]


@router.get("/technologies", response_model=list[TechnologyResponse])
async def list_technologies(
    use_case: ListTechnologies = Depends(get_list_technologies),
) -> list[TechnologyResponse]:
    results = await use_case.execute()
    return [TechnologyResponse(id=t.id, name=t.name) for t in results]


@router.get("/resumes/{resume_id}/skills", response_model=list[ResumeSkillEntryResponse])
async def get_resume_skills(
    resume_id: UUID,
    use_case: GetResumeSkills = Depends(get_resume_skills_use_case),
) -> list[ResumeSkillEntryResponse]:
    results = await use_case.execute(resume_id)
    return [resume_skill_entry_to_response(r) for r in results]


@router.put(
    "/resumes/{resume_id}/skills",
    response_model=list[ResumeSkillEntryResponse],
    status_code=status.HTTP_200_OK,
)
async def set_resume_skills(
    resume_id: UUID,
    body: SetResumeSkillsRequest,
    set_use_case: SetResumeSkills = Depends(get_set_resume_skills),
    get_use_case: GetResumeSkills = Depends(get_resume_skills_use_case),
) -> list[ResumeSkillEntryResponse]:
    await set_use_case.execute(
        resume_id,
        [SkillEntryInput(skill_id=s.skill_id, sort_order=s.sort_order) for s in body.skills],
    )
    results = await get_use_case.execute(resume_id)
    return [resume_skill_entry_to_response(r) for r in results]
