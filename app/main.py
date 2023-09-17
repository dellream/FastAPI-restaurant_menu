from fastapi import FastAPI

from app.api.menus.routers.dish_routers import dish_router as dish_routers
from app.api.menus.routers.menu_routers import menu_router as menu_routers
from app.api.menus.routers.submenu_routers import submenu_router as submenu_routers

# from app.config import CELERY_STATUS
# from app.tasks.tasks import update_base

description = """
REST API для работы с меню ресторана. 🚀

### Меню

- Вы можете **создавать, получать, изменять и удалять основное меню**.
- В одном меню может находиться несколько подменю.

### Подменю

- Вы можете **создавать, получать, изменять и удалять подменю**.
- В одном подменю может находиться несколько блюд.
- Одно и тоже подменю не может находиться в нескольких основных меню одновременно.

### Блюда

- Вы можете **создавать, получать, изменять и удалять блюда**.
- Одно и тоже блюдо не может находиться в нескольких подменю или меню одновременно.
- Блюдо всегда находится в подменю и не может напрямую взаимодействовать с основным меню.

Благодарю за уделенное внимание моему проекту, мои контакты представлены ниже:
"""
tags_metadata = [
    {
        'name': 'Меню',
        'description': 'Операции с основным меню.',
    },
    {
        'name': 'Подменю',
        'description': 'Операции с подменю из основного меню.',
    },
    {
        'name': 'Блюда',
        'description': 'Операции с блюдами из подменю.',
    },
]

app = FastAPI(
    title='Меню ресторана',
    description=description,
    version='1.0.1',
    contact={
        'name': 'Якимов Алексей',
        'url': 'https://github.com/dellream'
    },
    openapi_tags=tags_metadata
)

app.include_router(menu_routers)
app.include_router(submenu_routers)
app.include_router(dish_routers)


# @app.on_event('startup')
# async def on_startup():
#     """Выполняется при запуске приложения.
#     Инициализирует БД и запускает задачу обновления БД."""
#     if CELERY_STATUS:
#         update_base.delay()
