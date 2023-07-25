# REST API для работы с меню ресторана
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

### Описание проекта

Этот проект представляет собой REST API для работы с меню ресторана.
Основная цель данного тестового задания - пройти 161 тест в Postman, которые проверяют функциональность API.
Проект реализован с использованием FastAPI и PostgreSQL в качестве базы данных.

### Установка и настройка проекта

1. Убедитесь, что у вас установлен Python версии 3.7 или выше.
2. Клонируйте репозиторий с GitHub: `git clone https://github.com/dellream/REST-API-app_test_task.git`
3. Перейдите в каталог проекта
4. Установите зависимости: `pip install -r requirements.txt`
5. Убедитесь, что у вас установлен PostgreSQL и создайте базу данных для проекта.

### Настройка базы данных

1. Установите PostgreSQL: Убедитесь, что PostgreSQL установлен на вашей системе и работает.
   Если его нет, установите PostgreSQL, а также инструмент командной строки psql, который позволяет взаимодействовать с базой данных.
2. Создайте базу данных: Откройте командную строку или терминал и используйте psql, чтобы подключиться к PostgreSQL и создать базу данных для вашего проекта.
3. В файле **main.py** необходимо изменить строку (вставьте свои данные): 
```python
postgresql://username:password@host:port/database_name
```
4. Повторите тоже самое для файла **alembic.ini**, нужно изменить строку 
```python
sqlalchemy.url = postgresql://username:password@host:port/database_name
```
5. Создайте ревизию alembic: `alembic revision --autogenerate -m "Описание вашей ревизии"`
6. Выполните миграцию: `alembic upgrade head`

### Запуск проекта

1. Запустите сервер: `uvicorn src.app.main:app --reload`
2. API должно быть доступно по адресу, указанному в консоли
3. Пройдите все тесты в POSTMAN: 

![Screenshot of successful passing tests](https://github.com/dellream/REST-API-app_test_task/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82_%D1%81_Postman.png?raw=true)

<sub>Инструкция по работе с POSTMAN:<br>
![Screenshot with instructions for POSTMAN](https://zenclass-files-hot-01.storage.yandexcloud.net/0873bcaa-7dd7-47c5-a5e7-332f1a61a56f.png)
Нажимаем import (1 на скрине) и переносим два файла (*menu app.postman_collection.json* и *menu app.postman_environment.json*) в окно постман. Один файл - коллекция тестов, второй - переменные окружения.<br> 
В диалоговом окне подтверждаем импорт. После этого должна появиться коллекция (подчернута на скрине) menu app.<br>
Выбираем переменные окружения (2 на скрине) из выпадающего списка<br>
После этого можем зайти в коллекцию menu app и запустить каждый тест вручную. Для этого открываем коллекцию menu app, выбираем Тестовый сценарий -> CRUD для меню -> Просматривает список меню(или любой другой) у нас в центральной части появляется запрос, нажимаем Send и запрос летит в наше приложение.<br>
Если хотим запустит сразу всю коллекцию тестов, то жмем на три точки (3 на скрине) рядом с коллекцией и выбираем Run.</sub>
