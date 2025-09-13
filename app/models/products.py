from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Product(Base):
    """
    Модель товара
    
    Attributes:
        id: Уникальный идентификатор товара
        name: Название товара
        slug: URL-дружественное название
        description: Описание товара
        price: Цена в копейках
        image_url: URL изображения товара
        stock: Количество на складе
        category_id: ID категории
        rating: Рейтинг товара (0.0 - 5.0)
        is_active: Активен ли товар
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    __tablename__ = 'products'
    __table_args__ = {'keep_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(2000), nullable=False)
    price = Column(Integer, nullable=False)  # Цена в копейках
    image_url = Column(String(500), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
