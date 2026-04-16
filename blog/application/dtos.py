from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class TagOutput:
    id: UUID
    name: str
    slug: str
    created_at: datetime


@dataclass
class PostOutput:
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
    author_id: UUID # to be added later when the user module is built
    tags: list[TagOutput] = field(default_factory=list)


@dataclass
class PostSummaryOutput:
    id: UUID
    slug: str
    title: str
    excerpt: str | None
    cover_image_url: str | None
    reading_time_minutes: int | None
    published_at: datetime | None
    author_id: UUID
    tags: list[TagOutput] = field(default_factory=list)


@dataclass
class PostStatusOutput:
    id: UUID
    name: str
