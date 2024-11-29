from pathlib import Path
import json

from task import Task

from pydantic import TypeAdapter


class JsonTask:
    __task_adapter = TypeAdapter(list[Task])

    def __init__(self, path_json_file: Path) -> None:
        self.path_json: Path = self.__get_or_create(path_json_file)

    @property
    def __autoincrement_id(self) -> int:
        data = self.__get_data()
        ids = map(lambda task: task.id, data)
        return max(ids) + 1

    def __get_or_create(self, path_file: Path) -> Path:
        if not path_file.is_file():
            with open(path_file, mode="w", encoding="utf-8"):
                pass
        return path_file

    def __change_data(self, data: list[Task]) -> None:
        with open(self.path_json, mode="w", encoding="utf-8") as json_file:
            json_data = self.__task_adapter.dump_json(data, round_trip=True).decode()
            json_file.write(json_data)

    def __get_data(self) -> list[Task]:
        with open(self.path_json, mode="r", encoding="utf-8") as json_file:
            obj_data = self.__task_adapter.validate_json(json_file.read())
        return obj_data

    def search(self, **kwargs) -> list[Task]:
        pass

    def get(self, id: int = None, category: str = None) -> list[Task] | Task:
        data = self.__get_data()
        if id:
            task_for_id = list(filter(lambda task: task.id == id, data))

            if not task_for_id:
                except_message = ""
                raise ValueError(except_message)

            return task_for_id

        if category:
            tasks_for_category = list(filter(lambda task: task.category, data))

            if not tasks_for_category:
                except_message = ""
                raise ValueError(except_message)

            return tasks_for_category
        return data

    def post(self, **kwargs) -> Task:
        data = self.__get_data()
        new_object = Task(id=self.__autoincrement_id, **kwargs)
        new_data = data.append(new_object)
        return self.__change_data(new_data)

    def patch(self, id: int, **kwargs) -> Task:
        task_obj: Task = self.get(id)
        pass

    def delete(self, id: int = None, category: str = None) -> None:
        if id or category:
            pass

        except_message = ""
        raise ValueError(except_message)
