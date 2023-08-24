from fastapi import Depends, BackgroundTasks

from app.db.cache import CacheRepository
from app.db.repositories.dish_repository import AsyncDishRepository
from app.models.schemas.menus.dish_schemas import DishSchema


class AsyncDishService:
    """Сервисный репозиторий для блюда"""

    def __init__(self,
                 dish_repo: AsyncDishRepository = Depends(),
                 cache_repo: CacheRepository = Depends()):
        self.dish_repo = dish_repo
        self.cache_repo = cache_repo

    async def create_dish(self,
                          submenu_id: str,
                          dish: DishSchema,
                          background_tasks: BackgroundTasks):
        """
        Исправить

        Добавление нового блюда

        Создает в базе данных запись о новом блюде, создает фоновую задачу
        (чтобы пользователь не ждали кеширования запросов) на кеширование
        данного блюда и инвалидацию списка всех блюд

        :param submenu_id: Идентификатор подменю
        :param dish: Информация о блюде
        :param background_tasks: Фоновая задача
        :return: Информация о созданном блюде
        """
        dish_list = await self.dish_repo.create_dish(submenu_id, dish)
        menu_id = await self.dish_repo.get_menu_id_by_submenu_id(submenu_id)
        background_tasks.add_task(
            self.cache_repo.create_new_dish_cache,
            dish_list=dish_list,
            submenu_id=submenu_id,
            menu_id=menu_id
        )
        return dish_list

    async def read_all_dishes(self,
                              menu_id,
                              submenu_id,
                              background_tasks: BackgroundTasks):
        """
        Получение всех блюд

        Возвращает данные из кеша, если данные в кеше присутствуют.

        Если кеша нет, то совершает запрос в БД. Создает фоновую задачу
        на создание кеша для данного запроса

        :param menu_id: Идентификатор меню
        :param submenu_id: Идентификатор подменю
        :param background_tasks: Фоновая задача
        :return: Информацию обо всех блюдах
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
                        dish_id: str,
                        background_tasks: BackgroundTasks):
        """Получение блюд по id"""
        dish = await self.dish_repo.read_dish(dish_id)
        return dish

    async def update_dish(self,
                          dish_id: str,
                          updated_dish: DishSchema,
                          background_tasks: BackgroundTasks):
        """Изменение блюд по id"""
        return await self.dish_repo.update_dish(dish_id, updated_dish)

    async def delete_dish(self,
                          dish_id: str,
                          background_tasks: BackgroundTasks):
        """Удаление блюд по id"""
        return await self.dish_repo.delete_dish(dish_id)
