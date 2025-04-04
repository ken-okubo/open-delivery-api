from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.item import ItemCreate, ItemSchema
from app.crud import item as item_crud

router = APIRouter()


@router.get("/", response_model=list[ItemSchema])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await item_crud.get_all_items(db)


@router.get("/{item_id}", response_model=ItemSchema)
async def get(item_id: str, db: AsyncSession = Depends(get_db)):
    return await item_crud.get_item_by_id(item_id, db)


@router.post("/", response_model=ItemSchema, status_code=201)
async def create(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await item_crud.create_item(item, db)


@router.put("/item/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: str, item: ItemCreate, db: AsyncSession = Depends(get_db)
):
    return await item_crud.update_item(item_id, item, db)


@router.delete("/item/{item_id}", status_code=204)
async def delete_item(item_id: str, db: AsyncSession = Depends(get_db)):
    await item_crud.delete_item(item_id, db)
