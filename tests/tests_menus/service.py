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
    routes_dict = {}

    # Пройдемся по всем маршрутам в приложении и сформируем словарь
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes_dict[route.endpoint.__name__] = f'http://localhost:8000{route.path}'
    return routes_dict


def reverse(foo: Callable,
            routes_dict: dict[str, str] = get_routes(),
            **kwargs) -> str:
    """Получение url адреса."""
    path = routes_dict[foo.__name__]
    return path.format(**kwargs)


if __name__ == '__main__':
    # Отобразим сформированный словарь
    routes = get_routes()
    for key, value in routes.items():
        print(f'{key} : {value}')
