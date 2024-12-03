import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(
    path_log_file: Path, log_file_name: str, log_format: str
) -> None:
    """Configure logging from this project."""
    path_log_file.mkdir(exist_ok=True)
    log_file_path = path_log_file / log_file_name
    rotating_handler: RotatingFileHandler = RotatingFileHandler(
        log_file_path, encoding="utf-8", maxBytes=10**6, backupCount=5
    )
    logging.basicConfig(
        format=log_format, level=logging.INFO, handlers=(rotating_handler,)
    )
