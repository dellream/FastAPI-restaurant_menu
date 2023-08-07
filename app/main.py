import uvicorn
from fastapi import FastAPI

from app.api.menus.routers.menu_routers import router as menu_routers
from app.api.menus.routers.submenu_routers import router as submenu_routers
from app.api.menus.routers.dish_routers import router as dish_routers

app = FastAPI(
    title="Restaurant menu"
)

app.include_router(menu_routers)
app.include_router(submenu_routers)
app.include_router(dish_routers)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
