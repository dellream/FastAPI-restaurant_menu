import uuid
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct
from fastapi import HTTPException, status, Depends

from app.db.database_connect import get_db
from app.models.domain.menus_models import Menu, Submenu, Dish


class SubmenuRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_submenu(self, menu_id: str, submenu):
        submenu_obj = Submenu(title=submenu.title,
                              description=submenu.description,
                              menu_id=menu_id)
        submenu_obj.id = str(uuid.uuid4())
        self.session.add(submenu_obj)
        self.session.commit()
        self.session.refresh(submenu_obj)

        return submenu_obj

    def read_all_submenus(self) -> List[Submenu]:
        query = self.session.execute(
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                Submenu.menu_id,
                func.count(Dish.id).label('dishes_count')
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Submenu.id)
        )

        return query.all()

    def read_submenu(self, submenu_id: str) -> Submenu:
        query = self.session.execute(
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label('dishes_count')
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .filter(Submenu.id == submenu_id)
            .group_by(Submenu.id)
        )

        item: Submenu = query.first()

        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')

        return item

    def update_submenu(self, submenu_id: str, updated_submenu: dict):
        submenu = self.session.query(Submenu).get(submenu_id)

        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="submenu not found")

        for key, value in updated_submenu.dict(exclude_unset=True).items():
            setattr(submenu, key, value)

        self.session.commit()
        self.session.refresh(submenu)
        return submenu

    def delete_submenu(self, submenu_id: str):
        submenu = self.session.query(Submenu).get(submenu_id)
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
        self.session.delete(submenu)
        self.session.commit()
        return submenu
