from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.db.repositories.menu_repository import MenuRepository
from app.models.schemas.menus.menu_schemas import MenuSchema


class MenuService:
    def __init__(self, menu_repo: MenuRepository):
        self.menu_repo = menu_repo

    def create_menu(self, menu: MenuSchema):
        try:
            return self.menu_repo.create_menu(menu)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Menu with this title already exists")

    def read_all_menus(self):
        return self.menu_repo.read_all_menus()

    def read_menu(self, menu_id: str):
        menu = self.menu_repo.read_menu(menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
        return menu

    def update_menu(self, menu_id: str, updated_menu: MenuSchema):
        return self.menu_repo.update_menu(menu_id, updated_menu)

    def delete_menu(self, menu_id: str):
        return self.menu_repo.delete_menu(menu_id)
