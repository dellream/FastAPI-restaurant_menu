"""
Модуль для работы с API, связанным с меню.

Этот модуль определяет маршруты FastAPI для создания, чтения, обновления и удаления меню.

Атрибуты:
    menu_router (APIRouter): Экземпляр APIRouter FastAPI для маршрутов, связанных с меню.
"""

from fastapi import APIRouter, BackgroundTasks, Depends
from starlette import status

from app.api.menus.services.menu_service import AsyncMenuService
from app.models.schemas.menus.menu_schemas import (
    MenuCountResponse,
    MenuResponse,
    MenuSchema,
)

menu_router = APIRouter(
    prefix='/api/v1/menus',
    tags=['Меню']
)


@menu_router.post('/',
                  response_model=MenuResponse,
                  status_code=status.HTTP_201_CREATED,
                  summary='Создать меню')
async def create_menus(menu: MenuSchema,
                       background_tasks: BackgroundTasks,
                       menu_service: AsyncMenuService = Depends()) -> MenuResponse:
    """Создает новое меню."""
    return await menu_service.create_menu(menu, background_tasks)


@menu_router.get('/',
                 response_model=list[MenuResponse],
                 summary='Получить список всех меню')
async def read_all_menus(background_tasks: BackgroundTasks,
                         menu_service: AsyncMenuService = Depends()) -> list[MenuResponse]:
    """Получает список всех меню."""
    return await menu_service.read_all_menus(background_tasks)


@menu_router.get('/{menu_id}/',
                 response_model=MenuCountResponse,
                 summary='Получить меню')
async def read_menu(menu_id: str,
                    background_tasks: BackgroundTasks,
                    menu_service: AsyncMenuService = Depends()) -> MenuCountResponse:
    """Получает определенное меню по ID"""
    return await menu_service.read_menu(menu_id, background_tasks)


@menu_router.patch('/{menu_id}/',
                   response_model=MenuResponse,
                   summary='Изменить меню')
async def update_menu(menu_id: str,
                      updated_menu: MenuSchema,
                      background_tasks: BackgroundTasks,
                      menu_service: AsyncMenuService = Depends()) -> MenuResponse:
    """Изменяет определенное меню по ID"""
    return await menu_service.update_menu(menu_id, updated_menu, background_tasks)


@menu_router.delete('/{menu_id}/',
                    response_model=MenuResponse,
                    summary='Удалить меню')
async def delete_menu(menu_id: str,
                      background_tasks: BackgroundTasks,
                      menu_service: AsyncMenuService = Depends()) -> MenuResponse:
    """Удаляет определенное меню по ID"""
    return await menu_service.delete_menu(menu_id, background_tasks)
