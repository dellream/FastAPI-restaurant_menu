import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database_connect import get_async_session
from app.models.domain.menus_models import Dish, Submenu
from app.models.schemas.menus.dish_schemas import DishSchema


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
                                detail='dish with this title already exists')

    async def read_all_dishes(self, submenu_id) -> list[Dish]:
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

    async def update_dish(self, dish_id: str, updated_dish: DishSchema) -> Dish:
        """Изменение блюда по id"""
        # Находим текущее блюдо в бд
        current_dish = await self.session.get(Dish, dish_id)

        if current_dish:
            current_dish.title = updated_dish.title
            current_dish.description = updated_dish.description
            current_dish.price = updated_dish.price

            await self.session.merge(current_dish)
            await self.session.commit()
            await self.session.refresh(current_dish)
            return current_dish
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')

    async def delete_dish(self, dish_id: str):
        """Удаление блюда по id"""
        dish = await self.session.get(Dish, dish_id)
        if dish:
            await self.session.delete(dish)
            await self.session.commit()
            return dish
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')

    async def get_menu_id_by_submenu_id(self,
                                        submenu_id):
        """
        Получение menu_id по идентификатору подменю

        :param submenu_id: ID подменю
        :return: Возвращает menu_id, в котором хранится блюдо
        """
        query = await self.session.execute(
            select(Submenu.menu_id)
            .select_from(Dish)
            .join(Submenu, Dish.submenu_id == Submenu.id)
            .where(Dish.submenu_id == submenu_id)
            .limit(1)
        )

        # Получаем значение из первой колонки первой строки
        menu_id = query.scalar()

        if menu_id:
            return menu_id
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail='Номер меню у данного блюда не найден')
