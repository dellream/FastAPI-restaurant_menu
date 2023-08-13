from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from starlette import status

from app.db.database_connect import get_async_session
from app.db.repositories.dish_repository import AsyncDishRepository
from app.models.schemas.menus.dish_schemas import DishResponse, DishSchema
from app.api.menus.services.dish_service import AsyncDishService

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"]
)


def get_dish_service(session: Session = Depends(get_async_session)) -> AsyncDishService:
    dish_repo = AsyncDishRepository(session)
    return AsyncDishService(dish_repo)


@router.post("/", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(dish: DishSchema,
                      submenu_id: str,
                      dish_service: AsyncDishService = Depends(get_dish_service)):
    return await dish_service.create_dish(submenu_id, dish)


@router.get("/", response_model=List[DishResponse])
async def read_all_dishes(dish_service: AsyncDishService = Depends(get_dish_service)):
    return await dish_service.read_all_dishes()


@router.get("/{dish_id}/", response_model=DishResponse)
async def read_dish(dish_id: str,
                    dish_service: AsyncDishService = Depends(get_dish_service)):
    return await dish_service.read_dish(dish_id)


@router.patch("/{dish_id}/", response_model=DishResponse)
async def update_dish(dish_id: str,
                      updated_dish: DishSchema,
                      dish_service: AsyncDishService = Depends(get_dish_service)):
    return await dish_service.update_dish(dish_id, updated_dish)


@router.delete("/{dish_id}/", response_model=DishResponse)
async def delete_dish(dish_id: str,
                      dish_service: AsyncDishService = Depends(get_dish_service)):
    return await dish_service.delete_dish(dish_id)
