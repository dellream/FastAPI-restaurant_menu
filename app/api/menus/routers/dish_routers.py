from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm.exc import FlushError, NoResultFound
from starlette import status

from app.api.menus.services.dish_service import AsyncDishService
from app.models.schemas.menus.dish_schemas import DishResponse, DishSchema

dish_router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Блюда']
)


@dish_router.post('/',
                  response_model=DishResponse,
                  status_code=status.HTTP_201_CREATED,
                  summary='Создать блюдо в подменю')
async def create_dish(background_tasks: BackgroundTasks,
                      dish: DishSchema,
                      menu_id: str,
                      submenu_id: str,
                      dish_service: AsyncDishService = Depends()) -> DishResponse:
    try:
        return await dish_service.create_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish=dish,
            background_tasks=background_tasks
        )
    except FlushError as error:
        raise HTTPException(status_code=400, detail=error.args[0])
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@dish_router.get('/',
                 response_model=list[DishResponse],
                 summary='Получить список блюд из подменю')
async def read_all_dishes(background_tasks: BackgroundTasks,
                          menu_id: str,
                          submenu_id: str,
                          dish_service: AsyncDishService = Depends()) -> list[DishResponse]:
    """Получение всех блюд конкретного подменю в конкретном меню."""
    return await dish_service.read_all_dishes(
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks
    )


@dish_router.get('/{dish_id}/',
                 response_model=DishResponse,
                 summary='Получить информацию о блюде')
async def read_dish(background_tasks: BackgroundTasks,
                    menu_id: str,
                    submenu_id: str,
                    dish_id: str,
                    dish_service: AsyncDishService = Depends()) -> DishResponse:
    return await dish_service.read_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        background_tasks=background_tasks
    )


@dish_router.patch('/{dish_id}/',
                   response_model=DishResponse,
                   summary='Изменить блюдо')
async def update_dish(background_tasks: BackgroundTasks,
                      menu_id: str,
                      submenu_id: str,
                      dish_id: str,
                      updated_dish: DishSchema,
                      dish_service: AsyncDishService = Depends()) -> DishResponse:
    return await dish_service.update_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        updated_dish=updated_dish,
        background_tasks=background_tasks
    )


@dish_router.delete('/{dish_id}/',
                    response_model=DishResponse,
                    summary='Удалить блюдо')
async def delete_dish(background_tasks: BackgroundTasks,
                      menu_id: str,
                      submenu_id: str,
                      dish_id: str,
                      dish_service: AsyncDishService = Depends()) -> DishResponse:
    return await dish_service.delete_dish(
        dish_id=dish_id,
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks
    )
