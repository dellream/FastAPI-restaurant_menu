import uuid
from sqlalchemy import Column, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Menu(Base):
    __tablename__ = 'menus'

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=str(uuid.uuid4))
    title = Column(String, index=True, nullable=False)
    description = Column(String)

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan, delete")


class Submenu(Base):
    __tablename__ = 'submenus'

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=str(uuid.uuid4))
    title = Column(String, index=True, nullable=False)
    description = Column(String)

    # menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'), nullable=False)
    menu_id = Column(String, ForeignKey('menus.id'), nullable=False)
    menu = relationship("Menu", back_populates="submenus")

    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")


class Dish(Base):
    __tablename__ = 'dishes'

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=str(uuid.uuid4))
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    # price = Column(Numeric(precision=10, scale=2), nullable=False)
    price = Column(String, nullable=False)  # Изменил тип данных на строковый

    # submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'), nullable=False)
    submenu_id = Column(String, ForeignKey('submenus.id'), nullable=False)
    submenu = relationship("Submenu", back_populates="dishes")
