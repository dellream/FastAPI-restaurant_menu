import uuid
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Depends

from app.db.database_connect import get_async_session
from app.models.domain.menus_models import Dish


class AsyncDishRepository:
    """Репозиторий необходимых CRUD операций для модели Блюда"""
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    # Доработать репозиторий, не должно быть блюд с одинаковыми названиями
    async def create_dish(self, submenu_id: str, dish):
        """Добавление нового блюда"""
        try:
            dish_obj = Dish(title=dish.title,
                            description=dish.description,
                            submenu_id=submenu_id,
                            price=dish.price)
            dish_obj.id = str(uuid.uuid4())
            self.session.add(dish_obj)
            await self.session.commit()
            await self.session.refresh(dish_obj)
            return dish_obj
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="dish with this title already exists")

    async def read_all_dishes(self, submenu_id) -> List[Dish]:
        """Получение всех блюд"""
        query = await self.session.execute(
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price,
                Dish.submenu_id,
            )
            .where(Dish.submenu_id == submenu_id)
            .group_by(Dish.id)
        )

        return query.all()

    async def read_dish(self, dish_id: str) -> Dish:
        """Получение блюда по id"""
        query = await self.session.execute(
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price
            )
            .filter(Dish.id == dish_id)
        )

        item: Dish = query.first()

        if item:
            return item
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail='dish not found')

    async def update_dish(self, dish_id: str, updated_dish: dict):
        """Изменение блюда по id"""
        dish = await self.session.get(Dish, dish_id)

        if dish:
            for key, value in updated_dish.dict(exclude_unset=True).items():
                setattr(dish, key, value)

            await self.session.commit()
            await self.session.refresh(dish)
            return dish
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")

    async def delete_dish(self, dish_id: str):
        """Удаление блюда по id"""
        dish = await self.session.get(Dish, dish_id)
        if dish:
            await self.session.delete(dish)
            await self.session.commit()
            return dish
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")
