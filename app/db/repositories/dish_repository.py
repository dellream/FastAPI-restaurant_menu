import uuid
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct
from fastapi import HTTPException, status, Depends

from app.db.database_connect import get_db
from app.models.domain.menus_models import Menu, Submenu, Dish


class DishRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_dish(self, submenu_id: str, dish):
        dish_obj = Dish(title=dish.title,
                        description=dish.description,
                        submenu_id=submenu_id,
                        price=dish.price)
        dish_obj.id = str(uuid.uuid4())
        self.session.add(dish_obj)
        self.session.commit()
        self.session.refresh(dish_obj)

        return dish_obj

    def read_all_dishes(self) -> List[Dish]:
        query = self.session.execute(
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price,
                Dish.submenu_id,
            )
            .group_by(Dish.id)
        )

        return query.all()

    def read_dish(self, dish_id: str) -> Dish:
        query = self.session.execute(
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price
            )
            .filter(Dish.id == dish_id)
            .group_by(Dish.id)
        )

        item: Dish = query.first()

        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail='dish not found')

        return item

    def update_dish(self, dish_id: str, updated_dish: dict):
        dish = self.session.query(Dish).get(dish_id)

        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")

        for key, value in updated_dish.dict(exclude_unset=True).items():
            setattr(dish, key, value)

        self.session.commit()
        self.session.refresh(dish)
        return dish

    def delete_dish(self, dish_id: str):
        dish = self.session.query(Dish).get(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")
        self.session.delete(dish)
        self.session.commit()
        return dish
