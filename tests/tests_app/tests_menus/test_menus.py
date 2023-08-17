import pytest
import httpx

from fastapi.testclient import TestClient

from app.config import BASE_URL
from app.main import app

client = TestClient(app)


@pytest.fixture(scope='class')
async def http_client():
    async with httpx.AsyncClient(
            app=app,
            base_url=BASE_URL
    ) as aclient:
        yield aclient


@pytest.fixture(scope='function')
async def menu_id():
    data = {
        'title': 'Menu pytest title',
        'description': 'Menu pytest description'
    }
    async for every_client in http_client:
        response = await every_client.post('/api/v1/menus', json=data)
        assert response.status_code == 201
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
        assert response.status_code == 201
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
        assert response.status_code == 201
        assert response.json()['price'] == data['price']
        assert response.json()['title'] == data['title']
        assert response.json()['description'] == data['description']
        return response.json()['id']


class TestMenu:
    # Создает меню
    @pytest.mark.order(1)
    @pytest.mark.asyncio
    async def test_create_menu(self, http_client):
        url = f"{BASE_URL}/menus/"

        data = {
            "title": "Menu 1",
            "description": "Description of Menu 1"
        }

        async for every_client in http_client:
            response = await every_client.post(url, json=data)

            assert response.headers["Content-Type"] == "application/json"
            assert response.status_code == 201
            assert "id" in response.json()
            assert response.json()["title"] == data["title"]
            assert response.json()["description"] == data["description"]

    # Создает подменю
    @pytest.mark.order(2)
    @pytest.mark.asyncio
    async def test_create_submenu(self, http_client, menu_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/"
        data = {
            "title": "Submenu 1",
            "description": "Description of Submenu 1"
        }
        async for every_client in http_client:
            response = await every_client.post(url, json=data)
            assert response.status_code == 201
            assert "id" in response.json()
            assert response.json()["title"] == data["title"]
            assert response.json()["description"] == data["description"]
            assert 'dishes_count' in response.json() and (
                    response.json()['dishes_count'] == 0
            )

    # Создает два блюда
    @pytest.mark.order(3)
    @pytest.mark.asyncio
    async def test_create_two_dishes(self, http_client, menu_id, submenu_id):
        dishes_data = [
            {
                "title": "Dish 1",
                "description": "Description of Dish 1",
                "price": "10.99"
            },
            {
                "title": "Dish 2",
                "description": "Description of Dish 2",
                "price": "15.99"
            }
        ]

        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/"

        async for every_client in http_client:
            for data in dishes_data:
                response = await every_client.post(url, json=data)
                assert response.status_code == 201
                assert "id" in response.json()
                assert response.json()["title"] == data["title"]
                assert response.json()["description"] == data["description"]
                assert response.json()["price"] == data["price"]

    # Смотрит список всех меню
    @pytest.mark.order(4)
    @pytest.mark.asyncio
    async def test_read_all_menus(self, http_client):
        url = f"{BASE_URL}/menus/"
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    # Смотрит определенное меню
    @pytest.mark.order(5)
    @pytest.mark.asyncio
    async def test_read_menu(self, http_client):
        url = f"{BASE_URL}/menus/{menu_id}/"
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert "id" in response.json()
            assert "title" in response.json()
            assert "description" in response.json()
            assert "submenus_count" in response.json()
            assert "dishes_count" in response.json()

    # Смотрит список всех подменю
    @pytest.mark.order(6)
    @pytest.mark.asyncio
    async def test_read_all_submenus(self, http_client, menu_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/"
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    # Смотрит определенное подменю
    @pytest.mark.order(7)
    @pytest.mark.asyncio
    async def test_read_submenu(self, http_client, menu_id, submenu_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/"
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert "id" in response.json()
            assert "title" in response.json()
            assert "description" in response.json()
            assert "dishes_count" in response.json()

    # Смотрит список всех блюд
    @pytest.mark.order(8)
    @pytest.mark.asyncio
    async def test_read_all_dishes(self, http_client, menu_id, submenu_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/"
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    # Смотрит определенное меню
    @pytest.mark.order(9)
    @pytest.mark.asyncio
    async def test_read_dish(self, http_client, menu_id, submenu_id, dish_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/"
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert "id" in response.json()
            assert "title" in response.json()
            assert "description" in response.json()
            assert "price" in response.json()

    # Обновляет определенное меню
    @pytest.mark.order(10)
    @pytest.mark.asyncio
    async def test_update_menu(self, http_client, menu_id):
        url = f"{BASE_URL}/menus/{menu_id}/"
        data = {
            "title": "Updated Menu",
            "description": "Updated description"
        }
        async for every_client in http_client:
            response = await every_client.patch(url, json=data)
            assert response.status_code == 200
            assert response.json()["title"] == data["title"]
            assert response.json()["description"] == data["description"]

    # Обновляет определенное подменю
    @pytest.mark.order(11)
    @pytest.mark.asyncio
    async def test_update_submenu(self, http_client, menu_id, submenu_id):
        assert menu_id is not None, 'ID меню не был сохранен'
        assert submenu_id is not None, 'ID подменю не был сохранен'

        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/"
        data = {
            "title": "Updated Submenu",
            "description": "Updated description"
        }

        async for every_client in http_client:
            response = await every_client.patch(url, json=data)
            assert response.status_code == 200
            assert response.json()["title"] == data["title"]
            assert response.json()["description"] == data["description"]

    # Обновляет определенное блюдо
    @pytest.mark.order(12)
    @pytest.mark.asyncio
    async def test_update_dish(self, http_client, menu_id, submenu_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/"
        data = {
            "title": "Updated Dish",
            "description": "Updated description",
            "price": "12.99"
        }
        async for every_client in http_client:
            response = await every_client.patch(url, json=data)
            assert response.status_code == 200
            assert response.json()["title"] == data["title"]
            assert response.json()["description"] == data["description"]
            assert response.json()["price"] == data["price"]  # Приведение числа к строковому типу

    # Удаляет определенное блюдо
    @pytest.mark.order(13)
    @pytest.mark.asyncio
    async def test_delete_dish(self, http_client, menu_id, submenu_id, dish_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/"
        async for every_client in http_client:
            response = await every_client.delete(url)
            assert response.status_code == 200

    # Удаляет определенное подменю
    @pytest.mark.order(14)
    @pytest.mark.asyncio
    async def test_delete_submenu(self, http_client, menu_id, submenu_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/"
        async for every_client in http_client:
            response = every_client.delete(url)
            assert response.status_code == 200

    # Проверяет список всех подменю после удаления
    @pytest.mark.order(15)
    @pytest.mark.asyncio
    async def test_read_all_submenus_after_delete(self, http_client, menu_id, submenu_id):
        url = f"{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/"
        async for every_client in http_client:
            response = every_client.get(url)
            assert (response.json() == []), 'Ожидался пустой список, сейчас список не пуст'

    # Удаляет определенное меню
    @pytest.mark.order(16)
    @pytest.mark.asyncio
    async def test_delete_menu(self, http_client, menu_id):
        url = f"{BASE_URL}/menus/{menu_id}/"
        async for every_client in http_client:
            response = every_client.delete(url)
            assert response.status_code == 200
        async for every_client in http_client:
            response = every_client.get(url)
            assert response.status_code == 404


if __name__ == "__main__":
    pytest.main()
