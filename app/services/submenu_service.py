from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.db.repositories.submenu_repository import SubmenuRepository
from app.models.schemas.menus.submenu_schemas import SubmenuSchema


class SubmenuService:
    def __init__(self, submenu_repo: SubmenuRepository):
        self.submenu_repo = submenu_repo

    def create_submenu(self, menu_id: str, submenu: SubmenuSchema):
        try:
            return self.submenu_repo.create_submenu(menu_id, submenu)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="submenu with this title already exists")

    def read_all_submenus(self):
        return self.submenu_repo.read_all_submenus()

    def read_submenu(self, submenu_id: str):
        submenu = self.submenu_repo.read_submenu(submenu_id)
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
        return submenu

    def update_submenu(self, submenu_id: str, updated_submenu: SubmenuSchema):
        return self.submenu_repo.update_submenu(submenu_id, updated_submenu)

    def delete_submenu(self, submenu_id: str):
        return self.submenu_repo.delete_submenu(submenu_id)
