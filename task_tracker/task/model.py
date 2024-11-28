from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import BaseModel, Field, field_validator


class PriorityTask(str, Enum):
    HIGH = "Высокий"
    MEDIUM = "Средний"
    LOW = "Низкий"


class Task(BaseModel):

    id: int = Field(
        ...,
        title="Уникальный айди задачи в json",
    )
    title: str = Field(
        ...,
        title="Тема",
    )
    description: str = Field(
        ...,
        title="Описание",
    )
    category: str = Field(
        ...,
        title="Категория",
    )
    due_date: date = Field(
        ...,
        title="Срок выполнения",
    )
    priority: PriorityTask = Field(
        ...,
        title="Приоритет задачи",
    )
    status: bool = Field(
        ...,
        title="Выполнена ли задача",
        description="",
    )

    class Config:
        schema_extra: dict[str, Any] = {
            "example": {
                "id": 1,
                "title": "Изучить основы FastAPI",
                "description": "Пройти документация по FastAPI",
                "category": "Обучение",
                "due_date": "2024-11-30",
                "priority": "Высокий",
                "status": True
            }
        }

    def __str__(self) -> str:
        return f"Task {self.title}"
