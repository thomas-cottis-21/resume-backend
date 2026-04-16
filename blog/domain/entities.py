from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class Post:
    id: UUID
    slug: str
    title: str
    excerpt: str | None
    content: str
    cover_image_url: str | None
    reading_time_minutes: int | None
    status_id: UUID
    author_id: UUID
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime
    tags: list[Tag] = field(default_factory=list, compare=False)


@dataclass
class Tag:
    id: UUID
    name: str
    slug: str
    created_at: datetime


@dataclass
class PostStatus:
    id: UUID
    name: str
