from __future__ import annotations

from blog.application.dtos import PostSummaryOutput
from blog.application.queries._helpers import post_to_summary_output
from blog.domain.exceptions import StatusesNotFoundError
from blog.domain.repositories import PostRepository, StatusRepository


class ListPosts:
    def __init__(self, post_repo: PostRepository, status_repo: StatusRepository) -> None:
        self._post_repo = post_repo
        self._status_repo = status_repo

    async def execute(self) -> list[PostSummaryOutput]:
        statuses = await self._status_repo.list_statuses()
        published_status = next((s for s in statuses if s.name == "PUBLISHED"), None)
        if not published_status:
            raise StatusesNotFoundError()

        posts = await self._post_repo.list_all(status_id=published_status.id)
        return [post_to_summary_output(p) for p in posts]
