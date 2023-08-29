from pydantic import BaseModel


class MenuBase(BaseModel):
    """Базовая схема для основного меню."""

    title: str
    description: str | None


class MenuSchema(MenuBase):
    """Основная схема для работы с меню"""
    ...


class MenuResponse(MenuSchema):
    """Схема для получения ответа от эндпоинтов"""

    id: str | None


class MenuCountResponse(MenuResponse):
    """Схема для получения конкретного меню"""
    submenus_count: int
    dishes_count: int
