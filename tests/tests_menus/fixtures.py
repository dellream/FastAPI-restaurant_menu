from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import BASE_URL
from app.main import app

pytest_plugins = 'tests.tests_menus.fixtures'
client = TestClient(app)


@pytest.fixture(scope='class')
async def http_client():
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as aclient:
        yield aclient


@pytest.fixture(scope='function')
async def menu_id():
    data = {
        'title': 'Menu pytest title',
        'description': 'Menu pytest description'
    }
    async for every_client in http_client:
        response = await every_client.post('/api/v1/menus', json=data)
        return response.json()['id']


@pytest.fixture(scope='function')
async def submenu_id(menu_id):
    data = {
        'title': 'Submenu pytest title',
        'description': 'Submenu pytest description'
    }
    async for every_client in http_client:
        response = await every_client.post(
            f'/api/v1/menus/{menu_id}/submenus/',
            json=data
        )
        return response.json()['id']


@pytest.fixture(scope='function')
async def dish_id(menu_id, submenu_id):
    data = {
        'price': '12.59',
        'title': 'Dish title',
        'description': 'Dish description'
    }
    async for every_client in http_client:
        response = await every_client.post(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data
        )
        return response.json()['id']


@pytest.fixture
def menu_post() -> dict[str, str]:
    """Фикстура меню для POST."""
    return {
        'title': '1menu',
        'description': 'description'
    }


@pytest.fixture
def menu_patch() -> dict[str, str]:
    """Фикстура меню для PATCH."""
    return {
        'title': '1 menu updated',
        'description': 'description updated'
    }


@pytest.fixture
def submenu_post() -> dict[str, str]:
    """Фикстура подменю для POST."""
    return {
        'title': '1 submenu',
        'description': 'description'
    }


@pytest.fixture
def submenu_patch() -> dict[str, str]:
    """Фикстура подменю для PATCH."""
    return {
        'title': '1 submenu updated',
        'description': 'description updated'
    }


@pytest.fixture
def dish_post() -> dict[str, str]:
    """Фикстура блюда для POST."""
    return {
        'title': '1 dish',
        'description': 'description',
        'price': '123.123',
    }


@pytest.fixture
def dish_2_post() -> dict[str, str]:
    """Фикстура второго блюда для POST."""
    return {
        'title': '2 dish',
        'description': '2 description',
        'price': '321.123',
    }


@pytest.fixture
def dish_patch() -> dict[str, str]:
    """Фикстура блюда для PATCH."""
    return {
        'title': '1 dish updated',
        'description': 'description updated',
        'price': '321.123',
    }


@pytest.fixture(scope='module')
def saved_data() -> dict[str, Any]:
    """Фикстура дял сохранения объектов тестирования."""
    return {}
