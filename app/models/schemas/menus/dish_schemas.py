from pydantic import BaseModel


class DishBase(BaseModel):
    """Базовая схема блюда"""
    title: str
    description: str | None = None
    price: str


class DishSchema(DishBase):
    """Основная схема блюда"""
    ...


class DishResponse(DishSchema):
    """Схема для валидации данных после ответа от эндпоинта"""
    id: str
