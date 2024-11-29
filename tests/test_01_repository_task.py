from task_tracker.repository import RepositoryTask
from task_tracker.schemas import TaskSchema
from enum import Enum


class TestRepository:

    def test_create_json_file(self, repository: RepositoryTask):
        path_json = repository.path_json
        assert repository.path_json.is_file(), (
            f"После инициализации класса {RepositoryTask.__name__}, "
            f"должен появиться json файл по пути {path_json}."
        )

    def test_create_task(self, repository: RepositoryTask, task: TaskSchema):
        task_data = task.model_dump()
        task_data.pop("id")

        new_task = repository.create(**task_data)

        assert isinstance(new_task, TaskSchema), (
            "После создания задачи должен вернуться объект"
            f" {TaskSchema.__name__}"
        )

        new_task_data = new_task.model_dump()

        for field, value in task_data.items():
            assert (field in new_task_data), (
                f"После создания задачи в объекте {TaskSchema.__name__} "
                f"должно присутствовать поле {field}"
            )
            assert str(value) == str(new_task_data[field]), (
                f"После создания задачи в объекте {TaskSchema.__name__} "
                f"Поле {field} должно иметь значение {value}, "
                f"а не {new_task_data[field]}."
            )

    def test_get_all_task(self, repository: RepositoryTask, task: TaskSchema):
        count_item = 20

        task_data = task.model_dump()
        task_data.pop("id")
        for _ in range(count_item):
            repository.create(**task_data)

        tasks = repository.get_all()

        assert isinstance(tasks, list), (
            "При получении всех задач результатом "
            "должен быть список элементов."
        )
        assert len(tasks) == count_item, (
            "При получении всех элементов из json файла, количество"
            f" элементов должно быть равно {count_item}, а равняется"
            f" {len(tasks)}."
        )
        assert all(map(lambda item: isinstance(item, TaskSchema), tasks)), (
            f"Все задачи должны быть типом {TaskSchema.__name__}."
        )

    def test_get_task_for_id(self, repository: RepositoryTask, task: TaskSchema):
        self.test_get_all_task(repository, task)

        get_task = repository.get(obj_id=task.id)
        assert isinstance(get_task, TaskSchema), (
            "При получении элемента по айди, должен "
            f"вернуться единственный элемент с типом {TaskSchema.__name__}"
        )
        assert task.model_dump() == get_task.model_dump(), (
            "Все поля и значения из полученной модели по айди, и"
            "поля из первоначальной модели должны быть равны."
        )

    def test_get_task_for_category(self, repository: RepositoryTask, task: TaskSchema):
        count_item = 20
        count_item_other_category = 65

        task_data = task.model_dump()
        task_data.pop("id")
        for _ in range(count_item):
            repository.create(**task_data)

        new_category = "TestCategoryNew"
        task_data["category"] = new_category
        for _ in range(count_item_other_category):
            repository.create(**task_data)

        tasks = repository.get(category=task.category)

        assert isinstance(tasks, list), (
            "При получении задач категориям результатом "
            "должен быть список элементов."
        )
        assert len(tasks) == count_item, (
            "При получении элементов по категориям из json файла, количество"
            f" элементов должно быть равно {count_item}, а равняется"
            f" {len(tasks)}."
        )
        assert all(map(lambda item: isinstance(item, TaskSchema), tasks)), (
            f"Все задачи должны быть типом {TaskSchema.__name__}."
        )
