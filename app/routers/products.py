from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from typing import Annotated, List, Optional
from slugify import slugify

from app.backend.db_depends import get_db
from app.models import Product, Category
from app.schemas import (
    CreateProduct, 
    UpdateProduct, 
    ProductResponse, 
    MessageResponse,
    ErrorResponse
)

router = APIRouter(prefix='/products', tags=['Товары'])


@router.get(
    '/',
    response_model=List[ProductResponse],
    summary="Получить все активные товары",
    description="Возвращает список всех активных товаров с остатком на складе"
)
async def get_all_products(
    db: Annotated[Session, Depends(get_db)],
    limit: Optional[int] = Query(100, ge=1, le=1000, description="Максимальное количество товаров"),
        offset: Optional[int] = Query(0, ge=0, description="Смещение для пагинации")
) -> List[ProductResponse]:
    """
    Получить все активные товары с пагинацией
    :param db: Session - Сессия базы данных
    :param limit: int - Максимальное количество товаров на странице
    :param offset: int - Смещение для пагинации
    :return: List[ProductResponse] - Список товаров
    Если товаров не найдено, возвращает пустой список
    Если произошла ошибка, возвращает 500
    """
    try:
        products = db.scalars(
            select(Product)
            .where(Product.is_active == True, Product.stock > 0)
            .limit(limit)
            .offset(offset)
        ).all()
        
        if not products:
            return []
            
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении товаров: {str(e)}"
        )


@router.post(
    '/create',
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый товар",
    description="Создает новый товар в системе"
)
async def create_product(db: Annotated[Session, Depends(get_db)], create_product_data: CreateProduct) -> MessageResponse:
    """
    Создать новый товар
    :param db: Session - Сессия базы данных
    :param create_product_data: CreateProduct - Данные для создания товара
    :return: MessageResponse - Сообщение об успешном создании
    Если категория не найдена, возвращает 404
    Если товар с таким названием уже существует, возвращает 400
    """
    try:
        # Проверяем существование категории
        category = db.scalar(select(Category).where(Category.id == create_product_data.category))
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        
        # Проверяем уникальность slug
        slug = slugify(create_product_data.name)
        existing_product = db.scalar(select(Product).where(Product.slug == slug))
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Товар с таким названием уже существует"
            )
        
        # Создаем товар
        db.execute(
            insert(Product).values(
                name=create_product_data.name,
                description=create_product_data.description,
                price=create_product_data.price,
                image_url=str(create_product_data.image_url),
                stock=create_product_data.stock,
                category_id=create_product_data.category,
                rating=0.0,
                slug=slug
            )
        )
        db.commit()
        
        return MessageResponse(
            status_code=status.HTTP_201_CREATED,
            message="Товар успешно создан",
            transaction="Successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании товара: {str(e)}"
        )


@router.get(
    '/category/{category_slug}',
    response_model=List[ProductResponse],
    summary="Получить товары по категории",
    description="Возвращает все товары указанной категории и её подкатегорий"
)
async def get_products_by_category(db: Annotated[Session, Depends(get_db)], category_slug: str) -> List[ProductResponse]:
    """
    Получить товары по категории (включая подкатегории)
    :param db: Session - Сессия базы данных
    :param category_slug: str - Слуг категории
    :return: List[ProductResponse] - Список товаров
    Если категория не найдена, возвращает пустой список
    Если товары не найдены, возвращает пустой список
    Если произошла ошибка, возвращает 500
    """
    try:
        # Находим категорию
        category = db.scalar(select(Category).where(Category.slug == category_slug))
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        
        # Получаем все подкатегории
        subcategories = db.scalars(
            select(Category).where(Category.parent_id == category.id)
        ).all()
        
        # Собираем все ID категорий
        category_ids = [category.id] + [sub.id for sub in subcategories]
        
        # Получаем товары
        products = db.scalars(
            select(Product).where(
                Product.category_id.in_(category_ids),
                Product.is_active == True,
                Product.stock > 0
            )
        ).all()
        return products
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении товаров: {str(e)}"
        )


@router.get(
    '/detail/{product_slug}',
    response_model=ProductResponse,
    summary="Получить детали товара",
    description="Возвращает подробную информацию о товаре по его slug"
)
async def get_product_detail(db: Annotated[Session, Depends(get_db)], product_slug: str) -> ProductResponse:
    """
    Получить детальную информацию о товаре
    :param db: Session - Сессия базы данных
    :param product_slug: str - Слуг товара
    :return: ProductResponse - Детали товара
    """
    try:
        product = db.scalar(
            select(Product).where(
                Product.slug == product_slug,
                Product.is_active == True
            )
        )
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении товара: {str(e)}"
        )


@router.put(
    '/detail/{product_slug}',
    response_model=MessageResponse,
    summary="Обновить товар",
    description="Обновляет информацию о товаре"
)
async def update_product(db: Annotated[Session, Depends(get_db)], product_slug: str, update_data: UpdateProduct) -> MessageResponse:
    """
    Обновить товар
    :param db: Session - Сессия базы данных
    :param product_slug: str - Слуг товара
    :param update_data: UpdateProduct - Данные для обновления
    :return: MessageResponse - Сообщение об успешном обновлении
    """
    try:
        # Проверяем существование товара
        product = db.scalar(select(Product).where(Product.slug == product_slug))
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )
        
        # Подготавливаем данные для обновления
        update_values = {}
        
        if update_data.name is not None:
            update_values['name'] = update_data.name
            update_values['slug'] = slugify(update_data.name)
        
        if update_data.description is not None:
            update_values['description'] = update_data.description
        
        if update_data.price is not None:
            update_values['price'] = update_data.price
        
        if update_data.image_url is not None:
            update_values['image_url'] = str(update_data.image_url)
        
        if update_data.stock is not None:
            update_values['stock'] = update_data.stock
        
        if update_data.category is not None:
            # Проверяем существование категории
            category = db.scalar(select(Category).where(Category.id == update_data.category))
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категория не найдена"
                )
            update_values['category_id'] = update_data.category
        if not update_values:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нет данных для обновления"
            )
        # Обновляем товар
        db.execute(
            update(Product)
            .where(Product.slug == product_slug)
            .values(**update_values)
        )
        db.commit()
        return MessageResponse(
            status_code=status.HTTP_200_OK,
            message="Товар успешно обновлен",
            transaction="Product update is successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении товара: {str(e)}"
        )


@router.delete(
    '/delete/{product_id}',
    response_model=MessageResponse,
    summary="Удалить товар",
    description="Мягкое удаление товара (устанавливает is_active=False)"
)
async def delete_product(db: Annotated[Session, Depends(get_db)], product_id: int) -> MessageResponse:
    """
    Мягкое удаление товара
    :param db: Session - Сессия базы данных
    :param product_id: int - ID товара
    :return: MessageResponse - Сообщение об успешном удалении
    """
    try:
        # Проверяем существование товара
        product = db.scalar(select(Product).where(Product.id == product_id))
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )
        
        # Мягкое удаление
        db.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(is_active=False)
        )
        db.commit()
        
        return MessageResponse(
            status_code=status.HTTP_200_OK,
            message="Товар успешно удален",
            transaction="Product delete is successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении товара: {str(e)}"
        )
