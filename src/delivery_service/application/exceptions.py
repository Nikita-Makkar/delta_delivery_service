"""
Application-level exceptions for expected error cases.
"""


class ApplicationError(Exception):
    """Base class for application errors."""

    pass


class BoxNotFoundError(ApplicationError):
    """Raised when a box is not found."""

    pass


class ExchangeRateNotAvailableError(ApplicationError):
    """Raised when exchange rate cannot be fetched."""

    pass


class CacheError(ApplicationError):
    """Raised when cache operation fails."""

    pass


class DatabaseException(ApplicationError):
    """General database access error."""

    pass


class DatabaseOperationException(DatabaseException):
    """Raised when a DB operation fails."""

    pass


class SessionNotProvidedException(DatabaseException):
    """Raised when session is missing in context."""

    pass


class MessageQueueError(ApplicationError):
    """Raised when message queue operation fails."""

    pass
