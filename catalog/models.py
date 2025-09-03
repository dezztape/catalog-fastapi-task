from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    image = Column(String, nullable=True)
    category = Column(String, index=True, nullable=True)

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    cart_id = Column(Integer, ForeignKey("carts.id"))
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)