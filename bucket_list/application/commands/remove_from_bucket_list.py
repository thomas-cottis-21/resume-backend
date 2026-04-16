from uuid import UUID

from bucket_list.domain.exceptions import BucketListItemNotFound
from bucket_list.domain.repositories import BucketListItemRepository


class RemoveFromBucketList:
    def __init__(self, repo: BucketListItemRepository) -> None:
        self._repo = repo

    async def execute(self, item_id: UUID) -> None:
        item = await self._repo.get_by_id(item_id)
        if not item:
            raise BucketListItemNotFound(item_id)
        await self._repo.delete(item_id)
