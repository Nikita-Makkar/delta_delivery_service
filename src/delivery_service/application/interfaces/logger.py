from typing import Protocol


class ILogger(Protocol):
    """
    Interface for logging messagest.
    """

    def debug(self, msg: str) -> None:
        """Log a debug-level message."""
        ...

    def info(self, msg: str) -> None:
        """Log an info-level message."""
        ...

    def warning(self, msg: str) -> None:
        """Log a warning-level message."""
        ...

    def error(self, msg: str) -> None:
        """Log an error-level message."""
        ...
