from uuid import UUID

from sqlalchemy import types


class BinaryUUID(types.TypeDecorator):
    """Stores UUID as BINARY(16), compatible with MySQL's uuid_to_bin(uuid()) default."""

    impl = types.LargeBinary(16)
    cache_ok = True

    def process_bind_param(self, value: UUID | str | bytes | None, dialect) -> bytes | None:
        if value is None:
            return None
        if isinstance(value, UUID):
            return value.bytes
        if isinstance(value, bytes):
            return value
        return UUID(value).bytes

    def process_result_value(self, value: bytes | None, dialect) -> UUID | None:
        if value is None:
            return None
        return UUID(bytes=value)
