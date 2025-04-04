from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategorySchema,
)
from app.crud import category as category_crud

router = APIRouter()


@router.get("/", response_model=list[CategorySchema])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await category_crud.get_all_categories(db)


@router.get("/{category_id}", response_model=CategorySchema)
async def get(category_id: str, db: AsyncSession = Depends(get_db)):
    return await category_crud.get_category_by_id(category_id, db)


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await category_crud.create_category(category, db)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update(
    category_id: str,
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    return await category_crud.update_category(category_id, category, db)


@router.delete("/{category_id}", status_code=204)
async def delete(category_id: str, db: AsyncSession = Depends(get_db)):
    await category_crud.delete_category(category_id, db)
