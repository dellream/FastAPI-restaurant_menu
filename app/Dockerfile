# Используем образ Python в качестве базового образа
FROM python:3.10-slim

# Установим переменную окружения для предотвращения запуска приложения не в интерактивном режиме
ENV PYTHONUNBUFFERED 1

# Установим рабочую директорию
WORKDIR /app

# Установим зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем файлы alembic.ini
COPY alembic.ini /app/

# Скопируем файлы миграций Alembic в контейнер
COPY migrations /app/migrations

# Скопируем файлы FastAPI приложения в контейнер
COPY . /app/

# Документируем порт контейнера, на котором будет работать Uvicorn
EXPOSE 8000


