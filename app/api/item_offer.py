from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.item_offer import ItemOfferCreate, ItemOfferResponse
from app.crud import item_offer as crud

router = APIRouter()


@router.post("/", response_model=ItemOfferResponse, status_code=201)
async def create(data: ItemOfferCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item_offer(data, db)


@router.get("/{offer_id}", response_model=ItemOfferResponse)
async def get(offer_id: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_item_offer_by_id(offer_id, db)


@router.get("/", response_model=list[ItemOfferResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_item_offers(db)


@router.put("/{offer_id}", response_model=ItemOfferResponse)
async def update(
    offer_id: str, data: ItemOfferCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_item_offer(offer_id, data, db)


@router.delete("/{offer_id}", status_code=204)
async def delete(offer_id: str, db: AsyncSession = Depends(get_db)):
    await crud.delete_item_offer(offer_id, db)
