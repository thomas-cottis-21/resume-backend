from uuid import UUID

from bucket_list.application.dtos import BucketListItemOutput
from bucket_list.application.queries._helpers import item_to_output
from bucket_list.domain.exceptions import BucketListItemNotFound
from bucket_list.domain.repositories import BucketListItemRepository


class GetBucketListItem:
    def __init__(self, repo: BucketListItemRepository) -> None:
        self._repo = repo

    async def execute(self, item_id: UUID) -> BucketListItemOutput:
        item = await self._repo.get_by_id(item_id)
        if not item:
            raise BucketListItemNotFound(item_id)
        return item_to_output(item)
