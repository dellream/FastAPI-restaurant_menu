from fastapi import FastAPI

from app.api.menus.routers.menu_routers import menu_router as menu_routers
from app.api.menus.routers.submenu_routers import submenu_router as submenu_routers
from app.api.menus.routers.dish_routers import dish_router as dish_routers

app = FastAPI(
    title="Restaurant menu"
)

app.include_router(menu_routers)
app.include_router(submenu_routers)
app.include_router(dish_routers)
