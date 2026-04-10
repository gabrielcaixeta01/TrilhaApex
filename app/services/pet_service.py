from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.models import Pet
from app.schemas.schemas import PetStatus


def create_pet(
    db: Session,
    name: str,
    breed: str | None = None,
    sex: str | None = None,
    size: str | None = None,
    weight: float | None = None,
    health_notes: str | None = None,
    category_id: int | None = None,
    owner_id: int | None = None,
    species: str | None = None,
    birth_date: str | None = None,
    status: PetStatus | None = None,
    active: bool = True,
):
    if owner_id is None:
        raise HTTPException(status_code=400, detail="Dono do pet é obrigatório para criar pet")

    pet_data = {
        "name": name,
        "breed": breed,
        "sex": sex,
        "size": size,
        "weight": weight,
        "health_notes": health_notes,
        "category_id": category_id,
        "owner_id": owner_id,
    }

    db_pet = Pet(**pet_data)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def get_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet


def update_pet(
    db: Session,
    pet_id: int,
    name: str | None = None,
    breed: str | None = None,
    sex: str | None = None,
    size: str | None = None,
    weight: float | None = None,
    health_notes: str | None = None,
    category_id: int | None = None,
    owner_id: int | None = None,
    species: str | None = None,
    birth_date: str | None = None,
    status: PetStatus | None = None,
    active: bool | None = None,
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    updates = {
        "name": name,
        "breed": breed,
        "sex": sex,
        "size": size,
        "weight": weight,
        "health_notes": health_notes,
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
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    db.delete(pet)
    db.commit()

