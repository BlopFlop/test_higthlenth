from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
JSON_VALID_DATA: Final[Path] = (
    BASE_DIR / r"tests\test_json_data\task_db_vlaid_data.json"
)
JSON_INVALID_DATA: Final[Path] = (
    BASE_DIR / r"tests\test_json_data\task_db_invalid_data.json"
)
