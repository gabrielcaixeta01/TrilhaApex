from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

pet_tags = Table(
    "pet_tags",
    Base.metadata,
    Column("pet_id", Integer, ForeignKey("pets.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    
    pets = relationship("Pet", back_populates="category", cascade="all, delete-orphan")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)

    pets = relationship("Pet", secondary=pet_tags, back_populates="tags")

class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    photoUrls = Column(String, nullable=True)
    status = Column(String, default="available", nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    category = relationship("Category", back_populates="pets")
    tags = relationship("Tag", secondary=pet_tags, back_populates="pets")
    owner = relationship("UserModel", back_populates="pets")
    orders = relationship("Order", back_populates="pet", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    petId = Column(Integer, ForeignKey("pets.id"))
    quantity = Column(Integer, default=1)
    shipDate = Column(DateTime)
    status = Column(String, default="placed")
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="orders")
    pet = relationship("Pet", back_populates="orders")
    

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    password_hash = Column(String)
    phone = Column(String, nullable=True, unique=True)
    user_active = Column(Boolean, default=True)
    role = Column(String,default="user")

    pets = relationship("Pet", back_populates="owner")
    orders = relationship("Order", back_populates="owner")
