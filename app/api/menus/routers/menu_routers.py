from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List
from starlette import status

from app.models.schemas.menus.menu_schemas import (
    MenuSchema,
    MenuResponse,
    MenuCountResponse
)
from app.api.menus.services.menu_service import AsyncMenuService

menu_router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menus"]
)


@menu_router.post("/",
                  response_model=MenuResponse,
                  status_code=status.HTTP_201_CREATED)
async def create_menus(menu: MenuSchema,
                       background_tasks: BackgroundTasks,
                       menu_service: AsyncMenuService = Depends()):
    return await menu_service.create_menu(menu, background_tasks)


@menu_router.get("/",
                 response_model=List[MenuResponse])
async def read_all_menus(
        background_tasks: BackgroundTasks,
        menu_service: AsyncMenuService = Depends()
):
    return await menu_service.read_all_menus(background_tasks)


@menu_router.get("/{menu_id}/",
                 response_model=MenuCountResponse)
async def read_menu(menu_id: str,
                    background_tasks: BackgroundTasks,
                    menu_service: AsyncMenuService = Depends()):
    return await menu_service.read_menu(menu_id, background_tasks)


@menu_router.patch("/{menu_id}/",
                   response_model=MenuResponse)
async def update_menu(menu_id: str,
                      updated_menu: MenuSchema,
                      background_tasks: BackgroundTasks,
                      menu_service: AsyncMenuService = Depends()):
    return await menu_service.update_menu(menu_id, updated_menu, background_tasks)


@menu_router.delete("/{menu_id}/",
                    response_model=MenuResponse)
async def delete_menu(menu_id: str,
                      background_tasks: BackgroundTasks,
                      menu_service: AsyncMenuService = Depends()):
    return await menu_service.delete_menu(menu_id, background_tasks)
