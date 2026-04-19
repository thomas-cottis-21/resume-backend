from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ── Tag ───────────────────────────────────────────────────────────────────────

class TagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    created_at: datetime


# ── Post ──────────────────────────────────────────────────────────────────────

class PostCreateRequest(BaseModel):
    title: str
    excerpt: str | None = None
    content: str
    cover_image_url: str | None = None
    reading_time_minutes: int | None = None
    tag_ids: list[UUID] = []


class PostUpdateRequest(BaseModel):
    title: str | None = None
    excerpt: str | None = None
    content: str | None = None
    cover_image_url: str | None = None
    reading_time_minutes: int | None = None
    tag_ids: list[UUID] | None = None


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    title: str
    excerpt: str | None
    content: str
    cover_image_url: str | None
    reading_time_minutes: int | None
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime
    author_id: UUID
    tags: list[TagResponse]


class PostSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    title: str
    excerpt: str | None
    cover_image_url: str | None
    reading_time_minutes: int | None
    published_at: datetime | None
    author_id: UUID
    tags: list[TagResponse]
