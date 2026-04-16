from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    BOOLEAN,
    DATE,
    DATETIME,
    SMALLINT,
    TEXT,
    VARCHAR,
    ForeignKey,
    SmallInteger,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ResumeModel(Base):
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(VARCHAR(36), nullable=False, index=True)
    tagline: Mapped[str | None] = mapped_column(VARCHAR(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    work_experiences: Mapped[list[WorkExperienceModel]] = relationship(
        back_populates="resume", lazy="noload", cascade="all, delete-orphan"
    )
    education_entries: Mapped[list[EducationModel]] = relationship(
        back_populates="resume", lazy="noload", cascade="all, delete-orphan"
    )
    projects: Mapped[list[ProjectModel]] = relationship(
        back_populates="resume", lazy="noload", cascade="all, delete-orphan"
    )


class WorkExperienceModel(Base):
    __tablename__ = "work_experience"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    resume_id: Mapped[str] = mapped_column(
        VARCHAR(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    company: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    role: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    location: Mapped[str | None] = mapped_column(VARCHAR(255), nullable=True)
    start_date: Mapped[date] = mapped_column(DATE, nullable=False)
    end_date: Mapped[date | None] = mapped_column(DATE, nullable=True)
    sort_order: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    resume: Mapped[ResumeModel] = relationship(back_populates="work_experiences", lazy="noload")
    bullets: Mapped[list[WorkExperienceBulletModel]] = relationship(
        back_populates="experience", lazy="noload", cascade="all, delete-orphan",
        order_by="WorkExperienceBulletModel.sort_order"
    )


class WorkExperienceBulletModel(Base):
    __tablename__ = "work_experience_bullets"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    experience_id: Mapped[str] = mapped_column(
        VARCHAR(36),
        ForeignKey("work_experience.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(TEXT, nullable=False)
    sort_order: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=0)

    experience: Mapped[WorkExperienceModel] = relationship(
        back_populates="bullets", lazy="noload"
    )


class EducationModel(Base):
    __tablename__ = "education"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    resume_id: Mapped[str] = mapped_column(
        VARCHAR(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    institution: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    degree: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    start_year: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    end_year: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    sort_order: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    resume: Mapped[ResumeModel] = relationship(back_populates="education_entries", lazy="noload")


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    resume_id: Mapped[str] = mapped_column(
        VARCHAR(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    github_url: Mapped[str | None] = mapped_column(VARCHAR(500), nullable=True)
    live_url: Mapped[str | None] = mapped_column(VARCHAR(500), nullable=True)
    sort_order: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    resume: Mapped[ResumeModel] = relationship(back_populates="projects", lazy="noload")
    project_technologies: Mapped[list[ProjectTechnologyModel]] = relationship(
        back_populates="project",
        lazy="noload",
        cascade="all, delete-orphan",
        order_by="ProjectTechnologyModel.sort_order",
    )


class TechnologyModel(Base):
    __tablename__ = "technologies"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)

    project_technologies: Mapped[list[ProjectTechnologyModel]] = relationship(
        back_populates="technology", lazy="noload"
    )


class ProjectTechnologyModel(Base):
    __tablename__ = "project_technologies"

    project_id: Mapped[str] = mapped_column(
        VARCHAR(36), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    technology_id: Mapped[str] = mapped_column(
        VARCHAR(36), ForeignKey("technologies.id", ondelete="CASCADE"), primary_key=True
    )
    sort_order: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=0)

    project: Mapped[ProjectModel] = relationship(back_populates="project_technologies", lazy="noload")
    technology: Mapped[TechnologyModel] = relationship(back_populates="project_technologies", lazy="noload")


class SkillCategoryModel(Base):
    __tablename__ = "skill_categories"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    sort_order: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=0)

    skills: Mapped[list[SkillModel]] = relationship(
        back_populates="category", lazy="noload", order_by="SkillModel.name"
    )


class SkillModel(Base):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    category_id: Mapped[str] = mapped_column(
        VARCHAR(36), ForeignKey("skill_categories.id", ondelete="RESTRICT"), nullable=False
    )

    category: Mapped[SkillCategoryModel] = relationship(back_populates="skills", lazy="noload")


class ResumeSkillModel(Base):
    __tablename__ = "resume_skills"

    resume_id: Mapped[str] = mapped_column(
        VARCHAR(36), ForeignKey("resumes.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id: Mapped[str] = mapped_column(
        VARCHAR(36), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True
    )
    sort_order: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=0)
