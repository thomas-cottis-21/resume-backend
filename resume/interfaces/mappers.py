from resume.application.dtos import (
    BulletOutput,
    EducationOutput,
    ProjectOutput,
    ResumeLinkOutput,
    ResumeOutput,
    ResumeSkillEntryOutput,
    SkillCategoryOutput,
    SkillOutput,
    TechnologyOutput,
    WorkExperienceOutput,
)
from resume.interfaces.schemas import (
    BulletResponse,
    EducationResponse,
    ProjectResponse,
    ResumeLinkResponse,
    ResumeResponse,
    ResumeSkillEntryResponse,
    SkillCategoryResponse,
    SkillResponse,
    TechnologyResponse,
    WorkExperienceResponse,
)


def resume_to_response(dto: ResumeOutput) -> ResumeResponse:
    return ResumeResponse(
        id=dto.id,
        user_id=dto.user_id,
        tagline=dto.tagline,
        title=dto.title,
        is_active=dto.is_active,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )


def resume_link_to_response(dto: ResumeLinkOutput) -> ResumeLinkResponse:
    return ResumeLinkResponse(
        id=dto.id,
        resume_id=dto.resume_id,
        label=dto.label,
        url=dto.url,
        sort_order=dto.sort_order,
    )


def work_experience_to_response(dto: WorkExperienceOutput) -> WorkExperienceResponse:
    return WorkExperienceResponse(
        id=dto.id,
        resume_id=dto.resume_id,
        company=dto.company,
        role=dto.role,
        location=dto.location,
        start_date=dto.start_date,
        end_date=dto.end_date,
        sort_order=dto.sort_order,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        bullets=[
            BulletResponse(
                id=b.id,
                experience_id=b.experience_id,
                content=b.content,
                sort_order=b.sort_order,
            )
            for b in dto.bullets
        ],
    )


def education_to_response(dto: EducationOutput) -> EducationResponse:
    return EducationResponse(
        id=dto.id,
        resume_id=dto.resume_id,
        institution=dto.institution,
        degree=dto.degree,
        start_year=dto.start_year,
        end_year=dto.end_year,
        sort_order=dto.sort_order,
        created_at=dto.created_at,
    )


def project_to_response(dto: ProjectOutput) -> ProjectResponse:
    return ProjectResponse(
        id=dto.id,
        resume_id=dto.resume_id,
        name=dto.name,
        description=dto.description,
        github_url=dto.github_url,
        live_url=dto.live_url,
        sort_order=dto.sort_order,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        technologies=[
            TechnologyResponse(id=t.id, name=t.name) for t in dto.technologies
        ],
    )


def skill_category_to_response(dto: SkillCategoryOutput) -> SkillCategoryResponse:
    return SkillCategoryResponse(
        id=dto.id,
        name=dto.name,
        sort_order=dto.sort_order,
        skills=[
            SkillResponse(id=s.id, name=s.name, category_id=s.category_id)
            for s in dto.skills
        ],
    )


def resume_skill_entry_to_response(dto: ResumeSkillEntryOutput) -> ResumeSkillEntryResponse:
    return ResumeSkillEntryResponse(
        skill_id=dto.skill_id,
        sort_order=dto.sort_order,
        skill=(
            SkillResponse(
                id=dto.skill.id,
                name=dto.skill.name,
                category_id=dto.skill.category_id,
            )
            if dto.skill
            else None
        ),
    )
