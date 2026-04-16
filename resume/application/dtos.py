from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID


# ── Resume ────────────────────────────────────────────────────────────────────

@dataclass
class ResumeOutput:
    id: UUID
    user_id: UUID
    tagline: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ── Work Experience ───────────────────────────────────────────────────────────

@dataclass
class BulletOutput:
    id: UUID
    experience_id: UUID
    content: str
    sort_order: int


@dataclass
class WorkExperienceOutput:
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
    bullets: list[BulletOutput] = field(default_factory=list)


# ── Education ─────────────────────────────────────────────────────────────────

@dataclass
class EducationOutput:
    id: UUID
    resume_id: UUID
    institution: str
    degree: str
    start_year: int
    end_year: int | None
    sort_order: int
    created_at: datetime


# ── Project ───────────────────────────────────────────────────────────────────

@dataclass
class TechnologyOutput:
    id: UUID
    name: str


@dataclass
class ProjectOutput:
    id: UUID
    resume_id: UUID
    name: str
    description: str | None
    github_url: str | None
    live_url: str | None
    sort_order: int
    created_at: datetime
    updated_at: datetime
    technologies: list[TechnologyOutput] = field(default_factory=list)


# ── Skills ────────────────────────────────────────────────────────────────────

@dataclass
class SkillOutput:
    id: UUID
    name: str
    category_id: UUID


@dataclass
class SkillCategoryOutput:
    id: UUID
    name: str
    sort_order: int
    skills: list[SkillOutput] = field(default_factory=list)


@dataclass
class ResumeSkillEntryOutput:
    skill_id: UUID
    sort_order: int
    skill: SkillOutput | None = None


# ── Reorder ───────────────────────────────────────────────────────────────────

@dataclass
class ReorderItem:
    id: UUID
    sort_order: int
