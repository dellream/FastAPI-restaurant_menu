from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from starlette import status

from app.db.database_connect import get_async_session
from app.db.repositories.menu_repository import AsyncMenuRepository
from app.models.schemas.menus.menu_schemas import MenuSchema, MenuResponse, MenuCountResponse
from app.api.menus.services.menu_service import AsyncMenuService

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menus"]
)


def get_menu_service(session: Session = Depends(get_async_session)) -> AsyncMenuService:
    menu_repo = AsyncMenuRepository(session)
    return AsyncMenuService(menu_repo)


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menus(menu: MenuSchema,
                       menu_service: AsyncMenuService = Depends(get_menu_service)):
    return await menu_service.create_menu(menu)


@router.get("/", response_model=List[MenuResponse])
async def read_all_menus(menu_service: AsyncMenuService = Depends(get_menu_service)):
    return await menu_service.read_all_menus()


@router.get("/{menu_id}/", response_model=MenuCountResponse)
async def read_menu(menu_id: str,
                    menu_service: AsyncMenuService = Depends(get_menu_service)):
    return await menu_service.read_menu(menu_id)


@router.patch("/{menu_id}/", response_model=MenuResponse)
async def update_menu(menu_id: str,
                      updated_menu: MenuSchema,
                      menu_service: AsyncMenuService = Depends(get_menu_service)):
    return await menu_service.update_menu(menu_id, updated_menu)


@router.delete("/{menu_id}/", response_model=MenuResponse)
async def delete_menu(menu_id: str,
                      menu_service: AsyncMenuService = Depends(get_menu_service)):
    return await menu_service.delete_menu(menu_id)
