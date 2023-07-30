# Используем образ Python в качестве базового образа
FROM python:3.10-slim

# Установим переменную окружения для предотвращения запуска приложения не в интерактивном режиме
ENV PYTHONUNBUFFERED 1

# Установим рабочую директорию
WORKDIR /app

# Установим зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем файлы миграций Alembic в контейнер
COPY migrations /app/migrations

# Скопируем файлы вашего FastAPI приложения в контейнер
COPY src /app/src

# Документируем порт контейнера, на котором будет работать Uvicorn
EXPOSE 8000

# Запустим миграции Alembic для создания базы данных
RUN alembic upgrade head

# Запустим Uvicorn при старте контейнера
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
