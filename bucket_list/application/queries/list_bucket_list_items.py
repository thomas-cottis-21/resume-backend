from uuid import UUID

from bucket_list.application.dtos import BucketListItemOutput
from bucket_list.application.queries._helpers import item_to_output
from bucket_list.domain.repositories import BucketListItemRepository


class ListBucketListItems:
    def __init__(self, repo: BucketListItemRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: UUID) -> list[BucketListItemOutput]:
        items = await self._repo.list_by_user(user_id)
        return [item_to_output(item) for item in items]
