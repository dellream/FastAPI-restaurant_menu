from pydantic import BaseModel


class SubmenuBase(BaseModel):
    """Базовая схема подменю"""
    title: str
    description: str | None = None


class SubmenuSchema(SubmenuBase):
    """Основная схема подменю"""
    ...


class SubmenuResponse(SubmenuSchema):
    """Схема для валидации данных после ответа эндпоинта для подменю"""
    id: str
    menu_id: str


class SubmenuCountResponse(SubmenuSchema):
    """Схема подменю для получения конкретного подменю"""
    id: str
    dishes_count: int
