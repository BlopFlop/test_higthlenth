from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
JSON_FILE: Final[Path] = BASE_DIR / "task_db.json"

LOG_DIR: Final[Path] = BASE_DIR / "logging"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_FILE_NAME: Final[str] = "task_tracker.log"

# parser constants
DESCRIPTION_CONSOLE_PROGRAM: Final[str] = (
    "Консольная программа для просмотра, приложение для управления \n"
    "списком задач с возможностью добавления, выполнения, удаления и \n"
    "поиска задач"
)

ARG_GET_ALL: Final[str] = "get_all"
ARG_GET: Final[str] = "get"
ARG_POST: Final[str] = "post"
ARG_PATCH: Final[str] = "patch"
ARG_DELETE: Final[str] = "delete"
ARG_SEARCH: Final[str] = "search"

CRUD_ARGUMENTS_HELD_TEXT: Final[str] = (
    f"{ARG_GET_ALL} - Получение всех задач.\n"
    f"{ARG_GET} - Получение задач по айди или категории. \n"
    " Обязательные поля (--id=Идентификатор или --category=Категория)\n"
    f"{ARG_POST} - Создание задачи. \n"
    " Обязательные поля\n"
    " (--title=Тема задачи, --description=Описание задачи, \n"
    "  --category=Категория, --due_date=Дата завершения, \n"
    "  --priority=Приоритет (Высокий/Сердний/Низкий), \n"
    "  --status=Статус выполения (True/False))\n"
    f"{ARG_PATCH} - Обновление задачи. Обязательные поля(--id) \n"
    " Опциональные поля\n"
    " (--title=Тема задачи, --description=Описание задачи, \n"
    "  --category=Категория, --due_date=Дата завершения, \n"
    "  --priority=Приоритет (Высокий/Сердний/Низкий), \n"
    "  --status=Статус выполения (True/False))\n"
    f"{ARG_DELETE} - Удаление задачи. \n"
    " Обязательные поля (--id=Идентификатор или --category=Категория)\n"
    f"{ARG_SEARCH} - Поиск задачи по полю и ключевому слову.\n"
    "  Обязательные поля(-f/--field=Имя поля, -v/--value=Значение)"
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

NAME_FIELD_HELP_TEXT: Final[str] = "Имя поля."
VALUE_HELP_TEXT: Final[str] = "Значение для поиска."
