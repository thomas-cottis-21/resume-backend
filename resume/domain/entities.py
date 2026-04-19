from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID


@dataclass
class Resume:
    """Aggregate root for the Resume bounded context."""

    id: UUID
    user_id: UUID
    tagline: str | None
    title: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class ResumeLink:
    id: UUID
    resume_id: UUID
    label: str
    url: str
    sort_order: int


@dataclass
class WorkExperience:
    id: UUID
    resume_id: UUID
    company: str
    role: str
    location: str | None
    start_date: date
    end_date: date | None  # None = current position
    sort_order: int
    created_at: datetime
    updated_at: datetime
    bullets: list[WorkExperienceBullet] = field(default_factory=list)


@dataclass
class WorkExperienceBullet:
    id: UUID
    experience_id: UUID
    content: str
    sort_order: int


@dataclass
class Education:
    id: UUID
    resume_id: UUID
    institution: str
    degree: str
    start_year: int
    end_year: int | None  # None = still studying
    sort_order: int
    created_at: datetime


@dataclass
class Project:
    id: UUID
    resume_id: UUID
    name: str
    description: str | None
    github_url: str | None
    live_url: str | None
    sort_order: int
    created_at: datetime
    updated_at: datetime
    technologies: list[Technology] = field(default_factory=list)


@dataclass
class SkillCategory:
    id: UUID
    name: str
    sort_order: int
    skills: list[Skill] = field(default_factory=list)


@dataclass
class Skill:
    id: UUID
    name: str
    category_id: UUID


@dataclass
class Technology:
    id: UUID
    name: str


@dataclass
class ResumeSkillEntry:
    """Represents a skill assigned to a resume with a display order."""

    skill_id: UUID
    sort_order: int
    skill: Skill | None = None
