"""Shared entity → DTO conversion helpers for the bucket_list application layer."""
from __future__ import annotations

from bucket_list.application.dtos import (
    BucketListItemOutput,
    BucketListStatusOutput,
    DestinationCategoryOutput,
    DestinationOutput,
    VisitOutput,
)
from bucket_list.domain.entities import BucketListItem, Destination, Visit


def destination_to_output(d: Destination) -> DestinationOutput:
    return DestinationOutput(
        id=d.id,
        name=d.name,
        country=d.country,
        continent=d.continent,
        description=d.description,
        cover_image_url=d.cover_image_url,
        category_id=d.category_id,
        created_at=d.created_at,
        updated_at=d.updated_at,
        category=DestinationCategoryOutput(
            id=d.category.id,
            name=d.category.name,
            sort_order=d.category.sort_order,
        ) if d.category else None,
    )


def item_to_output(item: BucketListItem) -> BucketListItemOutput:
    return BucketListItemOutput(
        id=item.id,
        user_id=item.user_id,
        destination_id=item.destination_id,
        status_id=item.status_id,
        notes=item.notes,
        created_at=item.created_at,
        updated_at=item.updated_at,
        destination=destination_to_output(item.destination) if item.destination else None,
        status=BucketListStatusOutput(
            id=item.status.id,
            name=item.status.name,
        ) if item.status else None,
    )


def visit_to_output(visit: Visit) -> VisitOutput:
    return VisitOutput(
        id=visit.id,
        user_id=visit.user_id,
        destination_id=visit.destination_id,
        visited_at=visit.visited_at,
        notes=visit.notes,
        created_at=visit.created_at,
        destination=destination_to_output(visit.destination) if visit.destination else None,
    )
