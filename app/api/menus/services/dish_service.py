from fastapi import BackgroundTasks, Depends

from app.db.cache import CacheRepository
from app.db.repositories.dish_repository import AsyncDishRepository
from app.models.domain.menus_models import Dish
from app.models.schemas.menus.dish_schemas import DishSchema


class AsyncDishService:
    """Сервисный репозиторий для блюда"""

    def __init__(self,
                 dish_repo: AsyncDishRepository = Depends(),
                 cache_repo: CacheRepository = Depends()) -> None:
        self.dish_repo = dish_repo
        self.cache_repo = cache_repo

    async def create_dish(self,
                          submenu_id: str,
                          dish: DishSchema,
                          background_tasks: BackgroundTasks) -> Dish:
        """
        Исправить

        Добавление нового блюда

        Создает в базе данных запись о новом блюде, создает фоновую задачу
        (чтобы пользователь не ждали кеширования запросов) на кеширование
        данного блюда и инвалидацию списка всех блюд
        """
        dish_info = await self.dish_repo.create_dish(submenu_id, dish)
        menu_id = await self.dish_repo.get_menu_id_by_submenu_id(submenu_id)
        background_tasks.add_task(
            self.cache_repo.create_new_dish_cache,
            dish_info=dish_info,
            submenu_id=submenu_id,
            menu_id=menu_id
        )
        return dish_info

    async def read_all_dishes(self,
                              menu_id: str,
                              submenu_id: str,
                              background_tasks: BackgroundTasks) -> list[Dish]:
        """
        Получение всех блюд

        Возвращает данные из кеша, если данные в кеше присутствуют.

        Если кеша нет, то совершает запрос в БД. Создает фоновую задачу
        на создание кеша для данного запроса
        """
        cache = await self.cache_repo.get_all_dishes_cache(
            menu_id=menu_id,
            submenu_id=submenu_id
        )
        if cache:
            return cache
        dish_list = await self.dish_repo.read_all_dishes(
            submenu_id=submenu_id
        )
        background_tasks.add_task(
            self.cache_repo.set_all_dishes_cache,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_list=dish_list
        )
        return dish_list

    async def read_dish(self,
                        menu_id: str,
                        submenu_id: str,
                        dish_id: str,
                        background_tasks: BackgroundTasks) -> Dish:
        """Получение блюд по id"""
        cache = await self.cache_repo.get_dish_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        )
        if cache:
            return cache
        dish_info = await self.dish_repo.read_dish(dish_id)
        background_tasks.add_task(
            self.cache_repo.set_dish_cache,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_info=dish_info
        )
        return dish_info

    async def update_dish(self,
                          menu_id: str,
                          submenu_id: str,
                          dish_id: str,
                          updated_dish: DishSchema,
                          background_tasks: BackgroundTasks) -> Dish:
        """Изменение блюд по id"""
        dish = await self.dish_repo.update_dish(dish_id, updated_dish)
        background_tasks.add_task(
            self.cache_repo.update_dish_cache,
            dish_info=dish,
            menu_id=menu_id,
            submenu_id=submenu_id
        )
        return dish

    async def delete_dish(self,
                          menu_id: str,
                          submenu_id: str,
                          dish_id: str,
                          background_tasks: BackgroundTasks) -> Dish:
        """Удаление блюд по id"""
        dish = await self.dish_repo.delete_dish(dish_id=dish_id)
        background_tasks.add_task(
            self.cache_repo.delete_dish_cache,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        )
        return dish
