from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from bucket_list.application.commands.create_destination import CreateDestination, CreateDestinationInput
from bucket_list.application.commands.delete_destination import DeleteDestination
from bucket_list.application.commands.update_destination import UpdateDestination, UpdateDestinationInput
from bucket_list.application.queries.get_destination import GetDestination
from bucket_list.application.queries.list_bucket_list_statuses import ListBucketListStatuses
from bucket_list.application.queries.list_destination_categories import ListDestinationCategories
from bucket_list.application.queries.list_destinations import ListDestinations
from bucket_list.interfaces.dependencies import (
    get_create_destination,
    get_delete_destination,
    get_destination_query,
    get_list_bucket_list_statuses,
    get_list_destination_categories,
    get_list_destinations,
    get_update_destination,
)
from bucket_list.interfaces.mappers import (
    bucket_list_status_to_response,
    destination_category_to_response,
    destination_to_response,
)
from bucket_list.interfaces.schemas import (
    BucketListStatusResponse,
    DestinationCategoryResponse,
    DestinationCreateRequest,
    DestinationResponse,
    DestinationUpdateRequest,
)
from core.exceptions import NotFoundError

router = APIRouter(tags=["bucket-list"])


@router.get("/destination-categories", response_model=list[DestinationCategoryResponse])
async def list_destination_categories(
    use_case: ListDestinationCategories = Depends(get_list_destination_categories),
) -> list[DestinationCategoryResponse]:
    results = await use_case.execute()
    return [destination_category_to_response(r) for r in results]


@router.get("/bucket-list-statuses", response_model=list[BucketListStatusResponse])
async def list_bucket_list_statuses(
    use_case: ListBucketListStatuses = Depends(get_list_bucket_list_statuses),
) -> list[BucketListStatusResponse]:
    results = await use_case.execute()
    return [bucket_list_status_to_response(r) for r in results]


@router.get("/destinations", response_model=list[DestinationResponse])
async def list_destinations(
    category_id: UUID | None = None,
    country: str | None = None,
    continent: str | None = None,
    use_case: ListDestinations = Depends(get_list_destinations),
) -> list[DestinationResponse]:
    results = await use_case.execute(
        category_id=category_id,
        country=country,
        continent=continent,
    )
    return [destination_to_response(r) for r in results]


@router.get("/destinations/{destination_id}", response_model=DestinationResponse)
async def get_destination(
    destination_id: UUID,
    use_case: GetDestination = Depends(get_destination_query),
) -> DestinationResponse:
    try:
        result = await use_case.execute(destination_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return destination_to_response(result)


@router.post("/destinations", response_model=DestinationResponse, status_code=status.HTTP_201_CREATED)
async def create_destination(
    body: DestinationCreateRequest,
    use_case: CreateDestination = Depends(get_create_destination),
) -> DestinationResponse:
    result = await use_case.execute(
        CreateDestinationInput(
            name=body.name,
            country=body.country,
            continent=body.continent,
            description=body.description,
            cover_image_url=body.cover_image_url,
            category_id=body.category_id,
        )
    )
    return destination_to_response(result)


@router.put("/destinations/{destination_id}", response_model=DestinationResponse)
async def update_destination(
    destination_id: UUID,
    body: DestinationUpdateRequest,
    use_case: UpdateDestination = Depends(get_update_destination),
) -> DestinationResponse:
    try:
        result = await use_case.execute(
            UpdateDestinationInput(
                destination_id=destination_id,
                name=body.name,
                country=body.country,
                continent=body.continent,
                description=body.description,
                cover_image_url=body.cover_image_url,
                category_id=body.category_id,
            )
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return destination_to_response(result)


@router.delete("/destinations/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_destination(
    destination_id: UUID,
    use_case: DeleteDestination = Depends(get_delete_destination),
) -> None:
    try:
        await use_case.execute(destination_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
