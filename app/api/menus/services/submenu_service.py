from fastapi import Depends

from app.db.repositories.submenu_repository import AsyncSubmenuRepository
from app.models.schemas.menus.submenu_schemas import SubmenuSchema


class AsyncSubmenuService:
    def __init__(self,
                 submenu_repo: AsyncSubmenuRepository = Depends()):
        self.submenu_repo = submenu_repo

    async def create_submenu(self,
                             menu_id: str,
                             submenu: SubmenuSchema):
        return await self.submenu_repo.create_submenu(menu_id, submenu)

    async def read_all_submenus(self):
        return await self.submenu_repo.read_all_submenus()

    async def read_submenu(self,
                           submenu_id: str):
        submenu = await self.submenu_repo.read_submenu(submenu_id)
        return submenu

    async def update_submenu(self,
                             submenu_id: str,
                             updated_submenu: SubmenuSchema):
        return await self.submenu_repo.update_submenu(submenu_id, updated_submenu)

    async def delete_submenu(self, submenu_id: str):
        return await self.submenu_repo.delete_submenu(submenu_id)
