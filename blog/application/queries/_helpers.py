"""Shared entity → DTO conversion helpers for the blog application layer."""
from __future__ import annotations

from blog.application.dtos import PostOutput, PostSummaryOutput, TagOutput
from blog.domain.entities import Post


def _tags_to_output(post: Post) -> list[TagOutput]:
    return [TagOutput(id=t.id, name=t.name, slug=t.slug, created_at=t.created_at) for t in post.tags]


def post_to_summary_output(post: Post) -> PostSummaryOutput:
    return PostSummaryOutput(
        id=post.id,
        slug=post.slug,
        title=post.title,
        excerpt=post.excerpt,
        cover_image_url=post.cover_image_url,
        reading_time_minutes=post.reading_time_minutes,
        published_at=post.published_at,
        author_id=post.author_id,
        tags=_tags_to_output(post),
    )


def post_to_output(post: Post) -> PostOutput:
    return PostOutput(
        id=post.id,
        slug=post.slug,
        title=post.title,
        excerpt=post.excerpt,
        content=post.content,
        cover_image_url=post.cover_image_url,
        reading_time_minutes=post.reading_time_minutes,
        published_at=post.published_at,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author_id=post.author_id,
        tags=_tags_to_output(post),
    )
