from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Table
from sqlalchemy.orm import relationship

from app.database import Base


class Store(Base):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("nome", String(120), index=True, nullable=False)
    cnpj = Column(String(18), nullable=False, unique=True)
    phone = Column("telefone", String(20), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    active = Column("ativo", Boolean, nullable=False, default=True)
    created_at = Column("data_cadastro", DateTime, nullable=False, default=datetime.utcnow)
    cep = Column("end_cep", String(9), nullable=False)
    city = Column("end_cidade", String(120), nullable=False)
    state = Column("end_estado", String(2), nullable=False)
    address = Column("end_rua", String(255), nullable=False)
    neighborhood = Column("end_bairro", String(120), nullable=False)
    number = Column("end_numero", String(20), nullable=False)

    employees = relationship("EmployeeModel", back_populates="store", passive_deletes=True)
    appointments = relationship("Appointment", back_populates="store", passive_deletes=True)


class UserModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("nome", String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column("senha_hash", String(255), nullable=False)
    phone = Column("telefone", String(20), nullable=False)
    role = Column("tipo_perfil", String(20), nullable=False)
    cpf = Column(String(14))
    cnpj = Column(String(18))
    active = Column("ativo", Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    created_at = Column("data_cadastro", DateTime, nullable=False, default=datetime.utcnow)

    client_profile = relationship(
        "ClientModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    employee_profile = relationship(
        "EmployeeModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ClientModel(Base):
    __tablename__ = "clientes"

    user_id = Column("usuario_id", Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    client_type = Column("tipo_cliente", String(20), nullable=False)
    cep = Column("end_cep", String(9), nullable=False)
    state = Column("end_estado", String(2), nullable=False)
    city = Column("end_cidade", String(120), nullable=False)

    user = relationship("UserModel", back_populates="client_profile")
    pets = relationship("Pet", back_populates="owner", passive_deletes=True)
    appointments = relationship("Appointment", back_populates="client", passive_deletes=True)


class EmployeeModel(Base):
    __tablename__ = "funcionarios"

    user_id = Column("usuario_id", Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    matricula = Column(String(20), nullable=False, unique=True)
    job_title = Column("cargo", String(80), nullable=False)
    salary = Column("salario", Numeric(10, 2), nullable=False)
    hired_at = Column("data_contratacao", Date, nullable=False)
    store_id = Column("loja_id", Integer, ForeignKey("lojas.id", ondelete="CASCADE"), nullable=False)

    user = relationship("UserModel", back_populates="employee_profile")
    store = relationship("Store", back_populates="employees")
    appointments = relationship("Appointment", back_populates="worker", passive_deletes=True)


class Category(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("nome", String(80), index=True, unique=True, nullable=False)
    description = Column("descricao", String(255))

    pets = relationship("Pet", back_populates="category", cascade="all, delete-orphan", passive_deletes=True)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("nome", String(80), index=True, unique=True, nullable=False)
    description = Column("descricao", String(255))

    pets = relationship("Pet", secondary="pet_tags", back_populates="tags")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("nome", String(120), index=True)
    breed = Column("raca", String(80))
    sex = Column("sexo", String(20))
    size = Column("porte", String(20))
    weight = Column("peso", Numeric(6, 2))
    health_notes = Column("observacoes_saude", String(500))
    category_id = Column("categoria_id", Integer, ForeignKey("categorias.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column("dono_id", Integer, ForeignKey("clientes.usuario_id", ondelete="CASCADE"), nullable=False)

    category = relationship("Category", back_populates="pets")
    owner = relationship("ClientModel", back_populates="pets")
    tags = relationship("Tag", secondary="pet_tags", back_populates="pets")


pet_tags = Table(
    "pet_tags",
    Base.metadata,
    Column("pet_id", Integer, ForeignKey("pets.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Service(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("nome", String(120), nullable=False)
    description = Column("descricao", String(500))
    price = Column("preco", Numeric(10, 2), nullable=False)

    appointment_links = relationship("AppointmentService", back_populates="service", passive_deletes=True)


class Appointment(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value_final = Column("valor_final", Numeric(10, 2), nullable=False)
    service_at = Column("data_atendimento", DateTime, nullable=False, default=datetime.utcnow)
    payment_type = Column("forma_pagamento", String(20), nullable=False)
    status = Column(String(20), nullable=False)
    online = Column(Boolean, nullable=False, default=False)
    observations = Column("observacoes", String(500))
    store_id = Column("loja_id", Integer, ForeignKey("lojas.id", ondelete="CASCADE"), nullable=False)
    client_id = Column("cliente_id", Integer, ForeignKey("clientes.usuario_id"), nullable=False)
    worker_id = Column("funcionario_id", Integer, ForeignKey("funcionarios.usuario_id"), nullable=False)

    store = relationship("Store", back_populates="appointments")
    client = relationship("ClientModel", back_populates="appointments")
    worker = relationship("EmployeeModel", back_populates="appointments")
    items = relationship("AppointmentService", back_populates="appointment", cascade="all, delete-orphan")


class AppointmentService(Base):
    __tablename__ = "atendimento_servicos"

    appointment_id = Column(
        "atendimento_id",
        Integer,
        ForeignKey("atendimentos.id", ondelete="CASCADE"),
        primary_key=True,
    )
    service_id = Column("servico_id", Integer, ForeignKey("servicos.id", ondelete="CASCADE"), primary_key=True)
    charged_value = Column("valor_cobrado", Numeric(10, 2), nullable=False)
    order_date = Column("data_pedido", DateTime, nullable=False, default=datetime.utcnow)
    delivery_date = Column("data_entrega", DateTime)
    observations = Column("observacoes", String(500))

    appointment = relationship("Appointment", back_populates="items")
    service = relationship("Service", back_populates="appointment_links")
