from typing import Optional

from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: str


class DishSchema(DishBase):
    ...


class DishResponse(DishSchema):
    id: str
