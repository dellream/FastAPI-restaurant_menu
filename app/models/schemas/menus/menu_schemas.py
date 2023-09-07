from pydantic import BaseModel

from app.models.schemas.menus.submenu_schemas import SubmenuFullResponse


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


class MenuFullResponse(MenuResponse):
    """Схема для получения всех меню с раскрытием всех подменю и блюд"""
    submenus: list[SubmenuFullResponse]

    class Config:
        extra = 'ignore'
        from_attributes = True
