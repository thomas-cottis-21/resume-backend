from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from bucket_list.application.dtos import BucketListItemOutput
from bucket_list.application.queries._helpers import item_to_output
from bucket_list.domain.entities import BucketListItem
from bucket_list.domain.exceptions import (
    AlreadyInBucketList,
    BucketListStatusNotFound,
    DestinationNotFound,
)
from bucket_list.domain.repositories import (
    BucketListItemRepository,
    DestinationRepository,
    StatusRepository,
)


@dataclass
class AddToBucketListInput:
    user_id: UUID
    destination_id: UUID
    status_id: UUID
    notes: str | None = None


class AddToBucketList:
    def __init__(
        self,
        item_repo: BucketListItemRepository,
        destination_repo: DestinationRepository,
        status_repo: StatusRepository,
    ) -> None:
        self._item_repo = item_repo
        self._destination_repo = destination_repo
        self._status_repo = status_repo

    async def execute(self, input: AddToBucketListInput) -> BucketListItemOutput:
        destination = await self._destination_repo.get_by_id(input.destination_id)
        if not destination:
            raise DestinationNotFound(input.destination_id)

        status = await self._status_repo.get_status_by_id(input.status_id)
        if not status:
            raise BucketListStatusNotFound(input.status_id)

        existing = await self._item_repo.get_by_user_and_destination(
            input.user_id, input.destination_id
        )
        if existing:
            raise AlreadyInBucketList(input.destination_id)

        now = datetime.now(tz=timezone.utc)
        item = BucketListItem(
            id=uuid4(),
            user_id=input.user_id,
            destination_id=input.destination_id,
            status_id=input.status_id,
            notes=input.notes,
            created_at=now,
            updated_at=now,
        )
        await self._item_repo.save(item)
        loaded = await self._item_repo.get_by_id(item.id)
        return item_to_output(loaded)  # type: ignore[arg-type]
