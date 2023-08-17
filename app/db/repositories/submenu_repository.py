import uuid
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct
from fastapi import HTTPException, status, Depends

from app.db.database_connect import get_async_session
from app.models.domain.menus_models import Submenu, Dish


class AsyncSubmenuRepository:
    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def create_submenu(self, menu_id: str, submenu):
        submenu_obj = Submenu(title=submenu.title,
                              description=submenu.description,
                              menu_id=menu_id)
        submenu_obj.id = str(uuid.uuid4())
        self.session.add(submenu_obj)  # Добавляем сформированный объект в сессию
        await self.session.commit()
        await self.session.refresh(submenu_obj)
        return submenu_obj

    async def read_all_submenus(self) -> List[Submenu]:
        query = await self.session.execute(
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

    async def read_submenu(self, submenu_id: str) -> Submenu:
        query = await self.session.execute(
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

        if item:
            return item
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')

    async def update_submenu(self, submenu_id: str, updated_submenu: dict):
        submenu = await self.session.get(Submenu, submenu_id)

        if submenu:
            # Изменим текущее меню на основе принятого измененного updated_submenu
            for key, value in updated_submenu.dict(exclude_unset=True).items():
                setattr(submenu, key, value)  # Меняем значение аттрибута menu по его имени key на значение value

            await self.session.commit()
            await self.session.refresh(submenu)
            return submenu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="submenu not found")

    async def delete_submenu(self, submenu_id: str):
        submenu = await self.session.get(Submenu, submenu_id)
        if submenu:
            await self.session.delete(submenu)
            await self.session.commit()
            return submenu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

