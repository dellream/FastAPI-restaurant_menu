import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import distinct, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database_connect import get_async_session
from app.models.domain.menus_models import Dish, Menu, Submenu
from app.models.schemas.menus.menu_schemas import MenuSchema


class AsyncMenuRepository:
    """Репозиторий необходимых CRUD операций для модели Меню"""

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    # Необходимо доработать репозиторий на проверку существующего меню,
    # не должно быть два меню с одинаковым названием
    async def create_menu(self, menu):
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

    async def update_menu(self, menu_id: str, updated_menu: dict):
        """Изменение меню по id"""
        menu = await self.session.get(Menu, menu_id)

        if menu:
            # Изменим текущее меню на основе принятого измененного updated_menu
            updated_menu_model = MenuSchema(**updated_menu)  # Создаем экземпляр модели Pydantic
            updated_menu_dict = updated_menu_model.dict(exclude_unset=True)  # Преобразуем модель в словарь

            # Изменим текущее меню на основе принятого измененного updated_submenu
            for key, value in updated_menu_dict.items():
                setattr(menu, key, value)  # Меняем значение аттрибута menu по его имени key на значение value

            await self.session.commit()
            await self.session.refresh(menu)
            return menu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

    async def delete_menu(self, menu_id: str):
        """Удаление меню по id"""
        menu = await self.session.get(Menu, menu_id)
        if menu:
            await self.session.delete(menu)
            await self.session.commit()
            return menu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
