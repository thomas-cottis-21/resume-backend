from uuid import UUID

from fastapi import APIRouter, Depends, status

from bucket_list.application.commands.add_to_bucket_list import AddToBucketList, AddToBucketListInput
from bucket_list.application.commands.remove_from_bucket_list import RemoveFromBucketList
from bucket_list.application.commands.update_bucket_list_item import (
    UpdateBucketListItem,
    UpdateBucketListItemInput,
)
from bucket_list.application.queries.get_bucket_list_item import GetBucketListItem
from bucket_list.application.queries.list_bucket_list_items import ListBucketListItems
from bucket_list.interfaces.dependencies import (
    get_add_to_bucket_list,
    get_bucket_list_item_query,
    get_list_bucket_list_items,
    get_remove_from_bucket_list,
    get_update_bucket_list_item,
)
from bucket_list.interfaces.mappers import bucket_list_item_to_response
from bucket_list.interfaces.schemas import (
    BucketListItemCreateRequest,
    BucketListItemResponse,
    BucketListItemUpdateRequest,
)

router = APIRouter(tags=["bucket-list"])


@router.get("/users/{user_id}/bucket-list", response_model=list[BucketListItemResponse])
async def list_bucket_list_items(
    user_id: UUID,
    use_case: ListBucketListItems = Depends(get_list_bucket_list_items),
) -> list[BucketListItemResponse]:
    results = await use_case.execute(user_id)
    return [bucket_list_item_to_response(r) for r in results]


@router.post(
    "/users/{user_id}/bucket-list",
    response_model=BucketListItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_bucket_list(
    user_id: UUID,
    body: BucketListItemCreateRequest,
    use_case: AddToBucketList = Depends(get_add_to_bucket_list),
) -> BucketListItemResponse:
    result = await use_case.execute(
        AddToBucketListInput(
            user_id=user_id,
            destination_id=body.destination_id,
            status_id=body.status_id,
            notes=body.notes,
        )
    )
    return bucket_list_item_to_response(result)


@router.get("/users/{user_id}/bucket-list/{item_id}", response_model=BucketListItemResponse)
async def get_bucket_list_item(
    user_id: UUID,
    item_id: UUID,
    use_case: GetBucketListItem = Depends(get_bucket_list_item_query),
) -> BucketListItemResponse:
    result = await use_case.execute(item_id)
    return bucket_list_item_to_response(result)


@router.put("/users/{user_id}/bucket-list/{item_id}", response_model=BucketListItemResponse)
async def update_bucket_list_item(
    user_id: UUID,
    item_id: UUID,
    body: BucketListItemUpdateRequest,
    use_case: UpdateBucketListItem = Depends(get_update_bucket_list_item),
) -> BucketListItemResponse:
    result = await use_case.execute(
        UpdateBucketListItemInput(
            item_id=item_id,
            status_id=body.status_id,
            notes=body.notes,
        )
    )
    return bucket_list_item_to_response(result)


@router.delete(
    "/users/{user_id}/bucket-list/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_from_bucket_list(
    user_id: UUID,
    item_id: UUID,
    use_case: RemoveFromBucketList = Depends(get_remove_from_bucket_list),
) -> None:
    await use_case.execute(item_id)
