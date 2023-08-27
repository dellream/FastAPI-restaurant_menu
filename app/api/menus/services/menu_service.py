"""Сервисный слой для модели Меню"""
from fastapi import Depends, BackgroundTasks

from app.db.cache import CacheRepository
from app.db.repositories.menu_repository import AsyncMenuRepository
from app.models.schemas.menus.menu_schemas import MenuSchema


class AsyncMenuService:
    """Сервисный репозиторий для меню"""

    def __init__(self,
                 menu_repo: AsyncMenuRepository = Depends(),
                 cache_repo: CacheRepository = Depends()):
        self.menu_repo = menu_repo
        self.cache_repo = cache_repo

    async def create_menu(self,
                          menu: MenuSchema,
                          background_tasks: BackgroundTasks):
        """Добавление нового меню"""
        created_menu = await self.menu_repo.create_menu(menu)
        menu_info = await self.menu_repo.read_menu(menu_id=created_menu.id)
        background_tasks.add_task(
            self.cache_repo.create_new_menu_cache,
            menu_info=menu_info
        )
        return created_menu

    async def read_all_menus(self,
                             background_tasks: BackgroundTasks):
        """Получение всех меню"""
        cache = await self.cache_repo.get_all_menus_cache()
        if cache:
            return cache
        menu_list = await self.menu_repo.read_all_menus()
        background_tasks.add_task(
            self.cache_repo.set_all_menus_cache,
            menu_list
        )
        return menu_list

    async def read_menu(self,
                        menu_id: str,
                        background_tasks: BackgroundTasks):
        """Получение меню по id"""
        cache = await self.cache_repo.get_menu_cache(menu_id)
        if cache:
            return cache
        menu_info = await self.menu_repo.read_menu(menu_id)
        background_tasks.add_task(
            self.cache_repo.set_menu_cache,
            menu_info
        )
        return menu_info

    async def update_menu(self,
                          menu_id: str,
                          updated_menu: MenuSchema,
                          background_tasks: BackgroundTasks):
        """Изменение меню по id"""
        updated_menu_info = await self.menu_repo.update_menu(
            menu_id=menu_id,
            updated_menu=updated_menu
        )
        menu_info = await self.menu_repo.read_menu(menu_id)
        background_tasks.add_task(
            self.cache_repo.update_menu_cache,
            menu_info=menu_info,
            menu_id=menu_id
        )
        return updated_menu_info

    async def delete_menu(self,
                          menu_id: str,
                          background_tasks: BackgroundTasks):
        """Удаление меню по id"""
        deleted_menu = await self.menu_repo.delete_menu(menu_id)
        background_tasks.add_task(
            self.cache_repo.delete_menu_cache,
            menu_id=menu_id
        )
        return deleted_menu
