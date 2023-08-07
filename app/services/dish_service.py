from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.db.repositories.dish_repository import DishRepository
from app.models.schemas.menus.dish_schemas import DishSchema


class DishService:
    def __init__(self, dish_repo: DishRepository):
        self.dish_repo = dish_repo

    def create_dish(self, submenu_id: str, dish: DishSchema):
        try:
            return self.dish_repo.create_dish(submenu_id, dish)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="dish with this title already exists")

    def read_all_dishes(self):
        return self.dish_repo.read_all_dishes()

    def read_dish(self, dish_id: str):
        dish = self.dish_repo.read_dish(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")
        return dish

    def update_dish(self, dish_id: str, updated_dish: DishSchema):
        return self.dish_repo.update_dish(dish_id, updated_dish)

    def delete_dish(self, dish_id: str):
        return self.dish_repo.delete_dish(dish_id)
