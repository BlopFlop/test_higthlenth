from datetime import date
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class PriorityTask(str, Enum):
    HIGH = "Высокий"
    MEDIUM = "Средний"
    LOW = "Низкий"


class TaskSchema(BaseModel):
    """Pydantic schema for Task."""

    id: int = Field(
        title="Уникальный айди задачи в json",
    )
    title: str = Field(
        title="Тема",
    )
    description: str = Field(
        title="Описание",
    )
    category: str = Field(
        title="Категория",
    )
    due_date: date = Field(
        title="Срок выполнения",
    )
    priority: PriorityTask = Field(
        title="Приоритет задачи",
    )
    status: bool = Field(
        title="Выполнена ли задача",
    )

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "id": 1,
                "title": "Изучить основы FastAPI",
                "description": "Пройти документация по FastAPI",
                "category": "Обучение",
                "due_date": "2024-11-30",
                "priority": "Высокий",
                "status": True,
            }
        }

    def __str__(self) -> str:
        return f"Task {self.title}"


class TaskSchemaUpdate(BaseModel):
    """Pydantic schema for Task."""

    title: Optional[str] = Field(
        None,
        title="Тема",
    )
    description: Optional[str] = Field(
        None,
        title="Описание",
    )
    category: Optional[str] = Field(
        None,
        title="Категория",
    )
    due_date: Optional[date] = Field(
        None,
        title="Срок выполнения",
    )
    priority: Optional[PriorityTask] = Field(
        None,
        title="Приоритет задачи",
    )
    status: Optional[bool] = Field(
        None,
        title="Выполнена ли задача",
    )

    def __str__(self) -> str:
        return f"Task {self.title}"
