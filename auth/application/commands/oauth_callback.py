from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from auth.application.commands.register_user import TokenPair, _issue_token_pair
from auth.domain.entities import OAuthAccount, User
from auth.domain.repositories import OAuthAccountRepository, RefreshTokenRepository, UserRepository
from core.config import Settings


@dataclass
class OAuthCallbackInput:
    provider: str
    provider_user_id: str
    provider_email: str | None
    display_name: str


class OAuthCallback:
    def __init__(
        self,
        user_repo: UserRepository,
        oauth_account_repo: OAuthAccountRepository,
        refresh_token_repo: RefreshTokenRepository,
        settings: Settings,
    ) -> None:
        self._user_repo = user_repo
        self._oauth_account_repo = oauth_account_repo
        self._refresh_token_repo = refresh_token_repo
        self._settings = settings

    async def execute(self, input: OAuthCallbackInput) -> TokenPair:
        now = datetime.now(tz=timezone.utc)

        oauth_account = await self._oauth_account_repo.get_by_provider(
            input.provider, input.provider_user_id
        )

        if oauth_account:
            user = await self._user_repo.get_by_id(oauth_account.user_id)
        else:
            # Try linking to an existing account by email
            user = await self._user_repo.get_by_email(input.provider_email or "") if input.provider_email else None

            if not user:
                # New user — create account
                user = User(
                    id=uuid4(),
                    email=input.provider_email or "",
                    password_hash=None,
                    display_name=input.display_name,
                    bio=None,
                    avatar_url=None,
                    roles=["USER"],
                    created_at=now,
                    updated_at=now,
                )
                await self._user_repo.save(user)

            # Link OAuth account to user
            oauth_account = OAuthAccount(
                id=uuid4(),
                user_id=user.id,
                provider=input.provider,
                provider_user_id=input.provider_user_id,
                provider_email=input.provider_email,
                created_at=now,
                updated_at=now,
            )
            await self._oauth_account_repo.save(oauth_account)

        return await _issue_token_pair(user, self._refresh_token_repo, self._settings)
