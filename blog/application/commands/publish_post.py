from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from blog.application.dtos import PostOutput
from blog.application.queries._helpers import post_to_output
from blog.domain.exceptions import PostNotFoundError, PostOwnershipError, StatusesNotFoundError
from blog.domain.repositories import PostRepository, StatusRepository


@dataclass
class PublishPostInput:
    post_id: UUID
    user_id: UUID


class PublishPost:
    def __init__(self, post_repo: PostRepository, status_repo: StatusRepository) -> None:
        self._post_repo = post_repo
        self._status_repo = status_repo

    async def execute(self, input: PublishPostInput) -> PostOutput:
        post = await self._post_repo.get_by_id(input.post_id)
        if post is None:
            raise PostNotFoundError(post_id=input.post_id)

        if post.author_id != input.user_id:
            raise PostOwnershipError()

        statuses = await self._status_repo.list_statuses()
        published_status = next((s for s in statuses if s.name == "PUBLISHED"), None)
        if not published_status:
            raise StatusesNotFoundError()

        post.status_id = published_status.id
        post.published_at = datetime.now(tz=timezone.utc)
        post.updated_at = post.published_at

        await self._post_repo.save(post)

        loaded = await self._post_repo.get_by_id(post.id)
        return post_to_output(loaded)  # type: ignore[arg-type]
