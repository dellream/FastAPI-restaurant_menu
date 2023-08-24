from fastapi import APIRouter, Depends, BackgroundTasks

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
async def create_dish(background_tasks: BackgroundTasks,
                      dish: DishSchema,
                      submenu_id: str,
                      dish_service: AsyncDishService = Depends()):
    return await dish_service.create_dish(
        submenu_id=submenu_id,
        dish=dish,
        background_tasks=background_tasks
    )


@dish_router.get("/",
                 response_model=List[DishResponse])
async def read_all_dishes(background_tasks: BackgroundTasks,
                          menu_id: str,
                          submenu_id: str,
                          dish_service: AsyncDishService = Depends()):
    """
    Получение всех блюд конкретного подменю в конкретном меню

    :param background_tasks: Фоновая задача
    :param menu_id: Идентификатор меню
    :param submenu_id: Идентификатор подменю
    :param dish_service: Сервис для работы с блюдами
    :return: Список всех блюд указанного подменю в формате DishResponse.
    """
    return await dish_service.read_all_dishes(
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks
    )


@dish_router.get("/{dish_id}/",
                 response_model=DishResponse)
async def read_dish(background_tasks: BackgroundTasks,
                    menu_id: str,
                    submenu_id: str,
                    dish_id: str,
                    dish_service: AsyncDishService = Depends()):
    return await dish_service.read_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        background_tasks=background_tasks
    )


@dish_router.patch("/{dish_id}/",
                   response_model=DishResponse)
async def update_dish(background_tasks: BackgroundTasks,
                      menu_id: str,
                      submenu_id: str,
                      dish_id: str,
                      updated_dish: DishSchema,
                      dish_service: AsyncDishService = Depends()):
    return await dish_service.update_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        updated_dish=updated_dish,
        background_tasks=background_tasks
    )


@dish_router.delete("/{dish_id}/",
                    response_model=DishResponse)
async def delete_dish(background_tasks: BackgroundTasks,
                      menu_id: str,
                      submenu_id: str,
                      dish_id: str,
                      dish_service: AsyncDishService = Depends()):
    return await dish_service.delete_dish(
        dish_id=dish_id,
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks
    )
