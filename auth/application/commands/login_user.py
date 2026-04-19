from __future__ import annotations

from dataclasses import dataclass

from auth.application.commands.register_user import TokenPair, _issue_token_pair
from auth.domain.repositories import RefreshTokenRepository, UserRepository
from auth.infrastructure.security import verify_password
from core.config import Settings
from core.exceptions import AuthenticationError


@dataclass
class LoginUserInput:
    email: str
    password: str


class LoginUser:
    def __init__(
        self,
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository,
        settings: Settings,
    ) -> None:
        self._user_repo = user_repo
        self._refresh_token_repo = refresh_token_repo
        self._settings = settings

    async def execute(self, input: LoginUserInput) -> TokenPair:
        user = await self._user_repo.get_by_email(input.email)
        if not user or not user.password_hash:
            raise AuthenticationError("Invalid credentials")

        if not verify_password(input.password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        return await _issue_token_pair(user, self._refresh_token_repo, self._settings)
