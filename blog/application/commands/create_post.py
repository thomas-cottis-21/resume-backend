from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from blog.application.commands._helpers import slugify
from blog.application.dtos import PostOutput
from blog.application.queries._helpers import post_to_output
from blog.domain.entities import Post
from blog.domain.exceptions import DuplicatePostError, StatusesNotFoundError
from blog.domain.repositories import PostRepository, StatusRepository


@dataclass
class CreatePostInput:
    title: str  # slug is generated from the title
    excerpt: str | None
    content: str
    cover_image_url: str | None
    reading_time_minutes: int | None
    author_id: UUID
    tags: list[UUID] = field(default_factory=list)  # tag IDs; status defaults to DRAFT


class CreatePost:
    def __init__(self, post_repo: PostRepository, status_repo: StatusRepository) -> None:
        self._post_repo = post_repo
        self._status_repo = status_repo

    async def execute(self, input: CreatePostInput) -> PostOutput:
        statuses = await self._status_repo.list_statuses()
        draft_status = next((s for s in statuses if s.name == "DRAFT"), None)
        if not draft_status:
            raise StatusesNotFoundError()

        slug = slugify(input.title)
        if await self._post_repo.get_by_slug(slug):
            raise DuplicatePostError()

        now = datetime.now(tz=timezone.utc)
        post = Post(
            id=uuid4(),
            slug=slug,
            title=input.title,
            excerpt=input.excerpt,
            content=input.content,
            cover_image_url=input.cover_image_url,
            reading_time_minutes=input.reading_time_minutes,
            status_id=draft_status.id,
            author_id=input.author_id,
            published_at=None,
            created_at=now,
            updated_at=now,
        )
        await self._post_repo.save(post)
        await self._post_repo.set_tags(post.id, input.tags) # save the post, then associate the tags

        loaded = await self._post_repo.get_by_id(post.id)
        return post_to_output(loaded)  # type: ignore[arg-type]
