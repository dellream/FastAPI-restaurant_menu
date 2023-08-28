from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: str


class DishSchema(DishBase):
    ...


class DishResponse(DishSchema):
    id: str
