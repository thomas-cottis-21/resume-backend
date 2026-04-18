from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DATETIME, TEXT, VARCHAR, ForeignKey, SmallInteger, text
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from core.database.types import BinaryUUID


class Base(DeclarativeBase):
    pass


class PostStatusModel(Base):
    __tablename__ = "post_statuses"

    id: Mapped[UUID] = mapped_column(BinaryUUID(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)

    posts: Mapped[list[PostModel]] = relationship(back_populates="status", lazy="noload")


class TagModel(Base):
    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(BinaryUUID(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    post_tags: Mapped[list[PostTagModel]] = relationship(back_populates="tag", lazy="noload")


class PostTagModel(Base):
    __tablename__ = "post_tags"

    post_id: Mapped[UUID] = mapped_column(
        BinaryUUID(), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[UUID] = mapped_column(
        BinaryUUID(), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    post: Mapped[PostModel] = relationship(back_populates="post_tags", lazy="noload")
    tag: Mapped[TagModel] = relationship(back_populates="post_tags", lazy="noload")


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(BinaryUUID(), primary_key=True)
    slug: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    excerpt: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    content: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    cover_image_url: Mapped[str | None] = mapped_column(VARCHAR(500), nullable=True)
    reading_time_minutes: Mapped[int | None] = mapped_column(TINYINT(unsigned=True), nullable=True)
    status_id: Mapped[UUID] = mapped_column(
        BinaryUUID(), ForeignKey("post_statuses.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    author_id: Mapped[UUID] = mapped_column(
        BinaryUUID(), ForeignKey("users.id"), nullable=False, index=True
    )
    published_at: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    status: Mapped[PostStatusModel] = relationship(back_populates="posts", lazy="noload")
    post_tags: Mapped[list[PostTagModel]] = relationship(
        back_populates="post", lazy="noload", cascade="all, delete-orphan"
    )
