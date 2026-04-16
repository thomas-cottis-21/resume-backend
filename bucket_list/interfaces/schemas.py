from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ── Destination Category ───────────────────────────────────────────────────────

class DestinationCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    sort_order: int


# ── Bucket List Status ─────────────────────────────────────────────────────────

class BucketListStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


# ── Destination ────────────────────────────────────────────────────────────────

class DestinationCreateRequest(BaseModel):
    name: str
    country: str
    continent: str
    description: str | None = None
    cover_image_url: str | None = None
    category_id: UUID | None = None


class DestinationUpdateRequest(BaseModel):
    name: str
    country: str
    continent: str
    description: str | None = None
    cover_image_url: str | None = None
    category_id: UUID | None = None


class DestinationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    country: str
    continent: str
    description: str | None
    cover_image_url: str | None
    category_id: UUID | None
    created_at: datetime
    updated_at: datetime
    category: DestinationCategoryResponse | None


# ── Bucket List Item ───────────────────────────────────────────────────────────

class BucketListItemCreateRequest(BaseModel):
    destination_id: UUID
    status_id: UUID
    notes: str | None = None


class BucketListItemUpdateRequest(BaseModel):
    status_id: UUID
    notes: str | None = None


class BucketListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    destination_id: UUID
    status_id: UUID
    notes: str | None
    created_at: datetime
    updated_at: datetime
    destination: DestinationResponse | None
    status: BucketListStatusResponse | None


# ── Visit ──────────────────────────────────────────────────────────────────────

class VisitCreateRequest(BaseModel):
    destination_id: UUID
    visited_at: date
    notes: str | None = None


class VisitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    destination_id: UUID
    visited_at: date
    notes: str | None
    created_at: datetime
    destination: DestinationResponse | None
