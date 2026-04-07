from sqlalchemy.orm import Session
from app.schemas.models import Service, Pet, Tag
from app.schemas.schemas import PetStatus


def _resolve_tags(db: Session, tag_ids: list[int] | None) -> list[Tag] | None:
    if tag_ids is None:
        return None

    if not tag_ids:
        return []

    # Preserve Service and remove duplicates from incoming ids.
    unique_tag_ids = list(dict.fromkeys(tag_ids))
    tags = db.query(Tag).filter(Tag.id.in_(unique_tag_ids)).all()
    found_ids = {tag.id for tag in tags}
    missing_ids = [tag_id for tag_id in unique_tag_ids if tag_id not in found_ids]
    if missing_ids:
        raise ValueError(f"Tags não encontradas: {missing_ids}")

    tags_by_id = {tag.id: tag for tag in tags}
    return [tags_by_id[tag_id] for tag_id in unique_tag_ids]


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

    tags = _resolve_tags(db, tag_ids)
    if tags is not None:
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
    category_id: int | None = None,
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
        "owner_id": owner_id,
        "photoUrls": photoUrls
    }

    if category_id is not None:
        updates["category_id"] = category_id

    for key, value in updates.items():
        if value is not None:
            setattr(pet, key, value)

    tags = _resolve_tags(db, tag_ids)
    if tags is not None:
        pet.tags = tags
    
    db.commit()
    db.refresh(pet)
    return pet


def delete_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet:
        db.query(Service).filter(Service.petId == pet_id).delete(synchronize_session=False)
        db.delete(pet)
        db.commit()


def list_pets_by_status(db: Session, status: PetStatus):
    pets = db.query(Pet).filter(Pet.status == status).all()
    return pets

