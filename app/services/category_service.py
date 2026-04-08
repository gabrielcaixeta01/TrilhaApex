from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.models import Category


def create_category(db: Session, name: str, description: str | None = None):
    exists = db.query(Category).filter(Category.name == name).first()

    if exists:
        raise HTTPException(status_code=400, detail="Categoria já existe")
    
    db_category = Category(name=name, description=description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

def update_category(db: Session, category_id: int, name: str, description: str | None = None):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    if name is not None:
        if db.query(Category).filter(Category.name == name, Category.id != category_id).first():
            raise HTTPException(status_code=400, detail="Outra categoria já existe com esse nome")
        
        category.name = name
    
    if description is not None:
        category.description = description

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.delete(category)
    db.commit()
    return category

def list_categories(db: Session):
    return db.query(Category).all()