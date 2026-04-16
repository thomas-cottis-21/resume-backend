from fastapi import APIRouter

from resume.interfaces.routers.education import router as education_router
from resume.interfaces.routers.projects import router as projects_router
from resume.interfaces.routers.resumes import router as resumes_router
from resume.interfaces.routers.skills import router as skills_router
from resume.interfaces.routers.work_experience import router as work_experience_router

resume_router = APIRouter()

resume_router.include_router(resumes_router)
resume_router.include_router(work_experience_router)
resume_router.include_router(education_router)
resume_router.include_router(projects_router)
resume_router.include_router(skills_router)
