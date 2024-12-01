from datetime import date

from repository import RepositoryTask, TaskSchema
from constants import JSON_FILE

json_task_obj = RepositoryTask(JSON_FILE)
task_ = TaskSchema(
        id=1,
        title="Изучить основы FastAPI",
        description="Пройти документация по FastAPI",
        category="Обучение",
        due_date="2024-11-30",
        priority="Высокий",
        status=True,
    )
data = task_.model_dump()
data.pop("id")

# json_task_obj.create(
#     **data
# )

# print(json_task_obj.get())
