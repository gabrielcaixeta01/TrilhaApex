from sqlalchemy.orm import Session
from app.schemas.models import Pet, Tag
from app.schemas.schemas import PetStatus


def create_pet(
    db: Session,
    name: str,
    category_id: int,
    photoUrls: str | None = None,
    status: PetStatus | None = None,
    tag_ids: list[int] | None = None,
    owner_id: int | None = None,
):

    db_pet = Pet(
        name=name,
        photoUrls=photoUrls,
        status=status,
        category_id=category_id,
        owner_id=owner_id,
    )

    if tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
        db_pet.tags = tags

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
    category_id: int,
    name: str | None = None,
    status: PetStatus | None = None,
    tag_ids: list[int] | None = None,
    owner_id: int | None = None,
    photoUrls: str | None = None
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        return None

    updates = {
        "name": name,
        "status": status,
        "category_id": category_id,
        "owner_id": owner_id,
        "photoUrls": photoUrls
    }

    for key, value in updates.items():
        if value is not None:
            setattr(pet, key, value)

    if tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
        pet.tags = tags
    
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

