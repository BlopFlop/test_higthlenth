from pathlib import Path

from task_tracker.task import Task


class JsonData:
    def __init__(self, base_dir: Path) -> None:
        self.path_json: Path = self._get_or_create(base_dir)

    def _get_or_create(self, path_file: Path) -> Path:
        if not path_file.is_file():
            with open(path_file, mode="w", encoding="utf-8"):
                pass
        return path_file

    def _change_file(data: list[str]) -> None:
        pass

    def _get_data(self) -> list[Task]:
        pass

    def search(self, **kwargs) -> list[Task]:
        pass

    def get(self, id: int = None, category: str = None) -> list[Task] | Task:
        pass

    def post(self, **kwargs) -> Task:
        pass

    def patch(self, **kwargs) -> Task:
        pass

    def delete(self, id: int = None, category: str = None) -> None:
        pass
