import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import distinct, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database_connect import get_async_session
from app.models.domain.menus_models import Dish, Menu, Submenu
from app.models.schemas.menus.menu_schemas import MenuSchema


class AsyncMenuRepository:
    """Репозиторий необходимых CRUD операций для модели Меню"""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session

    # Необходимо доработать репозиторий на проверку существующего меню,
    # не должно быть два меню с одинаковым названием
    async def create_menu(self, menu: MenuSchema) -> Menu:
        """Добавление нового меню"""
        try:
            menu_obj = Menu(title=menu.title, description=menu.description)
            menu_obj.id = str(uuid.uuid4())
            self.session.add(menu_obj)
            await self.session.commit()
            await self.session.refresh(menu_obj)
            return menu_obj
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Menu with this title is already exists')

    async def read_all_menus(self) -> list[Menu]:
        """Получение всех меню"""
        query = await self.session.execute(
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(Submenu.id).label('submenus_count'),
                func.count(Dish.id).label('dishes_count')
            )
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Menu.id)
        )
        return query.all()

    async def read_menu(self, menu_id: str) -> Menu:
        """Получение меню по id"""
        query = await self.session.execute(
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count')
            )
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .filter(Menu.id == menu_id)
            .group_by(Menu.id)
        )
        item: Menu = query.first()

        if item:
            return item
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

    async def update_menu(self, menu_id: str, updated_menu: MenuSchema) -> Menu:
        """Изменение меню по id"""
        current_menu = await self.session.get(Menu, menu_id)

        if current_menu:
            current_menu.title = updated_menu.title
            current_menu.description = updated_menu.description

            await self.session.merge(current_menu)
            await self.session.commit()
            await self.session.refresh(current_menu)
            return current_menu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

    async def delete_menu(self, menu_id: str) -> Menu:
        """Удаление меню по id"""
        menu = await self.session.get(Menu, menu_id)
        if menu:
            await self.session.delete(menu)
            await self.session.commit()
            return menu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

    async def get_full_restaurant_menu(self) -> list[Menu]:
        """Получение полного списка всех меню, соответствующих подменю и соответствующих блюд"""
        query = (await self.session.execute(
            # При выполнении select в рамках одного запроса сразу же будут выводиться соответствующие подменю и блюда
            select(Menu).options(selectinload(Menu.submenus).selectinload(Submenu.dishes))
        )).scalars().fetchall()
        return query
