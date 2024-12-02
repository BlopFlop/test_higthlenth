from argparse import ArgumentParser, RawTextHelpFormatter

from constants import (
    CATEGORY_FIELD_HELP_TEXT,
    CRUD_ARGUMENTS_HELD_TEXT,
    DELETE_ARG,
    DESCRIPTION_CONSOLE_PROGRAM,
    DESCRIPTION_FIELD_HELP_TEXT,
    DUE_DATE_FIELD_HELP_TEXT,
    GET_ALL_ARG,
    GET_ARG,
    ID_FIELD_HELP_TEXT,
    JSON_FILE,
    PATCH_ARG,
    POST_ARG,
    PRIORITY_FIELD_HELP_TEXT,
    STATUS_FIELD_HELP_TEXT,
    TITLE_FIELD_HELP_TEXT,
)
from outputs import pretty_tasks_output
from repository import RepositoryTask


def get(repository: RepositoryTask, **kwargs) -> None:
    tasks = repository.get(
        obj_id=kwargs.get("id"), category=kwargs.get("category")
    )
    if isinstance(tasks, list):
        pretty_tasks_output(tasks)
    else:
        pretty_tasks_output([tasks])


def get_all(repository: RepositoryTask):
    tasks = repository.get_all()
    pretty_tasks_output(tasks)


def post(repository: RepositoryTask, **kwargs) -> None:
    new_task = repository.create(**kwargs)
    pretty_tasks_output([new_task])


def patch(repository: RepositoryTask, id: int, **kwargs) -> None:
    update_task = repository.update(obj_id=id, **kwargs)
    pretty_tasks_output([update_task])


def delete(repository: RepositoryTask, **kwargs) -> None:
    repository.remove(obj_id=kwargs.get("id"), category=kwargs.get("category"))
    print("Элементы успешно удалены.")


def search(repository: RepositoryTask, field: str, search_value) -> None:
    pass


CRUD = {
    GET_ALL_ARG: get_all,
    GET_ARG: get,
    POST_ARG: post,
    PATCH_ARG: patch,
    DELETE_ARG: delete,
    # "search": search
}


def main():
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
        "--status", type=bool, default=False, help=STATUS_FIELD_HELP_TEXT
    )

    args = parser.parse_args()

    parser_crud = args.crud
    arg_id = args.id
    arg_title = args.title
    arg_description = args.description
    arg_category = args.category
    arg_due_date = args.due_date
    arg_priority = args.priority
    arg_status = args.status

    repository = RepositoryTask(JSON_FILE)

    if parser_crud == GET_ARG:
        if arg_id and arg_category:
            CRUD[parser_crud](repository, id=arg_id, category=arg_category)
        else:
            print(
                "Чтобы получить элементы, вы должны передать"
                " либо id либо имя категории."
            )
    elif parser_crud == GET_ALL_ARG:
        CRUD[parser_crud](repository)
    elif parser_crud == POST_ARG:
        post_fields = dict(
            title=arg_title,
            description=arg_description,
            category=arg_category,
            due_date=arg_due_date,
            priority=arg_priority,
            status=arg_status,
        )
        if all(post_fields.values()):
            CRUD[parser_crud](repository, **post_fields)
        else:
            print(
                "Вы должны передать все обязательные поля чтобы "
                "создать объект задачи."
            )
    elif parser_crud == PATCH_ARG:
        patch_fields = dict(
            title=arg_title,
            description=arg_description,
            category=arg_category,
            due_date=arg_due_date,
            priority=arg_priority,
            status=arg_status,
        )
        if arg_id and any(patch_fields.values()):
            fields = {
                key: item for key, item in patch_fields.items() if key and item
            }
            CRUD[parser_crud](repository, id=arg_id, **fields)
        else:
            print(
                "Для изменения объекта вы должны передать айди "
                "и хотя бы одно поле с аргументом для изменения."
            )
    elif parser_crud == DELETE_ARG:
        if arg_id:
            CRUD[parser_crud](repository, id=arg_id)
        else:
            print("Для удаления объекта вы должны обязательно передать айди.")


if __name__ == "__main__":
    main()
