from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID


@dataclass
class DestinationCategoryOutput:
    id: UUID
    name: str
    sort_order: int


@dataclass
class BucketListStatusOutput:
    id: UUID
    name: str


@dataclass
class DestinationOutput:
    id: UUID
    name: str
    country: str
    continent: str
    description: str | None
    cover_image_url: str | None
    category_id: UUID | None
    created_at: datetime
    updated_at: datetime
    category: DestinationCategoryOutput | None = field(default=None)


@dataclass
class BucketListItemOutput:
    id: UUID
    user_id: UUID
    destination_id: UUID
    status_id: UUID
    notes: str | None
    created_at: datetime
    updated_at: datetime
    destination: DestinationOutput | None = field(default=None)
    status: BucketListStatusOutput | None = field(default=None)


@dataclass
class VisitOutput:
    id: UUID
    user_id: UUID
    destination_id: UUID
    visited_at: date
    notes: str | None
    created_at: datetime
    destination: DestinationOutput | None = field(default=None)
