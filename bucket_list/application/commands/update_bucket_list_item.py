from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from bucket_list.application.dtos import BucketListItemOutput
from bucket_list.application.queries._helpers import item_to_output
from bucket_list.domain.exceptions import BucketListItemNotFound, BucketListStatusNotFound
from bucket_list.domain.repositories import BucketListItemRepository, StatusRepository


@dataclass
class UpdateBucketListItemInput:
    item_id: UUID
    status_id: UUID
    notes: str | None = None


class UpdateBucketListItem:
    def __init__(
        self,
        item_repo: BucketListItemRepository,
        status_repo: StatusRepository,
    ) -> None:
        self._item_repo = item_repo
        self._status_repo = status_repo

    async def execute(self, input: UpdateBucketListItemInput) -> BucketListItemOutput:
        item = await self._item_repo.get_by_id(input.item_id)
        if not item:
            raise BucketListItemNotFound(input.item_id)

        status = await self._status_repo.get_status_by_id(input.status_id)
        if not status:
            raise BucketListStatusNotFound(input.status_id)

        item.status_id = input.status_id
        item.notes = input.notes
        item.updated_at = datetime.now(tz=timezone.utc)

        await self._item_repo.save(item)
        loaded = await self._item_repo.get_by_id(item.id)
        return item_to_output(loaded)  # type: ignore[arg-type]
