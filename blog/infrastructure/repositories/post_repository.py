from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from blog.domain.entities import Post, Tag
from blog.domain.repositories import PostRepository
from blog.infrastructure.models import PostModel, PostTagModel, TagModel


class SqlAlchemyPostRepository(PostRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, post_id: UUID) -> Post | None:
        result = await self._session.execute(
            select(PostModel)
            .options(selectinload(PostModel.post_tags).selectinload(PostTagModel.tag))
            .where(PostModel.id == post_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_slug(self, slug: str) -> Post | None:
        result = await self._session.execute(
            select(PostModel)
            .options(selectinload(PostModel.post_tags).selectinload(PostTagModel.tag))
            .where(PostModel.slug == slug)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_all(
        self,
        status_id: UUID | None = None,
        author_id: UUID | None = None,
    ) -> list[Post]:
        query = select(PostModel).options(
            selectinload(PostModel.post_tags).selectinload(PostTagModel.tag)
        )
        if status_id is not None:
            query = query.where(PostModel.status_id == status_id)
        if author_id is not None:
            query = query.where(PostModel.author_id == author_id)
        query = query.order_by(PostModel.published_at.desc())
        result = await self._session.execute(query)
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, post: Post) -> None:
        existing = await self._session.get(PostModel, post.id)
        if existing:
            existing.slug = post.slug
            existing.title = post.title
            existing.excerpt = post.excerpt
            existing.content = post.content
            existing.cover_image_url = post.cover_image_url
            existing.reading_time_minutes = post.reading_time_minutes
            existing.status_id = post.status_id
            existing.published_at = post.published_at
            existing.updated_at = post.updated_at
        else:
            self._session.add(
                PostModel(
                    id=post.id,
                    slug=post.slug,
                    title=post.title,
                    excerpt=post.excerpt,
                    content=post.content,
                    cover_image_url=post.cover_image_url,
                    reading_time_minutes=post.reading_time_minutes,
                    status_id=post.status_id,
                    author_id=post.author_id,
                    published_at=post.published_at,
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )
            )
        await self._session.flush()

    async def set_tags(self, post_id: UUID, tag_ids: list[UUID]) -> None:
        await self._session.execute(
            delete(PostTagModel).where(PostTagModel.post_id == post_id)
        )
        for tag_id in tag_ids:
            self._session.add(PostTagModel(post_id=post_id, tag_id=tag_id))
        await self._session.flush()

    async def delete(self, post_id: UUID) -> None:
        await self._session.execute(
            delete(PostModel).where(PostModel.id == post_id)
        )
        await self._session.flush()


def _to_entity(m: PostModel) -> Post:
    tags = [
        Tag(id=pt.tag.id, name=pt.tag.name, slug=pt.tag.slug, created_at=pt.tag.created_at)
        for pt in m.post_tags
    ]
    return Post(
        id=m.id,
        slug=m.slug,
        title=m.title,
        excerpt=m.excerpt,
        content=m.content,
        cover_image_url=m.cover_image_url,
        reading_time_minutes=m.reading_time_minutes,
        status_id=m.status_id,
        author_id=m.author_id,
        published_at=m.published_at,
        created_at=m.created_at,
        updated_at=m.updated_at,
        tags=tags,
    )
