"""
Сервисный слой для обновления данных в базе после парсинга файла.
"""

import requests  # type: ignore[import]

from app.config import BASE_URL


class BaseUpdaterRepo:
    """
    Класс для обновления или создания данных в базе данных,
    используя полученные после парсинга данные из файла.
    """

    def __init__(self, parser_data: list[dict]):
        self.parser_data = parser_data

    @staticmethod
    def get_menus_from_db() -> list[str]:
        """
        Выполняет запросы к базе данных, чтобы получить список ID существующих меню.
        """
        url = f'{BASE_URL}/menus'
        response = requests.get(url).json()
        menus_id = []
        for i in response:
            menus_id.append(i['id'])
        return menus_id

    @staticmethod
    def get_submenus_from_db(menu_id: str) -> list[str]:
        """Выполняет запросы к базе данных, чтобы получить список ID существующих подменю."""
        url = f'{BASE_URL}/menus/{menu_id}/submenus'
        response = requests.get(url).json()
        submenus_id = []
        for i in response:
            submenus_id.append(i['id'])
        return submenus_id

    @staticmethod
    def get_dishes_from_db(menu_id: str, submenu_id: str) -> list[str]:
        """Выполняет запросы к базе данных, чтобы получить список ID блюд."""
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes'
        response = requests.get(url).json()
        dishes_id = []
        for i in response:
            dishes_id.append(i['id'])
        return dishes_id

    def post_menu(self, menu: dict[str, str | list]) -> None:
        """
        Выполняет POST-запрос для добавления новых меню в базу данных.
        Принимает данные о меню в качестве аргумента и отправляет их на сервер.
        """
        url = f'{BASE_URL}/menus/'
        data = {
            'id': menu['id'],
            'title': menu['title'],
            'description': menu['description'],
        }
        requests.post(url, json=data)

    def post_submenu(
            self,
            submenu: dict[str, str | list],
            menu_id: str,
    ) -> None:
        """
        Выполняет POST-запрос для добавления новых подменю в базу данных.
        Принимает данные о подменю в качестве аргумента и отправляет их на сервер.
        """
        url = f'{BASE_URL}/menus/{menu_id}/submenus/'
        data = {
            'id': submenu['id'],
            'title': submenu['title'],
            'description': submenu['description'],
        }
        requests.post(url, json=data)

    def post_submenus_batch(
            self,
            submenus: list,
            menu_id: str
    ) -> None:
        """
        Выполняет POST-запрос для добавления новых подменю в базу данных (постит новые подменю в базу списком).
        Принимает данные о подменю в качестве аргумента и отправляет их на сервер.
        """
        for submenu in submenus:
            self.post_submenu(
                submenu=submenu,
                menu_id=menu_id,
            )

    def post_dish(
            self,
            dish: dict[str, str],
            submenu_id: str,
            menu_id: str,
    ) -> None:
        """
        Выполняет POST-запрос для добавления новых блюд в базу данных.
        Принимает данные о блюдах в качестве аргумента и отправляет их на сервер.
        """
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes'
        data = {
            'id': dish['id'],
            'title': dish['title'],
            'description': dish['description'],
            'price': dish['price'],
            'discount': dish['discount'],
        }
        requests.post(url, json=data)

    def post_dishes_batch(
            self,
            dishes: list,
            submenu_id: str,
            menu_id: str,
    ) -> None:
        """
        Выполняет POST-запрос для добавления новых блюд в базу данных (постит новые блюда в базу списком).
        Принимает данные о блюдах в качестве аргумента и отправляет их на сервер.
        """
        for dish in dishes:
            self.post_dish(
                dish=dish,
                submenu_id=submenu_id,
                menu_id=menu_id,
            )

    def patch_menu(self, menu: dict[str, str | list]) -> None:
        """
        Обновить данные о меню в базе.
        Выполняет PATCH-запрос для обновления данных о меню в базе данных.
        Сравнивает данные, полученные из файла Excel, с данными в базе данных и, если есть различия,
        обновляют соответствующие записи.
        """
        data = {
            'title': menu['title'],
            'description': menu['description'],
        }
        url = f'{BASE_URL}/menus/{menu["id"]}'
        requests.patch(url, json=data)

    def check_menu(self, menu: dict[str, str | list]) -> None:
        """
        Проверить состояние меню в базе и по необходимости обновить.
        """
        url = f'{BASE_URL}/menus/{menu["id"]}'
        current_menu = requests.get(url).json()
        if current_menu['title'] != menu['title'] or \
                current_menu['description'] != menu['description']:
            self.patch_menu(menu=menu)

    def patch_submenu(
            self,
            submenu: dict[str, str | list],
            menu_id: str,
    ) -> None:
        """
        Обновить данные о подменю в базе.
        Выполняет PATCH-запрос для обновления данных о подменю в базе данных.
        Сравнивает данные, полученные из файла Excel, с данными в базе данных и, если есть различия,
        обновляют соответствующие записи.
        """
        data = {
            'title': submenu['title'],
            'description': submenu['description'],
        }
        url = f'{BASE_URL}/menus/{menu_id}/submenus/{submenu["id"]}'
        requests.patch(url, json=data)

    def check_submenu(
            self,
            submenu: dict[str, str | list],
            menu_id: str,
    ) -> None:
        """Проверить состояние подменю в базе и по необходимости обновить."""
        pass

    def patch_dish(
            self,
            dish: dict[str, str],
            submenu_id: str,
            menu_id: str,
    ) -> None:
        """Обновить данные о блюде в базе."""
        pass

    def check_dish(
            self,
            dish: dict[str, str],
            submenu_id: str,
            menu_id: str,
    ) -> None:
        """
        Выполняет PATCH-запрос для обновления данных о блюдах в базе данных.
        Сравнивает данные, полученные из файла Excel, с данными в базе данных и, если есть различия,
        обновляют соответствующие записи.
        """
        pass

    def delete_menu(self, menu_id: str) -> None:
        """
        Выполняет DELETE-запросы для удаления меню из базы данных.
        """
        pass

    def delete_submenu(self, submenu_id: str, menu_id: str) -> None:
        """
        Выполняет DELETE-запросы для удаления подменю из базы данных.
        """
        pass

    def delete_dish(self, dish_id: str, menu_id: str, submenu_id: str) -> None:
        """
        Выполняет DELETE-запросы для удаления блюд из базы данных.
        """
        pass

    def check_dishes(
            self,
            dishes: list[dict[str, str]],
            menu_id: str,
            submenu_id: str,
    ) -> None:
        """
        Выполняет сравнение данных из файла Excel с данными в базе данных и
        вызывает соответствующие методы для создания, обновления и удаления записей в базе данных.
        """
        pass

    def check_submenus(
            self,
            submenus: list[dict],
            menu_id: str,
    ) -> None:
        """
        Выполняет сравнение данных из файла Excel с данными в базе данных и
        вызывает соответствующие методы для создания, обновления и удаления записей в базе данных.
        """
        pass

    def check_menus(self) -> None:
        """
        Выполняет сравнение данных из файла Excel с данными в базе данных и
        вызывает соответствующие методы для создания, обновления и удаления записей в базе данных.
        """
        pass

    def run(self) -> None:
        """Запустить обновление данных в базе."""
        self.check_menus()
