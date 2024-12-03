from task_tracker import (
    LOG_DIR,
    LOG_FILE_NAME,
    LOG_FORMAT,
    configure_logging,
    parser,
)

if __name__ == "__main__":
    configure_logging(LOG_DIR, LOG_FILE_NAME, LOG_FORMAT)
    parser()
