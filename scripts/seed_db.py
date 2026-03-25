from datetime import UTC, datetime, timedelta

from app.database import Base, SessionLocal, engine
from app.schemas.models import Category, Order, Pet, Tag, UserModel
from app.security import hash_password


CATEGORY_DATA = [
    {"id": 9101, "name": "Cachorro"},
    {"id": 9102, "name": "Gato"},
    {"id": 9103, "name": "Ave"},
    {"id": 9104, "name": "Roedor"},
    {"id": 9105, "name": "Peixe"},
]

TAG_DATA = [
    {"id": 9201, "name": "filhote"},
    {"id": 9202, "name": "vacinado"},
    {"id": 9203, "name": "castrado"},
    {"id": 9204, "name": "treinado"},
    {"id": 9205, "name": "adocao"},
]

PET_DATA = [
    {"id": 9301, "name": "Thor", "photoUrls": "https://pics.example/thor.jpg", "status": "available", "category_id": 9101},
    {"id": 9302, "name": "Luna", "photoUrls": "https://pics.example/luna.jpg", "status": "pending", "category_id": 9102},
    {"id": 9303, "name": "Pipoca", "photoUrls": "https://pics.example/pipoca.jpg", "status": "sold", "category_id": 9103},
    {"id": 9304, "name": "Nino", "photoUrls": "https://pics.example/nino.jpg", "status": "available", "category_id": 9104},
    {"id": 9305, "name": "Bidu", "photoUrls": "https://pics.example/bidu.jpg", "status": "pending", "category_id": 9105},
]

ORDER_DATA = [
    {"id": 9401, "petId": 9301, "quantity": 1, "shipDate": datetime.now(UTC) + timedelta(days=1), "status": "placed", "complete": False},
    {"id": 9402, "petId": 9302, "quantity": 2, "shipDate": datetime.now(UTC) + timedelta(days=2), "status": "approved", "complete": False},
    {"id": 9403, "petId": 9303, "quantity": 1, "shipDate": datetime.now(UTC) + timedelta(days=3), "status": "delivered", "complete": True},
    {"id": 9404, "petId": 9304, "quantity": 3, "shipDate": datetime.now(UTC) + timedelta(days=4), "status": "placed", "complete": False},
    {"id": 9405, "petId": 9305, "quantity": 1, "shipDate": datetime.now(UTC) + timedelta(days=5), "status": "approved", "complete": False},
]

USER_DATA = [
    {
        "id": 9501,
        "username": "seed_admin",
        "firstName": "Ana",
        "lastName": "Silva",
        "email": "ana.silva@example.com",
        "phone": "11911110001",
        "user_active": True,
        "role": "admin",
    },
    {
        "id": 9502,
        "username": "seed_user_1",
        "firstName": "Bruno",
        "lastName": "Souza",
        "email": "bruno.souza@example.com",
        "phone": "11911110002",
        "user_active": True,
        "role": "user",
    },
    {
        "id": 9503,
        "username": "seed_user_2",
        "firstName": "Carla",
        "lastName": "Mendes",
        "email": "carla.mendes@example.com",
        "phone": "11911110003",
        "user_active": True,
        "role": "viewer",
    },
    {
        "id": 9504,
        "username": "seed_user_3",
        "firstName": "Diego",
        "lastName": "Lima",
        "email": "diego.lima@example.com",
        "phone": "11911110004",
        "user_active": False,
        "role": "user",
    },
    {
        "id": 9505,
        "username": "seed_user_4",
        "firstName": "Elisa",
        "lastName": "Costa",
        "email": "elisa.costa@example.com",
        "phone": "11911110005",
        "user_active": True,
        "role": "user",
    },
]


def upsert_by_id(db, model, payload):
    record = db.query(model).filter(model.id == payload["id"]).first()
    if record:
        for key, value in payload.items():
            setattr(record, key, value)
        return record

    record = model(**payload)
    db.add(record)
    return record


def upsert_users(db):
    for payload in USER_DATA:
        password_hash = hash_password("senha123")
        final_payload = {**payload, "password_hash": password_hash}

        record = db.query(UserModel).filter(UserModel.username == payload["username"]).first()
        if record:
            for key, value in final_payload.items():
                setattr(record, key, value)
            continue

        db.add(UserModel(**final_payload))


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        for payload in CATEGORY_DATA:
            upsert_by_id(db, Category, payload)

        for payload in TAG_DATA:
            upsert_by_id(db, Tag, payload)

        for payload in PET_DATA:
            upsert_by_id(db, Pet, payload)

        for payload in ORDER_DATA:
            upsert_by_id(db, Order, payload)

        upsert_users(db)
        db.commit()

        print("Banco populado com sucesso.")
        print(f"categories: {db.query(Category).count()}")
        print(f"tags: {db.query(Tag).count()}")
        print(f"pets: {db.query(Pet).count()}")
        print(f"orders: {db.query(Order).count()}")
        print(f"users: {db.query(UserModel).count()}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
