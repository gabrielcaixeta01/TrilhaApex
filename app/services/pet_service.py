from scripts.script2 import Category
from sqlalchemy.orm import Session
from app.schemas.models import Pet, Category


def create_pet(db: Session, pet_id: int, name: str, category_id: int | None = None, 
               category_name: str | None = None, photoUrls: list[str] | None = None, 
               status: str = "available", tags: list[dict] | None = None):
    
    category = None
    if category_id or category_name:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            category = Category(id=category_id or 0, name=category_name or "")
            db.add(category)
            db.commit()
    
    db_pet = Pet(
        id=pet_id,
        name=name,
        photoUrls=",".join(photoUrls) if photoUrls else None,
        status=status,
        category_id=category.id if category else None
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def get_pet(db: Session, pet_id: int):
    return db.query(Pet).filter(Pet.id == pet_id).first()


def update_pet(db: Session, pet_id: int, **kwargs):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        return None
    
    for key, value in kwargs.items():
        if value is not None:
            setattr(pet, key, value)
    
    db.commit()
    db.refresh(pet)
    return pet


def delete_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet:
        db.delete(pet)
        db.commit()


def list_pets_by_status(db: Session, status: str):
    return db.query(Pet).filter(Pet.status == status).all()
