from blog.application.dtos import PostOutput, PostSummaryOutput, TagOutput
from blog.interfaces.schemas import PostResponse, PostSummaryResponse, TagResponse


def tag_to_response(dto: TagOutput) -> TagResponse:
    return TagResponse(id=dto.id, name=dto.name, slug=dto.slug, created_at=dto.created_at)


def post_to_response(dto: PostOutput) -> PostResponse:
    return PostResponse(
        id=dto.id,
        slug=dto.slug,
        title=dto.title,
        excerpt=dto.excerpt,
        content=dto.content,
        cover_image_url=dto.cover_image_url,
        reading_time_minutes=dto.reading_time_minutes,
        published_at=dto.published_at,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        author_id=dto.author_id,
        tags=[tag_to_response(t) for t in dto.tags],
    )


def post_summary_to_response(dto: PostSummaryOutput) -> PostSummaryResponse:
    return PostSummaryResponse(
        id=dto.id,
        slug=dto.slug,
        title=dto.title,
        excerpt=dto.excerpt,
        cover_image_url=dto.cover_image_url,
        reading_time_minutes=dto.reading_time_minutes,
        published_at=dto.published_at,
        author_id=dto.author_id,
        tags=[tag_to_response(t) for t in dto.tags],
    )
