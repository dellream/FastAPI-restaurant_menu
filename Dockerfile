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

COPY alembic.ini /project/

CMD ["bash", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
