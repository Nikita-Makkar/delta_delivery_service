import logging
from pathlib import Path


def get_file_handler(
    log_path: str,
    level: int = logging.INFO,
) -> logging.Handler:
    """
    Creates a file handler for logging.
    """
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(level)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%y %H:%M:%S",
    )
    handler.setFormatter(formatter)
    return handler
