from decimal import Decimal
from http import HTTPStatus
from typing import Any

import pytest
from httpx import AsyncClient

from app.api.menus.routers.dish_routers import create_dish, delete_dish
from app.api.menus.routers.menu_routers import (
    create_menus,
    delete_menu,
    get_full_restaurant_menu,
)
from app.api.menus.routers.submenu_routers import create_submenus, delete_submenu
from tests.tests_menus.service import reverse

pytest_plugins = 'tests.tests_menus.fixtures'


class TestFullMenu:
    # Проверка на пустой список неактуальна, так как excel заполняет бд
    # @pytest.mark.asyncio
    # async def test_all_menu_empty(self,
    #                               http_client: AsyncClient) -> None:
    #     """Проверка получения пустого списка меню."""
    #     async for client in http_client:
    #         response = await client.get(reverse(get_full_restaurant_menu))
    #         assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    #         assert response.json() == [], 'В ответе непустой список'

    @pytest.mark.asyncio
    async def test_post_menu(self,
                             menu_post: dict[str, str],
                             saved_data: dict[str, Any],
                             http_client: AsyncClient) -> None:
        """Добавление нового меню."""
        async for client in http_client:
            response = await client.post(reverse(create_menus), json=menu_post)
            assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
            assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
            assert 'title' in response.json(), 'Названия меню нет в ответе'
            assert 'description' in response.json(), 'Описания меню нет в ответе'

            saved_data['menu'] = response.json()

    @pytest.mark.asyncio
    async def test_post_submenu(self,
                                submenu_post: dict[str, str],
                                saved_data: dict[str, Any],
                                http_client: AsyncClient) -> None:
        """Добавление нового подменю."""
        async for client in http_client:
            menu = saved_data['menu']
            response = await client.post(reverse(create_submenus, menu_id=menu['id']),
                                         json=submenu_post)
            assert response.status_code == HTTPStatus.CREATED, \
                'Статус ответа не 201'
            assert 'id' in response.json(), 'Идентификатора подменю нет в ответе'
            assert 'menu_id' in response.json(), 'Идентификатора меню нет в ответе'
            assert 'title' in response.json(), 'Названия подменю нет в ответе'
            assert 'description' in response.json(), 'Описания подменю нет в ответе'
            assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
            assert response.json()['title'] == submenu_post['title'], \
                'Название подменю не соответствует ожидаемому'
            assert response.json()['description'] == submenu_post['description'], \
                'Описание подменю не соответствует ожидаемому'

            saved_data['submenu'] = response.json()

    @pytest.mark.asyncio
    async def test_post_dish(self,
                             dish_post: dict[str, str],
                             saved_data: dict[str, Any],
                             http_client: AsyncClient) -> None:
        """Добавление первого нового блюда."""
        async for client in http_client:
            menu = saved_data['menu']
            submenu = saved_data['submenu']
            response = await client.post(reverse(create_dish, menu_id=menu['id'], submenu_id=submenu['id']),
                                         json=dish_post)
            assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
            assert 'id' in response.json(), 'Идентификатора блюда нет в ответе'
            assert 'submenu_id' in response.json(), 'Идентификатора подменю нет в ответе'
            assert 'title' in response.json(), 'Названия блюда нет в ответе'
            assert 'description' in response.json(), 'Описания блюда нет в ответе'
            assert 'price' in response.json(), 'Цены блюда нет в ответе'
            assert response.json()['title'] == dish_post['title'], \
                'Название блюда не соответствует ожидаемому'
            assert response.json()['description'] == dish_post['description'], \
                'Описание блюда не соответствует ожидаемому'

            saved_data['dish'] = response.json()

    @pytest.mark.asyncio
    async def test_full_base(self,
                             menu_post: dict[str, str],
                             submenu_post: dict[str, str],
                             dish_post: dict[str, str],
                             saved_data: dict[str, Any],
                             http_client: AsyncClient) -> None:
        """Проверка полного вывода базы."""
        async for client in http_client:
            response = await client.get(reverse(get_full_restaurant_menu))
            assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'

            data = response.json()

            assert len(data) == 1, 'В ответе не одно меню'
            assert data[0]['title'] == menu_post['title'], 'Название меню не соответствует ожидаемому'
            assert data[0]['description'] == menu_post['description'], 'Описание меню не соответствует ожидаемому'
            assert data[0]['id'] == saved_data['menu']['id'], 'Идентификатора меню не соответствует ожидаемому'
            assert len(data[0]['submenus']) == 1, 'Количество подменю не соответствует ожидаемому'

            submenu = data[0]['submenus'][0]

            assert submenu['title'] == submenu_post['title'], 'Название подменю не соответствует ожидаемому'
            assert submenu['description'] == submenu_post['description'], 'Описание подменю не соответствует ожидаемому'
            assert submenu['id'] == saved_data['submenu']['id'], 'Идентификатора подменю не соответствует ожидаемому'
            assert len(submenu['dishes']) == 1, 'Количество блюд не соответствует ожидаемому'

            dish = submenu['dishes'][0]

            assert dish['title'] == dish_post['title'], 'Название блюда не соответствует ожидаемому'
            assert dish['description'] == dish_post['description'], 'Описание блюда не соответствует ожидаемому'
            assert dish['price'] == str(Decimal(dish_post['price']).quantize(Decimal('0.00'))), \
                'Цена блюда не соответствует ожидаемой'
            assert dish['id'] == saved_data['dish']['id'], 'Идентификатора блюда не соответствует ожидаемому'

    @pytest.mark.asyncio
    async def test_delete_dish(self,
                               saved_data: dict[str, Any],
                               http_client: AsyncClient) -> None:
        """Удаление текущего блюда."""
        async for client in http_client:
            menu = saved_data['menu']
            submenu = saved_data['submenu']
            dish = saved_data['dish']
            response = await client.delete(
                reverse(delete_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id'])
            )
            assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
            assert response.text == '"dish deleted"', 'Сообщение об удалении не соответствует ожидаемому'

    @pytest.mark.asyncio
    async def test_full_base_after_dish_delete(self,
                                               menu_post: dict[str, str],
                                               submenu_post: dict[str, str],
                                               saved_data: dict[str, Any],
                                               http_client: AsyncClient) -> None:
        """Проверка полного вывода базы после удаления блюда."""
        async for client in http_client:
            response = await client.get(
                reverse(get_full_restaurant_menu),
            )
            assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'

            data = response.json()

            assert len(data) == 1, 'В ответе не одно меню'
            assert data[0]['title'] == menu_post['title'], 'Название меню не соответствует ожидаемому'
            assert data[0]['description'] == menu_post['description'], 'Описание меню не соответствует ожидаемому'
            assert data[0]['id'] == saved_data['menu']['id'], 'Идентификатора меню не соответствует ожидаемому'
            assert len(data[0]['submenus']) == 1, 'Количество подменю не соответствует ожидаемому'

            submenu = data[0]['submenus'][0]

            assert submenu['title'] == submenu_post['title'], 'Название подменю не соответствует ожидаемому'
            assert submenu['description'] == submenu_post['description'], 'Описание подменю не соответствует ожидаемому'
            assert submenu['id'] == saved_data['submenu']['id'], 'Идентификатора подменю не соответствует ожидаемому'
            assert len(submenu['dishes']) == 0, 'Количество блюд не соответствует ожидаемому'

    @pytest.mark.asyncio
    async def test_delete_submenu(self,
                                  saved_data: dict[str, Any],
                                  http_client: AsyncClient) -> None:
        """Удаление текущего подменю."""
        async for client in http_client:
            menu = saved_data['menu']
            submenu = saved_data['submenu']
            response = await client.delete(
                reverse(delete_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
            )
            assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
            assert response.text == '"submenu deleted"', 'Сообщение об удалении не соответствует ожидаемому'

    @pytest.mark.asyncio
    async def test_full_base_after_submenu_delete(self,
                                                  menu_post: dict[str, str],
                                                  saved_data: dict[str, Any],
                                                  http_client: AsyncClient) -> None:
        """Проверка полного вывода базы после удаления блюда."""
        async for client in http_client:
            response = await client.get(reverse(get_full_restaurant_menu))
            assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'

            data = response.json()

            assert len(data) == 1, 'В ответе не одно меню'
            assert data[0]['title'] == menu_post['title'], 'Название меню не соответствует ожидаемому'
            assert data[0]['description'] == menu_post['description'], 'Описание меню не соответствует ожидаемому'
            assert data[0]['id'] == saved_data['menu']['id'], 'Идентификатора меню не соответствует ожидаемому'
            assert len(data[0]['submenus']) == 0, 'Количество подменю не соответствует ожидаемому'

    @pytest.mark.asyncio
    async def test_delete_menu(self,
                               saved_data: dict[str, Any],
                               http_client: AsyncClient) -> None:
        """Удаление текущего меню."""
        async for client in http_client:
            menu = saved_data['menu']
            response = await client.delete(reverse(delete_menu, menu_id=menu['id']))
            assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
            assert response.text == '"menu deleted"', 'Сообщение об удалении не соответствует ожидаемому'

    @pytest.mark.asyncio
    async def test_full_base_after_menu_delete(self, http_client: AsyncClient) -> None:
        """Проверка полного вывода базы после удаления меню."""
        async for client in http_client:
            response = await client.get(reverse(get_full_restaurant_menu))
            assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
            assert response.json() == [], 'В ответе непустой список'
