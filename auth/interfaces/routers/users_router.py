from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from auth.interfaces.schemas import UserResponse
from core.database.session import get_db_session
from core.exceptions import NotFoundError

router = APIRouter(tags=["users"])


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_public_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    repo = SqlAlchemyUserRepository(db)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        roles=user.roles,
    )
