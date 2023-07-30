# Используйте образ Python в качестве базового образа
FROM python:3.10-slim

# Установите переменную окружения для предотвращения запуска приложения не в интерактивном режиме
ENV PYTHONUNBUFFERED 1

# Установите рабочую директорию
WORKDIR /app

# Установите зависимости для выполнения тестов
COPY ../../test_requirements.txt /app/
RUN pip install --no-cache-dir -r test_requirements.txt

# Скопируйте файлы тестов в контейнер
COPY tests /app/tests

# Запустите тесты с помощью pytest при старте контейнера
CMD ["pytest"]
