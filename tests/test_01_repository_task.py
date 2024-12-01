from task_tracker.repository import RepositoryTask
from task_tracker.schemas import TaskSchema

import pytest


class TestRepository:
    # """Test class for RepositoryTask. It is testing CRUD features for Task objects."""

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
            assert field in new_task_data, (
                f"После создания задачи в объекте {TaskSchema.__name__} "
                f"должно присутствовать поле {field}"
            )
            assert str(value) == str(new_task_data[field]), (
                f"После создания задачи в объекте {TaskSchema.__name__} "
                f"Поле {field} должно иметь значение {value}, "
                f"а не {new_task_data[field]}."
            )

    @pytest.mark.parametrize
    def test_create_task_invalid_data(self, repository: RepositoryTask):
        return NotImplementedError

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
        assert all(
            map(lambda item: isinstance(item, TaskSchema), tasks)
        ), f"Все задачи должны быть типом {TaskSchema.__name__}."

    def test_get_task_for_id(
        self, repository: RepositoryTask, task: TaskSchema
    ):
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

    @pytest.mark.skip
    def test_get_task_for_invalid_id():
        return NotImplementedError

    def test_get_tasks_for_category(
        self, repository: RepositoryTask, task: TaskSchema, task_update: TaskSchema
    ):
        count_item = 20
        count_item_other_category = 65

        task_data = task.model_dump()
        task_data.pop("id")
        for _ in range(count_item):
            repository.create(**task_data)

        task_update_data = task_update.model_dump()
        task_update_data.pop("id")
        for _ in range(count_item_other_category):
            repository.create(**task_update_data)

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
        assert all(
            map(lambda item: isinstance(item, TaskSchema), tasks)
        ), f"Все задачи должны быть типом {TaskSchema.__name__}."

        for task_obj in tasks:
            assert task_obj.category == task.category, (
                "Все объекты полученные по категориям должны иметь"
                f" категорию {task.category}, а не {task_obj.category}."
            )

    @pytest.mark.skip
    def test_get_task_for_invalid_category():
        return NotImplementedError

    def test_update_task(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        count_item = 20

        task_data = task.model_dump()
        task_data.pop("id")
        for _ in range(count_item):
            repository.create(**task_data)

        update_task_data = task_update.model_dump()
        update_task_data.pop("id")

        patch_task = repository.update(obj_id=task.id, **update_task_data)
        get_id_patch_task = repository.get(obj_id=task.id)

        patch_task_data = patch_task.model_dump()
        get_id_patch_task_data = get_id_patch_task.model_dump()

        patch_task_id = patch_task_data.pop("id")
        get_id_patch_task_data.pop("id")

        assert task.id == patch_task_id, (
            "Айди объекта после обновления не должен "
            f"измениться, {task.id} != {patch_task_id}"
        )

        for field in task_data:
            fst_value_field = task_data[field]
            update_task_value_field = patch_task_data[field]
            get_id_task_value_filed = get_id_patch_task_data[field]

            assert fst_value_field != update_task_value_field, (
                "После обновления всех полей, значения объекта не "
                "должны быть равны значениям до обновления. "
                f"{fst_value_field} != {update_task_value_field}"
            )
            assert update_task_value_field == get_id_task_value_filed, (
                "После обновления всех полей, у полученного объекта по "
                "айди, все поля должны быть равны. "
                f"{update_task_value_field} != {get_id_task_value_filed}"
            )

    @pytest.mark.skip
    def test_update_task_invalid_data():
        return NotImplementedError

    def test_delete_task_for_id(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
    ):
        count_item = 20

        task_data = task.model_dump()
        task_data.pop("id")
        for _ in range(count_item):
            repository.create(**task_data)

        for task in repository.get_all()[:]:
            repository.remove(obj_id=task.id)
            new_all_data = repository.get_all()
            delete_task = list(
                filter(lambda task_: task_.id == task.id, new_all_data)
            )
            assert (
                not delete_task
            ), "После удаления объектов из json, он должен быть удален из бд."

    @pytest.mark.skip
    def test_delete_task_for_invalid_id():
        return NotImplementedError

    def test_delete_task_for_category(
        self, repository: RepositoryTask, task: TaskSchema, task_update: TaskSchema
    ):
        count_item = 20
        count_item_other_category = 65

        task_data = task.model_dump()
        task_data.pop("id")
        for _ in range(count_item):
            repository.create(**task_data)

        task_update_data = task_update.model_dump()
        task_update_data.pop("id")
        for _ in range(count_item_other_category):
            repository.create(**task_update_data)

        repository.remove(category=task.category)

        all_tasks = repository.get_all()
        filter_for_category_tasks = list(
            filter(lambda task_: task_.category == task.category, all_tasks)
        )
        count_filter_tasks = len(filter_for_category_tasks)
        assert not count_filter_tasks, (
            "После удаления элементов по категории, в json не должно остаться "
            f"объектов категории {task.category}, а их сейчас {count_filter_tasks}."
        )

    @pytest.mark.skip
    def test_delete_task_for_invalid_category():
        return NotImplementedError

    @pytest.mark.skip
    def search_tasks_for_fields(
        self, repository: RepositoryTask, task: TaskSchema, task_update: TaskSchema
    ):
        pass
