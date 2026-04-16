from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from blog.application.dtos import PostOutput
from blog.application.queries._helpers import post_to_output
from blog.domain.exceptions import PostIdentifierError, PostNotFoundError
from blog.domain.repositories import PostRepository


@dataclass
class GetPostInput:
    post_id: UUID | None
    post_slug: str | None


class GetPost:
    def __init__(self, post_repo: PostRepository):
        self._post_repo = post_repo

    async def execute(self, input: GetPostInput) -> PostOutput:
        if input.post_id is not None:
            post = await self._post_repo.get_by_id(input.post_id)

            if post is None:
                raise PostNotFoundError(post_id=input.post_id)

            return post_to_output(post)

        if input.post_slug is not None:
            post = await self._post_repo.get_by_slug(input.post_slug)

            if post is None:
                raise PostNotFoundError(post_id=input.post_slug)

            return post_to_output(post)

        raise PostIdentifierError()
