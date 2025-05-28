import logging

from delivery_service.application.interfaces.logger import ILogger
from delivery_service.infrastructure.logger.console_handler import \
    get_console_handler
from delivery_service.infrastructure.logger.file_handler import \
    get_file_handler
from delivery_service.infrastructure.logger.logger import Logger


class LoggerFactory:
    """
    Factory for creating and configuring application logger.
    """

    def __init__(self, log_level: int = logging.INFO):
        self._log_level = log_level
        self._instance: Logger | None = None

    def get_logger(self) -> ILogger:
        """
        Returns a configured logger instance.
        """
        if self._instance is None:
            logger = Logger(name="delivery_service", level=self._log_level)

            logger.add_handler(
                get_file_handler("logs/delivery_service.log", logging.ERROR)
            )
            logger.add_handler(get_console_handler(self._log_level))
            self._instance = logger
        return self._instance
