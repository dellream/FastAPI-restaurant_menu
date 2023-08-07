from typing import List

from pydantic import BaseModel

from app.models.schemas.menus.submenu_schemas import SubmenuSchema


class MenuBase(BaseModel):
    title: str
    description: str = None


class MenuSchema(MenuBase):
    submenus: List[SubmenuSchema] = []

    class Config:
        from_attributes = True


class MenuResponse(MenuSchema):
    id: str


class MenuCountResponse(MenuResponse):
    submenus_count: int
    dishes_count: int
