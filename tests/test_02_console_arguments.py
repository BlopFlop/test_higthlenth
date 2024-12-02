import pytest
from pydantic_core import ValidationError

from task_tracker.repository import RepositoryTask
from task_tracker.schemas import TaskSchema
from tests.constants import JSON_INVALID_DATA, JSON_VALID_DATA


class TestConsoleArguments:
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

    @pytest.mark.skip
    def test_start_program() -> int:
        pass

    @pytest.mark.skip
    def test_create_json_file():
        pass

    @pytest.mark.skip
    def test_read_json_file_invalid_data():
        pass

    @pytest.mark.skip
    def test_create_task():
        pass

    @pytest.mark.skip
    def test_create_task_invalid_data():
        pass

    @pytest.mark.skip
    def test_get_all_tasks():
        pass

    @pytest.mark.skip
    def test_get_task_for_id():
        pass

    @pytest.mark.skip
    def test_get_task_for_invalid_id():
        pass

    @pytest.mark.skip
    def test_get_tasks_for_category():
        pass

    @pytest.mark.skip
    def test_get_task_for_invalid_category():
        pass

    @pytest.mark.skip
    def test_update_task():
        pass

    @pytest.mark.skip
    def test_update_task_invalid_data():
        pass

    @pytest.mark.skip
    def test_delete_task_for_id():
        pass

    @pytest.mark.skip
    def test_delete_task_for_invalid_id():
        pass

    @pytest.mark.skip
    def test_delete_task_for_category():
        pass

    @pytest.mark.skip
    def test_delete_task_for_invalid_category():
        pass

    @pytest.mark.skip
    def test_search_task_for_keyword_argument():
        pass
