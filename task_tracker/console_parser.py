import logging
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from task_tracker.constants import (
    ARG_DELETE,
    ARG_GET,
    ARG_GET_ALL,
    ARG_PATCH,
    ARG_POST,
    ARG_SEARCH,
    CATEGORY_FIELD_HELP_TEXT,
    CRUD_ARGUMENTS_HELD_TEXT,
    DESCRIPTION_CONSOLE_PROGRAM,
    DESCRIPTION_FIELD_HELP_TEXT,
    DUE_DATE_FIELD_HELP_TEXT,
    ID_FIELD_HELP_TEXT,
    JSON_FILE,
    NAME_FIELD_HELP_TEXT,
    PRIORITY_FIELD_HELP_TEXT,
    STATUS_FIELD_HELP_TEXT,
    TITLE_FIELD_HELP_TEXT,
    VALUE_HELP_TEXT,
)
from task_tracker.outputs import pretty_tasks_output
from task_tracker.repository import RepositoryTask
from task_tracker.utils import except_control


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def get(repository: RepositoryTask, namespace: Namespace) -> None:
    """Get tasks for id or category."""
    obj_id = namespace.id
    category = namespace.category

    if (obj_id is None) and not category:
        warning_message = (
            "Чтобы получить элементы, вы должны передать"
            " либо id либо имя категории."
        )
        logging.warning(warning_message)
        print(warning_message)
        return

    tasks = repository.get(obj_id=obj_id, category=category)
    if isinstance(tasks, list):
        pretty_tasks_output(tasks)
    else:
        pretty_tasks_output([tasks])


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def get_all(repository: RepositoryTask, namespace: Namespace):
    """Get all tasks."""
    tasks = repository.get_all()
    pretty_tasks_output(tasks)


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def post(repository: RepositoryTask, namespace: Namespace) -> None:
    """Create tasks."""
    fields = dict(
        title=namespace.title,
        description=namespace.description,
        category=namespace.category,
        due_date=namespace.due_date,
        priority=namespace.priority,
        status=namespace.status,
    )
    for field_name in fields:
        if fields[field_name] is None:
            warning_message = (
                f"У обязательного поля {field_name} нет значения.",
                "Для создания объекта необходимо дать значение",
                "всех обязательных полей.",
            )
            logging.warning(warning_message)
            print(warning_message)
            return

    new_task = repository.create(**fields)
    pretty_tasks_output([new_task])


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def patch(repository: RepositoryTask, namespace: Namespace) -> None:
    """Update task for id."""
    obj_id = namespace.id
    fields = dict(
        title=namespace.title,
        description=namespace.description,
        category=namespace.category,
        due_date=namespace.due_date,
        priority=namespace.priority,
        status=namespace.status,
    )
    if obj_id is None:
        warning_message = "Для изменения объекта вы должны передать айди."
        logging.warning(warning_message)
        print(warning_message)
        return
    if not any(fields.values()):
        warning_message = (
            "Для изменения объекта хотя бы одно поле с "
            "аргументом для изменения."
        )
        logging.warning(warning_message)
        print(warning_message)
        return

    fields = {name: value for name, value in fields if value is not None}

    update_task = repository.update(obj_id=obj_id, **fields)
    pretty_tasks_output([update_task])


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def delete(repository: RepositoryTask, namespace: Namespace) -> None:
    """Delete tasks for id or category."""
    obj_id = namespace.id
    category = namespace.category

    if (obj_id is None) and not category:
        warning_message = (
            "Чтобы Удалить элементы, вы должны передать"
            " либо id либо имя категории."
        )
        logging.warning(warning_message)
        print(warning_message)
        return

    repository.remove(obj_id=obj_id, category=category)
    print("Элементы успешно удалены.")


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def search(repository: RepositoryTask, namespace: Namespace) -> None:
    """Search tasks for field and value."""
    field = namespace.field
    value = namespace.value

    if field is None or value is None:
        warning_message = (
            "Вы должны передать в аргументы поле и значение для поиска."
        )
        logging.warning(warning_message)
        print(warning_message)
        return

    tasks = repository.get_obj_for_field_arg(field=field, arg=value, many=True)
    pretty_tasks_output(tasks)


CRUD = {
    ARG_GET_ALL: get_all,
    ARG_GET: get,
    ARG_POST: post,
    ARG_PATCH: patch,
    ARG_DELETE: delete,
    ARG_SEARCH: search,
}


def parser():
    logging.info("Программа запущена.")

    repository = RepositoryTask(JSON_FILE)

    parser = ArgumentParser(
        description=DESCRIPTION_CONSOLE_PROGRAM,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("crud", choices=CRUD, help=CRUD_ARGUMENTS_HELD_TEXT)

    parser.add_argument("--id", type=int, help=ID_FIELD_HELP_TEXT)
    parser.add_argument("--title", type=str, help=TITLE_FIELD_HELP_TEXT)
    parser.add_argument(
        "--description", type=str, help=DESCRIPTION_FIELD_HELP_TEXT
    )
    parser.add_argument(
        "--category",
        type=str,
        default="Без категории",
        help=CATEGORY_FIELD_HELP_TEXT,
    )
    parser.add_argument("--due_date", type=str, help=DUE_DATE_FIELD_HELP_TEXT)
    parser.add_argument(
        "--priority",
        type=str,
        default="Средний",
        help=PRIORITY_FIELD_HELP_TEXT,
    )
    parser.add_argument(
        "--status",
        type=lambda x: (str(x).lower() == 'true'),
        help=STATUS_FIELD_HELP_TEXT
    )
    parser.add_argument("-f", "--field", type=str, help=NAME_FIELD_HELP_TEXT)
    parser.add_argument("-v", "--value", type=str, help=VALUE_HELP_TEXT)

    args: Namespace = parser.parse_args()
    parser_crud = args.crud

    logging.info(f"Программа запущена в режиме {parser_crud}")
    logging.info(f"Переданные аргументы {args}")
    CRUD[parser_crud](repository, namespace=args)
