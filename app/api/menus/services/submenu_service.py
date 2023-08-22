from fastapi import Depends

from app.db.repositories.submenu_repository import AsyncSubmenuRepository
from app.models.schemas.menus.submenu_schemas import SubmenuSchema


class AsyncSubmenuService:
    """Сервисный репозиторий для подменю"""

    def __init__(self,
                 submenu_repo: AsyncSubmenuRepository = Depends()):
        self.submenu_repo = submenu_repo

    async def create_submenu(self,
                             menu_id: str,
                             submenu: SubmenuSchema):
        """Добавление нового подменю"""
        return await self.submenu_repo.create_submenu(menu_id, submenu)

    async def read_all_submenus(self,
                                menu_id):
        """Получение всех подменю"""
        return await self.submenu_repo.read_all_submenus(menu_id)

    async def read_submenu(self,
                           submenu_id: str):
        """Получение подменю по id"""
        submenu = await self.submenu_repo.read_submenu(submenu_id)
        return submenu

    async def update_submenu(self,
                             submenu_id: str,
                             updated_submenu: SubmenuSchema):
        """Изменение подменю по id"""
        return await self.submenu_repo.update_submenu(submenu_id, updated_submenu)

    async def delete_submenu(self, submenu_id: str):
        """Удаление подменю по id"""
        return await self.submenu_repo.delete_submenu(submenu_id)
