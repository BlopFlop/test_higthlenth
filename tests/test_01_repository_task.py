import pytest
from pydantic_core import ValidationError

from task_tracker.repository import RepositoryTask
from task_tracker.schemas import TaskSchema
from tests.constants import JSON_INVALID_DATA, JSON_VALID_DATA


class TestRepository:
    """Test class for RepositoryTask.
    It is testing CRUD features for Task objects."""

    invalid_id = 999
    invalid_type_title = invalid_id
    invalid_type_description = invalid_id
    invalid_type_category = invalid_id
    invalid_category = "Такой категории не существует"
    invalid_type_due_date = invalid_id
    invalid_type_priority = invalid_id
    invalid_priority = "Такой приоретизации не существует"
    invalid_type_status = invalid_id

    def create_element_in_json(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ) -> int:
        count_item = 20
        count_item_other_category = 80

        task_data = task.model_dump()
        task_data.pop("id")
        for _ in range(count_item):
            repository.create(**task_data)

        task_update_data = task_update.model_dump()
        task_update_data.pop("id")
        for _ in range(count_item_other_category):
            repository.create(**task_update_data)

        return count_item + count_item_other_category

    def test_create_json_file(self, repository: RepositoryTask):
        path_json = repository.path_json
        assert repository.path_json.is_file(), (
            f"После инициализации класса {RepositoryTask.__name__}, "
            f"должен появиться json файл по пути {path_json}."
        )

    def test_read_json_file_data(self):
        json_file = RepositoryTask(JSON_VALID_DATA)
        count_elements = len(json_file.get_all())
        count_elements_confirm = 6
        assert count_elements == count_elements_confirm, (
            "После чтения валидного файла, результатом должен быть список "
            f"из {count_elements_confirm} объектов, а сейчас {count_elements}."
        )

    def test_read_json_file_invalid_data(self):
        with pytest.raises(ValueError) as ex:
            RepositoryTask(JSON_INVALID_DATA)
            assert ex, (
                "После чтения файла с невалидными данными должна появиться"
                f" ошибка {ValueError.__name__}."
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

    def test_create_task_invalid_data(self, repository: RepositoryTask):
        invalid_data = dict(
            category=self.invalid_type_category,
            description=self.invalid_type_description,
            due_date=self.invalid_type_due_date,
            priority=self.invalid_type_priority,
            status=self.invalid_type_status,
            title=self.invalid_type_title,
        )
        with pytest.raises(ValidationError) as ex:
            repository.create(**invalid_data)
            assert ex, (
                "При передаче невалидных данных для создания должна"
                f" возникнуть ошибка {ValidationError.__name__}."
            )

    def test_get_all_task(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        count_item = self.create_element_in_json(repository, task, task_update)

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
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        self.create_element_in_json(repository, task, task_update)

        get_task = repository.get(obj_id=task.id)
        assert isinstance(get_task, TaskSchema), (
            "При получении элемента по айди, должен "
            f"вернуться единственный элемент с типом {TaskSchema.__name__}"
        )
        assert task.model_dump() == get_task.model_dump(), (
            "Все поля и значения из полученной модели по айди, и"
            "поля из первоначальной модели должны быть равны."
        )

    def test_get_task_for_invalid_id(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        self.create_element_in_json(repository, task, task_update)
        with pytest.raises(ValueError) as ex:
            repository.get(obj_id=self.invalid_id)
            assert ex, (
                "При передаче невалидных данных для создания должна"
                f" возникнуть ошибка {ValueError.__name__}."
            )

    def test_get_tasks_for_category(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        count_item = 20
        self.create_element_in_json(repository, task, task_update)

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

    def test_get_task_for_invalid_category(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        self.create_element_in_json(repository, task, task_update)
        with pytest.raises(ValueError) as ex:
            repository.get(category=self.invalid_category)
            assert ex, (
                "При получении элемента по несуществующей категори, должна "
                f"возникнуть ошибка {ValueError.__name__}."
            )

    def test_update_task(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        self.create_element_in_json(repository, task, task_update)

        task_data = task.model_dump()
        task_data.pop("id")
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

    def test_update_task_invalid_data(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        invalid_data = dict(
            category=self.invalid_type_category,
            description=self.invalid_type_description,
            due_date=self.invalid_type_due_date,
            priority=self.invalid_type_priority,
            status=self.invalid_type_status,
            title=self.invalid_type_title,
        )
        self.create_element_in_json(repository, task, task_update)
        with pytest.raises(ValidationError) as ex:
            repository.update(obj_id=task.id, **invalid_data)
            assert ex, (
                "При получении элемента по несуществующей категори, должна "
                f"возникнуть ошибка {ValidationError.__name__}."
            )

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

    def test_delete_task_for_invalid_id(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        self.create_element_in_json(repository, task, task_update)
        with pytest.raises(ValueError) as ex:
            repository.remove(obj_id=self.invalid_id)
            assert ex, (
                "При удалении элемента по несуществующему id, должна "
                f"возникнуть ошибка {ValueError.__name__}."
            )

    def test_delete_task_for_category(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        self.create_element_in_json(repository, task, task_update)
        repository.remove(category=task.category)

        all_tasks = repository.get_all()
        filter_for_category_tasks = list(
            filter(lambda task_: task_.category == task.category, all_tasks)
        )
        count_filter_tasks = len(filter_for_category_tasks)
        assert not count_filter_tasks, (
            "После удаления элементов по категории, в json не должно остаться "
            f"объектов категории {task.category}, "
            f"а их сейчас {count_filter_tasks}."
        )

    def test_delete_task_for_invalid_category(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        self.create_element_in_json(repository, task, task_update)
        with pytest.raises(ValueError) as ex:
            repository.remove(category=self.invalid_category)
            assert ex, (
                "При удалении элементов по несуществующей категории, должна "
                f"возникнуть ошибка {ValueError.__name__}."
            )

    def test_search_task_for_keyword_argument(
        self,
        repository: RepositoryTask,
        task: TaskSchema,
        task_update: TaskSchema,
    ):
        self.create_element_in_json(repository, task, task_update)

        for field in task.model_fields_set:
            task_search = repository.get_obj_for_field_arg(
                field=field, arg=getattr(task, field), many=True
            )
            len_task_search = len(task_search)
            assert len_task_search > 0, (
                f"Поиск сущестующих элементов по полю {field}, "
                "должен дать список с элементами, сейчас он пуст."
            )
            filter_task_search = list(
                filter(
                    lambda task_: getattr(task_, field)
                    == getattr(task, field),
                    task_search,
                )
            )
            len_filter_task_search = len(filter_task_search)
            assert len_filter_task_search == len_task_search, (
                f"Значения поля {field} у всех найденных "
                "элементов должны быть равны."
            )
