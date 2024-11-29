from datetime import date

from db import JsonTask
from constants import JSON_FILE

json_task_obj = JsonTask(JSON_FILE)

json_task_obj.post(
    title="Изучить основы FastAPI",
    description="Пройти документация по FastAPI",
    category="Обучение",
    due_date="2024-11-30",
    priority="Высокий",
    status=True
)

print(json_task_obj.get())
