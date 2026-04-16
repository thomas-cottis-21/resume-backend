from core.exceptions import ConflictError, NotFoundError, OwnershipError, ValidationError


class PostNotFoundError(NotFoundError):
    def __init__(self, post_id: object) -> None:
        super().__init__(f"Post not found by identifier: {post_id}")


class StatusesNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__("Post statuses not found")


class DuplicatePostError(ConflictError):
    def __init__(self) -> None:
        super().__init__("Post already exists")


class PostOwnershipError(OwnershipError):
    def __init__(self) -> None:
        super().__init__("User is not owner of post")


class PostIdentifierError(ValidationError):
    def __init__(self) -> None:
        super().__init__("Post identifier not included")