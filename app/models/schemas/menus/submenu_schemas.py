from typing import Optional

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: Optional[str] = None


class SubmenuSchema(SubmenuBase):
    ...


class SubmenuResponse(SubmenuSchema):
    id: str


class SubmenuCountResponse(SubmenuResponse):
    dishes_count: int
