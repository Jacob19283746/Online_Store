from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional
from datetime import datetime


class CreateProduct(BaseModel):
    """Схема для создания нового товара"""
    name: str = Field(..., min_length=1, max_length=255, description="Название товара")
    description: str = Field(..., min_length=1, max_length=2000, description="Описание товара")
    price: int = Field(..., gt=0, description="Цена в копейках")
    image_url: HttpUrl = Field(..., description="URL изображения товара")
    stock: int = Field(..., ge=0, description="Количество на складе")
    category: int = Field(..., gt=0, description="ID категории")

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Название товара не может быть пустым')
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError('Описание товара не может быть пустым')
        return v.strip()


class UpdateProduct(BaseModel):
    """Схема для обновления товара"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Название товара")
    description: Optional[str] = Field(None, min_length=1, max_length=2000, description="Описание товара")
    price: Optional[int] = Field(None, gt=0, description="Цена в копейках")
    image_url: Optional[HttpUrl] = Field(None, description="URL изображения товара")
    stock: Optional[int] = Field(None, ge=0, description="Количество на складе")
    category: Optional[int] = Field(None, gt=0, description="ID категории")

    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Название товара не может быть пустым')
        return v.strip() if v else v

    @validator('description')
    def validate_description(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Описание товара не может быть пустым')
        return v.strip() if v else v


class ProductResponse(BaseModel):
    """Схема для ответа с информацией о товаре"""
    id: int
    name: str
    slug: str
    description: str
    price: int
    image_url: str
    stock: int
    category_id: int
    rating: Optional[float]
    is_active: bool

    class Config:
        from_attributes = True


class CreateCategory(BaseModel):
    """Схема для создания новой категории"""
    name: str = Field(..., min_length=1, max_length=255, description="Название категории")
    parent_id: Optional[int] = Field(None, gt=0, description="ID родительской категории")

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Название категории не может быть пустым')
        return v.strip()


class UpdateCategory(BaseModel):
    """Схема для обновления категории"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Название категории")
    parent_id: Optional[int] = Field(None, gt=0, description="ID родительской категории")

    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Название категории не может быть пустым')
        return v.strip() if v else v


class CategoryResponse(BaseModel):
    """Схема для ответа с информацией о категории"""
    id: int
    name: str
    slug: str
    is_active: bool
    parent_id: Optional[int]

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Схема для стандартных ответов API"""
    status_code: int
    message: str
    transaction: str


class ErrorResponse(BaseModel):
    """Схема для ответов об ошибках"""
    detail: str
    status_code: int
