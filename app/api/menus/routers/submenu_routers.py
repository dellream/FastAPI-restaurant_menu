from fastapi import APIRouter, Depends
from typing import List
from starlette import status

from app.models.schemas.menus.submenu_schemas import (
    SubmenuResponse,
    SubmenuSchema,
    SubmenuCountResponse
)
from app.api.menus.services.submenu_service import AsyncSubmenuService

submenu_router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["Submenus"]
)


@submenu_router.post("/",
                     response_model=SubmenuResponse,
                     status_code=status.HTTP_201_CREATED)
async def create_submenus(submenu: SubmenuSchema,
                          menu_id: str,
                          submenu_service: AsyncSubmenuService = Depends()):
    return await submenu_service.create_submenu(menu_id, submenu)


@submenu_router.get("/",
                    response_model=List[SubmenuResponse])
async def read_all_submenus(menu_id: str,
                            submenu_service: AsyncSubmenuService = Depends()):
    return await submenu_service.read_all_submenus(menu_id)


@submenu_router.get("/{submenu_id}/",
                    response_model=SubmenuCountResponse)
async def read_submenu(submenu_id: str,
                       submenu_service: AsyncSubmenuService = Depends()):
    return await submenu_service.read_submenu(submenu_id)


@submenu_router.patch("/{submenu_id}/",
                      response_model=SubmenuResponse)
async def update_submenu(submenu_id: str,
                         updated_submenu: SubmenuSchema,
                         submenu_service: AsyncSubmenuService = Depends()):
    return await submenu_service.update_submenu(submenu_id, updated_submenu)


@submenu_router.delete("/{submenu_id}/",
                       response_model=SubmenuResponse)
async def delete_submenu(submenu_id: str,
                         submenu_service: AsyncSubmenuService = Depends()):
    return await submenu_service.delete_submenu(submenu_id)
