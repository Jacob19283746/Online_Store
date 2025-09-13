from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Category(Base):
    """
    Модель категории
    
    Attributes:
        id: Уникальный идентификатор категории
        name: Название категории
        slug: URL-дружественное название
        is_active: Активна ли категория
        parent_id: ID родительской категории (для иерархии)
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    products = relationship("Product", back_populates="category")
    
    # Самосвязь для иерархии
    parent = relationship("Category", remote_side=[id], backref="children")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', parent_id={self.parent_id})>"
