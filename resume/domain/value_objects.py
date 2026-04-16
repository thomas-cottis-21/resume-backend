from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from urllib.parse import urlparse

from core.exceptions import ValidationError


@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date | None

    def __post_init__(self) -> None:
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValidationError("end_date cannot be before start_date")


@dataclass(frozen=True)
class SortOrder:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValidationError("sort_order must be non-negative")


@dataclass(frozen=True)
class Url:
    value: str

    def __post_init__(self) -> None:
        parsed = urlparse(self.value)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValidationError(f"Invalid URL: {self.value!r}")
