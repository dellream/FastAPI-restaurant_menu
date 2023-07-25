<h1 style="color: #008080; border-bottom: 1px solid #008080;">REST API для работы с меню ресторана</h1>

<h3 style="color: #0000FF; border-bottom: 1px solid #0000FF;">Описание проекта</h3>

<p>Этот проект представляет собой REST API для работы с меню ресторана.<br>
Основная цель данного тестового задания - пройти 161 тест в Postman, которые проверяют функциональность API.<br>
Проект реализован с использованием FastAPI и PostgreSQL в качестве базы данных.</p>

<h3 style="color: #0000FF; border-bottom: 1px solid #0000FF;">Установка и настройка проекта</h3>
<ol>
  <li>Убедитесь, что у вас установлен Python версии 3.7 или выше.</li>
  <li>Клонируйте репозиторий с GitHub: git clone https://github.com/dellream/REST-API-app_test_task.git</li>
  <li>Перейдите в каталог проекта</li>
  <li>Установите зависимости: `pip install -r requirements.txt`</li>
  <li>Убедитесь, что у вас установлен PostgreSQL и создайте базу данных для проекта.</li>
</ol>

<h3 style="color: #0000FF; border-bottom: 1px solid #0000FF;">Настройка базы данных</h3>
<ol>
  <li>Установите PostgreSQL: Убедитесь, что PostgreSQL установлен на вашей системе и работает.<br>
      Если его нет, установите PostgreSQL, а также инструмент командной строки psql, который позволяет взаимодействовать с базой данных.</li>
  <li>Создайте базу данных: Откройте командную строку или терминал и используйте psql, чтобы подключиться к PostgreSQL и создать базу данных для вашего проекта:</li>
  <li>В файле **main.py** необходимо изменить строку (вставьте свои данные) `SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/database_name"`</li>
  <li>Повторите тоже самое для файла **alembic.ini**, нужно изменить строку `sqlalchemy.url = postgresql://username:password@host:port/database_name`</li>
  <li>Создайте ревизию alembic: `alembic revision --autogenerate -m "Описание вашей ревизии"`</li>
  <li>Выполните миграцию: `alembic upgrade head`</li>
</ol>

<h3 style="color: #0000FF; border-bottom: 1px solid #0000FF;">Запуск проекта</h3>
<ol>
  <li>Запустите сервер: `uvicorn main:app --reload`</li>
  <li>API должно быть доступно по адресу, указанному в консоли</li>
</ol>
