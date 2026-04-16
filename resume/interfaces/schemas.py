from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ── Resume ────────────────────────────────────────────────────────────────────

class ResumeCreateRequest(BaseModel):
    tagline: str | None = None
    user_id: UUID


class ResumeUpdateRequest(BaseModel):
    tagline: str | None = None


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    tagline: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ── Work Experience ───────────────────────────────────────────────────────────

class BulletRequest(BaseModel):
    content: str
    sort_order: int = 0


class BulletResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    experience_id: UUID
    content: str
    sort_order: int


class WorkExperienceCreateRequest(BaseModel):
    company: str
    role: str
    start_date: date
    location: str | None = None
    end_date: date | None = None
    sort_order: int = 0
    bullets: list[BulletRequest] = []


class WorkExperienceUpdateRequest(BaseModel):
    company: str
    role: str
    start_date: date
    location: str | None = None
    end_date: date | None = None
    sort_order: int = 0
    bullets: list[BulletRequest] = []


class WorkExperienceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resume_id: UUID
    company: str
    role: str
    location: str | None
    start_date: date
    end_date: date | None
    sort_order: int
    created_at: datetime
    updated_at: datetime
    bullets: list[BulletResponse]


# ── Education ─────────────────────────────────────────────────────────────────

class EducationCreateRequest(BaseModel):
    institution: str
    degree: str
    start_year: int
    end_year: int | None = None
    sort_order: int = 0


class EducationUpdateRequest(BaseModel):
    institution: str
    degree: str
    start_year: int
    end_year: int | None = None
    sort_order: int = 0


class EducationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resume_id: UUID
    institution: str
    degree: str
    start_year: int
    end_year: int | None
    sort_order: int
    created_at: datetime


# ── Project ───────────────────────────────────────────────────────────────────

class TechnologyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class ProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    sort_order: int = 0
    technology_ids: list[UUID] = []


class ProjectUpdateRequest(BaseModel):
    name: str
    description: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    sort_order: int = 0
    technology_ids: list[UUID] = []


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resume_id: UUID
    name: str
    description: str | None
    github_url: str | None
    live_url: str | None
    sort_order: int
    created_at: datetime
    updated_at: datetime
    technologies: list[TechnologyResponse]


# ── Skills ────────────────────────────────────────────────────────────────────

class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    category_id: UUID


class SkillCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    sort_order: int
    skills: list[SkillResponse]


class ResumeSkillEntryResponse(BaseModel):
    skill_id: UUID
    sort_order: int
    skill: SkillResponse | None


class SkillEntryRequest(BaseModel):
    skill_id: UUID
    sort_order: int = 0


class SetResumeSkillsRequest(BaseModel):
    skills: list[SkillEntryRequest]


# ── Reorder ───────────────────────────────────────────────────────────────────

class ReorderItemRequest(BaseModel):
    id: UUID
    sort_order: int


class ReorderRequest(BaseModel):
    items: list[ReorderItemRequest]
