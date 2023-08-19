from fastapi import Depends

from app.db.repositories.dish_repository import AsyncDishRepository
from app.models.schemas.menus.dish_schemas import DishSchema


class AsyncDishService:
    def __init__(self, dish_repo: AsyncDishRepository = Depends()):
        self.dish_repo = dish_repo

    async def create_dish(self, submenu_id: str, dish: DishSchema):
        return await self.dish_repo.create_dish(submenu_id, dish)

    async def read_all_dishes(self):
        return await self.dish_repo.read_all_dishes()

    async def read_dish(self, dish_id: str):
        dish = await self.dish_repo.read_dish(dish_id)
        return dish

    async def update_dish(self, dish_id: str, updated_dish: DishSchema):
        return await self.dish_repo.update_dish(dish_id, updated_dish)

    async def delete_dish(self, dish_id: str):
        return await self.dish_repo.delete_dish(dish_id)
