from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from starlette import status

from app.db.database_connect import get_db
from app.db.repositories.menu_repository import MenuRepository
from app.models.schemas.menus.menu_schemas import MenuSchema, MenuResponse, MenuCountResponse
from app.services.menu_service import MenuService

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menus"]
)


def get_menu_service(session: Session = Depends(get_db)) -> MenuService:
    menu_repo = MenuRepository(session)
    return MenuService(menu_repo)


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menus(menu: MenuSchema,
                 menu_service: MenuService = Depends(get_menu_service)):
    return menu_service.create_menu(menu)


@router.get("/", response_model=List[MenuResponse])
def read_all_menus(menu_service: MenuService = Depends(get_menu_service)):
    return menu_service.read_all_menus()


@router.get("/{menu_id}/", response_model=MenuCountResponse)
def read_menu(menu_id: str,
              menu_service: MenuService = Depends(get_menu_service)):
    return menu_service.read_menu(menu_id)


@router.patch("/{menu_id}/", response_model=MenuResponse)
def update_menu(menu_id: str,
                updated_menu: MenuSchema,
                menu_service: MenuService = Depends(get_menu_service)):
    return menu_service.update_menu(menu_id, updated_menu)


@router.delete("/{menu_id}/", response_model=MenuResponse)
def delete_menu(menu_id: str,
                menu_service: MenuService = Depends(get_menu_service)):
    return menu_service.delete_menu(menu_id)
