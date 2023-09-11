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
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')

# Переменные для подключения к Redis
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

EXPIRATION = 3600


# Для переключения между докером и локалом необходимо закомментировать соответствующие переменные
# Общие переменные (используются в тестах)
BASE_URL = 'http://localhost:8000/api/v1'  # Локальный
# BASE_URL = 'http://backend:8000/api/v1'  # Для докера

# Переменные для подключения к Redis
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'  # Локальный
# REDIS_URL = f'redis://redis:{REDIS_PORT}/0'  # Для докера

# Данные для database_connect
# Локальный:
SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# Для Докера:
# SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_DOCKER_HOST}:{DB_PORT}/{DB_NAME}'

# Данные для celery и rabbitmq
RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_DEFAULT_PORT = os.getenv('RABBITMQ_DEFAULT_PORT')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
CELERY_STATUS = os.getenv('CELERY_STATUS') == 'true'
# Для Докера:
# MENU_FILE_PATH = '/project/app/admin/Menu.xlsx'
# Локальный:
MENU_FILE_PATH = '/app/admin/Menu.xlsx'
