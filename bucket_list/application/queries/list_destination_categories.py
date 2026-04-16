from bucket_list.application.dtos import DestinationCategoryOutput
from bucket_list.domain.repositories import StatusRepository


class ListDestinationCategories:
    def __init__(self, repo: StatusRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[DestinationCategoryOutput]:
        categories = await self._repo.list_categories()
        return [
            DestinationCategoryOutput(id=c.id, name=c.name, sort_order=c.sort_order)
            for c in categories
        ]
