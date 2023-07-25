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

1. Запустите сервер: `uvicorn main:app --reload`
2. API должно быть доступно по адресу, указанному в консоли
