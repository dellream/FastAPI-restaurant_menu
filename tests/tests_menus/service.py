"""
Реализация подобия Django reverse функции.

В Django reverse используется для создания URL-адресов на основе имен маршрутов и параметров представления,
а FastAPI использует декораторы и функции для определения маршрутов и их обработки.
Данный модуль создает подобный механизм для создания URL-адресов на основе имен маршрутов в FastAPI.

Справка: в документации в FastAPI есть раздел "Path Operation Advanced Configuration", где описано, что можно
изучить существующие в проекте пути следующим образом:

from fastapi.routing import APIRoute

for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"Маршрут: {route.path}, Метод: {route.methods}, Функция-обработчик: {route.endpoint.__name__}")
"""

from typing import Callable

from fastapi.routing import APIRoute

from app.main import app


def get_routes() -> dict[str, str]:
    """Получение словаря с маршрутами приложения."""
    routes = {}

    # Пройдемся по всем маршрутам в приложении и сформируем словарь
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes[route.endpoint.__name__] = f'http://localhost:8000{route.path}'
    return routes


def reverse(foo: Callable,
            routes: dict[str, str] = get_routes(),
            **kwargs) -> str:
    """Получение url адреса."""
    path = routes[foo.__name__]
    return path.format(**kwargs)


get_routes()
