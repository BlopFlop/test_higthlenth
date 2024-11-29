from typing import Final
from pathlib import Path

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent
JSON_FILE: Final[Path] = BASE_DIR / "task_db.json"
JOG_DIR: Final[Path] = BASE_DIR / "logging"
