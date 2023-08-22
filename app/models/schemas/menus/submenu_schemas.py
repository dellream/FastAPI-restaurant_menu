from typing import Optional

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: Optional[str] = None


class SubmenuSchema(SubmenuBase):
    ...


class SubmenuResponse(SubmenuSchema):
    id: str
    menu_id: str


class SubmenuCountResponse(SubmenuSchema):
    id: str
    dishes_count: int
