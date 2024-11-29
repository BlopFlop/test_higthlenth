from typing import Any
from pathlib import Path
from functools import wraps

from pydantic import TypeAdapter

from task_tracker.schemas import TaskSchema


class RepositoryTask:
    """Base CRUD operations in current application."""
    __task_adapter = TypeAdapter(list[TaskSchema])

    def __init__(self, path_json: Path):
        self.path_json = self.__get_or_create_json(path_json)
        self.data = self.__get_data()

    @property
    def __autoincrement_id(self) -> int:
        if not self.data:
            return 1
        ids = map(lambda task: task.id, self.data)
        return max(ids) + 1

    def __get_or_create_json(self, path_file: Path) -> Path:
        if not path_file.is_file():
            with open(path_file, mode="w", encoding="utf-8"):
                pass
        return path_file

    def __get_data(self) -> list[TaskSchema]:
        with open(self.path_json, mode="r", encoding="utf-8") as json_file:
            json_data = json_file.read()
            if not (json_data):
                return []
            obj_data = self.__task_adapter.validate_json(json_file.read())
        return obj_data

    def change_data_json_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self: RepositoryTask = args[0]

            result = func(*args, **kwargs)
            with open(self.path_json, mode="w", encoding="utf-8") as json_file:
                json_data = self.__task_adapter.dump_json(self.data).decode()
                json_file.write(json_data)
            return result
        return wrapper

    def get(
        self,
        obj_id: int = None,
        category: str = None
    ) -> TaskSchema | list[TaskSchema]:
        """Get task model for id."""
        if obj_id:
            return self.get_obj_for_field_arg("id", obj_id, False)

        if category:
            return self.get_obj_for_field_arg("category", category, True)

        except_message = ""
        raise ValueError(except_message)

    def get_all(self):
        return self.data

    @change_data_json_decorator
    def create(self, **kwargs) -> TaskSchema:
        """Create task."""
        task_new_obj = TaskSchema(id=self.__autoincrement_id, **kwargs)
        self.data.append(task_new_obj)
        return task_new_obj

    @change_data_json_decorator
    def update(self, obj_id: int, **kwargs):
        """Update task for id and other fields."""
        obj_db = self.get(obj_id)
        obj_data = obj_db.model_dump()

        for field in obj_data:
            if field in kwargs:
                setattr(obj_db, field, kwargs[field])

        return obj_db

    @change_data_json_decorator
    def remove(self, obj_id: int) -> None:
        """Delete item model for id."""
        remove_task = self.get(obj_id=obj_id)
        self.data = list(filter(lambda task: task.id != obj_id, remove_task))

    def get_obj_for_field_arg(self, field: str, arg: Any, many: bool):
        """Get model for keyword argument."""
        filter_data = list(filter(
            lambda task: getattr(task, field) == arg,
            self.data
        ))

        if not len(filter_data):
            except_message = ""
            raise ValueError(except_message)

        if many:
            return filter_data
        return filter_data[0]
