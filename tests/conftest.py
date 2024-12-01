import pytest
from pathlib import Path

from task_tracker.repository import RepositoryTask
from task_tracker.repository import TaskSchema


@pytest.fixture
def repository(tmpdir: Path) -> RepositoryTask:
    json_path = Path(tmpdir / "test_task.json")
    return RepositoryTask(json_path)


@pytest.fixture
def task() -> TaskSchema:
    task_ = TaskSchema(
        id=1,
        title="Изучить основы FastAPI",
        description="Пройти документация по FastAPI",
        category="Обучение",
        due_date="2024-11-30",
        priority="Высокий",
        status=True,
    )
    return task_


@pytest.fixture
def task_update() -> TaskSchema:
    task_ = TaskSchema(
        id=1,
        title="Изучить основы FastAPI_update",
        description="Пройти документация по FastAPI_update",
        category="Update category",
        due_date="2024-01-13",
        priority="Низкий",
        status=False,
    )
    return task_
