# REST API для работы с меню ресторана
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

### Описание проекта

Этот проект представляет собой REST API для работы с меню ресторана.
Основная цель данного тестового задания - создать REST API, обернуть приложение в Docker и написать тесты.
Проект реализован с использованием FastAPI и PostgreSQL в качестве базы данных.

### Установка и запуск проекта

1. Убедитесь, что у вас установлен Python версии 3.7 или выше.
2. Клонируйте репозиторий с GitHub: `git clone https://github.com/dellream/REST-API-app_test_task.git`
3. Запустите проект с помощью docker-compose `docker-compose up -d`

### Завершение работы
Чтобы остановить и удалить контейнеры, выполните следующую команду: `docker-compose down`

### Тестирование с помощью pytest

Запустите тесты с помощью следующей команды (после завершения тестов, контейнеры будут остановлены, но не удалены): 
```
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### Тестирование с помощью POSTMAN

В репозитории есть директория "other_for_git", где находятся файлы с форматом .json для POSTMAN

<sub>Инструкция по работе с POSTMAN:<br>
![Screenshot with instructions for POSTMAN](https://zenclass-files-hot-01.storage.yandexcloud.net/0873bcaa-7dd7-47c5-a5e7-332f1a61a56f.png)
Нажимаем import (1 на скрине) и переносим два файла (*menu app.postman_collection.json* и *menu app.postman_environment.json*) в окно постман. Один файл - коллекция тестов, второй - переменные окружения.<br> 
В диалоговом окне подтверждаем импорт. После этого должна появиться коллекция (подчернута на скрине) menu app.<br>
Выбираем переменные окружения (2 на скрине) из выпадающего списка<br>
После этого можем зайти в коллекцию menu app и запустить каждый тест вручную. Для этого открываем коллекцию menu app, выбираем Тестовый сценарий -> CRUD для меню -> Просматривает список меню(или любой другой) у нас в центральной части появляется запрос, нажимаем Send и запрос летит в наше приложение.<br>
Если хотим запустит сразу всю коллекцию тестов, то жмем на три точки (3 на скрине) рядом с коллекцией и выбираем Run.</sub>
