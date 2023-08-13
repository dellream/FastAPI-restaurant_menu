from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str = None


class MenuSchema(MenuBase):
    ...


class MenuResponse(MenuSchema):
    id: str


class MenuCountResponse(MenuResponse):
    submenus_count: int
    dishes_count: int
