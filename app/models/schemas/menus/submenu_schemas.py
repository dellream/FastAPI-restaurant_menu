from typing import List, Optional

from pydantic import BaseModel

from app.models.schemas.menus.dish_schemas import DishSchema


class SubmenuBase(BaseModel):
    title: str
    description: Optional[str] = None


class SubmenuSchema(SubmenuBase):
    dishes: List[DishSchema] = []

    class Config:
        from_attributes = True


class SubmenuResponse(SubmenuSchema):
    id: str


class SubmenuCountResponse(SubmenuResponse):
    dishes_count: int
