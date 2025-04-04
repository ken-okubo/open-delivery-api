from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.item_offer import ItemOffer
from app.schemas.item_offer import ItemOfferCreate, ItemOfferSchema
from app.utils.serializers import make_json_serializable


async def get_all_item_offers(db: AsyncSession):
    result = await db.execute(select(ItemOffer))
    offers = result.scalars().all()
    return [ItemOfferSchema.model_validate(offer) for offer in offers]


async def get_item_offer_by_id(item_offer_id: str, db: AsyncSession):
    result = await db.execute(
        select(ItemOffer).where(ItemOffer.id == item_offer_id)
    )
    offer = result.scalar_one_or_none()
    if not offer:
        raise HTTPException(status_code=404, detail="ItemOffer not found")
    return ItemOfferSchema.model_validate(offer)


async def create_item_offer(item_offer: ItemOfferCreate, db: AsyncSession):
    item_offer_data = item_offer.model_dump()

    if item_offer_data.get("price"):
        item_offer_data["price"] = make_json_serializable(
            item_offer_data["price"]
        )

    db_offer = ItemOffer(**item_offer_data)
    db.add(db_offer)
    await db.commit()
    await db.refresh(db_offer)
    return ItemOfferSchema.model_validate(db_offer)


async def update_item_offer(
    item_offer_id: str, item_offer: ItemOfferCreate, db: AsyncSession
):
    result = await db.execute(
        select(ItemOffer).where(ItemOffer.id == item_offer_id)
    )
    db_offer = result.scalar_one_or_none()

    if not db_offer:
        raise HTTPException(status_code=404, detail="ItemOffer not found")

    update_data = item_offer.model_dump(exclude_unset=True)

    if "price" in update_data:
        update_data["price"] = make_json_serializable(update_data["price"])

    for field, value in update_data.items():
        setattr(db_offer, field, value)

    await db.commit()
    await db.refresh(db_offer)
    return ItemOfferSchema.model_validate(db_offer)


async def delete_item_offer(item_offer_id: str, db: AsyncSession):
    result = await db.execute(
        select(ItemOffer).where(ItemOffer.id == item_offer_id)
    )
    db_offer = result.scalar_one_or_none()

    if not db_offer:
        raise HTTPException(status_code=404, detail="ItemOffer not found")

    await db.delete(db_offer)
    await db.commit()
