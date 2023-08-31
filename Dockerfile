# Используем образ Python в качестве базового образа
FROM python:3.10-slim

# Установим переменную окружения для предотвращения запуска приложения не в интерактивном режиме
ENV PYTHONUNBUFFERED 1

# Установим рабочую директорию
WORKDIR /project/

# Установим зависимости
COPY requirements.txt /project/

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Скопируем файлы FastAPI приложения в контейнер
COPY app /project/app
COPY migrations /project/migrations
COPY tests /project/tests

COPY alembic.ini /project/

# Документируем порт контейнера, на котором будет работать Uvicorn
EXPOSE 8000
