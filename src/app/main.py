import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import List

from .schemas import MenuSchema, SubmenuSchema, DishSchema, SubmenuCreate, DishCreate
from .models import Menu, Submenu, Dish

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1231@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Menu CRUD endpoints
@app.post("/api/v1/menus/", response_model=MenuSchema)  # Use MenuSchema for response
def create_menu(menu: MenuSchema, db: Session = Depends(get_db)):
    try:
        # Создаем объект сущности SQLAlchemy на основе данных из схемы Pydantic
        menu_obj = Menu(title=menu.title, description=menu.description)
        db.add(menu_obj)
        db.commit()
        db.refresh(menu_obj)

        menu_data = {
            "id": str(menu_obj.id),
            "title": menu_obj.title,
            "description": menu_obj.description,
            "submenus": [],
            "submenus_count": 0,
            "dishes_count": 0,
        }

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=menu_data)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Menu with this title already exists")


@app.get("/api/v1/menus/", response_model=List[MenuSchema])
def read_menus(db: Session = Depends(get_db)):
    return db.query(Menu).all()


@app.get("/api/v1/menus/{menu_id}/", response_model=MenuSchema)
def read_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()

    if menu:
        # Получаем количество подменю (submenus_count) и блюд (dishes_count) для данного меню
        submenus_count = db.query(Submenu).filter_by(menu_id=menu_id).count()
        dishes_count = db.query(Dish).join(Submenu).filter(Submenu.menu_id == menu_id).count()

        menu_data = {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": submenus_count,  # Количество подменю
            "dishes_count": dishes_count,  # Количество блюд
            "submenus": []
        }

        return JSONResponse(content=menu_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")


@app.patch("/api/v1/menus/{menu_id}/", response_model=MenuSchema)
def update_menu(menu_id: str, updated_menu: MenuSchema, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    for field, value in updated_menu.dict(exclude_unset=True).items():
        setattr(menu, field, value)
    db.commit()
    db.refresh(menu)
    return menu


@app.delete("/api/v1/menus/{menu_id}/", response_model=MenuSchema)
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    db.delete(menu)
    db.commit()
    return menu


# Submenu CRUD endpoints
@app.post("/api/v1/menus/{menu_id}/submenus/", response_model=SubmenuSchema)
def create_submenu(menu_id: str, submenu: SubmenuSchema, db: Session = Depends(get_db)):
    # Создаем объект сущности SQLAlchemy на основе данных из схемы Pydantic
    submenu_obj = Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(submenu_obj)
    db.commit()
    db.refresh(submenu_obj)

    submenu_data = {
        "id": str(submenu_obj.id),
        "title": submenu_obj.title,
        "description": submenu_obj.description,
        "menu_id": str(submenu_obj.menu_id)
    }

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=submenu_data)


@app.get("/api/v1/menus/{menu_id}/submenus/", response_model=List[SubmenuSchema])
def read_submenus(db: Session = Depends(get_db)):
    return db.query(Submenu).all()


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/", response_model=SubmenuSchema)
def read_submenu(submenu_id: str, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()

    if submenu:
        # Получаем количество блюд (dishes_count) для данного подменю
        dishes_count = db.query(Dish).filter_by(submenu_id=submenu_id).count()

        submenu_data = {
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "menu_id": str(submenu.menu_id),
            "dishes_count": dishes_count,  # Количество блюд в подменю
        }

        return JSONResponse(content=submenu_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/", response_model=SubmenuSchema)
def update_submenu(submenu_id: str, updated_submenu: SubmenuSchema, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    for field, value in updated_submenu.dict(exclude_unset=True).items():
        setattr(submenu, field, value)
    db.commit()
    db.refresh(submenu)
    return submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/", response_model=SubmenuSchema)
def delete_submenu(submenu_id: str, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    db.delete(submenu)
    db.commit()
    return submenu


# Dish CRUD endpoints
@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", response_model=DishSchema)
def create_dish(menu_id: str, submenu_id: str, dish: DishCreate, db: Session = Depends(get_db)):
    try:
        # Создаем объект сущности SQLAlchemy на основе данных из схемы Pydantic
        dish_obj = Dish(title=dish.title, price=dish.price, submenu_id=submenu_id)
        db.add(dish_obj)
        db.commit()
        db.refresh(dish_obj)

        dish_data = {
            "id": str(dish_obj.id),
            "title": dish_obj.title,
            "description": dish_obj.description,
            "price": str(dish_obj.price),
            "submenu_id": str(dish_obj.submenu_id)
        }

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=dish_data)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="dish with this name already exists")


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", response_model=List[DishSchema])
def read_dishes(db: Session = Depends(get_db)):
    return db.query(Dish).all()


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/", response_model=DishSchema)
def read_dish(dish_id: str, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish:
        dish_data = {
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": str(dish.price),
        }

        return JSONResponse(content=dish_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/", response_model=DishSchema)
def update_dish(dish_id: str, updated_dish: DishSchema, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

    for field, value in updated_dish.dict(exclude_unset=True).items():
        setattr(dish, field, value)

    db.commit()
    db.refresh(dish)

    # Преобразуем price в строку перед созданием словаря для JSON-ответа
    dish_data = {
        "id": str(dish.id),
        "title": dish.title,
        "description": dish.description,
        "price": str(dish.price),
    }

    return JSONResponse(content=dish_data)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/", response_model=DishSchema)
def delete_dish(dish_id: str, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    db.delete(dish)
    db.commit()
    return dish


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
