from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from resume.application.dtos import ReorderItem
from resume.domain.repositories import WorkExperienceRepository


class ReorderWorkExperiences:
    def __init__(self, repo: WorkExperienceRepository) -> None:
        self._repo = repo

    async def execute(self, items: list[ReorderItem]) -> None:
        await self._repo.update_sort_orders(
            [(item.id, item.sort_order) for item in items]
        )
