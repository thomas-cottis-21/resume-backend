from uuid import UUID

from fastapi import APIRouter, Depends, status

from auth.domain.entities import User
from auth.interfaces.dependencies import get_current_user
from blog.application.commands.create_post import CreatePost, CreatePostInput
from blog.application.commands.delete_post import DeletePost, DeletePostInput
from blog.application.commands.publish_post import PublishPost, PublishPostInput
from blog.application.commands.update_post import UpdatePost, UpdatePostInput, UNSET
from blog.application.queries.get_post import GetPost, GetPostInput
from blog.application.queries.list_post import ListPosts
from blog.interfaces.dependencies import (
    get_create_post,
    get_delete_post,
    get_get_post,
    get_list_posts,
    get_publish_post,
    get_tag_repository,
    get_update_post,
)
from blog.infrastructure.repositories.tag_repository import SqlAlchemyTagRepository
from blog.interfaces.mappers import post_summary_to_response, post_to_response, tag_to_response
from blog.interfaces.schemas import (
    PostCreateRequest,
    PostResponse,
    PostSummaryResponse,
    PostUpdateRequest,
    TagResponse,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/tags", response_model=list[TagResponse])
async def list_tags(
    repo: SqlAlchemyTagRepository = Depends(get_tag_repository),
) -> list[TagResponse]:
    tags = await repo.list_all()
    return [TagResponse(id=t.id, name=t.name, slug=t.slug, created_at=t.created_at) for t in tags]


@router.get("", response_model=list[PostSummaryResponse])
async def list_posts(
    use_case: ListPosts = Depends(get_list_posts),
) -> list[PostSummaryResponse]:
    results = await use_case.execute()
    return [post_summary_to_response(p) for p in results]


@router.get("/by-slug/{slug}", response_model=PostResponse)
async def get_post_by_slug(
    slug: str,
    use_case: GetPost = Depends(get_get_post),
) -> PostResponse:
    result = await use_case.execute(GetPostInput(post_id=None, post_slug=slug))
    return post_to_response(result)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: UUID,
    use_case: GetPost = Depends(get_get_post),
) -> PostResponse:
    result = await use_case.execute(GetPostInput(post_id=post_id, post_slug=None))
    return post_to_response(result)


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    body: PostCreateRequest,
    current_user: User = Depends(get_current_user),
    use_case: CreatePost = Depends(get_create_post),
) -> PostResponse:
    result = await use_case.execute(
        CreatePostInput(
            title=body.title,
            excerpt=body.excerpt,
            content=body.content,
            cover_image_url=body.cover_image_url,
            reading_time_minutes=body.reading_time_minutes,
            author_id=current_user.id,
            tags=body.tag_ids,
        )
    )
    return post_to_response(result)


@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: UUID,
    body: PostUpdateRequest,
    current_user: User = Depends(get_current_user),
    use_case: UpdatePost = Depends(get_update_post),
) -> PostResponse:
    result = await use_case.execute(
        UpdatePostInput(
            post_id=post_id,
            user_id=current_user.id,
            title=body.title if body.title is not None else UNSET,
            excerpt=body.excerpt if "excerpt" in body.model_fields_set else UNSET,
            content=body.content if body.content is not None else UNSET,
            cover_image_url=body.cover_image_url if "cover_image_url" in body.model_fields_set else UNSET,
            reading_time_minutes=body.reading_time_minutes if "reading_time_minutes" in body.model_fields_set else UNSET,
            tags=body.tag_ids if body.tag_ids is not None else UNSET,
        )
    )
    return post_to_response(result)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: DeletePost = Depends(get_delete_post),
) -> None:
    await use_case.execute(DeletePostInput(post_id=post_id, user_id=current_user.id))


@router.post("/{post_id}/publish", response_model=PostResponse)
async def publish_post(
    post_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: PublishPost = Depends(get_publish_post),
) -> PostResponse:
    result = await use_case.execute(PublishPostInput(post_id=post_id, user_id=current_user.id))
    return post_to_response(result)
