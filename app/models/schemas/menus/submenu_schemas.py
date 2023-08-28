from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str | None = None


class SubmenuSchema(SubmenuBase):
    ...


class SubmenuResponse(SubmenuSchema):
    id: str
    menu_id: str


class SubmenuCountResponse(SubmenuSchema):
    id: str
    dishes_count: int
