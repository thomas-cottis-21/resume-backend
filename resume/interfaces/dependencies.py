from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from resume.application.commands.activate_resume import ActivateResume
from resume.application.commands.add_education import AddEducation
from resume.application.commands.add_project import AddProject
from resume.application.commands.add_work_experience import AddWorkExperience
from resume.application.commands.create_resume import CreateResume
from resume.application.commands.delete_education import DeleteEducation
from resume.application.commands.delete_project import DeleteProject
from resume.application.commands.delete_resume import DeleteResume
from resume.application.commands.delete_work_experience import DeleteWorkExperience
from resume.application.commands.reorder_projects import ReorderProjects
from resume.application.commands.reorder_work_experiences import ReorderWorkExperiences
from resume.application.commands.set_resume_skills import SetResumeSkills
from resume.application.commands.update_education import UpdateEducation
from resume.application.commands.update_project import UpdateProject
from resume.application.commands.update_resume import UpdateResume
from resume.application.commands.update_work_experience import UpdateWorkExperience
from resume.application.queries.get_active_resume import GetActiveResume
from resume.application.queries.get_education_entry import GetEducationEntry
from resume.application.queries.get_project import GetProject
from resume.application.queries.get_resume_by_id import GetResumeById
from resume.application.queries.get_resume_skills import GetResumeSkills
from resume.application.queries.get_work_experience import GetWorkExperience
from resume.application.queries.list_education import ListEducation
from resume.application.queries.list_projects import ListProjects
from resume.application.queries.list_resumes import ListResumes
from resume.application.queries.list_skill_categories import ListSkillCategories
from resume.application.queries.list_skills import ListSkills
from resume.application.queries.list_technologies import ListTechnologies
from resume.application.queries.list_work_experiences import ListWorkExperiences
from core.database.session import get_db_session
from resume.infrastructure.repositories.education_repository import SqlAlchemyEducationRepository
from resume.infrastructure.repositories.project_repository import SqlAlchemyProjectRepository
from resume.infrastructure.repositories.resume_repository import SqlAlchemyResumeRepository
from resume.infrastructure.repositories.skill_repository import SqlAlchemySkillRepository
from resume.infrastructure.repositories.work_experience_repository import (
    SqlAlchemyWorkExperienceRepository,
)

# ── Query factories ────────────────────────────────────────────────────────────

async def get_list_resumes(session: AsyncSession = Depends(get_db_session)) -> ListResumes:
    return ListResumes(SqlAlchemyResumeRepository(session))


async def get_resume_by_id(session: AsyncSession = Depends(get_db_session)) -> GetResumeById:
    return GetResumeById(SqlAlchemyResumeRepository(session))


async def get_active_resume(session: AsyncSession = Depends(get_db_session)) -> GetActiveResume:
    return GetActiveResume(SqlAlchemyResumeRepository(session))


async def get_list_work_experiences(
    session: AsyncSession = Depends(get_db_session),
) -> ListWorkExperiences:
    return ListWorkExperiences(SqlAlchemyWorkExperienceRepository(session))


async def get_work_experience(
    session: AsyncSession = Depends(get_db_session),
) -> GetWorkExperience:
    return GetWorkExperience(SqlAlchemyWorkExperienceRepository(session))


async def get_list_education(session: AsyncSession = Depends(get_db_session)) -> ListEducation:
    return ListEducation(SqlAlchemyEducationRepository(session))


async def get_education_entry(
    session: AsyncSession = Depends(get_db_session),
) -> GetEducationEntry:
    return GetEducationEntry(SqlAlchemyEducationRepository(session))


async def get_list_projects(session: AsyncSession = Depends(get_db_session)) -> ListProjects:
    return ListProjects(SqlAlchemyProjectRepository(session))


async def get_project(session: AsyncSession = Depends(get_db_session)) -> GetProject:
    return GetProject(SqlAlchemyProjectRepository(session))


async def get_list_skill_categories(
    session: AsyncSession = Depends(get_db_session),
) -> ListSkillCategories:
    return ListSkillCategories(SqlAlchemySkillRepository(session))


async def get_list_skills(session: AsyncSession = Depends(get_db_session)) -> ListSkills:
    return ListSkills(SqlAlchemySkillRepository(session))


async def get_resume_skills(session: AsyncSession = Depends(get_db_session)) -> GetResumeSkills:
    return GetResumeSkills(SqlAlchemySkillRepository(session))


async def get_list_technologies(
    session: AsyncSession = Depends(get_db_session),
) -> ListTechnologies:
    return ListTechnologies(SqlAlchemySkillRepository(session))


# ── Command factories ──────────────────────────────────────────────────────────

async def get_create_resume(session: AsyncSession = Depends(get_db_session)) -> CreateResume:
    return CreateResume(SqlAlchemyResumeRepository(session))


async def get_update_resume(session: AsyncSession = Depends(get_db_session)) -> UpdateResume:
    return UpdateResume(SqlAlchemyResumeRepository(session))


async def get_delete_resume(session: AsyncSession = Depends(get_db_session)) -> DeleteResume:
    return DeleteResume(SqlAlchemyResumeRepository(session))


async def get_activate_resume(session: AsyncSession = Depends(get_db_session)) -> ActivateResume:
    return ActivateResume(SqlAlchemyResumeRepository(session))


async def get_add_work_experience(
    session: AsyncSession = Depends(get_db_session),
) -> AddWorkExperience:
    return AddWorkExperience(SqlAlchemyWorkExperienceRepository(session))


async def get_update_work_experience(
    session: AsyncSession = Depends(get_db_session),
) -> UpdateWorkExperience:
    return UpdateWorkExperience(SqlAlchemyWorkExperienceRepository(session))


async def get_delete_work_experience(
    session: AsyncSession = Depends(get_db_session),
) -> DeleteWorkExperience:
    return DeleteWorkExperience(SqlAlchemyWorkExperienceRepository(session))


async def get_reorder_work_experiences(
    session: AsyncSession = Depends(get_db_session),
) -> ReorderWorkExperiences:
    return ReorderWorkExperiences(SqlAlchemyWorkExperienceRepository(session))


async def get_add_education(session: AsyncSession = Depends(get_db_session)) -> AddEducation:
    return AddEducation(SqlAlchemyEducationRepository(session))


async def get_update_education(
    session: AsyncSession = Depends(get_db_session),
) -> UpdateEducation:
    return UpdateEducation(SqlAlchemyEducationRepository(session))


async def get_delete_education(
    session: AsyncSession = Depends(get_db_session),
) -> DeleteEducation:
    return DeleteEducation(SqlAlchemyEducationRepository(session))


async def get_add_project(session: AsyncSession = Depends(get_db_session)) -> AddProject:
    return AddProject(SqlAlchemyProjectRepository(session))


async def get_update_project(session: AsyncSession = Depends(get_db_session)) -> UpdateProject:
    return UpdateProject(SqlAlchemyProjectRepository(session))


async def get_delete_project(session: AsyncSession = Depends(get_db_session)) -> DeleteProject:
    return DeleteProject(SqlAlchemyProjectRepository(session))


async def get_reorder_projects(
    session: AsyncSession = Depends(get_db_session),
) -> ReorderProjects:
    return ReorderProjects(SqlAlchemyProjectRepository(session))


async def get_set_resume_skills(
    session: AsyncSession = Depends(get_db_session),
) -> SetResumeSkills:
    return SetResumeSkills(SqlAlchemySkillRepository(session))
