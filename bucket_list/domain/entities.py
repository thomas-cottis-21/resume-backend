from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID


@dataclass
class DestinationCategory:
    id: UUID
    name: str
    sort_order: int


@dataclass
class BucketListStatus:
    id: UUID
    name: str


@dataclass
class Destination:
    id: UUID
    name: str
    country: str
    continent: str
    description: str | None
    cover_image_url: str | None
    category_id: UUID | None
    created_at: datetime
    updated_at: datetime
    category: DestinationCategory | None = field(default=None, compare=False)


@dataclass
class BucketListItem:
    id: UUID
    user_id: UUID
    destination_id: UUID
    status_id: UUID
    notes: str | None
    created_at: datetime
    updated_at: datetime
    destination: Destination | None = field(default=None, compare=False)
    status: BucketListStatus | None = field(default=None, compare=False)


@dataclass
class Visit:
    id: UUID
    user_id: UUID
    destination_id: UUID
    visited_at: date
    notes: str | None
    created_at: datetime
    destination: Destination | None = field(default=None, compare=False)
