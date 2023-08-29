import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import distinct, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database_connect import get_async_session
from app.models.domain.menus_models import Dish, Submenu
from app.models.schemas.menus.submenu_schemas import SubmenuSchema


class AsyncSubmenuRepository:
    """Репозиторий необходимых CRUD операций для модели Подменю"""

    def __init__(self,
                 session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session

    # Доработать репозиторий, подменю с одинаковыми названиями не должно быть
    async def create_submenu(self, menu_id: str, submenu: SubmenuSchema) -> Submenu:
        """Добавление нового подменю"""
        try:
            submenu_obj = Submenu(title=submenu.title,
                                  description=submenu.description,
                                  menu_id=menu_id)
            submenu_obj.id = str(uuid.uuid4())
            self.session.add(submenu_obj)  # Добавляем сформированный объект в сессию
            await self.session.commit()
            await self.session.refresh(submenu_obj)
            return submenu_obj
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='submenu with this title already exists')

    async def read_all_submenus(self, menu_id: str) -> list[Submenu]:
        """Получение всех подменю"""
        query = await self.session.execute(
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                Submenu.menu_id,
                func.count(Dish.id).label('dishes_count')
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(Submenu.menu_id == menu_id)
            .group_by(Submenu.id)
        )

        return query.all()

    async def read_submenu(self,
                           submenu_id: str) -> Submenu:
        """Получение подменю по id"""
        query = await self.session.execute(
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label('dishes_count')
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(Submenu.id == submenu_id)
            .group_by(Submenu.id)
        )

        item: Submenu = query.first()

        if item:
            return item
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')

    async def update_submenu(self,
                             submenu_id: str,
                             updated_submenu: SubmenuSchema) -> Submenu:
        """Изменение подменю по id"""
        current_submenu = await self.session.get(Submenu, submenu_id)

        if current_submenu:
            current_submenu.title = updated_submenu.title
            current_submenu.description = updated_submenu.description

            await self.session.merge(current_submenu)
            await self.session.commit()
            await self.session.refresh(current_submenu)
            return current_submenu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')

    async def delete_submenu(self, submenu_id: str) -> Submenu:
        """Удаление подменю по id"""
        submenu = await self.session.get(Submenu, submenu_id)
        if submenu:
            await self.session.delete(submenu)
            await self.session.commit()
            return submenu
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')
