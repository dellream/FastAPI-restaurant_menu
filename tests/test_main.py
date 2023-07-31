import pytest
import requests

# Замените baseURL на адрес вашего сервера
baseURL = "http://api:8000/api/v1"

# Переменные окружения
ENV_MENU_ID = None
ENV_MENU_TITLE = None
ENV_MENU_DESCRIPTION = None

ENV_SUBMENU_ID = None
ENV_SUBMENU_TITLE = None
ENV_SUBMENU_DESCRIPTION = None

ENV_DISHES_ID = None
ENV_DISHES_TITLE = None
ENV_DISHES_DESCRIPTION = None
ENV_DISHES_PRICE = None


# Создаем меню и сохраняем id в переменную окружения
def test_create_menu():
    global ENV_MENU_ID, ENV_MENU_TITLE, ENV_MENU_DESCRIPTION
    url = f"{baseURL}/menus/"
    data = {
        "title": "Menu 1",
        "description": "Description of Menu 1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]

    # Сохраним сгенерированные значения в глобальные переменные
    ENV_MENU_ID = response.json()["id"]
    ENV_MENU_TITLE = response.json()["title"]
    ENV_MENU_DESCRIPTION = response.json()["description"]


def test_create_submenu():
    # Объявляем переменные как глобальные
    global ENV_MENU_ID, ENV_SUBMENU_ID, ENV_SUBMENU_TITLE, ENV_SUBMENU_DESCRIPTION
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus"
    data = {
        "title": "Submenu 1",
        "description": "Description of Submenu 1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["menu_id"] == ENV_MENU_ID

    # Сохраним сгенерированные значения в глобальные переменные
    ENV_SUBMENU_ID = response.json()["id"]
    ENV_SUBMENU_TITLE = response.json()["title"]
    ENV_SUBMENU_DESCRIPTION = response.json()["description"]


def test_create_dish():
    # Объявляем переменные как глобальные
    global ENV_MENU_ID, ENV_SUBMENU_ID, ENV_DISHES_ID, ENV_DISHES_TITLE, ENV_DISHES_DESCRIPTION, ENV_DISHES_PRICE
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/{ENV_SUBMENU_ID}/dishes"
    data = {
        "title": "Dish 1",
        "price": 10.99
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == data["title"]
    assert response.json()["price"] == str(data["price"])
    assert response.json()["submenu_id"] == ENV_SUBMENU_ID

    # Сохраним сгенерированные значения в глобальные переменные
    ENV_DISHES_ID = response.json()["id"]
    ENV_DISHES_TITLE = response.json()["title"]
    ENV_DISHES_DESCRIPTION = response.json()["description"]
    ENV_DISHES_PRICE = response.json()["price"]


def test_read_menus():
    url = f"{baseURL}/menus/"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_menu():
    global ENV_MENU_ID
    url = f"{baseURL}/menus/{ENV_MENU_ID}/"
    response = requests.get(url)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "submenus_count" in response.json()
    assert "dishes_count" in response.json()
    assert "submenus" in response.json()


def test_read_submenus():
    global ENV_MENU_ID, ENV_SUBMENU_ID
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_submenu():
    global ENV_MENU_ID, ENV_SUBMENU_ID
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/{ENV_SUBMENU_ID}/"
    response = requests.get(url)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "menu_id" in response.json()
    assert "dishes_count" in response.json()


def test_read_dishes():
    global ENV_MENU_ID, ENV_SUBMENU_ID
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/{ENV_SUBMENU_ID}/dishes/"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_dish():
    global ENV_MENU_ID, ENV_SUBMENU_ID
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/{ENV_SUBMENU_ID}/dishes/{ENV_DISHES_ID}"
    response = requests.get(url)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "price" in response.json()


def test_update_menu():
    global ENV_MENU_ID, ENV_MENU_TITLE, ENV_MENU_DESCRIPTION
    url = f"{baseURL}/menus/{ENV_MENU_ID}/"
    data = {
        "title": "Updated Menu",
        "description": "Updated description"
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]

    # Сохраним измененные значения в глобальные переменные
    ENV_MENU_TITLE = response.json()["title"]
    ENV_MENU_DESCRIPTION = response.json()["description"]


def test_update_submenu():
    global ENV_MENU_ID, ENV_SUBMENU_ID, ENV_SUBMENU_TITLE, ENV_SUBMENU_DESCRIPTION
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/{ENV_SUBMENU_ID}/"
    data = {
        "title": "Updated Submenu",
        "description": "Updated description"
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]

    # Сохраним измененные значения в глобальные переменные
    ENV_SUBMENU_TITLE = response.json()["title"]
    ENV_SUBMENU_DESCRIPTION = response.json()["description"]


def test_update_dish():
    global ENV_MENU_ID, ENV_SUBMENU_ID, ENV_DISHES_TITLE, ENV_DISHES_DESCRIPTION, ENV_DISHES_PRICE
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/{ENV_SUBMENU_ID}/dishes/{ENV_DISHES_ID}/"
    data = {
        "title": "Updated Dish",
        "description": "Updated description",
        "price": 12.99
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["price"] == str(data["price"])  # Приведение числа к строковому типу

    # Сохраним измененные значения в глобальные переменные
    ENV_DISHES_TITLE = response.json()["title"]
    ENV_DISHES_DESCRIPTION = response.json()["description"]
    ENV_DISHES_PRICE = response.json()["price"]


def test_delete_dish():
    global ENV_MENU_ID, ENV_SUBMENU_ID
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/{ENV_SUBMENU_ID}/dishes/{ENV_DISHES_ID}"
    response = requests.delete(url)
    assert response.status_code == 200


def test_delete_submenu():
    global ENV_MENU_ID, ENV_SUBMENU_ID
    url = f"{baseURL}/menus/{ENV_MENU_ID}/submenus/{ENV_SUBMENU_ID}/"
    response = requests.delete(url)
    assert response.status_code == 200


def test_delete_menu():
    global ENV_MENU_ID
    url = f"{baseURL}/menus/{ENV_MENU_ID}/"
    response = requests.delete(url)
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
