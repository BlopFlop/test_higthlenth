from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
JSON_FILE: Final[Path] = BASE_DIR / "task_db.json"
LOG_DIR: Final[Path] = BASE_DIR / "logging"
LOG_FILE_NAME: Final[str] = "task_tracker.log"

# parser constants
DESCRIPTION_CONSOLE_PROGRAM: Final[str] = (
    "Консольная программа для просмотра, приложение для управления \n"
    "списком задач с возможностью добавления, выполнения, удаления и \n"
    "поиска задач"
)

GET_ALL_ARG: Final[str] = "get_all"
GET_ARG: Final[str] = "get"
POST_ARG: Final[str] = "post"
PATCH_ARG: Final[str] = "patch"
DELETE_ARG: Final[str] = "delete"

CRUD_ARGUMENTS_HELD_TEXT: Final[str] = (
    f"{GET_ALL_ARG} - Получение всех задач.\n"
    f"{GET_ARG} - Получение задач по айди или категории. \n"
    " Обязательные поля (--id или --category)\n"
    f"{POST_ARG} - Создание задачи. \n"
    " Обязательные поля\n"
    " (--title, --description, --category, --due_date, --priority, --status)\n"
    f"{PATCH_ARG} - Обновление задачи. Обязательные поля(--id) \n"
    " Опциональные поля\n"
    " (--title, --description, --category, --due_date, --priority, --status)\n"
    f"{DELETE_ARG} - Удаление задачи. \n"
    "  Обязательные поля(--id или --category)\n"
)

ID_FIELD_HELP_TEXT: Final[str] = "Айди задачи в json."
TITLE_FIELD_HELP_TEXT: Final[str] = "Тема задачи."
DESCRIPTION_FIELD_HELP_TEXT: Final[str] = "Описание задачи."
CATEGORY_FIELD_HELP_TEXT: Final[str] = (
    "Имя категории. (По умолчанию: Нет категории)"
)
DUE_DATE_FIELD_HELP_TEXT: Final[str] = "Дата выполнения задачи."
PRIORITY_FIELD_HELP_TEXT: Final[str] = (
    "Приоритет выполнения задачи. (По умолчанию: Средний)"
)
STATUS_FIELD_HELP_TEXT: Final[str] = (
    "Статус выполнения задачи. (По умолчанию: False)"
)
