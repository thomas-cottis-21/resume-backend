from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.entities import User
from auth.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from auth.infrastructure.security import decode_access_token
from core.config import settings
from core.database.session import get_db_session
from core.exceptions import AuthenticationError

_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    if credentials is None:
        raise AuthenticationError("Missing authorization header")

    payload = decode_access_token(credentials.credentials, settings)
    try:
        user_id = UUID(payload["sub"])
    except (KeyError, ValueError):
        raise AuthenticationError("Invalid token payload")

    repo = SqlAlchemyUserRepository(db)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise AuthenticationError("User not found")

    return user
