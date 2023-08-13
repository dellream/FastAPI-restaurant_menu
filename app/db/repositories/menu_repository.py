import uuid
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct
from fastapi import HTTPException, status, Depends

from app.db.database_connect import get_async_session
from app.models.domain.menus_models import Menu, Submenu, Dish


class AsyncMenuRepository:
    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def create_menu(self, menu):
        menu_obj = Menu(title=menu.title, description=menu.description)
        menu_obj.id = str(uuid.uuid4())
        self.session.add(menu_obj)
        await self.session.commit()
        await self.session.refresh(menu_obj)
        return menu_obj

    async def read_all_menus(self) -> List[Menu]:
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
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

    async def update_menu(self, menu_id: str, updated_menu: dict):
        menu = await self.session.get(Menu, menu_id)

        if menu:
            # Изменим текущее меню на основе принятого измененного updated_menu
            for key, value in updated_menu.dict(exclude_unset=True).items():
                setattr(menu, key, value)  # Меняем значение аттрибута menu по его имени key на значение value

            await self.session.commit()
            await self.session.refresh(menu)
            return menu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    async def delete_menu(self, menu_id: str):
        menu = await self.session.get(Menu, menu_id)
        if menu:
            await self.session.delete(menu)
            await self.session.commit()
            return menu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
