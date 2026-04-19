from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    password_hash: str | None  # None for OAuth-only accounts
    display_name: str
    bio: str | None
    avatar_url: str | None
    roles: list[str] = field(default_factory=list)  # role name strings e.g. ["admin", "user"]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class OAuthAccount:
    id: UUID
    user_id: UUID
    provider: str
    provider_user_id: str
    provider_email: str | None
    created_at: datetime
    updated_at: datetime


@dataclass
class RefreshToken:
    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    revoked_at: datetime | None
    created_at: datetime
