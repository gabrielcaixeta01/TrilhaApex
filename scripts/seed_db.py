from datetime import datetime
from sqlalchemy import delete

from app.database import SessionLocal
from app.schemas.models import Category, Order, Pet, Tag, UserModel, pet_tags
from app.security import hash_password


def reset_and_seed() -> None:
    db = SessionLocal()
    try:
        # Clear dependent tables first to avoid foreign key issues.
        db.execute(delete(pet_tags))
        db.query(Order).delete()
        db.query(Pet).delete()
        db.query(UserModel).delete()
        db.query(Tag).delete()
        db.query(Category).delete()
        db.commit()

        categories = [
            Category(id=1, name="Cachorro"),
            Category(id=2, name="Gato"),
            Category(id=3, name="Ave"),
            Category(id=4, name="Roedor"),
            Category(id=5, name="Peixe"),
        ]
        db.add_all(categories)

        tags = [
            Tag(id=1, name="filhote"),
            Tag(id=2, name="vacinado"),
            Tag(id=3, name="castrado"),
            Tag(id=4, name="treinado"),
            Tag(id=5, name="adocao"),
            Tag(id=6, name="sociavel"),
            Tag(id=7, name="porte-pequeno"),
            Tag(id=8, name="porte-medio"),
            Tag(id=9, name="porte-grande"),
            Tag(id=10, name="especial"),
        ]
        db.add_all(tags)

        users = [
            UserModel(
                id=1,
                username="seed_admin",
                firstName="Ana",
                lastName="Silva",
                email="ana.silva@example.com",
                phone="11911110001",
                password_hash=hash_password("Senha@123"),
                role="admin",
                user_active=True,
            ),
            UserModel(
                id=2,
                username="seed_user_1",
                firstName="Bruno",
                lastName="Souza",
                email="bruno.souza@example.com",
                phone="11911110002",
                password_hash=hash_password("Senha@123"),
                role="user",
                user_active=True,
            ),
            UserModel(
                id=3,
                username="seed_user_2",
                firstName="Carla",
                lastName="Mendes",
                email="carla.mendes@example.com",
                phone="11911110003",
                password_hash=hash_password("Senha@123"),
                role="viewer",
                user_active=True,
            ),
            UserModel(
                id=4,
                username="seed_user_3",
                firstName="Diego",
                lastName="Lima",
                email="diego.lima@example.com",
                phone="11911110004",
                password_hash=hash_password("Senha@123"),
                role="user",
                user_active=False,
            ),
            UserModel(
                id=5,
                username="seed_user_4",
                firstName="Elisa",
                lastName="Costa",
                email="elisa.costa@example.com",
                phone="11911110005",
                password_hash=hash_password("Senha@123"),
                role="user",
                user_active=True,
            ),
            UserModel(
                id=6,
                username="seed_user_5",
                firstName="Felipe",
                lastName="Almeida",
                email="felipe.almeida@example.com",
                phone="11911110006",
                password_hash=hash_password("Senha@123"),
                role="user",
                user_active=True,
            ),
            UserModel(
                id=7,
                username="seed_user_6",
                firstName="Giovana",
                lastName="Ramos",
                email="giovana.ramos@example.com",
                phone="11911110007",
                password_hash=hash_password("Senha@123"),
                role="viewer",
                user_active=True,
            ),
            UserModel(
                id=8,
                username="seed_user_7",
                firstName="Henrique",
                lastName="Pereira",
                email="henrique.pereira@example.com",
                phone="11911110008",
                password_hash=hash_password("Senha@123"),
                role="user",
                user_active=True,
            ),
            UserModel(
                id=9,
                username="seed_user_8",
                firstName="Isabela",
                lastName="Nunes",
                email="isabela.nunes@example.com",
                phone="11911110009",
                password_hash=hash_password("Senha@123"),
                role="user",
                user_active=False,
            ),
            UserModel(
                id=10,
                username="seed_user_9",
                firstName="Joao",
                lastName="Oliveira",
                email="joao.oliveira@example.com",
                phone="11911110010",
                password_hash=hash_password("Senha@123"),
                role="user",
                user_active=True,
            ),
        ]
        db.add_all(users)

        tag_map = {tag.id: tag for tag in tags}
        pets = [
            Pet(id=1, name="Thor", photoUrls="https://pics.example/thor.jpg", status="available", category_id=1, owner_id=1),
            Pet(id=2, name="Luna", photoUrls="https://pics.example/luna.jpg", status="pending", category_id=2, owner_id=2),
            Pet(id=3, name="Pipoca", photoUrls="https://pics.example/pipoca.jpg", status="sold", category_id=3, owner_id=3),
            Pet(id=4, name="Nino", photoUrls="https://pics.example/nino.jpg", status="available", category_id=4, owner_id=4),
            Pet(id=5, name="Bidu", photoUrls="https://pics.example/bidu.jpg", status="pending", category_id=5, owner_id=5),
            Pet(id=6, name="Mel", photoUrls="https://pics.example/mel.jpg", status="available", category_id=1, owner_id=6),
            Pet(id=7, name="Fred", photoUrls="https://pics.example/fred.jpg", status="pending", category_id=2, owner_id=7),
            Pet(id=8, name="Nina", photoUrls="https://pics.example/nina.jpg", status="sold", category_id=3, owner_id=8),
            Pet(id=9, name="Bob", photoUrls="https://pics.example/bob.jpg", status="available", category_id=4, owner_id=9),
            Pet(id=10, name="Lilo", photoUrls="https://pics.example/lilo.jpg", status="pending", category_id=5, owner_id=10),
        ]
        pets[0].tags = [tag_map[1], tag_map[6]]
        pets[1].tags = [tag_map[2], tag_map[7]]
        pets[2].tags = [tag_map[3], tag_map[8]]
        pets[3].tags = [tag_map[4]]
        pets[4].tags = [tag_map[5]]
        pets[5].tags = [tag_map[6], tag_map[10]]
        pets[6].tags = [tag_map[7]]
        pets[7].tags = [tag_map[8], tag_map[2]]
        pets[8].tags = [tag_map[9]]
        pets[9].tags = [tag_map[10], tag_map[1]]
        db.add_all(pets)

        orders = [
            Order(id=1, petId=1, quantity=1, shipDate=datetime(2026, 3, 21, 10, 0, 0), status="placed", complete=False, owner_id=1),
            Order(id=2, petId=2, quantity=2, shipDate=datetime(2026, 3, 22, 10, 0, 0), status="approved", complete=False, owner_id=2),
            Order(id=3, petId=3, quantity=1, shipDate=datetime(2026, 3, 23, 10, 0, 0), status="delivered", complete=True, owner_id=3),
            Order(id=4, petId=4, quantity=3, shipDate=datetime(2026, 3, 24, 10, 0, 0), status="placed", complete=False, owner_id=4),
            Order(id=5, petId=5, quantity=1, shipDate=datetime(2026, 3, 25, 10, 0, 0), status="approved", complete=False, owner_id=5),
            Order(id=6, petId=6, quantity=2, shipDate=datetime(2026, 3, 26, 10, 0, 0), status="placed", complete=False, owner_id=6),
            Order(id=7, petId=7, quantity=1, shipDate=datetime(2026, 3, 27, 10, 0, 0), status="delivered", complete=True, owner_id=7),
            Order(id=8, petId=8, quantity=4, shipDate=datetime(2026, 3, 28, 10, 0, 0), status="approved", complete=False, owner_id=8),
            Order(id=9, petId=9, quantity=2, shipDate=datetime(2026, 3, 29, 10, 0, 0), status="placed", complete=False, owner_id=9),
            Order(id=10, petId=10, quantity=1, shipDate=datetime(2026, 3, 30, 10, 0, 0), status="approved", complete=False, owner_id=10),
        ]
        db.add_all(orders)

        db.commit()
        print("Seed concluido com sucesso.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    reset_and_seed()
