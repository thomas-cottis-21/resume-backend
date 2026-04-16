from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import DATE, DATETIME, TEXT, VARCHAR, ForeignKey, SmallInteger, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DestinationCategoryModel(Base):
    __tablename__ = "destination_categories"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    sort_order: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)

    destinations: Mapped[list[DestinationModel]] = relationship(
        back_populates="category", lazy="noload"
    )


class BucketListStatusModel(Base):
    __tablename__ = "bucket_list_statuses"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)

    bucket_list_items: Mapped[list[BucketListItemModel]] = relationship(
        back_populates="status", lazy="noload"
    )


class DestinationModel(Base):
    __tablename__ = "destinations"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    country: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    continent: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    cover_image_url: Mapped[str | None] = mapped_column(VARCHAR(500), nullable=True)
    category_id: Mapped[str | None] = mapped_column(
        VARCHAR(36),
        ForeignKey("destination_categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    category: Mapped[DestinationCategoryModel | None] = relationship(
        back_populates="destinations", lazy="noload"
    )
    bucket_list_items: Mapped[list[BucketListItemModel]] = relationship(
        back_populates="destination", lazy="noload"
    )
    visits: Mapped[list[VisitModel]] = relationship(
        back_populates="destination", lazy="noload"
    )


class BucketListItemModel(Base):
    __tablename__ = "bucket_list_items"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(VARCHAR(36), nullable=False, index=True)
    destination_id: Mapped[str] = mapped_column(
        VARCHAR(36),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
    )
    status_id: Mapped[str] = mapped_column(
        VARCHAR(36),
        ForeignKey("bucket_list_statuses.id", ondelete="RESTRICT"),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    destination: Mapped[DestinationModel] = relationship(
        back_populates="bucket_list_items", lazy="noload"
    )
    status: Mapped[BucketListStatusModel] = relationship(
        back_populates="bucket_list_items", lazy="noload"
    )


class VisitModel(Base):
    __tablename__ = "visits"

    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(VARCHAR(36), nullable=False, index=True)
    destination_id: Mapped[str] = mapped_column(
        VARCHAR(36),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
    )
    visited_at: Mapped[date] = mapped_column(DATE, nullable=False)
    notes: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    destination: Mapped[DestinationModel] = relationship(
        back_populates="visits", lazy="noload"
    )
