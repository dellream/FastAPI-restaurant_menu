import uuid
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct
from fastapi import HTTPException, status, Depends


from app.db.database_connect import get_db
from app.models.domain.menus_models import Menu, Submenu, Dish


class MenuRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    # def count_submenus(self, menu_id: int):
    #     return self.session.query(Submenu).filter_by(menu_id=menu_id).count()
    #
    # def count_dishes(self, menu_id: int):
    #     return self.session.query(Dish).join(Submenu).filter(Submenu.menu_id == menu_id).count()

    def create_menu(self, menu):
        menu_obj = Menu(title=menu.title,
                        description=menu.description)
        menu_obj.id = str(uuid.uuid4())
        self.session.add(menu_obj)
        self.session.commit()
        self.session.refresh(menu_obj)

        return menu_obj

    def read_all_menus(self) -> List[Menu]:
        query = self.session.execute(
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

    def read_menu(self, menu_id: str) -> Menu:
        query = self.session.execute(
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

        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

        return item

    def update_menu(self, menu_id: str, updated_menu: dict):
        menu = self.session.query(Menu).get(menu_id)

        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="menu not found")

        for key, value in updated_menu.dict(exclude_unset=True).items():
            setattr(menu, key, value)

        self.session.commit()
        self.session.refresh(menu)
        return menu

    def delete_menu(self, menu_id: str):
        menu = self.session.query(Menu).get(menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
        self.session.delete(menu)
        self.session.commit()
        return menu




