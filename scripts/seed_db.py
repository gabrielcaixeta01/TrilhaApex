from datetime import UTC, datetime, timedelta

from app.database import SessionLocal
from app.schemas.models import Category, Order, Pet, Tag, User


def get_or_create_category(db, name: str) -> Category:
    category = db.query(Category).filter(Category.name == name).first()
    if category:
        return category
    category = Category(name=name)
    db.add(category)
    db.flush()
    return category


def get_or_create_tag(db, name: str) -> Tag:
    tag = db.query(Tag).filter(Tag.name == name).first()
    if tag:
        return tag
    tag = Tag(name=name)
    db.add(tag)
    db.flush()
    return tag


def get_or_create_pet(db, name: str, status: str, category: Category, photo_url: str) -> Pet:
    pet = db.query(Pet).filter(Pet.name == name).first()
    if pet:
        pet.status = status
        pet.category_id = category.id
        pet.photoUrls = photo_url
        return pet

    pet = Pet(
        name=name,
        status=status,
        category_id=category.id,
        photoUrls=photo_url,
    )
    db.add(pet)
    db.flush()
    return pet


def get_or_create_user(
    db,
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
) -> User:
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.password = password
        user.firstName = first_name
        user.lastName = last_name
        user.email = email
        user.phone = phone
        return user

    user = User(
        username=username,
        password=password,
        firstName=first_name,
        lastName=last_name,
        email=email,
        phone=phone,
        userStatus=1,
    )
    db.add(user)
    db.flush()
    return user


def get_or_create_order(db, pet_id: int, quantity: int, status: str, complete: bool) -> Order:
    order = (
        db.query(Order)
        .filter(Order.petId == pet_id, Order.quantity == quantity, Order.status == status)
        .first()
    )
    if order:
        order.complete = complete
        return order

    order = Order(
        petId=pet_id,
        quantity=quantity,
        shipDate=datetime.now(UTC) + timedelta(days=2),
        status=status,
        complete=complete,
    )
    db.add(order)
    db.flush()
    return order


def run_seed() -> None:
    db = SessionLocal()
    try:
        dog = get_or_create_category(db, "Dogs")
        cat = get_or_create_category(db, "Cats")
        bird = get_or_create_category(db, "Birds")

        get_or_create_tag(db, "friendly")
        get_or_create_tag(db, "adopted")
        get_or_create_tag(db, "young")

        rex = get_or_create_pet(
            db, "Rex", "available", dog, "https://img.example/rex.png"
        )
        mia = get_or_create_pet(
            db, "Mia", "pending", cat, "https://img.example/mia.png"
        )
        get_or_create_pet(db, "Piu", "sold", bird, "https://img.example/piu.png")

        get_or_create_user(
            db,
            "admin",
            "admin123",
            "Gabriel",
            "Romero",
            "admin@apex.local",
            "11999990000",
        )
        get_or_create_user(
            db,
            "ana",
            "ana123",
            "Ana",
            "Silva",
            "ana@apex.local",
            "11988887777",
        )

        get_or_create_order(db, rex.id, 1, "placed", False)
        get_or_create_order(db, mia.id, 2, "approved", True)

        db.commit()
        print("Seed concluido com sucesso.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
