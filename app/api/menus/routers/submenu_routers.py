from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from starlette import status

from app.db.database_connect import get_db
from app.db.repositories.submenu_repository import SubmenuRepository
from app.models.schemas.menus.submenu_schemas import SubmenuResponse, SubmenuSchema, SubmenuCountResponse
from app.services.submenu_service import SubmenuService

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["Submenus"]
)


def get_submenu_service(session: Session = Depends(get_db)) -> SubmenuService:
    submenu_repo = SubmenuRepository(session)
    return SubmenuService(submenu_repo)


@router.post("/", response_model=SubmenuResponse, status_code=status.HTTP_201_CREATED)
def create_submenus(submenu: SubmenuSchema,
                    menu_id: str,
                    submenu_service: SubmenuService = Depends(get_submenu_service)):
    return submenu_service.create_submenu(menu_id, submenu)


@router.get("/", response_model=List[SubmenuResponse])
def read_all_submenus(submenu_service: SubmenuService = Depends(get_submenu_service)):
    return submenu_service.read_all_submenus()


@router.get("/{submenu_id}/", response_model=SubmenuCountResponse)
def read_submenu(submenu_id: str,
                 submenu_service: SubmenuService = Depends(get_submenu_service)):
    return submenu_service.read_submenu(submenu_id)


@router.patch("/{submenu_id}/", response_model=SubmenuResponse)
def update_submenu(submenu_id: str,
                   updated_submenu: SubmenuSchema,
                   submenu_service: SubmenuService = Depends(get_submenu_service)):
    return submenu_service.update_submenu(submenu_id, updated_submenu)


@router.delete("/{submenu_id}/", response_model=SubmenuResponse)
def delete_submenu(submenu_id: str,
                   submenu_service: SubmenuService = Depends(get_submenu_service)):
    return submenu_service.delete_submenu(submenu_id)
