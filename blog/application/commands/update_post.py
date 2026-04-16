from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from blog.application.dtos import PostOutput
from blog.application.queries._helpers import post_to_output
from blog.application.commands._helpers import slugify
from blog.domain.exceptions import DuplicatePostError, PostNotFoundError, PostOwnershipError
from blog.domain.repositories import PostRepository

# Sentinel — distinguishes "leave unchanged" from "set to None"
_UNSET = object()
UNSET: Any = _UNSET


@dataclass
class UpdatePostInput:
    post_id: UUID
    user_id: UUID
    title: str | object = UNSET
    excerpt: str | None | object = UNSET
    content: str | object = UNSET
    cover_image_url: str | None | object = UNSET
    reading_time_minutes: int | None | object = UNSET
    tags: list[UUID] | object = field(default=UNSET)


class UpdatePost:
    def __init__(self, post_repo: PostRepository) -> None:
        self._post_repo = post_repo

    async def execute(self, input: UpdatePostInput) -> PostOutput:
        post = await self._post_repo.get_by_id(input.post_id)
        if post is None:
            raise PostNotFoundError(post_id=input.post_id)

        if post.author_id != input.user_id:
            raise PostOwnershipError()

        if input.title is not UNSET:
            new_slug = slugify(input.title)  # type: ignore[arg-type]
            if new_slug != post.slug and await self._post_repo.get_by_slug(new_slug):
                raise DuplicatePostError()
            post.title = input.title  # type: ignore[assignment]
            post.slug = new_slug

        if input.excerpt is not UNSET:
            post.excerpt = input.excerpt  # type: ignore[assignment]

        if input.content is not UNSET:
            post.content = input.content  # type: ignore[assignment]

        if input.cover_image_url is not UNSET:
            post.cover_image_url = input.cover_image_url  # type: ignore[assignment]

        if input.reading_time_minutes is not UNSET:
            post.reading_time_minutes = input.reading_time_minutes  # type: ignore[assignment]

        post.updated_at = datetime.now(tz=timezone.utc)

        await self._post_repo.save(post)

        if input.tags is not UNSET:
            await self._post_repo.set_tags(post.id, input.tags)  # type: ignore[arg-type]

        loaded = await self._post_repo.get_by_id(post.id)
        return post_to_output(loaded)  # type: ignore[arg-type]
