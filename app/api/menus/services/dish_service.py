from fastapi import Depends

from app.db.repositories.dish_repository import AsyncDishRepository
from app.models.schemas.menus.dish_schemas import DishSchema


class AsyncDishService:
    """Сервисный репозиторий для блюда"""

    def __init__(self, dish_repo: AsyncDishRepository = Depends()):
        self.dish_repo = dish_repo

    async def create_dish(self,
                          submenu_id: str,
                          dish: DishSchema):
        """Добавление нового блюда"""
        return await self.dish_repo.create_dish(submenu_id, dish)

    async def read_all_dishes(self):
        """Получение всех блюд"""
        return await self.dish_repo.read_all_dishes()

    async def read_dish(self, dish_id: str):
        """Получение блюд по id"""
        dish = await self.dish_repo.read_dish(dish_id)
        return dish

    async def update_dish(self,
                          dish_id: str,
                          updated_dish: DishSchema):
        """Изменение блюд по id"""
        return await self.dish_repo.update_dish(dish_id, updated_dish)

    async def delete_dish(self, dish_id: str):
        """Удаление блюд по id"""
        return await self.dish_repo.delete_dish(dish_id)
