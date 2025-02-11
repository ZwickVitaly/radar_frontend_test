from sqlalchemy import Column, Integer, String, DateTime, func, Float, ARRAY

from db import Base


class User(Base):
    __tablename__ = "test_user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, server_default=func.now())
    brand = Column(String(100), nullable=True)
    weight = Column(Float, nullable=True)
    dimensions = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    images = Column(ARRAY(String), nullable=True, default=list())
    seller_id = Column(Integer, nullable=False)
    warranty_period = Column(Integer, nullable=True)
    return_policy = Column(String(200), nullable=True)
    barcode = Column(String(50), unique=True, nullable=False)