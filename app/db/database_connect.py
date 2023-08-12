from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Формируем строку для подключения
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



