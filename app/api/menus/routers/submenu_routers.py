from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from starlette import status

from app.db.database_connect import get_async_session
from app.db.repositories.submenu_repository import AsyncSubmenuRepository
from app.models.schemas.menus.submenu_schemas import SubmenuResponse, SubmenuSchema, SubmenuCountResponse
from app.api.menus.services.submenu_service import AsyncSubmenuService

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["Submenus"]
)


def get_submenu_service(session: Session = Depends(get_async_session)) -> AsyncSubmenuService:
    submenu_repo = AsyncSubmenuRepository(session)
    return AsyncSubmenuService(submenu_repo)


@router.post("/", response_model=SubmenuResponse, status_code=status.HTTP_201_CREATED)
async def create_submenus(submenu: SubmenuSchema,
                          menu_id: str,
                          submenu_service: AsyncSubmenuService = Depends(get_submenu_service)):
    return await submenu_service.create_submenu(menu_id, submenu)


@router.get("/", response_model=List[SubmenuResponse])
async def read_all_submenus(submenu_service: AsyncSubmenuService = Depends(get_submenu_service)):
    return await submenu_service.read_all_submenus()


@router.get("/{submenu_id}/", response_model=SubmenuCountResponse)
async def read_submenu(submenu_id: str,
                       submenu_service: AsyncSubmenuService = Depends(get_submenu_service)):
    return await submenu_service.read_submenu(submenu_id)


@router.patch("/{submenu_id}/", response_model=SubmenuResponse)
async def update_submenu(submenu_id: str,
                         updated_submenu: SubmenuSchema,
                         submenu_service: AsyncSubmenuService = Depends(get_submenu_service)):
    return await submenu_service.update_submenu(submenu_id, updated_submenu)


@router.delete("/{submenu_id}/", response_model=SubmenuResponse)
async def delete_submenu(submenu_id: str,
                         submenu_service: AsyncSubmenuService = Depends(get_submenu_service)):
    return await submenu_service.delete_submenu(submenu_id)
