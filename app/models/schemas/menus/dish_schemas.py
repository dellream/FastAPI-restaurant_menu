from pydantic import BaseModel


class DishBase(BaseModel):
    """Базовая схема блюда"""
    title: str
    description: str | None = None
    price: str


class DishSchema(DishBase):
    """Основная схема блюда"""
    id: str | None = None


class DishResponse(DishSchema):
    """Схема для валидации данных после ответа от эндпоинта"""
    id: str


class DishFullResponse(DishResponse):
    """Схема для получения всех меню с раскрытием всех подменю и блюд"""

    class Config:
        extra = 'ignore'
        from_attributes = True
