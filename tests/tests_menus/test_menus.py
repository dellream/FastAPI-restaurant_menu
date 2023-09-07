import pytest
from httpx import AsyncClient

from app.config import BASE_URL

pytest_plugins = 'tests.tests_menus.fixtures'


class TestMenu:
    # Создает меню
    @pytest.mark.asyncio
    async def test_create_menu(self, http_client: AsyncClient):
        url = f'{BASE_URL}/menus/'

        data = {
            'title': 'Menu 1',
            'description': 'Description of Menu 1'
        }

        async for every_client in http_client:
            response = await every_client.post(url, json=data)

            assert response.headers['Content-Type'] == 'application/json'
            assert response.status_code == 201
            assert 'id' in response.json()
            assert response.json()['title'] == data['title']
            assert response.json()['description'] == data['description']

    # Создает подменю
    @pytest.mark.asyncio
    async def test_create_submenu(self, http_client, menu_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/'
        data = {
            'title': 'Submenu 1',
            'description': 'Description of Submenu 1'
        }
        async for every_client in http_client:
            response = await every_client.post(url, json=data)
            assert response.status_code == 201
            assert 'id' in response.json()
            assert response.json()['title'] == data['title']
            assert response.json()['description'] == data['description']
            assert 'dishes_count' in response.json() and (
                response.json()['dishes_count'] == 0
            )

    # Создает два блюда
    @pytest.mark.asyncio
    async def test_create_two_dishes(self, http_client, menu_id, submenu_id):
        dishes_data = [
            {
                'title': 'Dish 1',
                'description': 'Description of Dish 1',
                'price': '10.99'
            },
            {
                'title': 'Dish 2',
                'description': 'Description of Dish 2',
                'price': '15.99'
            }
        ]

        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/'

        async for every_client in http_client:
            for data in dishes_data:
                response = await every_client.post(url, json=data)
                assert response.status_code == 201
                assert 'id' in response.json()
                assert response.json()['title'] == data['title']
                assert response.json()['description'] == data['description']
                assert response.json()['price'] == data['price']

    # Смотрит список всех меню
    @pytest.mark.asyncio
    async def test_read_all_menus(self, http_client):
        url = f'{BASE_URL}/menus/'
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    # Смотрит определенное меню
    @pytest.mark.asyncio
    async def test_read_menu(self, http_client, menu_id):
        url = f'{BASE_URL}/menus/{menu_id}/'
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert 'id' in response.json()
            assert 'title' in response.json()
            assert 'description' in response.json()
            assert 'submenus_count' in response.json()
            assert 'dishes_count' in response.json()

    # Смотрит список всех подменю
    @pytest.mark.asyncio
    async def test_read_all_submenus(self, http_client, menu_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/'
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    # Смотрит определенное подменю
    @pytest.mark.asyncio
    async def test_read_submenu(self, http_client, menu_id, submenu_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/'
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert 'id' in response.json()
            assert 'title' in response.json()
            assert 'description' in response.json()
            assert 'dishes_count' in response.json()

    # Смотрит список всех блюд
    @pytest.mark.asyncio
    async def test_read_all_dishes(self, http_client, menu_id, submenu_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/'
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    # Смотрит определенное меню
    @pytest.mark.asyncio
    async def test_read_dish(self, http_client, menu_id, submenu_id, dish_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/'
        async for every_client in http_client:
            response = await every_client.get(url)
            assert response.status_code == 200
            assert 'id' in response.json()
            assert 'title' in response.json()
            assert 'description' in response.json()
            assert 'price' in response.json()

    # Обновляет определенное меню
    @pytest.mark.asyncio
    async def test_update_menu(self, http_client, menu_id):
        url = f'{BASE_URL}/menus/{menu_id}/'
        data = {
            'title': 'Updated Menu',
            'description': 'Updated description'
        }
        async for every_client in http_client:
            response = await every_client.patch(url, json=data)
            assert response.status_code == 200
            assert response.json()['title'] == data['title']
            assert response.json()['description'] == data['description']

    # Обновляет определенное подменю
    @pytest.mark.asyncio
    async def test_update_submenu(self, http_client, menu_id, submenu_id):
        assert menu_id is not None, 'ID меню не был сохранен'
        assert submenu_id is not None, 'ID подменю не был сохранен'

        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/'
        data = {
            'title': 'Updated Submenu',
            'description': 'Updated description'
        }

        async for every_client in http_client:
            response = await every_client.patch(url, json=data)
            assert response.status_code == 200
            assert response.json()['title'] == data['title']
            assert response.json()['description'] == data['description']

    # Обновляет определенное блюдо
    @pytest.mark.asyncio
    async def test_update_dish(self, http_client, menu_id, submenu_id, dish_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/'
        data = {
            'title': 'Updated Dish',
            'description': 'Updated description',
            'price': '12.99'
        }
        async for every_client in http_client:
            response = await every_client.patch(url, json=data)
            assert response.status_code == 200
            assert response.json()['title'] == data['title']
            assert response.json()['description'] == data['description']
            assert response.json()['price'] == data['price']  # Приведение числа к строковому типу

    # Удаляет определенное блюдо
    @pytest.mark.asyncio
    async def test_delete_dish(self, http_client, menu_id, submenu_id, dish_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/'
        async for every_client in http_client:
            response = await every_client.delete(url)
            assert response.status_code == 200

    # Удаляет определенное подменю
    @pytest.mark.asyncio
    async def test_delete_submenu(self, http_client, menu_id, submenu_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/'
        async for every_client in http_client:
            response = every_client.delete(url)
            assert response.status_code == 200

    # Проверяет список всех подменю после удаления
    @pytest.mark.asyncio
    async def test_read_all_submenus_after_delete(self, http_client, menu_id, submenu_id):
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/'
        async for every_client in http_client:
            response = every_client.get(url)
            assert (response.json() == []), 'Ожидался пустой список, сейчас список не пуст'

    # Удаляет определенное меню
    @pytest.mark.asyncio
    async def test_delete_menu(self, http_client, menu_id):
        url = f'{BASE_URL}/menus/{menu_id}/'
        async for every_client in http_client:
            response = every_client.delete(url)
            assert response.status_code == 200
        async for every_client in http_client:
            response = every_client.get(url)
            assert response.status_code == 404


if __name__ == '__main__':
    pytest.main()
