from fastapi import Depends, BackgroundTasks

from app.db.cache import CacheRepository
from app.db.repositories.submenu_repository import AsyncSubmenuRepository
from app.models.schemas.menus.submenu_schemas import SubmenuSchema


class AsyncSubmenuService:
    """Сервисный репозиторий для подменю"""

    def __init__(self,
                 submenu_repo: AsyncSubmenuRepository = Depends(),
                 cache_repo: CacheRepository = Depends()):
        self.submenu_repo = submenu_repo
        self.cache_repo = cache_repo

    async def create_submenu(self,
                             menu_id: str,
                             submenu: SubmenuSchema,
                             background_tasks: BackgroundTasks):
        """Добавление нового подменю"""
        created_submenu = await self.submenu_repo.create_submenu(menu_id, submenu)
        submenu_info = await self.submenu_repo.read_submenu(
            submenu_id=created_submenu.id
        )
        background_tasks.add_task(
            self.cache_repo.create_new_submenu_cache,
            submenu_info=submenu_info,
            menu_id=menu_id,
            submenu_id=submenu_info.id
        )
        return created_submenu

    async def read_all_submenus(self,
                                menu_id: str,
                                background_tasks: BackgroundTasks):
        """Получение всех подменю"""
        cache = await self.cache_repo.get_all_submenus_cache(menu_id=menu_id)
        if cache:
            return cache
        submenu_list = await self.submenu_repo.read_all_submenus(menu_id)
        background_tasks.add_task(
            self.cache_repo.set_all_submenus_cache,
            menu_id=menu_id,
            submenu_list=submenu_list
        )
        return submenu_list

    async def read_submenu(self,
                           menu_id: str,
                           submenu_id: str,
                           background_tasks: BackgroundTasks):
        """Получение подменю по id"""
        cache = await self.cache_repo.get_submenu_cache(menu_id, submenu_id)
        if cache:
            return cache
        submenu_info = await self.submenu_repo.read_submenu(submenu_id)
        background_tasks.add_task(
            self.cache_repo.set_submenu_cache,
            menu_id=menu_id,
            submenu_id=submenu_id,
            submenu_info=submenu_info
        )
        return submenu_info

    async def update_submenu(self,
                             menu_id: str,
                             submenu_id: str,
                             updated_submenu: SubmenuSchema,
                             background_tasks: BackgroundTasks):
        """Изменение подменю по id"""
        updated_submenu_info = await self.submenu_repo.update_submenu(
            submenu_id=submenu_id,
            updated_submenu=updated_submenu
        )
        submenu_info = await self.submenu_repo.read_submenu(
            submenu_id=submenu_id
        )
        background_tasks.add_task(
            self.cache_repo.update_submenu_cache,
            submenu_info=submenu_info,
            menu_id=menu_id,
            submenu_id=submenu_id
        )
        return updated_submenu_info

    async def delete_submenu(self,
                             menu_id: str,
                             submenu_id: str,
                             background_tasks: BackgroundTasks):
        """Удаление подменю по id"""
        submenu = await self.submenu_repo.delete_submenu(submenu_id=submenu_id)
        background_tasks.add_task(
            self.cache_repo.delete_submenu_cache,
            submenu_id=submenu_id,
            menu_id=menu_id
        )
        return submenu
