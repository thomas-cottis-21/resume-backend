from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from blog.application.commands.create_post import CreatePost
from blog.application.commands.delete_post import DeletePost
from blog.application.commands.publish_post import PublishPost
from blog.application.commands.update_post import UpdatePost
from blog.application.queries.get_post import GetPost
from blog.application.queries.list_post import ListPosts
from blog.infrastructure.repositories.post_repository import SqlAlchemyPostRepository
from blog.infrastructure.repositories.status_repository import SqlAlchemyStatusRepository
from blog.infrastructure.repositories.tag_repository import SqlAlchemyTagRepository
from core.database.session import get_db_session

# ── Query factories ────────────────────────────────────────────────────────────

async def get_list_posts(session: AsyncSession = Depends(get_db_session)) -> ListPosts:
    return ListPosts(SqlAlchemyPostRepository(session), SqlAlchemyStatusRepository(session))


async def get_get_post(session: AsyncSession = Depends(get_db_session)) -> GetPost:
    return GetPost(SqlAlchemyPostRepository(session))


# ── Command factories ──────────────────────────────────────────────────────────

async def get_create_post(session: AsyncSession = Depends(get_db_session)) -> CreatePost:
    return CreatePost(SqlAlchemyPostRepository(session), SqlAlchemyStatusRepository(session))


async def get_update_post(session: AsyncSession = Depends(get_db_session)) -> UpdatePost:
    return UpdatePost(SqlAlchemyPostRepository(session))


async def get_delete_post(session: AsyncSession = Depends(get_db_session)) -> DeletePost:
    return DeletePost(SqlAlchemyPostRepository(session))


async def get_publish_post(session: AsyncSession = Depends(get_db_session)) -> PublishPost:
    return PublishPost(SqlAlchemyPostRepository(session), SqlAlchemyStatusRepository(session))
