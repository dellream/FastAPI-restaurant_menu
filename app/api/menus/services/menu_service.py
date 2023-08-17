from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.db.repositories.menu_repository import AsyncMenuRepository
from app.models.schemas.menus.menu_schemas import MenuSchema


class AsyncMenuService:
    def __init__(self, menu_repo: AsyncMenuRepository):
        self.menu_repo = menu_repo

    async def create_menu(self, menu: MenuSchema):
        try:
            return await self.menu_repo.create_menu(menu)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Menu with this title already exists")

    async def read_all_menus(self):
        return await self.menu_repo.read_all_menus()

    async def read_menu(self, menu_id: str):
        menu = await self.menu_repo.read_menu(menu_id)
        if menu:
            return menu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    async def update_menu(self, menu_id: str, updated_menu: MenuSchema):
        return await self.menu_repo.update_menu(menu_id, updated_menu)

    async def delete_menu(self, menu_id: str):
        return await self.menu_repo.delete_menu(menu_id)
