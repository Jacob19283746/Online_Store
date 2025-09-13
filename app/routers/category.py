from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from typing import Annotated, List, Optional
from slugify import slugify

from app.backend.db_depends import get_db
from app.models import Category
from app.schemas import (
    CreateCategory, 
    UpdateCategory, 
    CategoryResponse, 
    MessageResponse
)

router = APIRouter(prefix='/category', tags=['Категории'])


@router.post(
    '/create',
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую категорию",
    description="Создает новую категорию в системе"
)
async def create_category(
    db: Annotated[Session, Depends(get_db)], 
    create_category_data: CreateCategory
) -> MessageResponse:
    """
    Создать новую категорию
    """
    try:
        # Проверяем уникальность slug
        slug = slugify(create_category_data.name)
        existing_category = db.scalar(select(Category).where(Category.slug == slug))
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким названием уже существует"
            )
        
        # Если указан parent_id, проверяем его существование
        if create_category_data.parent_id:
            parent_category = db.scalar(
                select(Category).where(Category.id == create_category_data.parent_id)
            )
            if not parent_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Родительская категория не найдена"
                )
        
        # Создаем категорию
        db.execute(
            insert(Category).values(
                name=create_category_data.name,
                parent_id=create_category_data.parent_id,
                slug=slug
            )
        )
        db.commit()
        
        return MessageResponse(
            status_code=status.HTTP_201_CREATED,
            message="Категория успешно создана",
            transaction="Successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании категории: {str(e)}"
        )


@router.get(
    '/all_categories',
    response_model=List[CategoryResponse],
    summary="Получить все активные категории",
    description="Возвращает список всех активных категорий"
)
async def get_all_categories(
    db: Annotated[Session, Depends(get_db)],
    include_inactive: bool = Query(False, description="Включить неактивные категории")
) -> List[CategoryResponse]:
    """
    Получить все категории
    """
    try:
        query = select(Category)
        
        if not include_inactive:
            query = query.where(Category.is_active == True)
        
        categories = db.scalars(query).all()
        return categories
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении категорий: {str(e)}"
        )


@router.get(
    '/{category_id}',
    response_model=CategoryResponse,
    summary="Получить категорию по ID",
    description="Возвращает информацию о конкретной категории"
)
async def get_category_by_id(
    db: Annotated[Session, Depends(get_db)], 
    category_id: int
) -> CategoryResponse:
    """
    Получить категорию по ID
    """
    try:
        category = db.scalar(select(Category).where(Category.id == category_id))
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        return category
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении категории: {str(e)}"
        )


@router.get(
    '/slug/{category_slug}',
    response_model=CategoryResponse,
    summary="Получить категорию по slug",
    description="Возвращает информацию о категории по её slug"
)
async def get_category_by_slug(
    db: Annotated[Session, Depends(get_db)], 
    category_slug: str
) -> CategoryResponse:
    """
    Получить категорию по slug
    """
    try:
        category = db.scalar(select(Category).where(Category.slug == category_slug))
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        return category
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении категории: {str(e)}"
        )


@router.put(
    '/update/{category_id}',
    response_model=MessageResponse,
    summary="Обновить категорию",
    description="Обновляет информацию о категории"
)
async def update_category(
    db: Annotated[Session, Depends(get_db)], 
    category_id: int, 
    update_data: UpdateCategory
) -> MessageResponse:
    """
    Обновить категорию
    """
    try:
        # Проверяем существование категории
        category = db.scalar(select(Category).where(Category.id == category_id))
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        
        # Подготавливаем данные для обновления
        update_values = {}
        
        if update_data.name is not None:
            # Проверяем уникальность нового slug
            new_slug = slugify(update_data.name)
            existing_category = db.scalar(
                select(Category).where(Category.slug == new_slug, Category.id != category_id)
            )
            if existing_category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Категория с таким названием уже существует"
                )
            update_values['name'] = update_data.name
            update_values['slug'] = new_slug
        
        if update_data.parent_id is not None:
            # Проверяем существование родительской категории
            if update_data.parent_id == category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Категория не может быть родителем самой себе"
                )
            
            parent_category = db.scalar(
                select(Category).where(Category.id == update_data.parent_id)
            )
            if not parent_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Родительская категория не найдена"
                )
            update_values['parent_id'] = update_data.parent_id
        
        if not update_values:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нет данных для обновления"
            )
        
        # Обновляем категорию
        db.execute(
            update(Category)
            .where(Category.id == category_id)
            .values(**update_values)
        )
        db.commit()
        
        return MessageResponse(
            status_code=status.HTTP_200_OK,
            message="Категория успешно обновлена",
            transaction="Category update is successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении категории: {str(e)}"
        )


@router.delete(
    '/delete/{category_id}',
    response_model=MessageResponse,
    summary="Удалить категорию",
    description="Мягкое удаление категории (устанавливает is_active=False)"
)
async def delete_category(
    db: Annotated[Session, Depends(get_db)], 
    category_id: int
) -> MessageResponse:
    """
    Мягкое удаление категории
    """
    try:
        # Проверяем существование категории
        category = db.scalar(select(Category).where(Category.id == category_id))
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        
        # Проверяем, есть ли подкатегории
        subcategories = db.scalars(
            select(Category).where(Category.parent_id == category_id, Category.is_active == True)
        ).all()
        
        if subcategories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нельзя удалить категорию, у которой есть активные подкатегории"
            )
        
        # Мягкое удаление
        db.execute(
            update(Category)
            .where(Category.id == category_id)
            .values(is_active=False)
        )
        db.commit()
        
        return MessageResponse(
            status_code=status.HTTP_200_OK,
            message="Категория успешно удалена",
            transaction="Category delete is successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении категории: {str(e)}"
        )
