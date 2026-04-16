from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from blog.domain.exceptions import PostNotFoundError, PostOwnershipError
from blog.domain.repositories import PostRepository


@dataclass
class DeletePostInput:
    post_id: UUID
    user_id: UUID # this may not be the same as the author id;
    # user_id will be used to implement auth logic in the use case
    # TODO implement user_id in the controller from the JWT and not as a parameter


class DeletePost:
    def __init__(self, post_repo: PostRepository) -> None:
        self._post_repo = post_repo


    async def execute(self, input: DeletePostInput) -> None:
        post = await self._post_repo.get_by_id(input.post_id)

        if post is None:
            raise PostNotFoundError(post_id=input.post_id)

        if post.author_id == input.user_id:
            await self._post_repo.delete(input.post_id)
        else:
            raise PostOwnershipError()

