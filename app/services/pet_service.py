from sqlalchemy.orm import Session
from app.schemas.models import Pet, Category


def create_pet(db: Session, name: str, category_name: str | None = None,
               photoUrls: list[str] | None = None,
               status: str = "available", tags: list[dict] | None = None):

    category = None
    if category_name:
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.flush()
    
    db_pet = Pet(
        name=name,
        photoUrls=",".join(photoUrls) if photoUrls else None,
        status=status,
        category_id=category.id if category else None
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return _pet_to_dict(db_pet)


def get_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        return None
    return _pet_to_dict(pet)


def update_pet(db: Session, pet_id: int, **kwargs):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        return None
    
    for key, value in kwargs.items():
        if value is not None:
            setattr(pet, key, value)
    
    db.commit()
    db.refresh(pet)
    return _pet_to_dict(pet)


def delete_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet:
        db.delete(pet)
        db.commit()


def list_pets_by_status(db: Session, status: str):
    pets = db.query(Pet).filter(Pet.status == status).all()
    return [_pet_to_dict(pet) for pet in pets]


def _pet_to_dict(pet: Pet) -> dict:
    photo_urls = pet.photoUrls.split(",") if pet.photoUrls else []
    return {
        "id": pet.id,
        "name": pet.name,
        "status": pet.status,
        "photoUrls": photo_urls,
        "category": {
            "id": pet.category.id,
            "name": pet.category.name,
        } if pet.category else None,
        "tags": [],
    }
