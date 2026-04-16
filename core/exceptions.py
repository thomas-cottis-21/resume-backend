class NomadaException(Exception):
    """Base exception for all application errors."""


class NotFoundError(NomadaException):
    """Raised when a requested resource does not exist."""


class ConflictError(NomadaException):
    """Raised when an operation conflicts with existing state."""


class ValidationError(NomadaException):
    """Raised when input data fails domain validation."""


class OwnershipError(NomadaException):
    """Raised when a resource does not belong to the requesting user."""
