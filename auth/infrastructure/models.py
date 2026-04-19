from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DATETIME, TEXT, VARCHAR, ForeignKey, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from core.database.types import BinaryUUID


class AuthBase(DeclarativeBase):
    pass


class RoleModel(AuthBase):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(BinaryUUID(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)


class UserRoleModel(AuthBase):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(
        BinaryUUID(), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[UUID] = mapped_column(
        BinaryUUID(), ForeignKey("roles.id"), primary_key=True
    )


class UserModel(AuthBase):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(BinaryUUID(), primary_key=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    password_hash: Mapped[str | None] = mapped_column(VARCHAR(255), nullable=True)
    display_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    bio: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(VARCHAR(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    roles: Mapped[list[RoleModel]] = relationship(
        secondary="user_roles", lazy="selectin"
    )
    oauth_accounts: Mapped[list[OAuthAccountModel]] = relationship(
        back_populates="user", lazy="noload"
    )


class OAuthAccountModel(AuthBase):
    __tablename__ = "oauth_accounts"

    id: Mapped[UUID] = mapped_column(BinaryUUID(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        BinaryUUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    provider_email: Mapped[str | None] = mapped_column(VARCHAR(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    user: Mapped[UserModel] = relationship(back_populates="oauth_accounts", lazy="noload")


class RefreshTokenModel(AuthBase):
    __tablename__ = "refresh_tokens"

    id: Mapped[UUID] = mapped_column(BinaryUUID(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        BinaryUUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
