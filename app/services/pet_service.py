from sqlalchemy.orm import Session
from app.schemas.models import Pet


def create_pet(db: Session, name: str, photoUrls: str | None = None,
               status: str = "available", category_id: int | None = None):

    db_pet = Pet(
        name=name,
        photoUrls=photoUrls,
        status=status,
        category_id=category_id
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def get_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        return None
    return pet


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
    pets = db.query(Pet).filter(Pet.status == status).all()
    return pets

