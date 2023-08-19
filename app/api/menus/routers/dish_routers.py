from fastapi import APIRouter, Depends

from typing import List
from starlette import status

from app.models.schemas.menus.dish_schemas import DishResponse, DishSchema
from app.api.menus.services.dish_service import AsyncDishService

dish_router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"]
)


@dish_router.post("/",
                  response_model=DishResponse,
                  status_code=status.HTTP_201_CREATED)
async def create_dish(dish: DishSchema,
                      submenu_id: str,
                      dish_service: AsyncDishService = Depends()):
    return await dish_service.create_dish(submenu_id, dish)


@dish_router.get("/",
                 response_model=List[DishResponse])
async def read_all_dishes(dish_service: AsyncDishService = Depends()):
    return await dish_service.read_all_dishes()


@dish_router.get("/{dish_id}/",
                 response_model=DishResponse)
async def read_dish(dish_id: str,
                    dish_service: AsyncDishService = Depends()):
    return await dish_service.read_dish(dish_id)


@dish_router.patch("/{dish_id}/",
                   response_model=DishResponse)
async def update_dish(dish_id: str,
                      updated_dish: DishSchema,
                      dish_service: AsyncDishService = Depends()):
    return await dish_service.update_dish(dish_id, updated_dish)


@dish_router.delete("/{dish_id}/",
                    response_model=DishResponse)
async def delete_dish(dish_id: str,
                      dish_service: AsyncDishService = Depends()):
    return await dish_service.delete_dish(dish_id)
