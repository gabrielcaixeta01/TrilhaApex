from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Table
from sqlalchemy.orm import relationship
from app.database import Base


class Store(Base):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("nome", String(120), index=True, nullable=False)
    cnpj = Column(String(18), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    cep = Column(String(9), nullable=True)
    address = Column("endereco", String(255), nullable=True)
    city = Column(String)
    state = Column(String)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column("data_cadastro", DateTime, nullable=False, default=datetime.utcnow)

    users = relationship("UserModel", back_populates="store", passive_deletes=True)
    services = relationship("Service", back_populates="store", passive_deletes=True)

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column("nome", String(120), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column("senha_hash", String(255), nullable=False)
    role = Column("perfil", String(20), nullable=False)
    phone = Column("telefone", String)
    cpf = Column(String)
    cnpj = Column(String)
    client_type = Column("tipo_cliente", String(20))
    birth_date = Column("data_nascimento", Date)
    address = Column(String)
    job_title = Column("cargo", String(80))
    hired_at = Column("data_inicio", Date)
    store_id = Column("loja_id", Integer, ForeignKey("lojas.id", ondelete="CASCADE"), nullable=True)
    user_active = Column(Boolean, nullable=False, default=True)
    created_at = Column("data_cadastro", DateTime, nullable=False, default=datetime.utcnow)

    store = relationship("Store", back_populates="users")
    pets = relationship("Pet", back_populates="owner", foreign_keys="Pet.owner_id")
    client_services = relationship("Service", back_populates="client", foreign_keys="Service.client_id")
    worker_services = relationship("Service", back_populates="worker", foreign_keys="Service.worker_id")

    __table_args__ = (
        CheckConstraint("perfil IN ('cliente', 'funcionario', 'admin_loja', 'super_admin')", name="ck_users_profile"),
        CheckConstraint(
            "(perfil = 'funcionario') OR (perfil = 'admin_loja' AND loja_id IS NOT NULL) OR (perfil IN ('cliente', 'super_admin') AND loja_id IS NULL)",
            name="ck_users_store_by_profile",
        ),
    )


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String)

    pets = relationship("Pet", back_populates="category", cascade="all, delete-orphan", passive_deletes=True)
    
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String)

    pets = relationship("Pet", secondary="pet_tags", back_populates="tags")

class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("nome", String(120), index=True, nullable=False)
    species = Column("especie", String(60))
    breed = Column("raca", String(80))
    sex = Column("sexo", String(20))
    birth_date = Column("data_nascimento", Date)
    size = Column("porte", String(20))
    weight = Column("peso", Numeric(6, 2))
    health_notes = Column("observacoes_saude", String(500))
    status = Column(String(20), nullable=False, default="available")
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column("dono_id", Integer, ForeignKey("users.id"), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    category = relationship("Category", back_populates="pets")
    owner = relationship("UserModel", back_populates="pets", foreign_keys=[owner_id])
    tags = relationship("Tag", secondary="pet_tags", back_populates="pets")
    services = relationship("Service", back_populates="pet", passive_deletes=True)

pet_tags = Table(
    "pet_tags",
    Base.metadata,
    Column("pet_id", Integer, ForeignKey("pets.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Service(Base):
    __tablename__ = "atendimentos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_type = Column("tipo_servico", String(80), nullable=False)
    description = Column("descricao", String(500))
    service_at = Column("data_hora", DateTime, nullable=False)
    status = Column(String(30), nullable=False)
    price = Column("valor", Numeric(10, 2))
    discount = Column("desconto", Numeric(10, 2), default=0)
    payment_type = Column("forma_pagamento", String(40))
    observations = Column("observacoes", String(500))
    store_id = Column("loja_id", Integer, ForeignKey("lojas.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    client_id = Column("cliente_id", Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column("funcionario_id", Integer, ForeignKey("users.id"), nullable=False)

    store = relationship("Store", back_populates="services")
    pet = relationship("Pet", back_populates="services")
    client = relationship("UserModel", back_populates="client_services", foreign_keys=[client_id])
    worker = relationship("UserModel", back_populates="worker_services", foreign_keys=[worker_id])


Index(
    "ux_admin_loja_por_loja",
    UserModel.store_id,
    unique=True,
    sqlite_where=UserModel.role == "admin_loja",
)
