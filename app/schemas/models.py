from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    
    pets = relationship("Pet", back_populates="category")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)

    pets = relationship("Pet", back_populates="tag")

class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    photoUrls = Column(String, nullable=True)
    status = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    category = relationship("Category", back_populates="pets")
    tag = relationship("Tag", back_populates="pets")
    owner = relationship("UserModel", back_populates="pets")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    petId = Column(Integer, ForeignKey("pets.id"))
    quantity = Column(Integer, nullable=True)
    shipDate = Column(DateTime, nullable=True)
    status = Column(String, default="placed")
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    owner = relationship("UserModel", back_populates="orders")
    

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password_hash = Column(String)
    phone = Column(String, nullable=True)
    user_active = Column(Boolean, nullable=False, default=True)
    role = Column(String,default="user")

    pets = relationship("Pet", back_populates="owner")
    orders = relationship("Order", back_populates="owner")
