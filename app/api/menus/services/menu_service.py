"""Сервисный слой для модели Меню"""
from fastapi import Depends

from app.db.repositories.menu_repository import AsyncMenuRepository
from app.models.schemas.menus.menu_schemas import MenuSchema


class AsyncMenuService:
    """Сервисный репозиторий для меню"""

    def __init__(self,
                 menu_repo: AsyncMenuRepository = Depends()):
        self.menu_repo = menu_repo

    async def create_menu(self, menu: MenuSchema):
        """Добавление нового меню"""
        return await self.menu_repo.create_menu(menu)

    async def read_all_menus(self):
        """Получение всех меню"""
        return await self.menu_repo.read_all_menus()

    async def read_menu(self, menu_id: str):
        """Получение меню по id"""
        return await self.menu_repo.read_menu(menu_id)

    async def update_menu(self,
                          menu_id: str,
                          updated_menu: MenuSchema):
        """Изменение меню по id"""
        return await self.menu_repo.update_menu(menu_id, updated_menu)

    async def delete_menu(self, menu_id: str):
        """Удаление меню по id"""
        return await self.menu_repo.delete_menu(menu_id)
