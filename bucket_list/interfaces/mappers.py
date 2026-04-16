from bucket_list.application.dtos import (
    BucketListItemOutput,
    BucketListStatusOutput,
    DestinationCategoryOutput,
    DestinationOutput,
    VisitOutput,
)
from bucket_list.interfaces.schemas import (
    BucketListItemResponse,
    BucketListStatusResponse,
    DestinationCategoryResponse,
    DestinationResponse,
    VisitResponse,
)


def destination_category_to_response(dto: DestinationCategoryOutput) -> DestinationCategoryResponse:
    return DestinationCategoryResponse(id=dto.id, name=dto.name, sort_order=dto.sort_order)


def bucket_list_status_to_response(dto: BucketListStatusOutput) -> BucketListStatusResponse:
    return BucketListStatusResponse(id=dto.id, name=dto.name)


def _destination_dto_to_response(dto: DestinationOutput) -> DestinationResponse:
    return DestinationResponse(
        id=dto.id,
        name=dto.name,
        country=dto.country,
        continent=dto.continent,
        description=dto.description,
        cover_image_url=dto.cover_image_url,
        category_id=dto.category_id,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        category=DestinationCategoryResponse(
            id=dto.category.id,
            name=dto.category.name,
            sort_order=dto.category.sort_order,
        ) if dto.category else None,
    )


def destination_to_response(dto: DestinationOutput) -> DestinationResponse:
    return _destination_dto_to_response(dto)


def bucket_list_item_to_response(dto: BucketListItemOutput) -> BucketListItemResponse:
    return BucketListItemResponse(
        id=dto.id,
        user_id=dto.user_id,
        destination_id=dto.destination_id,
        status_id=dto.status_id,
        notes=dto.notes,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        destination=_destination_dto_to_response(dto.destination) if dto.destination else None,
        status=BucketListStatusResponse(
            id=dto.status.id,
            name=dto.status.name,
        ) if dto.status else None,
    )


def visit_to_response(dto: VisitOutput) -> VisitResponse:
    return VisitResponse(
        id=dto.id,
        user_id=dto.user_id,
        destination_id=dto.destination_id,
        visited_at=dto.visited_at,
        notes=dto.notes,
        created_at=dto.created_at,
        destination=_destination_dto_to_response(dto.destination) if dto.destination else None,
    )
