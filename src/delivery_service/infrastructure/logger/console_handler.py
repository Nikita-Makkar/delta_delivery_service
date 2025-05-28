import logging
import sys
from typing import TextIO


def get_console_handler(
    level: int = logging.INFO,
    stream: TextIO = sys.stdout,
) -> logging.Handler:
    """
    Creates a console handler for logging to stdout or stderr.
    """
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    formatter = logging.Formatter(
        fmt="\n%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%y %H:%M:%S",
    )
    handler.setFormatter(formatter)
    return handler
