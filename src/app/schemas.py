from typing import List, Optional

from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float


class DishCreate(DishBase):
    pass


class DishSchema(DishBase):
    class Config:
        from_attributes = True


class SubmenuBase(BaseModel):
    title: str
    description: Optional[str] = None


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuSchema(SubmenuBase):
    dishes: List[DishSchema] = []

    class Config:
        from_attributes = True


class MenuBase(BaseModel):
    title: str
    description: str = None


class MenuCreate(MenuBase):
    pass


class MenuSchema(MenuBase):
    submenus: List[SubmenuSchema] = []

    class Config:
        from_attributes = True
