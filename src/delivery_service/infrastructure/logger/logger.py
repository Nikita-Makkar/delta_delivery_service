import logging

from delivery_service.application.interfaces.logger import ILogger


class Logger(ILogger):
    """
    Logger.
    Supports adding custom handlers
    """

    def __init__(self, name: str, level: int = logging.INFO):
        """
        Creates a logger instance with specified name and level.
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.propagate = False

    def add_handler(self, handler: logging.Handler) -> None:
        """
        Adds a handler (e.g., console or file) to the logger.
        """
        self._logger.addHandler(handler)

    def debug(self, msg: str) -> None:
        """Log debug-level message."""
        self._logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log info-level message."""
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        """Log warning-level message."""
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        """Log error-level message."""
        self._logger.error(msg)
