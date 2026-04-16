from bucket_list.application.dtos import BucketListStatusOutput
from bucket_list.domain.repositories import StatusRepository


class ListBucketListStatuses:
    def __init__(self, repo: StatusRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[BucketListStatusOutput]:
        statuses = await self._repo.list_statuses()
        return [BucketListStatusOutput(id=s.id, name=s.name) for s in statuses]
