from core.exceptions import ConflictError, NotFoundError


class DestinationNotFound(NotFoundError):
    def __init__(self, destination_id: object) -> None:
        super().__init__(f"Destination not found: {destination_id}")


class BucketListItemNotFound(NotFoundError):
    def __init__(self, item_id: object) -> None:
        super().__init__(f"Bucket list item not found: {item_id}")


class VisitNotFound(NotFoundError):
    def __init__(self, visit_id: object) -> None:
        super().__init__(f"Visit not found: {visit_id}")


class BucketListStatusNotFound(NotFoundError):
    def __init__(self, status_id: object) -> None:
        super().__init__(f"Bucket list status not found: {status_id}")


class AlreadyInBucketList(ConflictError):
    def __init__(self, destination_id: object) -> None:
        super().__init__(f"Destination {destination_id} is already in the bucket list")
