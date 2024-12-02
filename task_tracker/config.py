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
        log_file_path, maxBytes=10**6, backupCount=5
    )
    rotating_handler.setFormatter(log_format)
    project_logger = logging.getLogger(log_file_path.stem)
    project_logger.setLevel(logging.INFO)
    project_logger.addHandler(rotating_handler)
    project_logger.addHandler(logging.StreamHandler())
