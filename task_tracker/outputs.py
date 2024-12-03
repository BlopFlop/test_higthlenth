import logging

from prettytable import PrettyTable

from task_tracker.repository import TaskSchema


def pretty_tasks_output(tasks: list[TaskSchema]) -> None:
    task_table = PrettyTable()
    task_table.field_names = (
        "id",
        "title",
        "description",
        "category",
        "due_date",
        "priority",
        "status",
    )
    task_table.align = "l"
    for task in tasks:
        rows = (
            task.id,
            task.title,
            task.description,
            task.category,
            task.due_date,
            task.priority[:],
            task.status,
        )
        task_table.add_row(rows)
    logging.info(f"Выведено {len(tasks)} задач")
    print(task_table)
