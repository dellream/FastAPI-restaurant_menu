import os

from dotenv import load_dotenv

load_dotenv()

# Переменные для подключения к Postgresql
DB_HOST = os.environ.get('DB_HOST')
DB_DOCKER_HOST = os.environ.get('DB_DOCKER_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Общие переменные (используются в тестах)
BASE_URL = 'http://localhost:8000/api/v1'
DOCKER_URL = 'http://backend:8000/api/v1'

# Переменные для подключения к Redis
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
# REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'  # Локальный
REDIS_URL = f'redis://redis:{REDIS_PORT}/0'  # Для докера
EXPIRATION = 3600

# # Переменные для Docker-compose
# DOCKER_POSTGRES_USER = os.environ.get('DOCKER_POSTGRES_USER')
# DOCKER_POSTGRES_DBNAME = os.environ.get('DOCKER_POSTGRES_DBNAME')

# Данные для database_connect
# SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'  # Локальный
SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://' \
                          f'{DB_USER}:{DB_PASSWORD}@{DB_DOCKER_HOST}:{DB_PORT}/{DB_NAME}'  # Для Докера
