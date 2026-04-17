from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas.models import Pet


def create_pet(
    db: Session,
    name: str,
    breed: str,
    sex: str,
    size: str,
    weight: float,
    category_id: int,
    owner_id: int,
    health_notes: str | None = None,
):
    name = name.strip() if name else name

    if not name:
        raise HTTPException(status_code=400, detail="Nome do pet é obrigatório")

    if category_id is None:
        raise HTTPException(status_code=400, detail="Categoria do pet é obrigatória")

    if owner_id is None:
        raise HTTPException(status_code=400, detail="Dono do pet é obrigatório para criar pet")

    duplicated_pet = (
        db.query(Pet)
        .filter(Pet.owner_id == owner_id, func.lower(Pet.name) == name.lower())
        .first()
    )
    if duplicated_pet:
        raise HTTPException(status_code=400, detail="Este dono já possui um pet com esse nome")

    db_pet = Pet(
        name=name,
        breed=breed,
        sex=sex,
        size=size,
        weight=weight,
        health_notes=health_notes,
        category_id=category_id,
        owner_id=owner_id,
    )

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
):
    pet = get_pet(db, pet_id)

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

    if pet.name is not None:
        pet.name = pet.name.strip()

    if not pet.name:
        raise HTTPException(status_code=400, detail="Nome do pet é obrigatório")

    if pet.category_id is None:
        raise HTTPException(status_code=400, detail="Categoria do pet é obrigatória")

    if pet.owner_id is None:
        raise HTTPException(status_code=400, detail="Dono do pet é obrigatório")

    duplicated_pet = (
        db.query(Pet)
        .filter(
            Pet.id != pet_id,
            Pet.owner_id == pet.owner_id,
            func.lower(Pet.name) == pet.name.lower(),
        )
        .first()
    )
    if duplicated_pet:
        raise HTTPException(status_code=400, detail="Este dono já possui um pet com esse nome")

  
    db.commit()
    db.refresh(pet)
    return pet


def delete_pet(db: Session, pet_id: int):
    pet = get_pet(db, pet_id)
    db.delete(pet)
    db.commit()


def list_pets( db: Session) -> list[Pet]:
    return db.query(Pet).order_by(Pet.id).all()

