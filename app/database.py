import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DEFAULT_SQLITE_URL = "sqlite:///./petstore.db"


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://") :]

    if url.startswith("postgresql://") and "+" not in url.split("://", 1)[0]:
        return "postgresql+psycopg://" + url[len("postgresql://") :]

    return url


raw_database_url = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL).strip()
DATABASE_URL = normalize_database_url(raw_database_url or DEFAULT_SQLITE_URL)

engine_kwargs = {"echo": False}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def initialize_database() -> None:
    """Create base tables and apply lightweight compatibility fixes."""
    from app.schemas import models  # noqa: F401  # ensure models are registered on Base metadata

    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_appointment_pet_id_column()
    _backfill_sqlite_appointment_pet_id()


def _ensure_sqlite_appointment_pet_id_column() -> None:
    if engine.dialect.name != "sqlite":
        return

    inspector = inspect(engine)
    if "appointments" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("appointments")}
    if "pet_id" in existing_columns:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE appointments ADD COLUMN pet_id INTEGER"))


def _backfill_sqlite_appointment_pet_id() -> None:
    if engine.dialect.name != "sqlite":
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                UPDATE appointments
                SET pet_id = COALESCE(
                    (
                        SELECT MIN(p.id)
                        FROM pets p
                        WHERE p.owner_id = appointments.client_id
                    ),
                    (SELECT MIN(p2.id) FROM pets p2)
                )
                WHERE pet_id IS NULL
                """
            )
        )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()