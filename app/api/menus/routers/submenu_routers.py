"""
Модуль для работы с API, связанным с подменю.

Этот модуль определяет маршруты FastAPI для создания, чтения, обновления и удаления подменю.

Атрибуты:
    submenu_router (APIRouter): Экземпляр APIRouter FastAPI для маршрутов, связанных с меню.
"""

from fastapi import APIRouter, BackgroundTasks, Depends
from starlette import status

from app.api.menus.services.submenu_service import AsyncSubmenuService
from app.models.schemas.menus.submenu_schemas import (
    SubmenuCountResponse,
    SubmenuResponse,
    SubmenuSchema,
)

submenu_router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['Подменю']
)


@submenu_router.post('/',
                     response_model=SubmenuResponse,
                     status_code=status.HTTP_201_CREATED,
                     summary='Создать подменю в основном меню')
async def create_submenus(submenu: SubmenuSchema,
                          menu_id: str,
                          background_tasks: BackgroundTasks,
                          submenu_service: AsyncSubmenuService = Depends()) -> SubmenuResponse:
    """Создает новое подменю."""
    return await submenu_service.create_submenu(
        menu_id=menu_id,
        submenu=submenu,
        background_tasks=background_tasks
    )


@submenu_router.get('/',
                    response_model=list[SubmenuResponse],
                    summary='Получить список подменю из меню')
async def read_all_submenus(menu_id: str,
                            background_tasks: BackgroundTasks,
                            submenu_service: AsyncSubmenuService = Depends()) -> list[SubmenuResponse]:
    """Получает список всех подменю, хранящихся в одном конкретном меню."""
    return await submenu_service.read_all_submenus(
        menu_id=menu_id,
        background_tasks=background_tasks
    )


@submenu_router.get('/{submenu_id}/',
                    response_model=SubmenuCountResponse,
                    summary='Получить подменю')
async def read_submenu(menu_id: str,
                       submenu_id: str,
                       background_tasks: BackgroundTasks,
                       submenu_service: AsyncSubmenuService = Depends()) -> SubmenuCountResponse:
    """Получает конкретное подменю, хранящееся в конкретном меню"""
    return await submenu_service.read_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks
    )


@submenu_router.patch('/{submenu_id}/',
                      response_model=SubmenuResponse,
                      summary='Изменить подменю')
async def update_submenu(menu_id: str,
                         submenu_id: str,
                         background_tasks: BackgroundTasks,
                         updated_submenu: SubmenuSchema,
                         submenu_service: AsyncSubmenuService = Depends()) -> SubmenuResponse:
    """Изменяет конкретное подменю в конкретном основном меню"""
    return await submenu_service.update_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        updated_submenu=updated_submenu,
        background_tasks=background_tasks
    )


@submenu_router.delete('/{submenu_id}/',
                       response_model=SubmenuResponse,
                       summary='Удалить подменю')
async def delete_submenu(menu_id: str,
                         submenu_id: str,
                         background_tasks: BackgroundTasks,
                         submenu_service: AsyncSubmenuService = Depends()) -> SubmenuResponse:
    """Удаляет конкретное подменю из конкретного основного меню"""
    return await submenu_service.delete_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks
    )
