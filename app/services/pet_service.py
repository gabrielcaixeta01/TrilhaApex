from sqlalchemy.orm import Session
from app.schemas.models import Pet
from app.schemas.schemas import PetStatus


def create_pet(
    db: Session,
    name: str,
    photoUrls: str | None = None,
    status: PetStatus | None = None,
    category_id: int | None = None,
    owner_id: int | None = None,
):

    db_pet = Pet(name=name, photoUrls=photoUrls, status=status, category_id=category_id, owner_id=owner_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def get_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        return None
    return pet


def update_pet(
    db: Session,
    pet_id: int,
    name: str | None = None,
    status: PetStatus | None = None,
    category_id: int | None = None,
    owner_id: int | None = None,
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        return None

    updates = {
        "name": name,
        "status": status,
        "category_id": category_id,
        "owner_id": owner_id,
    }

    for key, value in updates.items():
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


def list_pets_by_status(db: Session, status: PetStatus):
    pets = db.query(Pet).filter(Pet.status == status).all()
    return pets

