import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development").strip().lower()

_raw_database_url = os.getenv("DATABASE_URL")
if APP_ENV == "production" and not _raw_database_url:
    # Sem esse guard a aplicacao sobe em SQLite num disco efemero: tudo o que
    # for gravado desaparece no proximo restart, e sem nenhum erro visivel.
    raise RuntimeError("DATABASE_URL deve ser definida quando APP_ENV=production")

DATABASE_URL = _raw_database_url or "sqlite:///./petstore.db"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs = {"connect_args": {"check_same_thread": False}}
else:
    # Conexoes ociosas sao derrubadas pelo provedor gerenciado; sem isso a
    # primeira query depois de um periodo parado falha com
    # "server closed the connection unexpectedly".
    engine_kwargs = {"pool_pre_ping": True, "pool_recycle": 300}

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency para usar em rotas do FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()